---

description: "Task list for Critical Pipeline Remediation & Failing Test Resolution"
---

# Tasks: Critical Pipeline Remediation & Failing Test Resolution

**Input**: Design documents from `/specs/007-critical-pipeline-remediation/`
**Prerequisites**: [plan.md](plan.md) (required), [spec.md](spec.md) (required), [intent.md](intent.md), [constitution.md](../../.specify/memory/constitution.md)

**Tests**: Test tasks ARE included because TDD (Red-Green-Refactor) is mandated by [intent.md](intent.md), [plan.md](plan.md), and `AGENTS.md`.

**Organization**: Tasks are grouped by functional user story derived from `FR-001`–`FR-008` in [spec.md](spec.md) to enable independent implementation and testing of each slice.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`US1`–`US6`)
- Include exact file paths in descriptions

## Path Conventions

- **Scripts**: `src/scripts/` (using `REPO_ROOT = Path(__file__).resolve().parent.parent.parent`)
- **Skills**: `src/skills/` (deployed to `.agents/skills/` via `src/scripts/deploy_skills.py`)
- **Tests**: `tests/`
- **Architecture Diagrams**: `docs/architecture/`

---

## Phase 1: Setup (Shared Infrastructure & `src/` Layout — `FR-007`)

**Purpose**: Establish the CAS `src/` directory layout, `REPO_ROOT` path depth (`parent.parent.parent`), CI triggers, and local skill `.gitignore` rules.

- [X] T001 Relocate pipeline modules under `src/scripts/` (`src/scripts/__init__.py`, `src/scripts/canonical_models.py`, `src/scripts/canonical_validator.py`, `src/scripts/employment_validator.py`, `src/scripts/generate_upwork_biz_systems_playbook.py`, `src/scripts/generate_upwork_ea_ai_solution_consultants_playbook.py`, `src/scripts/generate_upwork_fractional_ai_playbook.py`, `src/scripts/generate_upwork_playbook.py`, `src/scripts/generate_upwork_system_architect_adviser_playbook.py`) and resolve `REPO_ROOT` via `Path(__file__).resolve().parent.parent.parent`
- [X] T002 [P] Relocate skill packages and definitions under `src/skills/` (`src/skills/__init__.py`, `src/skills/projection-validator/__init__.py`, `src/skills/projection-validator/employment_validator.py`, and all `src/skills/*/SKILL.md`)
- [X] T003 [P] Update diagram generator script invocation and `src/skills/**` path triggers in `.github/workflows/architecture-diagrams.yml`
- [X] T004 [P] Update `.gitignore` to ignore locally deployed playbook skill directories and `.agents/skills/.interview-playbook-skills-manifest.json`

---

## Phase 2: Foundational (Blocking Prerequisites — `FR-007`)

**Purpose**: Lock SDD governance routing and align existing test suite imports/paths with `src/scripts/` and `src/skills/`.

**⚠️ CRITICAL**: No user story remediation work can begin until governance verification and test path alignment are complete.

- [X] T005 Verify SDD intent anchors and Path A governance routing via `cas governance verify-intent --target-dir .` and `cas governance route-plan --target-dir .` for `specs/007-critical-pipeline-remediation/intent.md`, `specs/007-critical-pipeline-remediation/spec.md`, and `specs/007-critical-pipeline-remediation/plan.md`
- [X] T006 [P] Update legacy `skills/` path references to `src/skills/` across existing test modules (`tests/test_behaviour_profile.py`, `tests/test_brand_validator.py`, `tests/test_capability_extractor.py`, `tests/test_cover_letter_projection.py`, `tests/test_executive_brief_view.py`, `tests/test_executive_identity.py`, `tests/test_forensic_remediation_regression.py`, `tests/test_linkedin_projection.py`, `tests/test_narrative_engine.py`, `tests/test_opportunity_alignment_view.py`, `tests/test_opportunity_analyzer.py`, `tests/test_projection_registry.py`, `tests/test_resume_projection.py`, `tests/test_signature_achievements_curator.py`, `tests/test_skills.py`, `tests/test_story_engine.py`, `tests/test_v04_success_criteria.py`, `tests/test_v05_success_criteria.py`, `tests/test_v06_success_criteria.py`)

**Checkpoint**: Foundation ready — user story remediation slices can now proceed in parallel.

