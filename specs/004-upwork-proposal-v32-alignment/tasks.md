# Tasks: Upwork Proposal Generator — V3.2 Contract Alignment & Fixture Projection Refinement

**Feature Branch**: `004-upwork-proposal-v32-alignment`  
**Specification**: [`specs/004-upwork-proposal-v32-alignment/spec.md`](spec.md)  
**Implementation Plan**: [`specs/004-upwork-proposal-v32-alignment/plan.md`](plan.md)  
**Data Model**: [`specs/004-upwork-proposal-v32-alignment/data-model.md`](data-model.md)  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify repository environment and baseline test suite status.

- [X] T001 Verify baseline test suite state via pytest in `tests/test_upwork_proposal_generator.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core test framework setup for V3.2 artifact alignment validation.

- [X] T002 Create V3.2 test helpers and assertion setup in `tests/test_upwork_proposal_generator.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Executive Proposal Artifact Alignment (Priority: P1) 🎯 MVP

**Goal**: Render the complete 350–500 word Executive Proposal Cover Letter directly inside `out/<target-slug>/upwork-qualification-report.md` per `skills/upwork-proposal/SKILL.md` contract, rather than merely relocating the legacy hardcoded string.

**Independent Test**: Run `scripts/generate_upwork_biz_systems_playbook.py` and verify `out/upwork-business-systems-technology-architecture-consultant/upwork-qualification-report.md` contains the full 6-part proposal cover letter copy conforming to the canonical contract (350–500 words) with 0 static stubs.

### Tests for User Story 1

- [X] T003 [P] [US1] Add failing test verifying proposal cover letter placement and canonical contract conformance in `upwork-qualification-report.md` in `tests/test_upwork_proposal_generator.py`

### Implementation for User Story 1

- [X] T004 [US1] Refactor `generate_playbook_views()` in `scripts/generate_upwork_biz_systems_playbook.py` to conform to `skills/upwork-proposal/SKILL.md` contract, rendering the full 6-part executive proposal in `upwork-qualification-report.md` dynamically rather than relocating static strings

**Checkpoint**: User Story 1 complete and testable independently.

---

## Phase 4: User Story 2 - Screening Answer Scope Isolation (Priority: P1)

**Goal**: Ensure `out/<target-slug>/upwork-screening-answers.md` contains exclusively screening question responses (Question 1 through Question 5) with zero embedded `## Proposal Cover Letter` copy.

**Independent Test**: Run `scripts/generate_upwork_biz_systems_playbook.py` and verify `out/upwork-business-systems-technology-architecture-consultant/upwork-screening-answers.md` has no `## Proposal Cover Letter` header or proposal copy.

### Tests for User Story 2

- [X] T005 [P] [US2] Add failing test verifying zero proposal cover letter copy in `upwork-screening-answers.md` in `tests/test_upwork_proposal_generator.py`

### Implementation for User Story 2

- [X] T006 [US2] Remove proposal cover letter section from `u_screen` in `scripts/generate_upwork_biz_systems_playbook.py`

**Checkpoint**: User Story 2 complete and testable independently.

---

## Phase 5: User Story 3 - Runtime Qualification Context Binding (Priority: P2)

**Goal**: Bind projection generation in scripts/generate_upwork_biz_systems_playbook.py dynamically to the runtime qualification context in out/<target-slug>/runtime/upwork-qualification.yaml, using qualification state to determine projection behavior and any permitted artifact metadata.

**Independent Test**: Modify a qualification-state field in upwork-qualification.yaml that directly controls projection behavior (e.g. submission_readiness or proposal_content_mode), re-run the generator, and verify that the corresponding projection behavior changes without relying on hardcoded qualification-state values or leaking internal qualification state into client-facing proposal prose.

### Tests for User Story 3

- [X] T007 [P] [US3] Add failing test for runtime qualification-state-driven projection behavior in tests/test_upwork_proposal_generator.py

### Implementation for User Story 3

- [X] T008 [US3]  Implement runtime qualification-state-driven projection context in scripts/generate_upwork_biz_systems_playbook.py, loading upwork-qualification.yaml at execution time and using its qualification state to determine projection behavior and permitted artifact metadata. Do not hardcode qualification-state values or render internal qualification state as client-facing proposal prose.

**Checkpoint**: User Story 3 complete and testable independently.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation, regression testing, and documentation verification.

- [X] T009 [P] Execute the Upwork validator and full repository regression suite via pytest -v, including tests/test_upwork_proposal_generator.py.
- [X] T010 [P] Execute quickstart.md validation steps for generated artifacts in `out/upwork-business-systems-technology-architecture-consultant/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - User Story 1 (P1): MVP priority.
  - User Story 2 (P1): Can run in parallel with US1 (modifies screening answer block).
  - User Story 3 (P2): Depends on US1’s projection implementation because it establishes the qualification-report projection path; it does not depend on any specific client-facing header fields.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### Parallel Opportunities

- T003 [US1] and T005 [US2] test writing tasks can run in parallel.
- T009 and T010 polish verification tasks can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 & Phase 2 setup.
2. Complete Phase 3 (User Story 1): Render proposal cover letter in `upwork-qualification-report.md` conforming to canonical contract.
3. Validate User Story 1 independently.

### Incremental Delivery
1. Add User Story 2: Remove cover letter from `upwork-screening-answers.md`.
2. Add User Story 3: Bind projection behavior and permitted artifact metadata dynamically to qualification state.
3. Run Phase 6 polish & regression tests.
