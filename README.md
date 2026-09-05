# Curo

Model-agnostic AI systems operating standard and addendum package.

This project is organized for both human reading and machine processing. The canonical intent is:

- keep the operating standard model-neutral
- preserve provenance and version metadata
- separate policy, schema, harness, registry, provenance, replay, adapter, and anti-pattern concerns
- make ownership and validation explicit

## Canonical content

- `project.yaml` - machine-readable project metadata and lineage
- `docs/INDEX.md` - human navigation index and reading paths
- `docs/operating-standard.md` - integrated standard, accepted refinements, and five applied reasoning patterns
- `docs/addendum-a.md` - patch notes for the accepted amendments
- `docs/gaps-and-roadmap.md` - current maturity, known gaps, and extension order
- `scripts/validate_curo.py` - dependency-free self-check for package integrity
- `templates/project-kickoff.md` - human kickoff brief for applying Curo to a new project
- `templates/project-kickoff.yaml` - machine-readable kickoff equivalent

## Folder map

- `core-policies/` - governing rules and precedence
- `schemas/` - JSON and YAML structure contracts
- `anti-patterns/` - known failure modes and avoidance rules
- `adapters/` - model/provider interface expectations
- `harness/` - enforcement and execution boundaries
- `observability/` - run records, status, evidence links, checkpoints, and HITL boundaries
- `review/` - event-triggered Exception Review Protocol, findings, correction, and HITL artifacts
- `registry/` - canonical inventory of artifacts and ownership
- `provenance/` - sample record formats and trace notes
- `replay/` - manifests for rerun and verification
- `docs/` - narrative reference material
- `templates/` - reusable project initialization templates

## How to use

1. Read `project.yaml` first for scope, ownership, and lifecycle.
2. Read `docs/operating-standard.md` for the integrated operating model.
3. Use the relevant folder when making changes:
   - policy changes go in `core-policies/`
   - record shape changes go in `schemas/`
   - failure-mode updates go in `anti-patterns/`
   - provider integration changes go in `adapters/`
   - validation or enforcement changes go in `harness/`
   - exception review and HITL changes go in `review/`
   - inventory or naming changes go in `registry/`
   - evidence and trace updates go in `provenance/`
   - rerun packaging changes go in `replay/`

## Non-negotiable rules

- Unknown provenance stays unknown until the harness establishes it.
- Model output is a proposal until validated.
- Deterministic mechanisms outrank model judgment.
- The component that performs a check must write the check result.
- Do not overwrite unrelated files outside this project package.
