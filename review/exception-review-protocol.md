# Exception Review Protocol

## Purpose

Provide a bounded recovery path when normal planning or execution encounters a
material disagreement, failed validation, conflicting evidence, elevated risk,
or repeated non-convergence.

## State model

```text
NORMAL_WORKFLOW
  -> EXCEPTION_REVIEW_ACTIVE
  -> RESOLVED_AUTOMATICALLY
  -> RESOLVED_BY_MODEL
  -> RESOLVED_BY_EVIDENCE
  -> ESCALATED_TO_HITL
  -> BLOCKED
```

After resolution, the harness returns the workflow to its prior state unless an
authorized decision records a different transition.

## Activation triggers

Activate only for a material event:

- failed validation or cross-field contradiction
- conflicting authoritative evidence
- unresolved ownership or attempted authority override
- correctness dispute that changes expected behavior
- security, privacy, safety, regulatory, or irreversible-action concern
- schema, contract, scope, architecture, provider, tool, MCP, or hook change
- repeated non-convergence after the configured correction limit

## Review posture

Reviewers are adversarial but fair. They must identify assumptions, provide a
counterexample or failure mode, cite current-source evidence, and state an
acceptance test. Reviewers do not create authority by agreeing with one another.

## Finding classes

| Class | Default handler |
|---|---|
| `mechanical` | Harness or deterministic correction |
| `engineering` | Model proposes; validator verifies |
| `evidence_required` | Produce the missing check or artifact |
| `human_decision` | Batch into a HITL packet |

## Convergence policy

The harness should batch findings and allow a bounded number of correction
cycles. The default is three model revision cycles and two repetitions of the
same unresolved finding. Escalate after the limit rather than relaying another
individual correction through the requester.

Agreement means the requirements, ownership, evidence, and tests converge. It
does not require uniform reviewer preference.

## HITL boundary

Escalate when the unresolved issue changes authority, correctness, risk, scope,
or a user-owned decision. Do not escalate formatting, enum casing, registry
completion, path normalization, or other mechanically verifiable findings.

The HITL packet must state the decision, why automation cannot decide it,
available options, tradeoffs, recommended option, affected artifacts, and the
workflow transition authorized by the requester.
