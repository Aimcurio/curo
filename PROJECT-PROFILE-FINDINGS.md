# Curo Project-Profile and LLM-Assignment Findings

Status: `EVIDENCE_ANALYSIS_COMPLETE`

Mode: repository and conversation evidence analysis. This report is the only
file changed by Sub-agent A. No implementation, schema, template, registry,
historical-evidence, version, Git, or external-project state was modified.

## Evidence boundary

This report describes the working tree observed on 2026-09-07. The tree was
already dirty before this report was created: tracked protocol-integrity files
were modified, five files were staged, and substantial remediation/audit content
was untracked. That work is treated as pre-existing shared-workspace content and
must not be reset, cleaned, overwritten, or attributed to this analyst.

Authoritative repository observations were taken from current files, Git status,
schema validation, CLI help, and SHA-256 hashing. Conversation material is used
only to recover human intent and architectural boundaries; it is not treated as
observed runtime truth or provider/model verification.

Retained conversation evidence consulted:

- `Project Curo Framework` (`6a9c3c45-4f14-83e8-8a17-d03164b50c35`): Curo is
  the governing operating standard; Math Node is an actual governed project.
- `Projects And Frameworks List` (`6a9ceeff-3a14-83e8-9681-c260b5c2372b`):
  KAYO coordinates intelligence; Second Brain is the system of record; Control
  Room and Visual Data Node are operator/view layers rather than independent
  sources of truth.
- `Summarize KAYO Architecture` (`6a9f09e3-7e88-83e8-a7d2-29bd86ca02dc`):
  the consolidated boundary is `Second Brain = KNOW`, `KAYO = COORDINATE`,
  `Control Room = OBSERVE`, `Visual Node = UNDERSTAND`, `Executor = ACT`,
  `Validator = ESTABLISH EVIDENCE`, and `Human = AUTHORIZE`.
- Retained Curo history records the approved kickoff sequence as brief, model
  analysis/plan, human review of decisions, then separately authorized bounded
  implementation. It also assigns execution facts, provenance, evidence, and
  replay authority to the harness, not the model.

## Authority relationship that the implementation must preserve

```text
generic kickoff
    = intake and decision discovery

projects/<project_id>/project.yaml
    = human-readable, reviewed project intent

projects/<project_id>/llm-assignments.json
    = validated deterministic runtime assignment derived from the approved profile

run/provenance records
    = observed execution truth written by the observing harness
```

The YAML and JSON artifacts must be linked by a canonical project-profile hash;
they must not become independently editable competing sources of truth.
Configured or resolved identity must never be copied into observed identity.

## Findings register

### finding_id: PPA-001

- **priority:** P0
- **class:** contract_gap
- **files_affected:** `templates/project-kickoff.md`,
  `templates/project-kickoff.yaml`, `schemas/project-kickoff.schema.json`, new
  `templates/project-profile.yaml`, new `schemas/project-profile.schema.json`
- **observed_evidence:** The Markdown template calls itself a copy-and-fill
  kickoff brief (`templates/project-kickoff.md:1-5`) and ends by asking the model
  to convert the brief into later contracts and phases (`:176-188`). The YAML is
  intake-oriented and contains sentinel placeholders throughout. Its provider
  section contains only `initial_provider`, `initial_model`, portability, and
  credential availability (`templates/project-kickoff.yaml:66-71`). The kickoff
  schema delegates project, objective, scope, users, provider, privacy, and
  ownership to a generic `requiredObject` with only `minProperties: 1`
  (`schemas/project-kickoff.schema.json:31-36,49-52,60-64`). No separate project
  profile template or schema exists.
- **intended_authority:** The generic kickoff is intake only. A project-specific
  profile becomes reviewed human intent; it does not itself establish observed
  execution facts.
- **recommended_resolution:** Keep the kickoff deliberately lightweight. Add
  handoff fields for profile/assignment requirements, known roles, capability
  constraints, data classification, and human decisions. Create a strict,
  project-specific profile schema/template with explicit authority, context,
  storage, tool, model, validator, failure, observability, and approval policies.

### finding_id: PPA-002

- **priority:** P0
- **class:** missing_runtime_contract
- **files_affected:** new `schemas/llm-assignments.schema.json`, new
  `templates/llm-assignments.json`, new
  `harness/curo_harness/assignments.py`, `registry/registry.yaml`