---

## Phase 3: User Story 1 - Projection Validator Contract Conformance, Sanitization Preservation & Bypass Closure (Priority: P1) 🎯 MVP

**Goal**: Ensure `src/scripts/projection_validator.py` emits the exact six contract check keys (`education`, `certifications`, `languages`, `employment_chronology`, `technology_claims`, `cross_opportunity_isolation`), preserves Stage 1 `SANITIZED` findings (`PASSED_WITH_SANITIZATION`), blocks cross-opportunity references and empty/traversal target slugs, enforces dynamic `required_job_vocabulary` platform checks without `"ecosystem"`/`"pattern"` bypasses, and avoids corrupting non-education dates or inserting double spaces.

**Independent Test**: Run `.venv/bin/pytest tests/test_projection_validation_report_contract.py tests/test_projection_validator.py -v` and verify contract check keys, Stage 1 sanitization preservation, isolation failure, dynamic vocabulary enforcement, and date precision.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T007 [P] [US1] Add real validator contract conformance and Stage 1 sanitization-preservation tests against `specs/006-projection-data-integrity/contracts/projection-validation-report-contract.yaml` in `tests/test_projection_validation_report_contract.py`
- [X] T008 [P] [US1] Add bypass-closure (`"ecosystem"`/`"pattern"`), dynamic `required_job_vocabulary`, `cross_opportunity_isolation`, empty/missing directory, `target_slug` traversal, and education-date precision tests in `tests/test_projection_validator.py`

### Implementation for User Story 1

- [X] T009 [US1] Update `validate_projection_content()` in `src/scripts/projection_validator.py` to emit the six contract check keys (`education`, `certifications`, `languages`, `employment_chronology`, `technology_claims`, `cross_opportunity_isolation`), preserve `prior_sanitization_findings`, detect `out/<other-slug>/` isolation leaks, derive `unsupported_platforms` dynamically from `opportunity_analysis["ats_vocabulary"]["required_job_vocabulary"]`, and remove `"ecosystem"`/`"pattern"` from `TRANSFERABLE_INDICATORS`
- [X] T010 [US1] Fix `sanitize_projection_content()` in `src/scripts/projection_validator.py` to avoid inserting double spaces when rewriting education dates and restrict bare `1995–1999` sanitization to education-context lines
- [X] T011 [US1] Update `validate_opportunity_projections()` in `src/scripts/projection_validator.py` to validate `target_slug` against `^[A-Za-z0-9][A-Za-z0-9_-]*$`, scan `upwork-work-samples.md` and `upwork-evidence-gaps.md`, support `out_root` injection, record `WARNING` findings on YAML parse failures, fail fast (`FAILED` / exit code `1`) when zero projection files exist, and align `REPO_ROOT` (`parent.parent.parent`)

**Checkpoint**: User Story 1 (`FR-001`, `FR-002`) is independently functional and passes its contract and unit tests.

---

## Phase 4: User Story 2 - Zero-Fabrication Canonical Loading & Selection (Priority: P1)

**Goal**: Eliminate hardcoded factual fabrication defaults (`1988`, `2021`, `"London, UK"`, fallback languages/proficiencies, candidate-specific employer overrides) in `src/scripts/canonical_loader.py` and `src/scripts/canonical_selector.py`, extract certification years from `issue_date`, validate `target_slug` against traversal, match symbol-bearing terms (`C++`, `.NET`), and preload the OKF corpus once per `partition_ats_vocabulary` call.

**Independent Test**: Run `.venv/bin/pytest tests/test_canonical_loader.py tests/test_canonical_selection_contract.py tests/test_ats_vocabulary_partition.py -v` and confirm null-safe parsing, zero fabricated fields, traversal rejection, and symbol-term matching.

### Tests for User Story 2 ⚠️

- [X] T012 [P] [US2] Add certification year extraction from `issue_date`, null/non-dict YAML handling, missing-location preservation, generic consultancy `client` derivation, and non-fabrication tests in `tests/test_canonical_loader.py`
- [X] T013 [P] [US2] Add zero-fabrication (`start_year`, `year`, `selected_languages`), `target_slug` traversal rejection, and symbol-bearing term (`C++`, `.NET`) matching tests in `tests/test_canonical_selection_contract.py`

### Implementation for User Story 2

