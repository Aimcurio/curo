# Registry

This folder provides the machine-readable inventory of governed artifacts, their paths, versions, ownership, and source pointers.

Curo uses two registry levels:

1. `registry.yaml` — repository-wide canonical inventory for shared/core artifacts and major project-level records.
2. Scoped registry shards — authoritative inventories for bounded extensions with multiple internal artifacts.

Scoped shards prevent large extension modules from forcing unsafe whole-file rewrites of the central registry and let an extension own its internal inventory without becoming part of Curo core.

## Files

- [`registry.yaml`](registry.yaml) - repository-wide canonical artifact registry.
- [`deep-research.yaml`](deep-research.yaml) - complete artifact inventory for `skills/goal-driven-deep-research/`.

## Provenance rule

Every governed entry must include a `source` pointer or be covered by a scoped module manifest whose provenance is explicit. The pointer may identify the originating conversation, governing artifact, requester decision, or review decision. Provenance must not depend on inference.

## Change rule

Every canonical artifact must appear exactly once in either:

- the repository-wide registry, or
- an explicitly declared scoped registry shard referenced by `project.yaml`.

Do not duplicate the same artifact as authoritative in both levels.

Registry entries are metadata about artifacts; they do not replace the artifacts or their validators.
