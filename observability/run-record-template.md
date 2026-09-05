# Curo Governed Run Record

> Human-readable derived record only. It does not create authority or replace machine evidence.

## Run Identity

- Run ID: `<run_id>`
- Date/time: `<ISO-8601 timestamp with timezone>`
- Project: `<project_id>`
- Workflow: `<workflow_id>`
- Governed role: `<role>`
- Preferred component: `<component | NONE>`
- Required component: `<component | NONE>`
- Actual component: `<exact observed identity | UNKNOWN>`
- Fallback allowed: `[YES | NO | UNKNOWN]`
- Fallback used: `[YES | NO | UNKNOWN]`
- Fallback reason: `<reason | NONE | UNKNOWN>`
- Provenance source: `<HARNESS_API | HARNESS_CLI | UI_OBSERVATION | MODEL_SELF_REPORT | UNAVAILABLE>`

## Purpose

`<why this run exists>`

## Task

`<what this run attempted>`

## Assignment

`<who or what was responsible>`

## Progress

`<observed progress only>`

## Cutoffs

`<active gates, restrictions, or NONE>`

## Updates

`<material changes observed during the run>`

## Changes

`<files, artifacts, or state changed, or NONE>`

## Current Task

Exactly one immediate current task:

`<current task | NONE>`

## Run Result

- Status: `<governed status vocabulary>`
- Machine evidence locator(s): `<absolute path, relative path, run ID, manifest, commit, or NONE_WITH_REASON>`
- Evidence manifest/hash: `<locator and SHA-256, or NONE_WITH_REASON>`
- Files changed: `<path | NONE>`
- Blockers: `<blocker or NONE>`
- Status transition authorized: `[YES | NO]`
- Authorizing evidence / decision: `<locator | NONE>`

## Next Authorized Action

`<one next action | NONE>`

## Notes

Preserve prior failures, blockers, reversals, and unknowns. If the authoritative
result cannot be established, use `BLOCKED` or `UNKNOWN` rather than inventing
completion.