- [X] T014 [P] [US2] Update `src/scripts/canonical_loader.py` for null-safe YAML parsing, `issue_date` certification year extraction (returning `None` when absent), removal of default `"London, UK"` and candidate-specific overrides, generic `contracted to <client>` derivation, and `REPO_ROOT` alignment (`parent.parent.parent`)
- [X] T015 [P] [US2] Update `src/scripts/canonical_selector.py` to remove fabricated `1988`/`2021`/language defaults, validate `target_slug`, match non-word-boundary terms (`C++`, `.NET`) in `_text_contains_term()`, preload OKF corpus once in `partition_ats_vocabulary()`, and align `REPO_ROOT` (`parent.parent.parent`)

**Checkpoint**: User Story 2 (`FR-003`) is independently functional with zero fabricated defaults.

---

## Phase 5: User Story 3 - Upwork Validator CLI & Scoped Screening/Prose Checks (Priority: P2)

**Goal**: Expose a candidate-agnostic `main()` CLI (`--target-dir`, positional slug, or auto-discovery under `out/`) in `src/scripts/upwork_validator.py`, scan `proposal_md`, `screening_md`, and `work_samples_md` for internal tags/markers, and isolate Question 2 and Question 4 screening checks to their respective sections.

**Independent Test**: Run `.venv/bin/pytest tests/test_upwork_validator_cli.py tests/test_upwork_proposal_generator.py -v` and verify CLI exit codes (`0`/`1`), multi-file clean-prose enforcement, and scoped Q2/Q4 checks.

### Tests for User Story 3 ⚠️

- [X] T016 [P] [US3] Add CLI exit-code, auto-discovery, multi-file clean-prose (`proposal_md`, `screening_md`, `work_samples_md`), and scoped Q2/Q4 screening section tests pointing to `src/scripts/upwork_validator.py` in `tests/test_upwork_validator_cli.py`
- [X] T017 [P] [US3] Update `validator_path` and `src/skills/` paths in `tests/test_upwork_proposal_generator.py`

### Implementation for User Story 3

- [X] T018 [US3] Implement candidate-agnostic `main()` and `validate_upwork_directory()` in `src/scripts/upwork_validator.py`, extend clean-prose checks across `proposal_md`, `screening_md`, and `work_samples_md`, scope Q2/Q4 screening checks to their respective sections, remove dead regex/imports, and align `REPO_ROOT` (`parent.parent.parent`)

**Checkpoint**: User Story 3 (`FR-004`) is independently testable via CLI and unit tests.

---

## Phase 6: User Story 4 - Safe YAML Serialization & Rule Compliance in Portfolio Ingestor (Priority: P2)

**Goal**: Prevent YAML frontmatter injection in `src/scripts/ingest_portfolio.py` via `yaml.safe_dump()`, classify summary prose with `[evidence]`, ingest `.txt` files, emit dynamic UTC timestamps, prune stale `.md` files in `out/okf/sources/`, and fail fast when `portfolio_dir` or `target_opportunity.source` is missing.

**Independent Test**: Run `.venv/bin/pytest tests/test_portfolio_ingestor.py -v` and verify safe YAML serialization, `.txt` extraction, `[evidence]` tagging, stale-file pruning, and missing-input failure.

### Tests for User Story 4 ⚠️

- [X] T019 [P] [US4] Add YAML-injection safety, `.txt` ingestion, dynamic timestamp, `[evidence]`-tagged summary prose, stale source pruning, and missing-directory fail-fast tests in `tests/test_portfolio_ingestor.py`

### Implementation for User Story 4

- [X] T020 [US4] Update `src/scripts/ingest_portfolio.py` to add `format_okf_frontmatter()` using `yaml.safe_dump()`, extract `.txt` sources, tag summary prose with `[evidence] ... [^{slug}]`, emit UTC ISO timestamps in `index.md`, prune stale `.md` files in `out/okf/sources/`, fail fast on missing `portfolio_dir` or `target_opportunity.source`, serialize `employment-records.yaml` with `yaml.safe_dump()`, and align `REPO_ROOT` (`parent.parent.parent`)

**Checkpoint**: User Story 4 (`FR-005`) is independently functional and compliant with OKF rule invariants.

---

## Phase 7: User Story 5 - Valid Draw.io XML Generation & Hermetic Diagram Tests (Priority: P2)

