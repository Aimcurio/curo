"""Protocol-integrity regression tests for the Curo harness."""

import json
import shutil
import sys
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
HARNESS_DIR = ROOT / "harness"
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

from curo_harness.core import resolve_within, safe_write_json, sha256_bytes, sha256_dict, sha256_file
from curo_harness.distill import distill_learning_candidate
from curo_harness.escalate import generate_hitl_packet
from curo_harness.replay import execute_replay
from curo_harness.run import execute_run
from curo_harness.validator import validate_curo_payload
from curo_harness.vocabularies import CANDIDATE_TYPES, RUN_STATUSES


class HarnessTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = ROOT / "tests" / "scratch"
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True)
        self.input_file = self.test_dir / "sample_input.txt"
        self.input_file.write_bytes(b"curo-deterministic-input-data\n")
        self.output_file = self.test_dir / "sample_output.txt"

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def run_copy(self, run_id: str = "RUN-TEST-001", **overrides):
        kwargs = {
            "executable": sys.executable,
            "args": ["-c", "from pathlib import Path; Path('sample_output.txt').write_bytes(Path('sample_input.txt').read_bytes().upper())"],
            "run_id": run_id,
            "inputs": ["sample_input.txt"],
            "outputs": ["sample_output.txt"],
            "evidence_dir": "evidence/runs",
            "cwd": str(self.test_dir),
        }
        kwargs.update(overrides)
        return execute_run(**kwargs)


class TestValidator(HarnessTestCase):
    def valid_provenance(self):
        return {
            "record_type": "provenance_record", "artifact_id": "A", "input_hash": "UNKNOWN",
            "output_hash": "UNKNOWN", "validator_result": "UNKNOWN", "owner": "harness",
            "created_at": "2026-09-07T00:00:00Z", "source_conversation_id": None,
            "source_note": None, "validation_errors": [], "diagnostic_reasons": [],
        }

    def test_nullable_union_type(self):
        payload = self.valid_provenance()
        valid, errors = validate_curo_payload(payload, "provenance-record")
        self.assertTrue(valid, errors)

    def test_relative_ref(self):
        manifest = {
            "manifest_type": "execution_replay_manifest", "artifact_id": "A", "version": "1",
            "executable": sys.executable, "args": [], "cwd": str(self.test_dir), "timeout_seconds": 1,
            "inputs": [], "expected_outputs": [], "expected_checks": [], "provenance": self.valid_provenance(),
        }
        valid, errors = validate_curo_payload(manifest, "execution-replay-manifest")
        self.assertTrue(valid, errors)

    def test_zero_dependency_fallback_handles_nullable_and_relative_ref(self):
        manifest = {
            "manifest_type": "execution_replay_manifest", "artifact_id": "A", "version": "1",
            "executable": sys.executable, "args": [], "cwd": str(self.test_dir), "timeout_seconds": 1,
            "inputs": [], "expected_outputs": [], "expected_checks": [], "provenance": self.valid_provenance(),
        }
        original_import = __import__

        def without_jsonschema(name, *args, **kwargs):
            if name == "jsonschema":
                raise ImportError("simulated optional dependency absence")
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=without_jsonschema):
            valid, errors = validate_curo_payload(manifest, "execution-replay-manifest")
        self.assertTrue(valid, errors)

    def test_enum_violation(self):
        payload = self.valid_provenance()
        payload["validator_result"] = "SUCCESS"
        valid, errors = validate_curo_payload(payload, "provenance-record")
        self.assertFalse(valid)
        self.assertTrue(errors)

    def test_missing_required_field(self):
        payload = self.valid_provenance()
        del payload["owner"]
        self.assertFalse(validate_curo_payload(payload, "provenance-record")[0])

    def test_additional_properties_violation(self):
        payload = self.valid_provenance()
        payload["unexpected"] = True
        self.assertFalse(validate_curo_payload(payload, "provenance-record")[0])


