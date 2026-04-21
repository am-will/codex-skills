# pre-tool/console-log-cleaner

Warns about console.log statements when editing files on production branches (main/master). Helps prevent debug code from reaching production.

Compatibility: adapted

## Events
- PostToolUse: 1 matcher group(s)

## Notes
- PreToolUse -> PostToolUse: Warns after file edits instead of before them.

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
