# pre-tool/notify-before-bash

Show notification before any Bash command execution for security awareness. This hook displays a simple echo message '🔔 About to run bash command...' before Codex executes any bash command, giving you visibility into when system commands are about to run. Useful for monitoring and auditing command execution.

Compatibility: direct

## Events
- PreToolUse: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
