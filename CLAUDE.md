# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of Codex/Claude Code skills that extend AI agent capabilities through modular, self-contained packages. Skills are organized in the `/skills/` directory with each skill containing a `SKILL.md` file (YAML frontmatter + markdown instructions) and optional bundled resources (scripts, references, assets).

## Architecture

### Skill Structure

Each skill follows this pattern:
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name + description)
│   └── Markdown instructions
└── Optional: scripts/, references/, assets/
```

**Key principles:**
- Skills use progressive disclosure: metadata (always loaded) → SKILL.md body (when triggered) → bundled resources (as needed)
- The `description` field in YAML frontmatter is the primary triggering mechanism
- Skills should be concise - context window is a shared resource

### Skill Types in this Repo

1. **Planning skills** (`planner`, `plan-harder`, `swarm-planner`, `llm-council`)
   - Produce implementation plans before coding
   - Define phased execution and task-level validation
   - For `swarm-planner`, enforce explicit `depends_on` dependency maps

2. **Execution skills** (`parallel-task`, `parallel-task-spark`, `super-swarm-spark`)
   - Execute plan files with subagents
   - `parallel-task` and `parallel-task-spark` are dependency-aware (unblocked wave execution)
   - `super-swarm-spark` is a rolling-pool high-throughput executor that intentionally ignores dependency maps and expects orchestrator-side conflict resolution

3. **Documentation access skills** (`context7`, `openai-docs-skill`, `read-github`, `markdown-url`)
   - Fetch up-to-date docs and repo references
   - Query documentation via APIs or MCP servers
   - Convert URLs into LLM-friendly formats

4. **Domain expertise skills** (`frontend-design`, `frontend-responsive-ui`, `vercel-react-best-practices`)
   - Provide specialized patterns and best practices
   - Imported from authoritative sources (Anthropic, Vercel)

5. **Tool integration skills** (`agent-browser`, `gemini-computer-use`)
   - Browser automation and computer control
   - Integrate external tools into agent workflows

6. **Workflow utility skills** (`role-creator`, `tdd-test-writer`)
   - Manage Codex role configuration
   - Support test-first implementation workflows

## Working with Skills

### Creating New Skills

Use the skill-creator workflow (available via `/skill-creator` or from `~/.claude/skills/skill-creator`):

1. **Understand concrete examples** - How will users invoke this skill?
2. **Plan reusable contents** - What scripts/references/assets are needed?
3. **Initialize**: `python3 /path/to/skill-creator/scripts/init_skill.py <skill-name> --path ./skills`
4. **Edit SKILL.md**:
   - Write comprehensive `description` in YAML frontmatter (this triggers the skill)
   - Keep instructions concise and imperative
   - Move detailed content to `references/` files if SKILL.md approaches 500 lines
5. **Package**: `python3 /path/to/skill-creator/scripts/package_skill.py ./skills/<skill-name>`

**Important**: The `description` field must include both what the skill does AND when to use it. Only content in the description is available before the skill triggers.

### Modifying Existing Skills

1. Read the skill's SKILL.md to understand current structure
2. For prompts being converted to skills (like `/prompts/*.md`):
   - Optimize for conciseness (remove verbosity, keep essential workflow)
   - Extract the "when to use" triggers for the description field
   - Use imperative/infinitive form for instructions
3. Test the skill, then package it

### Installing Skills

**Via [skills.sh](https://skills.sh) CLI (recommended):**
```bash
# Install specific skills globally
npx skills add am-will/codex-skills --skill <skill-name> -g

# Install to specific agents
npx skills add am-will/codex-skills --skill <skill-name> -a claude-code -g

# List available skills
npx skills add am-will/codex-skills --list
```

**Manual installation:**
```bash
# To Codex
cp -r ./skills/<skill-name> ~/.codex/skills/

# To Claude Code
cp -r ./skills/<skill-name> ~/.claude/skills/
```

## Key Patterns

### Planning/Execution Patterns

- **Planning-first pattern** (`planner`, `plan-harder`, `swarm-planner`, `llm-council`)
  - Intake/clarification
  - Research and dependency modeling
  - Plan generation and review
  - No implementation at this stage

- **Dependency-aware execution pattern** (`parallel-task`, `parallel-task-spark`)
  - Parse task graph (`depends_on`)
  - Launch only unblocked tasks in parallel waves
  - Validate each wave, update plan state, repeat

- **Rolling-pool execution pattern** (`super-swarm-spark`)
  - Keep worker pool saturated for throughput
  - Relationship metadata is awareness-only (not a launch blocker)
  - Orchestrator resolves dependency/integration conflicts at the tail end

**Important for llm-council**: Do NOT yield/finish the response until the full 30-minute timer completes and `final-plan.md` is saved. The session must stay open to prevent premature termination.

### Progressive Disclosure Pattern

When a skill supports multiple variations (frameworks, domains, etc.):
- Keep core workflow in SKILL.md
- Move variant-specific details to `references/<variant>.md`
- Reference these files clearly from SKILL.md with "when to read" guidance

Example: `llm-council` has `references/rubric.md` and `references/templates/` that are loaded as needed.

## Distribution

Skills follow the [Agent Skills standard](https://skills.sh) and can be installed via the skills.sh CLI:

```bash
npx skills add am-will/codex-skills --skill <skill-name> -g
```

Skills are also packaged as `.skill` files (zip archives with `.skill` extension) containing the skill directory structure for manual distribution.
