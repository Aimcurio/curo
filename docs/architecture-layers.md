# Curo Architecture Layers

## Layer 1 — Curo Core

High-stability identity and extension semantics.

The core answers only the questions needed to keep Curo coherent:

- What is Curo?
- What is an extension/module boundary?
- How are capabilities composed?
- What makes an extension portable and model-agnostic?
- What rules govern extension and replacement?
- What constitutes a core redefinition?

Core changes should be rare.

## Layer 2 — Curo Extensions

Fast-evolving reusable functionality.

```text
skills
agents / role profiles
nodes / domain modules
validators
guards
workflows
specifications
governance
observability / evidence
adapters
execution integrations
research modules
project / lifecycle modules
future capabilities
```

Extension changes may be frequent.

## Dependency rule

Extensions may depend on stable Curo core contracts.

Curo core MUST NOT acquire a dependency on one specific extension merely because that extension is useful, sophisticated, mature, or widely used.

## Description rule

Canonical documentation should use:

> Curo is [core identity]. It includes/provides/composes [extension].

Avoid:

> Curo is [one extension].

## Extension rule

When a new feature is proposed, first attempt to classify it as Layer 2.

Only classify it as Layer 1 when the feature changes the semantics required for Curo to remain Curo.

## Architecture-review footer

```text
CORE IMPACT: NONE | COMPATIBLE EXTENSION | TENSION | REDEFINITION
CAPABILITY CATEGORY:
NEW CORE PRIMITIVE REQUIRED: YES | NO
DRIFT CHECK: PASS | ESCALATE
```
