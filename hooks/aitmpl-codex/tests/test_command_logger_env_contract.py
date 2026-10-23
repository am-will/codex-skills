"""Static contract check for the generated command-logger hook.

This intentionally reads hook files as text and never executes or installs them.
"""
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]
LOGGER = (
    REPO_ROOT
    / "hooks/aitmpl-codex/development-tools/command-logger/.codex/hooks/"
    "development-tools-command-logger-pretooluse-pretooluse-1-1.sh"
)
WRAPPER = REPO_ROOT / "hooks/aitmpl-codex/_shared/run-with-hook-env.sh"


class CommandLoggerEnvironmentContractTest(unittest.TestCase):
    def test_logger_reads_fields_exported_by_codex_adapter(self):
        logger = LOGGER.read_text(encoding="utf-8")
        wrapper = WRAPPER.read_text(encoding="utf-8")

        self.assertIn('"${CODEX_TOOL_NAME:-}"', logger)
        self.assertIn('"${CODEX_TOOL_FILE_PATH:-}"', logger)
        self.assertNotIn("CLAUDE_TOOL_NAME", logger)
        self.assertNotIn("CLAUDE_TOOL_FILE_PATH", logger)
        self.assertIn("export CODEX_TOOL_NAME=", wrapper)
        self.assertIn("export CODEX_TOOL_FILE_PATH=", wrapper)


if __name__ == "__main__":
    unittest.main()
