# Model-Agnostic AI Systems Operating Standard

Document version: 1.8.0
Updated: 2026-09-05  
Status: Canonical

## Purpose

This standard defines how to design, build, operate, validate, reuse, and evolve AI-assisted workflows without depending on any single model, vendor, interface, agent framework, or product.

The core idea is simple:

> Models are replaceable reasoning engines. The workflow, state, validation, evidence, and operating contracts are the system.

## Maturity and extension boundary

Curo is a foundation, not a completed universal runtime. This standard defines
portable meaning, ownership, contracts, and promotion rules. A project may add
an executable runtime, scripts, tools, MCP servers, hooks, adapters, and domain
validators, but those extensions remain project-specific until they are proven
reusable and promoted into the Curo foundation.

The standard must not claim that an enforcement capability exists merely because
its policy is documented. A capability is operational only when its implementing
component, deterministic checks, evidence output, and failure behavior have
been verified.

## Scope

This standard applies to:

- prompts
- context assembly
- harness behavior
- loop design
- validation
- provenance
- replay
- observability
- learning and distillation
- registry maintenance
- adapter boundaries
- anti-pattern management
- project kickoff and extension planning

The following are governed extension areas rather than implemented capabilities
of this package by default:

- executable runtime
- command-line scripts
- tool catalog
- MCP integrations
- lifecycle hooks
- evaluation runners
- review and promotion automation

It is intended to work across ChatGPT, ChatGPT Desktop, Gemini, DeepSeek, Claude, Google Antigravity, local models, hosted APIs, and future providers.

## Engineering hierarchy

Use this order of operations:

1. Can the harness enforce it?
2. Can context fix it?
3. Can the loop fix it?
4. Can the prompt fix it?
5. Only then consider changing the model.

This is the default diagnostic ladder. Do not skip directly to model replacement.

## Four disciplines

### Prompt engineering

Prompt engineering defines the immediate task:

- role
- objective
- constraints
- success criteria
- output shape
- escalation conditions

Prompts should stay thin. They should not become the system itself.

### Context engineering

Context engineering determines:

- what the model sees
- when it sees it
- how much it sees
- how evidence is prioritized
- what stays out of context

Context should be selective and progressive.

### Harness engineering

Harness engineering controls:

- tool invocation
- permissions
- state
- retries
- timeouts
- validation
- evidence capture
- replay packaging

### Loop engineering

Loop engineering controls iteration:

- plan
- act
- inspect
- validate
- recover
- continue or escalate

## Exception Review Protocol

Exception Review Mode is an event-triggered protocol, not a default workflow
state. The normal state remains standard planning or execution. Activate this
protocol only when a material issue prevents safe convergence.

Qualifying triggers include:

- failed validation or a material cross-field contradiction
- conflicting authoritative evidence
- unresolved ownership or an attempted authority override
- a correctness dispute that changes the expected result
- a security, privacy, regulatory, safety, or irreversible-action concern
- a schema, contract, scope, architecture, provider, tool, MCP, or hook change
- repeated non-convergence after bounded correction cycles

Inside Exception Review Mode, the review posture is adversarial but fair:
reviewers challenge assumptions, produce counterexamples, identify the
governing evidence, and propose an acceptance test. The harness batches the
findings and classifies them before asking for human input.

Use these finding classes:

- `mechanical`: fixable by deterministic rules or formatting
- `engineering`: model may propose a correction, which must be validated
- `evidence_required`: a check or artifact must be produced before resolution
- `human_decision`: the requester owns the decision

The harness may resolve mechanical findings and policy-settled disagreements.
It may allow only a bounded number of model correction cycles for engineering
findings. Escalate a consolidated HITL packet when the issue affects authority,
correctness, risk, scope, or remains unresolved after the correction limit.

The protocol exits with one of these outcomes:

- `RESOLVED_AUTOMATICALLY`
- `RESOLVED_BY_MODEL`
- `RESOLVED_BY_EVIDENCE`
- `ESCALATED_TO_HITL`
- `BLOCKED`

