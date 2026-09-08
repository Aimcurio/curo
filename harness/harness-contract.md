# Harness Contract

## Purpose

The harness is the enforcement layer.

## Responsibilities

- execute checks
- own authoritative records
- write provenance and evidence
- validate outputs
- control retries and timeouts
- manage replay packaging
- reject reads and writes outside resolved workspace/evidence boundaries
- redact common credential patterns before telemetry persistence
- validate every authoritative JSON payload against its identified canonical schema before writing it
- validate project profiles and reject unresolved approval claims
- deterministically compile assignment manifests from approved intent, explicit assignment input, policy version, and reference time
- verify assignment project ID and canonical source-profile hash before use
- enforce role authority, capability-preserving fallbacks, privacy limits, allowed paths, and plaintext-credential rejection

## Limits

- The harness should not depend on model self-report for authoritative facts.
- The harness should not silently accept unknown ownership.
- Process success is not validation success. `PASS` requires a zero exit code, verified declared inputs, present declared outputs, and successful artifact-schema validation.
- Canonical execution is `executable` plus `args[]` with `shell=False`. The legacy command string is deprecated, rejects shell syntax, and is never persisted as the canonical contract.
- Authoritative JSON persistence uses a same-directory temporary file, flush, atomic replace, and a bounded per-target local lock.
- On Windows, timeout handling uses a new process group and `taskkill /T /F`. If tree termination cannot be confirmed, the run remains `TIMED_OUT` and records the limitation explicitly.
- The project compiler may materialize desired and resolved identity only. It
  must not infer observed identity from preference, configuration, or
  resolution. Only a schema-valid trusted run record with required
  `observed_identity` evidence may establish actual provider/model identity;
  arbitrary caller mappings are not evidence. Missing evidence remains
  `UNKNOWN`.
- Approved profiles and assignment sets reference a repository-contained,
  SHA-256-bound, schema-valid human approval record written by the harness.
  Assignment approval also identifies a structured human actor matching a
  declared HUMAN role. A model role cannot approve its own assignment.
- A `VERIFIED` observed identity requires a repository-contained run record,
  the exact hashed observation evidence named by that record, and matching
  harness-owned provenance for the run. Bare caller mappings are not evidence.
- Identical normalized profile, assignment input, assignment policy version,
  and explicit reference time produce byte-equivalent canonical JSON. An
  implicit system clock does not participate in materialization.
