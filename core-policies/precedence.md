# Precedence Policy

## Order

1. Deterministic validator
2. Harness policy
3. Captured evidence
4. Context contract
5. Prompt instruction
6. Model judgment

Process exit state is evidence evaluated under the deterministic validator and harness policy; it never outranks them. When a runtime payload conflicts with its canonical schema, the write is blocked rather than the schema being weakened for convenience.

For project configuration, human-approved `projects/<id>/project.yaml` is the
intent authority. The compiled `llm-assignments.json` is subordinate and must
match the profile hash. Observed run/provenance evidence outranks configured or
resolved identity for claims about which provider or model actually executed.

## Conflict rule

When higher and lower precedence sources disagree, keep the higher-precedence source authoritative and mark the lower source as superseded or disputed.

## Notes

- Do not collapse conflict handling into an all-or-nothing block.
- Route by severity and owner.
- Preserve the conflicting evidence for review.