After exit, return to the workflow state that preceded the event. Do not mark a
project permanently adversarial because one exception occurred.

Agreement means convergence under requirements, evidence, ownership, and tests;
it does not require every reviewer to share the same preference. A plan must not
advance to implementation merely because reviewers agree if a human decision or
required evidence remains unresolved.

## Governing principles

- Model output is a proposal until validated.
- Deterministic mechanisms outrank model judgment.
- Unknown provenance should remain UNKNOWN. Never invent missing provenance.
- The component that performs a check must write the result of that check.
- Assertion ownership follows observation ownership.

## Ownership model

| Concern | Authoritative owner |
|---|---|
| Objective | Human / authorized caller |
| Operational state | Harness / state manager |
| Prompt template | Versioned artifact |
| Context selection | Context builder under harness policy |
| Tool authority | Harness / policy guard |
| Execution | Harness-controlled tool layer |
| Validation | Deterministic validator where feasible |
| Provenance | Harness |
| Evidence persistence | Harness |
| Replay manifests | Harness |
| Observability records and events | Harness / designated writer |
| Learning candidates | Model or analysis utility; proposal only |
| Learning validation and promotion | Harness, evaluation pipeline, and human approver where required |
| Capability measurements | Evaluation pipeline |
| Pending decisions | Human / authorized caller |

## Decision tree

Use this distinction:

- Rule: always-on behavior guardrail
- Skill: reusable procedure or runbook
- Agent: a named role with a behavioral contract
- Hook: event-triggered behavior
- MCP: external tool or service integration
- Plugin: distributable bundle that may contain rules, skills, hooks, and MCP configuration

## Validation order

1. Validate structure.
2. Validate evidence.
3. Validate ownership.
4. Validate replayability.
5. Validate only then promote.

## Learning and distillation

Learning is a post-execution governance loop. Observability identifies
evidence-backed runs and findings that are eligible for distillation; it does
not create or promote authoritative rules.

The learning utility may propose an anti-pattern, validator rule, regression
test, harness change, project rule, skill, or standard amendment. Every
candidate must link to source run, event, finding, and evidence identifiers.
Candidates remain proposals until deterministic validation, required testing,
and authorized promotion are complete.

A confirmed correction must be closed in the current revision, revalidated, and
protected by a regression guard when appropriate. If correction is prevented by
permissions, missing tools, inaccessible artifacts, service outage, quota, or
another external constraint, record and report the blocker rather than carrying
the same finding forward as unresolved.

Promotion to a canonical Curo policy, standard, addendum, ownership rule, or
registry authority requires HITL approval. Project-local rules may be promoted
within the project only when their owner, tests, provenance, and rollback path
are recorded.

## Failure handling

When a failure happens, record:

- what was attempted
- what was observed
- what was validated
- what remains unknown
- what changed

Do not fill gaps with guesses.

## Applied reasoning patterns

These patterns show how to use the standard when designing a real workflow.
They are reasoning guides, not provider-specific implementations or
sample payloads. For each pattern, move through the same sequence:

1. Define the situation and desired behavior.
2. Assign ownership before implementation.
3. Build the smallest contract that makes the behavior observable.
4. Enforce the contract in the harness or deterministic validator.
5. Preserve evidence and define the failure boundary.

### Pattern 1: Normal successful execution

**Situation:** A workflow receives an authorized input and is expected to reach
a valid completed state.

**Reasoning:** Start with the canonical request, message, and event contracts.
The interface or caller submits a canonical input. An adapter translates it for
the selected execution mechanism. The harness observes the returned events or
results, validates them, and decides whether completion actually occurred.

**Ownership decision:** A model or external component may propose content or a
result. The adapter owns format translation. The harness owns execution state,
completion status, validation, hashes, and provenance.

**Build order:** Define the input, output, and state contracts; build the
smallest deterministic or simulated execution; add the real execution adapter;
then add harness validation and evidence.

**Validation gate:** A response is promoted only when the request and events
are structurally valid, a completion event was observed, the final output was
persisted, and a harness-owned provenance record exists.

