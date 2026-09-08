# Curo Documentation Index

This index is the human navigation entry point for the Curo package. Start with the root [`README.md`](../README.md) and [`project.yaml`](../project.yaml) for package scope and metadata, then read the core identity before interpreting any subsystem as representative of the whole framework.

## Required identity path

1. [`../core-policies/core-identity.md`](../core-policies/core-identity.md) - canonical Curo identity and core-minimalism contract.
2. [`../core-policies/drift-check.md`](../core-policies/drift-check.md) - mandatory major-change drift gate.
3. [`architecture-layers.md`](architecture-layers.md) - stable core vs fast-evolving extension model.
4. [`../anti-patterns/framework-capture.md`](../anti-patterns/framework-capture.md) - feature, node, agent, skill, harness, and subsystem capture failure modes.

The governing rule is simple: **Curo stays small; capabilities attach to it.**

## Recommended reading paths

### New to Curo

1. [`beginner-guide.md`](beginner-guide.md) - what Curo is, when to use it, first-time commands, project setup, evidence, approval, and common mistakes.
2. [`../projects/README.md`](../projects/README.md) - current project examples and folder conventions.
3. [`../templates/project-kickoff.md`](../templates/project-kickoff.md) - begin a real project intake.

### Understand the standard

1. Complete the Required identity path above.
2. [`operating-standard.md`](operating-standard.md) - integrated operating standard.
3. [`addendum-a.md`](addendum-a.md) - accepted amendments and refinements.
4. [`addendum-b-protocol-integrity.md`](addendum-b-protocol-integrity.md) - executable validation, persistence, replay, path, redaction, and timeout guarantees for the harness extension.
5. [`../ARCHITECTURE.md`](../ARCHITECTURE.md) - current implementation and authority map, with the historical audit boundary.
6. [`../core-policies/precedence.md`](../core-policies/precedence.md) - order of authority when rules conflict.
7. [`gaps-and-roadmap.md`](gaps-and-roadmap.md) - maturity, known gaps, and extension order.

The operating standard includes applied reasoning patterns for successful execution, cancellation or early termination, dependency failure, unverifiable provenance, and component replacement. These are capabilities/patterns within the broader Curo framework; they do not redefine its core identity.

### Design model-readable packages

1. [`../skills/model-package-design/SKILL.md`](../skills/model-package-design/SKILL.md) - hybrid Markdown/YAML/JSON/JSONL/JSON-Schema packaging skill.
2. [`../agents/architecture-review.md`](../agents/architecture-review.md) - architecture-review role guard that prevents extension capture.

Use the model-package skill when complex work needs explicit semantic instructions, state, evidence, event history, and deterministic contracts without collapsing everything into one prompt or one data format.

### Conduct bounded deep research

1. [`../skills/goal-driven-deep-research/SKILL.md`](../skills/goal-driven-deep-research/SKILL.md) - goal-driven research lifecycle and completion boundary.
2. [`../skills/goal-driven-deep-research/module.yaml`](../skills/goal-driven-deep-research/module.yaml) - module inputs, outputs, policies, and schemas.
3. Use its evidence, contradiction, unknown, and stopping-rule artifacts to decide whether a goal is decision-ready; a report alone does not establish readiness.

### Implement selected capabilities

1. [`../core-policies/ownership.md`](../core-policies/ownership.md) - ownership rules for applicable system properties.
2. [`../harness/harness-contract.md`](../harness/harness-contract.md) - harness extension boundary when harnessed execution is selected.
3. [`../adapters/adapter-contract.md`](../adapters/adapter-contract.md) - provider/model adapter boundary.
4. [`../schemas/provenance-record.schema.json`](../schemas/provenance-record.schema.json) - evidence record shape.
5. [`../schemas/execution-replay-manifest.schema.json`](../schemas/execution-replay-manifest.schema.json) - structured execution replay shape.
6. [`../schemas/artifact-verification-manifest.schema.json`](../schemas/artifact-verification-manifest.schema.json) - non-executing artifact verification shape.

### Start a new project

1. [`../templates/project-kickoff.md`](../templates/project-kickoff.md) - fill-in brief for the requester.
2. [`../templates/project-kickoff.yaml`](../templates/project-kickoff.yaml) - machine-readable equivalent for tooling.
3. Use the completed brief to select the Curo extensions needed for that project.
4. Run the drift check before adding any new core concept.
5. [`../templates/project-profile.yaml`](../templates/project-profile.yaml) - project-specific intent proposal when the project-profile extension is selected.
6. [`../schemas/project-profile.schema.json`](../schemas/project-profile.schema.json) - governed profile contract.
7. Review and approve the profile; unresolved consequential decisions block approval.
8. [`../templates/llm-assignments.json`](../templates/llm-assignments.json) - assignment input/output shape.
9. [`../schemas/llm-assignments.schema.json`](../schemas/llm-assignments.schema.json) - hash-bound desired/resolved assignment contract.
10. [`../projects/README.md`](../projects/README.md) - project folder convention and current examples.
11. [`../schemas/project-relocation-record.schema.json`](../schemas/project-relocation-record.schema.json) - evidence-preserving path-relocation contract.

The handoff is kickoff → profile proposal → review → approval → deterministic
assignment compilation and validation → bounded implementation authorization.
Observed model identity belongs only to run and provenance evidence.

