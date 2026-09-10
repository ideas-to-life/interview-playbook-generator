# Tasks: Upwork Qualification, Evidence Integrity, and Proposal Generator

**Feature**: Upwork Opportunity Qualification, Evidence Integrity Controls, and Proposal Generation  
**Branch**: `001-upwork-proposal-generator`  
**Spec**: [specs/001-upwork-proposal-generator/spec.md](specs/001-upwork-proposal-generator/spec.md) (V2.0 Refinement)  
**Plan**: [specs/001-upwork-proposal-generator/plan.md](specs/001-upwork-proposal-generator/plan.md)  

---

## Phase 1: Setup (Machine-Readable Evidence Schema)

**Purpose**: Establish mandatory machine-readable frontmatter schema fields (`organisation.id`, `project.id`, `environment`, `production_verified`, `implementation_role`, `provenance`) across OKF Evidence Cards.

- [X] T001 Update OKF `EvidenceCard` generator schema in `skills/evidence-card-generator/SKILL.md` to require `organisation.id: "emp-wpp-media-2" | "personal-cas"`, `project.id: slug`, `environment: "production" | "staging" | "prototype" | "lab" | "personal" | "unknown"`, `production_verified: true | false`, `production_evidence_type: "telemetry" | "release_notes" | "client_signoff" | "attested_claim" | "none"`, `implementation_role: "lead_architect" | "sole_developer" | "contributor" | "advisor" | "evaluator" | "none"`, and `provenance.source_type: "production_telemetry" | "release_notes" | "client_signoff" | "repo_code" | "eval_harness" | "resume_claim"` frontmatter fields.
- [X] T002 [P] Update existing canonical OKF `EvidenceCard` markdown files in `out/okf/evidence/` with explicit frontmatter values matching `data-model.md` (setting `organisation.id: "emp-wpp-media-2"`, `project.id: "wpp-open-pca"`, `environment: "prototype"`, `production_verified: false`, `implementation_role: "lead_architect"` strictly from explicit source evidence per card, with zero contextual inheritance or inference from parent employment records or project folders).

---

## Phase 2: Foundational (Qualification Predicates & Isolation Rules)

**Purpose**: Implement Contract V2.0 qualification predicate logic and 15 negative inference rules in Runtime Layer qualification skill.

- [X] T003 Implement `PERSONAL_PRODUCTION_IMPLEMENTATION_EXPERIENCE` predicate in `skills/upwork-qualification/SKILL.md` requiring `(E.organisation.id == R.target_organisation_id OR R.organisation_bound == ANY) AND (E.project.id == R.target_project_id OR R.project_bound == ANY) AND (E.environment == "production" AND E.production_verified == true) AND (E.implementation_role IN ["lead_architect", "sole_developer", "contributor"])`.
- [X] T004 Implement 15 negative inference rules in `skills/upwork-qualification/SKILL.md` prohibiting inference of `production_verified = true` from 1) Employment relationship, 2) Employer name, 3) Repository name, 4) Directory name, 5) "production" in prose, 6) "deployed" in prose, 7) "operational" in prose, 8) Technology choice, 9) Evaluation metrics, 10) High success rate, 11) Low latency benchmarks, 12) Architecture diagrams, 13) Case study slides, 14) Personal CAS project evidence, or 15) Unverified resume claims.
- [X] T005 [P] Implement cross-organisation and cross-project isolation checks in `skills/upwork-qualification/SKILL.md` ensuring evidence from Company B or personal projects cannot satisfy Company A production requirements (`C_1.organisation.id == C_2.organisation.id` AND `C_1.project.id == C_2.project.id`).

**Checkpoint**: Foundation ready — user story implementation can now begin.

---

## Phase 3: User Story 1 - Production Evidence Integrity & Qualification Gate (Priority: P1) 🎯 MVP

**Goal**: Ingest Upwork job description, evaluate requirements against canonical OKF evidence frontmatter, enforce explicit dealbreaker hard gate (`UNKNOWN` $\rightarrow$ `DO NOT APPLY`), and emit machine-readable `out/<target-slug>/runtime/upwork-qualification.yaml`.

**Independent Test**: Execute `upwork-qualification` against reference target `upwork-senior-agentic-ai-architect` and verify generated `upwork-qualification.yaml` has `decision: "DO NOT APPLY"` and `proposal_generation: "blocked"` due to unverified WPP production status.

### Implementation for User Story 1

- [X] T006 [P] [US1] Implement dealbreaker hard gate evaluator in `skills/upwork-qualification/SKILL.md` evaluating `UNKNOWN` production status to `decision: "DO NOT APPLY"` (`proposal_generation: "blocked"`) when a requirement is an explicit client dealbreaker ("If you have not already done this in production, do not apply").
- [X] T007 [US1] Implement `CONDITIONAL` state evaluator in `skills/upwork-qualification/SKILL.md` to track open conditions (`proposal_generation: "allowed_with_conditions"`) when non-dealbreaker ambiguous requirements exist.
- [X] T008 [US1] Implement machine-readable `upwork-qualification.yaml` YAML output writer in `skills/upwork-qualification/SKILL.md` with complete 100% `claim_traceability` array matching schema (`requirement_id`, `claim_text`, `classification`, `okf_node_id`, `attribution`, `confidence`).
- [X] T009 [US1] Update pipeline execution script `scripts/generate_upwork_playbook.py` to invoke `upwork-qualification` and inspect `proposal_generation` control state (`allowed | allowed_with_conditions | blocked`).
- [X] T010 [US1] Implement `DO NOT APPLY` Gate Report generator in `skills/upwork-proposal/SKILL.md` to render blocking requirements, evidence gaps, and decision rationale in `out/<target-slug>/upwork-qualification-report.md` when `proposal_generation: "blocked"`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Independent Validation & Cross-Organisation Isolation (Priority: P1)

