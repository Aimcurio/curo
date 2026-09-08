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
- `docs/INDEX.md` - human navigation index and reading paths
- `docs/operating-standard.md` - integrated standard, accepted refinements, and five applied reasoning patterns
- `docs/addendum-a.md` - patch notes for the accepted amendments
- `docs/gaps-and-roadmap.md` - current maturity, known gaps, and extension order
- `skills/model-package-design/SKILL.md` - portable hybrid Markdown/YAML/JSON/JSONL/JSON-Schema packaging skill
- `agents/architecture-review.md` - agent-facing identity and drift guard for architecture work
- `scripts/validate_curo.py` - dependency-free self-check for package integrity
- `templates/project-kickoff.md` - human kickoff brief for applying Curo to a new project
- `templates/project-kickoff.yaml` - machine-readable kickoff equivalent

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
- `replay/` - manifests for rerun and verification
- `docs/` - narrative reference material
- `templates/` - reusable project initialization templates
- `scripts/` - dependency-free integrity and promotion checks

## How to use

1. Read `project.yaml` first for package metadata and lifecycle.
2. Read `core-policies/core-identity.md` before interpreting any subsystem as representative of the whole framework.
3. Read `core-policies/drift-check.md` before major architecture changes.
4. Read `docs/operating-standard.md` for the integrated operating model.
5. Use the relevant extension folder when making changes.
6. Ask **“How does this plug into Curo?”** before asking **“How do we add this to Curo?”**

## Non-negotiable rules

- Curo core stays small; extensions remain extensions unless an explicit `CORE REDEFINITION` is approved.
- No skill, agent, node, feature, workflow, subsystem, or implementation may redefine Curo merely because it is useful or mature.
- Unknown provenance stays unknown until the appropriate mechanism establishes it.
- Model output is a proposal until validated where validation is required.
- Deterministic mechanisms outrank model judgment for deterministically checkable claims.
- The component that performs a check must write the check result.
- Do not overwrite unrelated files outside this project package.