Validate and verify with `python curo.py project validate`, `project compile`,
and `project verify-assignments`; use each command's `--help` for arguments.

### Current and historical architecture

1. [`../ARCHITECTURE.md`](../ARCHITECTURE.md) describes current contracts and authority.
2. [`audits/2026-09-07-pre-remediation-architecture.md`](audits/2026-09-07-pre-remediation-architecture.md) preserves the pre-remediation audit byte-for-byte.
3. [`../.agents/README.md`](../.agents/README.md) indexes time-scoped agent execution evidence.
4. [`../CHANGE-MAP.md`](../CHANGE-MAP.md) and [`../REGRESSION-EVIDENCE.md`](../REGRESSION-EVIDENCE.md) record the remediation mapping and executable evidence.

### Observe and govern runs

1. [`../observability/observability-contract.md`](../observability/observability-contract.md) - observability authority and update rules when that extension is selected.
2. [`../observability/run-record-template.md`](../observability/run-record-template.md) - human-readable governed run record.
3. [`../observability/run-index-template.md`](../observability/run-index-template.md) - compact run index.
4. [`../observability/run-record.schema.json`](../observability/run-record.schema.json) - machine run-record contract.
5. [`../observability/run-event.schema.json`](../observability/run-event.schema.json) - machine observed-event contract.

Before promoting a Curo revision, run [`../scripts/validate_curo.py`](../scripts/validate_curo.py) to check package integrity.

### Operate and review

1. [`../core-policies/validation.md`](../core-policies/validation.md) - validation order and promotion gates.
2. [`../anti-patterns/anti-patterns.md`](../anti-patterns/anti-patterns.md) - existing failure modes.
3. [`../anti-patterns/framework-capture.md`](../anti-patterns/framework-capture.md) - identity-drift failure modes.
4. [`../registry/registry.yaml`](../registry/registry.yaml) - canonical artifact inventory.
5. [`../provenance/sample-provenance-record.yaml`](../provenance/sample-provenance-record.yaml) - example harness-owned evidence.
6. [`../replay/execution-replay-manifest-template.yaml`](../replay/execution-replay-manifest-template.yaml) - structured rerun template.
7. [`../replay/artifact-verification-manifest-template.yaml`](../replay/artifact-verification-manifest-template.yaml) - non-executing verification template.

### Resolve exceptions

1. [`../review/exception-review-protocol.md`](../review/exception-review-protocol.md) - event-triggered adversarial-but-fair review.
2. [`../review/findings-template.yaml`](../review/findings-template.yaml) - batched validator and reviewer findings.
3. [`../review/hitl-packet-template.yaml`](../review/hitl-packet-template.yaml) - consolidated requester decisions.
4. [`../schemas/review-findings.schema.json`](../schemas/review-findings.schema.json) - findings contract.
5. [`../schemas/hitl-packet.schema.json`](../schemas/hitl-packet.schema.json) - HITL escalation contract.

### Distill learning

1. [`../learning/learning-distillation-protocol.md`](../learning/learning-distillation-protocol.md) - post-execution proposal and promotion rules.
2. [`../learning/learning-candidate-template.yaml`](../learning/learning-candidate-template.yaml) - candidate proposal template.
3. [`../learning/promotion-record-template.yaml`](../learning/promotion-record-template.yaml) - promotion and regression-guard record.

## Folder map

| Folder | Purpose | Core status |
|---|---|---|
| [`core-policies/`](../core-policies/README.md) | Core identity, ownership, precedence, validation, and drift policy | Core policy |
| [`skills/`](../skills/model-package-design/SKILL.md) | Reusable knowledge/capability modules | Extension |
| [`agents/`](../agents/architecture-review.md) | Reusable agent/role profiles | Extension |
| [`schemas/`](../schemas/README.md) | Machine-readable record contracts | Extension/support |
| [`anti-patterns/`](../anti-patterns/README.md) | Known failure modes and detection guidance | Policy/support |
| [`adapters/`](../adapters/README.md) | Provider and model integration boundary | Extension |
| [`harness/`](../harness/README.md) | Enforcement and execution boundary | Extension |
| [`observability/`](../observability/README.md) | Run summaries and event contracts | Extension |
| [`registry/`](../registry/README.md) | Artifact inventory and canonical paths | Support |
| [`provenance/`](../provenance/README.md) | Evidence and trace examples | Extension/support |
| [`replay/`](../replay/README.md) | Reproducibility and rerun manifests | Extension/support |
| [`docs/`](README.md) | Narrative standard and navigation | Documentation |
| [`templates/`](../templates/README.md) | Reusable project initialization templates | Extension |
| [`review/`](../review/README.md) | Exception review and HITL packets | Extension |
| [`learning/`](../learning/README.md) | Governed learning/promotion artifacts | Extension |
| [`projects/`](../projects/README.md) | Project-specific profiles, assignments, and preserved evidence | Extension |
| [`scripts/`](../scripts/README.md) | Package integrity checks | Support |
| [`.agents/`](../.agents/README.md) | Historical agent reports and handoffs | Time-scoped evidence only |

## Change routing

Put a proposed change in the narrowest extension or policy folder that owns it. Before expanding core, apply [`../core-policies/drift-check.md`](../core-policies/drift-check.md). Prefer a bounded skill, agent, node, module, adapter, workflow, validator, or other extension whenever Curo would remain Curo without that capability.
