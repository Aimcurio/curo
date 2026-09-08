"""Adversarial regression tests for root and scoped registry authority."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScopedRegistryIntegrityTests(unittest.TestCase):
    def _copy_repository(self, temporary: str) -> Path:
        target = Path(temporary) / "curo"
        shutil.copytree(
            ROOT,
            target,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "scratch", "project-scratch"),
        )
        return target

    def _validate(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(root / "scripts/validate_curo.py")],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_clean_scoped_registry_passes(self):
        result = self._validate(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_undeclared_file_inside_scope_fails(self):
        with tempfile.TemporaryDirectory(prefix="curo-scoped-extra-") as temporary:
            root = self._copy_repository(temporary)
            extra = root / "skills/goal-driven-deep-research/undeclared.md"
            extra.write_text("not registered\n", encoding="utf-8")
            result = self._validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("file in scoped registry boundary is undeclared", result.stdout)

    def test_duplicate_authoritative_path_across_registries_fails(self):
        with tempfile.TemporaryDirectory(prefix="curo-scoped-duplicate-") as temporary:
            root = self._copy_repository(temporary)
            registry = root / "registry/registry.yaml"
            registry.write_text(
                registry.read_text(encoding="utf-8")
                + "\n  - id: invalid-duplicate-skill\n"
                + "    path: skills/goal-driven-deep-research/SKILL.md\n"
                + "    source: test\n"
                + "    type: skill\n"
                + "    version: 1.0.0\n"
                + "    owner: harness\n"
                + "    status: active\n"
                + "    updated_at: 2026-09-08\n"
                + "    authoritative: true\n",
                encoding="utf-8",
            )
            result = self._validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("artifact path is authoritative in more than one registry", result.stdout)

    def test_unreferenced_registry_shard_fails(self):
        with tempfile.TemporaryDirectory(prefix="curo-scoped-orphan-") as temporary:
            root = self._copy_repository(temporary)
            shutil.copy2(root / "registry/deep-research.yaml", root / "registry/orphan.yaml")
            result = self._validate(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scoped registry is not declared in project.yaml", result.stdout)


if __name__ == "__main__":
    unittest.main()
