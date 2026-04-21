#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if command -v semgrep >/dev/null 2>&1; then semgrep --config=auto "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true; fi; if command -v bandit >/dev/null 2>&1 && [[ "$CLAUDE_TOOL_FILE_PATH" == *.py ]]; then bandit "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true; fi; if command -v gitleaks >/dev/null 2>&1; then gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --no-git 2>/dev/null || true; fi; if grep -qE '(password|secret|key|token)\s*=\s*["\x27][^"\x27]{8,}' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then echo "Warning: Potential hardcoded secrets detected in $CLAUDE_TOOL_FILE_PATH" >&2; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
