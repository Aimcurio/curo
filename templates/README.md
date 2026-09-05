# Project Templates

This folder contains reusable starting points for applying Curo to a new
AI-assisted project.

## Files

- [`project-kickoff.md`](project-kickoff.md) - copy-and-fill human kickoff brief.
- [`project-kickoff.yaml`](project-kickoff.yaml) - machine-readable equivalent.

Use the Markdown template when communicating with a builder or reviewer. Use
the YAML template when the brief will be loaded by a harness, project tool, or
evaluation pipeline. Keep both forms aligned when the project is initialized.

The machine template has one authoritative `status` field. Use `DRAFT`,
`READY_FOR_DESIGN`, or `BLOCKED`; do not maintain a second status field.

The execution profile distinguishes deterministic projects, AI-assisted
projects, and hybrid projects. The workflow-capability fields cover interactive
interfaces, batch jobs, device workflows, audits, and other execution shapes.
Provider fields are not applicable to every project; use `NOT_APPLICABLE` when
no model is involved.

## Required before implementation

The requester must provide or explicitly accept defaults for the objective,
Version 1 scope, target environment, data constraints, provider direction, and
acceptance criteria. Missing information should be marked `UNKNOWN` or
`DECISION_REQUIRED`, not silently invented.
