"""Scoped canonical vocabularies shared by Curo runtime entry points."""

CANDIDATE_TYPES = ("rule", "skill", "anti_pattern", "validator", "standard_amendment")
PROVENANCE_RESULTS = ("PASS", "FAIL", "UNKNOWN")
RUN_STATUSES = ("PASS", "FAIL", "UNKNOWN", "TIMED_OUT")
PROCESS_STATUSES = ("COMPLETE", "FAIL", "TIMED_OUT", "NOT_STARTED")
LEARNING_STATUSES = ("PROPOSED", "VALIDATION_PENDING", "VALIDATED", "APPROVED", "PROMOTED", "REJECTED", "BLOCKED")
PROJECT_PROFILE_STATUSES = ("DRAFT", "DECISION_REQUIRED", "READY_FOR_APPROVAL", "APPROVED", "ACTIVE", "BLOCKED", "SUPERSEDED", "RETIRED")
ASSIGNMENT_STATUSES = ("PROPOSED", "UNRESOLVED", "READY_FOR_APPROVAL", "APPROVED", "RESOLVED", "UNAVAILABLE", "BLOCKED", "SUPERSEDED")
OBSERVED_IDENTITY_STATUSES = ("VERIFIED", "UNKNOWN", "UNAVAILABLE", "MISMATCH")
RUNTIME_ARTIFACT_SCHEMAS = {
    "provenance_record": "https://curo.local/schemas/provenance-record.schema.json",
    "observability_run_record": "https://curo.local/schemas/observability-run-record.schema.json",
    "execution_replay_manifest": "https://curo.local/schemas/execution-replay-manifest.schema.json",
    "artifact_verification_manifest": "https://curo.local/schemas/artifact-verification-manifest.schema.json",
    "curo_learning_candidate": "https://curo.local/schemas/learning-candidate.schema.json",
    "curo_hitl_packet": "https://curo.local/schemas/hitl-packet.schema.json",
    "curo_project_profile": "https://curo.local/schemas/project-profile.schema.json",
    "curo_llm_assignments": "https://curo.local/schemas/llm-assignments.schema.json",
    "curo_human_approval_record": "https://curo.local/schemas/human-approval-record.schema.json",
}
