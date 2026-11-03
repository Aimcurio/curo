# CURO: Governed AI Capability Framework

![Status](https://img.shields.io/badge/Status-Qualified_Framework_Core-green?style=flat-square) ![Language](https://img.shields.io/badge/Language-Python_3.11+-blue?style=flat-square) ![Standard](https://img.shields.io/badge/Standard-Schema_Architecture-orange?style=flat-square) ![Substrate](https://img.shields.io/badge/Substrate-Titan_Subordinate-lightgrey?style=flat-square)

**CURO** is a lightweight, modular, model-agnostic development framework providing the deterministic socket around which reusable, verifiable AI capabilities are composed, audited, and executed.

---

## Executive Overview

CURO decouples capability execution from underlying Large Language Model (LLM) providers. By enforcing strict JSON Schema boundaries, input/output validation, immutable replay logs, and multi-provider abstraction adapters (supporting Google Gemini, Anthropic Claude, OpenAI, and local models), CURO ensures that AI agent workflows remain auditable, reproducible, and resilient against model drift.

---

## Architectural Capabilities

- **Multi-Provider Adapter Plane (`adapters/`):** Unified interface for Gemini 2.5/3.8, Claude, and local models with automatic fallback and error sanitization.
- **Planner Protocol V0.1 Baseline (`docs/`):** Finite state transition specification governing plan generation, verification, and human-in-the-loop review.
- **Immutable Provenance & Observability (`observability/`):** Deterministic run records, hash-chained run events, and canonical execution replay manifests.
- **Strict Schema Enforcement (`schemas/`):** Every contract, capability, research result, and review packet is strictly validated via JSON Schema.

---

## Verified Maturity & Current Evidence

| Metric | Verified Status | Evidence Reference |
| :--- | :--- | :--- |
| **Maturity Tier** | **QUALIFIED / LOCAL FRAMEWORK (UNRELEASED)** | `C:\Users\15103\Projects\curo`, `E:\curo` |
| **Planner Protocol** | **FROZEN & VALIDATED (V0.1)** | Commit `b74a669` |
| **Schema Test Suite** | **PASS** across all contract and manifest schemas | `tests/test_gate_c_r2_semantic_evidence.py` |
| **Integration Boundary** | Subordinate to Titan governance substrate | `CURO_REGISTRY_CHECK_OBSERVATION.json` |
| **Planned / In-Progress** | Synchronization with Titan constitutional state machine | CR-001 Master Register |

---

## Quickstart & Local Verification

### Prerequisites
- Python 3.11+
- Virtual environment (`venv`)

### Installation & Test Execution
```powershell
# Clone repository
git clone https://github.com/Aimcurio/curo.git
cd curo

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install package in editable mode with test dependencies
pip install -e ".[dev]"

# Run test suite
pytest tests/
```

---

## Architectural Subordination Notice
CURO is architecturally subordinate to the Titan Governance Substrate. Provider error-handling contracts and capability grants are governed by Titan admission policies.
