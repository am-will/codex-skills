#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
bash -c 'echo "🔐 Environment Sync Status Check..."; if [ -n "$VERCEL_TOKEN" ]; then echo "✅ Vercel token configured"; if command -v vercel >/dev/null 2>&1; then echo "✅ Vercel CLI available"; PROJECT_STATUS=$(vercel project ls 2>/dev/null | head -1); if [[ "$PROJECT_STATUS" =~ "No projects found" ]]; then echo "⚠️ No Vercel project linked to current directory"; echo "💡 Run: vercel link"; else echo "✅ Vercel project linked"; fi; else echo "⚠️ Vercel CLI not installed"; echo "💡 Install with: npm i -g vercel"; fi; if [ -f ".env.example" ]; then echo "📋 .env.example found - template available"; fi; ENV_FILES=($(ls .env* 2>/dev/null | grep -v .env.example || true)); if [ ${#ENV_FILES[@]} -gt 0 ]; then echo "📁 Environment files found: ${ENV_FILES[*]}"; for file in "${ENV_FILES[@]}"; do VAR_COUNT=$(grep -c "^[A-Z_][A-Z0-9_]*=" "$file" 2>/dev/null || echo "0"); echo "  $file: $VAR_COUNT variables"; done; else echo "ℹ️ No .env files found"; fi; else echo "⚠️ VERCEL_TOKEN not configured"; echo "💡 Environment sync features disabled"; fi'
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
