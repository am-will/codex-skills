<img width="750" height="491" alt="image" src="https://github.com/user-attachments/assets/c244cbdd-6f98-40b5-81f0-754aad546be4" />


# CodexSkills

A collection of Codex/agent skills for planning, documentation access, frontend development, and browser automation.

## Available skills

### Agent Orchestration

- `planner`:
  Create comprehensive, phased implementation plans with sprints and atomic tasks. Use for planning implementations, breaking down features, or creating structured roadmaps.
- `plan-harder`:
  Enhanced planning variant for more detailed analysis and task breakdown.
- `parallel-task`:
  Execute plan files by launching multiple parallel subagents to complete tasks simultaneously. Requires an existing plan file from `planner`.
- `llm-council`:
  Multi-agent orchestration system for planning complex tasks. Spawns multiple AI planners (Claude, Codex, Gemini) to generate independent plans, then uses a judge agent to synthesize the best approach. Includes a real-time web UI for monitoring progress and refining plans interactively.

### Documentation Access

- `ctx7old`:
  Fetch up-to-date library documentation via Context7 CLI.
- `openai-docs-skill`:
  Query OpenAI developer docs via the OpenAI Docs MCP server using CLI.
- `markdown-url`:
  Prefix any website you need to visit with `https://markdown.new/` for a clean, Markdown-friendly view.
- `read-github`:
  Read and search GitHub repository documentation via gitmcp.io MCP service. Converts `github.com/owner/repo` URLs to `gitmcp.io/owner/repo` for LLM-friendly access to repos.

### Frontend & Design

- `frontend-design`:
  Distinctive frontend design system guidance (imported from Anthropic).
- `frontend-responsive-ui`:
  Responsive UI standards (imported from Anthropic).
- `vercel-react-best-practices`:
  React/Next.js performance guidance (imported from Vercel).

### Codex Tooling

- `create-hook`:
  Create or update Codex hooks for global or project scope. Guides users through scope, hook type, and behavior, then writes hook config and scripts.
- `pluginstaller`:
  Install a Codex plugin from a GitHub repo into a repo or personal marketplace. Handles plugin discovery, validation, and marketplace registration.
- `role-creator`:
  Create and update custom Codex agents as standalone TOML files. Collects required inputs and writes agent definitions to global or project scope.

### Browser Automation

- `gemini-computer-use`:
  Gemini 2.5 Computer Use browser-control agent skill (Playwright + safety confirmation loop).
- `agent-browser`:
  Fast Rust-based headless browser automation CLI from Vercel Labs with snapshot/act pattern for AI agents.

## Installation

Install skills using the [skills.sh](https://skills.sh) CLI:

```bash
# List available skills before installing
npx skills add am-will/codex-skills --list

# Install specific skills to user scope (global)
npx skills add am-will/codex-skills --skill planner --skill context7 -g

# Install all skills interactively (prompts for selection)
npx skills add am-will/codex-skills -g

# Install to specific agents
npx skills add am-will/codex-skills --skill planner -a claude-code -a codex -g

# Install to current project (instead of global)
npx skills add am-will/codex-skills --skill planner

# Non-interactive install (skip prompts)
npx skills add am-will/codex-skills --skill planner -g -y
```

**CLI Options:**
| Flag | Purpose |
|------|---------|
| `-g, --global` | Install to user directory (global for all projects) |
| `-a, --agent <agents...>` | Target specific agents (`claude-code`, `codex`, etc.) |
| `-s, --skill <skills...>` | Install specific skills by name |
| `-l, --list` | List available skills without installing |
| `-y, --yes` | Skip confirmation prompts |

**Other commands:**
```bash
npx skills list          # Show installed skills
npx skills remove <name> # Uninstall a skill
npx skills update        # Update all installed skills
```

**Note on Browser Tools**: The repo includes two browser automation tools (`gemini-computer-use` and `agent-browser`). You don't need to install both - choose the one that best fits your workflow. I recommend agent-browser for speed and simplicity.

**Note on Context7**: The `ctx7old` skill requires a Context7 API key in `CONTEXT7_API_KEY`. See `skills/ctx7old/.env.example` for setup.

**Note on Gemini Computer Use Skill**: This skill requires a GEMINI_API_KEY. Ask Codex to help you set it up.

**Note on llm-council**: This skill requires API keys or Active Subscriptions for multiple providers (Claude/Anthropic, OpenAI for Codex, Google for Gemini). Run `./setup.sh` in the skill directory to configure. Includes a real-time web UI that auto-launches during planning sessions.

---

### Codex Hook Catalog

The `hooks/` directory contains a catalog of **51 ready-to-install Codex hook bundles**, generated from an upstream hook template set and adapted for the current Codex event model. The active catalog now includes the former file-edit bundles that became viable once Codex started emitting `apply_patch` hook events with `Edit` and `Write` matcher compatibility.

**Categories:**

| Category | Bundles | Examples |
|---|---|---|
| `automation` | 18 | Slack/Discord/Telegram notifications, deployment health monitor, AGENTS loader, build/dependency automation |
| `development-tools` | 8 | Command logger, debug window, worktree ghostty, file backup, lint/format helpers |
| `git` | 3 | Conventional commits, prevent direct push, validate branch name |
| `git-workflow` | 2 | Auto git add, smart commit |
| `monitoring` | 2 | Desktop notification on stop, LangSmith tracing |
| `performance` | 2 | Performance monitor, performance budget guard |
| `post-tool` | 4 | Format JS/Python, git add changes, run tests after changes |
| `pre-tool` | 4 | Notify before bash, update search year, backup before edit, console log cleaner |
| `quality-gates` | 3 | Scope guard, plan gate, TDD gate |
| `security` | 4 | Dangerous command blocker, secret scanner, file protection, security scanner |
| `testing` | 1 | Test runner |

**Install a bundle:**
```bash
python3 hooks/aitmpl-codex/install-bundle.py hooks/aitmpl-codex/<category>/<bundle> <target-repo>
```

**Manual install:** Copy the bundle's `hooks.json` into `<repo>/.codex/hooks.json` and its `.codex/hooks/` scripts into `<repo>/.codex/hooks/`, then restart Codex.

See [`hooks/README.md`](hooks/README.md) for full details on compatibility, testing harness, and bundle structure.

---

### Custom Multi-Agents for Codex

The `agents/` directory contains custom multi-agent configurations for Codex. These TOML-based agent definitions provide specialized roles (architect, frontend, backend, security, etc.) and worker tiers for parallel task execution. Use them with Codex to spin up purpose-built agents tailored to your workflow.
