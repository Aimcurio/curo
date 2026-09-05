# Core Policies

This folder contains the governing rules that apply across every adapter, harness, record, and replay operation.

## Files

- [`ownership.md`](ownership.md) - authoritative owner for each system property.
- [`precedence.md`](precedence.md) - conflict-resolution hierarchy.
- [`validation.md`](validation.md) - deterministic validation and promotion order.

## Change rule

Policy changes alter system behavior and must be reflected in the canonical standard, reviewed for conflicts, and recorded in the registry or version metadata when applicable. The harness is responsible for enforcing these policies.
