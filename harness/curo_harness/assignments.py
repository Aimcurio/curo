"""Deterministic materialization and verification of project assignments."""

from __future__ import annotations

import copy
import datetime
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

from .core import get_curo_root, resolve_within, safe_read_json, sha256_file
from .approvals import validate_approval_reference
from .projects import (
    ProjectContractError,
    canonical_profile_hash,
    find_plaintext_credentials,
    issue,
    load_structured_file,
    validate_project_profile,
)
from .validator import validate_and_write_json, validate_curo_payload


ASSIGNMENT_SCHEMA = "llm-assignments"
_APPROVED_ASSIGNMENT_DOC_STATES = {"APPROVED"}
_APPROVED_ASSIGNMENT_STATES = {"APPROVED", "RESOLVED"}
_CLASSIFICATIONS = {"PUBLIC": 0, "INTERNAL": 1, "CONFIDENTIAL": 2, "RESTRICTED": 3}
_WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")


def _schema_issues(errors: List[str]) -> List[Dict[str, str]]:
    return [issue("SCHEMA_VALIDATION_ERROR", "$", error) for error in errors]


def _normalized_path(value: str) -> str:
    candidate = Path(value)
    if not candidate.is_absolute() and not _WINDOWS_ABSOLUTE.match(value):
        candidate = get_curo_root() / candidate
    return os.path.normcase(os.path.normpath(os.path.realpath(str(candidate.absolute()))))


def _is_within(candidate: str, boundary: str) -> bool:
    child = _normalized_path(candidate)
    parent = _normalized_path(boundary)
    try:
        return os.path.commonpath([child, parent]) == parent
    except ValueError:
        return False


def _authorized_by(candidate: str, boundaries: List[str]) -> bool:
    return any(_is_within(candidate, boundary) for boundary in boundaries)


def _profile_semantic_issues(assignments: Mapping[str, Any], profile: Mapping[str, Any]) -> List[Dict[str, str]]:
    findings: List[Dict[str, str]] = []
    if assignments.get("project_id") != profile.get("project_id"):
        findings.append(issue("PROJECT_ID_MISMATCH", "$.project_id", "Assignment project_id does not match the source profile"))

    actual_roots = [str(item) for item in profile.get("actual_project_roots", [])]
    for index, assignment in enumerate(assignments.get("assignments", [])):
        if not isinstance(assignment, Mapping):
            continue
        allowed = [str(item) for item in assignment.get("allowed_project_roots", [])]
        writes = [str(item) for item in assignment.get("allowed_write_roots", [])]
        for root_index, root in enumerate(allowed):
            if not _authorized_by(root, actual_roots):
                findings.append(issue(
                    "UNAUTHORIZED_PROJECT_ROOT",
                    f"$.assignments[{index}].allowed_project_roots[{root_index}]",
                    f"Project root is outside source-profile authority: {root}",
                ))
        for root_index, root in enumerate(writes):
            if not _authorized_by(root, allowed) or not _authorized_by(root, actual_roots):
                findings.append(issue(
                    "UNAUTHORIZED_WRITE_ROOT",
                    f"$.assignments[{index}].allowed_write_roots[{root_index}]",
                    f"Write root is outside assignment authority: {root}",
                ))
    return findings


