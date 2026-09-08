"""Project-profile loading, hashing, and semantic validation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Union

from .core import sha256_bytes
from .approvals import validate_approval_reference
from .security import redact_secrets
from .validator import validate_curo_payload


PROFILE_SCHEMA = "project-profile"
_UNRESOLVED_DECISION_STATES = {"OPEN", "DECISION_REQUIRED"}
_APPROVED_PROFILE_STATES = {"APPROVED", "ACTIVE"}
_SECRET_FIELD_RE = re.compile(
    r"(?:^|_)(?:api_?key|access_?token|refresh_?token|password|passwd|private_?key|"
    r"client_?secret|secret_?value|credential_?name|credential_?value|credentials?)(?:$|_)",
    re.IGNORECASE,
)
_SECRET_VALUE_RE = re.compile(
    r"(?:\bsk-(?:proj-)?[A-Za-z0-9_-]{8,}\b|\bgh[pousr]_[A-Za-z0-9_]{8,}\b|"
    r"\bAKIA[0-9A-Z]{12,}\b|-----BEGIN [^-]*PRIVATE KEY-----|"
    r"(?i:\b(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*[:=]\s*\S+))"
)
_UNRESOLVED_PLACEHOLDERS = {"REQUIRED", "REQUIRED_PROJECT_ROOT", "DECISION_REQUIRED"}


class ProjectContractError(ValueError):
    """Raised when a project artifact cannot be safely loaded or compiled."""

    def __init__(self, issues: List[Dict[str, str]]):
        self.issues = issues
        super().__init__("; ".join(item["message"] for item in issues))


def issue(code: str, path: str, message: str) -> Dict[str, str]:
    """Create one stable machine-readable validation issue."""
    clean, _ = redact_secrets(message)
    return {"code": code, "path": path, "message": clean}


def _schema_issues(errors: Iterable[str]) -> List[Dict[str, str]]:
    return [issue("SCHEMA_VALIDATION_ERROR", "$", error) for error in errors]


def load_structured_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load JSON with stdlib, or YAML with optional PyYAML and an explicit failure.

    JSON remains dependency-free even when it is stored with a YAML extension,
    because JSON is a YAML-compatible serialization.
    """
    path = Path(file_path)
    try:
        text = path.read_text(encoding="utf-8-sig")
    except Exception as exc:
        raise ProjectContractError([issue("READ_ERROR", "$", f"Unable to read {path}: {exc}")]) from exc

    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ProjectContractError([
                issue(
                    "YAML_PARSER_UNAVAILABLE",
                    "$",
                    "This profile is YAML. Install optional PyYAML, or provide the profile as JSON "
                    "(JSON remains dependency-free and may use a .yaml filename).",
                )
            ]) from exc
        try:
            value = yaml.safe_load(text)
        except Exception as exc:
            raise ProjectContractError([issue("PARSE_ERROR", "$", f"Unable to parse {path}: {exc}")]) from exc

    if not isinstance(value, dict):
        raise ProjectContractError([issue("DOCUMENT_TYPE_ERROR", "$", "Document root must be an object")])
    return value


