# Ownership Policy

## Rule

Every important fact, state transition, and check result must have a declared owner.

## Defaults

- Objective: human or authorized caller
- State: harness
- Validation: deterministic validator where feasible
- Evidence: harness
- Provenance: harness
- Pending decisions: human or authorized caller

## Constraints

- A model may propose a record, but it may not authoritatively write the record if it did not directly observe or verify it.
- Unknown provenance remains unknown until established by the harness.
- A record is not valid just because a model produced it.

