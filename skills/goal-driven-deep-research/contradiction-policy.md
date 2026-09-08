# Goal-Driven Deep Research Contradiction Policy

## Purpose

Require active search for evidence that could weaken, falsify, or materially alter preferred conclusions.

## Rules

- For each material finding, ask what evidence would make it false, incomplete, or misleading.
- Search for contrary primary sources or credible competing interpretations when feasible.
- Do not dismiss criticism because it conflicts with the preferred architecture or expected outcome.
- Distinguish true contradiction from differences in scope, date, version, methodology, or terminology.
- Record unresolved contradictions explicitly.
- If contradictions affect the decision materially, the goal cannot be marked decision-ready until they are resolved or surfaced as accepted uncertainty.

## Contradiction record

Each contradiction should contain:

- contradiction_id
- affected_finding_ids
- description
- evidence_for
- evidence_against
- likely_cause
- materiality: `LOW | MEDIUM | HIGH`
- resolution_status: `OPEN | EXPLAINED | RESOLVED | ACCEPTED_UNCERTAINTY`
- resolution_notes
