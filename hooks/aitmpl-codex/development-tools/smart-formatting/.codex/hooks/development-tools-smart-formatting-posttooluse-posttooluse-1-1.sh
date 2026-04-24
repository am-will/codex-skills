#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if [[ "$CODEX_TOOL_FILE_PATH" == *.js || "$CODEX_TOOL_FILE_PATH" == *.ts || "$CODEX_TOOL_FILE_PATH" == *.jsx || "$CODEX_TOOL_FILE_PATH" == *.tsx || "$CODEX_TOOL_FILE_PATH" == *.json || "$CODEX_TOOL_FILE_PATH" == *.css || "$CODEX_TOOL_FILE_PATH" == *.html ]]; then npx prettier --write "$CODEX_TOOL_FILE_PATH" 2>/dev/null || true; elif [[ "$CODEX_TOOL_FILE_PATH" == *.py ]]; then black "$CODEX_TOOL_FILE_PATH" 2>/dev/null || true; elif [[ "$CODEX_TOOL_FILE_PATH" == *.go ]]; then gofmt -w "$CODEX_TOOL_FILE_PATH" 2>/dev/null || true; elif [[ "$CODEX_TOOL_FILE_PATH" == *.rs ]]; then rustfmt "$CODEX_TOOL_FILE_PATH" 2>/dev/null || true; elif [[ "$CODEX_TOOL_FILE_PATH" == *.php ]]; then php-cs-fixer fix "$CODEX_TOOL_FILE_PATH" 2>/dev/null || true; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
