# Regression Evidence

Evidence date: 2026-09-07
Runtime observed: Python 3.13.5 on Windows
Release commit/version: not created; requester approval pending.

## Harness suite

Command:

```text
python -m unittest discover -s tests -v
```

Final observed result after project-profile integration and reviewer corrections:

```text
Ran 67 tests in 17.996s
OK
```

The suite covers the original protocol-integrity cases plus project profiles,
deterministic assignment compilation, identity/approval boundaries, KAYO,
historical migrations, repository mutation detection, and current/history
preservation. The project-specific matrix is detailed in
`PROJECT-PROFILE-REGRESSION-EVIDENCE.md`.

The final suite includes the optional-dependency fallback, atomic-write cleanup, and a Windows spawned-child timeout assertion.

## Repository integrity gate

Command:

```text
python scripts/validate_curo.py
```

Final observed result after documentation and registry updates:

```text
PASS: Curo foundation integrity checks
```

Additional deterministic checks observed:

```text
PASS: Python 3.9 grammar gate (final count recorded in project-profile evidence)
PASS: project profiles, assignments, relocations, verification, candidates, templates, and schemas validate
PASS: current-documentation Markdown links resolve
EXPECTED_EXCEPTION: preserved PDF candidate canonical validation = False
```

The upgraded gate checks runtime artifact schema IDs, CLI/runtime/schema enum agreement, scoped run/provenance statuses, replay class separation, Python UTF-8-without-BOM policy, schema references, registry entries, version synchronization, and the prior structural checks.

## Evidence boundary

- `IMPLEMENTED`: code and contracts exist in the working tree.
- `UNIT_TESTED` and `REGRESSION_TESTED`: named tests executed successfully on the observed Windows/Python runtime.
- `VERIFIED`: reserved here for behavior exercised by executable tests or the repository gate.
- Python 3.9 through 3.12 were not executed in this environment.
- Secret redaction is deliberately conservative and is not an exhaustive credential detector.
- Windows tree termination is claimed only when `timeout_termination_succeeded` is true.
- The former broken `skills/cli-creator.md` reference was removed after confirming no correct local target existed.
- Exact project provider/model selections and consequential approvals remain human decisions.
