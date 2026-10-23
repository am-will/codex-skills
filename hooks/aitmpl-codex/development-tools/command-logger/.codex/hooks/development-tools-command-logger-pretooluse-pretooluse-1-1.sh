#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
printf '[%s] Tool: %s | File: %s\n' "$(date)" "${CODEX_TOOL_NAME:-}" "${CODEX_TOOL_FILE_PATH:-}" >> ~/.codex/command-log.txt
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
