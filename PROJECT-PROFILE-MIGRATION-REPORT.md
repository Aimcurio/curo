# Curo Project-Profile Migration Report

Status: `IMPLEMENTED_AND_SCHEMA_VALIDATED`

Date: 2026-09-07

Owner: Sub-agent D, project profile and migration implementation

## Authority preserved

The migration implements this non-competing authority chain:

```text
generic kickoff = intake
projects/<id>/project.yaml = proposed human-readable project intent
projects/<id>/llm-assignments.json = validated desired/resolved assignment contract
run and provenance records = observed execution identity and facts
```

All three project profiles and assignment manifests remain
`DECISION_REQUIRED`. No exact provider, model, approval, or observed execution
identity was inferred. Assignment manifests intentionally contain no observed
provider/model fields.

## Projects created

| Project | Profile | Assignment manifest | Profile hash | Result |
|---|---|---|---|---|
| KAYO | `projects/kayo/project.yaml` | `projects/kayo/llm-assignments.json` | `sha256:a878c417b8ecbe11d9cad55cacbc9e21766e9a9f08dab82ecdff93dacf4303f5` | schema and linkage PASS |
| Spacetime | `projects/spacetime/project.yaml` | `projects/spacetime/llm-assignments.json` | `sha256:bcd6621be84887e93297c2a8af05a347e67e9668d4173cadc7840cf74a8fd9d9` | schema and linkage PASS |
| Math Node | `projects/math-node/project.yaml` | `projects/math-node/llm-assignments.json` | `sha256:4be98b50708afbed76792c9e8b1dc993b84ca4b69f67dc8dbaf780d06d15c148` | schema and linkage PASS |

Hashes were calculated with the runtime's canonical rule: parse the profile,
serialize it as sorted compact JSON with UTF-8 and no ASCII escaping, calculate
lowercase SHA-256, then add the `sha256:` prefix. Any material profile edit must
invalidate and regenerate the linked assignment hash.

## KAYO boundary and assignments

The KAYO profile preserves exactly:

```text
Second Brain = KNOW
KAYO = COORDINATE
Control Room = OBSERVE
Visual Data Node = UNDERSTAND
Executor = ACT
Validator = ESTABLISH EVIDENCE
Human = AUTHORIZE
```

Its assignment document keeps Strategist, Builder, Critic/Reviewer,
Deterministic Validator, Local/Private Model Lane, and Human Approver distinct.
Every role declares authority, capabilities, prohibited capabilities, context,
roots, writes, tools, privacy limits, validators, fallback policy, completion
evidence, review requirements, and escalation conditions. Exact identities and
the KAYO external root remain unresolved.

## Historical artifacts preserved

| Project | Original | Preserved copy | SHA-256 | Method |
|---|---|---|---|---|
| Spacetime | `manifests/spacetime-sim-learning-record.json` | `projects/spacetime/evidence/spacetime-sim-learning-record.json` | `ec0d0eb61854d39d5ea3343ace6cd085182a11043e3b7eb7889a9f23335cb5ca` | `COPY_PRESERVE_SOURCE`, byte-identical |
| Math Node | `manifests/math-node-v0.1-replay.json` | `projects/math-node/evidence/math-node-v0.1-replay.json` | `effb92008a760ae228803a427a146bec1b8cee8df1c764ac9c48f16c85b0b8c9` | `COPY_PRESERVE_SOURCE`, byte-identical |

The originals remain in `manifests/`. Each copy has a schema-valid relocation
record with the old path, new path, matching hashes, and preservation method.

The Math Node replacement is
`projects/math-node/evidence/math-node-v0.1-artifact-verification.json`. It uses
`artifact_verification_manifest`, links both the original and preserved copy,
and contains no executable command. It supersedes only the old replay
classification, never the historical bytes or claims.

## PDF learning candidate split

The invalid historical combined candidate remains unchanged at
`learning/candidates/LEARN-20260907-PDF-RESTORATION.yaml`, SHA-256
`4e0751651e1e5c887183789fd50a907fe516c7419547a9e1271fe96c4bed1b17`.

Two schema-valid, independently reviewable replacements were added:

- `learning/candidates/LEARN-20260907-PDF-RESTORATION-SKILL.yaml`, type
  `skill`, status `PROPOSED`;
- `learning/candidates/LEARN-20260907-PDF-RESTORATION-ANTI-PATTERN.yaml`, type
  `anti_pattern`, status `PROPOSED`.

Both reference the preserved original candidate, its SHA-256, the original run,
events, findings, and evidence paths. Neither inherits the historical file's
unsupported `APPROVED` status.

## Requirement evidence

| Finding | Decision | Files changed | Contract | Executable evidence | Remaining limitation | Review status |
|---|---|---|---|---|---|---|
| PPA-004 | Create a KAYO-specific profile with strict component/role boundaries | `projects/kayo/**` | project profile and assignment schemas | profile validation and assignment linkage PASS | roots, transports, providers, models, and approval unresolved | pending independent reviewer |
| PPA-006 | Copy and hash historical Spacetime evidence; create present contracts | `projects/spacetime/**` | profile, assignment, relocation schemas | source/copy SHA-256 match; all new governed artifacts validate | current external-root availability and work authority unresolved | pending independent reviewer |
| PPA-007 | Preserve legacy Math bytes and supersede only classification | `projects/math-node/**` | profile, assignment, relocation, artifact-verification schemas | source/copy SHA-256 match; replacement and relocation validate | current root and current validator commands unresolved | pending independent reviewer |
| PPA-008 | Split invalid combined proposal without altering it | two new `learning/candidates/*` files | learning-candidate schema | both replacements validate; original SHA-256 unchanged | HITL review and promotion remain required | pending independent reviewer |

## Validation performed

- Parsed and validated each `project.yaml` against the canonical project-profile
  schema and runtime semantic checks: PASS, 3 of 3.
- Validated each `llm-assignments.json` and verified live profile linkage through
  `verify_assignment_linkage`: PASS, 3 of 3.
- Validated both relocation records against the project-relocation schema: PASS,
  2 of 2.
- Validated the Math Node replacement through the artifact-verification schema,
  including its provenance reference: PASS.
- Validated both new PDF candidates through the canonical learning-candidate
  schema: PASS, 2 of 2.
- Recomputed original and copied historical SHA-256 values: exact match for both
  source/copy pairs.

This report does not claim the full repository integration suite or independent
review; those gates belong to the lead coordinator and review agent.