**Goal**: Escape XML attribute values (including `<target-slug>`) in `src/scripts/generate_architecture_diagrams.py`, align `v0.6` skill layer mappings, support `--output-dir` for hermetic testing, regenerate valid XML at `docs/architecture/4-layer-pipeline.drawio.xml`, and run diagram tests hermetically via `sys.executable`.

**Independent Test**: Run `.venv/bin/pytest tests/test_architecture_diagram_generator.py -v` and `.venv/bin/python3 -c "import xml.etree.ElementTree as ET; ET.parse('docs/architecture/4-layer-pipeline.drawio.xml')"` with exit code `0`.

### Tests for User Story 5 ⚠️

- [X] T021 [P] [US5] Update `tests/test_architecture_diagram_generator.py` to invoke `src/scripts/generate_architecture_diagrams.py` via `sys.executable` with `--output-dir tmp_path` and assert `xml.etree.ElementTree.parse` validity on `docs/architecture/4-layer-pipeline.drawio.xml`

### Implementation for User Story 5

- [X] T022 [US5] Update `build_pipeline_drawio_xml()` and CLI flags in `src/scripts/generate_architecture_diagrams.py` to XML-escape attribute values, update `v0.6` skill/layer mappings, fix geometry width expressions, support `--output-dir`, and resolve `REPO_ROOT` (`parent.parent.parent`)
- [X] T023 [US5] Regenerate `docs/architecture/4-layer-pipeline.drawio.xml` using `./.venv/bin/python3 src/scripts/generate_architecture_diagrams.py` and verify valid XML parsing

**Checkpoint**: User Story 5 (`FR-006`) passes hermetic diagram tests and emits valid Draw.io XML.

---

## Phase 8: User Story 6 - Copy-Based Skill Deployment & Global Cleanup (Priority: P2)

**Goal**: Provide a deterministic copy-based skill deployer (`src/scripts/deploy_skills.py`) that validates `SKILL.md` frontmatter, copies skills from `src/skills/` to `.agents/skills/` without symlinks, tracks deployed skills in `.interview-playbook-skills-manifest.json`, prunes only previously managed skills, and cleans repo symlinks/manifests from global directories via `--clean-global`.

**Independent Test**: Run `.venv/bin/pytest tests/test_deploy_skills.py -v` and `.venv/bin/python3 src/scripts/deploy_skills.py --dry-run` and confirm frontmatter validation, copy/prune isolation, and `--clean-global` cleanup.

### Tests for User Story 6 ⚠️

- [X] T024 [P] [US6] Write unit and end-to-end CLI tests (`discover_skills`, `validate_skill_md`, copy/symlink replacement, manifest-scoped pruning, `--dry-run`, `--clean-global`) in `tests/test_deploy_skills.py`

### Implementation for User Story 6

- [X] T025 [US6] Implement `src/scripts/deploy_skills.py` with YAML frontmatter validation (`name`, `description`), copy-based deployment excluding `__pycache__`/`*.pyc`/`.DS_Store`, manifest tracking (`.interview-playbook-skills-manifest.json`), scoped pruning, and `--clean-global` cleanup

**Checkpoint**: User Story 6 (`FR-008`) is independently functional and verified.

---

## Phase 9: Polish & Cross-Cutting Verification

**Purpose**: Execute full-repository test verification, CAS governance gates, and local skill deployment synchronization.

