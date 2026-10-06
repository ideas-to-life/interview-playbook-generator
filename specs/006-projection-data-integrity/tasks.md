# Implementation Tasks: Projection Data Integrity & Provenance Remediation

**Feature**: `006-projection-data-integrity`  
**Plan**: [specs/006-projection-data-integrity/plan.md](plan.md)  
**Spec**: [specs/006-projection-data-integrity/spec.md](spec.md)  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish directories and fact-free synthetic structural templates for projection skills.

- [x] T001 Create synthetic projection templates directory at `templates/projections/`
- [x] T002 [P] Create fact-free executive resume template with neutral placeholder data at `templates/projections/resume-executive.template.md`
- [x] T003 [P] Create fact-free ATS resume template with neutral placeholder data at `templates/projections/resume-ats.template.md`
- [x] T004 [P] Create fact-free cover letter template with neutral placeholder data at `templates/projections/cover-letter.template.md`
- [x] T005 [P] Create fact-free LinkedIn profile template with neutral placeholder data at `templates/projections/linkedin-profile.template.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core validation data structures and contract test suites that block user story implementation.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T006 Define data models for `ProjectionValidationReport` in `scripts/canonical_models.py` with `overall_status` enum `["PASSED", "FAILED", "PASSED_WITH_SANITIZATION"]` and `findings` with `severity` enum `["FATAL", "SANITIZED", "WARNING"]`
- [x] T007 [P] Implement contract test for projection validation report schema in `tests/test_projection_validation_report_contract.py` validating against `specs/006-projection-data-integrity/contracts/projection-validation-report-contract.yaml`
- [x] T008 [P] Implement contract test for ATS vocabulary partition schema in `tests/test_ats_vocabulary_partition_contract.py` validating against `specs/006-projection-data-integrity/contracts/ats-vocabulary-partition-contract.yaml`

**Checkpoint**: Foundational schemas and contract tests locked; user story implementation can begin.

---

## Phase 3: User Story 1 - Complete Canonical Context Injection & Context Isolation (Priority: P1) 🎯 MVP

**Goal**: Guarantee that 100% of `canonical-selection.yaml` (including facts beyond line 50: BSc 1988–1991, certifications, languages) is loaded into projection context, and isolate opportunity runs by eliminating references to prior opportunity outputs.

**Independent Test**: Generate collateral from a canonical selection where credentials appear past line 50, and where a prior opportunity directory contains corrupted claims, verifying all selected facts are preserved and zero corrupted facts leak into output.

### Tests for User Story 1 ⚠️

- [x] T009 [P] [US1] Write automated test in `tests/test_canonical_selection_contract.py` verifying facts beyond line 50 of `canonical-selection.yaml` (BSc 1988–1991, certifications, languages) remain fully available in model context
- [x] T010 [P] [US1] Write automated test in `tests/test_opportunity_isolation.py` verifying active generation runs read zero files from `out/<other-target-slug>/`

### Implementation for User Story 1

- [x] T011 [US1] Update `scripts/canonical_selector.py` to ensure complete, untruncated writing of all canonical sections (education, certs, languages, employment) to `out/<target-slug>/runtime/canonical-selection.yaml`
- [x] T012 [P] [US1] Update prompt loading in `skills/resume-projection/SKILL.md` to consume full `canonical-selection.yaml` and synthetic template `templates/projections/resume-executive.template.md` without reading prior opportunity outputs
- [x] T013 [P] [US1] Update prompt loading in `skills/cover-letter-projection/SKILL.md` to consume full `canonical-selection.yaml` and synthetic template `templates/projections/cover-letter.template.md` without reading prior opportunity outputs
- [x] T014 [P] [US1] Update prompt loading in `skills/linkedin-projection/SKILL.md` to consume full `canonical-selection.yaml` and synthetic template `templates/projections/linkedin-profile.template.md` without reading prior opportunity outputs
- [x] T015 [P] [US1] Update prompt loading in `skills/opportunity-alignment-view/SKILL.md` and `skills/executive-brief-view/SKILL.md` to enforce complete canonical selection injection and cross-opportunity isolation

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently (MVP ready).

---

## Phase 4: User Story 2 - Evidence-Aware Opportunity Analysis & ATS Scoring (Priority: P1)

**Goal**: Partition target JD vocabulary into `required_job_vocabulary` and `candidate_evidenced_vocabulary`, removing optimization incentives to claim unevidenced client tools.

**Independent Test**: Execute opportunity analysis on a JD requiring unevidenced enterprise platforms (Workday, NetSuite, Coupa, Concur), verify vocabulary is partitioned per contract, and verify density scoring awards 0% credit for unevidenced terms.

### Tests for User Story 2 ⚠️

- [x] T016 [P] [US2] Write unit tests in `tests/test_ats_vocabulary_partition.py` verifying vocabulary partitioning against `career-record.yaml` and `out/okf/` evidence

### Implementation for User Story 2

- [x] T017 [US2] Implement multi-tier evidence resolution helper in `scripts/canonical_selector.py` to classify extracted keywords against `career-record.yaml` and verified OKF capabilities
- [x] T018 [US2] Update `skills/opportunity-analyzer/SKILL.md` to partition extracted ATS terms into `candidate_evidenced_vocabulary` and `required_job_vocabulary` in `out/<target-slug>/runtime/opportunity-analysis.yaml`
- [x] T019 [US2] Update ATS density scoring logic in `skills/opportunity-analyzer/SKILL.md` and `skills/projection-validator/SKILL.md` to award credit exclusively for `candidate_evidenced_vocabulary` and assign integrity defect penalties for unevidenced direct claims

**Checkpoint**: User Stories 1 and 2 functional and testable independently.

---

## Phase 5: User Story 3 - Comprehensive Deterministic Post-Generation Factual Validation (Priority: P1)

**Goal**: Implement unified deterministic validator `scripts/projection_validator.py` executing hybrid remediation (automated sanitization of repairable dates/titles + hard validation failure on un-sanitizable direct claims), outputting `out/<target-slug>/runtime/projection-validation-report.yaml`.

**Independent Test**: Run validator against projections with mutated education dates, unverified certifications, inflated languages, and direct Workday implementation claims; verify automated repair of canonical facts and hard exit code 1 on direct unevidenced claims.

### Tests for User Story 3 ⚠️

- [x] T020 [P] [US3] Write unit tests in `tests/test_projection_validator.py` for education date/institution verification and automated sanitization (BSc 1988–1991 vs 1995–1999)
- [x] T021 [P] [US3] Write unit tests in `tests/test_projection_validator.py` for certification audit (failing on AWS, Sun SCEA/SCJP)
- [x] T022 [P] [US3] Write unit tests in `tests/test_projection_validator.py` for language proficiency audit (failing on Spanish Fluent vs Elementary)
- [x] T023 [P] [US3] Write unit tests in `tests/test_projection_validator.py` for named technology claims (failing on direct unevidenced platform claims while permitting transferable framing)

### Implementation for User Story 3

- [x] T024 [US3] Implement unified deterministic validator in `scripts/projection_validator.py` auditing education, certs, languages, employment facts, and technology claims against `canonical-selection.yaml` and emitting `out/<target-slug>/runtime/projection-validation-report.yaml`
- [x] T025 [US3] Implement Stage 1 automated in-place text sanitization in `scripts/projection_validator.py` for repairable canonical facts (dates, titles, formal degrees)
- [x] T026 [US3] Implement Stage 2 fatal defect detection in `scripts/projection_validator.py` halting completion with exit code 1 when un-sanitizable direct claims are detected
- [x] T027 [US3] Refactor `scripts/employment_validator.py` and `skills/projection-validator/SKILL.md` to delegate to `scripts/projection_validator.py`

**Checkpoint**: User Stories 1, 2, and 3 functional and testable independently.

---

## Phase 6: User Story 4 - Forensic Regression Test Suite & Invariant Verification (Priority: P2)

**Goal**: Implement all 10 diagnostic failure scenarios in an automated regression suite to ensure complete long-term protection against the Tenth AI failure modes.

**Independent Test**: Run `pytest tests/test_forensic_remediation_regression.py -v` and verify 100% deterministic pass rate across all 10 scenarios.

### Implementation for User Story 4

- [x] T028 [P] [US4] Implement Scenarios 1–3 in `tests/test_forensic_remediation_regression.py` (complete canonical selection loading, education date contradiction, certification invention)
- [x] T029 [P] [US4] Implement Scenarios 4–6 in `tests/test_forensic_remediation_regression.py` (language inflation, target JD platform leakage, previous projection contamination)
- [x] T030 [P] [US4] Implement Scenarios 7–10 in `tests/test_forensic_remediation_regression.py` (opportunity runtime isolation, unsupported technology claim, transferable framing allowance, canonical precedence)

**Checkpoint**: All 4 user stories functional; full forensic regression suite passing.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation updates, quickstart verification, and full repository test execution.

- [x] T031 [P] Update `AGENTS.md` and `RUNBOOK.md` documentation to reflect the unified `scripts/projection_validator.py` and the 5-tier information boundary
- [x] T032 Execute end-to-end quickstart validation per `specs/006-projection-data-integrity/quickstart.md` across test fixtures
- [x] T033 Run full repository test suite `pytest tests/ -v` to verify zero regressions across all existing test modules

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3–6)**: Depend on Foundational phase completion
  - Phase 3 (US1 - Context & Isolation) is the primary MVP.
  - Phase 4 (US2 - ATS Partitioning) depends on US1.
  - Phase 5 (US3 - Unified Validator) can proceed in parallel with US2.
  - Phase 6 (US4 - Forensic Regression Suite) executes against US1, US2, and US3.
- **Polish (Phase 7)**: Depends on all user story phases being complete.

### Parallel Opportunities

- In Phase 1: Tasks T002, T003, T004, T005 can be generated concurrently.
- In Phase 2: Tasks T007 and T008 can execute in parallel.
- In Phase 3: Tests T009 and T010 can execute in parallel; prompt skill updates T012, T013, T014, T015 can proceed in parallel.
- In Phase 5: Validator unit tests T020, T021, T022, T023 can be written concurrently.
- In Phase 6: Regression scenario modules T028, T029, T030 can be written concurrently.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup (`templates/projections/`)
2. Complete Phase 2: Foundational (Models & Contract Tests)
3. Complete Phase 3: User Story 1 (Full Canonical Context Injection & Context Isolation)
4. **Validate MVP**: Verify that education and credentials past line 50 are preserved and no prior-opportunity leakage occurs.

### Incremental Delivery
1. Deliver MVP (US1: Context & Isolation).
2. Deliver US2 (Evidence-Partitioned ATS Vocabulary & Scoring).
3. Deliver US3 (Unified Deterministic Factual Validator & Sanitizer).
4. Deliver US4 (10-Scenario Forensic Regression Suite).
5. Run full test suite and update documentation.
