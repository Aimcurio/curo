# Curo Project Kickoff

Copy this file into the new project, complete the sections marked `REQUIRED`,
and leave uncertain items as `UNKNOWN` or `DECISION_REQUIRED`. Do not replace
unknown information with assumptions.

## 1. Project identity

- Project name: `REQUIRED`
- One-sentence description: `REQUIRED`
- Requester / decision owner: `REQUIRED`
- Working directory or repository: `REQUIRED`
- Target start date: `OPTIONAL`
- Desired first release date: `OPTIONAL`

## 2. Objective

What problem should this project solve?

```text
REQUIRED: Describe the user, the problem, and the intended outcome.
```

What is explicitly out of scope?

```text
REQUIRED: List exclusions so scope cannot expand silently.
```

## 3. Version 1 scope

### Must have

- `REQUIRED: Feature or behavior`
- `REQUIRED: Feature or behavior`
- `OPTIONAL: Feature or behavior`

### Later

- `OPTIONAL: Deferred feature`
- `OPTIONAL: Deferred feature`

### Explicitly excluded

- `REQUIRED: Excluded feature or behavior`

## 4. Users and usage

- Primary user: `REQUIRED`
- User skill level: `REQUIRED`
- Main usage environment: `REQUIRED`
- Expected usage frequency or volume: `OPTIONAL`
- Accessibility requirements: `OPTIONAL`
- Languages or locales: `OPTIONAL`

## 5. Target environment

- Product type: `REQUIRED: browser, desktop, mobile, API, internal tool, etc.`
- Platforms: `REQUIRED`
- Existing repository: `REQUIRED: path or NEW_PROJECT`
- Deployment target: `REQUIRED or DECISION_REQUIRED`
- Authentication: `REQUIRED or NOT_NEEDED_FOR_V1`
- External services: `OPTIONAL`

## 6. Execution profile

- System type: `REQUIRED: deterministic, ai_assisted, or hybrid`
- AI assistance used: `REQUIRED: yes/no`
- Mutation level: `REQUIRED: read_only, reversible, or irreversible`
- Safety criticality: `REQUIRED: low, medium, or high`
- Runtime required: `REQUIRED: no, planned, or existing`

Use `deterministic` and `NOT_APPLICABLE` for projects that do not use a model.
Use `hybrid` when deterministic components establish facts and a model only
proposes interpretations or content.

## 7. UX and visual direction

- Primary layout: `REQUIRED`
- Visual direction: `REQUIRED`
- Responsive behavior: `REQUIRED`
- Important interaction states: `REQUIRED`
- Reference links or images: `OPTIONAL`
- Content or brand constraints: `OPTIONAL`

For an interactive workflow, explicitly decide whether Version 1 includes the
following capabilities where applicable:

- multiple sessions or work items
- streaming or incremental results
- cancellation or early termination
- retry
- provider, model, or component selection
- attachments
- tool calls
- voice
- structured or rich result rendering

Mark each item `IN`, `LATER`, or `OUT`.

## 8. Provider and model direction

- Initial provider: `REQUIRED, NOT_APPLICABLE, or FAKE_ADAPTER_FIRST`
- Initial model: `OPTIONAL, NOT_APPLICABLE, or UNKNOWN`
- Future provider portability required: `REQUIRED: yes/no`
- Provider credentials available through secure setup: `REQUIRED or NOT_YET`
- Provider-specific features allowed in Version 1: `REQUIRED`

Never paste credentials into this brief, chat, source files, or screenshots.

## 9. Data, privacy, and retention

- Data that may be entered: `REQUIRED`
- Data that may be stored: `REQUIRED`
- Storage location: `REQUIRED or DECISION_REQUIRED`
- Retention period: `REQUIRED or UNKNOWN`
- User deletion requirement: `REQUIRED`
- Raw provider response retention: `REQUIRED`
- Sensitive or regulated data involved: `REQUIRED: yes/no/unknown`
- Provider data-use constraints: `OPTIONAL`

## 10. Ownership decisions

Fill in the decision owner when it differs from the Curo default.

| Concern | Owner | Notes |
|---|---|---|
| Objective | Human / authorized caller | `REQUIRED` |
| UI state | Application state manager | `REQUIRED` |
| Execution state | Harness | `REQUIRED` |
| Provider translation | Adapter | `REQUIRED` |
| Validation result | Deterministic validator | `REQUIRED` |
| Provenance | Harness | `REQUIRED` |
| Replay manifest | Harness | `REQUIRED` |
| Pending product decisions | Human / authorized caller | `REQUIRED` |

## 11. Acceptance criteria

Write observable conditions, not aspirations.

- `REQUIRED: A user can ...`
- `REQUIRED: The system records ...`
- `REQUIRED: A failure results in ...`
- `REQUIRED: The system must not ...`

Define what makes the primary workflow `complete`, `failed`, and `cancelled`.
Completion must be based on an observed completion condition, not model or
agent self-report or the absence of more output.

## 12. Required failure cases

Choose at least one test for each applicable category:

- normal successful response
- cancellation or early termination
- dependency timeout or failure
- missing or unverifiable provenance
- component replacement

For each case, specify the expected state, user-visible behavior, evidence to
capture, and whether retry is allowed.

## 13. Approval boundaries

The builder may decide without additional approval:

- `REQUIRED: ordinary implementation decisions`

The requester must approve:

- `REQUIRED: scope changes`
- `REQUIRED: data or privacy changes`
- `REQUIRED: provider or deployment changes`
- `REQUIRED: irreversible or public actions`

## 14. Kickoff instruction

The kickoff is intake, not an operational assignment contract. Record only the
handoff information needed to draft the project-specific profile:

- `project_profile_required`: `true | false`
- `assignment_manifest_required`: `true | false`
- `known_roles`: `OPTIONAL list`
- `capability_requirements`: `OPTIONAL list`
- `data_classification_constraints`: `OPTIONAL list`
- `human_decisions_required`: `OPTIONAL list`

The governed handoff is:

```text
kickoff completed
    -> project profile proposed
    -> project profile reviewed
    -> project profile approved
    -> LLM/agent assignments compiled and validated
    -> bounded implementation authorized
```

The kickoff must not contain the full assignment contract. The approved
project profile owns project intent; the assignment manifest is derived from
and hash-bound to that profile; run and provenance records own observed
execution identity.

Use this brief with the following instruction:

```text
Use the Curo operating standard at the configured Curo root as the governing reference.
First propose a project-specific profile for review. Do not compile assignments
until the profile is approved. Then produce the ownership table, canonical
contracts, bounded implementation phases, validation gates, and an
evidence/replay plan.

If execution is in scope, define a structured executable and ordered arguments. State separately whether reproducibility needs process re-execution, historical artifact verification, or both; do not use a shell command string as the canonical replay contract.
Do not begin implementation until REQUIRED decisions are resolved or
explicitly marked UNKNOWN. Keep model output as proposal data until the
harness or deterministic validators establish authoritative facts.
```

## 15. Initial project record

- Brief status: `DRAFT | READY_FOR_DESIGN | BLOCKED`
- Open decisions: `REQUIRED`
- Known risks: `REQUIRED`
- First implementation slice: `REQUIRED`
- Template version: `1.2.0`
- Project brief version: `0.1.0`
- Updated: `2026-09-07`
