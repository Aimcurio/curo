# Harness

This folder defines the enforcement layer that controls tools, state transitions, validation, evidence persistence, and replay preparation.

## Files

- [`harness-contract.md`](harness-contract.md) - enforcement and execution contract.

## Ownership

The harness is the sole authoritative writer for externally verifiable execution facts in the package. A model process must have no write path to authoritative records, regardless of whether enforcement is implemented through filesystem permissions, an API boundary, a database role, or another deployment-specific mechanism.

The included local runtime uses structured argv execution, schema-before-write gates, resolved path containment, redacted telemetry, atomic JSON replacement, and bounded same-target locks. See [`harness-contract.md`](harness-contract.md) for exact semantics and limitations.
