# Curo Framework-Capture Anti-Patterns

## AP-001 — FRAMEWORK_COLLAPSE
A secondary capability becomes described or implemented as Curo's primary identity.

Examples:
- “Curo is a deterministic governance harness.”
- “Curo is an agent orchestrator.”
- “Curo is a project-management system.”
- “Curo is an LLM runtime.”
- “Curo is a validation engine.”

Corrective rule: reframe as “Curo includes/provides/composes X” unless an explicit `CORE REDEFINITION` has been approved.

## AP-002 — RECENCY_CAPTURE
The most recently developed subsystem receives disproportionate architectural importance because it dominates current discussion.

Detection question: **Would we describe Curo this way if this subsystem had not been worked on recently?**

## AP-003 — IMPLEMENTATION_BECOMES_IDENTITY
Existing code structure is treated as proof of conceptual identity.

Architecture defines implementation boundaries. Implementation does not silently redefine architecture.

## AP-004 — PROVIDER_CAPTURE
A model, provider, agent environment, or vendor-specific feature leaks into canonical Curo semantics.

Mitigation: isolate provider-specific behavior behind an adapter or projection.

## AP-005 — GOVERNANCE_CAPTURE
Governance, validation, authority, evidence, or provenance becomes treated as the purpose of the entire framework.

## AP-006 — ORCHESTRATION_CAPTURE
Multi-agent routing or execution becomes assumed to be Curo's universal topology.

## AP-007 — NODE_CAPTURE
A powerful domain node or specialized node becomes privileged as the framework's defining center.

## AP-008 — SKILL_CAPTURE
A reusable skill or skill family becomes mandatory to the definition of Curo instead of remaining a composable extension.

## AP-009 — SCOPE_INFLATION
A local feature request is solved by expanding Curo core instead of adding a bounded extension.

## AP-010 — TERMINOLOGY_DRIFT
Terms change meaning across documents without an explicit decision: module→agent, capability→runtime, framework→harness, optional subsystem→mandatory core.

## AP-011 — MONOLITHIC_COMPOSITION
Independent capabilities become fused so tightly that they cannot be selected, replaced, upgraded, or omitted independently.

## AP-012 — UNAPPROVED_CORE_REDEFINITION
A sequence of individually reasonable improvements cumulatively changes what Curo is without a deliberate, requester-approved decision.

## Default mitigation

Before major architecture work, read:
1. `core-policies/core-identity.md`
2. `core-policies/drift-check.md`

The burden of proof belongs to any proposal that expands Curo core.
