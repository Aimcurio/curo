# Adapters

This folder defines the boundary between the model-agnostic workflow and a specific provider, model, API, or agent runtime.

## Files

- [`adapter-contract.md`](adapter-contract.md) - required adapter behavior and portability boundary.

## Ownership

Adapters translate requests and responses. They do not own policy, authoritative state, validation results, provenance, or replay decisions. Provider-specific details must remain behind this boundary.
