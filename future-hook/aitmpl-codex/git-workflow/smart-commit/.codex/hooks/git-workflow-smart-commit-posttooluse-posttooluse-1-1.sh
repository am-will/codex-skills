#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if git rev-parse --git-dir >/dev/null 2>&1 && [[ -n "$CLAUDE_TOOL_FILE_PATH" ]]; then git add "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; CHANGED_LINES=$(git diff --cached --numstat "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null | awk '{print $1+$2}'); if [[ $CHANGED_LINES -gt 0 ]]; then FILENAME=$(basename "$CLAUDE_TOOL_FILE_PATH"); if [[ $CHANGED_LINES -lt 10 ]]; then SIZE="minor"; elif [[ $CHANGED_LINES -lt 50 ]]; then SIZE="moderate"; else SIZE="major"; fi; MSG="Update $FILENAME: $SIZE changes ($CHANGED_LINES lines)"; git commit -m "$MSG" "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true; fi; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
