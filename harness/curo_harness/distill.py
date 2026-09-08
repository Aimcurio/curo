"""Learning distillation engine converting observations into structured proposals."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .core import resolve_within, utc_now_iso
from .validator import validate_and_write_json
from .vocabularies import CANDIDATE_TYPES


def distill_learning_candidate(
    candidate_id: str,
    source_run_id: str,
    proposed_type: str = "rule",
    title: str = "Extracted Pattern",
    summary: str = "",
    pattern_description: str = "",
    evidence_references: Optional[List[str]] = None,
    output_dir: Optional[str] = None,
    project_id: str = "curo-project",
) -> Dict[str, Any]:
    """Distill an observed run event or finding into a Curo learning candidate proposal."""
    if proposed_type not in CANDIDATE_TYPES:
        raise ValueError(f"Invalid proposed_type '{proposed_type}'. Must be one of: {CANDIDATE_TYPES}")

    candidate = {
        "artifact_type": "curo_learning_candidate",
        "artifact_version": "1.0.0",
        "candidate_id": candidate_id,
        "project_id": project_id,
        "owner": "harness",
        "status": "PROPOSED",
        "candidate_type": proposed_type,
        "source_run_ids": [source_run_id],
        "evidence_refs": evidence_references or [source_run_id],
        "proposed_change": {
            "target": title,
            "description": pattern_description or summary or "Candidate requires further description."
        },
        "required_validation": [],
        "requires_hitl": True,
        "promotion_ref": None,
    }

    workspace_root = Path.cwd().resolve()
    target_dir = resolve_within(workspace_root, output_dir if output_dir else Path("evidence") / "learning")
    out_file = target_dir / f"{candidate_id}.json"
    valid, errors = validate_and_write_json(candidate, "learning-candidate", out_file)
    if not valid:
        return {"status": "FAIL", "candidate_id": candidate_id, "validation_errors": errors, "file": None}

    return {
        "status": "PROPOSED",
        "candidate_id": candidate_id,
        "candidate_type": proposed_type,
        "file": str(out_file),
        "candidate": candidate
    }