def _assignment_semantic_issues(document: Mapping[str, Any]) -> List[Dict[str, str]]:
    findings = find_plaintext_credentials(document)
    assignment_ids = set()
    role_ids = set()
    for index, assignment in enumerate(document.get("assignments", [])):
        if not isinstance(assignment, Mapping):
            continue
        base = f"$.assignments[{index}]"
        assignment_id = assignment.get("assignment_id")
        role_id = assignment.get("role_id")
        if assignment_id in assignment_ids:
            findings.append(issue("DUPLICATE_ASSIGNMENT_ID", f"{base}.assignment_id", f"Duplicate assignment_id: {assignment_id}"))
        if role_id in role_ids:
            findings.append(issue("DUPLICATE_ROLE_ID", f"{base}.role_id", f"Duplicate role_id: {role_id}"))
        assignment_ids.add(assignment_id)
        role_ids.add(role_id)

        authority = assignment.get("authority_scope", {})
        if assignment.get("role_type") != "HUMAN" and authority.get("may_approve") is True:
            code = "MODEL_APPROVAL_PROHIBITED" if assignment.get("role_type") == "MODEL" else "NON_HUMAN_APPROVAL_PROHIBITED"
            findings.append(issue(code, f"{base}.authority_scope.may_approve", "Only a human role may approve assignments"))
        reviewers = assignment.get("review_requirements", {}).get("reviewer_role_ids", [])
        if role_id in reviewers:
            findings.append(issue("SELF_REVIEW_PROHIBITED", f"{base}.review_requirements.reviewer_role_ids", "An assignment cannot name its own role as reviewer"))

        state = assignment.get("resolved_identity_state")
        provider = assignment.get("resolved_provider")
        model = assignment.get("resolved_model")
        if state == "RESOLVED" and (not provider or not model or provider == "UNKNOWN" or model == "UNKNOWN"):
            findings.append(issue("RESOLVED_IDENTITY_INCOMPLETE", f"{base}.resolved_identity_state", "RESOLVED requires non-UNKNOWN resolved provider and model"))
        if state != "RESOLVED" and (provider is not None or model is not None):
            findings.append(issue("UNRESOLVED_IDENTITY_HAS_VALUE", f"{base}.resolved_identity_state", "Only RESOLVED identity may contain resolved provider or model"))
        if assignment.get("assignment_status") == "RESOLVED" and state != "RESOLVED":
            findings.append(issue("RESOLVED_STATUS_IDENTITY_MISMATCH", f"{base}.assignment_status", "RESOLVED assignment status requires RESOLVED identity"))
        if state == "RESOLVED" and assignment.get("assignment_status") != "RESOLVED":
            findings.append(issue("RESOLVED_IDENTITY_STATUS_MISMATCH", f"{base}.resolved_identity_state", "RESOLVED identity requires RESOLVED assignment status"))
        if any(str(key).startswith("observed_") for key in assignment):
            findings.append(issue("OBSERVED_IDENTITY_PROHIBITED", base, "Observed identity belongs only in run and provenance evidence"))

        required_capabilities = set(assignment.get("required_capabilities", []))
        prohibited_capabilities = set(assignment.get("prohibited_capabilities", []))
        required_validators = set(assignment.get("required_validators", []))
        assignment_classification = assignment.get("data_classification_limit")
        fallback_ids = set()
        for fallback_index, fallback in enumerate(assignment.get("acceptable_fallbacks", [])):
            if not isinstance(fallback, Mapping):
                continue
            fallback_base = f"{base}.acceptable_fallbacks[{fallback_index}]"
            fallback_id = fallback.get("fallback_id")
            if fallback_id in fallback_ids:
                findings.append(issue("DUPLICATE_FALLBACK_ID", f"{fallback_base}.fallback_id", f"Duplicate fallback_id: {fallback_id}"))
            fallback_ids.add(fallback_id)
            capabilities = set(fallback.get("capabilities", []))
            if not required_capabilities.issubset(capabilities):
                findings.append(issue("FALLBACK_CAPABILITY_MISMATCH", f"{fallback_base}.capabilities", "Fallback lacks one or more required capabilities"))
            if capabilities & prohibited_capabilities:
                findings.append(issue("FALLBACK_PROHIBITED_CAPABILITY", f"{fallback_base}.capabilities", "Fallback includes a prohibited capability"))
            fallback_validators = set(fallback.get("required_validators", []))
            if not required_validators.issubset(fallback_validators):
                findings.append(issue("FALLBACK_VALIDATOR_WEAKENING", f"{fallback_base}.required_validators", "Fallback omits a required validator"))
            fallback_classification = fallback.get("data_classification_limit")
            if assignment_classification in _CLASSIFICATIONS and fallback_classification in _CLASSIFICATIONS:
                if fallback_classification != assignment_classification:
                    findings.append(issue("FALLBACK_DATA_POLICY_MISMATCH", f"{fallback_base}.data_classification_limit", "Fallback must preserve the assignment data-classification limit exactly"))
            fallback_authority = fallback.get("authority_scope", {})
            for capability, enabled in fallback_authority.items():
                if enabled is True and authority.get(capability) is not True:
                    findings.append(issue("FALLBACK_AUTHORITY_EXPANSION", f"{fallback_base}.authority_scope.{capability}", "Fallback may not expand assignment authority"))

    unresolved_roles = [item.get("role_id") for item in document.get("unresolved_assignments", []) if isinstance(item, Mapping)]
    if len(unresolved_roles) != len(set(unresolved_roles)):
        findings.append(issue("DUPLICATE_UNRESOLVED_ROLE", "$.unresolved_assignments", "Unresolved role IDs must be unique"))
    unresolved_role_set = set(unresolved_roles)
    human_role_ids = {
        item.get("role_id") for item in document.get("assignments", [])
        if isinstance(item, Mapping) and item.get("role_type") == "HUMAN"
    }
    for index, assignment in enumerate(document.get("assignments", [])):
        if not isinstance(assignment, Mapping):
            continue
        role_id = assignment.get("role_id")
        desired_unknown = assignment.get("preferred_provider") == "UNKNOWN" or assignment.get("preferred_model") == "UNKNOWN"
        if (assignment.get("assignment_status") == "UNRESOLVED" or desired_unknown) and role_id not in unresolved_role_set:
            findings.append(issue(
                "UNRESOLVED_ROLE_NOT_DECLARED",
                f"$.assignments[{index}].role_id",
                "An unresolved desired assignment must be listed in unresolved_assignments",
            ))
    if document.get("approval_status") in _APPROVED_ASSIGNMENT_DOC_STATES:
        if unresolved_roles:
            findings.append(issue("UNRESOLVED_ASSIGNMENTS_BLOCK_APPROVAL", "$.unresolved_assignments", "Approved assignments cannot contain unresolved roles"))
        if not document.get("approval_ref"):
            findings.append(issue("APPROVAL_REFERENCE_REQUIRED", "$.approval_ref", "Approved assignments require human approval evidence"))
        approval_actor = document.get("provenance", {}).get("approval_actor")
        if not isinstance(approval_actor, Mapping) or approval_actor.get("actor_type") != "HUMAN":
            findings.append(issue("APPROVAL_ACTOR_REQUIRED", "$.provenance.approval_actor", "Approved assignments require a human approval actor"))
        elif approval_actor.get("actor_id") not in human_role_ids:
            findings.append(issue("APPROVAL_ACTOR_UNAUTHORIZED", "$.provenance.approval_actor.actor_id", "Approval actor must identify a declared HUMAN assignment role"))
        else:
            findings.extend(validate_approval_reference(
                document.get("approval_ref"),
                project_id=str(document.get("project_id", "")),
                profile_hash=str(document.get("source_profile_hash", "")),
                expected_actor=approval_actor,
                assignment_ids=[
                    str(item.get("assignment_id")) for item in document.get("assignments", [])
                    if isinstance(item, Mapping)
                ],
            ))
        for index, assignment in enumerate(document.get("assignments", [])):
            if isinstance(assignment, Mapping) and assignment.get("assignment_status") not in _APPROVED_ASSIGNMENT_STATES:
                findings.append(issue("ASSIGNMENT_NOT_APPROVED", f"$.assignments[{index}].assignment_status", "Every assignment in an approved document must be approved or resolved"))
    return findings


