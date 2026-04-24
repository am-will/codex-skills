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

json_get() {
  local expr="$1"
  jq -r "$expr" <<<"$input" 2>/dev/null || true
}

export CODEX_SESSION_ID="$(json_get '.session_id // empty')"
export CODEX_TURN_ID="$(json_get '.turn_id // empty')"
export CODEX_TRANSCRIPT_PATH="$(json_get '.transcript_path // empty')"
export CODEX_CWD="$(json_get '.cwd // empty')"
export CODEX_PROJECT_DIR="${CODEX_CWD:-$(pwd)}"
export CODEX_HOOK_EVENT_NAME="$(json_get '.hook_event_name // empty')"
export CODEX_MODEL="$(json_get '.model // empty')"
export CODEX_PERMISSION_MODE="$(json_get '.permission_mode // empty')"
export CODEX_SOURCE="$(json_get '.source // empty')"
export CODEX_PROMPT="$(json_get '.prompt // empty')"
export CODEX_STOP_HOOK_ACTIVE="$(json_get '.stop_hook_active // empty')"
export CODEX_LAST_ASSISTANT_MESSAGE="$(json_get '.last_assistant_message // empty')"

export CODEX_CALL_ID="$(json_get '.call_id // empty')"
export CODEX_TOOL_USE_ID="$(json_get '.tool_use_id // empty')"
export CODEX_TOOL_NAME="$(json_get '.tool_name // empty')"
export CODEX_TOOL_KIND="$(json_get '.tool_kind // empty')"
export CODEX_DURATION_MS="$(json_get '.duration_ms // empty')"
export CODEX_EXECUTED="$(json_get '.executed // empty')"
export CODEX_SUCCESS="$(json_get '.success // empty')"
export CODEX_MUTATING="$(json_get '.mutating // empty')"
export CODEX_SANDBOX="$(json_get '.sandbox // empty')"
export CODEX_SANDBOX_POLICY="$(json_get '.sandbox_policy // empty')"
export CODEX_OUTPUT_PREVIEW="$(json_get '.output_preview // empty')"

tool_input_raw="$(json_get '.tool_input // empty')"
export CODEX_TOOL_INPUT="$tool_input_raw"

extract_patch_paths() {
  local patch_text="$1"
  awk '
    /^\*\*\* (Add|Update|Delete) File: / {
      sub(/^\*\*\* (Add|Update|Delete) File: /, "");
      print;
      next;
    }
    /^\*\*\* Move to: / {
      sub(/^\*\*\* Move to: /, "");
      print;
    }
  ' <<<"$patch_text" | awk 'NF && !seen[$0]++'
}

if [[ "$CODEX_HOOK_EVENT_NAME" == "PreToolUse" ]]; then
  export CODEX_TOOL_COMMAND="$(json_get '.tool_input.command // empty')"
  export CODEX_TOOL_FILE_PATH="$(json_get '.tool_input.file_path // empty')"
else
  if [[ -n "$tool_input_raw" && "$tool_input_raw" != "null" ]]; then
    tool_input_type="$(jq -r '.tool_input | type? // empty' <<<"$input" 2>/dev/null || true)"
    if [[ "$tool_input_type" == "object" || "$tool_input_type" == "array" ]]; then
      tool_input_json="$tool_input_raw"
    else
      tool_input_json="$(jq -r 'try fromjson catch empty' <<<"$tool_input_raw" 2>/dev/null || true)"
    fi
    if [[ -n "$tool_input_json" ]]; then
      export CODEX_TOOL_INPUT_JSON="$tool_input_json"
      export CODEX_TOOL_FILE_PATH="$(jq -r 'try (.file_path // .path // .destination // .params.file_path // .params.path // empty) catch ""' <<<"$tool_input_json" 2>/dev/null || true)"
      export CODEX_TOOL_COMMAND="$(jq -r 'try (.command // (.params.command | join(" ")) // empty) catch ""' <<<"$tool_input_json" 2>/dev/null || true)"
    fi
  fi
fi

: "${CODEX_TOOL_COMMAND:=}"
: "${CODEX_TOOL_FILE_PATH:=}"

if [[ -z "$CODEX_TOOL_FILE_PATH" && "$CODEX_TOOL_NAME" == "apply_patch" && -n "$CODEX_TOOL_COMMAND" ]]; then
  patch_paths="$(extract_patch_paths "$CODEX_TOOL_COMMAND")"
  if [[ -n "$patch_paths" ]]; then
    export CODEX_TOOL_FILE_PATH="$(head -n 1 <<<"$patch_paths")"
    export CODEX_TOOL_FILE_PATHS="$patch_paths"
  fi
fi

export CODEX_TOOL_INPUT_FILE="$CODEX_TOOL_FILE_PATH"

exec "$@" <<<"$input"
