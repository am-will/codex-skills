#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if [[ "${CODEX_HOOK_EVENT_NAME:-}" == PreToolUse || -n "${CODEX_TOOL_NAME:-}${CODEX_TOOL_FILE_PATH:-}" ]]; then
  logger_tool_name="${CODEX_TOOL_NAME:-}"
  logger_tool_file="${CODEX_TOOL_FILE_PATH:-}"
else
  logger_tool_name="${CLAUDE_TOOL_NAME:-}"
  logger_tool_file="${CLAUDE_TOOL_FILE_PATH:-}"
fi
echo "[$(date)] Tool: ${logger_tool_name} | File: ${logger_tool_file}" >> ~/.codex/command-log.txt
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
