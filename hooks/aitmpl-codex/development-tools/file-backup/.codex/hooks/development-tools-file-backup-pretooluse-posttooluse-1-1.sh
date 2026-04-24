#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if [[ -n "$CODEX_TOOL_FILE_PATH" && -f "$CODEX_TOOL_FILE_PATH" ]]; then mkdir -p .backups && cp "$CODEX_TOOL_FILE_PATH" ".backups/$(basename "$CODEX_TOOL_FILE_PATH").$(date +%Y%m%d_%H%M%S).bak"; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
