# automation/vercel-auto-deploy

Automatically trigger Vercel deployments when code changes are committed, with environment-specific deployment strategies and rollback on failure. Setup: Export environment variables 'export VERCEL_TOKEN=your_token' and 'export VERCEL_PROJECT_ID=your_project_id' (get your token from vercel.com/account/tokens and project ID from your Vercel dashboard). Hook triggers on PostToolUse for Write, Edit, and MultiEdit operations affecting source code files.

Compatibility: direct

## Events
- PostToolUse: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