- [X] T026 Run full test suite (`PATH="$PWD/.venv/bin:$PATH" ./.venv/bin/pytest tests/ -q`) and validate `docs/architecture/4-layer-pipeline.drawio.xml` with `xml.etree.ElementTree.parse`
- [X] T027 [P] Run deterministic CAS governance verification gates for `specs/007-critical-pipeline-remediation/` and `src/` (`cas governance verify-intent --target-dir .`, `cas governance route-plan --target-dir .`, `cas governance lint --target-dir .`, `cas governance verify-diff --target-dir .`, `cas governance review-pr --target-dir .`, and `cas governance watch --once`)
- [X] T028 [P] Deploy `src/skills/` to `.agents/skills/` via `./.venv/bin/python3 src/scripts/deploy_skills.py --scope local` and confirm `.agents/skills/.interview-playbook-skills-manifest.json` matches all `src/skills/*` entries

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — establishes `src/scripts/`, `src/skills/`, `.github/workflows/architecture-diagrams.yml`, and `.gitignore`.
- **Foundational (Phase 2)**: Depends on Setup completion (`T001`–`T004`) — BLOCKS all user story phases (`T005`–`T006`).
- **User Stories (Phases 3–8)**: All depend on Foundational phase completion:
  - **US1 (Phase 3 - P1 🎯 MVP)**: `FR-001`, `FR-002` in `src/scripts/projection_validator.py`.
  - **US2 (Phase 4 - P1)**: `FR-003` in `src/scripts/canonical_loader.py` and `src/scripts/canonical_selector.py`.
  - **US3 (Phase 5 - P2)**: `FR-004` in `src/scripts/upwork_validator.py`.
  - **US4 (Phase 6 - P2)**: `FR-005` in `src/scripts/ingest_portfolio.py`.
  - **US5 (Phase 7 - P2)**: `FR-006` in `src/scripts/generate_architecture_diagrams.py`.
  - **US6 (Phase 8 - P2)**: `FR-008` in `src/scripts/deploy_skills.py`.
- **Polish (Phase 9)**: Depends on Phases 3–8 completing.

### User Story Dependencies

- **US1 (P1)**, **US2 (P1)**, **US3 (P2)**, **US4 (P2)**, **US5 (P2)**, and **US6 (P2)** operate on distinct modules under `src/scripts/` and distinct test files under `tests/`, so once Phase 2 finishes they can execute independently or in parallel.
- Within each user story, TDD Red tests (`T007`–`T008`, `T012`–`T013`, `T016`–`T017`, `T019`, `T021`, `T024`) MUST be written before their corresponding implementation tasks.

### Parallel Opportunities

- **Phase 1**: `T002`, `T003`, `T004` run in parallel after `T001`.
- **Phase 3 (US1)**: `T007` and `T008` run in parallel before `T009`–`T011`.
- **Phase 4 (US2)**: `T012` and `T013` run in parallel; `T014` (`canonical_loader.py`) and `T015` (`canonical_selector.py`) run in parallel.
- **Phase 5 (US3)**: `T016` and `T017` run in parallel before `T018`.
- **Cross-Story**: Phases 3, 4, 5, 6, 7, and 8 can run concurrently across engineers/agents once Phase 2 is complete.

---

## Parallel Example: User Story 1 & User Story 2

```bash
# Launch US1 TDD Red test tasks together:
Task: "T007 [P] [US1] Add real validator contract conformance tests in tests/test_projection_validation_report_contract.py"
Task: "T008 [P] [US1] Add bypass-closure and dynamic vocabulary tests in tests/test_projection_validator.py"

# Launch US2 implementation modules in parallel (after T012-T013):
Task: "T014 [P] [US2] Update src/scripts/canonical_loader.py"
Task: "T015 [P] [US2] Update src/scripts/canonical_selector.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`src/` layout & workflow triggers)
2. Complete Phase 2: Foundational (SDD verification & test path alignment)
3. Complete Phase 3: User Story 1 (`projection_validator.py` contract conformance, sanitization preservation & bypass closure)
4. **STOP and VALIDATE**: Run `.venv/bin/pytest tests/test_projection_validation_report_contract.py tests/test_projection_validator.py -v`

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (`projection_validator.py`) → Test independently (MVP!)
3. Add US2 (`canonical_loader.py`, `canonical_selector.py`) → Test independently
4. Add US3 (`upwork_validator.py`), US4 (`ingest_portfolio.py`), US5 (`generate_architecture_diagrams.py`), US6 (`deploy_skills.py`) → Test each slice independently
5. Execute Phase 9 Polish (`pytest`, XML check, CAS gates, local skill deployment)

---

## Phase 10: Convergence

- [X] T029 Add `"responsibilities-response-guide": "Projection Layer"` to `layer_mapping` in `src/scripts/generate_architecture_diagrams.py` and assert its layer classification in `tests/test_architecture_diagram_generator.py` per FR-006 (partial)
- [X] T030 Regenerate `docs/architecture/4-layer-pipeline.drawio.xml` via `./.venv/bin/python3 src/scripts/generate_architecture_diagrams.py` and verify valid XML parsing including `responsibilities-response-guide` in the Projection Layer per FR-006 (partial)
