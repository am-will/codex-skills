# development-tools/file-backup

Automatically backup files before editing. Creates timestamped backups in a .backups directory when files are modified.

Compatibility: adapted

## Events
- PostToolUse: 1 matcher group(s)

## Notes
- PreToolUse -> PostToolUse: Backs up edited files after the tool finishes instead of before.

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
