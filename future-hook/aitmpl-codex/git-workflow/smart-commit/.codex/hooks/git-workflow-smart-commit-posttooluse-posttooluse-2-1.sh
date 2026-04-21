#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if git rev-parse --git-dir >/dev/null 2>&1 && [[ -n "$CLAUDE_TOOL_FILE_PATH" ]]; then git add "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; FILENAME=$(basename "$CLAUDE_TOOL_FILE_PATH"); git commit -m "Add new file: $FILENAME" "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
