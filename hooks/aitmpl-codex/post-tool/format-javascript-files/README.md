# post-tool/format-javascript-files

Automatically format JavaScript/TypeScript files after any Edit operation using prettier. This hook runs 'npx prettier --write' on any .js, .ts, .jsx, or .tsx file that Codex modifies, ensuring consistent code formatting. Uses npx so prettier doesn't need to be globally installed. Includes error suppression so it won't fail if prettier is not available.

Compatibility: direct

## Events
- PostToolUse: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
