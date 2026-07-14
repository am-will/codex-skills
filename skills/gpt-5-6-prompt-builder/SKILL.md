---
name: gpt-5-6-prompt-builder
description: Build, transform, audit, and migrate prompts for GPT-5.6 Sol using outcome-first contracts, explicit success criteria, evidence and tool rules, approval boundaries, output requirements, and stop conditions. Use when someone asks for a GPT-5.6 prompt, wants an existing prompt optimized for GPT-5.6, or needs a prompt stack adapted from an older model.
---

# GPT-5.6 Prompt Builder

Build prompts for GPT-5.6 Sol from a complete task contract. The model should receive the destination, the completion bar, the evidence it may use, the boundaries it must respect, and the output it must return. It should retain freedom to choose an efficient path.

This skill is based on OpenAI's [Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6). If the user asks about current model limits, pricing, API fields, or feature availability, consult the current GPT-5.6 model documentation separately; do not infer those details from this skill.

## Operating contract

1. Determine whether the request is to create, transform, audit, or migrate a prompt.
2. Extract known information from the user's request and any attached prompt, traces, schemas, tool descriptions, or examples.
3. Run the completeness gate below before writing the final prompt.
4. If a behavior-critical field is missing, stop prompt construction and ask for the smallest useful missing information. Use `request_user_input` when available; otherwise ask concise plain-text questions. Ask at most three high-value questions per round, then reassess.
5. Do not ask for permission to draft once the contract is complete. Do not invent missing requirements, tool capabilities, evidence, thresholds, or approval policy.
6. When the contract is complete, produce one execution-ready prompt. Do not bury the prompt in a long essay or provide several competing drafts unless the user asks for variants.

## Completeness gate

Treat a field as complete only when its absence would not change the model's behavior. Some fields can be `not applicable`, but that decision must be explicit for high-risk or tool-using tasks.

Required for every prompt:

- **Execution target:** GPT-5.6 Sol or GPT-5.6 family; API/agent/runtime surface; where the prompt will live (system, developer, user, or a stack); and whether `text.verbosity` or reasoning effort is configured outside the prompt.
- **Role and context:** what the model is responsible for and the relevant product, project, audience, or operating context.
- **Goal:** the user-visible outcome, stated as a destination rather than a prescribed procedure.
- **Success criteria:** observable conditions that must be true before the model finishes, including required decisions, actions, artifacts, fields, or citations.
- **Constraints and guardrails:** policy, safety, privacy, business, scope, evidence, side-effect, and resource limits. Identify true invariants separately from judgment calls.
- **Autonomy and approval:** what safe local/read-only work is authorized; what in-scope changes are authorized; and what requires confirmation, especially external writes, destructive actions, purchases, costly operations, or scope expansion.
- **Evidence and source of truth:** inputs the model may rely on, required retrieval, citation rules, freshness requirements, and what to do when evidence is absent, conflicting, partial, or suspicious.
- **Tools:** available tools, routing rules, prerequisites, important return fields, error/fallback behavior, and tools that are out of scope. If no tools are available, say so.
- **Output contract:** required sections or schema, format, language, length/detail, tone, and facts or structure to preserve.
- **Stop rules:** when to answer, ask, retry, fall back, abstain, report a blocker, or stop. Include any retry limits and the definition of “enough evidence.”
- **Validation:** how the result will be checked before completion, and what to report when validation cannot run.

Additional fields for migrations or transformations:

- the existing prompt or prompt stack, verbatim;
- current model and reasoning setting;
- representative inputs and outputs or failure traces;
- the measured regression or behavior to preserve;
- available evals and the comparison method;
- which changes are in scope.

Ask only about missing fields that can change behavior. Do not force the user to specify an implementation path when the desired outcome and constraints are sufficient. Do not accept vague labels such as “be smart,” “be helpful,” “be concise,” or “use good judgment” without translating them into observable behavior when that behavior matters.

## Questioning protocol

When information is missing, use this order:

1. Resolve the goal and completion bar.
2. Resolve safety, authority, side effects, and approval boundaries.
3. Resolve evidence, tools, and prerequisites.
4. Resolve output shape, tone, and detail.
5. Resolve validation and stop conditions.

Prefer questions that offer a concrete answer shape. For example:

- “What must be true for this to count as complete? Please list the required actions, decisions, or output fields.”
- “Which actions may the model take without asking, and which require confirmation? Include external writes, destructive actions, purchases, or scope expansion.”
- “What evidence may it use, which sources are authoritative, and what should it do when the evidence is missing or conflicting?”

If a user provides an incomplete prompt but asks for an immediate draft, return `Prompt readiness: BLOCKED` and ask the missing questions instead of silently filling the gaps. If the user explicitly authorizes reasonable assumptions, record each assumption in the final prompt's assumptions section and keep assumptions conservative.

## Transformation rules

When the gate passes, rewrite the prompt using these rules:

- Lead with the outcome and completion bar. Describe the destination; let GPT-5.6 choose an efficient path.
- Keep required constraints, safety/business/evidence/permission rules, tool routing, output shape, and validation. Remove repeated instructions, redundant examples, obsolete scaffolding, irrelevant tools, and process narration that does not change behavior.
- Review for contradictions. Resolve conflicts explicitly using priority order rather than repeating both rules.
- Use `MUST`, `NEVER`, `ALWAYS`, and `ONLY` only for true invariants. Use decision rules for judgment calls such as when to search, ask, retry, use a tool, or continue.
- Preserve explicit user values. When a value is implicit, provide decision criteria; do not invent universal defaults, keyword maps, or broad semantic shortcuts.
- Define personality and collaboration style separately and briefly. Specify writing choices and action behavior instead of relying on labels like “friendly” or “empathetic.”
- If brevity matters, state what must be preserved and what may be omitted. Do not add a generic “be concise” instruction unless it changes the required output.
- Put autonomy and approval policy in one compact section. Name safe local actions and distinguish research, design, implementation, review, and external coordination.
- Require prerequisite discovery, retrieval, and validation before an action when correctness depends on them. Parallelize independent reads; keep decision-dependent work sequential.
- If evidence is required, define what counts as support, attach citations to supported claims, label inference, state conflicts, and report missing evidence instead of guessing.
- If a tool result is empty, partial, or suspiciously narrow, specify meaningful fallbacks and a bounded retry policy.
- For long-running or tool-heavy work, require a short visible preamble before the first tool call and sparse updates only at major phase changes. Do not ask for narration of routine tool calls.
- For reusable prompt stacks, keep stable prefixes stable and avoid unnecessary churn; use explicit cache breakpoints only when measured cache behavior and cost improve.
- Ask for the smallest missing field when required evidence or input is absent. Do not force a guess merely to keep moving.
- Do not request hidden chain-of-thought. Request concise decisions, evidence, assumptions, validation results, and blockers when they are needed by the user.

## Canonical prompt shape

Use this structure for the generated prompt. Keep sections short and add detail only where it changes behavior. Add `Context and evidence`, `Autonomy and approvals`, or `Validation` when they carry behavior-critical information.

```text
Role: [function and relevant context]

Personality: [tone, directness, formality, warmth, and polish]
Collaboration: [when to ask, assume, take initiative, explain tradeoffs, check work, and handle uncertainty]

Goal: [user-visible outcome]

Context and evidence:
- [authoritative inputs and available artifacts]
- [retrieval/citation/freshness rules]

Success criteria:
- [observable completion condition]
- [observable completion condition]

Constraints:
- [true invariants: safety, policy, privacy, business, scope, or evidence]
- [limits on side effects, cost, time, or data handling]

Autonomy and approvals:
- [safe actions authorized without asking]
- [actions requiring confirmation]

Tools:
- [tool and when to use it]
- [prerequisites, important return fields, errors, and fallbacks]
- [tools or routes not to use]

Output:
- [required format, sections/schema, language, length/detail, and tone]
- [facts, structure, or artifact to preserve]

Validation:
- [checks required before completion]
- [what to report if validation cannot run]

Stop rules:
- [answer when the core request has sufficient evidence]
- [ask for the smallest missing input when blocked]
- [bounded retries/fallbacks]
- [abstain, report blockers, or stop conditions]
```

## Task-specific additions

Use only the additions that apply:

- **Coding/build/fix:** require targeted tests for changed behavior, type/lint checks when applicable, affected-package builds, and a minimal smoke test when full validation is too expensive. If validation cannot run, require the reason and next-best check.
- **Visual/frontend:** require preservation of the existing design system, responsive behavior, and expected states; forbid unrequested decorative features; require rendering and inspection for clipping, spacing, missing content, and consistency before finalizing.
- **Research/synthesis:** require citations only from retrieved sources, claim-level support, separate labels for inference and direct fact, conflict reporting, and narrowing/reporting missing evidence instead of guessing.
- **Editing/rewriting/summarization:** require preservation of the requested artifact, length, structure, genre, and factual claims before improving clarity or flow; forbid new claims, sections, or promotional tone unless requested.
- **Implementation planning:** require requirements, named files/resources, state transitions or data flow, validation, failure behavior, privacy/security considerations, and material open questions.
- **Bounded programmatic tool work:** define the bounded stage, eligible read-only tools, compact output schema, retry limit, stop condition, and one handoff back to direct model judgment. Do not use programmatic calling for semantic judgment, approvals, citations, or final validation.
- **Migration from an older model:** preserve the current reasoning setting as the baseline, run representative evals first, remove one class of obsolete scaffolding at a time, make the smallest targeted change for a measured regression, and rerun the same evals after each change. Do not rewrite a working prompt stack all at once.

## Reasoning-effort guidance

Do not use higher reasoning effort to compensate for a missing goal, dependency rule, tool route, success criterion, or validation loop. For migrations, preserve the existing setting as the baseline; compare the same setting and one level lower on representative tasks. Treat `medium` as a balanced starting point, use `low` when latency matters and quality holds, and recommend higher settings only when evals demonstrate a meaningful gain.

## Final response contract

When ready, return:

1. `Prompt readiness: READY`
2. `Execution target` with model/runtime, prompt layer, reasoning effort, and verbosity settings.
3. `GPT-5.6 prompt` as one copyable code block.
4. `Assumptions` only when the user explicitly authorized them; otherwise state `None`.
5. `Validation checklist` with the concrete checks or evals to run.
6. A brief `Applied transformations` note naming only material changes.

When blocked, return:

1. `Prompt readiness: BLOCKED`
2. The smallest set of unanswered questions, grouped by decision impact.
3. A one-sentence explanation of why each answer changes the prompt.

Do not output a falsely complete prompt alongside unresolved behavior-critical questions.
