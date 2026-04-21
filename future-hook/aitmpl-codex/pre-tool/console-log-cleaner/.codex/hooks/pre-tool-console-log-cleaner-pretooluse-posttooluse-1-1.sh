#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if git rev-parse --git-dir >/dev/null 2>&1 && [[ -n "$CLAUDE_TOOL_FILE_PATH" ]]; then BRANCH=$(git branch --show-current 2>/dev/null); if [[ "$BRANCH" =~ ^(main|master|production|prod)$ ]]; then EXT="${CLAUDE_TOOL_FILE_PATH##*.}"; if [[ "$EXT" =~ ^(js|ts|jsx|tsx|mjs|cjs)$ ]]; then LOGS=$(grep -n 'console\.' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null); if [[ -n "$LOGS" ]]; then echo "⚠️  WARNING: console statements found on '$BRANCH' branch:"; echo "$LOGS" | head -5; COUNT=$(echo "$LOGS" | wc -l); if [[ $COUNT -gt 5 ]]; then echo "... and $((COUNT-5)) more"; fi; echo "Consider removing debug statements before merging."; fi; fi; fi; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
