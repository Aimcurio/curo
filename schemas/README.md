# Schemas

This folder defines machine-readable contracts for evidence and replay artifacts.

Schemas are centralized here when they define a cross-folder machine contract.
Some colocated schemas remain beside their observability contracts because the
runtime record and event templates are maintained as one operational unit.

## Files

- [`provenance-record.schema.json`](provenance-record.schema.json) - schema for harness-owned execution evidence.
- [`replay-manifest.schema.json`](replay-manifest.schema.json) - schema for replay inputs, versions, and validation results.
- [`project-kickoff.schema.json`](project-kickoff.schema.json) - schema for completed project kickoff briefs.
- [`review-findings.schema.json`](review-findings.schema.json) - batched review findings and correction classification.
- [`hitl-packet.schema.json`](hitl-packet.schema.json) - consolidated human decision escalation.
- [`learning-candidate.schema.json`](learning-candidate.schema.json) - evidence-backed learning proposals.
- [`promotion-record.schema.json`](promotion-record.schema.json) - validated promotion and regression closure.
- Colocated observability schemas: [`../observability/run-record.schema.json`](../observability/run-record.schema.json) and [`../observability/run-event.schema.json`](../observability/run-event.schema.json).

## Change rule

Schema changes are interface changes. Keep them backward-compatible where possible, update examples and consumers together, and validate every instance before promotion. Unknown values must remain explicit rather than being silently inferred.
