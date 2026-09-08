"""Execution replay and non-executing artifact verification."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .core import resolve_within, safe_read_json, sha256_file, utc_now_iso
from .process import run_structured_process
from .security import redact_secrets
from .validator import validate_curo_payload


def _load_manifest(manifest_path: str, workspace_root: Path) -> Dict[str, Any]:
    path = resolve_within(workspace_root, manifest_path)
    if not path.is_file():
        raise FileNotFoundError(f"Replay manifest file not found: {manifest_path}")
    payload = safe_read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Replay manifest must be a JSON object")
    return payload


def _check_files(items: List[Dict[str, Any]], workspace_root: Path) -> tuple[List[Dict[str, Any]], bool]:
    checks: List[Dict[str, Any]] = []
    passed = True
    for item in items:
        declared = item.get("path", "")
        try:
            path = resolve_within(workspace_root, declared)
        except ValueError as exc:
            checks.append({"path": declared, "status": "FAIL", "reason": str(exc)})
            passed = False
            continue
        if not path.is_file():
            checks.append({"path": declared, "status": "FAIL", "reason": "REQUIRED_ARTIFACT_MISSING"})
            passed = False
            continue
        actual = sha256_file(path)
        expected = item.get("sha256")
        matched = expected != "UNKNOWN" and actual == expected
        checks.append({"path": declared, "status": "PASS" if matched else "FAIL", "expected": expected, "actual": actual})
        passed = passed and matched
    return checks, passed


def _verify_artifacts(manifest: Dict[str, Any], workspace_root: Path) -> Dict[str, Any]:
    checks, passed = _check_files(manifest["artifacts"], workspace_root)
    for item, check in zip(manifest["artifacts"], checks):
        schema_name = item.get("schema")
        if check["status"] == "PASS" and schema_name:
            payload = safe_read_json(resolve_within(workspace_root, item["path"]))
            valid, errors = validate_curo_payload(payload, schema_name)
            check["schema_status"] = "PASS" if valid else "FAIL"
            check["schema_errors"] = errors
            passed = passed and valid
    return {
        "status": "VERIFIED" if passed else "FAIL",
        "manifest_type": "artifact_verification_manifest",
        "artifact_id": manifest["artifact_id"],
        "artifact_checks": checks,
        "timestamp": utc_now_iso(),
    }


def execute_replay(manifest_path: str, cwd: Optional[str] = None) -> Dict[str, Any]:
    """Dispatch a validated replay artifact by its non-overlapping manifest type."""
    workspace_root = Path(cwd).resolve() if cwd else Path.cwd().resolve()
    try:
        manifest = _load_manifest(manifest_path, workspace_root)
    except Exception as exc:
        return {"status": "FAIL", "error": str(exc)}

    manifest_type = manifest.get("manifest_type")
    schema_name = {
        "execution_replay_manifest": "execution-replay-manifest",
        "artifact_verification_manifest": "artifact-verification-manifest",
    }.get(manifest_type)
    if schema_name is None:
        return {"status": "FAIL", "error": f"Unknown replay artifact class: {manifest_type!r}"}
    valid, errors = validate_curo_payload(manifest, schema_name)
    if not valid:
        return {"status": "FAIL", "error": "Replay manifest validation failed", "validation_errors": errors}
    if manifest_type == "artifact_verification_manifest":
        return _verify_artifacts(manifest, workspace_root)

    try:
        execution_cwd = resolve_within(workspace_root, manifest["cwd"])
        input_checks, inputs_passed = _check_files(manifest["inputs"], workspace_root)
    except Exception as exc:
        return {"status": "FAIL", "error": f"Execution replay boundary rejected: {exc}"}
    if not inputs_passed:
        return {"status": "BLOCKED", "reason": "Pre-flight input verification failed", "input_checks": input_checks}

    try:
        result = run_structured_process(
            manifest["executable"], manifest["args"], str(execution_cwd), manifest["timeout_seconds"]
        )
    except Exception as exc:
        return {"status": "FAIL", "error": f"Replay process launch failed: {exc}"}
    _, stderr_redacted = redact_secrets(result.stderr)
    stderr, _ = redact_secrets(result.stderr)
    if result.timed_out:
        return {
            "status": "TIMED_OUT", "exit_code": result.exit_code,
            "timeout_termination_succeeded": result.timeout_termination_succeeded,
            "stderr": stderr[-500:], "redaction_applied": stderr_redacted,
        }
    if result.exit_code != 0:
        return {"status": "FAIL", "exit_code": result.exit_code, "stderr": stderr[-500:], "redaction_applied": stderr_redacted}

    output_checks, outputs_passed = _check_files(manifest["expected_outputs"], workspace_root)
    return {
        "status": "REPLAY_VERIFIED" if outputs_passed else "REPLAY_DRIFT_DETECTED",
        "manifest_type": manifest_type,
        "artifact_id": manifest["artifact_id"],
        "duration_ms": result.duration_ms,
        "input_checks": input_checks,
        "output_checks": output_checks,
        "timestamp": utc_now_iso(),
    }
