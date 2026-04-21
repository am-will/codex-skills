# automation/change-logger

Log every file mutation to CSV for demo prep. Records timestamp, tool, file path, action, and details for Edit, MultiEdit, Write, and Bash operations. Output: .codex/critical_log_changes.csv

Compatibility: direct

## Events
- PostToolUse: 4 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
