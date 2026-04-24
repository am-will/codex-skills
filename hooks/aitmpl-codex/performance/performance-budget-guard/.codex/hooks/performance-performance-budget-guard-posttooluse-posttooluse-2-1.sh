#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
bash -c 'input=$(cat); FILE_PATH=$(echo "$input" | jq -r ".tool_input.file_path // empty"); SUCCESS=$(echo "$input" | jq -r ".tool_response.success // false"); if [ "$SUCCESS" = "true" ] && [[ "$FILE_PATH" =~ \.(js|jsx|ts|tsx)$ ]] && [[ ! "$FILE_PATH" =~ node_modules ]]; then echo "🔍 Performance Guard: Checking code changes in $FILE_PATH..."; if [ -f "$FILE_PATH" ]; then FILE_SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null); FILE_SIZE_KB=$((FILE_SIZE / 1024)); if [ $FILE_SIZE_KB -gt 100 ]; then echo "⚠️ Large file detected: ${FILE_SIZE_KB}KB"; echo "💡 Consider splitting large components or lazy loading"; fi; IMPORTS_COUNT=$(grep -c "^import" "$FILE_PATH" 2>/dev/null || echo "0"); if [ $IMPORTS_COUNT -gt 15 ]; then echo "📦 Many imports detected: $IMPORTS_COUNT imports"; echo "💡 Consider consolidating imports or tree-shaking unused code"; fi; if grep -q "import.*\*.*from" "$FILE_PATH" 2>/dev/null; then echo "🚨 Wildcard import detected in $FILE_PATH"; echo "💡 Use specific imports instead of wildcard imports for better tree-shaking"; fi; if grep -q "moment" "$FILE_PATH" 2>/dev/null; then echo "📅 Moment.js usage detected"; echo "💡 Consider using date-fns or native Date for smaller bundle size"; fi; if grep -q "lodash" "$FILE_PATH" 2>/dev/null && ! grep -q "lodash/" "$FILE_PATH" 2>/dev/null; then echo "🔧 Full Lodash import detected"; echo "💡 Use specific Lodash functions: import debounce from \"lodash/debounce\""; fi; echo "✅ Performance check completed for $FILE_PATH"; else echo "❌ File $FILE_PATH not found"; fi; else echo "ℹ️ Performance check skipped (not a JavaScript/TypeScript file or failed operation)"; fi'
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
