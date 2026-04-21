# quality-gates/plan-gate

Planning gate that warns when editing production code without an approved specification. Checks for recent .spec.md files in the project directory (last 14 days). If no spec is found, shows a warning suggesting to create one first. Non-blocking (exit 0) — acts as a reminder, not a hard gate. Supports 16 programming languages. Part of the Spec-Driven Development (SDD) methodology where every implementation should be backed by an approved specification.

Compatibility: adapted

## Events
- PostToolUse: 3 matcher group(s)

## Notes
- PreToolUse -> PostToolUse: Plan reminder runs after file edits instead of before them.

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
