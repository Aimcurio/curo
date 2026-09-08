# Curo Protocol-Integrity Remediation Findings

Status: REMEDIATED_WITH_RECORDED_EXCEPTIONS; RELEASE_APPROVAL_PENDING
Audit date: 2026-09-07
Authority: executable behavior must conform to canonical Curo contracts; evidence outranks process success and model self-report.

| Finding ID | Priority | Class | Observed conflict | Intended authority | Planned resolution |
|---|---|---|---|---|---|
| CURO-PI-001 | P0 | IMPLEMENTATION / SCHEMA | Fallback validation cannot handle union types and optional `jsonschema` does not receive a repository-local reference base. | Canonical JSON schemas. | Repair recursive fallback validation and repository-relative reference resolution; return explicit errors. |
| CURO-PI-002 | P0 | IMPLEMENTATION / SECURITY | Run, replay, learning, and HITL artifacts are persisted without successful canonical-schema validation. | Harness validation gate. | Validate before atomic persistence; return errors and write nothing on failure. |
| CURO-PI-003 | P0 | IMPLEMENTATION / SCHEMA | Runtime run, replay, learning, and HITL payloads do not match their schemas. | Artifact-specific canonical schemas and ownership policy. | Reconcile runtime payloads and schemas without permissive coercion; regression guard each emitted artifact. |
| CURO-PI-004 | P0 | FRAMEWORK / IMPLEMENTATION | Exit code zero alone produces provenance `PASS`. | Validation and provenance policies. | Require process success, verifiable required inputs, present required outputs, and valid authoritative artifacts; otherwise `FAIL` or `UNKNOWN` with diagnostic reasons. |
| CURO-PI-005 | P0 | SECURITY / IMPLEMENTATION | Commands are executed through `shell=True` and persisted as shell strings. | Structured execution contract. | Use executable plus argv with `shell=False`; isolate deprecated string parsing behind a rejecting compatibility layer. |
| CURO-PI-006 | P0 | SCHEMA / FRAMEWORK | Executable replay and non-executing artifact verification share one overloaded manifest class. | Replay purpose and authority boundary. | Define distinct execution replay and artifact verification schemas, templates, registry entries, and runtime dispatch. |
| CURO-PI-007 | P0 | SECURITY / IMPLEMENTATION | Read/write paths are not checked against resolved workspace/evidence boundaries. | Configured local authority boundary. | Add reusable resolved containment checks and reject traversal, external absolute paths, prefix collisions, and drive escapes. |
| CURO-PI-008 | P0 | SECURITY / IMPLEMENTATION | stdout/stderr can persist secrets verbatim. | Safe observability defaults. | Deterministically redact common credential patterns before persistence and record whether redaction occurred. |
| CURO-PI-009 | P1 | IMPLEMENTATION / SECURITY | Timeout handling may leave descendants alive, especially on Windows. | Harness-owned deterministic execution state. | Use process groups and a Windows-native tree termination fallback; report termination failure explicitly and preserve partial output where possible. |
| CURO-PI-010 | P1 | SCHEMA / IMPLEMENTATION | Learning candidate types and lifecycle/status values drift across CLI, runtime, templates, and schemas. | Scoped artifact vocabularies. | Centralize canonical candidate types, define scoped statuses, and validate runtime emissions. |
| CURO-PI-011 | P1 | IMPLEMENTATION | JSON writes are direct and non-atomic; concurrent namespace writers are uncoordinated. | Harness persistence contract. | Add same-directory temp write, flush/fsync, replace, and bounded per-target lock files. |
| CURO-PI-012 | P1 | TEST / IMPLEMENTATION | Python BOM policy and annotation-import hygiene are not enforced. | Repository source policy. | Normalize Python sources to UTF-8 without BOM and add a fast integrity check. |
| CURO-PI-013 | P1 | TEST | Repository validator checks structure but not runtime/schema IDs, enum alignment, replay class separation, BOMs, or new registry contracts. | Fast foundation-integrity gate. | Extend deterministic static checks without turning the script into an integration suite. |
| CURO-PI-014 | P1 | DOCUMENTATION / FRAMEWORK | Documentation describes guarantees the current harness does not enforce. | Tested implementation first, then authoritative documentation. | Update affected documentation only after executable regression tests pass. |
| CURO-PI-015 | P2 | FRAMEWORK / DOCUMENTATION | Ten audit lessons require classification and human-controlled promotion decisions. | Learning/distillation protocol. | Produce proposals and an unresolved-decision register; do not auto-promote. |
| CURO-PI-016 | P1 | SCHEMA / DOCUMENTATION | Pre-existing `LEARN-20260907-PDF-RESTORATION.yaml` uses candidate type `skill_and_anti_pattern_distillation`, outside the requested five-type canonical vocabulary. | Canonical learning-candidate contract; historical evidence immutability. | Do not rewrite the existing user-owned candidate in place; record migration/approval decision separately. |

## Evidence baseline

- `python -m unittest discover -s tests -v`: 4 tests passed, but the current tests assert legacy shell-string behavior.
- `python scripts/validate_curo.py`: reports `PASS: Curo foundation integrity checks`, demonstrating that the current gate does not detect the protocol drift above.
- Git working tree was already non-clean before remediation. Existing changes are preserved and are not attributed to this release.

## Closure rule

A finding is closed only when its contract decision is recorded, its implementation is changed, its named regression test passes, and observed output is captured in `CHANGE-MAP.md`. Code inspection alone is not `VERIFIED` when executable validation is practical.

## Closure summary

- CURO-PI-001 through CURO-PI-015: remediated and covered by executable or deterministic repository-gate evidence recorded in `CHANGE-MAP.md`.
- CURO-PI-016: canonical contract remediated; one preserved pre-existing candidate requires a requester-approved superseding migration and remains a recorded P1 exception.
- P0 remaining: 0 known.
- Release state: stopped before version bump and commit as required.
