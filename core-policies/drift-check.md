# Curo Architectural Drift Check

Every major Curo architecture proposal MUST be classified as exactly one of:

- `NO_DRIFT` — preserves identity and existing boundaries.
- `EXTENSION` — adds a capability/module without changing core identity.
- `TENSION` — useful change that pressures one or more core invariants.
- `REDEFINITION` — changes what Curo fundamentally is and requires explicit requester approval.

## Required checks

1. **Identity check** — Restate Curo's canonical identity in one sentence.
2. **Change-type check** — Classify the proposal as core, module, primitive, adapter, validator, rule, skill, agent/role, node, workflow, guard, governance capability, observability capability, execution capability, domain capability, or other.
3. **Removability check** — If removed, would Curo still be Curo?
4. **Center-of-gravity check** — Does this make a secondary capability the primary explanation of Curo?
5. **Model-agnostic check** — Does canonical behavior depend on one model/provider/environment?
6. **Modularity check** — Can the capability be replaced, upgraded, or omitted without rewriting unrelated Curo components?
7. **Lineage check** — Which core principle or approved decision does this derive from?
8. **Semantic-reframing check** — Did wording shift from “Curo has X” to “Curo is X” without an approved redefinition?
9. **Scope-inflation check** — Is a local problem being solved by expanding the entire framework?
10. **Final drift decision** — Record the classification and required action.

## Machine-readable review footer

```yaml
curo_drift_review:
  identity_restated: ""
  change_type: ""
  removal_preserves_identity: true
  center_of_gravity_shift: false
  model_agnostic: true
  modular_boundary_preserved: true
  lineage: []
  semantic_reframing_detected: false
  scope_inflation_detected: false
  classification: NO_DRIFT
  required_action: none
  reviewer_notes: ""
```

## Approval policy

- `NO_DRIFT` → ordinary change process.
- `EXTENSION` → ordinary architecture review; register the new module/category if needed.
- `TENSION` → architecture decision required before implementation.
- `REDEFINITION` → explicit `CORE REDEFINITION` record and requester approval required.

Recent implementation sophistication is never proof that the implemented subsystem represents Curo's core identity.
