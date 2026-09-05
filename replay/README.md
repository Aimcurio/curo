# Replay

This folder contains the inputs needed to rerun or independently verify an execution without treating the original model response as proof of completion.

## Files

- [`replay-manifest-template.yaml`](replay-manifest-template.yaml) - starting point for a replay manifest.

## Ownership

The harness creates and updates replay manifests from the actual artifact versions, inputs, environment, tool events, and validation outcomes. A replay is complete only when its deterministic checks and evidence links pass.
