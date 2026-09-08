# Goal-Driven Deep Research Evidence Policy

## Evidence classes

Research outputs must distinguish:

- `EVIDENCE` — directly supported by retrieved material.
- `INFERENCE` — reasoned conclusion drawn from evidence.
- `RECOMMENDATION` — proposed action or preference.
- `UNKNOWN` — unresolved information gap.

## Rules

- Never label inference as evidence.
- Preserve uncertainty when evidence is incomplete or conflicting.
- Record which evidence supports or challenges each finding.
- Confidence describes the researcher's assessment; it does not upgrade an inference into fact.
- Tool execution or source retrieval is telemetry, not proof by itself.
- A finding with no evidence references must not be marked `SUPPORTED`.
- Contradictory evidence must remain linked to the affected finding.
- Downstream models must be able to recover the basis of each material conclusion.

## Finding statuses

Allowed values:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `CHALLENGED`
- `CONTRADICTED`
- `INSUFFICIENT_EVIDENCE`
- `UNKNOWN`

## Confidence

Allowed values:

- `HIGH`
- `MEDIUM`
- `LOW`

Confidence and status are separate fields.
