# Gaps And Roadmap

This document records what Curo currently is, what it does not yet implement,
and the order for extending it. It prevents a documented policy from being
mistaken for an already-enforced capability.

## Current status

| Area | Status | Meaning |
|---|---|---|
| Operating standard | Ready | Human-readable governing rules exist. |
| Kickoff templates | Ready | Human and machine-readable project intake exists. |
| Project profiles | Implemented core | Project-specific intent is schema-governed under `projects/<project-id>/project.yaml`; approval remains human-owned. |
| LLM/agent assignments | Implemented core | Deterministic manifests bind desired/resolved roles to the canonical profile hash; exact provider/model choices remain project decisions. |
| Core policies | Ready | Ownership, precedence, and validation rules exist. |
| Provenance and replay schemas | Implemented | Harness writers validate provenance and the two distinct replay artifact classes before persistence. |
| Observability layer | Implemented core | The local harness emits schema-valid run records; indexes and domain-specific events remain project extensions. |
| Executable runtime | Implemented core | Standard-library-first structured execution, containment, redaction, timeout handling, and atomic evidence writes are regression-tested. |
| Curo package self-check | Ready | `scripts/validate_curo.py` checks structure plus runtime/schema IDs, enums, replay class separation, BOM policy, and registry coverage. |
| Project contract CLI | Implemented core | Local commands validate profiles, deterministically compile assignments from approved intent, and verify profile linkage. |
| Project domain validation | Project extension | Each project must still provide or adopt verified domain-specific validators. |
| Tools, MCP, and hooks | Extension area | Contracts and permissions must be defined per project before use. |
| Evaluation runner | Planned | Project-specific evaluation cases and runners are still required. |
| Review and promotion automation | Foundation | Event-triggered exception review, batched findings, correction limits, and HITL packet contracts exist; runtime automation remains project-specific. |
| Learning and distillation | Implemented proposal writer | The harness emits schema-valid candidates for five canonical types; validation, approval, and promotion remain governed steps. |

## Required project extensions

Every new project starts with `projects/<project-id>/project.yaml` and
`llm-assignments.json`, then adds only the extensions it needs:

- `contracts/` for domain-specific schemas
- `runtime/` or `server/harness/` for execution control
- `scripts/` for deterministic checks and preflight
- `tools/`, `mcp/`, and `hooks/` for authorized capabilities
- `evaluations/` for expected behavior and failure cases
- `provenance/` and `replay/` for run evidence
- `learning/` for evidence-backed proposals and promotion records

## Recommended build order

1. Validate the generic kickoff against [`../schemas/project-kickoff.schema.json`](../schemas/project-kickoff.schema.json).
2. Propose a project-specific profile and validate it against [`../schemas/project-profile.schema.json`](../schemas/project-profile.schema.json).
3. Review and obtain human approval for consequential intent and authority decisions.
4. Compile and validate [`../schemas/llm-assignments.schema.json`](../schemas/llm-assignments.schema.json) from the approved profile using an explicit reference time.
5. Freeze the project ownership table and canonical contracts.
6. Authorize and build the smallest bounded deterministic or fake-adapter slice.
7. Add project-specific runtime enforcement, tools, MCP servers, and hooks only with explicit permissions.
8. Add evaluations for success, failure, cancellation, provenance, and portability where applicable.
9. Add provenance and the appropriate execution-replay or artifact-verification writers.
10. Run package integrity and promotion checks.
11. Use Exception Review Mode only when a qualifying event occurs; return to the prior workflow state after resolution.
12. Promote reusable patterns back into Curo only after evidence from more than one project.

## Promotion rule

A project artifact should become part of Curo only when it is reusable across
projects, has an explicit owner, has deterministic checks where feasible, has
documented failure behavior, and has evidence that it works independently of a
single provider or framework.
