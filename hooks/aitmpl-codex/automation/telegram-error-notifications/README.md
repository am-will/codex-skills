# automation/telegram-error-notifications

Send Telegram notifications when Codex encounters long-running operations or when tools take significant time. Helps monitor productivity and catch potential issues. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.

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
