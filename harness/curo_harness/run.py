"""Structured execution wrapper with validated evidence generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .core import resolve_within, safe_write_json, sha256_dict, sha256_file, utc_now_iso
from .process import ProcessResult, run_structured_process
from .security import parse_legacy_command, redact_secrets
from .validator import validate_curo_payload


def _result_failure(run_id: str, message: str, errors: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "status": "FAIL",
        "exit_code": 1,
        "error": message,
        "validation_errors": errors or [],
        "provenance_file": None,
        "run_record_file": None,
        "replay_manifest_file": None,
    }


def execute_run(
    executable: Optional[str] = None,
    args: Optional[List[str]] = None,
    run_id: str = "",
    inputs: Optional[List[str]] = None,
    outputs: Optional[List[str]] = None,
    timeout_seconds: float = 300.0,
    evidence_dir: Optional[str] = None,
    cwd: Optional[str] = None,
    command: Optional[str] = None,
    project_id: str = "curo-project",
    workflow_id: str = "structured-execution",
    provenance_source: str = "HARNESS_API",
) -> Dict[str, Any]:
    """Execute argv with ``shell=False`` and persist only schema-valid artifacts.

    ``command`` is a deprecated compatibility input. It rejects shell operators and
    is converted to the canonical executable/args representation before execution.
    """
    if not run_id:
        return _result_failure(run_id, "run_id is required")
    try:
        if executable is None:
            if command is None:
                raise ValueError("executable is required")
            executable, parsed_args = parse_legacy_command(command)
            if args:
                raise ValueError("args cannot be combined with deprecated command input")
            args = parsed_args
        canonical_args = [str(item) for item in (args or [])]
        working_dir = Path(cwd).resolve() if cwd else Path.cwd().resolve()
        if not working_dir.is_dir():
            raise ValueError(f"Working directory does not exist: {working_dir}")
        target_evidence_dir = resolve_within(
            working_dir, evidence_dir if evidence_dir is not None else Path("evidence") / "runs"
        )
        input_paths = [(item, resolve_within(working_dir, item)) for item in (inputs or [])]
        output_paths = [(item, resolve_within(working_dir, item)) for item in (outputs or [])]
    except Exception as exc:
        return _result_failure(run_id, f"Execution contract rejected: {exc}")

    input_hashes: Dict[str, str] = {}
    diagnostic_reasons: List[str] = []
    for declared, path in input_paths:
        if path.is_file():
            input_hashes[declared] = sha256_file(path)
        else:
            input_hashes[declared] = "UNKNOWN"
            diagnostic_reasons.append(f"REQUIRED_INPUT_UNVERIFIABLE:{declared}")

    started_at = utc_now_iso()
    process_result: ProcessResult
    if diagnostic_reasons:
        process_result = ProcessResult(None, "", "Execution blocked by unverifiable required input.", False, 0.0, None)
        process_status = "NOT_STARTED"
    else:
        try:
            process_result = run_structured_process(str(executable), canonical_args, str(working_dir), timeout_seconds)
            process_status = "TIMED_OUT" if process_result.timed_out else (
                "COMPLETE" if process_result.exit_code == 0 else "FAIL"
            )
        except Exception as exc:
            process_result = ProcessResult(1, "", f"Process launch error: {exc}", False, 0.0, None)
            process_status = "FAIL"
            diagnostic_reasons.append("PROCESS_LAUNCH_FAILED")
    completed_at = utc_now_iso()

    output_hashes: Dict[str, str] = {}
    for declared, path in output_paths:
        if path.is_file():
            output_hashes[declared] = sha256_file(path)
        else:
            output_hashes[declared] = "UNKNOWN"
            diagnostic_reasons.append(f"REQUIRED_OUTPUT_MISSING:{declared}")

    if process_result.timed_out:
        status, validation_status = "TIMED_OUT", "FAIL"
        diagnostic_reasons.append("PROCESS_TIMED_OUT")
        if process_result.timeout_termination_succeeded is False:
            diagnostic_reasons.append("PROCESS_TREE_TERMINATION_UNCONFIRMED")
    elif process_status == "NOT_STARTED":
        status, validation_status = "UNKNOWN", "UNKNOWN"
    elif process_result.exit_code != 0:
        status, validation_status = "FAIL", "FAIL"
        diagnostic_reasons.append("PROCESS_EXIT_NONZERO")
    elif any(value == "UNKNOWN" for value in output_hashes.values()):
        status, validation_status = "FAIL", "FAIL"
    else:
        status, validation_status = "PASS", "PASS"

    stdout, stdout_redacted = redact_secrets(process_result.stdout)
    stderr, stderr_redacted = redact_secrets(process_result.stderr)
    redaction_applied = stdout_redacted or stderr_redacted
    input_hash = "UNKNOWN" if any(value == "UNKNOWN" for value in input_hashes.values()) else sha256_dict(input_hashes)
    output_hash = "UNKNOWN" if any(value == "UNKNOWN" for value in output_hashes.values()) else sha256_dict(output_hashes)

    target_evidence_dir.mkdir(parents=True, exist_ok=True)
    prov_path = target_evidence_dir / f"{run_id}-provenance.json"
    run_path = target_evidence_dir / f"{run_id}-run.json"
    replay_path = target_evidence_dir / f"{run_id}-execution-replay.json"
    provenance_record = {
        "record_type": "provenance_record",
        "artifact_id": run_id,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "validator_result": validation_status,
        "owner": "harness",
        "created_at": completed_at,
        "source_conversation_id": "curo-execution-harness",
        "source_note": "Structured executable and argv executed by the Curo harness.",
        "validation_errors": [],
        "diagnostic_reasons": diagnostic_reasons,
        "observed_identity": {
            "state": "UNKNOWN",
            "provider": None,
            "model": None,
            "evidence_source": None,
            "evidence_sha256": None,
        },
    }
    run_record = {
        "record_type": "observability_run_record",
        "run_id": run_id,
        "recorded_at": completed_at,
        "project_id": project_id,
        "workflow_id": workflow_id,
        "role": "harness",
        "status": status,
        "process_status": process_status,
        "validation_status": validation_status,
        "provenance_source": provenance_source,
        "observed_identity": {
            "state": "UNKNOWN",
            "provider": None,
            "model": None,
            "evidence_source": None,
            "evidence_sha256": None,
        },
        "evidence_locators": [str(prov_path), str(replay_path)],
        "next_authorized_action": "REVIEW_FAILURE" if status != "PASS" else "REPLAY_OR_PROMOTE",
        "execution": {
            "executable": str(executable), "args": canonical_args, "cwd": str(working_dir),
            "timeout_seconds": timeout_seconds, "exit_code": process_result.exit_code,
            "duration_ms": process_result.duration_ms,
            "timeout_termination_succeeded": process_result.timeout_termination_succeeded,
        },
        "inputs": input_hashes,
        "outputs": output_hashes,
        "diagnostic_reasons": diagnostic_reasons,
        "stdout_snippet": stdout[-1000:],
        "stderr_snippet": stderr[-1000:],
        "redaction_applied": redaction_applied,
    }
    replay_manifest = {
        "manifest_type": "execution_replay_manifest",
        "artifact_id": run_id,
        "version": "1.0.0",
        "executable": str(executable),
        "args": canonical_args,
        "cwd": str(working_dir),
        "timeout_seconds": timeout_seconds,
        "inputs": [{"path": key, "sha256": value, "status": "UNKNOWN" if value == "UNKNOWN" else "VERIFIED"} for key, value in input_hashes.items()],
        "expected_outputs": [{"path": key, "sha256": value, "status": "UNKNOWN" if value == "UNKNOWN" else "VERIFIED"} for key, value in output_hashes.items()],
        "expected_checks": ["input_hash_verification", "process_exit_zero", "output_hash_verification", "artifact_schema_validation"],
        "provenance": provenance_record,
    }

    artifacts = (
        (provenance_record, "provenance-record", prov_path),
        (run_record, "run-record", run_path),
        (replay_manifest, "execution-replay-manifest", replay_path),
    )
    validation_errors: List[str] = []
    for payload, schema_name, _ in artifacts:
        valid, errors = validate_curo_payload(payload, schema_name)
        if not valid:
            validation_errors.extend(f"{schema_name}: {error}" for error in errors)
    if validation_errors:
        return _result_failure(run_id, "Authoritative artifact validation failed; no artifacts written", validation_errors)
    try:
        for payload, _, path in artifacts:
            safe_write_json(path, payload)
    except Exception as exc:
        return _result_failure(run_id, f"Authoritative artifact persistence failed: {exc}")

    return {
        "run_id": run_id, "status": status, "process_status": process_status,
        "validation_status": validation_status, "exit_code": process_result.exit_code,
        "duration_ms": process_result.duration_ms, "provenance_file": str(prov_path),
        "run_record_file": str(run_path), "replay_manifest_file": str(replay_path),
        "inputs": input_hashes, "outputs": output_hashes,
        "diagnostic_reasons": diagnostic_reasons,
    }
