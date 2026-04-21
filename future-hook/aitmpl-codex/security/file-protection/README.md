# security/file-protection

Protect critical files from accidental modification. Prevents editing of important system files, configuration files, and production code.

Compatibility: adapted

## Events
- PostToolUse: 1 matcher group(s)

## Notes
- PreToolUse -> PostToolUse: Protection warnings are emitted after the edit/write completes.

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
