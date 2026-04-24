# post-tool/git-add-changes

Automatically stage changes in git after file modifications for easier commit workflow. This hook runs 'git add' on any file that Codex edits or writes, automatically staging changes for the next commit. Includes error suppression so it won't fail in non-git repositories. Helps streamline the development workflow by preparing files for commit.

Compatibility: direct

## Events
- PostToolUse: 2 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
