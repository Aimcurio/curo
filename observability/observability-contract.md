# Curo Observability Contract

## Purpose

Observability provides a concise, reconstructable view of workflow execution
for human operators and review systems. It connects a run to its evidence,
status transitions, blockers, decisions, and next authorized action.

## Authority boundary

Observability records are derived summaries. They do not create authority and
do not replace contracts, validation results, provenance records, replay
manifests, review findings, adjudications, or governed outcomes.

```text
OBSERVABILITY_RECORD != AUTHORITY
```

If an observability record conflicts with an authoritative artifact, the
authoritative artifact wins and the summary must be corrected.

## Required run information

Every governed run should record:

- run identifier
- timestamp with timezone
- project and workflow identifier
- governed role
- preferred, required, and actual component identity when applicable
- fallback state and reason
- result status
- machine-evidence locator
- evidence manifest or hash when available
- files or artifacts changed
- blockers
- authorized status transition
- authorizing evidence or decision
- exactly one immediate next authorized action

## Designated writer

Only the run's designated writer may update its human-readable observability
record. A role does not gain project mutation authority merely because it can
write an observability file. A run record is documentation, not permission to
change the governed project.

## Update order

Use this order:

1. Finalize machine evidence.
2. Determine the run result from that evidence.
3. Write or update the observability record.
4. Include concrete evidence references.
5. Preserve previous failures, blockers, reversals, and cutoffs.
6. Update the run index.
7. Create a checkpoint snapshot only for a meaningful milestone.

Do not update a status from an unverified intermediate claim.

## Status vocabulary

Use explicit statuses:

```text
CREATED
RUNNING
COMPLETE
PASS
FAIL
BLOCKED
PARTIAL
CANCELLED
TIMED_OUT
IMPLEMENTED
CLEAR
MATERIAL_FINDINGS
DEFERRED
NOT_STARTED
NOT_AUTHORIZED
FROZEN
UNKNOWN
```

Do not use informal replacements such as `basically done`, `probably passed`,
or `looks good`.

## Evidence rule

`evidence_locator` must identify concrete machine evidence, a manifest, a run
ID, a commit, or a hash. `logs checked` is not an evidence locator.

If no locator exists, record `NONE_WITH_REASON` and explain why. Never estimate
or invent a hash.

## HITL and cutoffs

Human-in-the-loop approval is required when the workflow reaches a declared
high-impact boundary, including:

- irreversible or safety-critical mutation
- policy override
- disputed material finding
- promotion to canonical authority
- public deployment
- unresolved deadlock after bounded recovery

Exception Review Mode is event-triggered rather than a natural or permanent
run state. Record the activation event, trigger, affected finding IDs, severity,
and prior workflow state. Record the resolution outcome and return to the prior
state unless the human decision authorizes a different transition.

Do not escalate routine formatting, schema normalization, registry completion,
or other mechanically verifiable findings. Batch all remaining findings into a
single review result or HITL packet. A disagreement becomes a HITL issue only
when it changes authority, correctness, risk, scope, or cannot converge after
the configured correction limit.

Observability records the approval and its evidence; it does not grant the
approval. Active cutoffs must be preserved even when they delay progress.

## Checkpoints and history

Create a checkpoint only for a meaningful event:

- architecture or contract version change
- decision-set expansion
- freeze or authorization
- milestone completion
- major blocker or HITL escalation
- baseline replacement

Routine runs update living records and the run index. They do not create a full
project record each time.
