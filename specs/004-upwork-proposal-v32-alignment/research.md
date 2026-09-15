# Research & Architecture Decisions: Upwork Proposal Generator (V3.2 Alignment)

## Overview

Investigates the divergence between the canonical `upwork-proposal` skill contract (`skills/upwork-proposal/SKILL.md`) and the offline fixture generator (`scripts/generate_upwork_biz_systems_playbook.py`), and documents the architectural design for V3.2 alignment.

---

## Decisions & Rationales

### 1. Proposal Artifact Allocation & Generator Alignment

- **Decision**: Align `scripts/generate_upwork_biz_systems_playbook.py` (`generate_playbook_views()`) to write the 350–500 word Executive Proposal / Cover Letter directly into `out/<target-slug>/upwork-qualification-report.md`.
- **Rationale**: `skills/upwork-proposal/SKILL.md` defines `upwork-qualification-report.md` as the primary client-facing Executive Proposal draft. The previous behavior of writing a 3-line static verdict stub to `upwork-qualification-report.md` was a legacy artifact error.
- **Alternatives Considered**:
  - *Option A*: Retain 3-line stub and add a new file `upwork-proposal.md`. (Rejected: Violates `skills/projection-registry/SKILL.md` contract and breaks `scripts/upwork_validator.py` expectation that `upwork-qualification-report.md` contains proposal copy).
  - *Option B*: Relocate hardcoded string without binding. (Rejected: Violates FR-066 requirement that output must reflect `runtime/upwork-qualification.yaml`).

---

### 2. Screening Answer Isolation

- **Decision**: Remove the `## Proposal Cover Letter` section from `u_screen` (`out/<target-slug>/upwork-screening-answers.md`). Restrict `upwork-screening-answers.md` exclusively to client screening questions (Question 1 through Question 5).
- **Rationale**: Enforces FR-065, preventing duplicate copy between `upwork-qualification-report.md` and `upwork-screening-answers.md` and ensuring clean separation of application artifacts.
- **Alternatives Considered**:
  - *Option A*: Leave cover letter in screening answers as fallback. (Rejected: Violates FR-065 and causes validator confusion).

---

### 3. Dynamic Qualification Context Binding

- **Decision**: Bind header metadata attributes in `upwork-qualification-report.md` (`Submission Readiness`, `Machine Recommendation`, `User Decision State`, `Proposal Content Mode`) directly to values loaded from `out/<target-slug>/runtime/upwork-qualification.yaml`.
- **Rationale**: Ensures that offline generator scripts accurately reflect the runtime qualification context and submission readiness state, supporting both `SUBMISSION_READY` and `HUMAN_REVIEW_REQUIRED` workflows.
- **Alternatives Considered**:
  - *Option A*: Hardcode `SUBMISSION_READY` header string. (Rejected: Violates FR-066 and breaks validation when material requirements are `HUMAN_REVIEW_REQUIRED`).

---

### 4. Preservation of Candidate Agnosticism & Existing Invariants

- **Decision**: Ensure all generator helper functions operate dynamically on generic context objects (`qualification_data`, `opportunity_analysis`, `okf_evidence`) without embedding hardcoded candidate identity facts or employer strings in python logic.
- **Rationale**: Preserves FR-063 candidate-agnostic engine invariants and ensures regression test suites (`test_candidate_agnosticism_verification`, `test_upwork_proposal_generator.py`) continue to pass 100%.

---

## Technical Context Summary

- **Language/Version**: Python 3.13 / PyYAML / pytest
- **Primary Dependencies**: PyYAML, pytest
- **Storage**: Disk files (`out/<target-slug>/`, `out/<target-slug>/runtime/`, `out/okf/`)
- **Testing**: `pytest -v` (151 tests)
- **Target Platform**: macOS / Linux CLI runtime
- **Project Type**: CLI application / Python pipeline generator
