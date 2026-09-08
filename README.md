# Curo

Curo is a **small, modular, model-agnostic framework** around which reusable AI capabilities can be built, composed, replaced, and evolved.

**Curo provides the socket, not the appliance.** Skills, agents, nodes, validators, workflows, governance, observability, execution systems, research systems, adapters, and future capabilities may attach to Curo, but none of them defines Curo by itself.

This project is organized for both human reading and machine processing. The canonical intent is:

- keep Curo core small and stable
- default new functionality to extension/module status
- keep the framework model- and provider-neutral
- preserve provenance and version metadata
- separate policy, schema, harness, registry, provenance, replay, adapter, skill, agent, and anti-pattern concerns
- make ownership and validation explicit
- prevent any skill, agent, node, feature, harness, or subsystem from silently redefining Curo

## Canonical content

- `project.yaml` - machine-readable project metadata and lineage
- `core-policies/core-identity.md` - canonical Curo identity and core-minimalism contract
- `core-policies/drift-check.md` - mandatory architecture drift classification gate
- `anti-patterns/framework-capture.md` - failure modes that allow extensions to capture framework identity
- `docs/architecture-layers.md` - stable-core vs fast-evolving-extension model
- `docs/beginner-guide.md` - plain-language first-use guide and practical workflows
- `docs/INDEX.md` - human navigation index and reading paths
- `docs/operating-standard.md` - integrated standard, accepted refinements, and five applied reasoning patterns
- `docs/addendum-a.md` - patch notes for the accepted amendments
- `docs/gaps-and-roadmap.md` - current maturity, known gaps, and extension order
- `skills/model-package-design/SKILL.md` - portable hybrid Markdown/YAML/JSON/JSONL/JSON-Schema packaging skill
- `skills/goal-driven-deep-research/SKILL.md` - bounded research extension with evidence, contradiction, unknown, and stopping rules
- `agents/architecture-review.md` - agent-facing identity and drift guard for architecture work
- `ARCHITECTURE.md` - current architecture and authority map; links to the preserved pre-remediation audit
- `scripts/validate_curo.py` - dependency-free self-check for package integrity
- `templates/project-kickoff.md` - human kickoff brief for applying Curo to a new project
- `templates/project-kickoff.yaml` - machine-readable kickoff equivalent
- `templates/project-profile.yaml` - project-specific human-governed intent template
- `templates/llm-assignments.json` - deterministic assignment-manifest template

## Folder map

- `core-policies/` - core identity, governing rules, drift checks, and precedence
- `skills/` - reusable optional Curo capabilities and knowledge packs
- `agents/` - optional agent/role profiles that consume Curo policies and skills
- `schemas/` - JSON and YAML structure contracts
- `anti-patterns/` - known failure modes and avoidance rules
- `adapters/` - model/provider interface expectations
- `harness/` - optional enforcement and execution boundaries
- `observability/` - run records, status, evidence links, checkpoints, and HITL boundaries
- `review/` - event-triggered Exception Review Protocol, findings, correction, and HITL artifacts
- `learning/` - post-execution learning candidates and governed promotion records
- `registry/` - canonical inventory of artifacts and ownership
- `provenance/` - sample record formats and trace notes
- `replay/` - distinct structured-execution replay and non-executing artifact-verification manifests
- `docs/` - narrative reference material
- `templates/` - reusable project initialization templates
- `projects/` - project-specific profiles, assignment manifests, and preserved project evidence; not source repositories
- `.agents/` - historical execution reports and handoffs, indexed separately from current architecture
- `scripts/` - dependency-free integrity and promotion checks

## How to use

1. If Curo is new to you, start with [`docs/beginner-guide.md`](docs/beginner-guide.md).
2. Read `project.yaml` for scope, ownership, and lifecycle.
3. Read `core-policies/core-identity.md` before treating any subsystem as representative of the whole framework.
4. Read `core-policies/drift-check.md` before major architecture changes.
5. Read `docs/architecture-layers.md` and `ARCHITECTURE.md` for the extension and current-contract maps.
6. Read `docs/operating-standard.md` for the integrated operating model.
7. For a real project, complete generic intake, propose and approve
   `projects/<project-id>/project.yaml`, then compile and validate
   `projects/<project-id>/llm-assignments.json`.
8. Use the relevant extension folder when making changes:
   - policy changes go in `core-policies/`
   - record shape changes go in `schemas/`
   - failure-mode updates go in `anti-patterns/`
   - provider integration changes go in `adapters/`
   - validation or enforcement changes go in `harness/`
   - exception review and HITL changes go in `review/`
   - learning and promotion changes go in `learning/`
   - inventory or naming changes go in `registry/`
   - evidence and trace updates go in `provenance/`
   - rerun packaging changes go in `replay/`
   - project-specific governance and historical evidence go in `projects/`
9. Ask **“How does this plug into Curo?”** before asking **“How do we add this to Curo?”**

The local CLI supports:

```text
python curo.py project validate projects/<project-id>/project.yaml
python curo.py project compile projects/<project-id>/project.yaml --assignments <input.json> --reference-time <ISO-8601> --output projects/<project-id>/llm-assignments.json
python curo.py project verify-assignments projects/<project-id>/llm-assignments.json
```

Compilation requires approved project intent. Preferred and resolved identity
remain assignment intent; actual provider/model identity is authoritative only
when captured by the observing run and provenance records.

The project-profile implementation is documented in:

- [`PROJECT-PROFILE-FINDINGS.md`](PROJECT-PROFILE-FINDINGS.md)
- [`PROJECT-PROFILE-CHANGE-MAP.md`](PROJECT-PROFILE-CHANGE-MAP.md)
- [`PROJECT-PROFILE-MIGRATION-REPORT.md`](PROJECT-PROFILE-MIGRATION-REPORT.md)
- [`PROJECT-PROFILE-UNRESOLVED-DECISIONS.md`](PROJECT-PROFILE-UNRESOLVED-DECISIONS.md)
- [`PROJECT-PROFILE-REVIEW.md`](PROJECT-PROFILE-REVIEW.md)
- [`PROJECT-PROFILE-REGRESSION-EVIDENCE.md`](PROJECT-PROFILE-REGRESSION-EVIDENCE.md)

## Non-negotiable rules

- Curo core stays small; extensions remain extensions unless an explicit `CORE REDEFINITION` is approved.
- No skill, agent, node, feature, workflow, subsystem, or implementation may redefine Curo merely because it is useful or mature.
- Unknown provenance stays unknown until the appropriate selected mechanism establishes it.
- Process success is not validation success; authoritative JSON persistence is schema-gated.
- Canonical process execution uses an executable plus `args[]` with `shell=False`.
- When the included harness extension is selected, file access is constrained by resolved workspace/evidence boundaries and persisted telemetry is redacted by default.

The current protocol-integrity behavior and its residual limits are specified in [`docs/addendum-b-protocol-integrity.md`](docs/addendum-b-protocol-integrity.md).
- Model output is a proposal until validated.
- Deterministic mechanisms outrank model judgment.
- The component that performs a check must write the check result.
- Do not overwrite unrelated files outside this project package.