- **observed_evidence:** No LLM-assignment schema, template, runtime module, or
  registry entry exists. `harness/curo_harness/vocabularies.py:8-15` registers
  only provenance, run, replay/verification, learning, and HITL artifacts.
  `registry/registry.yaml:68-103` registers kickoff and replay schemas but has no
  project-profile or assignment entry.
- **intended_authority:** `llm-assignments.json` is a validated deterministic
  runtime contract compiled from an approved project profile and explicit
  assignment inputs. A model may propose it but may not approve it.
- **recommended_resolution:** Add a strict multi-role assignment schema and
  deterministic materializer. Require role purpose, capabilities, prohibited
  capabilities, authority, roots, context, tools, privacy/data limits,
  credentials requirements without secret values, validators, completion
  evidence, fallback rules, review, and escalation. Link every manifest to the
  source profile and its canonical hash.

### finding_id: PPA-003

- **priority:** P0
- **class:** truth_ownership_gap
- **files_affected:** new assignment contract, `observability/run-record.schema.json`,
  `observability/run-record-template.md`, `harness/curo_harness/run.py`, new
  project compiler/verifier
- **observed_evidence:** The run schema has optional
  `preferred_component`, `required_component`, and `actual_component`
  (`observability/run-record.schema.json:15-20`), but no explicit desired,
  resolved, and observed provider/model identities or identity-verification
  state. The current run writer omits those optional fields entirely
  (`harness/curo_harness/run.py:140-165`). The sample places a configured-looking
  string in `actual_component` (`observability/sample-run-record.yaml:7-9`) but
  the contract does not demonstrate how it was observed. No assignment compiler
  exists to compare the three states.
- **intended_authority:** Desired identity belongs to project intent; resolved
  identity belongs to deterministic assignment resolution; observed identity
  belongs only to a run/provenance observer. Missing observed identity is
  `UNKNOWN`, never inferred from configuration.
- **recommended_resolution:** Define distinct desired/resolved fields in the
  assignment artifact and distinct observed provider/model plus
  `VERIFIED | UNKNOWN | UNAVAILABLE | MISMATCH` state in run evidence. Add a
  comparator that detects mismatch without promoting desired or resolved values
  into observed truth.

### finding_id: PPA-004

- **priority:** P1
- **class:** architecture_boundary
- **files_affected:** new `projects/kayo/project.yaml`, new
  `projects/kayo/llm-assignments.json`, new `projects/kayo/README.md`
- **observed_evidence:** Retained conversations describe Curo as governance and
  KAYO as multi-model orchestration. They consistently place the Second Brain as
  knowledge/system-of-record, Control Room as an operational view, and Visual
  Data Node as a structural/graph view. Earlier KAYO evidence distinguishes a
  static `OFFLINE_MOCK` cockpit from the requested multichat bridge and says
  transport claims must be independently verified. No KAYO profile exists in
  this repository.
- **intended_authority:** Second Brain owns knowledge; KAYO coordinates;
  Control Room observes; Visual Node explains relationships; executor acts;
  validator establishes evidence; human authorizes. Interfaces must not directly
  mutate authoritative knowledge.
- **recommended_resolution:** Make KAYO the first complete project-profile
  example with separate Strategist, Builder, Critic/Reviewer, deterministic
  Validator, private/local lane, and Human Approver assignments. Record named
  environments as desired intent only. Leave exact providers/models
  `UNKNOWN`/`DECISION_REQUIRED` until runtime evidence verifies them.

### finding_id: PPA-005

- **priority:** P1
- **class:** repository_structure_gap
- **files_affected:** new `projects/README.md`, new `projects/<project_id>/...`,
  `README.md`, `docs/INDEX.md`, `registry/registry.yaml`, `project.yaml`
- **observed_evidence:** `projects/` does not exist. Root `project.yaml:1-24`
  describes Curo itself, including its name, slug, version, source conversation,
  and governing lineage. Root navigation documents only kickoff templates and
  then asks users to derive contracts (`docs/INDEX.md:30-34`).
- **intended_authority:** The root file remains Curo package metadata. The
  `projects/` folder is the correct home for Curo-governed, project-specific
  profiles, assignment manifests, documentation, and scoped evidence; it is not
  a replacement for external source repositories.
