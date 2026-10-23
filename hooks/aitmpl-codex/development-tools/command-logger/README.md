# development-tools/command-logger

Logs each matching `PreToolUse` event's timestamp, tool name, and file path (when provided) to `~/.codex/command-log.txt`. The log appends indefinitely without rotation or redaction; file paths may reveal sensitive project information, so protect the log appropriately.

Compatibility: direct

## Events
- PreToolUse: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
