# Ownership Policy

## Rule

Every important fact, state transition, and check result must have a declared owner.

## Defaults

- Objective: human or authorized caller
- State: harness
- Validation: deterministic validator where feasible
- Evidence: harness
- Provenance: harness
- Observability records and events: harness or designated writer
- Pending decisions: human or authorized caller
- Project profile intent and approval: human or authorized caller
- Assignment compilation and linkage validation: harness
- Assignment approval: human or authorized caller; never the assigned model
- Desired identity: approved project profile and assignment policy
- Resolved identity: assignment resolver under harness policy
- Observed provider/model identity: the harness or adapter that observed the run

## Constraints

- A model may propose a record, but it may not authoritatively write the record if it did not directly observe or verify it.
- Unknown provenance remains unknown until established by the harness.
- A record is not valid just because a model produced it.
- The process runner owns exit and timeout facts; the validator owns schema results; the harness composes those facts into provenance and persists them only after validation.
- The caller owns the configured workspace/evidence boundary. The harness must resolve and enforce it before authoritative reads or writes.
- `project.yaml` is the human-readable project-intent authority.
  `llm-assignments.json` is a validated, deterministic derivative bound to that
  profile's canonical hash; it is not an independent source of project intent.
- Preferred or resolved identity must never populate observed identity. Run and
  provenance evidence establish observed identity, or preserve it as `UNKNOWN`.
