# Skill: Model Package Design

## Purpose

Design portable, model-agnostic task packages that separate semantic instructions, configuration/state, structured records, event history, and deterministic validation.

This is a Curo extension. It does not redefine Curo core.

## Representation policy

Use the representation that best matches the information type:

| Information | Preferred representation |
|---|---|
| Mission / instructions | Markdown |
| Architecture explanation | Markdown |
| Behavioral rules | Markdown |
| Examples | Markdown |
| Current goal | YAML |
| Project configuration | YAML |
| Agent assignments | YAML |
| Research / working state | YAML |
| Decisions / typed records | JSON |
| Evidence records | JSON |
| Tool / API messages | JSON |
| Append-only event ledger | JSONL |
| Validation requirements | JSON Schema |
| Human reports | Markdown |
| Tiny terse handoffs | Plain text |

## Core rule

> Do not encode rich semantics into structured data merely because structured data is available.

A behavioral rule such as “the critic must surface contradictory evidence and may not dismiss it because it conflicts with the preferred architecture” belongs in Markdown. YAML or JSON may reference that rule by stable ID.

## Single-owner rule

> **One semantic fact → one authoritative representation.**

Do not duplicate authoritative state across Markdown, YAML, JSON, and event records.

Bad:

```text
goal.yaml       = OPEN
result.json     = COMPLETE
INSTRUCTIONS.md = WAITING_FOR_REVIEW
```

Good:

```text
goal.yaml = authoritative current goal state
INSTRUCTIONS.md = explains how state transitions work
result.json = reports output, not competing goal state
```

## Recommended package shape

```text
/project-package
├── package.yaml
├── INSTRUCTIONS.md
├── goal.yaml
├── context.yaml
├── constraints.yaml
├── research-plan.yaml
├── agents.yaml
├── schemas/
│   ├── evidence.schema.json
│   ├── decision.schema.json
│   └── result.schema.json
├── events.jsonl
└── artifacts/
```

## Self-describing manifest

```yaml
package:
  id: PKG-001
  type: research
  version: 1.0.0

entrypoints:
  instructions: INSTRUCTIONS.md
  goal: goal.yaml
  context: context.yaml

contracts:
  evidence: schemas/evidence.schema.json
  decision: schemas/decision.schema.json

events:
  ledger: events.jsonl
```

A model must not have to guess which file to read first, which records are authoritative, which are examples, or which outputs must validate.

## Authority precedence

For structural conflicts:

```text
JSON Schema > explicit machine state > package manifest > Markdown instructions > examples
```

For semantic/behavioral conflicts:

```text
Curo core identity / approved rules > package instructions > role instructions > task examples
```

Schemas validate shape; they do not automatically become the source of behavioral meaning.

## Package-design workflow

1. Identify semantic instructions and behavioral constraints.
2. Identify current configuration and mutable state.
3. Identify typed records and evidence.
4. Identify append-only events.
5. Identify fields that require deterministic validation.
6. Assign one canonical owner to each semantic fact.
7. Create or update `package.yaml` with explicit entrypoints and contracts.
8. Check for duplicated authority.
9. Check model/provider neutrality.
10. Run the Curo drift check if the package introduces a new capability category.

## Completion criteria

A package is ready when:

- a human can understand the intent from Markdown;
- a model can identify entrypoints without guessing;
- mutable state is explicit;
- typed outputs are machine-readable;
- append-only history is independently parseable where required;
- schemas validate enforceable contracts;
- no authoritative fact has conflicting owners;
- provider-specific details are isolated behind adapters/configuration;
- the package remains an extension rather than redefining Curo.
