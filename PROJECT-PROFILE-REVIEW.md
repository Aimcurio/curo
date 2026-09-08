# Curo Project-Profile Independent Protocol Review

Status: `PASS_WITH_EXCEPTIONS`

Review mode: `READ_ONLY_REVIEW`
Reviewer: Sub-agent F
Final review date: 2026-09-07

Reviewer silence is not approval. This verdict is based on the executable final
pass below.

## Final verdict

The project-definition and LLM-assignment layer is implemented and verified at
the repository-contract level. All eight protocol/integration findings raised
during independent review were corrected and retested. No P0 or P1 protocol
finding remains.

The result is `PASS_WITH_EXCEPTIONS` because actual KAYO and Math Node roots,
exact provider/model choices, current Spacetime authority, and human approval
references remain deliberately `UNKNOWN` or `DECISION_REQUIRED`. Those are
correct authority boundaries, not failed implementation claims.

- P0 remaining: 0
- P1 remaining: 0
- reviewer verdict: `PASS_WITH_EXCEPTIONS`
- unresolved decisions: `PROJECT-PROFILE-UNRESOLVED-DECISIONS.md`

## Required review questions

| # | Question | Final result | Evidence |
|---:|---|---|---|
| 1 | Is the generic kickoff still generic? | PASS | It retains intake fields and adds only the six lightweight `project_handoff` fields. |
| 2 | Does every project receive a specific operational profile? | PASS_WITH_EXPECTED_DECISIONS | KAYO, Spacetime, and Math Node each have a specific profile and assignment manifest; unresolved roots/approvals correctly prevent premature operation. |
| 3 | Are YAML intent and JSON runtime assignments prevented from drifting independently? | PASS | Every assignment carries the parsed-profile SHA-256; live linkage passes and an isolated hash mutation is rejected. |
| 4 | Are desired, resolved, and observed identities separate? | PASS | Assignment preference/resolution is separate from observed identity, which requires a bounded run-record path plus matched evidence and provenance. |
| 5 | Can configured model identity incorrectly become observed truth? | PASS | Bare mappings and invalid, untrusted, cross-project, cross-role, unbound, missing, or hash-mismatched evidence remain `UNKNOWN`. |
| 6 | Can a model approve its own assignment? | PASS_AT_CONTRACT_BOUNDARY | Non-human roles cannot approve; self-review is prohibited; approved profiles and manifests require a contained, SHA-bound, schema-valid harness approval record. Profile actors must match declared HUMAN operators; assignment actors must match declared HUMAN roles and the record must cover the exact assignment IDs and profile hash. |
| 7 | Can a fallback weaken privacy or authority? | PASS | Mutations confirm rejection of missing capabilities/validators, changed classification, prohibited capabilities, and expanded authority. |
| 8 | Can assignment files contain plaintext credentials? | PASS_WITH_PATTERN_LIMIT | Schemas admit credential metadata only; runtime scanning rejects tested secret fields/values without echoing them. Detection is conservatively documented as non-exhaustive. |
| 9 | Does changed profile content invalidate prior assignment approval? | PASS | Material edits change the canonical hash; linkage reports `SOURCE_PROFILE_HASH_MISMATCH`, and recompilation downgrades stale approval. |
| 10 | Are unauthorized paths rejected? | PASS | Parent, sibling, drive, real-target/junction, source-profile, compiler-input, and output boundaries are enforced. |
| 11 | Is materialization deterministic? | PASS | Identical governed inputs and explicit time produce byte-identical JSON; mapping-key order is canonicalized. |
| 12 | Is system time excluded from the deterministic core? | PASS | A clock-denial regression proves compilation does not call ambient `now`/`utcnow`. |
| 13 | Does KAYO preserve the Second Brain/KAYO/Control Room/Visual Node boundary? | PASS | KNOW / COORDINATE / OBSERVE / UNDERSTAND / ACT / ESTABLISH EVIDENCE / AUTHORIZE remain distinct and mutation-tested. |
| 14 | Are Spacetime and Math Node migrations evidence-preserving? | PASS | Source/copy hashes match; relocations validate; Math Node is `artifact_verification_manifest` with no execution field. |
| 15 | Were historical agent and architecture reports preserved rather than rewritten? | PASS | The archive hash matches the recorded original; the 89-file pre-existing `.agents` inventory hash is unchanged. Current indexes identify historical scope. |
| 16 | Do all new artifacts validate? | PASS | Fourteen selected profiles, assignments, templates, relocations, verification evidence, and superseding candidates validate. |
| 17 | Does the repository validator detect intentional drift mutations? | PASS | A clean temporary copy passed; a zeroed KAYO hash and a Control Room `KNOW` mutation each failed for the intended reason. |
| 18 | Are documentation claims supported by executable evidence? | PASS_WITH_EVIDENCE_BOUNDARY | Links and registry pass, required reports exist, and current claims match the final checks. Exact providers/models and approvals remain explicitly unverified. |

