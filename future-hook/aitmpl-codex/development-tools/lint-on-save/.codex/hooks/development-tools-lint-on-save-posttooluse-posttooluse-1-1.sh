#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if [[ "$CLAUDE_TOOL_FILE_PATH" == *.js || "$CLAUDE_TOOL_FILE_PATH" == *.ts || "$CLAUDE_TOOL_FILE_PATH" == *.jsx || "$CLAUDE_TOOL_FILE_PATH" == *.tsx ]]; then npx eslint "$CLAUDE_TOOL_FILE_PATH" --fix 2>/dev/null || true; elif [[ "$CLAUDE_TOOL_FILE_PATH" == *.py ]]; then pylint "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true; elif [[ "$CLAUDE_TOOL_FILE_PATH" == *.rb ]]; then rubocop "$CLAUDE_TOOL_FILE_PATH" --auto-correct 2>/dev/null || true; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
