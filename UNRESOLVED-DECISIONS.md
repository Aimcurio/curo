# Unresolved Decisions

Status: REQUESTER_APPROVAL_REQUIRED

## DEC-PI-001 — Release version

The remediation changes public artifact contracts: the old replay schema/template is replaced by two classes, canonical execution changes from a shell string to executable plus argv, run `SUCCESS` becomes evidence-backed `PASS`, and learning payload fields are aligned to the canonical schema. The legacy command input remains as a restricted compatibility path, but persisted contracts are not backward-compatible.

Recommendation: **MAJOR**. If Curo's documented version is treated as the public contract version, use `2.0.0`; align the harness package version under the same release decision. No version file has been changed.

## DEC-PI-002 — Existing PDF learning candidate migration

The pre-existing user-owned `learning/candidates/LEARN-20260907-PDF-RESTORATION.yaml` uses `candidate_type: skill_and_anti_pattern_distillation`, which is outside the five canonical types. Rewriting it would conflict with the instruction not to rewrite historical evidence in place.

Recommendation: preserve it as historical input and create one or more superseding candidates using `skill` and `anti_pattern` after human approval. Until then, it is not schema-valid under the new canonical candidate contract.

## DEC-PI-003 — Legacy command-string removal window

The runtime still accepts a deprecated simple command string after rejecting shell operators and converting it to executable plus argv. This eases migration but retains a compatibility surface.

Recommendation: announce removal for the next major release after consumers migrate to `--executable` and repeated `--arg` values.

## DEC-PI-004 — Stronger Windows containment

The zero-mandatory-dependency implementation uses a new process group plus Windows `taskkill /T /F`. Tests verify that a spawned child does not survive a timeout. If `taskkill` cannot confirm termination, the record explicitly says so; the direct child is killed as a fallback, but descendant termination is not claimed.

Recommendation: accept this bounded native strategy for the local-first runtime. Evaluate Job Objects only if a later Windows deployment contract requires a stronger guarantee.

## DEC-PI-005 — Stale lock recovery policy

Per-target lock files are bounded and cross-platform, but a host crash can leave a stale lock that requires operator removal. Automatic age-based lock breaking can violate active-writer safety.

Recommendation: retain explicit timeout/failure behavior for this release and document an operator recovery procedure before adding automated stale-lock handling.
