#!/usr/bin/env python3
"""Regression checks for the generated command-logger hook."""

from __future__ import annotations

import json
import os
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CATALOG = Path(__file__).resolve().parent.parent
BUNDLE = CATALOG / "development-tools" / "command-logger"
LOGGER_SOURCE = Path("development-tools/command-logger.json")
LEGACY_COMMAND = (
    'echo "[$(date)] Tool: $CLAUDE_TOOL_NAME | File: $CLAUDE_TOOL_FILE_PATH"'
    " >> ~/.codex/command-log.txt"
)


def hook_command(bundle):
    config = json.loads((bundle / "hooks.json").read_text())
    return config["hooks"]["PreToolUse"][0]["hooks"][0]["command"]


class CommandLoggerGenerationTest(unittest.TestCase):
    def test_generator_reproduces_the_checked_in_hook(self):
        generator = runpy.run_path(str(CATALOG / "generate.py"))
        rewrite = generator["rewrite_command"]
        with tempfile.TemporaryDirectory(prefix="logger-generation-") as temp:
            generated = Path(temp) / "hook.sh"
            generator["write_wrapper_script"](generated, rewrite(LEGACY_COMMAND, LOGGER_SOURCE), BUNDLE)
            self.assertEqual(generated.read_text(), (BUNDLE / hook_command(BUNDLE)).read_text())
        self.assertEqual(rewrite(LEGACY_COMMAND, Path("other.json")), generator["sanitize_hook_text"](LEGACY_COMMAND))


@unittest.skipUnless(shutil.which("jq"), "The hook wrapper requires jq")
class CommandLoggerHookTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="command-logger-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.home = root / "fake-home"
        self.log = self.home / ".codex" / "command-log.txt"
        self.log.parent.mkdir(parents=True)
        self.workspace = root / "workspace"
        self.workspace.mkdir()
        subprocess.run(
            [sys.executable, str(CATALOG / "install-bundle.py"), str(BUNDLE), str(self.workspace)],
            check=True,
            capture_output=True,
            timeout=30,
        )

    def invoke(self, payload, **extra_env):
        env = os.environ.copy()
        for name in ("BASH_ENV", "ENV", "CODEX_HOME", "CLAUDE_TOOL_NAME", "CLAUDE_TOOL_FILE_PATH"):
            env.pop(name, None)
        env.update(HOME=str(self.home), **extra_env)
        result = subprocess.run(
            ["bash", "-c", hook_command(self.workspace / ".codex")],
            cwd=self.workspace,
            input=payload,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.log.read_text().splitlines()[-1]

    def test_codex_uses_the_tool_name_and_file_path(self):
        line = self.invoke(json.dumps({
            "hook_event_name": "PreToolUse", "tool_name": "Write",
            "tool_input": {"file_path": "/tmp/example.txt"},
        }))
        self.assertRegex(line, r"^\[.+\] Tool: Write \| File: /tmp/example\.txt$")

    def test_missing_codex_path_does_not_reuse_claude_path_or_log_the_command(self):
        line = self.invoke(json.dumps({
            "hook_event_name": "PreToolUse", "tool_name": "Bash",
            "tool_input": {"command": "echo command-data-stays-out"},
        }), CLAUDE_TOOL_FILE_PATH="/tmp/stale-claude.txt")
        self.assertRegex(line, r"^\[.+\] Tool: Bash \| File: $")

    def test_legacy_fields_are_used_without_a_codex_event(self):
        line = self.invoke("", CLAUDE_TOOL_NAME="Edit", CLAUDE_TOOL_FILE_PATH="/tmp/claude.txt")
        self.assertRegex(line, r"^\[.+\] Tool: Edit \| File: /tmp/claude\.txt$")

    def test_empty_codex_event_fields_stay_empty(self):
        line = self.invoke('{"hook_event_name":"PreToolUse"}', CLAUDE_TOOL_NAME="Edit")
        self.assertRegex(line, r"^\[.+\] Tool:  \| File: $")


if __name__ == "__main__":
    unittest.main()
