# Validation Policy

## Rule

Validation must be explicit, recorded, and owned by the component that actually performed it.

```text
PROCESS SUCCESS != VALIDATION SUCCESS
```

No authoritative Curo JSON artifact may be persisted unless its canonical contract is identified and validation succeeds. Validation failure returns machine-readable errors and blocks the write; malformed payloads are not silently coerced.

## Required checks

- structure check
- ownership check
- provenance check
- schema check
- replay check
- project-profile schema and unresolved-decision check
- assignment-to-profile hash and project-ID linkage check
- assignment authority, capability, fallback, path, and credential-field checks
- desired/resolved/observed identity separation check

## Acceptance rule

Promotion is allowed only after the required checks succeed and the evidence is captured in the harness-owned record.

For execution provenance, `PASS` requires all of the following: process exit zero, every declared required input verifiable, every declared required output present, and every emitted authoritative artifact schema-valid. Use `FAIL` for observed failed checks and `UNKNOWN` when a required fact could not be established.

Project assignment compilation requires schema-valid, approved project intent
and an explicit reference time. A material profile change changes its canonical
hash and invalidates prior assignment approval. Assignment files may express
desired and resolved identity, but observed identity is validated only against
run evidence produced by the component that observed execution.
