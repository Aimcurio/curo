---
name: monorepo-contract-auditor
description: Multi-package monorepo architecture and boundary audit pattern for Curo projects.
---

# Monorepo Contract & Architecture Auditor Pattern

## Purpose
Performs deterministic static analysis on Curo-compliant monorepos to verify boundary contracts, unidirectional dependency rules (e.g. `AGENTS.md`), error sanitization, and test evidence.

## Audit Workflow

### 1. Workspace & Dependency Topology Mapping
- Parse `pnpm-workspace.yaml`, `package.json`, and all package-level `package.json` files.
- Map the declared dependency graph between `packages/*` and `apps/*`.
- Verify presence of all declared workspaces and identify any missing snapshot directories.

### 2. Boundary & Isolation Verification
- Parse `AGENTS.md` to extract explicit architecture isolation constraints:
  - Verify sibling package independence (e.g. sibling packages must not depend on each other).
  - Verify UI client isolation (ensure frontend apps never import backend persistence or state reducers directly).
  - Verify export map usage (ensure consumers import via package root exports, not deep-imports).

### 3. Error Sanitization & Resilience Review
- Inspect server and API route handlers for proper error handling.
- Ensure backend errors sanitize internal filepaths, database queries, and stack traces before returning responses to clients.
- Verify frontend client implementations for graceful degradation (e.g. `Promise.allSettled`, error fallback banners).

### 4. Verification Evidence & Oracle Auditing
- Inspect `evidence/verification/` run logs for pre/post cryptographic hashes.
- Verify semantic oracle coverage, test counts, and exit codes.

### 5. Validation & Observability
- Route all audit findings through Curo exception review protocol or export structured audit markdown documents.
