"""Repository-level regression tests for project profiles and migrations."""

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
HARNESS_DIR = ROOT / "harness"
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

from curo_harness.assignments import (  # noqa: E402
    compare_identities,
    compile_assignments,
    validate_assignment_manifest,
    verify_assignment_linkage,
)
from curo_harness.core import resolve_within  # noqa: E402
from curo_harness.projects import (  # noqa: E402
    ProjectContractError,
    canonical_profile_hash,
    load_structured_file,
    validate_project_profile,
)
from curo_harness.validator import validate_curo_payload  # noqa: E402


def write_approval_record(profile, directory, *, approval_id="PROFILE-APPROVAL", actor_id="human-requester", assignment_ids=None):
    record = {
        "artifact_type": "curo_human_approval_record", "artifact_version": "1.0.0",
        "approval_id": approval_id, "project_id": profile["project_id"], "decision": "APPROVE",
        "approved_profile_hash": canonical_profile_hash(profile),
        "approved_assignment_ids": list(assignment_ids or []),
        "actor": {"actor_type": "HUMAN", "actor_id": actor_id},
        "recorded_at": "2026-09-07T00:00:00Z", "recorded_by": "harness",
        "evidence_source": "authorized test fixture",
    }
    path = directory / f"{approval_id.lower()}.json"
    path.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
    return {
        "artifact_path": path.relative_to(ROOT).as_posix(),
        "artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "approval_id": approval_id,
    }


class ProjectContractIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_structured_file(ROOT / "projects/kayo/project.yaml")
        cls.assignments = json.loads((ROOT / "projects/kayo/llm-assignments.json").read_text(encoding="utf-8"))

    def test_profile_missing_id_and_undeclared_property_are_rejected(self):
        missing = copy.deepcopy(self.profile)
        missing.pop("project_id")
        extra = copy.deepcopy(self.profile)
        extra["undeclared"] = True
        self.assertFalse(validate_project_profile(missing)["valid"])
        self.assertFalse(validate_project_profile(extra)["valid"])

    def test_profile_plaintext_credential_is_rejected(self):
        profile = copy.deepcopy(self.profile)
        profile["extensions"] = {"api_key": "not-allowed"}
        codes = {item["code"] for item in validate_project_profile(profile)["errors"]}
        self.assertIn("PLAINTEXT_CREDENTIAL_FIELD", codes)

    def test_duplicate_assignment_and_role_ids_are_rejected(self):
        document = copy.deepcopy(self.assignments)
        duplicate = copy.deepcopy(document["assignments"][0])
        document["assignments"].append(duplicate)
        codes = {item["code"] for item in validate_assignment_manifest(document, self.profile)["errors"]}
        self.assertIn("DUPLICATE_ASSIGNMENT_ID", codes)
        self.assertIn("DUPLICATE_ROLE_ID", codes)

    def test_resolved_or_preferred_identity_never_becomes_observed(self):
        assignment = copy.deepcopy(self.assignments["assignments"][0])
        assignment.update({
            "preferred_provider": "desired-provider",
            "preferred_model": "desired-model",
            "resolved_identity_state": "RESOLVED",
            "resolved_provider": "resolved-provider",
            "resolved_model": "resolved-model",
        })
        comparison = compare_identities(assignment)
        self.assertEqual(comparison["observed"], {"state": "UNKNOWN", "provider": None, "model": None})
        self.assertNotEqual(comparison["desired"], comparison["observed"])
        self.assertNotEqual(comparison["resolved"], comparison["observed"])

        forged = compare_identities(assignment, {
            "state": "VERIFIED", "provider": "configured", "model": "configured",
        })
        self.assertEqual(forged["observed"]["state"], "UNKNOWN")
        self.assertFalse(forged["observed_evidence_valid"])

    def test_verified_observed_identity_requires_trusted_valid_run_record(self):
        assignment = copy.deepcopy(self.assignments["assignments"][0])
        assignment.update({
            "resolved_identity_state": "RESOLVED", "resolved_provider": "observed-provider",
            "resolved_model": "observed-model", "assignment_status": "RESOLVED",
        })
        with tempfile.TemporaryDirectory(dir=ROOT / "tests", prefix="identity-evidence-") as temporary:
            temp = Path(temporary)
            evidence_path = temp / "adapter-response-metadata.json"
            evidence_path.write_text('{"provider":"observed-provider","model":"observed-model"}\n', encoding="utf-8")
            evidence_ref = evidence_path.relative_to(ROOT).as_posix()
            identity = {
                "state": "VERIFIED", "provider": "observed-provider", "model": "observed-model",
                "evidence_source": evidence_ref,
                "evidence_sha256": hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
            }
            provenance = {
                "record_type": "provenance_record", "artifact_id": "RUN-EXAMPLE-001",
                "input_hash": "UNKNOWN", "output_hash": "UNKNOWN", "validator_result": "PASS",
                "owner": "harness", "created_at": "2026-09-07T00:00:00Z",
                "source_conversation_id": None, "source_note": "Harness-bound observed identity.",
                "validation_errors": [], "diagnostic_reasons": [], "observed_identity": identity,
            }
            provenance_path = temp / "provenance.json"
            provenance_path.write_text(json.dumps(provenance), encoding="utf-8")
            run = load_structured_file(ROOT / "observability/sample-run-record.yaml")
            run["project_id"] = "kayo"
            run["role"] = assignment["role_id"]
            run["observed_identity"] = identity
            run["evidence_locators"] = [evidence_ref, provenance_path.relative_to(ROOT).as_posix()]
            run_path = temp / "run.json"
            run_path.write_text(json.dumps(run), encoding="utf-8")

            comparison = compare_identities(assignment, run_path, expected_project_id="kayo")
            self.assertTrue(comparison["observed_evidence_valid"])
            self.assertEqual(comparison["observed"]["state"], "VERIFIED")
            self.assertTrue(comparison["resolved_matches_observed"])

            run["provenance_source"] = "MODEL_SELF_REPORT"
            run_path.write_text(json.dumps(run), encoding="utf-8")
            untrusted = compare_identities(assignment, run_path, expected_project_id="kayo")
            self.assertEqual(untrusted["observed"]["state"], "UNKNOWN")
            self.assertFalse(untrusted["observed_evidence_valid"])

            run["provenance_source"] = "HARNESS_CLI"
            run["project_id"] = "different-project"
            run_path.write_text(json.dumps(run), encoding="utf-8")
            cross_project = compare_identities(assignment, run_path, expected_project_id="kayo")
            self.assertEqual(cross_project["observed"]["state"], "UNKNOWN")
            self.assertFalse(cross_project["observed_evidence_valid"])

    def test_resolved_status_and_identity_must_agree(self):
        document = copy.deepcopy(self.assignments)
        document["assignments"][0]["assignment_status"] = "RESOLVED"
        codes = {item["code"] for item in validate_assignment_manifest(document, self.profile)["errors"]}
        self.assertIn("RESOLVED_STATUS_IDENTITY_MISMATCH", codes)

    def test_approved_assignment_requires_structured_human_actor(self):
        document = copy.deepcopy(self.assignments)
        document["approval_status"] = "APPROVED"
        document["approval_ref"] = "APPROVAL-1"
        document["unresolved_assignments"] = []
        document["provenance"]["approval_actor"] = {"actor_type": "HUMAN", "actor_id": "same-model"}
        for role in document["assignments"]:
            role["assignment_status"] = "APPROVED"
        result = validate_assignment_manifest(document, self.profile)
        self.assertFalse(result["valid"])
        rendered = json.dumps(result["errors"])
        self.assertIn("APPROVAL_ACTOR_UNAUTHORIZED", rendered)

    def test_approved_assignment_requires_hash_bound_approval_evidence(self):
        document = copy.deepcopy(self.assignments)
        document["approval_status"] = "APPROVED"
        document["unresolved_assignments"] = []
        document["provenance"]["approval_actor"] = {"actor_type": "HUMAN", "actor_id": "human-approver"}
        for role in document["assignments"]:
            role["assignment_status"] = "APPROVED"
            role["preferred_provider"] = "approved-provider"
            role["preferred_model"] = "approved-model"
        document["approval_ref"] = {
            "artifact_path": "tests/missing-approval.json",
            "artifact_sha256": "0" * 64,
            "approval_id": "ASSIGNMENT-APPROVAL",
        }
        missing = validate_assignment_manifest(document, self.profile)
        self.assertIn("APPROVAL_EVIDENCE_MISSING", {item["code"] for item in missing["errors"]})
        with tempfile.TemporaryDirectory(dir=ROOT / "tests", prefix="approval-evidence-") as temporary:
            temp = Path(temporary)
            document["approval_ref"] = write_approval_record(
                self.profile, temp, approval_id="ASSIGNMENT-APPROVAL",
                actor_id="human-approver",
                assignment_ids=[item["assignment_id"] for item in document["assignments"]],
            )
            approved = validate_assignment_manifest(document, self.profile)
            self.assertTrue(approved["valid"], approved["errors"])

    def test_unknown_desired_assignment_must_remain_declared_unresolved(self):
        document = copy.deepcopy(self.assignments)
        document["unresolved_assignments"] = []
        codes = {item["code"] for item in validate_assignment_manifest(document, self.profile)["errors"]}
        self.assertIn("UNRESOLVED_ROLE_NOT_DECLARED", codes)

    def test_realpath_boundary_check_rejects_junction_escape(self):
        boundary = str(ROOT / "tests" / "authorized")
        candidate = str(ROOT / "tests" / "authorized" / "junction" / "file.txt")
        external = str(ROOT.parent / "outside" / "file.txt")
        realpath = __import__("os").path.realpath

        def junction_aware(path, *args, **kwargs):
            normalized = str(path)
            if "junction" in normalized:
                return external
            return realpath(normalized)

        with mock.patch("curo_harness.core.os.path.realpath", side_effect=junction_aware):
            with self.assertRaises(ValueError):
                resolve_within(boundary, candidate)

    def test_assignment_source_profile_cannot_escape_repository(self):
        document = copy.deepcopy(self.assignments)
        document["source_project_profile"] = "../outside/project.yaml"
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as temporary:
            manifest = Path(temporary) / "assignments.json"
            manifest.write_text(json.dumps(document), encoding="utf-8")
            result = verify_assignment_linkage(manifest)
        self.assertIn("SOURCE_PROFILE_PATH_UNAUTHORIZED", {item["code"] for item in result["errors"]})

    def test_compiler_rejects_external_inputs_before_persistence(self):
        with tempfile.TemporaryDirectory(prefix="curo-external-input-") as temporary:
            external = Path(temporary)
            profile_path = external / "project.yaml"
            assignment_path = external / "assignments.json"
            profile_path.write_text(json.dumps(self.profile), encoding="utf-8")
            assignment_path.write_text(json.dumps(self.assignments), encoding="utf-8")
            output = ROOT / "tests" / "external-input-output.json"
            output.unlink(missing_ok=True)
            with self.assertRaises(ProjectContractError) as caught:
                compile_assignments(profile_path, assignment_path, "2026-09-07T00:00:00Z", output)
            self.assertIn("COMPILER_INPUT_PATH_UNAUTHORIZED", {item["code"] for item in caught.exception.issues})
            self.assertFalse(output.exists())

    def test_schema_invalid_assignment_is_not_persisted(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as temporary:
            temp = Path(temporary)
            profile = copy.deepcopy(load_structured_file(ROOT / "templates/project-profile.yaml"))
            profile.update({
                "project_id": "persistence-test", "display_name": "Persistence Test",
                "description": "Test validation before persistence.", "profile_status": "APPROVED",
                "actual_project_roots": [str(temp)],
            })
            profile["execution_environment"]["workspace_boundary"] = str(temp)
            profile["objectives"]["primary"] = "Test persistence."
            profile["architecture"]["summary"] = "Test fixture."
            profile["storage_policy"]["retention"] = "Test lifetime."
            profile["open_decisions"] = []
            profile["provenance"]["approval_ref"] = write_approval_record(profile, temp)
            profile_path = temp / "project.yaml"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            assignment = json.loads((ROOT / "templates/llm-assignments.json").read_text(encoding="utf-8"))
            assignment["assignments"][0].pop("purpose")
            assignment["assignments"][0]["allowed_project_roots"] = [str(temp)]
            input_path = temp / "input.json"
            input_path.write_text(json.dumps(assignment), encoding="utf-8")
            output = ROOT / "tests" / "invalid-persistence-output.json"
            output.unlink(missing_ok=True)
            with self.assertRaises(ProjectContractError):
                compile_assignments(profile_path, input_path, "2026-09-07T00:00:00Z", output)
            self.assertFalse(output.exists())

    def test_material_change_changes_profile_hash(self):
        changed = copy.deepcopy(self.profile)
        changed["description"] += " Material change."
        self.assertNotEqual(canonical_profile_hash(self.profile), canonical_profile_hash(changed))

    def test_compiler_does_not_consult_implicit_clock(self):
        import curo_harness.assignments as assignment_module

        class NoClock(assignment_module.datetime.datetime):
            @classmethod
            def now(cls, *args, **kwargs):
                raise AssertionError("implicit clock access is prohibited")

            @classmethod
            def utcnow(cls):
                raise AssertionError("implicit clock access is prohibited")

        with tempfile.TemporaryDirectory(dir=ROOT / "tests") as temporary:
            temp = Path(temporary)
            profile = copy.deepcopy(load_structured_file(ROOT / "templates/project-profile.yaml"))
            profile.update({"project_id": "clock-test", "display_name": "Clock Test", "description": "Clock independence.", "profile_status": "APPROVED", "actual_project_roots": [str(temp)]})
            profile["execution_environment"]["workspace_boundary"] = str(temp)
            profile["objectives"]["primary"] = "Prove clock independence."
            profile["architecture"]["summary"] = "Test fixture."
            profile["storage_policy"]["retention"] = "Test lifetime."
            profile["open_decisions"] = []
            profile["provenance"]["approval_ref"] = write_approval_record(profile, temp)
            profile_path = temp / "project.yaml"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")
            assignment = json.loads((ROOT / "templates/llm-assignments.json").read_text(encoding="utf-8"))
            assignment["assignments"][0]["allowed_project_roots"] = [str(temp)]
            input_path = temp / "input.json"
            input_path.write_text(json.dumps(assignment), encoding="utf-8")
            with mock.patch.object(assignment_module.datetime, "datetime", NoClock):
                result = compile_assignments(profile_path, input_path, "2026-09-07T01:02:03Z")
            self.assertEqual(result["generated_at"], "2026-09-07T01:02:03Z")

    def test_all_real_projects_validate_and_link(self):
        for folder in sorted(path for path in (ROOT / "projects").iterdir() if path.is_dir()):
            with self.subTest(project=folder.name):
                profile = validate_project_profile(folder / "project.yaml")
                linkage = verify_assignment_linkage(folder / "llm-assignments.json")
                self.assertTrue(profile["valid"], profile["errors"])
                self.assertTrue(linkage["valid"], linkage["errors"])
                self.assertEqual(profile["profile"]["project_id"], folder.name)

    def test_kayo_roles_and_authority_boundaries_remain_distinct(self):
        roles = {item["role_id"]: item for item in self.assignments["assignments"]}
        required = {"strategist", "builder", "critic-reviewer", "deterministic-validator", "local-private-model-lane", "human-approver"}
        self.assertTrue(required.issubset(roles))
        for role in roles.values():
            if role["role_type"] == "MODEL":
                self.assertFalse(role["authority_scope"]["may_approve"])
                self.assertEqual(role["resolved_identity_state"], "UNRESOLVED")
                self.assertIsNone(role["resolved_provider"])
                self.assertIsNone(role["resolved_model"])
        components = {item["component_id"]: set(item["authority"]) for item in self.profile["components"]}
        expected = {"second-brain": "KNOW", "kayo": "COORDINATE", "control-room": "OBSERVE", "visual-data-node": "UNDERSTAND", "executor": "ACT", "validator": "ESTABLISH EVIDENCE", "human": "AUTHORIZE"}
        for component, authority in expected.items():
            self.assertIn(authority, components[component])
        self.assertTrue(components["control-room"].isdisjoint({"KNOW", "ACT", "AUTHORIZE"}))
        self.assertTrue(components["visual-data-node"].isdisjoint({"KNOW", "ACT", "AUTHORIZE"}))

    def test_historical_migrations_preserve_bytes_and_classification(self):
        pairs = (
            ("manifests/spacetime-sim-learning-record.json", "projects/spacetime/evidence/spacetime-sim-learning-record.json"),
            ("manifests/math-node-v0.1-replay.json", "projects/math-node/evidence/math-node-v0.1-replay.json"),
        )
        for source, copy_path in pairs:
            self.assertEqual((ROOT / source).read_bytes(), (ROOT / copy_path).read_bytes())
        replacement = json.loads((ROOT / "projects/math-node/evidence/math-node-v0.1-artifact-verification.json").read_text(encoding="utf-8"))
        self.assertEqual(replacement["manifest_type"], "artifact_verification_manifest")
        self.assertTrue(validate_curo_payload(replacement, "artifact-verification-manifest")[0])
        self.assertTrue(set(replacement).isdisjoint({"executable", "command", "args", "cwd", "timeout_seconds"}))
        for path in sorted((ROOT / "projects").glob("*/evidence/*relocation-record.json")):
            relocation = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(validate_curo_payload(relocation, "project-relocation-record")[0])
            self.assertEqual(relocation["preservation_status"], "BYTE_IDENTICAL")

    def test_pdf_candidates_split_without_rewriting_original(self):
        original = ROOT / "learning/candidates/LEARN-20260907-PDF-RESTORATION.yaml"
        self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(), "4e0751651e1e5c887183789fd50a907fe516c7419547a9e1271fe96c4bed1b17")
        candidates = [
            load_structured_file(ROOT / "learning/candidates/LEARN-20260907-PDF-RESTORATION-SKILL.yaml"),
            load_structured_file(ROOT / "learning/candidates/LEARN-20260907-PDF-RESTORATION-ANTI-PATTERN.yaml"),
        ]
        self.assertEqual({item["candidate_type"] for item in candidates}, {"skill", "anti_pattern"})
        for candidate in candidates:
            self.assertEqual(candidate["status"], "PROPOSED")
            self.assertTrue(validate_curo_payload(candidate, "learning-candidate")[0])

    def test_preexisting_agent_evidence_is_unchanged(self):
        evidence_root = ROOT / "evidence/historical-agent-runs"
        manifest = json.loads((evidence_root / "evidence-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["legacy_inventory_sha256"], "8b81449bd3c5dad13f9cbf26f11adb6ae602d8fb41567b5ca83f6c98a031fc0b")
        self.assertEqual(manifest["inventory_sha256"], "7c896325c8bce7ad3e653f8052d693e06766a60f188bccd69684c060bbdb895e")
        records = []
        total_bytes = 0
        for path in sorted(evidence_root.rglob("*")):
            if path.is_file() and path.name not in {"README.md", "evidence-manifest.json"}:
                relative = path.relative_to(ROOT).as_posix()
                content = path.read_bytes()
                total_bytes += len(content)
                records.append(f"{relative} {hashlib.sha256(content).hexdigest()}\n")
        if not records:
            return
        inventory = hashlib.sha256("".join(records).encode("utf-8")).hexdigest()
        self.assertEqual(len(records), manifest["file_count"])
        self.assertEqual(total_bytes, manifest["total_bytes"])
        self.assertEqual(inventory, manifest["inventory_sha256"])

    def test_archived_architecture_hash_is_preserved(self):
        archived = ROOT / "docs/audits/2026-09-07-pre-remediation-architecture.md"
        expected = "09ddf0dea36fd05208855baa7c471a752eb297d7abbcdb76faad708712cf1bae"
        self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(), expected)
        self.assertIn(expected, (ROOT / "docs/audits/2026-09-07-pre-remediation-architecture.sha256").read_text(encoding="utf-8"))
        self.assertIn("pre-remediation", (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8").lower())

    def test_repository_validator_detects_profile_hash_drift(self):
        with tempfile.TemporaryDirectory(prefix="curo-validator-mutation-") as temporary:
            copy_root = Path(temporary) / "curo"
            shutil.copytree(
                ROOT,
                copy_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "scratch", "project-scratch"),
            )
            assignment_path = copy_root / "projects/kayo/llm-assignments.json"
            document = json.loads(assignment_path.read_text(encoding="utf-8"))
            document["source_profile_hash"] = "sha256:" + ("0" * 64)
            assignment_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(copy_root / "scripts/validate_curo.py")],
                cwd=copy_root,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SOURCE_PROFILE_HASH_MISMATCH", result.stdout)


if __name__ == "__main__":
    unittest.main()
