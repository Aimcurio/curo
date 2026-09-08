"""Project profile and deterministic assignment runtime tests."""

import copy
import contextlib
import io
import json
import shutil
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
HARNESS_DIR = ROOT / "harness"
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

from curo_harness.assignments import compare_identities, compile_assignments, validate_assignment_manifest, verify_assignment_linkage
from curo_harness.cli import main
from curo_harness.projects import ProjectContractError, canonical_profile_hash, validate_project_profile


def write_profile_approval(profile, directory):
    record = {
        "artifact_type": "curo_human_approval_record", "artifact_version": "1.0.0",
        "approval_id": "PROFILE-APPROVAL-001", "project_id": profile["project_id"],
        "decision": "APPROVE", "approved_profile_hash": canonical_profile_hash(profile),
        "approved_assignment_ids": [],
        "actor": {"actor_type": "HUMAN", "actor_id": "human-requester"},
        "recorded_at": "2026-09-07T00:00:00Z", "recorded_by": "harness",
        "evidence_source": "authorized test fixture",
    }
    path = directory / "profile-approval.json"
    path.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
    import hashlib
    return {
        "artifact_path": path.relative_to(ROOT).as_posix(),
        "artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "approval_id": record["approval_id"],
    }


class ProjectRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.scratch = ROOT / "tests" / "project-scratch"
        if self.scratch.exists():
            shutil.rmtree(self.scratch)
        self.scratch.mkdir(parents=True)
        self.profile = self._load_yaml(ROOT / "templates" / "project-profile.yaml")
        self.profile.update({
            "project_id": "test-project",
            "display_name": "Test Project",
            "description": "A bounded test project.",
            "profile_status": "APPROVED",
            "actual_project_roots": [str(self.scratch)],
            "execution_environment": {**self.profile["execution_environment"], "workspace_boundary": str(self.scratch)},
        })
        self.profile["open_decisions"] = []
        self.profile["objectives"]["primary"] = "Verify project assignment contracts."
        self.profile["architecture"]["summary"] = "A local test fixture."
        self.profile["storage_policy"]["retention"] = "Delete during test teardown."
        self.profile["provenance"]["approval_ref"] = write_profile_approval(self.profile, self.scratch)
        self.profile_path = self.scratch / "project.yaml"
        # JSON is valid YAML and exercises the dependency-free profile path.
        self.profile_path.write_text(json.dumps(self.profile), encoding="utf-8")
        self.assignment = json.loads((ROOT / "templates" / "llm-assignments.json").read_text(encoding="utf-8"))
        self.assignment["project_id"] = "test-project"
        self.assignment["assignments"][0]["allowed_project_roots"] = [str(self.scratch)]
        self.assignment_path = self.scratch / "input.json"
        self.assignment_path.write_text(json.dumps(self.assignment), encoding="utf-8")

    def tearDown(self):
        if self.scratch.exists():
            shutil.rmtree(self.scratch)

    @staticmethod
    def _load_yaml(path):
        try:
            import yaml
        except ImportError as exc:
            raise unittest.SkipTest("PyYAML unavailable for loading the repository YAML fixture") from exc
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_project_profile_validates_and_hash_ignores_key_order(self):
        result = validate_project_profile(self.profile)
        self.assertTrue(result["valid"], result["errors"])
        reordered = dict(reversed(list(self.profile.items())))
        self.assertEqual(canonical_profile_hash(self.profile), canonical_profile_hash(reordered))

    def test_approved_profile_requires_declared_human_operator(self):
        profile = copy.deepcopy(self.profile)
        approval_path = ROOT / profile["provenance"]["approval_ref"]["artifact_path"]
        record = json.loads(approval_path.read_text(encoding="utf-8"))
        record["actor"]["actor_id"] = "undeclared-human"
        approval_path.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
        import hashlib
        profile["provenance"]["approval_ref"]["artifact_sha256"] = hashlib.sha256(approval_path.read_bytes()).hexdigest()

        result = validate_project_profile(profile)

        self.assertIn("APPROVAL_ACTOR_UNAUTHORIZED", {item["code"] for item in result["errors"]})

    def test_unresolved_decision_blocks_approved_profile(self):
        profile = copy.deepcopy(self.profile)
        profile["open_decisions"] = [{"decision_id": "d1", "question": "Choose", "status": "OPEN", "owner": "human"}]
        result = validate_project_profile(profile)
        self.assertIn("UNRESOLVED_DECISIONS_BLOCK_APPROVAL", {item["code"] for item in result["errors"]})

    def test_compile_is_byte_deterministic_and_linked(self):
        output = self.scratch / "assignments.json"
        first = compile_assignments(self.profile_path, self.assignment_path, "2026-09-07T12:00:00Z", output)
        first_bytes = output.read_bytes()
        second = compile_assignments(self.profile_path, self.assignment_path, "2026-09-07T12:00:00Z", output)
        self.assertEqual(first, second)
        self.assertEqual(first_bytes, output.read_bytes())
        self.assertEqual(first["generated_at"], "2026-09-07T12:00:00Z")
        self.assertTrue(verify_assignment_linkage(output)["valid"])

    def test_compile_canonicalizes_mapping_key_order(self):
        first_output = self.scratch / "assignments-first.json"
        second_output = self.scratch / "assignments-second.json"
        compile_assignments(self.profile_path, self.assignment_path, "2026-09-07T12:00:00Z", first_output)
        reordered = dict(reversed(list(self.assignment.items())))
        reordered["assignments"] = [dict(reversed(list(item.items()))) for item in self.assignment["assignments"]]
        reordered_path = self.scratch / "reordered-input.json"
        reordered_path.write_text(json.dumps(reordered), encoding="utf-8")
        compile_assignments(self.profile_path, reordered_path, "2026-09-07T12:00:00Z", second_output)
        self.assertEqual(first_output.read_bytes(), second_output.read_bytes())

    def test_changed_profile_invalidates_linkage(self):
        output = self.scratch / "assignments.json"
        compile_assignments(self.profile_path, self.assignment_path, "2026-09-07T12:00:00Z", output)
        self.profile["description"] = "Materially changed."
        self.profile_path.write_text(json.dumps(self.profile), encoding="utf-8")
        result = verify_assignment_linkage(output)
        self.assertIn("SOURCE_PROFILE_HASH_MISMATCH", {item["code"] for item in result["errors"]})

    def test_model_self_approval_and_observed_identity_are_rejected(self):
        document = copy.deepcopy(self.assignment)
        document["assignments"][0]["authority_scope"]["may_approve"] = True
        document["assignments"][0]["observed_model"] = "not-evidence"
        result = validate_assignment_manifest(document, self.profile)
        codes = {item["code"] for item in result["errors"]}
        self.assertIn("MODEL_APPROVAL_PROHIBITED", codes)
        self.assertIn("OBSERVED_IDENTITY_PROHIBITED", codes)

    def test_fallback_cannot_weaken_contract(self):
        document = copy.deepcopy(self.assignment)
        role = document["assignments"][0]
        role["acceptable_fallbacks"] = [{
            "fallback_id": "bad", "provider": "p", "model": "m", "capabilities": [],
            "data_classification_limit": "PUBLIC",
            "authority_scope": {"may_read": True, "may_write": True, "may_execute": False, "may_validate": False, "may_approve": False},
            "required_validators": [],
        }]
        result = validate_assignment_manifest(document, self.profile)
        codes = {item["code"] for item in result["errors"]}
        self.assertTrue({"FALLBACK_CAPABILITY_MISMATCH", "FALLBACK_VALIDATOR_WEAKENING", "FALLBACK_DATA_POLICY_MISMATCH", "FALLBACK_AUTHORITY_EXPANSION"}.issubset(codes))

    def test_unauthorized_write_path_is_rejected(self):
        document = copy.deepcopy(self.assignment)
        document["assignments"][0]["allowed_write_roots"] = [str(ROOT.parent / "outside")]
        result = validate_assignment_manifest(document, self.profile)
        self.assertIn("UNAUTHORIZED_WRITE_ROOT", {item["code"] for item in result["errors"]})

    def test_plaintext_secret_is_rejected_and_not_echoed(self):
        document = copy.deepcopy(self.assignment)
        document["assignments"][0]["extensions"] = {"api_key": "sk-proj-supersecret123"}
        result = validate_assignment_manifest(document, self.profile)
        rendered = json.dumps(result["errors"])
        self.assertIn("PLAINTEXT_CREDENTIAL", rendered)
        self.assertNotIn("supersecret123", rendered)

    def test_identity_comparison_preserves_unknown(self):
        identity = compare_identities(self.assignment["assignments"][0])
        self.assertEqual(identity["observed"]["state"], "UNKNOWN")
        self.assertIsNone(identity["resolved_matches_observed"])

    def test_cli_failure_is_nonzero(self):
        bad = self.scratch / "bad.json"
        bad.write_text("{}", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            exit_code = main(["project", "validate", str(bad)])
        self.assertNotEqual(exit_code, 0)
        self.assertFalse(json.loads(output.getvalue())["valid"])

    def test_compile_requires_approved_profile(self):
        self.profile["profile_status"] = "DECISION_REQUIRED"
        self.profile["provenance"]["approval_ref"] = None
        self.profile_path.write_text(json.dumps(self.profile), encoding="utf-8")
        with self.assertRaises(ProjectContractError) as caught:
            compile_assignments(self.profile_path, self.assignment_path, "2026-09-07T12:00:00Z")
        self.assertIn("PROFILE_NOT_APPROVED", {item["code"] for item in caught.exception.issues})

    def test_compile_rejects_implicit_timezone(self):
        with self.assertRaises(ProjectContractError) as caught:
            compile_assignments(self.profile_path, self.assignment_path, "2026-09-07T12:00:00")
        self.assertIn("INVALID_REFERENCE_TIME", {item["code"] for item in caught.exception.issues})

    def test_approved_profile_rejects_required_placeholder(self):
        profile = copy.deepcopy(self.profile)
        profile["display_name"] = "REQUIRED"
        result = validate_project_profile(profile)
        self.assertIn("UNRESOLVED_REQUIRED_VALUE", {item["code"] for item in result["errors"]})

    def test_stdlib_fallback_enforces_new_schema_keywords(self):
        original_import = __import__

        def without_jsonschema(name, *args, **kwargs):
            if name == "jsonschema":
                raise ImportError("simulated optional dependency absence")
            return original_import(name, *args, **kwargs)

        invalid = copy.deepcopy(self.profile)
        invalid["project_id"] = "Invalid Project ID"
        invalid["created_at"] = "2026-09-07T12:00:00"
        invalid["observability"]["observed_identity_state_values"] = [
            "VERIFIED", "UNKNOWN", "UNAVAILABLE", "MISMATCH", "MISMATCH",
        ]
        with mock.patch("builtins.__import__", side_effect=without_jsonschema):
            result = validate_project_profile(invalid)
        messages = "\n".join(item["message"] for item in result["errors"])
        self.assertIn("does not match pattern", messages)
        self.assertIn("date-time with timezone", messages)
        self.assertIn("more than 4 items", messages)
        self.assertIn("not unique", messages)


if __name__ == "__main__":
    unittest.main()
