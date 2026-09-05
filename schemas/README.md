# Schemas

This folder defines machine-readable contracts for evidence and replay artifacts.

## Files

- [`provenance-record.schema.json`](provenance-record.schema.json) - schema for harness-owned execution evidence.
- [`replay-manifest.schema.json`](replay-manifest.schema.json) - schema for replay inputs, versions, and validation results.
- [`project-kickoff.schema.json`](project-kickoff.schema.json) - schema for completed project kickoff briefs.
- [`review-findings.schema.json`](review-findings.schema.json) - batched review findings and correction classification.
- [`hitl-packet.schema.json`](hitl-packet.schema.json) - consolidated human decision escalation.

## Change rule

Schema changes are interface changes. Keep them backward-compatible where possible, update examples and consumers together, and validate every instance before promotion. Unknown values must remain explicit rather than being silently inferred.
