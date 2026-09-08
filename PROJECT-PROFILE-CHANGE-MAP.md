# Curo Project-Profile and LLM-Assignment Change Map

Status: `REGRESSION_TESTED; HUMAN_PROJECT_APPROVAL_PENDING`
Evidence date: 2026-09-07

The generic kickoff remains intake. Project YAML owns reviewed intent,
assignment JSON owns deterministic desired/resolved configuration bound to the
profile hash, and trusted run/provenance evidence owns observed execution.

| Finding | Decision | Agent owner | Files changed | Contract | Test or gate | Observed result | Historical hash | Remaining limitation | Review status |
|---|---|---|---|---|---|---|---|---|---|
| PPA-001 | Add a project-specific profile layer | B / lead | `schemas/project-profile.schema.json`, `templates/project-profile.yaml` | `curo_project_profile` | profile schema and fallback tests | valid profiles accepted; undeclared and missing fields rejected | n/a | Profiles require human approval | VERIFIED |
| PPA-002 | Add deterministic multi-role assignments | B / C / lead | `schemas/llm-assignments.schema.json`, `templates/llm-assignments.json`, `assignments.py` | `curo_llm_assignments` | assignment, fallback, identity, approval tests | desired, resolved, observed, authority, fallback, and secret guards pass | n/a | Exact project providers/models unresolved | VERIFIED |
| PPA-003 | Bind JSON assignments to YAML intent | C / lead | `projects.py`, `assignments.py`, `cli.py` | canonical parsed-profile SHA-256 | determinism/linkage/drift tests | identical inputs are byte-identical; changed profile is rejected | n/a | YAML parsing uses optional PyYAML; JSON remains dependency-free | VERIFIED |
| PPA-004 | Add bounded project CLI | C | `cli.py`, `curo.py` | `project validate`, `compile`, `verify-assignments` | CLI nonzero and linkage tests | invalid input returns machine-readable errors and nonzero | n/a | Compilation requires approved intent | VERIFIED |
| PPA-005 | Create KAYO-specific governance | D | `projects/kayo/**` | profile and six-role assignment | KAYO boundary and linkage tests | KNOW/COORDINATE/OBSERVE/UNDERSTAND/ACT/ESTABLISH EVIDENCE/AUTHORIZE remain distinct | n/a | Root, transports, providers, models, and approval unresolved | VERIFIED |
| PPA-006 | Preserve and relocate Spacetime evidence | D | `projects/spacetime/**` | relocation and project contracts | byte/hash and schema checks | source and copy are byte-identical | `ec0d0eb61854d39d5ea3343ace6cd085182a11043e3b7eb7889a9f23335cb5ca` | Current external-root authority still needs confirmation | VERIFIED |
| PPA-007 | Reclassify Math Node without rewriting history | D | `projects/math-node/**` | `artifact_verification_manifest` | schema/no-executable/hash tests | historical bytes preserved; replacement has no executable | `effb92008a760ae228803a427a146bec1b8cee8df1c764ac9c48f16c85b0b8c9` | Current root and validator commands unresolved | VERIFIED |
| PPA-008 | Split the invalid combined PDF proposal | D | two superseding learning candidates | learning candidate schema | candidate validation tests | `skill` and `anti_pattern` both `PROPOSED`; original unchanged | `4e0751651e1e5c887183789fd50a907fe516c7419547a9e1271fe96c4bed1b17` | HITL validation/promotion pending | VERIFIED |
| PPA-009 | Preserve historical architecture and agent evidence | E | `ARCHITECTURE.md`, `docs/audits/**`, `.agents/README.md` | current/history boundary | archive and `.agents` inventory tests | audit copy matches original; 89 earlier agent files unchanged | `09ddf0dea36fd05208855baa7c471a752eb297d7abbcdb76faad708712cf1bae` | Historical links intentionally not treated as current claims | VERIFIED |
| PPA-010 | Keep kickoff generic and add a handoff | E | kickoff MD/YAML/schema | `project_handoff` | schema, repository, and docs checks | exactly six lightweight handoff fields; no embedded assignment contract | n/a | Intake still requires project-specific completion | VERIFIED |
| PPA-011 | Register and document current authority | E | root docs, policies, contracts, registry | registry/read-order/current docs | repository validator and link check | current contracts registered; stale replay targets absent | n/a | External URLs not network-tested | VERIFIED |
| PPR-001 | Resolve junctions before path authority checks | F / lead | `core.py`, `assignments.py` | filesystem containment | junction escape regression | escaped real target rejected | n/a | Nonexistent descendants rely on the nearest resolvable path | VERIFIED |
| PPR-002 | Bind observed identity to trusted run evidence | F / lead | run/provenance schemas and samples, `run.py`, `assignments.py` | observed identity | forged/cross-project/untrusted/hash/provenance tests | arbitrary mappings remain UNKNOWN; VERIFIED requires contained hashed evidence plus matching harness-owned provenance | n/a | Authenticity still depends on the harness/adapter trust boundary | VERIFIED |
| PPR-003 | Require hash-bound human approval evidence | F / lead | human-approval/profile/assignment schemas, `approvals.py`, project and assignment validators | approval authority | missing/hash/actor/self-approval tests | APPROVED requires a contained SHA-bound harness record; assignment actor matches a HUMAN role and exact assignment IDs | n/a | The authorized harness input channel authenticates the human | VERIFIED |
| PPR-004 | Align assignment and identity resolution | F / lead | `assignments.py` | assignment state machine | contradiction/unresolved-list tests | contradictory RESOLVED state rejected; unknown desired roles remain declared unresolved | n/a | Approval-before-runtime-resolution remains distinct from RESOLVED | VERIFIED |
| PPR-007 | Contain compiler inputs before reading/writing | F / lead | `assignments.py` | compiler boundary | external-input persistence test | external inputs rejected and output absent | n/a | External source repositories are described by profiles, not read as compiler inputs | VERIFIED |

No version bump, commit, tag, push, automatic assignment approval, or external
project mutation was performed.
