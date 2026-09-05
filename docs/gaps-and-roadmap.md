# Gaps And Roadmap

This document records what Curo currently is, what it does not yet implement,
and the order for extending it. It prevents a documented policy from being
mistaken for an already-enforced capability.

## Current status

| Area | Status | Meaning |
|---|---|---|
| Operating standard | Ready | Human-readable governing rules exist. |
| Kickoff templates | Ready | Human and machine-readable project intake exists. |
| Core policies | Ready | Ownership, precedence, and validation rules exist. |
| Provenance and replay schemas | Foundation | Contracts exist; a project must implement the writers and validators. |
| Observability layer | Foundation | Run records, indexes, event contracts, evidence links, and HITL boundaries exist; runtime emitters remain project-specific. |
| Executable runtime | Planned | No universal Curo runtime is included yet. |
| Curo package self-check | Ready | `scripts/validate_curo.py` checks basic foundation integrity. |
| Project command-line validation scripts | Planned | Projects must provide or adopt verified domain scripts. |
| Tools, MCP, and hooks | Extension area | Contracts and permissions must be defined per project before use. |
| Evaluation runner | Planned | Project-specific evaluation cases and runners are still required. |
| Review and promotion automation | Foundation | Event-triggered exception review, batched findings, correction limits, and HITL packet contracts exist; runtime automation remains project-specific. |
| Learning and distillation | Foundation | Evidence-backed candidate and promotion contracts exist; automated distillation remains project-specific. |

## Required project extensions

Every new project should add only the extensions it needs:

- `contracts/` for domain-specific schemas
- `runtime/` or `server/harness/` for execution control
- `scripts/` for deterministic checks and preflight
- `tools/`, `mcp/`, and `hooks/` for authorized capabilities
- `evaluations/` for expected behavior and failure cases
- `provenance/` and `replay/` for run evidence
- `learning/` for evidence-backed proposals and promotion records

## Recommended build order

1. Validate the kickoff brief against [`../schemas/project-kickoff.schema.json`](../schemas/project-kickoff.schema.json).
2. Freeze the project ownership table and canonical contracts.
3. Build the smallest deterministic or fake-adapter slice.
4. Add project-specific runtime enforcement.
5. Add tools, MCP servers, and hooks only with explicit permissions.
6. Add evaluations for success, failure, cancellation, provenance, and portability where applicable.
7. Add provenance and replay writers.
8. Run package integrity and promotion checks.
9. Use Exception Review Mode only when a qualifying event occurs; return to the prior workflow state after resolution.
10. Promote reusable patterns back into Curo only after evidence from more than one project.

## Promotion rule

A project artifact should become part of Curo only when it is reusable across
projects, has an explicit owner, has deterministic checks where feasible, has
documented failure behavior, and has evidence that it works independently of a
single provider or framework.
