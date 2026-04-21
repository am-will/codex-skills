#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
from collections import OrderedDict
from pathlib import Path

SOURCE_ROOT = Path(
    os.environ.get(
        "AITMPL_HOOKS_SOURCE",
        "/tmp/upstream-hook-templates/cli-tool/components/hooks",
    )
)
OUTPUT_ROOT = Path(__file__).resolve().parent
SHARED_WRAPPER_SRC = OUTPUT_ROOT / "_shared" / "run-with-hook-env.sh"

SUPPORTED_EVENTS = (
    "PreToolUse",
    "PostToolUse",
    "SessionStart",
    "UserPromptSubmit",
    "Stop",
)

EVENT_REMAP = {
    "SessionEnd": "Stop",
    "SubagentStop": "Stop",
    "Notification": "Stop",
    "WorktreeCreate": "SessionStart",
    "WorktreeRemove": "Stop",
}

PRETOOL_ADAPTATIONS = {
    "pre-tool/update-search-year.json": {
        "event": "UserPromptSubmit",
        "approximation": "Prompt-level approximation of the original search-year rewrite hook.",
    },
    "pre-tool/backup-before-edit.json": {
        "event": "PostToolUse",
        "approximation": "Best-effort backup after the edit completes; Codex cannot prehook Edit/MultiEdit.",
    },
    "pre-tool/console-log-cleaner.json": {
        "event": "PostToolUse",
        "approximation": "Warns after file edits instead of before them.",
    },
    "development-tools/file-backup.json": {
        "event": "PostToolUse",
        "approximation": "Backs up edited files after the tool finishes instead of before.",
    },
    "quality-gates/plan-gate.json": {
        "event": "PostToolUse",
        "approximation": "Plan reminder runs after file edits instead of before them.",
    },
    "quality-gates/tdd-gate.json": {
        "event": "PostToolUse",
        "approximation": "TDD reminder runs after file edits instead of before them.",
    },
    "security/file-protection.json": {
        "event": "PostToolUse",
        "approximation": "Protection warnings are emitted after the edit/write completes.",
    },
}


def main() -> None:
    if not SOURCE_ROOT.exists():
        raise SystemExit(f"source tree not found: {SOURCE_ROOT}")
    if not SHARED_WRAPPER_SRC.exists():
        raise SystemExit(f"shared wrapper not found: {SHARED_WRAPPER_SRC}")

    bundles = []
    for source_json in sorted(SOURCE_ROOT.rglob("*.json")):
        if source_json.name == "HOOK_PATTERNS_COMPRESSED.json":
            continue
        data = json.loads(source_json.read_text())
        if "hooks" not in data:
            continue
        bundles.append(generate_bundle(source_json, data))

    write_json(OUTPUT_ROOT / "catalog.json", {"sourceRoot": str(SOURCE_ROOT), "bundles": bundles})
    write_root_readme(bundles)


