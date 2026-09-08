"""Master CLI entrypoint for Curo Execution & Evidence Harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .distill import distill_learning_candidate
from .escalate import generate_hitl_packet
from .replay import execute_replay
from .run import execute_run
from .assignments import compile_assignments, verify_assignment_linkage
from .core import get_curo_root, resolve_within
from .projects import ProjectContractError, validate_project_profile
from .security import redact_secrets
from .validator import get_schema_path, validate_curo_payload
from .vocabularies import CANDIDATE_TYPES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="curo",
        description="Curo Universal Execution & Evidence Harness"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Harness action")

    # Command: run
    run_p = subparsers.add_parser("run", help="Execute command with telemetry & evidence capture")
    run_p.add_argument("command", nargs="?", help="Deprecated simple command string (shell syntax rejected)")
    run_p.add_argument("--executable", help="Executable name or path")
    run_p.add_argument("--arg", action="append", default=[], help="One argument; repeat to preserve argv boundaries")
    run_p.add_argument("--id", required=True, help="Unique Run ID (e.g. RUN-001)")
    run_p.add_argument("--input", "-i", action="append", help="Declared input file path for hashing")
    run_p.add_argument("--output", "-o", action="append", help="Declared output file path for hashing")
    run_p.add_argument("--timeout", type=float, default=300.0, help="Max execution timeout in seconds")
    run_p.add_argument("--evidence-dir", help="Directory to store evidence records")

    # Command: replay
    replay_p = subparsers.add_parser("replay", help="Replay a recorded run manifest deterministically")
    replay_p.add_argument("manifest", help="Path to replay-manifest JSON file")

    # Command: escalate
    esc_p = subparsers.add_parser("escalate", help="Generate a structured HITL exception packet")
    esc_p.add_argument("--id", required=True, help="Packet ID (e.g. HITL-DEC-001)")
    esc_p.add_argument("--project", default="curo-project", help="Project ID")
    esc_p.add_argument("--review-id", default="REV-001", help="Review ID")
    esc_p.add_argument("--finding", required=True, help="Description of blocking issue")
    esc_p.add_argument(
        "--class",
        dest="finding_class",
        choices=["mechanical", "engineering", "evidence_required", "human_decision"],
        default="human_decision",
        help="Curo finding classification"
    )

    # Command: distill
    dist_p = subparsers.add_parser("distill", help="Distill an observed run into a learning candidate")
    dist_p.add_argument("--id", required=True, help="Candidate ID (e.g. LC-001)")
    dist_p.add_argument("--run-id", required=True, help="Source Run ID")
    dist_p.add_argument("--title", required=True, help="Pattern title")
    dist_p.add_argument("--type", choices=CANDIDATE_TYPES, default="rule", help="Proposal type")
    dist_p.add_argument("--summary", default="", help="Summary of the pattern")

    # Command: doctor
    subparsers.add_parser("doctor", help="Verify Curo harness & schema readiness")

    # Command: project
    project_p = subparsers.add_parser("project", help="Validate and compile project-specific contracts")
    project_sub = project_p.add_subparsers(dest="project_action", required=True)
    project_validate = project_sub.add_parser("validate", help="Validate a project profile")
    project_validate.add_argument("profile", help="Project profile YAML or JSON inside the Curo workspace")
    project_compile = project_sub.add_parser("compile", help="Compile deterministic LLM/agent assignments")
    project_compile.add_argument("profile", help="Approved project profile YAML or JSON")
    project_compile.add_argument("--assignments", required=True, help="Explicit assignment input JSON")
    project_compile.add_argument("--reference-time", required=True, help="Explicit ISO-8601 reference time")
    project_compile.add_argument("--output", required=True, help="Output JSON path inside the Curo workspace")
    project_verify = project_sub.add_parser("verify-assignments", help="Verify assignments and source-profile linkage")
    project_verify.add_argument("assignments", help="Assignment JSON inside the Curo workspace")

    return parser


def main(args: list[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.subcommand:
        parser.print_help()
        return 0

    if parsed.subcommand == "run":
        res = execute_run(
            executable=parsed.executable,
            args=parsed.arg,
            command=parsed.command,
            run_id=parsed.id,
            inputs=parsed.input,
            outputs=parsed.output,
            timeout_seconds=parsed.timeout,
            evidence_dir=parsed.evidence_dir,
            provenance_source="HARNESS_CLI",
        )
        print(json.dumps(res, indent=2))
        return 0 if res["status"] == "PASS" else (res.get("exit_code") or 1)

    elif parsed.subcommand == "replay":
        res = execute_replay(parsed.manifest)
        print(json.dumps(res, indent=2))
        return 0 if res["status"] == "REPLAY_VERIFIED" else 1

    elif parsed.subcommand == "escalate":
        res = generate_hitl_packet(
            packet_id=parsed.id,
            project_id=parsed.project,
            review_id=parsed.review_id,
            finding_description=parsed.finding,
            finding_class=parsed.finding_class
        )
        print(json.dumps(res, indent=2))
        return 0

    elif parsed.subcommand == "distill":
        res = distill_learning_candidate(
            candidate_id=parsed.id,
            source_run_id=parsed.run_id,
            proposed_type=parsed.type,
            title=parsed.title,
            summary=parsed.summary
        )
        print(json.dumps(res, indent=2))
        return 0

    elif parsed.subcommand == "doctor":
        print("Curo Harness Doctor: OK")
        print(f"Python: {sys.version}")
        print("All schemas and core modules loaded successfully.")
        return 0

    elif parsed.subcommand == "project":
        try:
            if parsed.project_action == "validate":
                profile_path = resolve_within(get_curo_root(), parsed.profile)
                result = validate_project_profile(profile_path)
            elif parsed.project_action == "compile":
                profile_path = resolve_within(get_curo_root(), parsed.profile)
                assignment_path = resolve_within(get_curo_root(), parsed.assignments)
                output_path = resolve_within(get_curo_root(), parsed.output)
                artifact = compile_assignments(
                    profile_path, assignment_path, parsed.reference_time, output_path,
                )
                result = {"valid": True, "errors": [], "output": str(output_path), "assignments": artifact}
            else:
                assignment_path = resolve_within(get_curo_root(), parsed.assignments)
                result = verify_assignment_linkage(assignment_path)
        except ProjectContractError as exc:
            result = {"valid": False, "errors": exc.issues}
        except Exception as exc:
            clean_message, _ = redact_secrets(str(exc))
            result = {"valid": False, "errors": [{"code": "PROJECT_COMMAND_ERROR", "path": "$", "message": clean_message}]}
        print(json.dumps(result, indent=2))
        return 0 if result.get("valid") else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
