"""Run dependency-free integrity checks for the Curo foundation package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACT_IDS = {
    "operating-standard",
    "addendum-a",
    "gaps-and-roadmap",
    "ownership-policy",
    "precedence-policy",
    "validation-policy",
    "project-kickoff-schema",
    "provenance-record-schema",
    "replay-manifest-schema",
    "anti-patterns",
    "adapter-contract",
    "harness-contract",
    "provenance-sample",
    "replay-manifest-template",
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
    ids = {match.group(1) for match in re.finditer(r"^  - id:\s*(\S+)", text, re.MULTILINE)}
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


def check_standard_headings(errors: list[str]) -> None:
    path = ROOT / "docs/operating-standard.md"
    headings = re.findall(r"^#{1,3} .+$", path.read_text(encoding="utf-8"), re.MULTILINE)
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    for heading in duplicates:
        fail(errors, f"duplicate standard heading: {heading}")


def check_version_sync(errors: list[str]) -> None:
    project = (ROOT / "project.yaml").read_text(encoding="utf-8")
    standard = (ROOT / "docs/operating-standard.md").read_text(encoding="utf-8")
    replay = (ROOT / "replay/replay-manifest-template.yaml").read_text(encoding="utf-8")
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
        "replay/replay-manifest-template.yaml": replay_match.group(1) if replay_match else None,
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
    replay = json.loads((ROOT / "schemas/replay-manifest.schema.json").read_text(encoding="utf-8"))
    reference = replay.get("properties", {}).get("provenance", {}).get("$ref")
    if reference != "provenance-record.schema.json":
        fail(errors, "replay schema does not reference the provenance schema")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_json_schemas(errors)
    check_registry(errors)
    check_standard_headings(errors)
    check_version_sync(errors)
    check_sentinels(errors)
    check_schema_links(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Curo foundation integrity checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
