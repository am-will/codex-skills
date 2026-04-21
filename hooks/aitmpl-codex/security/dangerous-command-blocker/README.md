# security/dangerous-command-blocker

Advanced protection against dangerous shell commands with multi-level security. Blocks catastrophic operations (rm -rf /, dd, mkfs), protects critical paths (.codex/, .git/, node_modules/), and warns about suspicious patterns. Features: catastrophic command blocking, critical path protection, smart pattern detection, and detailed safety messages.

Compatibility: direct

## Events
- PreToolUse: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
