# Historical agent execution evidence

This directory is the tracked index for agent-produced historical evidence.
The raw reports, briefs, handoffs, progress notes, and verification utilities
remain protected local files and are intentionally not required for a clean
checkout to validate.

The raw files were originally recorded under the legacy `.agents/` path. They
are historical execution evidence, not current agent definitions or current
architecture documentation. Assertions about earlier runner behavior, test
counts, schema behavior, status, or replay shape remain observations of the
snapshots in which they were recorded and must not be silently rewritten.

[`evidence-manifest.json`](evidence-manifest.json) records the count, byte size,
legacy digest, and destination-path digest of the protected raw files. The
repository validator checks the manifest in every checkout and, when the raw
files are locally present here, verifies them against the destination digest.

For current state, check:

1. [`../../ARCHITECTURE.md`](../../ARCHITECTURE.md)
2. [`../../schemas/`](../../schemas/README.md)
3. [`../../harness/harness-contract.md`](../../harness/harness-contract.md) and current runtime code
4. [`../../CHANGE-MAP.md`](../../CHANGE-MAP.md)
5. [`../../REGRESSION-EVIDENCE.md`](../../REGRESSION-EVIDENCE.md)
6. [`../../registry/registry.yaml`](../../registry/registry.yaml)

The pre-remediation architecture report is preserved separately at
[`../../docs/audits/2026-09-07-pre-remediation-architecture.md`](../../docs/audits/2026-09-07-pre-remediation-architecture.md)
with its recorded SHA-256. References to `.agents/` in preserved audits and
review records describe the evidence's original location and are intentionally
not rewritten. Deleting or publishing the protected raw evidence requires a
separate governed retention and privacy decision.
