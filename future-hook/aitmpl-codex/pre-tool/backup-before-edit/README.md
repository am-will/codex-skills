# pre-tool/backup-before-edit

Create automatic backup of files before any Edit operation for safety. This hook creates a timestamped backup copy (filename.backup.timestamp) of any existing file before Codex modifies it. Provides a safety net to recover previous versions if needed. Only backs up existing files, includes error suppression to handle edge cases gracefully.

Compatibility: adapted

## Events
- PostToolUse: 1 matcher group(s)

## Notes
- PreToolUse -> PostToolUse: Best-effort backup after the edit completes; Codex cannot prehook Edit/MultiEdit.

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
