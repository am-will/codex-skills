#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
PROTECTED_PATTERNS=('*/etc/*' '*/usr/bin/*' '*/usr/sbin/*' '*.production.*' '*prod*config*' '*/node_modules/*' '*/vendor/*'); for pattern in "${PROTECTED_PATTERNS[@]}"; do if [[ "$CLAUDE_TOOL_FILE_PATH" == $pattern ]]; then echo "Error: File $CLAUDE_TOOL_FILE_PATH is protected from modification" >&2; exit 1; fi; done
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