def generate_bundle(source_json: Path, data: dict) -> dict:
    rel_json = source_json.relative_to(SOURCE_ROOT)
    bundle_name = rel_json.with_suffix("")
    bundle_dir = OUTPUT_ROOT / bundle_name
    bundle_dir.mkdir(parents=True, exist_ok=True)

    bundle_hooks_dir = bundle_dir / ".codex" / "hooks"
    bundle_hooks_dir.mkdir(parents=True, exist_ok=True)
    copy_shared_wrapper(bundle_hooks_dir / "_shared" / "run-with-hook-env.sh")

    metadata = OrderedDict()
    metadata["sourcePath"] = str(rel_json)
    metadata["name"] = "/".join(bundle_name.parts)
    metadata["description"] = data.get("description", "")

    hooks_out: dict[str, list[dict]] = {event: [] for event in SUPPORTED_EVENTS}
    event_notes = []
    direct = True
    rel_json_key = rel_json.as_posix()

    if rel_json_key == "pre-tool/update-search-year.json":
        direct = False
        event_notes.append(
            "PreToolUse/WebSearch was rewritten as a UserPromptSubmit approximation."
        )
        script_name = script_filename(rel_json, "user-prompt-submit", "user-prompt-submit", 0, 0)
        script_path = bundle_hooks_dir / script_name
        write_update_search_year_script(script_path)
        user_prompt_groups = [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": f"./.codex/hooks/{script_name}",
                    }
                ]
            }
        ]
        hooks_out = {"UserPromptSubmit": user_prompt_groups}
        write_json(bundle_dir / "hooks.json", {"hooks": hooks_out})
        write_bundle_readme(bundle_dir, rel_json, data, hooks_out, event_notes, direct)
        write_bundle_manifest(bundle_dir, rel_json, data, hooks_out, event_notes, direct)
        copy_supporting_files(
            source_json,
            data.get("supportingFiles", []),
            bundle_dir,
            data["hooks"],
        )
        return OrderedDict(
            sourcePath=str(rel_json),
            bundlePath=str(bundle_name),
            description=data.get("description", ""),
            compatibility="adapted",
            events=list(hooks_out.keys()),
            notes=event_notes,
        )

    for source_event, matcher_groups in data["hooks"].items():
        mapped_event = EVENT_REMAP.get(source_event, source_event)
        if mapped_event not in SUPPORTED_EVENTS:
            continue
        if source_event == "PreToolUse":
            adapt = PRETOOL_ADAPTATIONS.get(str(rel_json))
            if adapt is not None:
                mapped_event = adapt["event"]
                direct = False
                event_notes.append(f"{source_event} -> {mapped_event}: {adapt['approximation']}")
            else:
                if any(
                    (group.get("matcher") not in (None, "Bash", "*"))
                    for group in matcher_groups
                ):
                    direct = False
                    mapped_event = "PostToolUse"
                    event_notes.append(
                        f"{source_event} on non-Bash matchers was remapped to PostToolUse."
                    )
        elif source_event != mapped_event:
            direct = False
            event_notes.append(f"{source_event} -> {mapped_event}")

        for group_index, group in enumerate(matcher_groups):
            matcher = group.get("matcher")
            hooks_out[mapped_event].append(
                build_group(
                    bundle_dir=bundle_dir,
                    bundle_hooks_dir=bundle_hooks_dir,
                    source_json=source_json,
                    rel_json=rel_json,
                    source_event=source_event,
                    mapped_event=mapped_event,
                    matcher=matcher,
                    hooks=group.get("hooks", []),
                    group_index=group_index,
                )
            )

    hooks_out = {event: groups for event, groups in hooks_out.items() if groups}
    write_json(bundle_dir / "hooks.json", {"hooks": hooks_out})
    write_bundle_readme(bundle_dir, rel_json, data, hooks_out, event_notes, direct)
    write_bundle_manifest(bundle_dir, rel_json, data, hooks_out, event_notes, direct)
    copy_supporting_files(
        source_json,
        data.get("supportingFiles", []),
        bundle_dir,
        data["hooks"],
    )

    return OrderedDict(
        sourcePath=str(rel_json),
        bundlePath=str(bundle_name),
        description=data.get("description", ""),
        compatibility="direct" if direct and not event_notes else "adapted",
        events=list(hooks_out.keys()),
        notes=event_notes,
    )


def build_group(
    *,
    bundle_dir: Path,
    bundle_hooks_dir: Path,
    source_json: Path,
    rel_json: Path,
    source_event: str,
    mapped_event: str,
    matcher: str | None,
    hooks: list[dict],
    group_index: int,
) -> dict:
    out_group: dict = {}
    if matcher is not None:
        out_group["matcher"] = matcher
    out_group["hooks"] = []
    for hook_index, hook in enumerate(hooks):
        if hook.get("type") != "command":
            raise SystemExit(f"unsupported hook type in {rel_json}: {hook.get('type')}")
        source_command = hook["command"]
        command = rewrite_command(source_command, rel_json)
        script_name = script_filename(rel_json, source_event, mapped_event, group_index, hook_index)
        script_path = bundle_hooks_dir / script_name
        write_wrapper_script(script_path, command, bundle_dir)
        entry = {
            "type": "command",
            "command": f"./.codex/hooks/{script_name}",
        }
        timeout = hook.get("timeout", hook.get("timeoutSec"))
        if timeout is not None:
            entry["timeout"] = timeout
        if hook.get("async"):
            entry["async"] = True
        if hook.get("statusMessage"):
            entry["statusMessage"] = hook["statusMessage"]
        out_group["hooks"].append(entry)
    return out_group


