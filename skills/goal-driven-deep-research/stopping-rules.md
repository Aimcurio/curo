# Goal-Driven Deep Research Stopping Rules

## Principle

Research stops when the decision is supportable, not when a report has been written and not when arbitrary source-count targets are reached.

## Investigation-level stopping

An investigation may close when one of these states is justified:

- `COMPLETE` — completion criteria met.
- `BLOCKED` — required access/data is unavailable.
- `INSUFFICIENT_EVIDENCE` — relevant retrieval was attempted but support remains inadequate.
- `SUPERSEDED` — another investigation made it unnecessary.

Before `COMPLETE`, confirm:

- required evidence was retrieved;
- source quality was assessed;
- contradiction search was performed where material;
- remaining unknowns were recorded;
- additional retrieval is unlikely to materially change this investigation's answer.

## Goal-level decision readiness

The goal may be marked `DECISION_READY` only when:

- the decision question is explicit;
- all critical investigations are complete, blocked, or explicitly insufficient;
- high-materiality contradictions are resolved or carried forward as accepted uncertainty;
- critical unknowns are below the decision's tolerance threshold or explicitly prevent a decision;
- evidence is traceable to the material findings;
- the permitted outcome set includes `INSUFFICIENT_EVIDENCE`.

## Required final outcomes

A goal-driven research run must terminate in one of:

- `DECISION_READY`
- `INSUFFICIENT_EVIDENCE`
- `BLOCKED`
- `CANCELLED`

It must not manufacture certainty merely to avoid `INSUFFICIENT_EVIDENCE`.

## Marginal-value rule

Launch another investigation only when its expected information could materially change:

- the recommended decision;
- confidence in a material finding;
- resolution of a high-materiality contradiction;
- or a critical unknown.
