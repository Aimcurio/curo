# Curo Beginner Guide

This guide is for someone using Curo for the first time. You do not need to
understand AI infrastructure, JSON Schema, or agent orchestration before you
start.

## What Curo is

Curo is a small, modular, model-agnostic framework for reusable AI
capabilities. Think of Curo as a socket: projects can attach skills, agents,
models, validators, workflows, research systems, governance, observability,
and execution systems without any one of those extensions becoming Curo's
entire identity.

This repository includes working governance, project-profile, validation,
execution-harness, evidence, replay, review, learning, and goal-driven deep
research extensions. When selected, they help answer six practical questions:

1. What is the project trying to accomplish?
2. Which person, agent, model, or program is responsible for each part?
3. What information and tools may each role use?
4. What may each role change?
5. How will the result be checked?
6. What evidence proves what actually happened?

The included governed-execution pattern follows this rule:

```text
Models propose.
Harnesses enforce boundaries.
Validators check results.
Evidence records what happened.
Humans authorize consequential decisions.
```

## What Curo is not

Curo is not an AI model, chatbot, project source-code folder, or automatic
approval system. It does not build KAYO, the Second Brain, or another product
by itself. Instead, those capabilities plug into Curo as bounded extensions.
The included goal-driven deep-research extension can organize investigations,
evidence, contradictions, unknowns, and stopping decisions, but it does not
perform product implementation or turn a research report into approval.

Curo also does not prove that a model ran merely because its name appears in a
configuration file. Actual model identity remains `UNKNOWN` until trusted run
evidence establishes it.

## When to use Curo

Use Curo and select the relevant extensions when work involves one or more of
the following:

- several AI agents, models, tools, or human roles;
- private, confidential, or restricted information;
- commands that create or modify files;
- decisions that require human approval;
- a result that must be tested rather than merely accepted;
- a need to know which inputs, tools, and model produced an output;
- a workflow that may need to be replayed or audited later;
- a lesson that might become a reusable rule, skill, validator, or anti-pattern.

For casual brainstorming with no execution, sensitive data, or lasting claim,
the full governed-execution extension set may be unnecessary. Use only the
capabilities and governance that match the project and its risk.

## The main parts

### Core identity and drift check

[`../core-policies/core-identity.md`](../core-policies/core-identity.md) defines
the small, stable Curo core. [`../core-policies/drift-check.md`](../core-policies/drift-check.md)
helps decide whether a proposed capability is an ordinary extension or would
redefine the framework. New functionality should remain an extension unless a
human explicitly approves a `CORE REDEFINITION`.

### Generic kickoff

The kickoff captures the initial request. It is intentionally short and does
not contain the project's complete operating contract.

Start with [`../templates/project-kickoff.md`](../templates/project-kickoff.md).

### Project profile

The project profile is the human-readable source of project intent. It records
the project's purpose, roots, components, constraints, data classification,
authority, validation requirements, risks, and unresolved decisions.

Each governed project has:

```text
projects/<project-id>/project.yaml
```

Use [`../templates/project-profile.yaml`](../templates/project-profile.yaml) as
the starting template.

### Assignment manifest

The assignment manifest describes the roles that will do the work. It can
assign model-assisted, deterministic, and human roles while limiting their
tools, context, writes, fallbacks, and authority.

Each governed project has:

```text
projects/<project-id>/llm-assignments.json
```

The assignment file is linked to the project profile by a cryptographic hash.
A material profile change makes the previous assignment approval stale.

### Skills

Files under [`../skills/`](../skills/) are reusable playbooks. A skill explains
how to perform a particular kind of work; it does not grant permission or prove
successful execution. Project and assignment rules still decide whether an
agent may use it, and validators still check the result.

A learning candidate with `candidate_type: skill` is only a proposal. It does
not become an active skill until it passes validation and human-governed
promotion.

### Harness extension

The included harness is an optional enforcement extension. When selected, it
runs structured commands, checks path boundaries, redacts common credential
patterns, validates records before writing them, and produces evidence.

### Validators

Validators determine whether testable claims pass or fail. A process finishing
successfully is not enough: required inputs, outputs, schemas, and project
checks must also pass.

### Evidence and observability

Run records, provenance records, and evidence files describe what was actually
observed. Missing evidence must remain `UNKNOWN`; a model's statement about its
own execution is not sufficient proof.

### Human approval

Humans approve consequential choices such as project intent, agent authority,
writable locations, provider/model selection, and promotion. An approved
profile or assignment set requires a contained, hash-bound approval record.
Models cannot approve their own assignments.

## One governed project workflow

```text
1. Complete the generic kickoff.
2. Create a project-specific profile.
3. Leave unknown facts and open decisions explicit.
4. Validate the profile.
5. Have an authorized human review and approve it.
6. Define the project roles and assignment input.
7. Compile and validate the assignment manifest.
8. Authorize a bounded implementation task.
9. Run work through the selected harness where evidence is required.
10. Validate the result.
11. Review exceptions and human decisions.
12. Preserve evidence and propose reusable lessons when justified.
```

Do not combine planning and implementation authorization silently. A proposed
plan remains a proposal until the required review and approval occur.

## First-time setup check

Open PowerShell in `E:\curo`, then run:

```powershell
python curo.py doctor
python scripts/validate_curo.py
python -m unittest discover -s tests -v
```

Expected outcomes are a successful doctor check, a repository validation
`PASS`, and an `OK` test result. If a command fails, read the reported error
instead of assuming the installation is ready.

To see all commands:

```powershell
python curo.py --help
python curo.py project --help
```

## Starting a project

### 1. Complete intake

