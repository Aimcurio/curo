# Curo Protocol-Integrity Release Impact

Status: approval gate; no version bump and no release commit performed.

## Outcome

The executable harness now conforms to the core authority rule: a process exit is not validation success, and no authoritative JSON artifact produced by run, distill, escalation, or replay-manifest generation is written before its canonical schema validates.

## Breaking changes

- Canonical replay is split into `execution_replay_manifest` and `artifact_verification_manifest`; the old overloaded schema/template is removed.
- Canonical process input is `executable` plus ordered `args[]`; shell syntax is rejected and never persisted.
- Run success is `PASS`, not `SUCCESS`, and is conditioned on declared evidence plus artifact validation.
- Runtime learning candidates now use schema field names and the five-type enum.
- Governed paths outside the configured workspace/evidence boundary are rejected.

## Migration implications

- Convert stored executable replay records from `command` to `executable`, `args`, `cwd`, and `timeout_seconds`.
- Convert historical, non-executing digest manifests to `artifact_verification_manifest` with `artifacts[]`.
- Update callers that expect run `SUCCESS` to expect `PASS`, and read `process_status` separately.
- Use `--executable` and repeat `--arg` for CLI argv boundaries; the positional command is deprecated compatibility only.
- Supersede, rather than rewrite, historical learning candidates whose type is outside the canonical enum.

## Remaining limitations

- The redactor covers common deterministic patterns but cannot guarantee discovery of every secret form.
- Windows descendant termination depends on the native `taskkill` facility. Failure is explicit and no stronger guarantee is claimed.
- A host crash may leave a per-target lock file that needs operator review.
- The current executable evidence is from Python 3.13.5 on Windows; the declared Python 3.9+ range has not been exercised as a version matrix in this workspace.
- A pre-existing untracked skill document has a missing relative reference; it is outside the protocol-integrity scope and remains unchanged.

## Release recommendation

Recommended version: **MAJOR** because persisted replay and run contracts change incompatibly despite a bounded legacy CLI adapter. Suggested target is Curo `2.0.0`, with the harness package version aligned by the requester-approved release decision.

## CURO PROTOCOL-INTEGRITY STATUS

**PASS_WITH_EXCEPTIONS**

- P0 remaining: 0 known implementation blockers after final gates.
- P1 remaining: 1 approval/migration item for the pre-existing noncanonical PDF learning candidate; operational residuals are documented.
- Breaking changes: replay artifact split, structured argv authority, run status semantics, candidate payload alignment, and path-boundary enforcement.
- Migration implications: conversion is required for stored replay/run consumers; historical evidence should be superseded, not rewritten.
- Version recommendation: **MAJOR**.