- **recommended_resolution:** Create one directory per normalized project ID,
  require folder/profile/assignment ID agreement, document the layout, and keep
  `actual_project_roots` as explicit paths in the profile. Do not move or modify
  the external project source repositories.

### finding_id: PPA-006

- **priority:** P1
- **class:** evidence_migration
- **files_affected:** `manifests/spacetime-sim-learning-record.json`, new
  `projects/spacetime/evidence/`, new project profile/assignment, new relocation
  record
- **observed_evidence:** The manifest is a project-specific historical record:
  it identifies `spacetime-gravity-sim`, target directory `E:\\spacetime`, Curo
  observability root, four named subagents, and historical PASS/build claims
  (`manifests/spacetime-sim-learning-record.json:2-43`). It is not a modern Curo
  project profile or assignment contract. Observed SHA-256:
  `1957C443EAC32F4302C59B072363E048919B79E41DA5C94B99E1E64986999A63`.
- **intended_authority:** Historical bytes remain historical evidence; the new
  profile is present intent; the assignment document is proposed/resolved
  runtime policy. Historical claims do not establish present provider/model
  availability.
- **recommended_resolution:** Preserve the original bytes and hash under
  `projects/spacetime/evidence/`; create separate schema-valid profile and
  assignment artifacts. If the old path is removed, validate a relocation record
  containing old path, new path, hash, and preservation method. Update references
  without reinterpreting or rewriting the record.

### finding_id: PPA-007

- **priority:** P1
- **class:** legacy_artifact_classification
- **files_affected:** `manifests/math-node-v0.1-replay.json`, new
  `projects/math-node/evidence/`, new project profile/assignment, artifact
  verification manifest
- **observed_evidence:** The legacy file declares `manifest_type:
  replay_manifest` (`:2`) but contains contract/source digests and expected
  checks (`:5-35`) and no executable command. `ARCHITECTURE.md:1011` already
  records that replay execution fails because a command is absent. The remediated
  canonical non-executing class is `artifact_verification_manifest`
  (`schemas/artifact-verification-manifest.schema.json:7-27`). Observed legacy
  SHA-256:
  `EFFB92008A760AE228803A427A146BEC1B8CEE8DF1C764AC9C48F16C85B0B8C9`.
- **intended_authority:** The old bytes are historical evidence. A new artifact
  verification manifest may supersede the classification but must not claim the
  old record was executable or rewrite it in place.
- **recommended_resolution:** Preserve/link the old file and hash, then create a
  command-free `artifact_verification_manifest` under
  `projects/math-node/evidence/`, explicitly marked as a classification
  supersession. Add a modern project profile and separate assignment manifest.

### finding_id: PPA-008

- **priority:** P1
- **class:** invalid_learning_artifact
- **files_affected:**
  `learning/candidates/LEARN-20260907-PDF-RESTORATION.yaml`, two new superseding
  candidate files
- **observed_evidence:** The candidate says `owner: model`, `status: APPROVED`,
  `candidate_type: skill_and_anti_pattern_distillation`, and
  `requires_hitl: true` (`:5-7,39`). Canonical types are only `rule`, `skill`,
  `anti_pattern`, `validator`, and `standard_amendment`
  (`schemas/learning-candidate.schema.json:13-14`). Direct validation returned
  `False` with the exact candidate-type enum error. Observed SHA-256:
  `17A1E9986178A9669A79DC3F7A77E14D42F6183904BB17600DD6EB78EF54DBB8`.
- **intended_authority:** A model may propose candidates but cannot approve its
  own promotion; a HITL-required combined historical candidate cannot confer
  approval on replacements.
- **recommended_resolution:** Do not edit the existing file. Create one
  schema-valid `skill` candidate and one schema-valid `anti_pattern` candidate,
  each with a unique ID, reference to the original, preserved evidence refs, and
  `PROPOSED` status unless exact independent approval evidence exists.

### finding_id: PPA-009

- **priority:** P2
- **class:** stale_metadata
- **files_affected:** `project.yaml`, `templates/project-kickoff.yaml`,
  `templates/project-kickoff.md`
