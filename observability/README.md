# Observability

This folder defines Curo's observability layer for reconstructing workflow
state without reconstructing it from chat history.

The design is adapted from the observed `E:\observe hitl` pattern, especially
its separation between a human-readable ledger and authoritative machine
evidence. Curo's version is workflow-neutral and does not copy project-specific
names, paths, or decisions.

## Files

- [`observability-contract.md`](observability-contract.md) - ownership, update, status, and HITL rules.
- [`run-record-template.md`](run-record-template.md) - human-readable record for one governed run.
- [`run-index-template.md`](run-index-template.md) - compact index of governed runs.
- [`run-record.schema.json`](run-record.schema.json) - machine contract for a run record.
- [`run-event.schema.json`](run-event.schema.json) - machine contract for an observed runtime event.

## Separation rule

Observability summarizes and links to execution. It does not create authority.
Authoritative facts remain in harness-owned provenance, validation, replay, and
outcome records. It is not a memory store, vector database, raw telemetry
archive, or place for hidden model scratchpads or private chain-of-thought.

## Use

At the end of a governed run:

1. Finalize machine evidence.
2. Determine the actual result.
3. Write the run record from that result.
4. Link concrete evidence paths or hashes.
5. Preserve prior history and active cutoffs.
6. Update the current task and run index.

If the authoritative result cannot be established, record `BLOCKED` or
`UNKNOWN`; never report completion by inference.