Copy and fill in the generic kickoff:

```powershell
Copy-Item templates\project-kickoff.md projects\my-project-kickoff.md
```

Replace `my-project` with a stable lowercase project ID. Record missing facts
as unknown or decisions required; do not invent paths, providers, models, or
approvals.

### 2. Create the project folder and profile

```powershell
New-Item -ItemType Directory -Path projects\my-project
Copy-Item templates\project-profile.yaml projects\my-project\project.yaml
```

Edit the copied profile so that its `project_id` matches the folder name. Keep
the profile in `DRAFT` or `DECISION_REQUIRED` while consequential facts remain
unresolved.

The `projects/` folder holds Curo's project contracts and preserved evidence.
It is not a replacement for the project's source-code repository.

### 3. Validate the profile

```powershell
python curo.py project validate projects\my-project\project.yaml
```

A zero exit code and a valid machine-readable result mean the profile satisfies
the current contract. This does not supply missing human approval.

### 4. Prepare assignments

```powershell
Copy-Item templates\llm-assignments.json projects\my-project\assignment-input.json
```

Edit each role's purpose, capabilities, tools, context, allowed roots,
validators, fallbacks, evidence, and escalation conditions. Keep actual
provider/model identity `UNKNOWN` unless trusted observation establishes it.

### 5. Review and approve

An authorized human must resolve consequential decisions and provide a valid
approval record before an `APPROVED` profile can be compiled. Curo currently
validates approval records but does not provide a general-purpose `approve`
CLI command. Use the approved harness or organizational approval channel that
owns this decision; do not create a label that merely says "approved."

### 6. Compile the assignment manifest

After valid approval evidence exists:

```powershell
python curo.py project compile projects\my-project\project.yaml `
  --assignments projects\my-project\assignment-input.json `
  --reference-time 2026-09-08T12:00:00Z `
  --output projects\my-project\llm-assignments.json
```

The reference time is explicit so identical inputs produce byte-equivalent
output. Use the real authorized timestamp; the example is only a format.

### 7. Verify profile-to-assignment linkage

```powershell
python curo.py project verify-assignments projects\my-project\llm-assignments.json
```

Run this again after changing the project profile. If the profile changed
materially, review and approval must be renewed rather than bypassed.

## Running a bounded command with evidence

Use a structured executable and repeated arguments rather than a shell command
string. For example:

```powershell
python curo.py run --id RUN-001 --executable python --arg=--version `
  --evidence-dir evidence
```

For real work, declare important input and output files with `--input` and
`--output`. Keep the executable, files, and evidence directory within the
authorized workspace boundaries.

Use `python curo.py run --help` before running a consequential command. Curo
does not turn an unsafe or unauthorized operation into a safe one merely by
recording it.

## Replay, exception review, and learning

Use replay when a schema-valid execution replay manifest already exists:

```powershell
python curo.py replay path\to\execution-replay-manifest.json
```

Use escalation when work needs evidence or a human decision:

```powershell
python curo.py escalate --id HITL-001 --project my-project `
  --finding "Writable project root requires approval" --class human_decision
```

Use distillation only to propose a reusable lesson from an observed run:

```powershell
python curo.py distill --id LC-001 --run-id RUN-001 `
  --title "Reusable validation procedure" --type skill
```

Distillation creates a candidate. It does not automatically change canonical
policy or install a skill.

## How to read Curo statuses

- `DRAFT` or `PROPOSED`: prepared for review, not authorized.
- `DECISION_REQUIRED`: a person must resolve one or more choices.
- `APPROVED`: valid approval evidence exists for this exact content.
- `RESOLVED`: a runtime choice has been selected; it is not yet observed truth.
- `VERIFIED`: the required evidence and validation establish the claim.
- `UNKNOWN`: evidence is missing or insufficient.
- `BLOCKED`: a required step cannot safely continue.
- `FAIL`: an executed check established failure.

Do not translate `UNKNOWN` into success, and do not treat `COMPLETE` as proof
that validation passed.

## Common beginner mistakes

- Putting project source code inside `projects/` instead of storing only Curo
  contracts and preserved evidence there.
- Treating the generic kickoff as the finished project definition.
- Copying a preferred model name into observed identity.
- Marking work approved without valid human approval evidence.
- Allowing a model to approve its own role or output.
- Storing API keys or tokens in profiles, assignments, logs, or evidence.
- Expanding a fallback's permissions beyond the primary assignment.
- Editing historical evidence to make an old report look current.
- Calling a completed process verified before validators check the result.
- Promoting a learning candidate directly into a skill or policy.

## Where to look next

- [`../core-policies/core-identity.md`](../core-policies/core-identity.md)
  explains what is and is not Curo core.
- [`INDEX.md`](INDEX.md) provides reading paths for each Curo subsystem.
- [`../projects/README.md`](../projects/README.md) explains project folder rules
  and links to the KAYO, Spacetime, and Math Node examples.
- [`operating-standard.md`](operating-standard.md) contains the complete
  governance model.
- [`../harness/harness-contract.md`](../harness/harness-contract.md) describes
  exact enforcement behavior.
- [`../observability/observability-contract.md`](../observability/observability-contract.md)
  explains observed truth and evidence.
- [`../review/exception-review-protocol.md`](../review/exception-review-protocol.md)
  explains exception handling and human escalation.
- [`../learning/learning-distillation-protocol.md`](../learning/learning-distillation-protocol.md)
  explains how lessons become governed candidates and, after approval, promoted
  artifacts.

When uncertain, stop at the earliest safe boundary, preserve the evidence, and
ask the person who owns the decision.
