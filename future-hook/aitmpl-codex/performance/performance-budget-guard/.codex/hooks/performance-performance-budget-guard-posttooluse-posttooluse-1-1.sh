#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
bash -c 'input=$(cat); COMMAND=$(echo "$input" | jq -r ".tool_input.command // empty"); SUCCESS=$(echo "$input" | jq -r ".tool_response.success // false"); if [ "$SUCCESS" = "true" ] && [[ "$COMMAND" =~ (npm\ run\ build|next\ build|vercel\ build|yarn\ build) ]]; then echo "📊 Performance Budget Guard: Analyzing build output..."; if [ -d ".next" ]; then BUNDLE_SIZE=$(find .next/static/chunks -name "*.js" -exec stat -f%z {} + 2>/dev/null | awk "{total += \$1} END {print total}"); BUNDLE_SIZE_KB=$((BUNDLE_SIZE / 1024)); BUDGET_LIMIT=350; echo "📦 Total bundle size: ${BUNDLE_SIZE_KB}KB"; if [ $BUNDLE_SIZE_KB -gt $BUDGET_LIMIT ]; then echo "🚨 PERFORMANCE BUDGET EXCEEDED!"; echo "Current bundle size: ${BUNDLE_SIZE_KB}KB"; echo "Budget limit: ${BUDGET_LIMIT}KB"; echo "Overage: $((BUNDLE_SIZE_KB - BUDGET_LIMIT))KB"; echo "" >&2; echo "⚠️ Performance budget exceeded by $((BUNDLE_SIZE_KB - BUDGET_LIMIT))KB!" >&2; echo "" >&2; echo "📋 Bundle Analysis:" >&2; find .next/static/chunks -name "*.js" -exec ls -lah {} + 2>/dev/null | sort -k5 -hr | head -5 >&2; echo "" >&2; echo "💡 Optimization recommendations:" >&2; echo "• Use dynamic imports for large components" >&2; echo "• Implement code splitting with next/dynamic" >&2; echo "• Check for duplicate dependencies" >&2; echo "• Optimize third-party libraries" >&2; echo "• Run: npm run analyze for detailed bundle analysis" >&2; exit 2; else echo "✅ Bundle size within budget: ${BUNDLE_SIZE_KB}KB / ${BUDGET_LIMIT}KB"; REMAINING=$((BUDGET_LIMIT - BUNDLE_SIZE_KB)); echo "🎯 Remaining budget: ${REMAINING}KB"; if [ $REMAINING -lt 50 ]; then echo "⚠️ Warning: Less than 50KB remaining in performance budget"; fi; fi; else echo "❌ No .next build directory found. Run build first."; fi; else echo "ℹ️ Performance check skipped (not a build command or failed build)"; fi'
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
