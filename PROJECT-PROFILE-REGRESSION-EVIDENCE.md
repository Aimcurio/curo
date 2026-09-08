# Curo Project-Profile Regression Evidence

Evidence date: 2026-09-07
Runtime observed: Python 3.13.5 on Windows
Release state: no version bump, commit, tag, or push

## Executable results

```text
python -m unittest discover -s tests -v
Ran 67 tests in 17.996s
OK

python scripts/validate_curo.py
PASS: Curo foundation integrity checks
```

Additional lead integration gates:

```text
JSON Schema self-check: 14/14 PASS
Governed project artifacts/templates: 14/14 PASS
Deterministic materialization: 3192 bytes, two outputs byte-identical
Python 3.9 grammar: 27/27 PASS
Python UTF-8 BOM check: 27 files, 0 BOMs
Current Markdown relative links: 154 checked, 0 broken
git diff --check: no whitespace errors; line-ending advisories only
git status: inspected; pre-existing and integrated dirty work preserved
```

The suite covers the prior protocol-integrity harness plus project schema
validation, optional-dependency fallback keywords, profile approval gates,
canonical hashing, byte-identical compilation, explicit reference time,
implicit-clock exclusion, validation-before-persistence, source linkage,
profile drift, mapping-key order, duplicate identifiers, secret rejection,
fallback constraints, real-target path containment, compiler input containment,
hash-bound human approval, assignment/identity state consistency, trusted
observed-run/evidence/provenance binding, all three project profiles, KAYO boundaries, historical
migrations, PDF supersession, architecture preservation, `.agents` preservation,
and an intentional repository hash-drift mutation.

## Governed artifacts

- Four project-layer schemas and two templates validate; all 14 repository JSON schemas pass schema self-checks.
- KAYO, Spacetime, and Math Node profiles validate.
- All three assignment manifests validate and match their live source-profile hashes.
- Both relocation records validate and their source/copy hashes match.
- Math Node's replacement validates as `artifact_verification_manifest` and has no executable field.
- Both superseding PDF candidates validate and remain `PROPOSED`.
- The generic kickoff validates with exactly the lightweight project handoff.

## Historical hashes

```text
pre-remediation architecture
09ddf0dea36fd05208855baa7c471a752eb297d7abbcdb76faad708712cf1bae

Spacetime historical record
ec0d0eb61854d39d5ea3343ace6cd085182a11043e3b7eb7889a9f23335cb5ca

Math Node historical record
effb92008a760ae228803a427a146bec1b8cee8df1c764ac9c48f16c85b0b8c9

original combined PDF candidate
4e0751651e1e5c887183789fd50a907fe516c7419547a9e1271fe96c4bed1b17

pre-existing .agents inventory excluding the new index
8b81449bd3c5dad13f9cbf26f11adb6ae602d8fb41567b5ca83f6c98a031fc0b
```

## Status meanings

- `IMPLEMENTED`: the code or contract exists in the working tree.
- `UNIT_TESTED`: a focused executable test passed.
- `REGRESSION_TESTED`: the complete suite passed after integration.
- `VERIFIED`: executable evidence directly established the claim.
- `UNKNOWN`: the evidence needed to establish a claim is unavailable.
- `BLOCKED`: an in-scope required outcome cannot proceed.

## Evidence boundary

Exact KAYO, Spacetime, and Math Node providers/models are not verified and are
not claimed. KAYO and Math Node roots remain `UNKNOWN`; Spacetime's recorded
root still needs current human confirmation. Profiles and assignment manifests
remain `DECISION_REQUIRED`. Python 3.9 grammar is checked syntactically during
the final gate, but only Python 3.13.5 executed the suite. Secret-pattern
detection is conservative, and trust in a `VERIFIED` model identity ultimately
depends on the designated harness or adapter that owns the linked evidence.
Approval records are structurally and cryptographically bound inside the
repository, while authentication of the human at record creation remains the
authorized harness input channel's responsibility.