**Goal**: Extend `projection-validator` to independently inspect canonical OKF `EvidenceCard` frontmatter and cross-verify `upwork-qualification.yaml` `claim_traceability` entries, and render clean executive proposal markdown for qualified applications.

**Independent Test**: Run `projection-validator` on generated Upwork artifacts and verify it detects any unevidenced production claims, cross-organisation evidence bleeding, or cross-project isolation breaches.

### Implementation for User Story 2

- [X] T011 [P] [US2] Update `skills/projection-validator/SKILL.md` to cross-verify `upwork-qualification.yaml` `claim_traceability` entries against canonical OKF `EvidenceCard` frontmatter metadata (`organisation.id`, `project.id`, `environment`, `production_verified`, `implementation_role`).
- [X] T012 [P] [US2] Update `skills/projection-validator/SKILL.md` to flag any production claim in proposal prose that is not backed by `environment: "production"` and `production_verified: true` in OKF frontmatter.
- [X] T013 [US2] Implement clean executive proposal renderer in `skills/upwork-proposal/SKILL.md` (6-part structure: Opening, Proof Mapping, Project Snapshots, Approach, Smart Questions, CTA) free of inline tags (`[evidence]`) or footnotes (`[^source-id]`) for marketplace submission, target word count 350-500 words.
- [X] T014 [US2] Register `upwork-proposal` in `skills/projection-registry/SKILL.md` and update `skills/playbook-orchestrator/SKILL.md` to orchestrate Upwork targets through `upwork-qualification` and `upwork-proposal`.

**Checkpoint**: At this point, User Stories 1 AND 2 work independently and interoperate cleanly.

---

## Phase 5: User Story 3 - Automated Regression Protection Suite (Priority: P2)

**Goal**: Implement comprehensive automated regression test suite covering all 10 defined regression scenarios across qualification, projection, validation, and isolation controls.

**Independent Test**: Execute `pytest tests/test_upwork_proposal_generator.py tests/test_projection_validator.py` and verify all 10 regression test scenarios pass cleanly.

### Implementation for User Story 3

- [X] T015 [P] [US3] Implement unit and integration tests for Scenarios 1-7 (Scenario 1: `DO NOT APPLY` missing WPP production attestation, Scenario 2: `APPLY` with explicit production evidence, Scenario 3: Cross-organisation isolation, Scenario 4: Cross-project isolation, Scenario 5: Negative inference prohibition, Scenario 6: Hard dealbreaker gate, Scenario 7: `CONDITIONAL` open conditions) in `tests/test_upwork_proposal_generator.py`.
- [X] T016 [P] [US3] Implement validation tests for Scenarios 8-10 (Scenario 8: Clean proposal output, Scenario 9: Word count bounds 350-500 words, Scenario 10: Validation error reporting) in `tests/test_projection_validator.py`.
- [X] T017 [US3] Create reference golden snapshot outputs for Upwork test targets in `tests/golden/upwork/`.

**Checkpoint**: User Stories 1, 2, and 3 are fully functional and protected by automated regression tests.

---

## Phase 6: Polish & Verification

**Purpose**: Update architecture documentation, perform end-to-end verification, and validate quickstart scenarios.

- [X] T018 [P] Update architecture documentation in `ARCHITECTURE.md` and `AGENTS.md` reflecting Evidence Integrity & Production Qualification Controls V2.0.
- [X] T019 Execute end-to-end playbook run `/skill playbook-orchestrator` on target `upwork-senior-agentic-ai-architect` and verify `DO NOT APPLY` gate report output in `out/upwork-senior-agentic-ai-architect/upwork-qualification-report.md`.
- [X] T020 Run full pytest suite across `tests/test_upwork_proposal_generator.py` and `tests/test_projection_validator.py` and verify 100% test pass rate.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion. (MVP Gate)
- **User Story 2 (Phase 4)**: Depends on US1 completion.
- **User Story 3 (Phase 5)**: Depends on US1 and US2 completion.
- **Polish (Phase 6)**: Depends on all user stories being complete.

---

## Parallel Opportunities

- T002, T005 can run in parallel during Setup & Foundational phases.
- T006, T008 can run in parallel for US1.
- T011, T012 can run in parallel for US2.
- T015, T016 can run in parallel for US3.
- T018 can run in parallel during Polish phase.

---

## Implementation Strategy

### MVP First (User Story 1 - Production Qualification Gate)
1. Complete Phase 1: Setup (Schema update)
2. Complete Phase 2: Foundational (Predicate logic & isolation rules)
3. Complete Phase 3: User Story 1 (Dealbreaker Hard Gate & `DO NOT APPLY` report)
4. **STOP and VALIDATE**: Run `upwork-qualification` against `upwork-senior-agentic-ai-architect` and confirm `decision: "DO NOT APPLY"` and `proposal_generation: "blocked"`.