class TestRun(HarnessTestCase):
    def test_core_hashing(self):
        self.assertEqual(sha256_file(self.input_file), sha256_bytes(self.input_file.read_bytes()))
        self.assertEqual(len(sha256_dict({"key": "value"})), 64)

    def test_structured_run_and_artifacts_validate(self):
        result = self.run_copy()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["process_status"], "COMPLETE")
        self.assertEqual(self.output_file.read_bytes(), b"CURO-DETERMINISTIC-INPUT-DATA\n")
        pairs = (("provenance_file", "provenance-record"), ("run_record_file", "run-record"),
                 ("replay_manifest_file", "execution-replay-manifest"))
        for key, schema in pairs:
            payload = json.loads(Path(result[key]).read_text(encoding="utf-8"))
            valid, errors = validate_curo_payload(payload, schema)
            self.assertTrue(valid, errors)

    def test_missing_input_cannot_pass(self):
        result = self.run_copy(inputs=["missing.txt"])
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["process_status"], "NOT_STARTED")
        self.assertFalse(self.output_file.exists())

    def test_missing_expected_output_cannot_pass(self):
        result = self.run_copy(args=["-c", "print('no output')"])
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("REQUIRED_OUTPUT_MISSING:sample_output.txt", result["diagnostic_reasons"])

    def test_schema_invalid_run_artifact_is_blocked(self):
        real_validate = validate_curo_payload

        def reject_run(payload, schema_name):
            return (False, ["forced invalid run record"]) if schema_name == "run-record" else real_validate(payload, schema_name)

        with mock.patch("curo_harness.run.validate_curo_payload", side_effect=reject_run):
            result = self.run_copy()
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("forced invalid", " ".join(result["validation_errors"]))
        self.assertFalse((self.test_dir / "evidence" / "runs" / "RUN-TEST-001-run.json").exists())
        self.assertFalse((self.test_dir / "evidence" / "runs" / "RUN-TEST-001-provenance.json").exists())

    def test_secret_bearing_stdout_is_redacted(self):
        result = self.run_copy(args=["-c", "print('Authorization: Bearer secret-token-12345'); from pathlib import Path; Path('sample_output.txt').write_text('ok')"])
        record = json.loads(Path(result["run_record_file"]).read_text(encoding="utf-8"))
        self.assertTrue(record["redaction_applied"])
        self.assertNotIn("secret-token-12345", record["stdout_snippet"])

    def test_malicious_legacy_shell_syntax_is_not_executed(self):
        marker = self.test_dir / "should-not-exist.txt"
        result = execute_run(command=f"echo safe && echo bad > {marker.name}", run_id="RUN-MAL",
                             cwd=str(self.test_dir), evidence_dir="evidence/runs")
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(marker.exists())

    def test_timeout_records_timed_out(self):
        result = self.run_copy(args=["-c", "import time; time.sleep(3)"], outputs=[], timeout_seconds=0.2)
        self.assertEqual(result["status"], "TIMED_OUT")
        record = json.loads(Path(result["run_record_file"]).read_text(encoding="utf-8"))
        self.assertEqual(record["process_status"], "TIMED_OUT")
        self.assertIsInstance(record["execution"]["timeout_termination_succeeded"], bool)

    @unittest.skipUnless(sys.platform == "win32", "Windows process-tree assertion")
    def test_windows_timeout_terminates_child_tree(self):
        child_code = "import time; from pathlib import Path; time.sleep(1); Path('orphan-marker.txt').write_text('orphan')"
        parent_code = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{child_code!r}]); time.sleep(3)"
        result = self.run_copy(args=["-c", parent_code], outputs=[], timeout_seconds=0.2)
        time.sleep(1.3)
        self.assertEqual(result["status"], "TIMED_OUT")
        self.assertTrue(result["diagnostic_reasons"] == ["PROCESS_TIMED_OUT"])
        self.assertFalse((self.test_dir / "orphan-marker.txt").exists())

    def test_every_emitted_run_status_is_schema_accepted(self):
        results = [
            self.run_copy("RUN-PASS"),
            self.run_copy("RUN-FAIL", args=["-c", "raise SystemExit(2)"], outputs=[]),
            self.run_copy("RUN-UNKNOWN", inputs=["missing.txt"], outputs=[]),
            self.run_copy("RUN-TIMEOUT", args=["-c", "import time; time.sleep(3)"], outputs=[], timeout_seconds=0.2),
        ]
        self.assertEqual({item["status"] for item in results}, set(RUN_STATUSES))
        for result in results:
            record = json.loads(Path(result["run_record_file"]).read_text(encoding="utf-8"))
            self.assertTrue(validate_curo_payload(record, "run-record")[0])


