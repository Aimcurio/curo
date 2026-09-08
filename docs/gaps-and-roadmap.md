# Gaps And Roadmap

This document records what Curo currently is, what it does not yet implement,
and the order for extending it. It prevents a documented policy from being
mistaken for an already-enforced capability.

## Current status

| Area | Status | Meaning |
|---|---|---|
| Operating standard | Ready | Human-readable governing rules exist. |
| Kickoff templates | Ready | Human and machine-readable project intake exists. |
| Project profiles | Implemented core | Project-specific intent is schema-governed under `projects/<project-id>/project.yaml`; approval remains human-owned. |
| LLM/agent assignments | Implemented core | Deterministic manifests bind desired/resolved roles to the canonical profile hash; exact provider/model choices remain project decisions. |
| Core policies | Ready | Ownership, precedence, and validation rules exist. |
| Provenance and replay schemas | Implemented | Harness writers validate provenance and the two distinct replay artifact classes before persistence. |
| Observability layer | Implemented core | The local harness emits schema-valid run records; indexes and domain-specific events remain project extensions. |
| Executable runtime | Implemented core | Standard-library-first structured execution, containment, redaction, timeout handling, and atomic evidence writes are regression-tested. |
| Curo package self-check | Ready | `scripts/validate_curo.py` checks structure plus runtime/schema IDs, enums, replay class separation, BOM policy, and registry coverage. |
| Project contract CLI | Implemented core | Local commands validate profiles, deterministically compile assignments from approved intent, and verify profile linkage. |
| Project domain validation | Project extension | Each project must still provide or adopt verified domain-specific validators. |
| Tools, MCP, and hooks | Extension area | Contracts and permissions must be defined per project before use. |
| Evaluation runner | Planned | Project-specific evaluation cases and runners are still required. |
| Review and promotion automation | Foundation | Event-triggered exception review, batched findings, correction limits, and HITL packet contracts exist; runtime automation remains project-specific. |
| Learning and distillation | Implemented proposal writer | The harness emits schema-valid candidates for five canonical types; validation, approval, and promotion remain governed steps. |

## Learning brain and evaluation backlog

The learning brain must treat ChatGPT and Antigravity product/base files as
read-only sources. User-owned global rules and skills are controlled promotion
targets, not automatic write destinations. No candidate may modify an agent,
skill, rule, or global configuration before evaluation and explicit approval.

### P0 - Build the evaluation and benchmark foundation

- [ ] Define versioned schemas for evaluation cases, benchmark suites, run
  results, scorecards, and promotion recommendations.
- [ ] Create `evaluations/` and `benchmarks/` with golden tasks, failure cases,
  adversarial cases, and regression fixtures.
- [ ] Implement a deterministic evaluation runner with reproducible inputs,
  environment metadata, hashes, and replay references.
- [ ] Define hard safety gates for authority compliance, path containment,
  provenance, evidence quality, schema validity, and critical regressions.
- [ ] Define scored measures for task correctness, completeness, portability,
  latency, cost, and unnecessary tool use.
- [ ] Compare the installed incumbent and isolated candidate on the same suite;
  never treat a higher aggregate score as overriding a failed hard gate.
- [ ] Add benchmark tests for rules, agent instructions, new skills, compatible
  skill updates, breaking skill versions, validators, and anti-patterns.
- [ ] Add model- and provider-portability runs where a candidate claims to be
  model agnostic.

### P1 - Implement the governed learning intake

- [ ] Define a read-only import contract for `/learn` output from Antigravity,
  ChatGPT, and other approved sources.
- [ ] Preserve source platform, conversation/run identifiers, original proposal,
  evidence references, source hashes, and approval state.
- [ ] Normalize imported findings into Curo learning candidates without writing
  to source-platform base or configuration files.
- [ ] Separate `LEARN`, `ANALYZE`, and `EXPLAIN` intents so an analysis request is
  not misreported as a completed learning cycle.
- [ ] Extend the learning utility to inspect a requested topic, task, run, or
  evidence bundle and return reusable findings rather than requiring the user to
  supply the conclusion.