def _validate_reference_time(reference_time: str) -> None:
    try:
        parsed = datetime.datetime.fromisoformat(reference_time.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ProjectContractError([issue("INVALID_REFERENCE_TIME", "$.reference_time", "Reference time must be an ISO-8601 date-time with a timezone")]) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ProjectContractError([issue("INVALID_REFERENCE_TIME", "$.reference_time", "Reference time must include an explicit timezone")])


def validate_assignment_manifest(
    document_or_path: Union[Mapping[str, Any], str, Path],
    profile: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Validate assignment schema, semantics, and optional source-profile linkage."""
    try:
        document = (
            load_structured_file(document_or_path)
            if isinstance(document_or_path, (str, Path))
            else dict(document_or_path)
        )
    except ProjectContractError as exc:
        return {"valid": False, "errors": exc.issues, "assignments": None}
    valid, errors = validate_curo_payload(document, ASSIGNMENT_SCHEMA)
    findings = _schema_issues(errors)
    findings.extend(_assignment_semantic_issues(document))
    if profile is not None:
        findings.extend(_profile_semantic_issues(document, profile))
        expected_hash = canonical_profile_hash(profile)
        if document.get("source_profile_hash") != expected_hash:
            findings.append(issue(
                "SOURCE_PROFILE_HASH_MISMATCH",
                "$.source_profile_hash",
                "Assignment approval is invalid because the source project profile changed",
            ))
    return {"valid": bool(valid and not findings), "errors": findings, "assignments": document}


def _source_profile_path(manifest_path: Path, source_ref: str) -> Path:
    candidate = Path(source_ref)
    if candidate.is_absolute() or _WINDOWS_ABSOLUTE.match(source_ref):
        return resolve_within(get_curo_root(), candidate)
    # Canonical source references are repository-relative. Do not reinterpret
    # an escaping or missing reference relative to the manifest directory.
    return resolve_within(get_curo_root(), get_curo_root() / candidate)


def verify_assignment_linkage(manifest_path: Union[str, Path]) -> Dict[str, Any]:
    """Verify an assignment file and its declared source project profile."""
    path = Path(manifest_path).resolve()
    initial = validate_assignment_manifest(path)
    if initial["assignments"] is None:
        return initial
    document = initial["assignments"]
    findings = list(initial["errors"])
    source_ref = document.get("source_project_profile")
    if not isinstance(source_ref, str):
        return {"valid": False, "errors": findings, "assignments": document}
    try:
        profile_path = _source_profile_path(path, source_ref)
    except ValueError:
        findings.append(issue(
            "SOURCE_PROFILE_PATH_UNAUTHORIZED",
            "$.source_project_profile",
            "Source project profile escapes the Curo workspace boundary",
        ))
        return {"valid": False, "errors": findings, "assignments": document}
    profile_result = validate_project_profile(profile_path)
    if not profile_result["valid"]:
        findings.append(issue("SOURCE_PROFILE_INVALID", "$.source_project_profile", f"Source project profile is missing or invalid: {profile_path}"))
        findings.extend(profile_result["errors"])
        # A changed profile may invalidate its own approval evidence as well as
        # the assignment linkage. Preserve the direct linkage diagnostic when
        # the document was still parseable so callers do not have to infer it
        # from the broader SOURCE_PROFILE_INVALID result.
        invalid_profile = profile_result.get("profile")
        if isinstance(invalid_profile, Mapping):
            expected_hash = canonical_profile_hash(invalid_profile)
            if document.get("source_profile_hash") != expected_hash:
                findings.append(issue(
                    "SOURCE_PROFILE_HASH_MISMATCH",
                    "$.source_profile_hash",
                    "Assignment approval is invalid because the source project profile changed",
                ))
        return {"valid": False, "errors": findings, "assignments": document}
    profile = profile_result["profile"]
    expected_hash = canonical_profile_hash(profile)
    if document.get("source_profile_hash") != expected_hash and not any(
        item.get("code") == "SOURCE_PROFILE_HASH_MISMATCH" for item in findings
    ):
        findings.append(issue("SOURCE_PROFILE_HASH_MISMATCH", "$.source_profile_hash", "Assignment approval is invalid because the source project profile changed"))
    findings.extend(_profile_semantic_issues(document, profile))
    return {"valid": not findings, "errors": findings, "assignments": document, "profile_hash": expected_hash}


def _portable_source_ref(profile_path: Path) -> str:
    try:
        return profile_path.resolve().relative_to(get_curo_root()).as_posix()
    except ValueError:
        return str(profile_path.resolve())


def compile_assignments(
    profile_path: Union[str, Path],
    assignment_input_path: Union[str, Path],
    reference_time: str,
    output_path: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Deterministically bind explicit assignment input to approved project intent."""
    try:
        profile_file = resolve_within(get_curo_root(), profile_path)
        assignment_input_file = resolve_within(get_curo_root(), assignment_input_path)
    except ValueError as exc:
        raise ProjectContractError([
            issue("COMPILER_INPUT_PATH_UNAUTHORIZED", "$", "Compiler profile and assignment inputs must remain inside the Curo workspace")
        ]) from exc
    profile_result = validate_project_profile(profile_file)
    if not profile_result["valid"]:
        raise ProjectContractError(profile_result["errors"])
    profile = profile_result["profile"]
    if profile.get("profile_status") not in {"APPROVED", "ACTIVE"}:
        raise ProjectContractError([issue("PROFILE_NOT_APPROVED", "$.profile_status", "Assignment compilation requires APPROVED or ACTIVE project intent")])

    try:
        assignment_input = load_structured_file(assignment_input_file)
    except ProjectContractError:
        raise
    input_result = validate_assignment_manifest(assignment_input)
    if not input_result["valid"]:
        raise ProjectContractError(input_result["errors"])
    _validate_reference_time(reference_time)
    document = copy.deepcopy(assignment_input)
    current_hash = canonical_profile_hash(profile)
    prior_hash = document.get("source_profile_hash")
    profile_changed = prior_hash not in (None, current_hash)

    document["artifact_type"] = "curo_llm_assignments"
    document["project_id"] = profile["project_id"]
    document["source_project_profile"] = _portable_source_ref(profile_file)
    document["source_profile_hash"] = current_hash
    document["reference_time"] = reference_time
    document["generated_at"] = reference_time
    document["generated_by"] = {
        "generator_type": "CURO_COMPILER",
        "generator_id": "curo-project-compiler",
        "deterministic": True,
    }
    if profile_changed and document.get("approval_status") == "APPROVED":
        document["approval_status"] = "DECISION_REQUIRED"
        document["approval_ref"] = None
        provenance = document.get("provenance")
        if isinstance(provenance, dict):
            provenance["approval_actor"] = None
        for assignment in document.get("assignments", []):
            if isinstance(assignment, dict) and assignment.get("assignment_status") == "APPROVED":
                assignment["assignment_status"] = "READY_FOR_APPROVAL"

    # Normalize mapping order recursively so the persisted pretty JSON is
    # byte-equivalent for the same parsed inputs and reference time.
    document = json.loads(json.dumps(document, sort_keys=True, ensure_ascii=False, allow_nan=False))

    result = validate_assignment_manifest(document, profile=profile)
    if not result["valid"]:
        raise ProjectContractError(result["errors"])
    if output_path is not None:
        destination = resolve_within(get_curo_root(), output_path)
        persisted, errors = validate_and_write_json(document, ASSIGNMENT_SCHEMA, destination)
        if not persisted:
            raise ProjectContractError(_schema_issues(errors))
    return document


def compare_identities(
    assignment: Mapping[str, Any],
    observed_run_record: Optional[Union[str, Path]] = None,
    *,
    expected_project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Compare identity using only a validated, trusted observed run record."""
    desired = {"provider": assignment.get("preferred_provider"), "model": assignment.get("preferred_model")}
    resolved = {
        "state": assignment.get("resolved_identity_state", "UNRESOLVED"),
        "provider": assignment.get("resolved_provider"),
        "model": assignment.get("resolved_model"),
    }
    observed_identity = {"state": "UNKNOWN", "provider": None, "model": None}
    evidence_valid = False
    if isinstance(observed_run_record, (str, Path)):
        try:
            run_path = resolve_within(get_curo_root(), observed_run_record)
            run_document = safe_read_json(run_path)
            run_valid, _ = validate_curo_payload(run_document, "run-record")
            trusted_source = run_document.get("provenance_source") in {
                "HARNESS_API", "HARNESS_CLI", "UI_OBSERVATION",
            }
            candidate = run_document.get("observed_identity", {})
            project_matches = bool(expected_project_id) and run_document.get("project_id") == expected_project_id
            role_matches = run_document.get("role") == assignment.get("role_id")
            evidence_ref = candidate.get("evidence_source") if isinstance(candidate, Mapping) else None
            evidence_path = resolve_within(get_curo_root(), evidence_ref) if evidence_ref else None
            evidence_hash_matches = bool(
                evidence_path and evidence_path.is_file()
                and sha256_file(evidence_path) == candidate.get("evidence_sha256")
            )
            locator_paths = []
            for locator in run_document.get("evidence_locators", []):
                try:
                    locator_paths.append(resolve_within(get_curo_root(), locator))
                except ValueError:
                    continue
            evidence_bound = evidence_path in locator_paths if evidence_path else False
            provenance_bound = False
            for locator_path in locator_paths:
                if not locator_path.is_file() or locator_path == evidence_path:
                    continue
                try:
                    provenance = safe_read_json(locator_path)
                except Exception:
                    continue
                provenance_valid, _ = validate_curo_payload(provenance, "provenance-record")
                if (
                    provenance_valid
                    and provenance.get("owner") == "harness"
                    and provenance.get("artifact_id") == run_document.get("run_id")
                    and provenance.get("observed_identity") == candidate
                ):
                    provenance_bound = True
                    break
            if (
                run_valid and trusted_source and project_matches and role_matches
                and evidence_bound and evidence_hash_matches and provenance_bound
                and isinstance(candidate, Mapping)
            ):
                observed_identity = {
                    "state": candidate.get("state", "UNKNOWN"),
                    "provider": candidate.get("provider"),
                    "model": candidate.get("model"),
                }
                evidence_valid = True
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            evidence_valid = False
    matches = None
    if observed_identity["state"] == "VERIFIED" and resolved["state"] == "RESOLVED":
        matches = observed_identity["provider"] == resolved["provider"] and observed_identity["model"] == resolved["model"]
        if not matches:
            observed_identity["state"] = "MISMATCH"
    return {
        "desired": desired,
        "resolved": resolved,
        "observed": observed_identity,
        "observed_evidence_valid": evidence_valid,
        "resolved_matches_observed": matches,
    }
