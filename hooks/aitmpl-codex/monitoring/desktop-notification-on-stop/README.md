# monitoring/desktop-notification-on-stop

Sends a native desktop notification when Codex finishes responding. Uses the Stop hook event so you get a single notification per response instead of one per tool call (which is very noisy with PostToolUse). Supports macOS (osascript) and Linux (notify-send). Useful when you switch to another window while Codex works — you'll get a notification when it's ready for your input.

Compatibility: direct

## Events
- Stop: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
