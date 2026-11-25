#!/usr/bin/env python3
"""Focused regression tests for the development-tools/command-logger hook bundle."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
CATALOG_ROOT = TOOLS_DIR.parent
INSTALL_SCRIPT = CATALOG_ROOT / "install-bundle.py"
BUNDLE_DIR = CATALOG_ROOT / "development-tools" / "command-logger"

JQ_SHIM_SOURCE = """#!/usr/bin/env python3
import json
import sys

args = sys.argv[1:]
raw = False
if "-r" in args:
    raw = True
    args.remove("-r")
if not args:
    sys.exit(2)
expr = args[0]
text = sys.stdin.read().strip()
if not text:
    sys.exit(0)
try:
    data = json.loads(text)
except Exception:
    sys.exit(5)


def emit(val):
    if val is None:
        return
    if isinstance(val, (dict, list)):
        print(json.dumps(val, separators=(",", ":")))
    elif isinstance(val, bool):
        print("true" if val else "false")
    else:
        print(val if raw else json.dumps(val))


if expr == ".tool_input | type? // empty":
    if isinstance(data, dict) and "tool_input" in data and data["tool_input"] is not None:
        v = data["tool_input"]
        t = {
            dict: "object",
            list: "array",
            str: "string",
            bool: "boolean",
            int: "number",
            float: "number",
        }.get(type(v), "null")
        emit(t)
elif expr == "try fromjson catch empty":
    if isinstance(data, str):
        try:
            emit(json.loads(data))
        except Exception:
            pass
elif expr.startswith("try (.file_path"):
    if isinstance(data, dict):
        params = data.get("params") if isinstance(data.get("params"), dict) else {}
        for v in (
            data.get("file_path"),
            data.get("path"),
            data.get("destination"),
            params.get("file_path"),
            params.get("path"),
        ):
            if v not in (None, ""):
                emit(v)
                break
elif expr.startswith("try (.command"):
    if isinstance(data, dict):
        cmd = data.get("command")
        if (
            cmd in (None, "")
            and isinstance(data.get("params"), dict)
            and isinstance(data["params"].get("command"), list)
        ):
            cmd = " ".join(str(x) for x in data["params"]["command"])
        if cmd not in (None, ""):
            emit(cmd)
elif expr.endswith(" // empty"):
    path = expr[: -len(" // empty")].strip()
    cur = data
    for part in path.lstrip(".").split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            cur = None
            break
    if cur not in (None, ""):
        emit(cur)
else:
    sys.exit(1)
