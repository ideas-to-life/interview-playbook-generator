# Implementation Plan: Upwork Proposal Generator — Evidence Attribution, Composition & Claim Projection Integrity (V3.1)

**Branch**: `003-upwork-proposal-refinement` | **Date**: 2026-09-15 | **Spec**: [`specs/003-upwork-proposal-refinement/spec.md`](spec.md)

**Input**: Feature specification from `/specs/003-upwork-proposal-refinement/spec.md`

## Summary

This plan specifies the implementation roadmap for V3.1 Evidence Attribution, Composition & Claim Projection Integrity. The core refinement establishes structured, non-linear attribution assessment upstream in the Runtime Layer (`upwork-qualification` skill and `upwork-qualification.yaml` context), preventing candidate contribution inflation and unsupported cross-source evidence composition before qualification and prose projection take place. Automated validation (`upwork_validator.py`) functions as a cross-cutting quality gate checking projection consistency against upstream attribution context. Per FR-063, the engine logic and validators remain strictly candidate-agnostic, with specific candidate scenarios (such as WPP/CAS) restricted to external test fixtures.

## Technical Context

**Language/Version**: Python 3.13 (Pytest test runner environment)

**Primary Dependencies**: PyYAML, Jinja2 / Python standard library, Markdown parsers, existing OKF graph modules

**Storage**: YAML file-based runtime context at `out/<target-slug>/runtime/upwork-qualification.yaml` and validation report at `out/<target-slug>/runtime/upwork-validation-report.yaml`

**Testing**: Pytest (`tests/test_upwork_proposal_generator.py`)

**Target Platform**: macOS / Linux CLI runtime (`playbook-orchestrator`, `upwork-qualification`, `upwork-proposal`, `upwork_validator.py`)

**Project Type**: CLI / Skill Pipeline for career projection & Upwork proposal generation

**Performance Goals**: Sub-second qualification analysis & proposal projection execution (<2.0s per opportunity)

**Constraints**: 100% deterministic, zero LLM hallucination in validation, 4-layer architectural boundary, zero fabrication, non-linear attribution assessment, 100% candidate-agnostic engine logic (FR-063)

**Scale/Scope**: Opportunities with complex multi-source evidence graphs (parameterized test datasets and real candidate evidence)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Zero Fabrication & Absolute Claim Classification**: Preserves strict prohibition against fabricated metrics, projects, technologies, tenure, or deployment status. All unverified facts recorded as `missing_facts`.
- [x] **II. Footnote Source Attribution & OKF v0.2 Compliance**: Preserves OKF v0.2 graph structure and footnote attribution metadata without altering canonical OKF specification.
- [x] **III. Identity Preservation & Expression Tailoring**: Tailors expression to opportunity without altering candidate's canonical identity. Prevents target requirements from becoming candidate evidence.
- [x] **IV. Career History & Evidence Integrity**: Employer names, dates, titles, and locations remain immutable. Prohibits inferring leadership/ownership from contribution or upgrading advisory to implementation.
- [x] **V. Idempotent Execution & Deterministic Pipeline**: Execution remains 100% deterministic and idempotent. Disk writes cleanly overwrite target output directories.
- [x] **Architectural Layering & Pipeline Constraints**: Preserves core 4 architectural layers (Knowledge, Runtime, Coaching, Projection). Validation operates as a cross-cutting quality gate, not a 5th layer.
- [x] **Human Sovereignty**: Machine recommendations (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`) and readiness labels (`HUMAN_REVIEW_REQUIRED`) leave `user_decision_state` (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`) under human control.
- [x] **Candidate-Agnostic Engine (FR-063)**: Production code, schemas, prompts, and validator rules contain ZERO hardcoded candidate entity names or evidence instances. Candidate scenarios exist strictly in external test fixtures.

## Project Structure

### Documentation (this feature)

```text
specs/003-upwork-proposal-refinement/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   ├── upwork-qualification-contract.md
│   ├── upwork-proposal-contract.md
│   └── upwork-validation-contract.md
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
skills/
├── upwork-qualification/
│   └── SKILL.md         # Extended with V3.1 7-dimension attribution & candidate-agnostic rules
└── upwork-proposal/
    └── SKILL.md         # Extended with attribution-bounded prose generation

scripts/
├── upwork_validator.py  # Extended with candidate-agnostic metadata shift & composition checks
├── generate_upwork_playbook.py
└── generate_upwork_biz_systems_playbook.py

tests/
└── test_upwork_proposal_generator.py # Extended with FR-058 & FR-059 parameterized test fixtures
```

**Structure Decision**: Single Python project layout leveraging existing `skills/`, `scripts/`, and `tests/` directories.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *Fully compliant with Constitution* | *N/A* |
