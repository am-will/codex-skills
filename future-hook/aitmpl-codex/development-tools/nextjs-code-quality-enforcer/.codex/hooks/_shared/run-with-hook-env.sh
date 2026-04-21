#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: run-with-hook-env.sh -- <command> [args...]" >&2
  exit 64
fi

if [[ "${1:-}" == "--" ]]; then
  shift
fi

input="$(cat)"

export CODEX_HOOK_INPUT_JSON="$input"
export CLAUDE_HOOK_INPUT_JSON="$input"

json_get() {
  local expr="$1"
  jq -r "$expr" <<<"$input" 2>/dev/null || true
}

export CLAUDE_SESSION_ID="$(json_get '.session_id // empty')"
export CLAUDE_TURN_ID="$(json_get '.turn_id // empty')"
export CLAUDE_TRANSCRIPT_PATH="$(json_get '.transcript_path // empty')"
export CLAUDE_CWD="$(json_get '.cwd // empty')"
export CLAUDE_PROJECT_DIR="${CLAUDE_CWD:-$(pwd)}"
export CLAUDE_HOOK_EVENT_NAME="$(json_get '.hook_event_name // empty')"
export CLAUDE_MODEL="$(json_get '.model // empty')"
export CLAUDE_PERMISSION_MODE="$(json_get '.permission_mode // empty')"
export CLAUDE_SOURCE="$(json_get '.source // empty')"
export CLAUDE_PROMPT="$(json_get '.prompt // empty')"
export CLAUDE_STOP_HOOK_ACTIVE="$(json_get '.stop_hook_active // empty')"
export CLAUDE_LAST_ASSISTANT_MESSAGE="$(json_get '.last_assistant_message // empty')"

export CODEX_SESSION_ID="$CLAUDE_SESSION_ID"
export CODEX_TURN_ID="$CLAUDE_TURN_ID"
export CODEX_TRANSCRIPT_PATH="$CLAUDE_TRANSCRIPT_PATH"
export CODEX_CWD="$CLAUDE_CWD"
export CODEX_PROJECT_DIR="$CLAUDE_PROJECT_DIR"
export CODEX_HOOK_EVENT_NAME="$CLAUDE_HOOK_EVENT_NAME"
export CODEX_MODEL="$CLAUDE_MODEL"
export CODEX_PERMISSION_MODE="$CLAUDE_PERMISSION_MODE"
export CODEX_SOURCE="$CLAUDE_SOURCE"
export CODEX_PROMPT="$CLAUDE_PROMPT"
export CODEX_STOP_HOOK_ACTIVE="$CLAUDE_STOP_HOOK_ACTIVE"
export CODEX_LAST_ASSISTANT_MESSAGE="$CLAUDE_LAST_ASSISTANT_MESSAGE"

export CLAUDE_CALL_ID="$(json_get '.call_id // empty')"
export CLAUDE_TOOL_NAME="$(json_get '.tool_name // empty')"
export CLAUDE_TOOL_KIND="$(json_get '.tool_kind // empty')"
export CLAUDE_DURATION_MS="$(json_get '.duration_ms // empty')"
export CLAUDE_EXECUTED="$(json_get '.executed // empty')"
export CLAUDE_SUCCESS="$(json_get '.success // empty')"
export CLAUDE_MUTATING="$(json_get '.mutating // empty')"
export CLAUDE_SANDBOX="$(json_get '.sandbox // empty')"
export CLAUDE_SANDBOX_POLICY="$(json_get '.sandbox_policy // empty')"
export CLAUDE_OUTPUT_PREVIEW="$(json_get '.output_preview // empty')"

export CODEX_CALL_ID="$CLAUDE_CALL_ID"
export CODEX_TOOL_NAME="$CLAUDE_TOOL_NAME"
export CODEX_TOOL_KIND="$CLAUDE_TOOL_KIND"
export CODEX_DURATION_MS="$CLAUDE_DURATION_MS"
export CODEX_EXECUTED="$CLAUDE_EXECUTED"
export CODEX_SUCCESS="$CLAUDE_SUCCESS"
export CODEX_MUTATING="$CLAUDE_MUTATING"
export CODEX_SANDBOX="$CLAUDE_SANDBOX"
export CODEX_SANDBOX_POLICY="$CLAUDE_SANDBOX_POLICY"
export CODEX_OUTPUT_PREVIEW="$CLAUDE_OUTPUT_PREVIEW"

tool_input_raw="$(json_get '.tool_input // empty')"
export CLAUDE_TOOL_INPUT="$tool_input_raw"
export CODEX_TOOL_INPUT="$tool_input_raw"

if [[ "$CLAUDE_HOOK_EVENT_NAME" == "PreToolUse" ]]; then
  export CLAUDE_TOOL_COMMAND="$(json_get '.tool_input.command // empty')"
  export CLAUDE_TOOL_FILE_PATH="$(json_get '.tool_input.file_path // empty')"
else
  if [[ -n "$tool_input_raw" && "$tool_input_raw" != "null" ]]; then
    tool_input_json="$(jq -r 'try fromjson catch empty' <<<"$tool_input_raw" 2>/dev/null || true)"
    if [[ -n "$tool_input_json" ]]; then
      export CLAUDE_TOOL_INPUT_JSON="$tool_input_json"
      export CLAUDE_TOOL_FILE_PATH="$(jq -r 'try (fromjson | .file_path // .path // .destination // .params.file_path // .params.path // empty) catch ""' <<<"$tool_input_raw" 2>/dev/null || true)"
      export CLAUDE_TOOL_COMMAND="$(jq -r 'try (fromjson | .command // (.params.command | join(" ")) // empty) catch ""' <<<"$tool_input_raw" 2>/dev/null || true)"
      export CODEX_TOOL_INPUT_JSON="$tool_input_json"
    fi
  fi
fi

: "${CLAUDE_TOOL_COMMAND:=}"
: "${CLAUDE_TOOL_FILE_PATH:=}"

export CODEX_TOOL_COMMAND="$CLAUDE_TOOL_COMMAND"
export CODEX_TOOL_FILE_PATH="$CLAUDE_TOOL_FILE_PATH"

exec "$@" <<<"$input"
