# Curo Current Architecture

Status: current working-tree architecture; release approval pending
Updated: 2026-09-07
Package version: 1.8.2

Curo core remains the small, modular, model-agnostic framework defined by
[`core-policies/core-identity.md`](core-policies/core-identity.md). The project
profiles, harness, governance, observability, replay, review, and learning
layers documented below are selected extensions; their presence does not make
any one of them the definition of Curo.

## Historical boundary

The prior root architecture report is preserved byte-for-byte as
[`docs/audits/2026-09-07-pre-remediation-architecture.md`](docs/audits/2026-09-07-pre-remediation-architecture.md).
Its SHA-256 is recorded in
[`docs/audits/2026-09-07-pre-remediation-architecture.sha256`](docs/audits/2026-09-07-pre-remediation-architecture.sha256):

```text
09ddf0dea36fd05208855baa7c471a752eb297d7abbcdb76faad708712cf1bae
```

That audit accurately described the pre-remediation snapshot, including
`shell=True` execution, a four-test suite, the then-current status claims,
schema-reference limitations, and the overloaded `replay_manifest` contract.
Those observations are historical evidence, not descriptions of the current
working tree. Individual reports under [`evidence/historical-agent-runs/`](evidence/historical-agent-runs/README.md) are
preserved on the same time-scoped basis.

Current implementation authority resides in the current schemas, contracts,
runtime code, registry, [`CHANGE-MAP.md`](CHANGE-MAP.md), and
[`REGRESSION-EVIDENCE.md`](REGRESSION-EVIDENCE.md). When a historical statement
conflicts with those current artifacts, preserve the historical statement and
use current executable evidence to determine present behavior.

## Authority model

```text
human or authorized caller
    owns objective, consequential project intent, and approval
            |
generic kickoff intake
            |
projects/<id>/project.yaml
    owns human-readable approved project intent
            |
deterministic compiler + validators
            |
projects/<id>/llm-assignments.json
    owns desired/resolved runtime assignments bound to profile SHA-256
            |
harness-controlled execution
            |
run + provenance evidence
    owns observed process, validation, provider, and model facts
```

Desired identity is not resolved identity, and neither is observed identity.
The observing harness or adapter establishes actual provider/model identity;
when it cannot, the value remains `UNKNOWN`. Identity comparison accepts only
a schema-valid trusted run record with the required `observed_identity`
evidence object, never an arbitrary mapping.

## Repository layers

| Layer | Current authority |
|---|---|
| Standard and policy | [`docs/operating-standard.md`](docs/operating-standard.md), [`core-policies/`](core-policies/README.md) |
| Project intake | [`templates/project-kickoff.md`](templates/project-kickoff.md), [`templates/project-kickoff.yaml`](templates/project-kickoff.yaml) |
| Project intent | [`schemas/project-profile.schema.json`](schemas/project-profile.schema.json), `projects/<id>/project.yaml` |
| Role assignments | [`schemas/llm-assignments.schema.json`](schemas/llm-assignments.schema.json), `projects/<id>/llm-assignments.json` |
| Execution and enforcement | [`harness/harness-contract.md`](harness/harness-contract.md), `harness/curo_harness/` |
| Validation contracts | [`schemas/`](schemas/README.md) and project-specific validators |
| Observed execution | [`observability/observability-contract.md`](observability/observability-contract.md), run and provenance records |
| Re-execution | [`schemas/execution-replay-manifest.schema.json`](schemas/execution-replay-manifest.schema.json) |
| Non-executing verification | [`schemas/artifact-verification-manifest.schema.json`](schemas/artifact-verification-manifest.schema.json) |
| Historical relocation | [`schemas/project-relocation-record.schema.json`](schemas/project-relocation-record.schema.json) |
| Artifact inventory | [`registry/registry.yaml`](registry/registry.yaml) |

## Project lifecycle

1. Complete the generic kickoff and its lightweight project handoff.
2. Propose a project-specific profile under `projects/<project-id>/project.yaml`.
3. Validate the profile and resolve consequential human decisions.
4. Obtain human approval; an assigned model cannot approve itself.
5. Compile `llm-assignments.json` deterministically with an explicit reference time.
6. Validate schema, authority, paths, capability-preserving fallbacks, privacy limits, and the source-profile hash.
7. Authorize only the bounded implementation described by the approved profile.
8. Record observed execution identity and results in run/provenance evidence.

The `projects/` directory contains project-specific governance records and
preserved evidence, not the external projects' source repositories. KAYO,
Spacetime, and Math Node provide current examples; unresolved exact roots,
providers, or models remain explicit decisions rather than invented facts.

## Runtime integrity

Canonical process execution uses `executable` plus ordered `args[]` with
`shell=False`. Governed paths are resolved against configured boundaries.
Authoritative JSON is schema-validated before atomic persistence. Common secret
patterns are redacted before telemetry storage. Timeout handling records an
explicit result and, on Windows, attempts process-tree termination without
claiming success it cannot confirm.

Execution replay and artifact verification are deliberately separate:

- `execution_replay_manifest` contains structured process execution data.
- `artifact_verification_manifest` checks hashes and optional schemas without
  introducing an executable command.

See [`docs/addendum-b-protocol-integrity.md`](docs/addendum-b-protocol-integrity.md)
for exact current guarantees and limitations.

## Local project commands

```text
python curo.py project validate <project.yaml>
python curo.py project compile <project.yaml> --assignments <input.json> --reference-time <ISO-8601> --output <llm-assignments.json>
python curo.py project verify-assignments <llm-assignments.json>
```

Compilation requires approved project intent. Validation errors are explicit
and nonzero; assignment compilation cannot establish observed model identity.

## Verification and release boundary

Use [`scripts/validate_curo.py`](scripts/validate_curo.py) for fast repository
integrity checks and the test suite for runtime and regression behavior. Read
[`PROJECT-PROFILE-REGRESSION-EVIDENCE.md`](PROJECT-PROFILE-REGRESSION-EVIDENCE.md)
for the current project-profile verification scope and limitations. The earlier
[`REGRESSION-EVIDENCE.md`](REGRESSION-EVIDENCE.md) remains the consolidated
protocol-integrity record.

This integration adopts the existing upstream package version `1.8.2`. It does
not create another version bump, tag, or GitHub Release. Future release impact
and the version recommendation are recorded in
[`RELEASE-IMPACT.md`](RELEASE-IMPACT.md).

## Curo drift review

```yaml
curo_drift_review:
  identity_restated: "Curo is a small, modular, model-agnostic framework for composable AI capabilities."
  change_type: "project-profile, harness, governance, validation, evidence, replay, review, and learning extensions"
  removal_preserves_identity: true
  center_of_gravity_shift: false
  model_agnostic: true
  modular_boundary_preserved: true
  lineage:
    - core-policies/core-identity.md
    - core-policies/drift-check.md
    - docs/operating-standard.md
  semantic_reframing_detected: false
  scope_inflation_detected: false
  classification: EXTENSION
  required_action: "register and validate the extensions without redefining core"
  reviewer_notes: "The included extensions are usable together but remain replaceable and optional at the Curo identity boundary."
```
