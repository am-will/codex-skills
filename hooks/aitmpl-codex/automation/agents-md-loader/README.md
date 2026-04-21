# automation/agents-md-loader

Automatically loads AGENTS.md configuration file content at session start to ensure Codex follows project-specific agent behavior. Only loads if AGENTS.md exists, otherwise passes empty context. Supports the universal AGENTS.md standard for cross-platform AI assistant compatibility.

Compatibility: direct

## Events
- SessionStart: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