**Failure boundary:** A result without a valid terminal condition is partial or
incomplete output, not a completed execution.

### Pattern 2: Cancellation or early termination

**Situation:** A user, timeout, policy guard, or system event stops a workflow
before its normal terminal condition.

**Reasoning:** Cancellation is a state transition, not a special kind of
successful response. Preserve the partial output, record the cancellation, and
prevent the UI from presenting it as complete.

**Ownership decision:** The initiating actor requests cancellation. The harness
signals the execution mechanism, records the observed termination, and sets the
final state. The model or task component does not decide whether cancellation
succeeded.

**Build order:** Define explicit states such as `running`, `cancelled`, and
`complete`; implement an abort or stop path; preserve partial output or partial
work; then add the evidence record and replay expectation.

**Validation gate:** Confirm that cancellation was requested, execution was
actually terminated or reached a known terminal condition, partial work was
preserved where required, and `complete` was not asserted without completion
evidence.

**Failure boundary:** If termination cannot be verified, the completion status
remains `UNKNOWN` or `pending`; it must not be guessed from a visible screen or
an agent statement.

### Pattern 3: Dependency timeout or failure

**Situation:** A provider, tool, service, device, or other dependency times out,
rejects an input, or becomes temporarily unavailable.

**Reasoning:** Classify the error deterministically before deciding whether to
retry. A retry is a harness policy decision, not a model decision. Bound the
number of attempts and preserve each attempt as evidence.

**Ownership decision:** The adapter or integration reports the observed error. The
harness classifies retryability, applies the retry budget, updates state, and
escalates when the limit is reached.

**Build order:** Define normalized error categories, define retry limits, add
timeouts and cancellation, persist attempt records, and then expose recovery or
retry behavior.

**Validation gate:** Verify that only retryable errors are retried, attempts do
not exceed the configured limit, non-retryable failures stop immediately, and
the final state matches the observed outcome.

**Failure boundary:** A timeout is not a successful empty result. If the
dependency outcome is unknown, preserve that uncertainty and do not fabricate a
completed result.

### Pattern 4: Missing or unverifiable provenance

**Situation:** A workflow claims to have used a file, source, measurement, tool
result, or other input that was not actually supplied or verified.

**Reasoning:** Check context and evidence before allowing the response to claim
that the source was used. If the source is absent, the correct result is a
bounded response with `UNKNOWN` provenance, a request for the missing input, or
an explicit refusal to make the claim.

**Ownership decision:** The context builder records what entered context. The
harness records whether the source was available and verified. The model may
propose an interpretation but cannot establish source provenance.

**Build order:** Create an input or context manifest, attach source identifiers
to inputs, validate source availability, and add a guard against unsupported
claims.

**Validation gate:** Compare the model's source claims with the context and
tool evidence. Reject, qualify, or flag claims that cannot be grounded in an
observed source.

**Failure boundary:** Unknown provenance remains `UNKNOWN`. Never replace it
with a plausible filename, citation, or statement that the source was read.

### Pattern 5: Component replacement

**Situation:** The project must replace a provider, model, tool, service,
framework, or execution component without rewriting the workflow contract.

**Reasoning:** Treat the component as replaceable behind an adapter contract.
Keep canonical inputs, outputs, policies, validators, and evidence formats
stable. Compare components through the same evaluation cases and replay inputs.

**Ownership decision:** The adapter owns translation and raw-component details.
The application owns component-neutral behavior. The evaluation pipeline owns
capability measurements. The harness owns the evidence that makes the
comparison trustworthy.

**Build order:** Freeze the canonical contracts, implement the replacement
adapter, run the same evaluations, compare evidence and failure behavior, then
promote the replacement only after replay and validation checks pass.

**Validation gate:** Confirm that both providers satisfy the same event
contract, error states remain portable, provenance distinguishes raw facts from
inferences, and the workflow does not contain component-specific assumptions.

**Failure boundary:** A replacement component may improve capability, but it
does not repair a broken harness, missing evidence, or incorrect state
transition. Fix the owning layer first.
