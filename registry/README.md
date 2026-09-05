# Registry

This folder provides the machine-readable inventory of canonical artifacts, their paths, versions, ownership, and source pointers. Navigation-only READMEs are intentionally not registry artifacts; the registry is reserved for governed content and executable checks.

Every governed entry must include a `source` pointer. The pointer may identify
the originating conversation, a governing artifact, or a review decision. It
must be explicit enough that provenance does not depend on inference.

## Files

- [`registry.yaml`](registry.yaml) - canonical artifact registry.

## Change rule

Every canonical artifact must have one registry entry with an exact relative path and owner. Registry entries are metadata about artifacts; they do not replace the artifacts or their validators.