- **observed_evidence:** Root `project.yaml:9` now claims
  `implemented_and_regression_tested`, but `updated_at` remains 2026-09-05 at
  `:11` despite 2026-09-07 working-tree changes. The kickoff templates similarly
  retain 2026-09-05 metadata (`templates/project-kickoff.yaml:2-4`,
  `templates/project-kickoff.md:197-199`) although their replay language was
  modified in the current working tree.
- **intended_authority:** Metadata should accurately date the current artifact
  revision; dates do not by themselves authorize a release.
- **recommended_resolution:** Update dates when integrating the new contract and
  make the repository gate check metadata freshness for governed current files.
  Do not change package versions as part of the metadata correction.

### finding_id: PPA-010

- **priority:** P1
- **class:** current_historical_documentation_conflict
- **files_affected:** `ARCHITECTURE.md`, new archived audit copy/current pointer,
  `.agents/` index/scope document
- **observed_evidence:** Root `ARCHITECTURE.md:1-3` labels itself authoritative,
  yet it documents the removed replay schema (`:380,409,465-467`), `shell=True`
  execution (`:600,676,869-887`), and the overloaded replay format
  (`:631-643,897-910`). Current code uses `shell=False`
  (`harness/curo_harness/process.py:39,56`), distinct replay classes, and a
  29-test suite (`REGRESSION-EVIDENCE.md:18`). `.agents/` contains time-bound
  audit reports that state `Ran 4 tests` and call the then-current tree pristine
  (`.agents/teamwork_preview_worker_1/handoff.md:38,66`) but has no README or
  INDEX explaining historical scope. Observed `ARCHITECTURE.md` SHA-256:
  `09DDF0DEA36FD05208855BAA7C471A752EB297D7ABBCDB76FAAD708712CF1BAE`.
- **intended_authority:** Historical reports remain immutable evidence of the
  repository state they observed. Current architecture authority must follow
  current schemas, code, change map, and regression evidence.
- **recommended_resolution:** Preserve the architecture document byte-for-byte
  under `docs/audits/2026-09-07-pre-remediation-architecture.md` with its hash,
  then replace the root location with a clear current pointer or current
  architecture document. Add `.agents/README.md` or `.agents/INDEX.md` stating
  that individual reports are historical observations, not automatically current
  specifications. Do not rewrite individual reports.

### finding_id: PPA-011

- **priority:** P2
- **class:** broken_reference
- **files_affected:** `skills/cli-creator.md` and its intended reference source
- **observed_evidence:** `skills/cli-creator.md:52` links to
  `references/agent-cli-patterns.md`. Neither `skills/references/` nor root
  `references/` exists, and a bounded search of installed skill/plugin content
  found no `agent-cli-patterns.md` source.
- **intended_authority:** A skill instruction must point to a real, reviewable
  reference; a missing reference must not silently become invented guidance.
- **recommended_resolution:** Determine the source/provenance of the intended
  reference. Restore it under `skills/references/agent-cli-patterns.md` if it is
  an authorized artifact, or revise/remove the sentence to point to an existing
  authoritative document. Add link validation as a regression guard.

### finding_id: PPA-012

- **priority:** P1
- **class:** registry_and_validation_coverage_gap
- **files_affected:** `registry/registry.yaml`, `scripts/validate_curo.py`,
  `schemas/README.md`, `templates/README.md`, `docs/INDEX.md`
- **observed_evidence:** Registry version 6 is dated 2026-09-07, but its project
  contract coverage stops at the generic kickoff
  (`registry/registry.yaml:68-76,176-193`). The repository validator's required
  registry entries and runtime schema map likewise contain no project profile or
  assignment artifacts (`scripts/validate_curo.py:20-47` and
  `harness/curo_harness/vocabularies.py:8-15`). `projects/` is absent.
- **intended_authority:** The registry is navigation/contract metadata, while
  schemas and executable validators establish structural validity. Registration
  must cover every new canonical artifact but must not itself prove runtime
  correctness.
- **recommended_resolution:** Register all new schemas, templates, project
  profiles, assignment manifests, preservation/relocation records, and current
  architecture references. Extend the fast repository gate for folder/ID/hash,
  vocabulary, identity separation, secret-field, KAYO-role, migration, metadata,
  and current-versus-historical checks; retain integration behavior in tests.

### finding_id: PPA-013

