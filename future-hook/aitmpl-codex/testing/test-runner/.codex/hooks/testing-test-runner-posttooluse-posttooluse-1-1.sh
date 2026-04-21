#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
command=$(cat <<'__CODEx_HOOK_COMMAND__'
if [[ "$CLAUDE_TOOL_FILE_PATH" == *.js || "$CLAUDE_TOOL_FILE_PATH" == *.ts ]] && [[ -f package.json ]]; then npm test 2>/dev/null || yarn test 2>/dev/null || true; elif [[ "$CLAUDE_TOOL_FILE_PATH" == *.py ]] && [[ -f pytest.ini || -f setup.cfg || -f pyproject.toml ]]; then pytest "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || python -m pytest "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true; elif [[ "$CLAUDE_TOOL_FILE_PATH" == *.rb ]] && [[ -f Gemfile ]]; then bundle exec rspec "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true; fi
__CODEx_HOOK_COMMAND__
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
