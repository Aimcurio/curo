# Curo Protocol-Integrity Change Map

Status: REGRESSION_TESTED; RELEASE_APPROVAL_PENDING
Evidence date: 2026-09-07

| Finding ID | Files changed | Contract or schema affected | Test name / gate | Test result and observed output | Remaining limitation |
|---|---|---|---|---|---|
| CURO-PI-001 | `harness/curo_harness/validator.py` | All repository-local JSON schemas | `test_nullable_union_type`; `test_relative_ref`; `test_enum_violation`; `test_missing_required_field`; `test_additional_properties_violation`; `test_zero_dependency_fallback_handles_nullable_and_relative_ref` | VERIFIED — all named tests `ok`; full suite `Ran 29 tests ... OK`. | Fallback intentionally implements the Curo schema subset, not every JSON Schema 2020-12 keyword. |
| CURO-PI-002 | `validator.py`, `run.py`, `distill.py`, `escalate.py` | Provenance, run record, execution replay, learning candidate, HITL schemas | `test_schema_invalid_run_artifact_is_blocked`; `test_invalid_hitl_is_not_persisted`; candidate/HITL validation tests | VERIFIED — forced-invalid payloads returned errors and authoritative files did not exist. | Multi-file run persistence is validation-atomic but not transactionally all-or-none across a host failure between replaces. |
| CURO-PI-003 | `run.py`, `distill.py`, `escalate.py`, `observability/run-record.schema.json`, learning/HITL/provenance schemas and samples | Canonical artifact contracts | `test_structured_run_and_artifacts_validate`; `test_all_five_candidate_types_are_accepted_and_valid`; `test_hitl_packet_validates_before_persistence` | VERIFIED — every emitted artifact validated against its named schema. | Pre-existing PDF candidate needs a superseding migration decision. |
| CURO-PI-004 | `run.py`, `provenance-record.schema.json`, validation policy, Addendum B | Provenance and run result semantics | `test_missing_input_cannot_pass`; `test_missing_expected_output_cannot_pass`; `test_every_emitted_run_status_is_schema_accepted` | VERIFIED — missing input emitted `UNKNOWN`/`NOT_STARTED`; missing output emitted `FAIL`; neither produced `PASS`. | No undeclared output can be treated as required; callers must declare required evidence. |
| CURO-PI-005 | `process.py`, `security.py`, `run.py`, `replay.py`, `cli.py` | Structured execution contract | `test_malicious_legacy_shell_syntax_is_not_executed`; `test_execution_replay_uses_structured_argv` | VERIFIED — shell syntax was rejected, marker was absent, and structured replay returned `REPLAY_VERIFIED`. | Restricted command-string compatibility remains pending removal policy. |
| CURO-PI-006 | execution/artifact-verification schemas and templates, `replay.py`, registry and docs | Replay artifact classes | `test_execution_replay_uses_structured_argv`; `test_artifact_verification_manifest_requires_no_command`; repository replay-class check | VERIFIED — execution replay ran argv; artifact verification returned `VERIFIED` without a command; integrity gate passed. | Historical manifests require conversion or explicit preservation as legacy evidence. |
| CURO-PI-007 | `core.py`, `run.py`, `replay.py` | Workspace/evidence boundary | `test_parent_escape`; `test_absolute_external_path`; `test_sibling_prefix_collision`; `test_valid_nested_path`; `test_windows_drive_boundary`; `test_replay_path_escape_is_rejected` | VERIFIED — all invalid boundary cases were rejected and valid nesting passed. | Symlink/reparse behavior follows final resolved paths; authorization is only as correct as the configured root. |
| CURO-PI-008 | `security.py`, `run.py`, `replay.py`, Addendum B | Observability telemetry | `test_secret_bearing_stdout_is_redacted` | VERIFIED — persisted snippet omitted the test token and recorded `redaction_applied: true`. | Deterministic patterns are conservative, not exhaustive secret detection. |
| CURO-PI-009 | `process.py`, `run.py` | Timeout/process status | `test_timeout_records_timed_out`; `test_windows_timeout_terminates_child_tree` | VERIFIED — status was `TIMED_OUT`; Windows child marker remained absent after its scheduled write time. | Native `taskkill` availability is required for confirmed descendant termination; failure is explicit. |
| CURO-PI-010 | `vocabularies.py`, `cli.py`, `distill.py`, run/learning/provenance schemas, observability and learning docs | Scoped statuses and five candidate types | candidate-type/status tests; `check_enum_alignment`; machine-example vocabulary check | VERIFIED — all five types emitted schema-valid candidates; all run states validated; integrity gate passed. | Review, HITL, promotion, and learning keep intentionally separate domain vocabularies. |
| CURO-PI-011 | `core.py` | Authoritative flat-file persistence | `test_atomic_write_cleans_temporary_state` | VERIFIED — second atomic write replaced the first and left no temporary/lock file. | A host crash may leave a stale lock; automatic lock breaking is intentionally not implemented. |
| CURO-PI-012 | six normalized Python files; source-hygiene tests and validator | UTF-8 without BOM policy | `test_python_sources_are_utf8_without_bom`; `check_python_bom_policy` | VERIFIED — test `ok`; integrity gate passed. | Tested repository files only; future drift is guarded by both gates. |
| CURO-PI-013 | `scripts/validate_curo.py` | Foundation-integrity gate | `python scripts/validate_curo.py` | VERIFIED — observed `PASS: Curo foundation integrity checks`. | Fast structural gate does not replace runtime integration tests. |
| CURO-PI-014 | README, operating standard, Addendum B, policies, harness/replay/observability/learning docs, roadmap, templates | Authoritative narrative contracts | full suite followed by integrity gate | REGRESSION_TESTED — documentation updated only after executable suite first passed; final gates pass. | Version metadata remains unchanged pending requester approval. |
| CURO-PI-015 | `FRAMEWORK-LESSON-PROPOSALS.md`, `UNRESOLVED-DECISIONS.md` | Learning/promotion authority | document and registry integrity gate | IMPLEMENTED — ten lessons classified; none automatically promoted. | Human promotion decisions remain required. |
| CURO-PI-016 | `schemas/learning-candidate.schema.json`, `UNRESOLVED-DECISIONS.md` | Learning candidate type contract | candidate enum gate and five-type tests | PASS_WITH_EXCEPTION — canonical runtime/schema contract passes; historical file was preserved. | One P1 migration/approval item remains for the pre-existing PDF candidate. |

## Aggregate observed gates

```text
python -m unittest discover -s tests -v
Ran 29 tests in 7.936s
OK

python scripts/validate_curo.py
PASS: Curo foundation integrity checks
```

The final verification run after all documentation and registry edits is recorded in `REGRESSION-EVIDENCE.md`. No version bump, release tag, commit, or push was performed.
