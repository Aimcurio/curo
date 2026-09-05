# Exception Review

This folder defines Curo's event-triggered Exception Review Protocol. It is
not the normal planning state. It is entered when validation fails, evidence
conflicts, ownership is unclear, risk increases, scope changes, or bounded
model correction does not converge.

## Files

- [`exception-review-protocol.md`](exception-review-protocol.md) - operating rules and state transitions.
- [`findings-template.yaml`](findings-template.yaml) - batched findings and correction actions.
- [`hitl-packet-template.yaml`](hitl-packet-template.yaml) - consolidated human decisions.

## Operating rule

Use an adversarial-but-fair posture inside the protocol. Resolve mechanical
findings automatically, require evidence for factual claims, and escalate only
authority, correctness, risk, scope, or persistent-convergence issues to HITL.
Return to the prior workflow state after the event is resolved.
