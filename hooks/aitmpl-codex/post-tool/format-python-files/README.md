# post-tool/format-python-files

Automatically format Python files after any Edit operation using black formatter. This hook runs 'black' on any .py file that Codex modifies, ensuring consistent Python code formatting. Requires black to be installed ('pip install black'). The command includes error suppression (2>/dev/null || true) so it won't fail if black is not installed.

Compatibility: direct

## Events
- PostToolUse: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
