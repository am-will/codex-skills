# automation/discord-notifications

Send Discord notifications when Codex finishes working. Requires DISCORD_WEBHOOK_URL environment variable. Get webhook URL from Discord Server Settings -> Integrations -> Webhooks.

Compatibility: adapted

## Events
- Stop: 2 matcher group(s)

## Notes
- SubagentStop -> Stop

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
