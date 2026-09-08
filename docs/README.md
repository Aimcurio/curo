# Documentation

This folder contains the narrative source of truth for the operating standard and its accepted amendments.

## Files

- [`INDEX.md`](INDEX.md) - navigation, reading paths, and folder ownership map.
- [`beginner-guide.md`](beginner-guide.md) - plain-language introduction, use cases, first-time setup, and practical workflows.
- [`operating-standard.md`](operating-standard.md) - canonical integrated standard.
- [`addendum-a.md`](addendum-a.md) - amendment history and refinements.
- [`addendum-b-protocol-integrity.md`](addendum-b-protocol-integrity.md) - executable protocol-integrity rules and residual limitations.
- [`gaps-and-roadmap.md`](gaps-and-roadmap.md) - maturity boundary and planned extensions.
- [`audits/2026-09-07-pre-remediation-architecture.md`](audits/2026-09-07-pre-remediation-architecture.md) - byte-preserved historical architecture audit.
- [`audits/2026-09-07-pre-remediation-architecture.sha256`](audits/2026-09-07-pre-remediation-architecture.sha256) - preservation digest.

The standard explains what the system must mean. Its Applied reasoning patterns
section shows how to move from a situation to ownership, implementation order,
validation, and a failure boundary. The implementation folders explain how
those requirements are represented, enforced, and replayed.

Current architecture is described by [`../ARCHITECTURE.md`](../ARCHITECTURE.md).
The audit under `audits/` and reports under [`evidence/historical-agent-runs/`](../evidence/historical-agent-runs/README.md)
remain historical observations; they must not be read as current contracts
without checking current schemas, code, change maps, and regression evidence.

## Ownership

Human or authorized callers own objectives and policy decisions. The harness owns enforcement facts, evidence persistence, and replay state. Models may propose content but cannot authoritatively establish externally verifiable facts.
