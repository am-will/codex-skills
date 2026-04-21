# automation/vercel-environment-sync

Synchronize environment variables between local development and Vercel deployments, ensuring consistency across all environments. Detects changes to .env files and provides options to sync with Vercel, validates environment variable format, and ensures required variables are present. Setup: Export 'export VERCEL_TOKEN=your_token' (get from vercel.com/account/tokens).

Compatibility: direct

## Events
- PostToolUse: 1 matcher group(s)
- SessionStart: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
