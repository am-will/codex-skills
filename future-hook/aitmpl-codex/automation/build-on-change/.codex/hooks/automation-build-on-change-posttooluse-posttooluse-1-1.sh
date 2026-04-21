#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if [[ -f package.json ]] && grep -q '"build"' package.json; then npm run build 2>/dev/null || yarn build 2>/dev/null || true; elif [[ -f Makefile ]]; then make 2>/dev/null || true; elif [[ -f Cargo.toml ]]; then cargo build 2>/dev/null || true; elif [[ -f pom.xml ]]; then mvn compile 2>/dev/null || true; elif [[ -f build.gradle ]]; then ./gradlew build 2>/dev/null || true; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
