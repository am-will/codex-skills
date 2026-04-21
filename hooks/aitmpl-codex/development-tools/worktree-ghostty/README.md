# development-tools/worktree-ghostty

Worktree Ghostty Layout. Opens a 3-panel Ghostty layout when creating worktrees: Codex (left) | lazygit (top-right) / yazi (bottom-right). Creates worktrees in a sibling directory (../worktrees/<repo>/<name>/) and cleans up on removal. macOS only. Requires: jq, Ghostty terminal, lazygit, yazi. Ghostty keybindings required: super+d = new_split:right, super+shift+d = new_split:down.

Compatibility: adapted

## Events
- SessionStart: 1 matcher group(s)
- Stop: 1 matcher group(s)

## Notes
- WorktreeCreate -> SessionStart
- WorktreeRemove -> Stop

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