"""

LOG_LINE_RE = re.compile(r"^\[(?P<ts>.+)\] Tool: (?P<tool>.*) \| File: (?P<file>.*)$")


class CommandLoggerHookTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(prefix="command-logger-test-")
        self.root = Path(self._tmpdir.name)
        self.workspace = self.root / "workspace"
        self.fake_home = self.root / "fake-home"
        self.workspace.mkdir()
        self.fake_home.mkdir()

        subprocess.run(
            ["python3", str(INSTALL_SCRIPT), str(BUNDLE_DIR), str(self.workspace)],
            check=True,
            capture_output=True,
            text=True,
        )

        hooks_cfg = json.loads((self.workspace / ".codex" / "hooks.json").read_text())
        self.hook_command = hooks_cfg["hooks"]["PreToolUse"][0]["hooks"][0]["command"]

        self.shim_bin: Path | None = None
        if shutil.which("jq") is None:
            self.shim_bin = self.root / "shim-bin"
            self.shim_bin.mkdir()
            jq_path = self.shim_bin / "jq"
            jq_path.write_text(JQ_SHIM_SOURCE)
            jq_path.chmod(jq_path.stat().st_mode | stat.S_IXUSR)

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def run_hook(
        self,
        stdin_payload: str,
        extra_env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        for key in (
            "CODEX_HOME",
            "CODEX_TOOL_NAME",
            "CODEX_TOOL_FILE_PATH",
            "CLAUDE_TOOL_NAME",
            "CLAUDE_TOOL_FILE_PATH",
        ):
            env.pop(key, None)
        env["HOME"] = str(self.fake_home)
        if self.shim_bin is not None:
            env["PATH"] = f"{self.shim_bin}:{env.get('PATH', '')}"
        if extra_env:
            env.update(extra_env)

        return subprocess.run(
            ["bash", "-lc", self.hook_command],
            input=stdin_payload,
            cwd=self.workspace,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def parse_log_lines(self, log_path: Path) -> list[tuple[str, str, str]]:
        self.assertTrue(log_path.is_file(), f"missing log file: {log_path}")
        raw_lines = log_path.read_text().splitlines()
        parsed: list[tuple[str, str, str]] = []
        for line in raw_lines:
            match = LOG_LINE_RE.match(line)
            self.assertIsNotNone(match, f"unexpected log line format: {line!r}")
            assert match is not None
            parsed.append((match.group("ts"), match.group("tool"), match.group("file")))
        return parsed

    def test_codex_pretooluse_logs_exact_tool_and_file_path(self) -> None:
        payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": "/tmp/example.txt"},
            }
        )
        proc = self.run_hook(payload)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)

        log_path = self.fake_home / ".codex" / "command-log.txt"
        entries = self.parse_log_lines(log_path)
        self.assertEqual(len(entries), 1)
        ts, tool, file_path = entries[0]
        self.assertTrue(ts.strip())
        self.assertEqual(tool, "Write")
        self.assertEqual(file_path, "/tmp/example.txt")

    def test_codex_pretooluse_missing_file_path_is_safe_and_isolated(self) -> None:
        payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "echo secret-command-not-logged"},
            }
        )
        proc = self.run_hook(
            payload,
            extra_env={"CLAUDE_TOOL_FILE_PATH": "/tmp/stale-claude-path.txt"},
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)

        log_path = self.fake_home / ".codex" / "command-log.txt"
        entries = self.parse_log_lines(log_path)
        self.assertEqual(len(entries), 1)
        _, tool, file_path = entries[0]
        self.assertEqual(tool, "Bash")
        self.assertEqual(file_path, "")
        self.assertNotIn("secret-command-not-logged", log_path.read_text())

    def test_claude_env_integration_fallback(self) -> None:
        proc = self.run_hook(
            "",
            extra_env={
                "CLAUDE_TOOL_NAME": "Edit",
                "CLAUDE_TOOL_FILE_PATH": "/tmp/claude-target.txt",
            },
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)

        log_path = self.fake_home / ".codex" / "command-log.txt"
        entries = self.parse_log_lines(log_path)
        self.assertEqual(len(entries), 1)
        _, tool, file_path = entries[0]
        self.assertEqual(tool, "Edit")
        self.assertEqual(file_path, "/tmp/claude-target.txt")

    def test_empty_input_and_empty_json_preserve_log_format(self) -> None:
        proc_empty = self.run_hook("")
        self.assertEqual(proc_empty.returncode, 0, msg=proc_empty.stderr)

        proc_obj = self.run_hook("{}")
        self.assertEqual(proc_obj.returncode, 0, msg=proc_obj.stderr)

        log_path = self.fake_home / ".codex" / "command-log.txt"
        entries = self.parse_log_lines(log_path)
        self.assertEqual(len(entries), 2)
        for ts, tool, file_path in entries:
            self.assertTrue(ts.strip())
            self.assertEqual(tool, "")
            self.assertEqual(file_path, "")

    def test_codex_home_override(self) -> None:
        custom_codex_home = self.root / "custom-codex-home"
        payload = json.dumps(
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/tmp/readme.md"},
            }
        )
        proc = self.run_hook(payload, extra_env={"CODEX_HOME": str(custom_codex_home)})
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)

        default_log = self.fake_home / ".codex" / "command-log.txt"
        custom_log = custom_codex_home / "command-log.txt"
        self.assertFalse(default_log.exists())
        entries = self.parse_log_lines(custom_log)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][1], "Read")
        self.assertEqual(entries[0][2], "/tmp/readme.md")


if __name__ == "__main__":
    unittest.main()
