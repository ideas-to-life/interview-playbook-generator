# Implementation Plan: Human-Owned Opportunity Decision & Evidence-Gap Handling (Upwork Proposal Generator V2.1)

**Branch**: `002-upwork-proposal-refinements` | **Date**: 2026-09-10 | **Spec**: [spec.md](file:///Users/avfranco/GitHub/interview-playbook-generator/specs/002-upwork-proposal-refinements/spec.md)

**Input**: Feature specification from `/specs/002-upwork-proposal-refinements/spec.md`

## Summary

Extend the Upwork Proposal Generator (V2.1) to decouple machine evidence integrity from the human application decision. Incomplete evidence (`UNKNOWN`, `PARTIALLY_SUPPORTED`) will surface specific missing facts and generate candidate confirmation questions without suppressing proposal/review artifact generation or forcing an autonomous machine decision. The machine emits advisory recommendations (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`), while reserving the final decision state (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`) for the human candidate. Artifacts with unresolved conditions are labelled `HUMAN_REVIEW_REQUIRED`.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: PyYAML, Markdown render utilities, Pytest  
**Storage**: File-based (YAML runtime context at `out/<target-slug>/runtime/upwork-qualification.yaml` and Markdown artifacts at `out/<target-slug>/`)  
**Testing**: Pytest (`tests/test_upwork_proposal_generator.py`)  
**Target Platform**: CLI / Antigravity AGY Agent Context  
**Project Type**: Agentic Knowledge Pipeline / Projection Engine  
**Performance Goals**: Qualification & proposal projection completion in < 5 seconds  
**Constraints**: Zero fabrication, clean client prose (no internal tags in `upwork-qualification-report.md`), strict V2.0 isolation rules preserved  
**Scale/Scope**: 2 Skills updated (`skills/upwork-qualification`, `skills/upwork-proposal`), 1 Validator extended (`skills/projection-validator`), Pytest test suite updated  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate / Principle | Status | Compliance Rationale |
|------------------|--------|----------------------|
| **I. Zero Fabrication & Absolute Claim Classification** | **PASS** | `UNKNOWN` / `PARTIALLY_SUPPORTED` evidence never generates fabricated claims or metrics; missing facts surfaced in `upwork-evidence-gaps.md`. |
| **II. Footnote Source Attribution & OKF Compliance** | **PASS** | Provenance retained in `claim_traceability` runtime context; clean copy-paste prose in client proposal. |
| **III. Identity Preservation & Expression Tailoring** | **PASS** | Tailors expression of candidate to opportunity without altering canonical career identity or upgrading personal projects. |
| **IV. Career History & Evidence Integrity** | **PASS** | Career history immutable; personal/prototype project isolation and cross-organisation isolation enforced. |
| **V. Idempotent Execution & Deterministic Pipeline** | **PASS** | Re-running pipeline after updating OKF evidence deterministically regenerates submission-ready artifacts. |

## Project Structure

### Documentation (this feature)

```text
specs/002-upwork-proposal-refinements/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── upwork-qualification-contract.md
│   ├── upwork-proposal-contract.md
│   └── upwork-validation-contract.md
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code (repository root)

```text
skills/
├── upwork-qualification/
│   └── SKILL.md         # Updated runtime qualification gate (V2.1 4-status classification & human confirmation questions)
├── upwork-proposal/
│   └── SKILL.md         # Updated proposal projection (clean prose, evidence gaps report, screening answers)
├── projection-validator/
│   └── SKILL.md         # Extended validation rules for V2.1 claim traceability & readiness checks
└── projection-registry/
    └── SKILL.md         # Projection registry entry point

scripts/
└── generate_upwork_playbook.py # Pipeline execution entry point

tests/
└── test_upwork_proposal_generator.py # Comprehensive V2.1 test suite & regression scenarios
```

**Structure Decision**: Reuses and extends existing V2.0 skills in `skills/` and test file `tests/test_upwork_proposal_generator.py` in accordance with repository conventions.

## Complexity Tracking

*No constitution violations present. Design adheres strictly to repository layering and governance principles.*
