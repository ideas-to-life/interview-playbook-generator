# Implementation Tasks: Canonical Career Record Integration

**Feature**: `005-canonical-record-integration`  
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)  
**Status**: Ready for Execution  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, configuration keys, and directory structures.

- [x] T001 Configure canonical career record path under `candidate.canonical_record` in `config/config.yaml` and sync `config/config.example.yaml`
- [x] T002 [P] Create runtime schema directory structure at `specs/005-canonical-record-integration/contracts/`
- [x] T003 [P] Verify pytest and PyYAML environment dependencies in `.venv`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core canonical loading and validation modules that MUST be complete before any user story can run.

**⚠️ CRITICAL**: No user story work can begin until this foundational phase is complete.

- [x] T004 Implement canonical discovery, parsing, and fast-fail error handling in `scripts/canonical_loader.py`
- [x] T005 [P] Implement data models and validation constraints for `CareerEntry`, `EducationEntry`, `CertificationEntry`, and `UnresolvedQuestion` in `scripts/canonical_models.py`
- [x] T006 Unit tests for canonical loader validation, missing file fast-fail (<1s), and read-only integrity in `tests/test_canonical_loader.py`

**Checkpoint**: Foundation ready — canonical career record can be loaded and validated deterministically.

---

## Phase 3: User Story 1 - Authoritative Career Fact Ingestion & Quarantine Exclusion (Priority: P1) 🎯 MVP

**Goal**: Discover and ingest verified career facts exclusively from the canonical record into OKF, while structurally excluding quarantined content and deprecating legacy CSV parsing.

**Independent Test**: Run `python3 scripts/ingest_portfolio.py` and verify that `out/okf/sources/` contains zero files from `quarantine/`, and `out/okf/employment-records.yaml` is populated exclusively from `canonical/career-record.yaml` with zero contaminated records.

### Tests for User Story 1 ⚠️

- [x] T007 [P] [US1] Unit test asserting quarantine directory paths are excluded from ingestion in `tests/test_canonical_record_regression.py` (Scenario 7)
- [x] T008 [P] [US1] Integration test verifying `out/okf/employment-records.yaml` contains no legacy `Positions.csv` artifacts in `tests/test_canonical_record_regression.py`

### Implementation for User Story 1

- [x] T009 [US1] Implement directory exclusion filter for `quarantine` in `os.walk` file discovery in `scripts/ingest_portfolio.py`
- [x] T010 [US1] Remove legacy `Positions.csv` parsing logic from `scripts/ingest_portfolio.py`
- [x] T011 [US1] Implement direct generation of `out/okf/employment-records.yaml` from `career-record.yaml` using `scripts/canonical_loader.py` in `scripts/ingest_portfolio.py`
- [x] T012 [P] [US1] Update portfolio ingestion skill instructions for canonical record and quarantine rules in `skills/portfolio-ingestor/SKILL.md`

**Checkpoint**: User Story 1 is fully functional and testable independently. Quarantined data is 100% blocked, and `employment-records.yaml` is clean.

---

## Phase 4: User Story 2 - Strict Canonical Precedence & Title / Qualification Protection (Priority: P1)

**Goal**: Prevent title inflation (formal title vs acting scope) and qualification inflation (BSc vs MSc) across all outputs, and emit a structured conflict audit report.

**Independent Test**: Run validation against conflicting derived claims and verify that formal titles and degrees are strictly preserved, with discrepancies automatically sanitized and logged in `out/<target-slug>/runtime/canonical-conflict-report.yaml` and `out/<target-slug>/runtime/projection-validation-report.yaml`.

### Tests for User Story 2 ⚠️