def rewrite_command(command: str, rel_json: Path) -> str:
    if rel_json.as_posix() == "pre-tool/update-search-year.json":
        return ""
    command = re.sub(
        r'"\$(?:CLAUDE|CODEX)_PROJECT_DIR"/\.(?:claude|codex)/hooks/([A-Za-z0-9._-]+(?:\.[A-Za-z0-9._-]+)?)',
        r'"./.codex/hooks/\1"',
        command,
    )
    command = re.sub(
        r'\$(?:CLAUDE|CODEX)_PROJECT_DIR/\.(?:claude|codex)/hooks/([A-Za-z0-9._-]+(?:\.[A-Za-z0-9._-]+)?)',
        r'./.codex/hooks/\1',
        command,
    )
    command = re.sub(
        r'\.(?:claude|codex)/hooks/([A-Za-z0-9._-]+(?:\.[A-Za-z0-9._-]+)?)',
        r'./.codex/hooks/\1',
        command,
    )
    return sanitize_hook_text(command)


def write_wrapper_script(script_path: Path, command: str, bundle_dir: Path) -> None:
    script_path.parent.mkdir(parents=True, exist_ok=True)
    delimiter = pick_delimiter(command)
    body = f"""#!/usr/bin/env bash
set -euo pipefail

bundle_root="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/../.." && pwd)"
command=$(cat <<'{delimiter}'
{command}
{delimiter}
)

cd "$bundle_root"
exec "$bundle_root/.codex/hooks/_shared/run-with-hook-env.sh" -- bash -lc "$command"
"""
    script_path.write_text(body)
    script_path.chmod(0o755)


def write_update_search_year_script(script_path: Path) -> None:
    script_path.parent.mkdir(parents=True, exist_ok=True)
    body = """#!/usr/bin/env bash
set -euo pipefail

input="$(cat)"
prompt="$(jq -r '.prompt // empty' <<<"$input" 2>/dev/null || true)"
current_year="$(date +%Y)"

if [[ -z "$prompt" ]]; then
  exit 0
fi

if [[ "$prompt" =~ (latest|recent|current|new|now|today|search|lookup|find) ]] && ! [[ "$prompt" =~ (20[0-9]{2}) ]]; then
  cat <<JSON
{"continue":true,"systemMessage":"[HOOK FIRED] Add the current year to web searches unless the user asks for a different year.","hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"When you search, prefer $current_year unless the user specifies a year."}}
JSON
fi
"""
    script_path.write_text(body)
    script_path.chmod(0o755)


def pick_delimiter(command: str) -> str:
    delimiter = "__CODEx_HOOK_COMMAND__"
    while delimiter in command:
        delimiter += "_X"
    return delimiter


def copy_shared_wrapper(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SHARED_WRAPPER_SRC, destination)
    destination.chmod(0o755)


def copy_supporting_files(
    source_json: Path,
    supporting_files: list[dict],
    bundle_dir: Path,
    hooks: dict,
) -> None:
    destinations = set()
    for item in supporting_files:
        source = source_json.parent / item["source"]
        destination = bundle_dir / rewrite_destination(item["destination"])
        copy_text_file(source, destination, item.get("executable", False))
        destinations.add(destination)

    for helper in discover_helper_files(source_json.parent, hooks):
        destination = bundle_dir / ".codex" / "hooks" / helper.name
        if destination in destinations:
            continue
        copy_text_file(helper, destination, True)


def rewrite_destination(destination: str) -> str:
    return sanitize_hook_text(destination).lstrip("/")


def discover_helper_files(source_dir: Path, hooks: dict) -> list[Path]:
    helper_names: list[str] = []
    pattern = re.compile(r"\.(?:claude|codex)/hooks/([A-Za-z0-9._-]+\.(?:sh|py))")
    for matcher_groups in hooks.values():
        for group in matcher_groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                helper_names.extend(pattern.findall(command))
    helpers = []
    for helper_name in sorted(set(helper_names)):
        candidate = source_dir / helper_name
        if candidate.exists():
            helpers.append(candidate)
    return helpers


