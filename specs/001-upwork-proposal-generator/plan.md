# Implementation Plan: Upwork Qualification and Proposal Generator

**Branch**: `001-upwork-proposal-generator` | **Date**: 2026-09-10 | **Spec**: [specs/001-upwork-proposal-generator/spec.md](specs/001-upwork-proposal-generator/spec.md)

**Input**: Feature specification from `specs/001-upwork-proposal-generator/spec.md` (refinement v1)

## Summary

Add Upwork opportunity qualification and proposal generation capability to the platform as a governed projection of existing OKF career evidence. The feature implements a 4-stage processing pipeline conforming to the repository's 4-layer architecture: Opportunity Analysis → Qualification (`skills/upwork-qualification/SKILL.md` in Runtime Layer) → Proposal Strategy → Proposal Projection (`skills/upwork-proposal/SKILL.md` in Projection Layer). Qualification enforces strict hard evidence-integrity rules (`APPLY`, `CONDITIONAL`, `DO NOT APPLY`) and explicit `proposal_generation` control semantics (`allowed`, `allowed_with_conditions`, `blocked`). Proposal text is rendered clean of internal metadata markup (`[evidence]` tags, `[^source-id]` footnotes) for direct marketplace submission, while `out/<target-slug>/runtime/upwork-qualification.yaml` stores 100% machine-readable `claim_traceability` for automated validation via `projection-validator`.

## Technical Context

**Language/Version**: Python 3.11+, Markdown (OKF v0.2), YAML

**Primary Dependencies**: PyYAML, Jinja2, pytest

**Storage**: File-based pipeline state (`out/okf/`, `out/<target-slug>/runtime/`, `out/<target-slug>/`)

**Testing**: Pytest (`tests/test_upwork_proposal_generator.py`) + automated validation via `skills/projection-validator/SKILL.md`

**Target Platform**: CLI / Local agent execution runtime

**Project Type**: Agentic Pipeline & Executive Communication Projection Platform

**Performance Goals**: Qualification & proposal generation completed in < 30 seconds per opportunity

**Constraints**: Zero fabrication, 100% internal claim traceability (`claim_traceability` array in `upwork-qualification.yaml`); clean proposal prose for marketplace submission; proposal length target 350-500 words.

**Scale/Scope**: 1 target opportunity per run; up to 3 work samples; 100% test coverage across APPLY, CONDITIONAL, and DO NOT APPLY scenarios.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Zero Fabrication & Absolute Claim Classification**: All generated proposal prose uses internal claim traceability (`claim_traceability` array) with `[assumption]` markers for missing values.
- [x] **II. Footnote Source Attribution & OKF v0.2 Compliance**: Every claim maps to an authoritative source entry in OKF v0.2 evidence cards.
- [x] **III. Identity Preservation & Expression Tailoring**: Tailors expression to target opportunity without altering canonical identity.
- [x] **IV. Career History & Evidence Integrity**: Employment facts are immutable. Personal/prototype projects cannot satisfy explicit client production implementation requirements.
- [x] **V. Idempotent Execution & Deterministic Pipeline**: Clean file overwrite in `out/<target-slug>/` on each run.

## Project Structure

### Documentation (this feature)

```text
specs/001-upwork-proposal-generator/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── qualification-skill-contract.md
│   ├── proposal-projection-contract.md
│   └── validation-contract.md
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code (repository root)

```text
skills/
├── upwork-qualification/
│   └── SKILL.md         # Runtime Layer qualification skill
├── upwork-proposal/
│   └── SKILL.md         # Projection Layer proposal skill
├── projection-registry/
│   └── SKILL.md         # Updated to register upwork-proposal
├── playbook-orchestrator/
│   └── SKILL.md         # Updated to execute upwork-qualification & proposal projection
└── projection-validator/
    └── SKILL.md         # Updated to validate upwork proposals & screening answers via runtime trace

tests/
├── test_upwork_proposal_generator.py # Unit and integration test suite
└── golden/
    └── upwork/          # Golden snapshot test outputs
```

**Structure Decision**: Standard repository Skill layout under `skills/` and test suites under `tests/`.

## Plan Phases

### Phase 0: Research & Alignment (Completed)
- Resolved architectural placement (`upwork-qualification` in Runtime, `upwork-proposal` in Projection).
- Defined qualification taxonomy (direct/adjacent/transferable/absent; verified_production/verified_non_production) and `proposal_generation` control state.
- Established clean proposal prose rule for client submission and internal `claim_traceability` in YAML.
- Extended `projection-validator` for internal runtime provenance validation.

### Phase 1: Design & Contracts (Completed)
- Created `data-model.md` defining YAML and Markdown schemas.
- Created `contracts/` defining Skill contracts for qualification, projection, and validation.
- Created `quickstart.md` defining runnable validation scenarios (`APPLY`, `CONDITIONAL`, `DO NOT APPLY`).

### Phase 2: Tasks & Implementation (Pending `/speckit-tasks`)
- Task breakdown for `skills/upwork-qualification/SKILL.md`.
- Task breakdown for `skills/upwork-proposal/SKILL.md`.
- Registry and orchestrator integration updates.
- Validator skill updates and pytest test suite `tests/test_upwork_proposal_generator.py`.
