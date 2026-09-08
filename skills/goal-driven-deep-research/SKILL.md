# Skill: Goal-Driven Deep Research

## Purpose

Use Deep Research as a bounded Curo extension that advances a decision goal through explicit investigations, evidence capture, contradiction search, unknown tracking, and stopping rules.

The goal is not complete because a report exists. The goal is complete only when sufficient evidence exists to support the requested decision, or when the system records that evidence remains insufficient.

This skill does not redefine Curo core.

## Required references

Before use, read:

1. `core-policies/core-identity.md`
2. `core-policies/drift-check.md`
3. `skills/model-package-design/SKILL.md`
4. `skills/goal-driven-deep-research/retrieval-policy.md`
5. `skills/goal-driven-deep-research/evidence-policy.md`
6. `skills/goal-driven-deep-research/contradiction-policy.md`
7. `skills/goal-driven-deep-research/stopping-rules.md`

## Canonical lifecycle

```text
GOAL
  ↓
DECOMPOSE INTO INVESTIGATIONS
  ↓
RETRIEVE EVIDENCE
  ↓
RECORD FINDINGS + CONTRADICTIONS + UNKNOWNS
  ↓
CRITIC / GAP REVIEW
  ↓
IS EVIDENCE SUFFICIENT?
  ├─ NO → launch next bounded investigation
  └─ YES → produce decision-readiness packet
```

## Research behavior

- Separate evidence from inference.
- Prefer primary sources when available.
- Use secondary sources for discovery, synthesis, and context.
- Search explicitly for contradictory evidence.
- Preserve unresolved unknowns.
- Do not convert model confidence into factual certainty.
- Do not claim deterministic verification from model judgment.
- Do not suppress evidence because it conflicts with a preferred architecture.
- Do not declare the implementation complete; this skill produces research and decision-readiness artifacts.

## Required package inputs

```text
goal.yaml
context.yaml
constraints.yaml
research-plan.yaml
```

## Required research outputs

```text
research/
├── investigations.json
├── findings.json
├── evidence.jsonl
├── contradictions.json
├── unknowns.yaml
└── decision-readiness.json
```

## Investigation rule

Each investigation MUST have:

- a bounded question;
- relevance to the goal or decision;
- retrieval scope;
- source-quality expectations;
- completion criteria;
- unresolved unknown tracking.

## Completion rule

An investigation is complete only when its completion criteria are met or it is explicitly marked `BLOCKED` or `INSUFFICIENT_EVIDENCE`.

The overall goal may transition to decision-ready only when the stopping rules permit it.

## Output authority

Deep Research outputs are evidence and research-state artifacts. They may inform downstream LLM reasoning, architecture, recommendations, and plans, but downstream models MUST distinguish:

```text
evidence
inference
recommendation
unknown
```

## Drift classification

This skill is a Curo `EXTENSION`.
