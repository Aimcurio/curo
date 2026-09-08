# Framework Lesson Proposals

Status: PROPOSAL_ONLY
Promotion authority: human approval plus the Curo learning/promotion protocol.

| ID | Audit lesson | Classification | Proposed destination | Rationale | Promotion state |
|---|---|---|---|---|---|
| LESSON-PI-01 | Process success is not validation success. | RULE | `core-policies/validation.md` | Always-on authority boundary applicable to every governed execution. | PROPOSED |
| LESSON-PI-02 | Authoritative persistence requires successful schema validation. | RULE | `core-policies/validation.md` | Always-on precondition for authoritative JSON writes. | PROPOSED |
| LESSON-PI-03 | Runtime implementation must not drift from canonical schemas. | VALIDATOR | `scripts/validate_curo.py` | A deterministic repository gate can detect ID and vocabulary drift. | PROPOSED |
| LESSON-PI-04 | Replayable execution must use structured executable plus argv contracts. | STANDARD_AMENDMENT | `docs/addendum-b-protocol-integrity.md` | Changes the canonical representation and execution boundary. | PROPOSED |
| LESSON-PI-05 | Verification manifests and executable replay manifests are separate artifact classes. | STANDARD_AMENDMENT | Replay schemas and standard | Establishes separate purposes and prevents accidental execution. | PROPOSED |
| LESSON-PI-06 | Workspace containment uses resolved path boundaries, not string prefixes. | VALIDATOR | Harness path-boundary utility and integrity tests | The behavior is deterministic and reusable. | PROPOSED |
| LESSON-PI-07 | Secret-bearing telemetry is redacted before persistence. | RULE | Harness and observability policies | A safe default applies across projects, with documented non-exhaustiveness. | PROPOSED |
| LESSON-PI-08 | Repository state and deployed/runtime state are distinct lifecycle dimensions. | DOCUMENTATION_ONLY | Lifecycle guidance | Important conceptual clarification, but no universal runtime transition can establish deployment state. | PROPOSED |
| LESSON-PI-09 | Framework learning completes only with traceable promotion and a regression guard. | RULE | Learning/distillation protocol | Reinforces the existing evidence-to-promotion authority chain. | PROPOSED |
| LESSON-PI-10 | Fixed environment assumptions require explicit contracts or validated derivation. | PROJECT_SPECIFIC | Project kickoff and adapter contracts | The rule is reusable, but actual environment derivation remains project-owned. | PROPOSED |

Implementation during remediation supplies evidence for these proposals but does not constitute framework promotion approval. Registry inclusion, canonical versioning, and release remain at the requester approval gate.
