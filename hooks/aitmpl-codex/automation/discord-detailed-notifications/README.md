# automation/discord-detailed-notifications

Send detailed Discord notifications with session information when Codex finishes. Includes working directory, session duration, and system info with rich embeds. Requires DISCORD_WEBHOOK_URL environment variable.

Compatibility: direct

## Events
- SessionStart: 1 matcher group(s)
- Stop: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
