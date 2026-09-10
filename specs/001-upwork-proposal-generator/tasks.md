# Tasks: Upwork Qualification and Proposal Generator

**Feature**: Upwork opportunity qualification and proposal generation
**Branch**: `001-upwork-proposal-generator`
**Plan**: [specs/001-upwork-proposal-generator/plan.md](specs/001-upwork-proposal-generator/plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initial environment and configuration setup for Upwork feature support.

- [ ] T001 Verify project configuration schemas and extend target opportunity options in `config/config.example.yaml`
- [ ] T002 [P] Configure test fixture paths and test environment setup in `tests/test_upwork_proposal_generator.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation.

- [ ] T003 Establish core Python qualification data structures and YAML parser helpers for requirement mapping (`direct`, `adjacent`, `transferable`, `absent`), evidence strength (`strong`, `moderate`, `weak`), and production status (`verified_production`, `verified_non_production`, `unknown`) in `skills/upwork-qualification/SKILL.md`
- [ ] T004 [P] Implement OKF evidence retrieval helper routines prioritizing evidence cards, signature achievements, and capabilities in `skills/upwork-qualification/SKILL.md`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Opportunity Qualification & Hard Gate (Priority: P1) 🎯 MVP

**Goal**: Ingest Upwork job description, map requirements to canonical OKF evidence, evaluate hard gate rules (`APPLY`, `CONDITIONAL`, `DO NOT APPLY`), enforce `proposal_generation` control state (`allowed`, `allowed_with_conditions`, `blocked`), and write `out/<target-slug>/runtime/upwork-qualification.yaml`.

**Independent Test**: Execute `upwork-qualification` against reference test cases (Scenario 1 `DO NOT APPLY` and Scenario 2 `APPLY`) and verify generated `upwork-qualification.yaml` status, `proposal_generation` state, and `claim_traceability` schema match.

### Implementation for User Story 1

- [ ] T005 [P] [US1] Write unit tests for qualification decision rules (`APPLY`, `CONDITIONAL`, `DO NOT APPLY`) and `proposal_generation` control states in `tests/test_upwork_proposal_generator.py`
- [ ] T006 [P] [US1] Create requirement mapping parser in `skills/upwork-qualification/SKILL.md`
- [ ] T007 [US1] Implement production evidence validation logic in `skills/upwork-qualification/SKILL.md` to ensure prototype/lab evidence cannot satisfy explicit client production implementation requirements
- [ ] T008 [US1] Implement `CONDITIONAL` state evaluator in `skills/upwork-qualification/SKILL.md` to track open conditions requiring candidate confirmation
- [ ] T009 [US1] Implement YAML output writer in `skills/upwork-qualification/SKILL.md` to write `out/<target-slug>/runtime/upwork-qualification.yaml` containing `proposal_generation` control status and `claim_traceability` array

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Upwork Proposal Projection (Priority: P1)

**Goal**: Generate clean, tailored executive proposal markdown (`out/<target-slug>/upwork-proposal.md`) free of visible inline tags or footnotes for direct marketplace submission, respecting qualification decisions and word count constraints (350-500 words).

**Independent Test**: Run `upwork-proposal` projection on qualified (`APPLY`), conditional (`CONDITIONAL`), and disqualified (`DO NOT APPLY`) qualification outputs and verify markdown outputs.

### Implementation for User Story 2

- [ ] T010 [P] [US2] Write unit tests for proposal projection generation and `DO NOT APPLY` gate reports in `tests/test_upwork_proposal_generator.py`
- [ ] T011 [P] [US2] Implement `DO NOT APPLY` Gate Report generator in `skills/upwork-proposal/SKILL.md` to render blocking requirements, evidence gaps, and decision rationale when `proposal_generation: blocked`
- [ ] T012 [P] [US2] Implement `CONDITIONAL` proposal renderer in `skills/upwork-proposal/SKILL.md` to display `[OPEN CONDITION: <fact>]` banners when `proposal_generation: allowed_with_conditions`
- [ ] T013 [US2] Implement `APPLY` proposal renderer in `skills/upwork-proposal/SKILL.md` to generate clean 6-part executive proposal (Opening, Proof Mapping, Project Snapshots, Approach, Smart Questions, CTA) free of visible `[evidence]` tags or `[^source-id]` footnotes, while recording claim traceability in `upwork-qualification.yaml`
- [ ] T014 [US2] Implement word count target bounds validation (350-500 words) in `skills/upwork-proposal/SKILL.md`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Screening Answers & Work Sample Projection (Priority: P2)

**Goal**: Generate `out/<target-slug>/upwork-screening-answers.md` and `out/<target-slug>/upwork-work-samples.md`.

**Independent Test**: Verify screening answers cover all client questions with explicit evidence and `[OPEN CONDITION]` tags where applicable, and work samples select up to 3 evidence-backed artifacts.

### Implementation for User Story 3

- [ ] T015 [P] [US3] Write unit tests for screening answers and work sample recommendations in `tests/test_upwork_proposal_generator.py`
- [ ] T016 [P] [US3] Implement screening answer generator in `skills/upwork-proposal/SKILL.md` answering all client questions with direct response + evidence proof, attaching `[OPEN CONDITION: <fact>]` tags under `CONDITIONAL` status
- [ ] T017 [US3] Implement work sample selector in `skills/upwork-proposal/SKILL.md` recommending up to 3 evidence-backed work samples mapped to client requirements

**Checkpoint**: User Stories 1, 2, and 3 are functional independently.

---

## Phase 6: User Story 4 - Pipeline Orchestration & Registry Integration (Priority: P2)

**Goal**: Integrate `upwork-qualification` into Runtime Layer and `upwork-proposal` into `projection-registry` so `playbook-orchestrator` automatically runs Upwork proposals when `target_type: upwork`.

**Independent Test**: Execute `/skill playbook-orchestrator` with `target_type: upwork` and confirm automated execution of qualification and proposal projection.

### Implementation for User Story 4

- [ ] T018 [P] [US4] Register `upwork-proposal` in `skills/projection-registry/SKILL.md` for `target_type == 'upwork'`
- [ ] T019 [US4] Update `skills/playbook-orchestrator/SKILL.md` to invoke `upwork-qualification` in the Runtime Layer and dispatch `upwork-proposal` via `projection-registry`

---

## Phase 7: User Story 5 - Automated Quality Gate & Evaluation Extension (Priority: P3)

**Goal**: Extend `skills/projection-validator/SKILL.md` to evaluate Upwork proposal artifacts by inspecting internal `claim_traceability` in `upwork-qualification.yaml` and append metrics to `out/<target-slug>/runtime/projection-validation-report.yaml`.

**Independent Test**: Run `/skill projection-validator` and check validation report for internal claim classification rate, evidence attribution rate, word count validity, and open condition marker presence.

### Implementation for User Story 5

- [ ] T020 [P] [US5] Write validation rules for Upwork proposal artifacts and internal provenance checking in `skills/projection-validator/SKILL.md`
- [ ] T021 [US5] Update `skills/projection-validator/SKILL.md` to parse `upwork-proposal.md`, `upwork-screening-answers.md`, and `upwork-qualification.yaml` `claim_traceability` and append validation metrics to `out/<target-slug>/runtime/projection-validation-report.yaml`

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation updates, integration testing, and final quality verification.

- [ ] T022 [P] Update repository architecture documentation in `ARCHITECTURE.md` and `AGENTS.md`
- [ ] T023 Run full pytest suite in `tests/test_upwork_proposal_generator.py` and execute `quickstart.md` validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - US1 (P1) → US2 (P1) → US3 (P2) → US4 (P2) → US5 (P3)
- **Polish (Phase 8)**: Depends on all user stories being complete.

---

## Parallel Opportunities

- T002, T004 can run in parallel during Setup & Foundational phases.
- T005, T006 can run in parallel for US1.
- T010, T011, T012 can run in parallel for US2.
- T015, T016 can run in parallel for US3.
- T018 can run in parallel for US4.
- T020 can run in parallel for US5.
- T022 can run in parallel during Polish phase.

---

## Implementation Strategy

### MVP First (User Story 1 & User Story 2)
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Qualification & Gate)
4. Complete Phase 4: User Story 2 (Proposal Projection)
5. **STOP and VALIDATE**: Verify clean proposal generation and gate report behavior independently.