class TestReplay(HarnessTestCase):
    def test_execution_replay_uses_structured_argv(self):
        run = self.run_copy()
        replay = execute_replay(run["replay_manifest_file"], cwd=str(self.test_dir))
        self.assertEqual(replay["status"], "REPLAY_VERIFIED")

    def test_artifact_verification_manifest_requires_no_command(self):
        provenance = TestValidator.valid_provenance(self)
        manifest = {
            "manifest_type": "artifact_verification_manifest", "artifact_id": "VERIFY-1", "version": "1.0.0",
            "artifacts": [{"path": "sample_input.txt", "sha256": sha256_file(self.input_file), "schema": None}],
            "expected_checks": ["hash"], "provenance": provenance,
        }
        path = self.test_dir / "verification.json"
        safe_write_json(path, manifest)
        result = execute_replay(str(path), cwd=str(self.test_dir))
        self.assertEqual(result["status"], "VERIFIED")

    def test_replay_path_escape_is_rejected(self):
        outside = self.test_dir.parent / "outside.json"
        safe_write_json(outside, {})
        try:
            result = execute_replay(str(outside), cwd=str(self.test_dir))
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("escapes authorized boundary", result["error"])
        finally:
            outside.unlink(missing_ok=True)


class TestPathsAndPersistence(HarnessTestCase):
    def test_parent_escape(self):
        with self.assertRaises(ValueError):
            resolve_within(self.test_dir, "../outside")

    def test_absolute_external_path(self):
        with self.assertRaises(ValueError):
            resolve_within(self.test_dir, self.test_dir.parent / "outside")

    def test_sibling_prefix_collision(self):
        sibling = self.test_dir.with_name(self.test_dir.name + "-evil")
        with self.assertRaises(ValueError):
            resolve_within(self.test_dir, sibling)

    def test_valid_nested_path(self):
        self.assertEqual(resolve_within(self.test_dir, "a/b"), (self.test_dir / "a/b").resolve())

    def test_atomic_write_cleans_temporary_state(self):
        target = self.test_dir / "atomic.json"
        safe_write_json(target, {"state": "first"})
        safe_write_json(target, {"state": "second"})
        self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"state": "second"})
        self.assertEqual(list(self.test_dir.glob(".atomic.json.*")), [])

    @unittest.skipUnless(sys.platform == "win32", "Windows drive-boundary assertion")
    def test_windows_drive_boundary(self):
        with self.assertRaises(ValueError):
            resolve_within(self.test_dir, "Z:/external")


class TestDistillAndEscalation(HarnessTestCase):
    def test_all_five_candidate_types_are_accepted_and_valid(self):
        for candidate_type in CANDIDATE_TYPES:
            result = distill_learning_candidate(
                candidate_id=f"LC-{candidate_type}", source_run_id="RUN-1", proposed_type=candidate_type,
                title="Candidate", summary="Evidence-backed proposal", output_dir=str(self.test_dir / "learning"),
            )
            self.assertEqual(result["status"], "PROPOSED")
            payload = json.loads(Path(result["file"]).read_text(encoding="utf-8"))
            self.assertTrue(validate_curo_payload(payload, "learning-candidate")[0])

    def test_hitl_packet_validates_before_persistence(self):
        result = generate_hitl_packet(
            packet_id="HITL-1", project_id="project", review_id="review",
            finding_description="Human authority required", output_dir=str(self.test_dir / "review"),
        )
        self.assertEqual(result["status"], "ESCALATED")
        payload = json.loads(Path(result["file"]).read_text(encoding="utf-8"))
        self.assertTrue(validate_curo_payload(payload, "hitl-packet")[0])

    def test_invalid_hitl_is_not_persisted(self):
        with mock.patch("curo_harness.escalate.validate_and_write_json", return_value=(False, ["invalid packet"])):
            result = generate_hitl_packet(
                packet_id="HITL-BAD", project_id="project", review_id="review",
                finding_description="bad", output_dir=str(self.test_dir / "review"),
            )
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse((self.test_dir / "review" / "HITL-BAD.json").exists())


class TestSourceHygiene(unittest.TestCase):
    def test_python_sources_are_utf8_without_bom(self):
        offenders = []
        for path in ROOT.rglob("*.py"):
            if any(part in {".git", "__pycache__"} for part in path.parts):
                continue
            data = path.read_bytes()
            if data.startswith(b"\xef\xbb\xbf"):
                offenders.append(str(path.relative_to(ROOT)))
            data.decode("utf-8")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
