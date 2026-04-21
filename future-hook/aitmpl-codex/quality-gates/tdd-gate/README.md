# quality-gates/tdd-gate

Test-Driven Development enforcement hook. Blocks editing production code files (.cs, .py, .ts, .go, .rs, .rb, .php, .java, .kt, .swift, .dart) unless a corresponding test file exists. Forces the TDD workflow: write tests first, then implement. Automatically skips config files, migrations, DTOs, test files themselves, and infrastructure files. Looks for test files with common naming patterns (MyClassTest.ext, my-class.test.ext, my_class_test.ext, test_my_class.ext). Inspired by pm-workspace's Spec-Driven Development methodology.

Compatibility: adapted

## Events
- PostToolUse: 3 matcher group(s)

## Notes
- PreToolUse -> PostToolUse: TDD reminder runs after file edits instead of before them.

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
