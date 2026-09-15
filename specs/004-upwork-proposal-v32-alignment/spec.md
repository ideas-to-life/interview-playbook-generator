# Feature Specification: Upwork Proposal Generator — V3.2 Contract Alignment & Fixture Projection Refinement

**Feature Branch**: `004-upwork-proposal-v32-alignment`  
**Created**: 2026-09-15  
**Status**: Draft  
**Refinement Base**: Refinement for `003-upwork-proposal-refinement` / V3.1 Projection Contract  

## Problem Description

Forensic analysis of the Upwork proposal generation path revealed an architectural divergence between the canonical projection contract (`skills/upwork-proposal/SKILL.md`) and the offline fixture generator (`scripts/generate_upwork_biz_systems_playbook.py`):

1. **Misallocated Proposal Output**: The offline generator writes a 3-line static verdict stub to `upwork-qualification-report.md`, while incorrectly placing the 350–500 word Executive Proposal Cover Letter inside `upwork-screening-answers.md` under `## Proposal Cover Letter`.
2. **Contract Contradiction**: Under `skills/upwork-proposal/SKILL.md`, `upwork-qualification-report.md` is specified as the clean 350–500 word client-facing Executive Proposal Draft, while `upwork-screening-answers.md` must contain only screening question answers.
3. **Unbound Generator Logic**: The offline generator script contains stale, hardcoded duplicate projection logic rather than dynamically rendering views bound to `out/<target-slug>/runtime/upwork-qualification.yaml`.

## Required V3.2 Behavior

1. **Executive Proposal Alignment**: `upwork-qualification-report.md` MUST contain the clean client-facing Executive Proposal / Cover Letter defined by the canonical projection contract (`skills/upwork-proposal/SKILL.md`). The canonical skills/upwork-proposal/SKILL.md remains the authoritative projection contract; the offline Python generator is a fixture/offline execution path that must conform to that contract and must not establish a competing projection contract.
2. **Screening Answer Isolation**: `upwork-screening-answers.md` MUST contain exclusively actual screening-question responses and MUST NOT contain the proposal/cover letter section.
3. **Qualification Context Binding**: Generator output MUST be dynamically bound to `out/<target-slug>/runtime/upwork-qualification.yaml` state (`submission_readiness`, `proposal_content_mode`, `user_decision_state`, `requirement_assessments`) rather than emitting a static verdict stub.
4. **Contract Preservation for Companion Artifacts**: `upwork-work-samples.md` and `upwork-evidence-gaps.md` MUST continue to conform to their existing contracts without regression.
5. **Clean Client Prose Standard**: Client-facing proposal copy MUST remain 100% clean of internal tags (`[evidence]`, `[inference]`), source footnote IDs (`[^source-id]`), diagnostic markers (`[OPEN CONDITION]`), or internal qualification metadata.
6. **Integrity Invariants Preserved**: All upstream attribution, evidence-boundary, candidate-agnostic, and non-fabrication rules remain intact.

---

## User Scenarios & Testing

### User Story 1 — Executive Proposal Artifact Alignment (Priority: P1)

As an Upwork candidate reviewing generated application materials, I want `out/<target-slug>/upwork-qualification-report.md` to be the primary, submission-ready Executive Proposal / Cover Letter draft so that I can copy-paste a complete 350–500 word proposal directly into the Upwork marketplace.

**Why this priority**: Eliminates artifact confusion and restores alignment with the canonical projection contract.

**Independent Test**: Execute the fixture generator for target `upwork-business-systems-technology-architecture-consultant`. Verify that `upwork-qualification-report.md` contains the complete 6-part executive proposal (350–500 words) and does NOT contain the 3-line static verdict stub.

**Acceptance Scenarios**:
1. **Given** a generated Upwork output package, **When** inspecting `upwork-qualification-report.md`, **Then** it contains the complete, submission-ready Executive Proposal / Cover Letter formatted according to the 6-part canonical structure (Opening, Proof Mapping, Snapshots, Proposed Approach, Smart Questions, CTA).
2. **Given** an opportunity where qualification state is `SUBMISSION_READY`, **When** `upwork-qualification-report.md` is rendered, **Then** it contains clean, natural proposal prose free of static verdict stubs or internal markdown tags.

---

### User Story 2 — Screening Answer Scope Isolation (Priority: P1)

As a candidate preparing application responses, I want `out/<target-slug>/upwork-screening-answers.md` to contain strictly answers to client screening questions, so that proposal text is not duplicated or mixed with Q&A responses.

**Why this priority**: Prevents redundant content and ensures screening answers adhere strictly to screening question prompts.

**Independent Test**: Inspect `upwork-screening-answers.md` after running the generator. Verify that no `## Proposal Cover Letter` heading or proposal body text exists in the file, and that all sections correspond to specific client screening questions.

**Acceptance Scenarios**:
1. **Given** a generated `upwork-screening-answers.md` artifact, **When** parsing headers, **Then** zero `## Proposal Cover Letter` sections exist, and content is limited to client question responses.

