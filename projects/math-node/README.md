# Math Node project profile

This directory preserves the legacy Math Node `replay_manifest` bytes while
superseding only that record's classification. The old record contains artifact
digests and expected checks but no executable command, so the new governed
record is an `artifact_verification_manifest`, not an execution replay.

The byte-identical historical copy has SHA-256
`effb92008a760ae228803a427a146bec1b8cee8df1c764ac9c48f16c85b0b8c9`.
The original remains at `manifests/math-node-v0.1-replay.json`; the relocation
record uses `COPY_PRESERVE_SOURCE`. No current project root, provider, model, or
execution identity is inferred from the historical manifest.