## Finding dispositions

### PPR-001 — Junction escape bypassed path authority

- finding_id: `PPR-001`
- severity: `P1`, resolved
- file and line: `harness/curo_harness/assignments.py:36-53`
- evidence: authorization now compares real targets before `commonpath`.
- counterexample or reproduction: the original Windows junction escape was
  recreated; validation now returned `UNAUTHORIZED_WRITE_ROOT`.
- required correction: completed; use real-target containment.
- acceptance test: `test_realpath_boundary_check_rejects_junction_escape` and
  the independent actual-junction reproduction pass closed.

### PPR-002 — Caller input could become VERIFIED observation

- finding_id: `PPR-002`
- severity: `P1`, resolved
- file and line: `harness/curo_harness/assignments.py:346-426`
- evidence: comparison now reads a repository-contained run path and requires
  schema validity, trusted source, expected project, matching role, evidence
  membership/hash, and matching schema-valid harness-owned provenance.
- counterexample or reproduction: bare configured mappings, self-report,
  cross-project, and unbound evidence remain `UNKNOWN`; a valid bounded chain
  verifies.
- required correction: completed; mappings are not evidence inputs.
- acceptance test: identity-separation and trusted-observed-run tests pass.

### PPR-003 — Approval actor did not establish human role authority

- finding_id: `PPR-003`
- severity: `P1`, resolved at the contract boundary
- file and line: `schemas/human-approval-record.schema.json:1-46`,
  `harness/curo_harness/approvals.py:18-72`, and
  `harness/curo_harness/assignments.py:173-196`
- evidence: approval requires a contained record whose bytes match the declared
  SHA-256 and whose schema, approval ID, project ID, current profile hash,
  harness recorder, actor, and exact assignment-ID set all match. Non-human
  roles cannot approve, and unresolved roles block approval.
- counterexample or reproduction: missing evidence, changed hashes, string
  actors, undeclared/non-human actors, stale profile hashes, and incomplete
  assignment-ID sets are rejected; current projects claim no approval.
- required correction: completed. Authentication of the human when the harness
  creates the record remains the authorized input-channel responsibility.
- acceptance test: hash-bound approval, structured-human, self-approval, and
  unresolved-role tests pass.

### PPR-004 — RESOLVED status contradicted unresolved identity

- finding_id: `PPR-004`
- severity: `P1`, resolved
- file and line: `harness/curo_harness/assignments.py:109-121`
- evidence: status and identity resolution are now bidirectionally consistent.
- counterexample or reproduction: `RESOLVED` plus `UNRESOLVED` now returns
  `RESOLVED_STATUS_IDENTITY_MISMATCH`.
- required correction: completed.
- acceptance test: `test_resolved_status_and_identity_must_agree` passes.

### PPR-005 — Documentation/registry integration was incomplete

- finding_id: `PPR-005`
- severity: `P1`, resolved
- file and line: `registry/registry.yaml`, `ARCHITECTURE.md`, `.agents/README.md`
- evidence: required artifacts are registered and present; current/history
  scope and root metadata are correct.
- counterexample or reproduction: the validator that previously listed missing
  registrations/history files now exits zero.
- required correction: completed.
- acceptance test: repository validator, archive test, registry gate, and link
  check pass.

### PPR-006 — Required regression matrix was incomplete

