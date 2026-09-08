# Historical agent execution evidence

This directory is the tracked index for agent-produced historical evidence.
The raw reports, briefs, handoffs, progress notes, and verification utilities
remain in the protected local Curo checkout and are intentionally not required
for a clean checkout to validate.

The raw files are historical execution evidence. They are not automatically
current architecture documentation. Assertions about earlier runner behavior,
test counts, schema behavior, status, or replay shape remain observations of
the snapshots in which they were recorded and must not be silently rewritten.

[`evidence-manifest.json`](evidence-manifest.json) records the count, byte size,
and aggregate SHA-256 inventory digest of the protected raw files. The
repository validator checks the manifest in every checkout and, when the raw
files are locally present, verifies them against that digest.

For current state, check:

1. [`../ARCHITECTURE.md`](../ARCHITECTURE.md)
2. [`../schemas/`](../schemas/README.md)
3. [`../harness/harness-contract.md`](../harness/harness-contract.md) and current runtime code
4. [`../CHANGE-MAP.md`](../CHANGE-MAP.md)
5. [`../REGRESSION-EVIDENCE.md`](../REGRESSION-EVIDENCE.md)
6. [`../registry/registry.yaml`](../registry/registry.yaml)

The pre-remediation architecture report is preserved separately at
[`../docs/audits/2026-09-07-pre-remediation-architecture.md`](../docs/audits/2026-09-07-pre-remediation-architecture.md)
with its recorded SHA-256. Deleting or publishing the protected raw evidence
requires a separate governed retention and privacy decision.
