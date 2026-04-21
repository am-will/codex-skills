# monitoring/langsmith-tracing

Automatically send Codex conversation traces to LangSmith for monitoring and analysis. Prerequisites: jq (brew install jq on macOS or sudo apt-get install jq on Linux), curl and uuidgen (usually pre-installed), LangSmith account and API key. Configuration: install the matching LangSmith setting from the upstream template source, or manually add to `.codex/settings.local.json` the following environment variables: `TRACE_TO_LANGSMITH=true`, `CC_LANGSMITH_API_KEY=lsv2_pt_...`, `CC_LANGSMITH_PROJECT=project-name`, `CC_LANGSMITH_DEBUG=true` (optional). How it works: Runs in background on Stop event after each Codex response, reads conversation transcript, converts to LangSmith format, sends to LangSmith API, groups by `thread_id` for session continuity. Debugging: Check logs at `~/.codex/state/hook.log`. Privacy note: System prompts not included in traces.

Compatibility: direct

## Events
- Stop: 1 matcher group(s)

## Install
Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.
If the bundle includes `.codex/hooks/` support files, copy that directory too.