- finding_id: `PPR-006`
- severity: `P1`, resolved
- file and line: `tests/test_project_integrity.py`, `tests/test_projects.py`
- evidence: the suite expanded from 43 provisional tests to 67 and covers the
  named schema, assignment, determinism, KAYO, migration, preservation,
  compiler-boundary, and repository-mutation requirements.
- counterexample or reproduction: the final full discovery run reports 67 tests
  and `OK`.
- required correction: completed; unavailable environment checks remain labeled.
- acceptance test: full suite and repository gate pass together.

### PPR-007 — Compiler API accepted external inputs before persistence

- finding_id: `PPR-007`
- severity: `P1`, resolved
- file and line: `harness/curo_harness/assignments.py:276-303`
- evidence: compiler profile and assignment inputs are contained before read.
- counterexample or reproduction: external `%TEMP%` inputs now return
  `COMPILER_INPUT_PATH_UNAUTHORIZED` and create no output.
- required correction: completed.
- acceptance test: `test_compiler_rejects_external_inputs_before_persistence`
  and independent direct-API reproduction pass closed.

### PPR-008 — Approved profiles accepted an undeclared HUMAN actor

- finding_id: `PPR-008`
- severity: `P1`, resolved
- file and line: `harness/curo_harness/projects.py:198-212` and
  `harness/curo_harness/approvals.py:61-69`
- evidence: approved-profile validation now derives the declared HUMAN operator
  IDs and requires the hash-bound approval record's actor ID to be in that set.
- counterexample or reproduction: a contained, schema-valid, correctly hashed
  record naming `undeclared-human` previously validated a profile whose only
  HUMAN operator was `human-requester`. The independent final reproduction now
  returns `APPROVAL_ACTOR_UNAUTHORIZED`.
- required correction: completed; bind approved-profile actors to declared
  HUMAN operators.
- acceptance test: `test_approved_profile_requires_declared_human_operator`
  passes, and the independent negative reproduction fails closed.

## Independent executable evidence

```text
python -m unittest discover -s tests -v
Ran 67 tests in 17.167s
OK

python scripts/validate_curo.py
PASS: Curo foundation integrity checks
```

Additional final evidence:

- 14 selected governed project artifacts/templates: 14 PASS, 0 FAIL; all 14
  repository JSON schemas, including the human-approval schema, pass self-checks.
- Python 3.9 grammar: 27 files, 0 errors.
- UTF-8 BOM check: 27 Python files, 0 BOMs.
- Current Markdown relative links: 120 checked, 0 broken.
- `git diff --check`: no whitespace errors; line-ending advisories only.
- Clean-copy validator baseline: PASS.
- Profile-hash and KAYO authority mutations: both detected.

Historical hashes independently confirmed:

```text
pre-remediation architecture
09ddf0dea36fd05208855baa7c471a752eb297d7abbcdb76faad708712cf1bae

Spacetime source and copy
ec0d0eb61854d39d5ea3343ace6cd085182a11043e3b7eb7889a9f23335cb5ca

Math Node source and copy
effb92008a760ae228803a427a146bec1b8cee8df1c764ac9c48f16c85b0b8c9

original combined PDF candidate
4e0751651e1e5c887183789fd50a907fe516c7419547a9e1271fe96c4bed1b17

pre-existing .agents inventory, excluding new index
8b81449bd3c5dad13f9cbf26f11adb6ae602d8fb41567b5ca83f6c98a031fc0b
```

## Exceptions and unavailable facts

- KAYO root, transports, providers/models, private boundary, validators, and
  approvals remain `DECISION_REQUIRED`.
- Math Node root, lifecycle decision, providers/models, validators, and
  approvals remain `DECISION_REQUIRED`.
- Spacetime's recorded `E:\spacetime` root and current work authority require
  human confirmation.
- Actual provider/model identity remains `UNKNOWN` until a bounded observer
  produces the required run/evidence/provenance chain.
- Only Python 3.13.5 executed the suite; Python 3.9 grammar was checked.
- Secret detection is pattern-based and external URLs were not network-tested.

No reset, clean, commit, tag, push, or version bump was performed. Exceptions
are not reported as implemented, approved, available, or observed.
