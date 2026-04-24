# performance/performance-budget-guard

Monitor bundle size and Core Web Vitals metrics during development, blocking deployments that exceed performance budgets with detailed reports. Automatically analyzes Next.js build output, checks bundle sizes against predefined budgets, and provides optimization recommendations. Hook triggers on PostToolUse for build-related operations and file changes that could affect performance.

Compatibility: direct

## Events
- PostToolUse: 2 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
