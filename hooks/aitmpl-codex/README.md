# AITMPL to Codex Hook Catalog

This catalog mirrors an upstream hook template set and rewrites it into Codex hook bundles.

- Bundles: 27
- Direct: 18
- Adapted: 9

Each active bundle contains:

- `hooks.json` for Codex
- `.codex/hooks/` support files when the template needs them
- `bundle.json` metadata
- `README.md` install notes
- `install-bundle.py` to merge a bundle into a target repo's `.codex/`
- `tools/harness.py` to smoke-test every bundle in a temp workspace

To install a bundle:

1. Copy the bundle contents into the project root you want Codex to use.
2. Merge the bundle's `hooks.json` into your project `.codex/hooks.json`.
3. Copy the bundle's `.codex/hooks/` directory into your project `.codex/hooks/`.
4. Or run `python3 hooks/aitmpl-codex/install-bundle.py hooks/aitmpl-codex/<bundle> <target-root>`.

Archived bundles that rely on unsupported `Edit|Write|MultiEdit` matcher paths now live under `future-hook/aitmpl-codex/`.

Catalog:
- `automation/agents-md-loader` - direct - Automatically loads AGENTS.md configuration file content at session start to ensure Codex follows project-specific agent behavior. Only loads if AGENTS.md exists, otherwise passes empty context. Supports the universal AGENTS.md standard for cross-platform AI assistant compatibility.
- `automation/deployment-health-monitor` - direct - Monitor deployment status, error rates, and performance metrics, sending notifications for failed deployments or performance degradation. Tracks Vercel deployment health, monitors build success/failure rates, and provides alerts for deployment issues. Setup: Export 'export VERCEL_TOKEN=your_token' and 'export VERCEL_PROJECT_ID=your_project_id' (get from vercel.com/account/tokens and Vercel dashboard).
- `automation/discord-detailed-notifications` - direct - Send detailed Discord notifications with session information when Codex finishes. Includes working directory, session duration, and system info with rich embeds. Requires DISCORD_WEBHOOK_URL environment variable.
- `automation/discord-error-notifications` - adapted - Send Discord notifications when Codex encounters long-running operations or when tools take significant time. Helps monitor productivity and catch potential issues with rich embeds. Requires DISCORD_WEBHOOK_URL environment variable.
- `automation/discord-notifications` - adapted - Send Discord notifications when Codex finishes working. Requires DISCORD_WEBHOOK_URL environment variable. Get webhook URL from Discord Server Settings -> Integrations -> Webhooks.
- `automation/simple-notifications` - direct - Send simple desktop notifications when Codex operations complete. Works on macOS and Linux systems.
- `automation/slack-detailed-notifications` - direct - Send detailed Slack notifications with session information when Codex finishes. Includes working directory, session duration, and system info. Requires SLACK_WEBHOOK_URL environment variable.
- `automation/slack-error-notifications` - adapted - Send Slack notifications when Codex encounters long-running operations or when tools take significant time. Helps monitor productivity and catch potential issues. Requires SLACK_WEBHOOK_URL environment variable.
- `automation/slack-notifications` - adapted - Send Slack notifications when Codex finishes working. Requires SLACK_WEBHOOK_URL environment variable. Get webhook URL from Slack App settings -> Incoming Webhooks.
- `automation/telegram-detailed-notifications` - direct - Send detailed Telegram notifications with session information when Codex finishes. Includes working directory, session duration, and system info. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
- `automation/telegram-error-notifications` - adapted - Send Telegram notifications when Codex encounters long-running operations or when tools take significant time. Helps monitor productivity and catch potential issues. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
- `automation/telegram-notifications` - adapted - Send Telegram notifications when Codex finishes working. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables. Get bot token from @BotFather, get chat ID by messaging the bot and visiting https://api.telegram.org/bot<TOKEN>/getUpdates
- `automation/telegram-pr-webhook` - direct - Send Telegram notification when a new PR is created via gh pr create. Includes PR URL and Vercel preview URL. Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables. Optionally set VERCEL_PROJECT_NAME and VERCEL_TEAM_SLUG to construct the Vercel preview URL automatically.
- `development-tools/command-logger` - direct - Log all Codex commands to a file for audit and debugging purposes. Simple logging that records tool usage with timestamps.
- `development-tools/debug-window` - adapted - Auto Debug Log Viewer. Opens a live-tailing debug log window when Codex starts with --debug or -d flag. The window closes automatically on session end. To keep the debug window open after session ends, set DEBUG_WINDOW_AUTO_CLOSE_DISABLE=1 in your settings.json. Tested on Intel Mac. Supports macOS, Linux, and Windows (Git Bash/Cygwin). Contributions from other platform users are welcome.
- `development-tools/worktree-ghostty` - adapted - Worktree Ghostty Layout. Opens a 3-panel Ghostty layout when creating worktrees: Codex (left) | lazygit (top-right) / yazi (bottom-right). Creates worktrees in a sibling directory (../worktrees/<repo>/<name>/) and cleans up on removal. macOS only. Requires: jq, Ghostty terminal, lazygit, yazi. Ghostty keybindings required: super+d = new_split:right, super+shift+d = new_split:down.
- `git/conventional-commits` - direct - Enforce conventional commit message format for all git commits. Validates commit messages follow the pattern: type(scope): description. Supported types: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert. Ensures consistent commit history for changelog generation and semantic versioning.
- `git/prevent-direct-push` - direct - Prevent direct pushes to protected branches (main, develop). Blocks git push commands targeting main or develop branches to enforce Git Flow workflow. Requires using feature/release/hotfix branches and pull requests instead of direct commits to protected branches.
- `git/validate-branch-name` - direct - Validate Git Flow branch naming conventions before checkout. Ensures branches follow the pattern: feature/*, release/v*.*.*, hotfix/*. Prevents creation of branches that don't follow Git Flow standards.
- `monitoring/desktop-notification-on-stop` - direct - Sends a native desktop notification when Codex finishes responding. Uses the Stop hook event so you get a single notification per response instead of one per tool call (which is very noisy with PostToolUse). Supports macOS (osascript) and Linux (notify-send). Useful when you switch to another window while Codex works — you'll get a notification when it's ready for your input.
- `monitoring/langsmith-tracing` - direct - Automatically send Codex conversation traces to LangSmith for monitoring and analysis. Prerequisites: jq (brew install jq on macOS or sudo apt-get install jq on Linux), curl and uuidgen (usually pre-installed), LangSmith account and API key. Configuration: install the matching LangSmith setting from the upstream template source, or manually add to `.codex/settings.local.json` the following environment variables: `TRACE_TO_LANGSMITH=true`, `CC_LANGSMITH_API_KEY=lsv2_pt_...`, `CC_LANGSMITH_PROJECT=project-name`, `CC_LANGSMITH_DEBUG=true` (optional). How it works: Runs in background on Stop event after each Codex response, reads conversation transcript, converts to LangSmith format, sends to LangSmith API, groups by `thread_id` for session continuity. Debugging: Check logs at `~/.codex/state/hook.log`. Privacy note: System prompts not included in traces.
- `performance/performance-monitor` - direct - Monitor system performance during Codex operations. Tracks CPU, memory usage, and execution time for performance optimization.
- `pre-tool/notify-before-bash` - direct - Show notification before any Bash command execution for security awareness. This hook displays a simple echo message '🔔 About to run bash command...' before Codex executes any bash command, giving you visibility into when system commands are about to run. Useful for monitoring and auditing command execution.
- `pre-tool/update-search-year` - adapted - Automatically adds current year to WebSearch queries when no year is specified. This hook intercepts WebSearch tool usage and appends the current year to queries that don't already contain a year, ensuring search results are current and relevant.
- `quality-gates/scope-guard` - direct - Scope guard that detects files modified outside the declared scope of a specification. When a .spec.md file contains a 'Files to Create/Modify' section, this hook compares git-modified files against the declared list. Files outside scope trigger a warning (non-blocking). Automatically excludes test files, config files, infrastructure files, and documentation. Essential for Spec-Driven Development to prevent scope creep during implementation.
- `security/dangerous-command-blocker` - direct - Advanced protection against dangerous shell commands with multi-level security. Blocks catastrophic operations (rm -rf /, dd, mkfs), protects critical paths (.codex/, .git/, node_modules/), and warns about suspicious patterns. Features: catastrophic command blocking, critical path protection, smart pattern detection, and detailed safety messages.
- `security/secret-scanner` - direct - Automatically detects hardcoded secrets before git commits. Scans for API keys from 30+ providers (Anthropic: sk-ant-..., OpenAI: sk-..., AWS: AKIA..., Stripe: sk_live_..., Google: AIza..., GitHub: ghp_..., Vercel, Supabase, Hugging Face: hf_..., Replicate: r8_..., Groq: gsk_..., Databricks: dapi..., GitLab, DigitalOcean, npm, PyPI, and more), tokens, passwords, private keys, and database credentials. Blocks commits containing secrets and suggests using environment variables instead.
