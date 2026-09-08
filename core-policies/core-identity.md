# Curo Core Identity Contract

## Canonical identity

Curo is a **small, modular, model-agnostic framework** around which reusable AI capabilities can be built, composed, replaced, and evolved.

Curo provides the stable socket, not the appliance.

Skills, agents, nodes, validators, workflows, governance, observability, execution systems, research systems, adapters, and future capabilities may attach to Curo, but none of them defines Curo by itself.

## Core invariants

### CI-001 — Core minimalism
Curo core MUST contain only the concepts required for Curo to remain a modular, model-agnostic framework.

### CI-002 — Extension by default
New functionality MUST default to extension/module status. Importance, complexity, popularity, or implementation maturity do not make a feature part of core.

### CI-003 — No feature capture
No skill, agent, node, feature, workflow, subsystem, harness, governance mechanism, validator, or implementation may silently redefine Curo around itself.

### CI-004 — Model/provider agnosticism
Canonical Curo semantics MUST NOT depend on one specific model, provider, agent product, or vendor environment. Provider-specific behavior belongs behind adapters or projections.

### CI-005 — Removability test
For every proposed capability ask: **If this capability were removed, would Curo still be Curo?**

If YES, it belongs outside core.
If NO, treat the proposal as a potential core change and require explicit architectural review.

### CI-006 — Composition over absorption
Capabilities should attach through explicit boundaries and contracts instead of being absorbed into an increasingly monolithic core.

### CI-007 — Explicit redefinition only
Changing what Curo fundamentally is requires an explicit `CORE REDEFINITION` decision approved by the requester. Ordinary feature work may not redefine the framework implicitly.

## Core vs extensions

```text
CURO CORE
= identity
+ module boundaries
+ composition rules
+ portability rules
+ extension rules

EVERYTHING ELSE
= skills
+ agents
+ nodes
+ validators
+ workflows
+ governance
+ observability
+ execution systems
+ research systems
+ domain modules
+ adapters
+ future capabilities
```

## Description rule

Prefer:

> Curo is a modular, model-agnostic framework. It includes/provides/composes X.

Avoid:

> Curo is X.

when X is a single capability such as a harness, orchestrator, governance system, validator, runtime, project manager, or evidence platform.

## Architectural maxim

> **Ask “How does this plug into Curo?” before asking “How do we add this to Curo?”**
