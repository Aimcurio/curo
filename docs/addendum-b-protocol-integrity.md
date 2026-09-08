# Addendum B: Executable Protocol Integrity

Status: implemented and regression-tested; release approval pending
Date: 2026-09-07

## Authority rule

No authoritative Curo JSON artifact may be persisted unless the runtime identifies its canonical schema, validation succeeds, and the runtime state uses the schema's scoped vocabulary. A process exit code is process evidence only:

```text
PROCESS SUCCESS != VALIDATION SUCCESS
```

Run-level `PASS` requires process exit zero, verified declared inputs, present declared outputs, and schema-valid provenance, run, and replay artifacts. An observed failed check is `FAIL`; an unestablished required fact is `UNKNOWN`. Diagnostics are stored separately and do not replace canonical states.

## Execution and replay

Canonical execution consists of `executable`, ordered `args[]`, `cwd`, and `timeout_seconds`, executed with `shell=False`. Shell command strings are not canonical. The compatibility input accepts only simple commands, rejects shell operators, and is converted before execution.

An `execution_replay_manifest` can re-execute that structured contract. An `artifact_verification_manifest` performs hash and optional schema checks without executing a process. Their schema constants and required fields are disjoint.

## Boundaries and persistence

All governed paths are resolved and checked with path semantics against the configured workspace or evidence root. Parent traversal, external absolute paths, sibling-prefix collisions, and cross-drive paths are rejected.

Authoritative JSON writes use a temporary file in the target directory, flush and filesystem sync, then atomic replace under a bounded per-target local lock. This is single-machine coordination, not a distributed lock.

## Telemetry and timeouts

stdout and stderr snippets are scrubbed before persistence for common authorization headers, credential assignments, private-key blocks, and common token prefixes. `redaction_applied` records whether text changed. The scrubber is conservative and deterministic, not exhaustive secret detection.

On Windows, a run starts in a new process group. Timeout handling invokes the Windows-native `taskkill /T /F` tree operation and preserves partial output where possible. The record is always `TIMED_OUT`; if tree termination cannot be confirmed, `timeout_termination_succeeded` is false and the diagnostic states that residual risk. Curo does not claim a stronger guarantee.

## Scoped vocabularies

- Run result: `PASS`, `FAIL`, `UNKNOWN`, `TIMED_OUT`.
- Process state: `COMPLETE`, `FAIL`, `TIMED_OUT`, `NOT_STARTED`.
- Validation/provenance result: `PASS`, `FAIL`, `UNKNOWN`.
- Learning candidate type: `rule`, `skill`, `anti_pattern`, `validator`, `standard_amendment`.
- Learning lifecycle: `PROPOSED`, `VALIDATION_PENDING`, `VALIDATED`, `APPROVED`, `PROMOTED`, `REJECTED`, `BLOCKED`.
- Review and HITL retain their own domain vocabularies.

These vocabularies are intentionally scoped. `COMPLETE` says a process finished; it does not mean validation passed. `APPROVED` says an authorized approval exists; it does not mean promotion occurred.

## Project definition and assignment integrity

The generic kickoff is intake only. A project-specific
`projects/<project-id>/project.yaml` expresses human-readable intent and must be
reviewed and approved before assignment compilation. The generated
`llm-assignments.json` is a deterministic runtime contract bound to the
canonical profile SHA-256, not a competing source of truth.

The compiler rejects unresolved approval claims, plaintext credential fields,
unauthorized paths, invalid role authority, and fallbacks that weaken required
capability or data classification. Its deterministic inputs include the
profile, explicit assignment input, policy version, and explicit reference
time; ambient clock time does not affect canonical bytes.

Desired, resolved, and observed identities remain separate. Assignment
configuration can establish desired or resolved identity only. The observing
run/provenance writer establishes actual provider/model identity, or records
`UNKNOWN` when it cannot. A comparison consumes observed identity only from a
schema-valid trusted run record whose required `observed_identity` object names
its state, provider, model, evidence source, and SHA-256. The contained evidence
must match that hash and be corroborated by matching harness-owned provenance;
arbitrary mappings are not accepted as observed evidence. Approved profiles
and assignments reference a contained, hash-bound human approval record.
Assignment approval binds the exact assignment IDs and a declared HUMAN actor,
never a model self-approval. Authenticating that actor remains the authorized
harness input channel's responsibility.