- [x] T013 [P] [US2] Regression test asserting MSc Federal University of Rio de Janeiro is rejected and BSc Mogi das Cruzes is preserved in `tests/test_canonical_record_regression.py` (Scenario 1)
- [x] T014 [P] [US2] Regression test asserting BBC formal title is preserved and Head of Enterprise Architecture title is rejected in `tests/test_canonical_record_regression.py` (Scenario 2)
- [x] T015 [P] [US2] Regression test asserting BBC operational acting scope is distinguished from formal title in `tests/test_canonical_record_regression.py` (Scenario 3)
- [x] T016 [P] [US2] Regression test asserting unsupported enhancement (supported vs established governance) is rejected in `tests/test_canonical_record_regression.py` (Scenario 8)

### Implementation for User Story 2

- [x] T017 [US2] Implement conflict audit detector emitting `out/<target-slug>/runtime/canonical-conflict-report.yaml` in `scripts/canonical_validator.py`
- [x] T018 [US2] Expand `scripts/employment_validator.py` to validate academic degrees, institutions, and certifications against canonical records
- [x] T019 [US2] Implement automated sanitization in `scripts/employment_validator.py` to rewrite detected output discrepancies back to canonical truth with alert logging
- [x] T020 [P] [US2] Update projection validator skill instructions with conflict audit and automated sanitization in `skills/projection-validator/SKILL.md`
- [x] T021 [P] [US2] Update executive resume projection skill instructions to enforce canonical title and credential grounding in `skills/resume-projection/SKILL.md`

**Checkpoint**: User Stories 1 AND 2 are functional. Title and degree inflation are deterministically blocked and auto-sanitized.

---

## Phase 5: User Story 3 - Chronology, Employment Boundaries & Unresolved Item Safety (Priority: P2)

**Goal**: Preserve exact canonical dates, multi-stage consulting/direct employment relationships, and safe handling of unresolved items.

**Independent Test**: Verify that Compugraf/Souza Cruz are presented as consulting relationships, WPP Media/Mostelli remain distinct, and unresolved items are omitted from external collateral while flagged `[NEEDS CONFIRMATION]` in coaching artifacts.

### Tests for User Story 3 ⚠️

- [x] T022 [P] [US3] Regression test asserting complete BAT chronology is preserved over secondary incomplete sources in `tests/test_canonical_record_regression.py` (Scenario 4)
- [x] T023 [P] [US3] Regression test asserting Compugraf is represented as consultancy contracted to Souza Cruz in `tests/test_canonical_record_regression.py` (Scenario 5)
- [x] T024 [P] [US3] Regression test asserting WPP Media (direct) and Mostelli (advisory) are distinct timeline entries in `tests/test_canonical_record_regression.py` (Scenario 6)
- [x] T025 [P] [US3] Unit test asserting unresolved canonical items are omitted from external collateral and flagged `[NEEDS CONFIRMATION]` in coaching in `tests/test_canonical_record_regression.py`

### Implementation for User Story 3

- [x] T026 [US3] Implement engagement type handling (direct, consultancy, advisory) and client relationship mapping in `scripts/canonical_loader.py`
- [x] T027 [US3] Implement unresolved question filter (resolved -> fact; unresolved -> omit external, flag coaching) in `scripts/canonical_models.py`
- [x] T028 [P] [US3] Update coaching and interview strategy skills for `[NEEDS CONFIRMATION]` handling in `skills/interview-strategy-generator/SKILL.md`
- [x] T029 [P] [US3] Update knowledge gap evaluation skill to incorporate unresolved canonical questions in `skills/knowledge-gaps/SKILL.md`

**Checkpoint**: Chronology, employer relationships, and unresolved item policies are strictly enforced across all outputs.

---

## Phase 6: User Story 4 - Factual Selection vs Narrative Projection Separation (Priority: P2)

**Goal**: Decouple factual selection (Activity A) from narrative projection (Activity B) by producing an intermediate runtime artifact `out/<target-slug>/runtime/canonical-selection.yaml`.

**Independent Test**: Generate `canonical-selection.yaml` for a target opportunity and verify that all downstream projection skills consume immutable selected facts without re-interpretation.