def canonical_profile_bytes(profile: Mapping[str, Any]) -> bytes:
    """Return the canonical UTF-8 representation used for profile linkage."""
    try:
        normalized = json.loads(json.dumps(profile, ensure_ascii=False, allow_nan=False))
        # Approval evidence is metadata about authorization, not material
        # project intent. Normalizing it to null avoids a circular hash where
        # the approval record must itself name the approved profile hash.
        provenance = normalized.get("provenance")
        if isinstance(provenance, dict):
            provenance["approval_ref"] = None
        return json.dumps(
            normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ProjectContractError([issue("CANONICALIZATION_ERROR", "$", str(exc))]) from exc


def canonical_profile_hash(profile_or_path: Union[Mapping[str, Any], str, Path]) -> str:
    """Hash a parsed profile, independent of YAML formatting and map order."""
    profile = (
        load_structured_file(profile_or_path)
        if isinstance(profile_or_path, (str, Path))
        else dict(profile_or_path)
    )
    return f"sha256:{sha256_bytes(canonical_profile_bytes(profile))}"


def find_plaintext_credentials(value: Any, path: str = "$") -> List[Dict[str, str]]:
    """Reject plaintext credential-shaped fields and common secret values."""
    findings: List[Dict[str, str]] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            item_path = f"{path}.{key}"
            # These are the only credential metadata names admitted by the schema.
            if key not in {"credential_requirements", "credential_id", "secret_source"} and _SECRET_FIELD_RE.search(str(key)):
                findings.append(issue("PLAINTEXT_CREDENTIAL_FIELD", item_path, "Credential value fields are prohibited"))
            findings.extend(find_plaintext_credentials(item, item_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(find_plaintext_credentials(item, f"{path}[{index}]"))
    elif isinstance(value, str) and _SECRET_VALUE_RE.search(value):
        findings.append(issue("PLAINTEXT_CREDENTIAL_VALUE", path, "A plaintext credential-like value is prohibited"))
    return findings


def _duplicate_id_issues(profile: Mapping[str, Any]) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    collections = (
        ("components", "component_id"),
        ("operators", "operator_id"),
        ("approval_boundaries", "action"),
        ("required_validators", "validator_id"),
        ("workflow_definitions", "workflow_id"),
        ("dependencies", "dependency_id"),
        ("open_decisions", "decision_id"),
        ("known_risks", "risk_id"),
    )
    for collection, key in collections:
        seen = set()
        for index, item in enumerate(profile.get(collection, [])):
            if not isinstance(item, Mapping) or key not in item:
                continue
            identifier = item[key]
            if identifier in seen:
                issues.append(issue("DUPLICATE_ID", f"$.{collection}[{index}].{key}", f"Duplicate {key}: {identifier}"))
            seen.add(identifier)
    return issues


def _placeholder_issues(value: Any, path: str = "$") -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            findings.extend(_placeholder_issues(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(_placeholder_issues(item, f"{path}[{index}]"))
    elif isinstance(value, str) and (value in _UNRESOLVED_PLACEHOLDERS or value.startswith("REQUIRED_")):
        findings.append(issue("UNRESOLVED_REQUIRED_VALUE", path, "Approved project intent cannot contain a required-value placeholder"))
    return findings


def validate_project_profile(profile_or_path: Union[Mapping[str, Any], str, Path]) -> Dict[str, Any]:
    """Validate project-profile schema and cross-field governance rules."""
    try:
        profile = (
            load_structured_file(profile_or_path)
            if isinstance(profile_or_path, (str, Path))
            else dict(profile_or_path)
        )
    except ProjectContractError as exc:
        return {"valid": False, "errors": exc.issues, "profile": None}

    valid, errors = validate_curo_payload(profile, PROFILE_SCHEMA)
    findings = _schema_issues(errors)
    findings.extend(find_plaintext_credentials(profile))
    findings.extend(_duplicate_id_issues(profile))

    profile_status = profile.get("profile_status")
    unresolved = [
        item for item in profile.get("open_decisions", [])
        if isinstance(item, Mapping) and item.get("status") in _UNRESOLVED_DECISION_STATES
    ]
    if profile_status in _APPROVED_PROFILE_STATES and unresolved:
        findings.append(issue(
            "UNRESOLVED_DECISIONS_BLOCK_APPROVAL",
            "$.open_decisions",
            "APPROVED or ACTIVE profiles cannot contain unresolved decisions",
        ))
    if profile_status in _APPROVED_PROFILE_STATES:
        findings.extend(_placeholder_issues(profile))
    approval_ref = profile.get("provenance", {}).get("approval_ref") if isinstance(profile.get("provenance"), Mapping) else None
    if profile_status in _APPROVED_PROFILE_STATES and not approval_ref:
        findings.append(issue("APPROVAL_REFERENCE_REQUIRED", "$.provenance.approval_ref", "Approved project intent requires human approval evidence"))
    elif profile_status in _APPROVED_PROFILE_STATES:
        human_operator_ids = [
            str(operator.get("operator_id"))
            for operator in profile.get("operators", [])
            if isinstance(operator, Mapping) and operator.get("operator_type") == "HUMAN"
        ]
        findings.extend(validate_approval_reference(
            approval_ref,
            project_id=str(profile.get("project_id", "")),
            profile_hash=canonical_profile_hash(profile),
            allowed_actor_ids=human_operator_ids,
        ))

    return {
        "valid": bool(valid and not findings),
        "errors": findings,
        "profile": profile,
        "profile_hash": canonical_profile_hash(profile) if valid else None,
    }
