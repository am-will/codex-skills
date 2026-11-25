#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if [[ -n "${CODEX_TOOL_NAME:-}${CODEX_TOOL_FILE_PATH:-}" ]]; then
  tool_name="${CODEX_TOOL_NAME:-}"
  tool_file="${CODEX_TOOL_FILE_PATH:-}"
else
  tool_name="${CLAUDE_TOOL_NAME:-}"
  tool_file="${CLAUDE_TOOL_FILE_PATH:-}"
fi
log_dir=~/.codex
log_dir="${CODEX_HOME:-$log_dir}"
mkdir -p "$log_dir"
printf '[%s] Tool: %s | File: %s\n' "$(date)" "$tool_name" "$tool_file" >> "$log_dir/command-log.txt"
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
