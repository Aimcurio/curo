"""Run dependency-free integrity checks for the Curo foundation package."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACT_IDS = {
    "beginner-guide",
    "core-identity",
    "architecture-drift-check",
    "architecture-layers",
    "framework-capture-anti-patterns",
    "model-package-design-skill",
    "architecture-review-agent",
    "operating-standard",
    "addendum-a",
    "addendum-b-protocol-integrity",
    "gaps-and-roadmap",
    "ownership-policy",
    "precedence-policy",
    "validation-policy",
    "project-kickoff-schema",
    "provenance-record-schema",
    "execution-replay-manifest-schema",
    "artifact-verification-manifest-schema",
    "anti-patterns",
    "adapter-contract",
    "harness-contract",
    "provenance-sample",
    "execution-replay-manifest-template",
    "artifact-verification-manifest-template",
    "project-kickoff-template-human",
    "project-kickoff-template-machine",
    "curo-validation-script",
    "observability-contract",
    "observability-run-record-template",
    "observability-run-index-template",
    "observability-run-record-schema",
    "observability-run-event-schema",
    "exception-review-protocol",
    "review-findings-template",
    "hitl-packet-template",
    "review-findings-schema",
    "hitl-packet-schema",
    "learning-distillation-protocol",
    "learning-candidate-template",
    "promotion-record-template",
    "learning-candidate-schema",
    "promotion-record-schema",
    "observability-run-record-sample",
    "observability-run-event-sample",
    "project-profile-schema",
    "llm-assignments-schema",
    "project-relocation-record-schema",
    "project-profile-template",
    "llm-assignments-template",
    "projects-index",
    "kayo-project-profile",
    "kayo-llm-assignments",
    "spacetime-project-profile",
    "spacetime-llm-assignments",
    "math-node-project-profile",
    "math-node-llm-assignments",
    "human-approval-record-schema",
    "scoped-registry-schema",
    "historical-agent-evidence-manifest-schema",
    "deep-research-registry",
    "agent-evidence-index",
    "agent-evidence-manifest",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_required_files(errors: list[str]) -> None:
    registry = ROOT / "registry/registry.yaml"
    required = ["README.md", "project.yaml", "registry/registry.yaml"]
    required.extend(re.findall(r"^    path:\s*(\S+)", registry.read_text(encoding="utf-8"), re.MULTILINE))
    for relative in required:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")


def check_json_schemas(errors: list[str]) -> None:
    for path in sorted(ROOT.glob("*/*.schema.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"invalid JSON schema {path.relative_to(ROOT)}: {exc}")


def check_registry(errors: list[str]) -> None:
    path = ROOT / "registry/registry.yaml"
    text = path.read_text(encoding="utf-8")
    entry_blocks = re.split(r"(?=^  - id: )", text, flags=re.MULTILINE)[1:]
    if not entry_blocks:
        fail(errors, "registry contains no artifact entries")
        return

    required_metadata = ("path:", "source:", "type:", "version:", "owner:", "status:", "updated_at:", "authoritative:")
    id_values = re.findall(r"^  - id:\s*(\S+)", text, re.MULTILINE)
    ids = set(id_values)
    for duplicate in sorted({value for value in id_values if id_values.count(value) > 1}):
        fail(errors, f"registry contains duplicate artifact ID: {duplicate}")
    path_values = re.findall(r"^    path:\s*(\S+)", text, re.MULTILINE)
    for duplicate in sorted({value for value in path_values if path_values.count(value) > 1}):
        fail(errors, f"registry contains duplicate artifact path: {duplicate}")
    for missing_id in sorted(EXPECTED_ARTIFACT_IDS - ids):
        fail(errors, f"registry missing expected artifact: {missing_id}")
    for block in entry_blocks:
        first_line = block.splitlines()[0]
        for field in required_metadata:
            if not re.search(rf"^    {re.escape(field)}", block, re.MULTILINE):
                fail(errors, f"registry entry {first_line!r} lacks {field}")
        match = re.search(r"^    path:\s*(\S+)", block, re.MULTILINE)
        if match and not (ROOT / match.group(1)).is_file():
            fail(errors, f"registry path does not exist: {match.group(1)}")


def _scoped_registry_declarations() -> list[tuple[str, str]]:
    project = (ROOT / "project.yaml").read_text(encoding="utf-8")
    block = re.search(r"^    scoped:\s*\n((?:^      \S.*(?:\n|$))*)", project, re.MULTILINE)
    if not block:
        return []
    return re.findall(r"^      ([a-z0-9_]+):\s*(\S+)", block.group(1), re.MULTILINE)


def _scoped_entry_blocks(text: str) -> list[str]:
    match = re.search(r"^artifacts:\s*\n(.*?)(?=^\S|\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    return re.split(r"(?=^  - id: )", match.group(1), flags=re.MULTILINE)[1:]


def check_scoped_registries(errors: list[str]) -> None:
    declarations = _scoped_registry_declarations()
    names = [name for name, _ in declarations]
    paths = [path for _, path in declarations]
    for duplicate in sorted({value for value in names if names.count(value) > 1}):
        fail(errors, f"project.yaml declares duplicate scoped registry name: {duplicate}")
    for duplicate in sorted({value for value in paths if paths.count(value) > 1}):
        fail(errors, f"project.yaml declares duplicate scoped registry path: {duplicate}")

    declared = set(paths)
    discovered = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "registry").glob("*.yaml")
        if path.name != "registry.yaml"
    }
    for relative in sorted(discovered - declared):
        fail(errors, f"scoped registry is not declared in project.yaml: {relative}")
    for relative in sorted(declared - discovered):
        fail(errors, f"declared scoped registry does not exist: {relative}")

    root_text = (ROOT / "registry/registry.yaml").read_text(encoding="utf-8")
    root_ids = set(re.findall(r"^  - id:\s*(\S+)", root_text, re.MULTILINE))
    root_paths = set(re.findall(r"^    path:\s*(\S+)", root_text, re.MULTILINE))
    seen_ids = set(root_ids)
    seen_paths = set(root_paths)
    required_top = ("registry_version", "registry_id", "scope", "owner", "updated_at", "status")
    required_entry = ("id", "path", "type", "version", "owner", "status", "authoritative")

    for relative in paths:
        if relative not in root_paths:
            fail(errors, f"scoped registry is not registered in root registry: {relative}")
        shard_path = ROOT / relative
        if not shard_path.is_file():
            continue
        text = shard_path.read_text(encoding="utf-8")
        values = {}
        for field in required_top:
            match = re.search(rf"^{field}:\s*([^\s#]+)", text, re.MULTILINE)
            values[field] = match.group(1).strip("'\"") if match else None
            if values[field] is None:
                fail(errors, f"scoped registry {relative} lacks top-level {field}")
        scope = values.get("scope")
        if scope and (scope.startswith(("/", "\\")) or "\\" in scope or ".." in scope.split("/")):
            fail(errors, f"scoped registry {relative} has unsafe scope: {scope}")

        module_match = re.search(r"^module:\s*\n(.*?)(?=^\S|\Z)", text, re.MULTILINE | re.DOTALL)
        blocks = [(module_match.group(1), "  ")] if module_match else []
        if not module_match:
            fail(errors, f"scoped registry {relative} lacks module entry")
        artifact_blocks = _scoped_entry_blocks(text)
        if not artifact_blocks:
            fail(errors, f"scoped registry {relative} contains no artifact entries")
        blocks.extend((block, "    ") for block in artifact_blocks)

        shard_ids: list[str] = []
        shard_paths: list[str] = []
        for block, indent in blocks:
            fields = {}
            for field in required_entry:
                prefix = "  - " if field == "id" and indent == "    " else indent
                match = re.search(rf"^{re.escape(prefix)}{field}:\s*([^\s#]+)", block, re.MULTILINE)
                fields[field] = match.group(1).strip("'\"") if match else None
                if fields[field] is None:
                    fail(errors, f"scoped registry {relative} entry lacks {field}")
            entry_id = fields.get("id")
            entry_path = fields.get("path")
            if fields.get("authoritative") not in {"true", "false"}:
                fail(errors, f"scoped registry {relative} entry {entry_id or '<unknown>'} has invalid authoritative value")
            if entry_id:
                shard_ids.append(entry_id)
            if entry_path:
                shard_paths.append(entry_path)
                if scope and not entry_path.startswith(f"{scope}/"):
                    fail(errors, f"scoped registry {relative} path escapes scope {scope}: {entry_path}")
                if not (ROOT / entry_path).is_file():
                    fail(errors, f"scoped registry {relative} path does not exist: {entry_path}")

        for duplicate in sorted({value for value in shard_ids if shard_ids.count(value) > 1}):
            fail(errors, f"scoped registry {relative} contains duplicate artifact ID: {duplicate}")
        for duplicate in sorted({value for value in shard_paths if shard_paths.count(value) > 1}):
            fail(errors, f"scoped registry {relative} contains duplicate artifact path: {duplicate}")
        for duplicate in sorted(set(shard_ids) & seen_ids):
            fail(errors, f"artifact ID is authoritative in more than one registry: {duplicate}")
        for duplicate in sorted(set(shard_paths) & seen_paths):
            fail(errors, f"artifact path is authoritative in more than one registry: {duplicate}")
        seen_ids.update(shard_ids)
        seen_paths.update(shard_paths)

        if scope and (ROOT / scope).is_dir():
            actual = {
                path.relative_to(ROOT).as_posix()
                for path in (ROOT / scope).rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            }
            registered = set(shard_paths)
            for missing in sorted(actual - registered):
                fail(errors, f"file in scoped registry boundary is undeclared: {missing}")
            for outside in sorted(registered - actual):
                fail(errors, f"scoped registry declares missing boundary file: {outside}")


def check_historical_agent_evidence_manifest(errors: list[str]) -> None:
    evidence_root = ROOT / "evidence/historical-agent-runs"
    path = evidence_root / "evidence-manifest.json"
    if not path.is_file():
        fail(errors, "missing historical agent evidence manifest")
        return
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"invalid historical agent evidence manifest: {exc}")
        return
    if manifest.get("manifest_type") != "curo_historical_agent_evidence_manifest":
        fail(errors, "historical agent evidence manifest has invalid manifest_type")
    digest = manifest.get("inventory_sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        fail(errors, "historical agent evidence manifest has invalid inventory_sha256")
    raw_files = sorted(
        item for item in evidence_root.rglob("*")
        if item.is_file() and item.name not in {"README.md", "evidence-manifest.json"}
    )
    if not raw_files:
        return
    records = []
    total_bytes = 0
    for item in raw_files:
        relative = item.relative_to(ROOT).as_posix()
        content = item.read_bytes()
        total_bytes += len(content)
        records.append(f"{relative} {hashlib.sha256(content).hexdigest()}\n")
    actual_digest = hashlib.sha256("".join(records).encode("utf-8")).hexdigest()
    if len(raw_files) != manifest.get("file_count"):
        fail(errors, f"historical agent evidence count drift: expected={manifest.get('file_count')} actual={len(raw_files)}")
    if total_bytes != manifest.get("total_bytes"):
        fail(errors, f"historical agent evidence byte-size drift: expected={manifest.get('total_bytes')} actual={total_bytes}")
    if actual_digest != digest:
        fail(errors, f"historical agent evidence digest drift: expected={digest} actual={actual_digest}")


def check_standard_headings(errors: list[str]) -> None:
    path = ROOT / "docs/operating-standard.md"
    headings = re.findall(r"^#{1,3} .+$", path.read_text(encoding="utf-8"), re.MULTILINE)
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    for heading in duplicates:
        fail(errors, f"duplicate standard heading: {heading}")


def check_version_sync(errors: list[str]) -> None:
    project = (ROOT / "project.yaml").read_text(encoding="utf-8")
    standard = (ROOT / "docs/operating-standard.md").read_text(encoding="utf-8")
    replay = (ROOT / "replay/execution-replay-manifest-template.yaml").read_text(encoding="utf-8")
    registry = (ROOT / "registry/registry.yaml").read_text(encoding="utf-8")

    project_match = re.search(r"^version:\s*(\S+)", project, re.MULTILINE)
    standard_match = re.search(r"^Document version:\s*(\S+)", standard, re.MULTILINE)
    replay_match = re.search(r"^version:\s*(\S+)", replay, re.MULTILINE)
    registry_block = re.search(
        r"^  - id: operating-standard\n(.*?)(?=^  - id: |\Z)",
        registry,
        re.MULTILINE | re.DOTALL,
    )
    registry_match = (
        re.search(r"^    version:\s*(\S+)", registry_block.group(1), re.MULTILINE)
        if registry_block
        else None
    )
    matches = {
        "project.yaml": project_match.group(1) if project_match else None,
        "docs/operating-standard.md": standard_match.group(1) if standard_match else None,
        "replay/execution-replay-manifest-template.yaml": replay_match.group(1) if replay_match else None,
        "registry operating-standard": registry_match.group(1) if registry_match else None,
    }
    if None in matches.values():
        fail(errors, f"version metadata missing: {matches}")
    elif len(set(matches.values())) != 1:
        fail(errors, f"version metadata out of sync: {matches}")


def check_sentinels(errors: list[str]) -> None:
    standard = (ROOT / "docs/operating-standard.md").read_text(encoding="utf-8")
    sample = (ROOT / "provenance/sample-provenance-record.yaml").read_text(encoding="utf-8")
    if "Unknown provenance should remain UNKNOWN" not in standard:
        fail(errors, "standard is missing the UNKNOWN provenance rule")
    if re.search(r"^(input_hash|output_hash): unknown$", sample, re.MULTILINE):
        fail(errors, "sample provenance uses lowercase unknown sentinel")


def check_schema_links(errors: list[str]) -> None:
    for name in ("execution-replay-manifest", "artifact-verification-manifest"):
        schema = json.loads((ROOT / f"schemas/{name}.schema.json").read_text(encoding="utf-8"))
        reference = schema.get("properties", {}).get("provenance", {}).get("$ref")
        if reference != "provenance-record.schema.json":
            fail(errors, f"{name} schema does not reference the provenance schema")


def check_runtime_schema_ids(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "harness"))
    try:
        from curo_harness.vocabularies import RUNTIME_ARTIFACT_SCHEMAS
    except Exception as exc:
        fail(errors, f"cannot load runtime artifact/schema map: {exc}")
        return
    discovered = {}
    for path in sorted(ROOT.glob("*/*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        discovered[schema.get("$id")] = path
    for artifact_type, schema_id in RUNTIME_ARTIFACT_SCHEMAS.items():
        if schema_id not in discovered:
            fail(errors, f"runtime artifact {artifact_type} references missing canonical schema ID {schema_id}")


def check_enum_alignment(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "harness"))
    try:
        from curo_harness.vocabularies import CANDIDATE_TYPES, LEARNING_STATUSES, PROVENANCE_RESULTS, RUN_STATUSES
    except Exception as exc:
        fail(errors, f"cannot load canonical vocabularies: {exc}")
        return
    learning = json.loads((ROOT / "schemas/learning-candidate.schema.json").read_text(encoding="utf-8"))
    run = json.loads((ROOT / "observability/run-record.schema.json").read_text(encoding="utf-8"))
    provenance = json.loads((ROOT / "schemas/provenance-record.schema.json").read_text(encoding="utf-8"))
    comparisons = {
        "candidate types": (set(CANDIDATE_TYPES), set(learning["properties"]["candidate_type"]["enum"])),
        "learning statuses": (set(LEARNING_STATUSES), set(learning["properties"]["status"]["enum"])),
        "run statuses": (set(RUN_STATUSES), set(run["properties"]["status"]["enum"])),
        "provenance results": (set(PROVENANCE_RESULTS), set(provenance["properties"]["validator_result"]["enum"])),
    }
    for label, (runtime_values, schema_values) in comparisons.items():
        if runtime_values != schema_values:
            fail(errors, f"{label} drift: runtime={sorted(runtime_values)} schema={sorted(schema_values)}")
    cli = (ROOT / "harness/curo_harness/cli.py").read_text(encoding="utf-8")
    if "choices=CANDIDATE_TYPES" not in cli:
        fail(errors, "CLI candidate types do not use the canonical runtime vocabulary")


def check_replay_class_distinction(errors: list[str]) -> None:
    execution = json.loads((ROOT / "schemas/execution-replay-manifest.schema.json").read_text(encoding="utf-8"))
    verification = json.loads((ROOT / "schemas/artifact-verification-manifest.schema.json").read_text(encoding="utf-8"))
    execution_const = execution["properties"]["manifest_type"].get("const")
    verification_const = verification["properties"]["manifest_type"].get("const")
    if execution_const == verification_const:
        fail(errors, "replay artifact classes share the same manifest_type")
    for field in ("executable", "args", "cwd", "timeout_seconds"):
        if field not in execution.get("required", []):
            fail(errors, f"execution replay schema does not require {field}")
        if field in verification.get("properties", {}) or field in verification.get("required", []):
            fail(errors, f"artifact verification schema improperly contains execution field {field}")
    templates = {
        "execution_replay_manifest": ROOT / "replay/execution-replay-manifest-template.yaml",
        "artifact_verification_manifest": ROOT / "replay/artifact-verification-manifest-template.yaml",
    }
    for expected, path in templates.items():
        if not re.search(rf"^manifest_type:\s*{expected}$", path.read_text(encoding="utf-8"), re.MULTILINE):
            fail(errors, f"replay template {path.relative_to(ROOT)} has the wrong artifact class")


def check_python_bom_policy(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.py")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            fail(errors, f"Python source contains UTF-8 BOM: {path.relative_to(ROOT)}")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            fail(errors, f"Python source is not UTF-8: {path.relative_to(ROOT)}: {exc}")


def check_machine_examples_use_canonical_vocabularies(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "harness"))
    from curo_harness.vocabularies import CANDIDATE_TYPES, PROVENANCE_RESULTS, RUN_STATUSES

    checks = (
        (ROOT / "learning/learning-candidate-template.yaml", "candidate_type", set(CANDIDATE_TYPES)),
        (ROOT / "learning/learning-candidate-template.yaml", "status", {"PROPOSED"}),
        (ROOT / "provenance/sample-provenance-record.yaml", "validator_result", set(PROVENANCE_RESULTS)),
        (ROOT / "observability/sample-run-record.yaml", "status", set(RUN_STATUSES)),
    )
    for path, field, allowed in checks:
        match = re.search(rf"^{re.escape(field)}:\s*([^\s#]+)", path.read_text(encoding="utf-8"), re.MULTILINE)
        value = match.group(1) if match else None
        if value not in allowed:
            fail(errors, f"{path.relative_to(ROOT)} uses noncanonical {field}: {value!r}")


def _registry_paths() -> set[str]:
    text = (ROOT / "registry/registry.yaml").read_text(encoding="utf-8")
    return set(re.findall(r"^    path:\s*(\S+)", text, re.MULTILINE))


def check_project_contract_registration(errors: list[str]) -> None:
    expected = {
        "schemas/project-profile.schema.json",
        "schemas/llm-assignments.schema.json",
        "schemas/project-relocation-record.schema.json",
        "schemas/human-approval-record.schema.json",
        "templates/project-profile.yaml",
        "templates/llm-assignments.json",
        "projects/README.md",
    }
    registered = _registry_paths()
    for relative in sorted(expected - registered):
        fail(errors, f"project contract is not registered: {relative}")

    canonical_ids = {
        "project-profile.schema.json": "https://curo.local/schemas/project-profile.schema.json",
        "llm-assignments.schema.json": "https://curo.local/schemas/llm-assignments.schema.json",
        "project-relocation-record.schema.json": "https://curo.local/schemas/project-relocation-record.schema.json",
        "human-approval-record.schema.json": "https://curo.local/schemas/human-approval-record.schema.json",
    }
    for name, expected_id in canonical_ids.items():
        path = ROOT / "schemas" / name
        if not path.is_file():
            fail(errors, f"missing project schema: schemas/{name}")
            continue
        actual = json.loads(path.read_text(encoding="utf-8")).get("$id")
        if actual != expected_id:
            fail(errors, f"noncanonical schema ID in schemas/{name}: {actual!r}")


def check_project_vocabularies(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "harness"))
    try:
        from curo_harness.vocabularies import ASSIGNMENT_STATUSES, OBSERVED_IDENTITY_STATUSES, PROJECT_PROFILE_STATUSES
    except Exception as exc:
        fail(errors, f"cannot load project vocabularies: {exc}")
        return
    profile_schema = json.loads((ROOT / "schemas/project-profile.schema.json").read_text(encoding="utf-8"))
    assignment_schema = json.loads((ROOT / "schemas/llm-assignments.schema.json").read_text(encoding="utf-8"))
    run_schema = json.loads((ROOT / "observability/run-record.schema.json").read_text(encoding="utf-8"))
    comparisons = {
        "project profile statuses": (
            set(PROJECT_PROFILE_STATUSES), set(profile_schema["properties"]["profile_status"]["enum"]),
        ),
        "assignment statuses": (
            set(ASSIGNMENT_STATUSES), set(assignment_schema["$defs"]["assignment"]["properties"]["assignment_status"]["enum"]),
        ),
        "observed identity states": (
            set(OBSERVED_IDENTITY_STATUSES),
            set(profile_schema["$defs"]["observability"]["properties"]["observed_identity_state_values"]["items"]["enum"]),
        ),
    }
    for label, (runtime_values, schema_values) in comparisons.items():
        if runtime_values != schema_values:
            fail(errors, f"{label} drift: runtime={sorted(runtime_values)} schema={sorted(schema_values)}")
    run_observed = set(run_schema["properties"]["observed_identity"]["properties"]["state"]["enum"])
    if run_observed != set(OBSERVED_IDENTITY_STATUSES):
        fail(errors, f"run observed identity status drift: runtime={sorted(OBSERVED_IDENTITY_STATUSES)} schema={sorted(run_observed)}")

    assignment_properties = assignment_schema["$defs"]["assignment"]["properties"]
    for prohibited in ("observed_provider", "observed_model", "observed_identity"):
        if prohibited in assignment_properties:
            fail(errors, f"assignment schema improperly owns observed identity field: {prohibited}")
    for required in ("preferred_provider", "preferred_model", "resolved_identity_state", "resolved_provider", "resolved_model"):
        if required not in assignment_properties:
            fail(errors, f"assignment schema lacks desired/resolved identity field: {required}")


def check_project_layout_and_linkage(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "harness"))
    try:
        from curo_harness.assignments import verify_assignment_linkage
        from curo_harness.projects import find_plaintext_credentials, load_structured_file, validate_project_profile
    except Exception as exc:
        fail(errors, f"cannot load project runtime: {exc}")
        return

    projects_root = ROOT / "projects"
    if not projects_root.is_dir():
        fail(errors, "missing projects directory")
        return
    registered = _registry_paths()
    project_dirs = sorted(path for path in projects_root.iterdir() if path.is_dir())
    if not project_dirs:
        fail(errors, "projects directory contains no project profiles")
    for folder in project_dirs:
        profile_path = folder / "project.yaml"
        assignment_path = folder / "llm-assignments.json"
        readme_path = folder / "README.md"
        for path in (profile_path, assignment_path, readme_path):
            if not path.is_file():
                fail(errors, f"project folder lacks required file: {path.relative_to(ROOT)}")
        if not profile_path.is_file() or not assignment_path.is_file():
            continue
        profile_result = validate_project_profile(profile_path)
        if not profile_result.get("valid"):
            fail(errors, f"invalid project profile {profile_path.relative_to(ROOT)}: {profile_result.get('errors')}")
            continue
        profile = profile_result["profile"]
        if profile.get("project_id") != folder.name:
            fail(errors, f"project folder/id mismatch: {folder.name} != {profile.get('project_id')}")
        linkage = verify_assignment_linkage(assignment_path)
        if not linkage.get("valid"):
            fail(errors, f"invalid assignment linkage {assignment_path.relative_to(ROOT)}: {linkage.get('errors')}")
        assignment = linkage.get("assignments") or {}
        if assignment.get("project_id") != profile.get("project_id"):
            fail(errors, f"profile/assignment project mismatch in {folder.name}")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", str(assignment.get("source_profile_hash", ""))):
            fail(errors, f"missing canonical source-profile hash in {assignment_path.relative_to(ROOT)}")
        for finding in find_plaintext_credentials({"profile": profile, "assignment": assignment}):
            fail(errors, f"plaintext credential rejection in {folder.name}: {finding['path']}")
        for path in (profile_path, assignment_path):
            relative = path.relative_to(ROOT).as_posix()
            if relative not in registered:
                fail(errors, f"project artifact is not registered: {relative}")


def check_kayo_boundaries(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "harness"))
    try:
        from curo_harness.projects import load_structured_file
    except Exception as exc:
        fail(errors, f"cannot inspect KAYO project: {exc}")
        return
    profile_path = ROOT / "projects/kayo/project.yaml"
    assignment_path = ROOT / "projects/kayo/llm-assignments.json"
    if not profile_path.is_file() or not assignment_path.is_file():
        fail(errors, "KAYO project artifacts are missing")
        return
    profile = load_structured_file(profile_path)
    assignments = load_structured_file(assignment_path)
    authorities = {
        item.get("component_id"): set(item.get("authority", []))
        for item in profile.get("components", []) if isinstance(item, dict)
    }
    expected = {
        "second-brain": "KNOW", "kayo": "COORDINATE", "control-room": "OBSERVE",
        "visual-data-node": "UNDERSTAND", "executor": "ACT",
        "validator": "ESTABLISH EVIDENCE", "human": "AUTHORIZE",
    }
    for component, authority in expected.items():
        if authority not in authorities.get(component, set()):
            fail(errors, f"KAYO boundary missing: {component}={authority}")
    roles = {item.get("role_id"): item for item in assignments.get("assignments", []) if isinstance(item, dict)}
    required_roles = {"strategist", "builder", "critic-reviewer", "deterministic-validator", "local-private-model-lane", "human-approver"}
    for missing in sorted(required_roles - set(roles)):
        fail(errors, f"KAYO assignment lacks required role: {missing}")
    for role_id, role in roles.items():
        if role.get("role_type") == "MODEL" and role.get("authority_scope", {}).get("may_approve"):
            fail(errors, f"KAYO model role may approve its assignment: {role_id}")
        if any(str(key).startswith("observed_") for key in role):
            fail(errors, f"KAYO assignment claims observed identity: {role_id}")
    for view_id in ("control-room", "visual-data-node"):
        if not authorities.get(view_id, set()).isdisjoint({"KNOW", "ACT", "AUTHORIZE"}):
            fail(errors, f"KAYO read-only view has authoritative capability: {view_id}")


def check_historical_project_evidence(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT / "harness"))
    try:
        from curo_harness.validator import validate_curo_payload
    except Exception as exc:
        fail(errors, f"cannot load artifact validator: {exc}")
        return
    for path in sorted((ROOT / "projects").glob("*/evidence/*relocation-record.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"cannot read relocation record {path.relative_to(ROOT)}: {exc}")
            continue
        valid, validation_errors = validate_curo_payload(record, "project-relocation-record")
        if not valid:
            fail(errors, f"invalid relocation record {path.relative_to(ROOT)}: {validation_errors}")
            continue
        source = ROOT / record["original_path"]
        destination = ROOT / record["relocated_path"]
        if not source.is_file() or not destination.is_file():
            fail(errors, f"relocation path missing in {path.relative_to(ROOT)}")
            continue
        import hashlib
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        destination_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
        if source_hash != record["original_sha256"] or destination_hash != record["relocated_sha256"]:
            fail(errors, f"relocation hash mismatch in {path.relative_to(ROOT)}")
        if source_hash != destination_hash or record.get("preservation_status") != "BYTE_IDENTICAL":
            fail(errors, f"historical evidence is not byte-identical in {path.relative_to(ROOT)}")

    math_path = ROOT / "projects/math-node/evidence/math-node-v0.1-artifact-verification.json"
    if math_path.is_file():
        payload = json.loads(math_path.read_text(encoding="utf-8"))
        valid, validation_errors = validate_curo_payload(payload, "artifact-verification-manifest")
        if not valid:
            fail(errors, f"invalid Math Node artifact verification: {validation_errors}")
        for execution_field in ("executable", "command", "args", "cwd", "timeout_seconds"):
            if execution_field in payload:
                fail(errors, f"Math Node verification improperly contains execution field: {execution_field}")
    else:
        fail(errors, "missing Math Node artifact-verification replacement")


def check_current_history_distinction(errors: list[str]) -> None:
    root_architecture = ROOT / "ARCHITECTURE.md"
    archived = ROOT / "docs/audits/2026-09-07-pre-remediation-architecture.md"
    agents_index = ROOT / "evidence/historical-agent-runs/README.md"
    if not archived.is_file():
        fail(errors, "missing archived pre-remediation architecture audit")
    if not root_architecture.is_file() or "pre-remediation" not in root_architecture.read_text(encoding="utf-8").lower():
        fail(errors, "root architecture document does not distinguish the pre-remediation audit")
    if not agents_index.is_file() or "historical" not in agents_index.read_text(encoding="utf-8").lower():
        fail(errors, "historical agent-runs index does not identify reports as historical evidence")

    project_text = (ROOT / "project.yaml").read_text(encoding="utf-8")
    registry_text = (ROOT / "registry/registry.yaml").read_text(encoding="utf-8")
    project_updated = re.search(r"^updated_at:\s*([^\s#]+)", project_text, re.MULTILINE)
    registry_updated = re.search(r"^updated_at:\s*([^\s#]+)", registry_text, re.MULTILINE)
    project_date = project_updated.group(1).strip("'\"") if project_updated else None
    registry_date = registry_updated.group(1).strip("'\"") if registry_updated else None
    if not project_date or not registry_date or project_date != registry_date:
        fail(
            errors,
            f"root project.yaml and registry metadata dates differ: "
            f"project={project_date}, registry={registry_date}",
        )

    current_roots = [ROOT / "README.md", ROOT / "project.yaml", ROOT / "core-policies", ROOT / "harness", ROOT / "observability", ROOT / "templates", ROOT / "registry", ROOT / "projects"]
    stale_targets = ("schemas/replay-manifest.schema.json", "replay/replay-manifest-template.yaml")
    for base in current_roots:
        paths = [base] if base.is_file() else list(base.rglob("*.md")) + list(base.rglob("*.yaml")) + list(base.rglob("*.json"))
        for path in paths:
            if not path.is_file() or "evidence" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for stale in stale_targets:
                if stale in text:
                    fail(errors, f"current artifact references removed replay contract {stale}: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_json_schemas(errors)
    check_registry(errors)
    check_scoped_registries(errors)
    check_historical_agent_evidence_manifest(errors)
    check_standard_headings(errors)
    check_version_sync(errors)
    check_sentinels(errors)
    check_schema_links(errors)
    check_runtime_schema_ids(errors)
    check_enum_alignment(errors)
    check_replay_class_distinction(errors)
    check_python_bom_policy(errors)
    check_machine_examples_use_canonical_vocabularies(errors)
    check_project_contract_registration(errors)
    check_project_vocabularies(errors)
    check_project_layout_and_linkage(errors)
    check_kayo_boundaries(errors)
    check_historical_project_evidence(errors)
    check_current_history_distinction(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Curo foundation integrity checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
