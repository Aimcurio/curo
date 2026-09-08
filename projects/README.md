# Governed projects

This directory contains Curo's project-specific governance records. It does not
contain or replace the projects' source repositories.

Each project directory contains:

- `project.yaml`: human-readable project intent, constraints, authority, and
  unresolved decisions;
- `llm-assignments.json`: desired and resolved role assignments bound to the
  parsed project profile by a canonical SHA-256 hash;
- `README.md`: project-specific interpretation and approval notes;
- `evidence/`, when needed: preserved historical records and validated
  relocation or classification-supersession records.

The generic kickoff remains intake. A human must review and approve a specific
profile before its assignments can become approved. Preferred or resolved
provider/model values are never observed execution identity; only run and
provenance records created by the observing harness establish that truth.

The current profiles remain `DECISION_REQUIRED`. Exact KAYO, Math Node, and
unverified runtime locations and model selections are intentionally `UNKNOWN`.
