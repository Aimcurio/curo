# Replay

This folder contains two deliberately separate manifest classes. Neither treats a model response or a successful process exit as proof of validation.

## Files

- [`execution-replay-manifest-template.yaml`](execution-replay-manifest-template.yaml) - re-executes a structured executable and argv contract with `shell=False`.
- [`artifact-verification-manifest-template.yaml`](artifact-verification-manifest-template.yaml) - verifies historical artifacts, hashes, lineage, and optional schemas without executing a process.

## Ownership

The harness creates manifests from observed inputs, outputs, environment, tool events, and validation outcomes. An execution replay requires `executable`, `args`, `cwd`, and `timeout_seconds`; an artifact verification manifest must not contain those execution fields. Referenced paths must remain inside the configured workspace boundary.

A replay is complete only when its declared checks and evidence links pass. Process exit zero is only a process fact.
