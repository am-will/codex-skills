# automation/slack-error-notifications

Send Slack notifications when Codex encounters long-running operations or when tools take significant time. Helps monitor productivity and catch potential issues. Requires SLACK_WEBHOOK_URL environment variable.

Compatibility: adapted

## Events
- PreToolUse: 1 matcher group(s)
- PostToolUse: 1 matcher group(s)
- Stop: 1 matcher group(s)

## Notes
- Notification -> Stop

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
