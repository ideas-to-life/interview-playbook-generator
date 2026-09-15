# Implementation Tasks: Upwork Proposal Generator — Evidence Attribution, Composition & Claim Projection Integrity (V3.1)

**Feature Branch**: `003-upwork-proposal-refinement`  
**Specification**: [`specs/003-upwork-proposal-refinement/spec.md`](spec.md)  
**Implementation Plan**: [`specs/003-upwork-proposal-refinement/plan.md`](plan.md)  
**Data Model**: [`specs/003-upwork-proposal-refinement/data-model.md`](data-model.md)  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify project configuration and test environment setup.

- [ ] T001 [P] Verify specification, implementation plan, and candidate-agnostic engine requirements (FR-063) in `specs/003-upwork-proposal-refinement/plan.md`
- [ ] T002 [P] Verify test runner and pytest fixtures in `tests/test_upwork_proposal_generator.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core candidate-agnostic data model schemas and validation infrastructure required before implementing user stories.

**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete.

- [ ] T003 Extend runtime data model definitions for `attributed_historical_claims` and 3 independent state axes (`requirement_qualification_status`, `content_generation_safety`, `user_decision_state`) in `skills/upwork-qualification/SKILL.md`
- [ ] T004 [P] Define candidate-agnostic attribution shift and composition validation helper functions in `scripts/upwork_validator.py` operating strictly on metadata attributes (`candidate_contribution`, `system_production_status`, `candidate_production_deployment_status`) without hardcoded employer or project names

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Evidence Ownership & Attribution Integrity (Priority: P1) 🎯 MVP

**Goal**: Establish upstream non-linear attribution assessment (evaluating subject, candidate contribution, system production status, candidate implementation status, candidate production deployment status) preventing candidate contribution inflation.

**Independent Test**: Process enterprise architecture evidence card from a synthetic fixture (`OrgAlpha`). Verify `candidate_contribution: architected`, `candidate_production_deployment_status: unverified`, `requirement_qualification_status: PARTIALLY_SUPPORTED`, and zero client-facing prose asserting candidate production deployment.

### Tests for User Story 1
- [ ] T005 [P] [US1] Create test suite for non-linear attribution assessment and contribution inflation prevention using parameterized test fixtures (`OrgAlpha`, `ProjectBeta`) in `tests/test_upwork_proposal_generator.py`

### Implementation for User Story 1
- [ ] T006 [US1] Implement candidate-agnostic upstream attribution interpretation logic and `attributed_historical_claims` generator in `skills/upwork-qualification/SKILL.md`
- [ ] T007 [US1] Update `requirement_assessments` builder in `skills/upwork-qualification/SKILL.md` to evaluate candidate contribution independently from system production status
- [ ] T008 [US1] Update proposal prose generator in `skills/upwork-proposal/SKILL.md` to enforce bounded formulations (`led architecture`, `shaped architecture`, `aligned teams`) based on upstream attribution context
- [ ] T009 [US1] Implement candidate-agnostic attribution shift validation rules (platform → candidate, team → candidate, architecture → implementation) in `scripts/upwork_validator.py`

**Checkpoint**: User Story 1 is fully functional and testable independently (MVP ready).

---

## Phase 4: User Story 2 - Composition Boundary Preservation Across Multiple Contexts (Priority: P2)

**Goal**: Permit multi-context capability presentation while prohibiting synthesized composite historical claims across separate projects for single requirement satisfaction.

**Independent Test**: Evaluate enterprise architecture card (`OrgAlpha`) + personal lab coding card (`ProjectBeta`) against a single enterprise production requirement. Verify composition classification is `complementary_multi_context`, requirement qualification remains `PARTIALLY_SUPPORTED`, and proposal prose keeps separate contexts distinct.

### Tests for User Story 2
- [ ] T010 [P] [US2] Create test suite for cross-source composition boundaries and single-fact requirement validation using parameterized fixtures in `tests/test_upwork_proposal_generator.py`

### Implementation for User Story 2
- [ ] T011 [US2] Implement candidate-agnostic `composition_classification` (`same_context`, `complementary_multi_context`, `unsupported_composite`) logic in `skills/upwork-qualification/SKILL.md`
- [ ] T012 [US2] Update proposal projection in `skills/upwork-proposal/SKILL.md` to present multi-context capabilities as distinct evidence contexts without merging facts
- [ ] T013 [US2] Implement evidence composition validator check in `scripts/upwork_validator.py` to flag unsupported composite historical claims using generic metadata checks

**Checkpoint**: User Stories 1 AND 2 work independently.

---

## Phase 5: User Story 3 - Historical vs. Proposed Architecture Disambiguation (Priority: P3)

**Goal**: Enforce clear syntactic and semantic separation between past historical experience ("At [Organization], I led...") and proposed future architecture ("For your environment, I would implement...").

**Independent Test**: Generate proposal specifying proposed technologies (LangGraph, Temporal, OpenAI Agents SDK). Verify all references use prospective modal verbs ("would", "propose to") and zero references claim past historical usage without canonical evidence.

### Tests for User Story 3
- [ ] T014 [P] [US3] Create test suite for historical vs proposed technology separation in `tests/test_upwork_proposal_generator.py`

### Implementation for User Story 3
- [ ] T015 [US3] Update proposed approach generator in `skills/upwork-proposal/SKILL.md` to tag proposed technologies with `temporal_scope: proposed` and enforce prospective phrasing
- [ ] T016 [US3] Implement proposed-vs-historical validation check in `scripts/upwork_validator.py` flagging historical claims for proposed-only technologies

**Checkpoint**: User Stories 1, 2, and 3 work independently.

---

## Phase 6: User Story 4 - Strict Multi-Axis Validation & Screening Consistency (Priority: P4)

**Goal**: Ensure 3 independent state axes (`requirement_qualification`, `content_generation_safety`, `user_decision_state`), non-contradictory screening answers, and work sample narrative alignment.

**Independent Test**: Run proposal, screening, and validation generation for an unresolved requirement. Verify screening answers present bounded context with precise confirmation questions, work sample narratives match `project_type`, zero assertion-then-disclaimer patterns exist, and `user_decision_state` remains human-owned.

### Tests for User Story 4
- [ ] T017 [P] [US4] Create test suite for screening answer consistency, assertion-then-disclaimer prohibition, and work sample metadata alignment in `tests/test_upwork_proposal_generator.py`

### Implementation for User Story 4
- [ ] T018 [US4] Update screening answer generator in `skills/upwork-proposal/SKILL.md` to derive responses from 3 independent state axes and generate precision confirmation questions
- [ ] T019 [US4] Update work sample generator in `skills/upwork-proposal/SKILL.md` to enforce metadata alignment (`project_type`, `candidate_contribution`, `demonstrated_capability`)
- [ ] T020 [US4] Implement screening consistency, assertion-then-disclaimer, and work sample narrative validation checks in `scripts/upwork_validator.py`

**Checkpoint**: All 4 User Stories are independently functional.

---

## Phase 7: Polish & Golden Regression Validation

**Purpose**: Verify end-to-end regression compliance across Golden Scenarios using external test fixtures and candidate agnosticism checks.

- [ ] T021 [P] Implement Golden Scenario 1 (WPP+CAS FR-058) regression test case using external test dataset fixtures in `tests/test_upwork_proposal_generator.py`
- [ ] T022 [P] Implement Golden Scenario 2 (Project In Progress at Departure FR-059) regression test case using external test dataset fixtures in `tests/test_upwork_proposal_generator.py`
- [ ] T023 Run quickstart validation guide scenarios in `specs/003-upwork-proposal-refinement/quickstart.md` using `scripts/generate_upwork_playbook.py` and `scripts/upwork_validator.py`
- [ ] T024 [P] Verify Candidate Agnosticism (FR-063, SC-038) ensuring zero hardcoded employer or project names exist in `skills/` or `scripts/upwork_validator.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories.
- **User Stories (Phase 3+)**: Depend on Foundational phase completion. User stories can proceed in priority order (US1 → US2 → US3 → US4).
- **Polish (Phase 7)**: Depends on User Stories completion.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Can start after Foundational (Phase 2); integrates with US1 qualification structures.
- **User Story 3 (P3)**: Can start after Foundational (Phase 2); integrates with US1 proposal projection structures.
- **User Story 4 (P4)**: Can start after Foundational (Phase 2); integrates with US1/US2/US3 validation rules.

---

## Parallel Opportunities

- Setup tasks `T001` and `T002` can run in parallel.
- Test creation tasks `T005`, `T010`, `T014`, `T017` marked `[P]` can be authored in parallel with corresponding model design.
- Golden scenario tests `T021`, `T022`, and candidate agnosticism check `T024` can run in parallel during Phase 7.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete Phase 3 (User Story 1 - Evidence Ownership & Attribution Integrity).
3. **STOP and VALIDATE**: Test User Story 1 independently using `tests/test_upwork_proposal_generator.py`.

### Incremental Delivery
1. Add User Story 2 (Composition Boundaries) → Test independently.
2. Add User Story 3 (Historical vs Proposed Architecture) → Test independently.
3. Add User Story 4 (Multi-Axis Validation & Screening Consistency) → Test independently.
4. Execute Golden Regression Suite & Candidate Agnosticism Check (`T021`, `T022`, `T023`, `T024`).
