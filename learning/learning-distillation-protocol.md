# Learning Distillation Protocol

## Purpose

Convert evidence-backed execution failures, corrections, and reusable patterns
into bounded proposals for anti-patterns, validators, tests, harness changes,
project rules, skills, or Curo amendments.

## Lifecycle

```text
OBSERVED_RUN
  -> LEARNING_ELIGIBLE
  -> CANDIDATE_PROPOSED
  -> VALIDATION_PENDING
  -> VALIDATED
  -> HITL_REQUIRED or PROJECT_PROMOTION
  -> PROMOTED or REJECTED
  -> REGRESSION_VERIFIED
```

Observability records eligibility and references. The learning utility creates a
proposal. The harness or evaluation pipeline establishes validation. The
registry and authorized approver establish promotion.

## Eligible triggers

- failed, blocked, partial, cancelled, or materially reviewed run
- repeated finding or repeated correction
- successful behavior worth preserving as a reusable pattern
- HITL escalation or newly discovered anti-pattern

## Required evidence

Every candidate must link to source run IDs, event IDs, finding IDs, and concrete
evidence. A model explanation may be recorded as a proposal, but it cannot be
treated as an established root cause without an observation or test.

## Promotion boundary

Canonical Curo policy, standard, addendum, ownership, and registry changes
require HITL approval. Project-local changes may be promoted by the project
owner after validation, provenance, rollback, and regression coverage are
recorded.

Confirmed corrections are closed in the current revision and revalidated. If an
external constraint prevents correction, record the blocker and notify the
requester; do not silently repeat the same finding.
