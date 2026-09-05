# Model-Agnostic AI Systems Operating Standard - Addendum A

This addendum captures the accepted amendments and refinements from the latest conversation thread. It patches the main standard rather than replacing it.

## Accepted refinements

- The four-discipline split is real and useful: prompt, context, harness, loop.
- The engineering hierarchy is the default order of operations.
- GP-003 and GP-004 are first-class principles:
  - model output is a proposal until validated
  - deterministic mechanisms outrank model judgment
- Unknown provenance stays UNKNOWN.
- Harness-owned evidence is required.
- Assertion ownership follows observation ownership.
- Anti-pattern detection must be executed by the harness, not self-reported by the model.

## Amendment summary

### Amendment 1

A model process must have no write path to authoritative records. This is a property requirement, not a single implementation requirement.

### Amendment 2

Registry entries need explicit ownership and source pointers so provenance can be traced without inference.

### Amendment 3

Capability measures must come from evidence, not self-report.

### Amendment 4

Raw provider outputs must be preserved where possible so later review can inspect the original source of truth.

### Amendment 5

Retention rules must preserve the evidence trail long enough to support replay, review, and failure analysis.

### Amendment 6

Conflict handling must be explicit, but no rule should hard-block all conflict severity. Conflict handling must classify, route, and escalate by severity.

### Amendment 7

Registry citation requirements are only valid if enforcement is external to the model.

### Amendment 8

The harness must execute the actual anti-pattern query. The model may propose the query, but it may not attest to having run it unless the harness ran it.

## Final principle

If a field claims a check happened, the component that performed the check owns the field.
