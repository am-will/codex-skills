# post-tool/run-tests-after-changes

Automatically run quick tests after code modifications to ensure nothing breaks. This hook executes 'npm run test:quick' silently after any Edit operation and provides feedback on test status. Helps catch breaking changes immediately during development. Only runs if package.json exists and the test:quick script is available.

Compatibility: direct

## Events
- PostToolUse: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
