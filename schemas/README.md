# Schemas

This folder defines machine-readable contracts for evidence and replay artifacts.

Schemas are centralized here when they define a cross-folder machine contract.
Some colocated schemas remain beside their observability contracts because the
runtime record and event templates are maintained as one operational unit.

## Files

- [`provenance-record.schema.json`](provenance-record.schema.json) - schema for harness-owned execution evidence.
- [`execution-replay-manifest.schema.json`](execution-replay-manifest.schema.json) - structured executable and argv replay contract.
- [`artifact-verification-manifest.schema.json`](artifact-verification-manifest.schema.json) - non-executing historical artifact and lineage verification contract.
- [`project-kickoff.schema.json`](project-kickoff.schema.json) - schema for completed project kickoff briefs.
- [`review-findings.schema.json`](review-findings.schema.json) - batched review findings and correction classification.
- [`hitl-packet.schema.json`](hitl-packet.schema.json) - consolidated human decision escalation.
- [`learning-candidate.schema.json`](learning-candidate.schema.json) - evidence-backed learning proposals.
- [`human-approval-record.schema.json`](human-approval-record.schema.json) - hash-bound, harness-recorded human approval evidence for project profiles and assignment sets.
- [`project-profile.schema.json`](project-profile.schema.json) - project-specific human intent, constraints, authority, and validation requirements.
- [`llm-assignments.schema.json`](llm-assignments.schema.json) - deterministic desired/resolved role assignment contract bound to a project-profile hash.
- [`project-relocation-record.schema.json`](project-relocation-record.schema.json) - provenance for preserved project artifact copies and relocations.

Runtime writers identify one canonical schema before persistence. Relative repository-local `$ref` links resolve from the containing schema, with a standard-library fallback when the optional `jsonschema` package is unavailable.
- [`promotion-record.schema.json`](promotion-record.schema.json) - validated promotion and regression closure.
- Colocated observability schemas: [`../observability/run-record.schema.json`](../observability/run-record.schema.json) and [`../observability/run-event.schema.json`](../observability/run-event.schema.json).

## Change rule

Schema changes are interface changes. Keep them backward-compatible where possible, update examples and consumers together, and validate every instance before promotion. Unknown values must remain explicit rather than being silently inferred.
