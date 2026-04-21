# Future Hook Archive

This folder holds Codex hook bundles that are not currently compatible with the live Codex hook runtime.

Archived here:
- Bundles whose `PreToolUse` or `PostToolUse` logic depends on `Edit`, `Write`, or `MultiEdit` matcher paths that current Codex does not emit.
- Bundles that are only partially compatible today and would otherwise appear installable from the active catalog.

Layout:
- `aitmpl-codex/<category>/<bundle>/` preserves each original bundle directory.

The active, installable catalog remains under `hooks/aitmpl-codex/`.
