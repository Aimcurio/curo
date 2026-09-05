# Curo Documentation Index

This index is the human navigation entry point for the Curo package. Start with the root [`README.md`](../README.md) and [`project.yaml`](../project.yaml) when you need package scope, ownership, lineage, or lifecycle metadata.

## Recommended reading paths

### Understand the standard

1. [`operating-standard.md`](operating-standard.md) - canonical integrated standard.
2. [`addendum-a.md`](addendum-a.md) - accepted amendments and refinements that were integrated into the standard.
3. [`../core-policies/precedence.md`](../core-policies/precedence.md) - order of authority when rules conflict.
4. [`gaps-and-roadmap.md`](gaps-and-roadmap.md) - what is implemented in the foundation and what projects must add.

The operating standard includes five applied reasoning patterns: successful
execution, cancellation or early termination, dependency failure,
unverifiable provenance, and component replacement. Use them as design
walkthroughs when starting any project or workflow, whether deterministic,
AI-assisted, or hybrid.

### Implement the system

1. [`../core-policies/ownership.md`](../core-policies/ownership.md) - who owns each system property.
2. [`../harness/harness-contract.md`](../harness/harness-contract.md) - enforcement and execution boundary.
3. [`../adapters/adapter-contract.md`](../adapters/adapter-contract.md) - provider/model adapter boundary.
4. [`../schemas/provenance-record.schema.json`](../schemas/provenance-record.schema.json) - evidence record shape.
5. [`../schemas/replay-manifest.schema.json`](../schemas/replay-manifest.schema.json) - replay package shape.

### Start a new project

1. [`../templates/project-kickoff.md`](../templates/project-kickoff.md) - fill-in brief for the requester.
2. [`../templates/project-kickoff.yaml`](../templates/project-kickoff.yaml) - machine-readable equivalent for tooling.
3. Use the completed brief to produce the project ownership table, contracts, implementation phases, validation gates, and replay plan.

### Observe and govern runs

1. [`../observability/observability-contract.md`](../observability/observability-contract.md) - observability authority and update rules.
2. [`../observability/run-record-template.md`](../observability/run-record-template.md) - human-readable governed run record.
3. [`../observability/run-index-template.md`](../observability/run-index-template.md) - compact run index.
4. [`../observability/run-record.schema.json`](../observability/run-record.schema.json) - machine run-record contract.
5. [`../observability/run-event.schema.json`](../observability/run-event.schema.json) - machine observed-event contract.

Before promoting a Curo revision, run [`../scripts/validate_curo.py`](../scripts/validate_curo.py) to check required files, JSON schemas, registry paths and metadata, duplicate standard headings, and provenance sentinels.

### Operate and review

1. [`../core-policies/validation.md`](../core-policies/validation.md) - validation order and promotion gates.
2. [`../anti-patterns/anti-patterns.md`](../anti-patterns/anti-patterns.md) - failure modes to detect.
3. [`../registry/registry.yaml`](../registry/registry.yaml) - canonical artifact inventory.
4. [`../provenance/sample-provenance-record.yaml`](../provenance/sample-provenance-record.yaml) - example harness-owned evidence.
5. [`../replay/replay-manifest-template.yaml`](../replay/replay-manifest-template.yaml) - rerun and verification template.

### Resolve exceptions

1. [`../review/exception-review-protocol.md`](../review/exception-review-protocol.md) - event-triggered adversarial-but-fair review.
2. [`../review/findings-template.yaml`](../review/findings-template.yaml) - batched validator and reviewer findings.
3. [`../review/hitl-packet-template.yaml`](../review/hitl-packet-template.yaml) - consolidated requester decisions.
4. [`../schemas/review-findings.schema.json`](../schemas/review-findings.schema.json) - findings contract.
5. [`../schemas/hitl-packet.schema.json`](../schemas/hitl-packet.schema.json) - HITL escalation contract.

## Folder map

| Folder | Purpose | Primary authority |
|---|---|---|
| [`core-policies/`](../core-policies/README.md) | Ownership, precedence, and validation rules | Policy artifacts |
| [`schemas/`](../schemas/README.md) | Machine-readable record contracts | JSON Schema files |
| [`anti-patterns/`](../anti-patterns/README.md) | Known failure modes and detection guidance | Anti-pattern catalog |
| [`adapters/`](../adapters/README.md) | Provider and model integration boundary | Adapter contract |
| [`harness/`](../harness/README.md) | Enforcement, execution, and evidence boundary | Harness contract |
| [`observability/`](../observability/README.md) | Human-readable run summaries and runtime event contracts | Observability contract |
| [`registry/`](../registry/README.md) | Artifact inventory and canonical paths | Registry YAML |
| [`provenance/`](../provenance/README.md) | Evidence and trace examples | Harness-produced records |
| [`replay/`](../replay/README.md) | Reproducibility and rerun manifests | Harness-produced manifests |
| [`docs/`](README.md) | Narrative standard and navigation | This index and canonical standard |
| [`templates/`](../templates/README.md) | Reusable project kickoff templates | Template files |

## Change routing

Put a proposed change in the narrowest folder that owns it. Update the registry when a canonical artifact is added, removed, renamed, or promoted. Update the standard or addendum when the governing meaning changes. Validate machine-readable files before promotion and preserve prior versions when replacing an active artifact.
