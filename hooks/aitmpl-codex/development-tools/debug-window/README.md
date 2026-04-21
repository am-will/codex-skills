# development-tools/debug-window

Auto Debug Log Viewer. Opens a live-tailing debug log window when Codex starts with --debug or -d flag. The window closes automatically on session end. To keep the debug window open after session ends, set DEBUG_WINDOW_AUTO_CLOSE_DISABLE=1 in your settings.json. Tested on Intel Mac. Supports macOS, Linux, and Windows (Git Bash/Cygwin). Contributions from other platform users are welcome.

Compatibility: adapted

## Events
- SessionStart: 1 matcher group(s)
- Stop: 1 matcher group(s)

## Notes
- SessionEnd -> Stop

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