---

### User Story 3 — Runtime Qualification Context Binding (Priority: P2)

As an automated validation check or candidate reviewer, I want the generator logic to derive header metadata and readiness framing dynamically from `out/<target-slug>/runtime/upwork-qualification.yaml` so that proposal output accurately reflects qualification context.


**Why this priority**: Replaces hardcoded string literals with dynamic context binding while preserving contract compliance.

**Independent Test**: Modify a qualification-state field in upwork-qualification.yaml that directly controls projection behavior (for example submission_readiness or proposal_content_mode). Re-run the generator and verify that the corresponding projected behavior changes without any hardcoded static override.

**Acceptance Scenarios**:
1. **Given** `out/<target-slug>/runtime/upwork-qualification.yaml`, **When** the projection generator runs, **Then** header attributes (`Submission Readiness`, `Machine Recommendation`, `User Decision State`, `Proposal Content Mode`) in `upwork-qualification-report.md` are bound directly to the runtime YAML values.

---

## Non-Goals

- Do not redesign qualification scoring or qualification taxonomy.
- Do not alter canonical evidence schemas or upstream attribution semantics.
- Do not redesign proposal positioning strategy or wording rules.
- Do not introduce candidate-specific runtime code or hardcoded candidate identity facts.
- Do not modify unrelated legacy non-Upwork generator scripts.
- Do not merely relocate the existing hardcoded proposal string; the generator must conform dynamically to the canonical projection contract.

---

## Requirements

### Functional Requirements

- **FR-064 (Executive Proposal Placement)**: `out/<target-slug>/upwork-qualification-report.md` MUST serve as the sole primary container for the generated Executive Proposal / Cover Letter prose (target word count: 350–500 words).
- **FR-065 (Screening Answer Isolation)**: `out/<target-slug>/upwork-screening-answers.md` MUST contain exclusively screening-question responses. Proposal cover letters MUST NOT be embedded within screening answer artifacts.
- **FR-066 (Runtime Qualification Binding)**: The projection generator MUST read out/<target-slug>/runtime/upwork-qualification.yaml at execution time and use its qualification state (submission_readiness, machine_recommendation, user_decision_state, proposal_content_mode, and requirement_assessments) to determine projection behavior and permitted artifact metadata. Internal qualification state MUST NOT be rendered as client-facing proposal prose.
- **FR-067 (Companion Artifact Contract Preservation)**: `out/<target-slug>/upwork-work-samples.md` and `out/<target-slug>/upwork-evidence-gaps.md` MUST continue to be generated in compliance with their established V3.1 contracts.
- **FR-068 (Clean Client Prose Preservation)**: Proposal prose rendered in `upwork-qualification-report.md` MUST contain zero visible `[evidence]`, `[inference]`, `[^source-id]`, or `[OPEN CONDITION]` tags.
- **FR-069 (Attribution & Evidence Integrity Safeguards)**: Existing attribution safeguards (no production status inflation, no linear responsibility ladder inference, historical vs proposed technology separation, cross-context composition boundaries) MUST remain fully enforced.
- **FR-070 (Candidate-Agnostic Projection)**: No candidate-specific identity facts, employer strings, project names, or experience claims are hardcoded in production generator logic.

---

## Success Criteria & Acceptance Scenarios

### Measurable Outcomes

- **SC-039 (Proposal Output Correctness)**: `out/<target-slug>/upwork-qualification-report.md` contains the complete generated 6-part proposal cover letter (350–500 words), and the generated client-facing artifacts must not contain the stale static verdict stub.
- **SC-040 (Screening Answer Cleanliness)**: `out/<target-slug>/upwork-screening-answers.md` contains 0 instances of `## Proposal Cover Letter` or proposal body copy.
- **SC-041 (Qualification Context Fidelity)**: All qualification-derived metadata rendered in upwork-qualification-report.md matches the corresponding values in out/<target-slug>/runtime/upwork-qualification.yaml; no qualification-derived projection behavior relies on hardcoded static values.
- **SC-042 (Clean Prose Pass Rate)**: 100% of generated client-facing proposal artifacts pass `scripts/upwork_validator.py` zero-internal-tag checks.
- **SC-043 (Regression Test Suite Pass Rate)**: 100% of existing unit and integration tests in `tests/test_upwork_proposal_generator.py` pass cleanly.
- **SC-044 (Candidate Agnosticism Pass Rate)**: Zero candidate-specific identity facts or employer strings hardcoded in generator logic.

---

## Key Entities

- **UpworkQualificationReportV32**: Client-facing Markdown artifact at `out/<target-slug>/upwork-qualification-report.md` containing the generated Executive Proposal / Cover Letter and any permitted projection metadata.
- **UpworkScreeningAnswersV32**: Client-facing Markdown artifact at `out/<target-slug>/upwork-screening-answers.md` containing screening Q&A pairs only.
- **UpworkQualificationContextV31**: Shared runtime execution context at `out/<target-slug>/runtime/upwork-qualification.yaml`.