### Tests for User Story 4 ⚠️

- [x] T030 [P] [US4] Contract test validating `out/<target-slug>/runtime/canonical-selection.yaml` against schema contract in `tests/test_canonical_selection_contract.py`
- [x] T031 [P] [US4] Integration test verifying multiple projection variants share identical canonical dates and formal titles in `tests/test_projection_consistency.py`

### Implementation for User Story 4

- [x] T032 [US4] Implement Activity A factual selection engine in `scripts/canonical_selector.py` emitting `out/<target-slug>/runtime/canonical-selection.yaml`
- [x] T033 [US4] Integrate `canonical_selector.py` into runtime opportunity analysis in `skills/opportunity-analyzer/SKILL.md`
- [x] T034 [P] [US4] Update cover letter projection skill to consume `canonical-selection.yaml` in `skills/cover-letter-projection/SKILL.md`
- [x] T035 [P] [US4] Update LinkedIn projection skill to consume `canonical-selection.yaml` in `skills/linkedin-projection/SKILL.md`
- [x] T036 [P] [US4] Update playbook assembler skill to consume `canonical-selection.yaml` in `skills/playbook-assembler/SKILL.md`

**Checkpoint**: Factual selection is locked into runtime context. Projection skills tailor narrative without altering facts.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: End-to-end regression validation, documentation updates, and quickstart verification.

- [x] T037 [P] Execute full forensic regression suite `pytest -v tests/test_canonical_record_regression.py` asserting all 8 scenarios pass
- [x] T038 Execute end-to-end quickstart validation workflow per `specs/005-canonical-record-integration/quickstart.md`
- [x] T039 [P] Update system architecture documentation with canonical layer diagrams in `ARCHITECTURE.md`
- [x] T040 [P] Update pipeline agent guidelines with canonical precedence and quarantine rules in `AGENTS.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Independent — can start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories.
- **User Story 1 (Phase 3 - MVP)**: Depends on Phase 2. Enables clean OKF ingestion.
- **User Story 2 (Phase 4)**: Depends on Phase 2 and Phase 3. Adds validation, conflict audit, and sanitization.
- **User Story 3 (Phase 5)**: Depends on Phase 2 and Phase 3. Adds employer relationship and unresolved question safety.
- **User Story 4 (Phase 6)**: Depends on Phase 2, Phase 3, and Phase 4. Adds runtime selection decoupling.
- **Polish (Phase 7)**: Depends on all user stories being complete.

### Parallel Opportunities

- **Phase 1**: T002 and T003 can execute in parallel.
- **Phase 2**: T005 can execute in parallel with T004.
- **Phase 3**: Tests T007 and T008 can run in parallel; T012 can run in parallel with T011.
- **Phase 4**: Tests T013, T014, T015, T016 can be written in parallel; T020 and T021 can be updated in parallel.
- **Phase 5**: Tests T022, T023, T024, T025 can be written in parallel; T028 and T029 can be updated in parallel.
- **Phase 6**: Tests T030 and T031 can be written in parallel; T034, T035, and T036 can be updated in parallel.
- **Phase 7**: T037, T039, and T040 can execute in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Setup (Phase 1).
2. Complete Foundational (Phase 2) — `canonical_loader.py` ready.
3. Complete User Story 1 (Phase 3) — Quarantine excluded, `Positions.csv` removed, `employment-records.yaml` clean.
4. **VALIDATE**: Run `python3 scripts/ingest_portfolio.py` and inspect `out/okf/`.

### Incremental Delivery
1. Foundation + US1 → Clean canonical knowledge substrate (MVP!).
2. Add US2 → Title and degree inflation protection with conflict reporting and auto-sanitization.
3. Add US3 → Chronology, consulting boundaries, and unresolved item flagging.
4. Add US4 → Runtime factual selection artifact (`canonical-selection.yaml`) locking facts for all projections.
5. Polish → Full test suite execution and architectural documentation sync.
