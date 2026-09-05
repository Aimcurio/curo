# Curo Validation Scripts

This folder contains lightweight checks for the Curo package itself. These
checks do not constitute the universal Curo runtime; they verify package
integrity and catch basic drift between contracts, registry entries, and
documentation.

## Files

- [`validate_curo.py`](validate_curo.py) - dependency-free self-check.

Run from the Curo package root:

```text
python scripts/validate_curo.py
```

The script must pass before promoting a Curo package revision. Project-specific
projects still need their own validators for domain behavior, permissions,
tools, hooks, MCP servers, and runtime execution.
