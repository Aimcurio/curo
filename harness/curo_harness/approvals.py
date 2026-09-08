"""Validation of harness-recorded human approval evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional

from .core import get_curo_root, resolve_within, safe_read_json, sha256_file
from .security import redact_secrets
from .validator import validate_curo_payload


def _issue(code: str, path: str, message: str) -> Dict[str, str]:
    clean, _ = redact_secrets(message)
    return {"code": code, "path": path, "message": clean}


def validate_approval_reference(
    reference: Any,
    *,
    project_id: str,
    profile_hash: str,
    expected_actor: Optional[Mapping[str, Any]] = None,
    allowed_actor_ids: Optional[Iterable[str]] = None,
    assignment_ids: Optional[Iterable[str]] = None,
) -> list[Dict[str, str]]:
    """Validate a contained, hash-bound, schema-valid human approval record."""
    if not isinstance(reference, Mapping):
        return [_issue("APPROVAL_EVIDENCE_REQUIRED", "$.approval_ref", "Approval requires a structured evidence reference")]
    try:
        artifact_path = resolve_within(get_curo_root(), str(reference.get("artifact_path", "")))
    except ValueError:
        return [_issue("APPROVAL_EVIDENCE_PATH_UNAUTHORIZED", "$.approval_ref.artifact_path", "Approval evidence escapes the Curo workspace")]
    if not artifact_path.is_file():
        return [_issue("APPROVAL_EVIDENCE_MISSING", "$.approval_ref.artifact_path", "Approval evidence file does not exist")]
    if sha256_file(artifact_path) != reference.get("artifact_sha256"):
        return [_issue("APPROVAL_EVIDENCE_HASH_MISMATCH", "$.approval_ref.artifact_sha256", "Approval evidence hash does not match")]
    try:
        record = safe_read_json(artifact_path)
    except Exception:
        return [_issue("APPROVAL_EVIDENCE_INVALID", "$.approval_ref.artifact_path", "Approval evidence is not valid JSON")]
    valid, schema_errors = validate_curo_payload(record, "human-approval-record")
    findings = [
        _issue("APPROVAL_EVIDENCE_INVALID", "$.approval_ref.artifact_path", error)
        for error in schema_errors
    ]
    if not valid:
        return findings
    comparisons = (
        (record.get("approval_id") == reference.get("approval_id"), "APPROVAL_ID_MISMATCH", "Approval ID does not match the reference"),
        (record.get("project_id") == project_id, "APPROVAL_PROJECT_MISMATCH", "Approval project does not match"),
        (record.get("approved_profile_hash") == profile_hash, "APPROVAL_PROFILE_HASH_MISMATCH", "Approval does not cover the current profile hash"),
        (record.get("recorded_by") == "harness", "APPROVAL_RECORDER_INVALID", "Approval must be recorded by the harness"),
    )
    for condition, code, message in comparisons:
        if not condition:
            findings.append(_issue(code, "$.approval_ref", message))
    actor = record.get("actor")
    if expected_actor is not None and actor != dict(expected_actor):
        findings.append(_issue("APPROVAL_ACTOR_MISMATCH", "$.approval_ref", "Approval record actor does not match the declared actor"))
    if allowed_actor_ids is not None:
        allowed = set(allowed_actor_ids)
        actor_id = actor.get("actor_id") if isinstance(actor, Mapping) else None
        if actor_id not in allowed:
            findings.append(_issue(
                "APPROVAL_ACTOR_UNAUTHORIZED",
                "$.approval_ref",
                "Approval record actor is not a declared HUMAN project operator",
            ))
    if assignment_ids is not None and set(record.get("approved_assignment_ids", [])) != set(assignment_ids):
        findings.append(_issue("APPROVAL_ASSIGNMENTS_MISMATCH", "$.approval_ref", "Approval record does not cover exactly these assignments"))
    return findings