- [ ] Classify each finding as `rule`, `skill`, `anti_pattern`, `validator`, or
  `standard_amendment`, while retaining `no_candidate` as a valid outcome.
- [ ] Generate an isolated candidate implementation, required evaluations,
  rollback plan, and proposed target scope.

### P1 - Implement recommendation and approval

- [ ] Produce an evidence-backed recommendation to update an agent, update an
  existing skill, create a compatible skill version, create a breaking/new
  version, create a separate skill, defer, or reject.
- [ ] Require explicit human approval for the exact candidate content, version,
  scope, and target before promotion.
- [ ] Keep candidate approval separate from implementation authorization and
  promotion completion.
- [ ] Record rejected, superseded, blocked, and inconclusive candidates so they
  are not silently rediscovered or treated as approved.

### P2 - Implement controlled promotion and learning observability

- [ ] Add adapters for approved user-owned global rule and skill locations;
  exclude Antigravity and ChatGPT product/base files from writable targets.
- [ ] Verify the destination, current version, expected hash, backup/rollback,
  and write boundary immediately before promotion.
- [ ] Create a versioned promotion record and run the regression suite after the
  promoted artifact is installed.
- [ ] Roll back or block promotion when post-install regression fails.
- [ ] Add a learning registry that links observation, candidate, benchmark
  scorecard, approval, promoted version, and regression result.
- [ ] Expose a read-only summary suitable for a future Curo development portal;
  the portal must not become the authority or promotion mechanism.

### Initial benchmark candidates

- [ ] Evidence-tag discipline for research and architecture documents: test
  factual traceability, false tagging, excessive tagging, and validator support.
- [ ] Antigravity-specific large-file delivery: test exact bytes, encoding,
  special characters, long paths, failure recovery, and source-tool drift before
  considering a user-global skill.
- [ ] Research-document acceptance audit: test against seeded shallow sections,
  false citations, missing metric fields, missing threat fields, and unsupported
  conclusions; treat it as a skill candidate rather than an automatic rule.

### Learning-brain readiness gate

The learning brain is ready for promotion-capable use only when the benchmark
runner is reproducible, hard gates are enforced, incumbent-versus-candidate
comparison is recorded, imports are read-only, approval is content-bound, global
writes are adapter-controlled, and post-promotion regression plus rollback have
been demonstrated end to end.

## Required project extensions

Every new project starts with `projects/<project-id>/project.yaml` and
`llm-assignments.json`, then adds only the extensions it needs:

- `contracts/` for domain-specific schemas
- `runtime/` or `server/harness/` for execution control
- `scripts/` for deterministic checks and preflight
- `tools/`, `mcp/`, and `hooks/` for authorized capabilities
- `evaluations/` for expected behavior and failure cases
- `provenance/` and `replay/` for run evidence
- `learning/` for evidence-backed proposals and promotion records

## Recommended build order

1. Validate the generic kickoff against [`../schemas/project-kickoff.schema.json`](../schemas/project-kickoff.schema.json).
2. Propose a project-specific profile and validate it against [`../schemas/project-profile.schema.json`](../schemas/project-profile.schema.json).
3. Review and obtain human approval for consequential intent and authority decisions.
4. Compile and validate [`../schemas/llm-assignments.schema.json`](../schemas/llm-assignments.schema.json) from the approved profile using an explicit reference time.
5. Freeze the project ownership table and canonical contracts.
6. Authorize and build the smallest bounded deterministic or fake-adapter slice.
7. Add project-specific runtime enforcement, tools, MCP servers, and hooks only with explicit permissions.
8. Add evaluations for success, failure, cancellation, provenance, and portability where applicable.
9. Add provenance and the appropriate execution-replay or artifact-verification writers.
10. Run package integrity and promotion checks.
11. Use Exception Review Mode only when a qualifying event occurs; return to the prior workflow state after resolution.
12. Promote reusable patterns back into Curo only after evidence from more than one project.

## Promotion rule

A project artifact should become part of Curo only when it is reusable across
projects, has an explicit owner, has deterministic checks where feasible, has
documented failure behavior, and has evidence that it works independently of a
single provider or framework.