- **priority:** P0
- **class:** shared_worktree_integrity
- **files_affected:** entire working tree during integration
- **observed_evidence:** `git describe --tags --always --dirty` returned
  `v1.8.0-dirty`; current HEAD is
  `484555191b976bb34dc6d38b50255b78095a927f`. Git showed 31 tracked working-tree
  changes plus five staged files, and many untracked remediation, harness, test,
  manifest, rule, skill, and audit artifacts. `.agents/` is ignored by
  `.git/info/exclude`, not absent. The assigned findings file did not exist at
  the start or immediately before editing, so no collision was observed.
- **intended_authority:** Existing dirty content belongs to the user/shared team
  unless file ownership explicitly assigns it. Integration must preserve staged
  state and never infer that untracked means disposable.
- **recommended_resolution:** Maintain one file owner per agent, inspect before
  each edit, recheck status/diffs after each wave, and reject reset/clean/revert
  operations. Attribute only newly owned changes. Preserve historical hashes
  before moves or copies.

### finding_id: PPA-014

- **priority:** P1
- **class:** release_and_approval_boundary
- **files_affected:** `project.yaml`, `harness/curo_harness/__init__.py`, release
  documentation and eventual release metadata
- **observed_evidence:** The published baseline remains Curo `1.8.0`
  (`project.yaml:6`, HEAD/tag above) while the harness reports `1.0.0`
  (`harness/curo_harness/__init__.py:3`). The current remediation explicitly
  recommends a MAJOR release because replay/run contracts changed
  incompatibly (`RELEASE-IMPACT.md:33-45`; `UNRESOLVED-DECISIONS.md:5-9`). No
  version bump, release commit, tag, or push has occurred.
- **intended_authority:** Version selection and promotion are consequential human
  decisions after implementation, independent review, migration evidence, and
  complete verification.
- **recommended_resolution:** Complete the project-profile/assignment work and
  final gates without changing versions. Then present a consolidated MAJOR
  recommendation (likely `2.0.0` if Curo's document version is the public
  contract version) and request approval before any bump, commit, tag, or push.

## Read-only checks performed

- Read the complete multi-agent objective before investigation.
- Inspected `git status --short`, tracked/unstaged statistics, current tag/HEAD,
  ignore provenance, and the absence of the assigned output before editing.
- Inspected the root project metadata, kickoff Markdown/YAML/schema, harness CLI,
  runtime vocabulary, run-record construction/schema, registry, relevant docs,
  historical manifests, learning candidate/schema, `ARCHITECTURE.md`, `.agents/`,
  and the broken skill link.
- Ran `python curo.py --help`; observed only `run`, `replay`, `escalate`,
  `distill`, and `doctor`, confirming no project-profile/assignment CLI exists.
- Validated the existing PDF candidate through the current Curo validator;
  observed `False` with the invalid combined candidate-type error.
- Calculated SHA-256 values for the four named historical artifacts without
  modifying them.
- Searched available Curo/KAYO retained conversation evidence and clearly
  separated human architectural intent from executable evidence.

No unit or integration suite was rerun by this read-only analyst because the
assigned goal was evidence registration, not implementation verification. The
existing `REGRESSION-EVIDENCE.md` test result is reported as an observed record,
not independently re-certified here.

## Assumptions and decisions still requiring evidence

- Exact KAYO provider/model availability, credentials, transports, external
  roots, and observed execution identities remain `UNKNOWN` or
  `DECISION_REQUIRED`; conversation references cannot verify them.
- The user has confirmed project folders are appropriate for project-specific
  Curo records. This does not authorize moving or editing external source repos.
- Copy-versus-move for historical manifests should favor byte-preserving copy
  until references and relocation records are validated; removal of an original
  path requires an explicit auditable relocation chain.
- Project profile approval, assignment approval, candidate promotion, and release
  version remain human authority boundaries.

## Analyst conclusion

The working tree contains a substantial protocol-integrity remediation, but the
project-definition layer is genuinely missing. The correct implementation is not
to make the generic kickoff enormous. It is to preserve kickoff as intake, add a
strict project-specific profile, derive one validated/hash-linked assignment
manifest from it, and reserve actual provider/model identity for observed run
evidence. KAYO, Spacetime, and Math Node should then become concrete examples
under `projects/`, with historical bytes preserved and no invented assignments.
