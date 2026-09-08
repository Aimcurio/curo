"""HITL Exception packet generator for Curo review protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .core import resolve_within, utc_now_iso
from .validator import validate_and_write_json


def generate_hitl_packet(
    packet_id: str,
    project_id: str,
    review_id: str,
    finding_description: str,
    finding_class: str = "human_decision",
    blocking: bool = True,
    decisions_required: Optional[List[Dict[str, Any]]] = None,
    authorized_transition: str = "WAIT_FOR_HUMAN_REVIEW",
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """Generate a structured Curo Human-in-the-Loop exception packet."""
    valid_classes = {"mechanical", "engineering", "evidence_required", "human_decision"}
    if finding_class not in valid_classes:
        raise ValueError(f"Invalid finding_class '{finding_class}'. Must be one of: {valid_classes}")

    packet = {
        "artifact_type": "curo_hitl_packet",
        "packet_version": "1.0.0",
        "packet_id": packet_id,
        "project_id": project_id,
        "review_id": review_id,
        "status": "HITL_REQUIRED",
        "created_at": utc_now_iso(),
        "summary": {
            "automatic_corrections_applied": 0,
            "model_resolutions_applied": 0,
            "evidence_checks_pending": 1 if finding_class == "evidence_required" else 0,
            "human_decisions_required": 1 if finding_class == "human_decision" else 0
        },
        "blocking_findings": [
            {
                "id": f"FINDING-{packet_id}",
                "severity": "critical" if blocking else "warning",
                "finding_class": finding_class,
                "description": finding_description,
                "blocking": blocking
            }
        ],
        "decisions": decisions_required or [],
        "authorized_transition": authorized_transition
    }

    workspace_root = Path.cwd().resolve()
    target_dir = resolve_within(workspace_root, output_dir if output_dir else Path("evidence") / "review")
    out_file = target_dir / f"{packet_id}.json"
    valid, errors = validate_and_write_json(packet, "hitl-packet", out_file)
    if not valid:
        return {"status": "FAIL", "packet_id": packet_id, "validation_errors": errors, "file": None}

    return {
        "status": "ESCALATED",
        "packet_id": packet_id,
        "finding_class": finding_class,
        "file": str(out_file),
        "packet": packet
    }