def copy_text_file(source: Path, destination: Path, executable: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    content = sanitize_hook_text(source.read_text())
    if source.name == "change-logger.py":
        content = content.replace(
            '    tool_input = data.get("tool_input", {})\n',
            '    tool_input = data.get("tool_input", {})\n    if isinstance(tool_input, str):\n        try:\n            tool_input = json.loads(tool_input)\n        except json.JSONDecodeError:\n            tool_input = {}\n',
        )
    destination.write_text(content)
    mode = source.stat().st_mode
    destination.chmod(mode | 0o111 if executable else mode & ~0o111)


def script_filename(rel_json: Path, source_event: str, mapped_event: str, group_index: int, hook_index: int) -> str:
    base = rel_json.with_suffix("").as_posix().replace("/", "-")
    return f"{base}-{source_event.lower()}-{mapped_event.lower()}-{group_index + 1}-{hook_index + 1}.sh"


def sanitize_hook_text(content: str) -> str:
    content = content.replace("Claude Code", "Codex")
    content = content.replace("Claude CLI", "Codex CLI")
    content = content.replace("~/.claude/", "~/.codex/")
    content = content.replace("~/.claude", "~/.codex")
    content = content.replace(".claude/hooks/", ".codex/hooks/")
    content = content.replace(".claude/", ".codex/")
    content = content.replace("CLAUDE_", "CODEX_")
    return content


def write_bundle_manifest(
    bundle_dir: Path,
    rel_json: Path,
    data: dict,
    hooks_out: dict[str, list[dict]],
    event_notes: list[str],
    direct: bool,
) -> None:
    manifest = OrderedDict()
    manifest["name"] = rel_json.with_suffix("").as_posix()
    manifest["sourcePath"] = str(rel_json)
    manifest["description"] = data.get("description", "")
    manifest["compatibility"] = "direct" if direct and not event_notes else "adapted"
    manifest["notes"] = event_notes
    manifest["events"] = list(hooks_out.keys())
    manifest["hasSupportingFiles"] = bool(data.get("supportingFiles"))
    write_json(bundle_dir / "bundle.json", manifest)


def write_bundle_readme(
    bundle_dir: Path,
    rel_json: Path,
    data: dict,
    hooks_out: dict[str, list[dict]],
    event_notes: list[str],
    direct: bool,
) -> None:
    lines = [
        f"# {rel_json.with_suffix('').as_posix()}",
        "",
        data.get("description", ""),
        "",
        f"Compatibility: {'direct' if direct and not event_notes else 'adapted'}",
        "",
        "## Events",
    ]
    for event, groups in hooks_out.items():
        lines.append(f"- {event}: {len(groups)} matcher group(s)")
    if event_notes:
        lines.extend(["", "## Notes"])
        lines.extend(f"- {note}" for note in event_notes)
    lines.extend(
        [
            "",
            "## Install",
            "Copy this bundle into a project and merge its `.codex/hooks.json` into your project `.codex/hooks.json`.",
            "If the bundle includes `.codex/hooks/` support files, copy that directory too.",
        ]
    )
    (bundle_dir / "README.md").write_text("\n".join(lines) + "\n")


def write_root_readme(bundles: list[dict]) -> None:
    direct = sum(1 for bundle in bundles if bundle["compatibility"] == "direct")
    adapted = len(bundles) - direct
    lines = [
        "# AITMPL to Codex Hook Catalog",
        "",
        "This catalog mirrors an upstream hook template set and rewrites it into Codex hook bundles.",
        "",
        f"- Bundles: {len(bundles)}",
        f"- Direct: {direct}",
        f"- Adapted: {adapted}",
        "",
        "Each bundle contains:",
        "",
        "- `hooks.json` for Codex",
        "- `.codex/hooks/` support files when the template needs them",
        "- `bundle.json` metadata",
        "- `README.md` install notes",
        "",
        "To install a bundle:",
        "",
        "1. Copy the bundle contents into the project root you want Codex to use.",
        "2. Merge the bundle's `hooks.json` into your project `.codex/hooks.json`.",
        "3. Copy the bundle's `.codex/hooks/` directory into your project `.codex/hooks/`.",
        "",
        "Catalog:",
    ]
    for bundle in bundles:
        lines.append(
            f"- `{bundle['bundlePath']}` - {bundle['compatibility']} - {bundle['description']}"
        )
    (OUTPUT_ROOT / "README.md").write_text("\n".join(lines) + "\n")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
