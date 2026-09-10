# Implementation Plan: Upwork Qualification, Evidence Integrity Controls, and Proposal Generator

**Branch**: `001-upwork-proposal-generator` | **Date**: 2026-09-10 | **Spec**: [specs/001-upwork-proposal-generator/spec.md](specs/001-upwork-proposal-generator/spec.md)

**Input**: Feature specification V2.0 from `specs/001-upwork-proposal-generator/spec.md` (Refined for Evidence Integrity & Production Qualification Controls)

## Summary

Add Upwork opportunity qualification and proposal generation capability to the platform as a governed projection over canonical OKF career evidence. The feature implements a 4-stage processing pipeline conforming strictly to the repository's 4-layer architecture: Opportunity Analysis $\rightarrow$ Qualification (`skills/upwork-qualification/SKILL.md` in Runtime Layer) $\rightarrow$ Proposal Strategy $\rightarrow$ Proposal Projection (`skills/upwork-proposal/SKILL.md` in Projection Layer). 

Refinement V2.0 enforces machine-readable evidence integrity (`organisation.id`, `project.id`, `environment`, `production_verified`, `implementation_role`), strict explicit-only card metadata population (zero contextual inheritance during migration), negative inference prohibitions (prohibiting production inference from repo names, latency metrics, or company names), cross-organisation and cross-project isolation, and strict dealbreaker gates (`UNKNOWN` $\rightarrow$ `DO NOT APPLY`). Proposal prose is rendered clean of internal metadata markup (`[evidence]` tags, `[^source-id]` footnotes) for direct marketplace submission, while `out/<target-slug>/runtime/upwork-qualification.yaml` stores 100% machine-readable `claim_traceability` for automated, independent validation via `skills/projection-validator/SKILL.md`.

## Technical Context

**Language/Version**: Python 3.11+, Markdown (OKF v0.2), YAML

**Primary Dependencies**: PyYAML, Jinja2, pytest

**Storage**: File-based pipeline state (`out/okf/`, `out/<target-slug>/runtime/`, `out/<target-slug>/`)

**Testing**: Pytest (`tests/test_upwork_proposal_generator.py`, `tests/test_projection_validator.py`) + automated validation via `skills/projection-validator/SKILL.md`

**Target Platform**: CLI / Local agent execution runtime

**Project Type**: Agentic Pipeline & Executive Communication Projection Platform

**Performance Goals**: Qualification & proposal generation completed in < 30 seconds per opportunity

**Constraints**: Zero fabrication; 100% internal claim traceability (`claim_traceability` array in `upwork-qualification.yaml`); clean proposal prose for marketplace submission; proposal length target 350-500 words; strict negative inference rules (no repo name or metric inference); explicit dealbreaker gate (`UNKNOWN` $\rightarrow$ `DO NOT APPLY`).

**Scale/Scope**: 1 target opportunity per run; up to 3 work samples; 100% test coverage across 10 regression scenarios.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Zero Fabrication & Absolute Claim Classification**: All generated proposal prose uses internal claim traceability (`claim_traceability` array) with `[assumption]` markers for missing values.
- [x] **II. Footnote Source Attribution & OKF v0.2 Compliance**: Every claim maps to an authoritative source entry in OKF v0.2 evidence cards. Machine-readable frontmatter metadata extended cleanly.
- [x] **III. Identity Preservation & Expression Tailoring**: Tailors expression to target opportunity without altering canonical identity.
- [x] **IV. Career History & Evidence Integrity**: Employment facts are immutable. Personal/prototype/lab projects CANNOT satisfy explicit client production implementation requirements. Cross-organisation and cross-project isolation strictly enforced.
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
├── evidence-card-generator/
│   └── SKILL.md         # Updated to emit machine-readable frontmatter metadata
├── upwork-qualification/
│   └── SKILL.md         # Runtime Layer qualification skill with contract v1 predicates
├── upwork-proposal/
│   └── SKILL.md         # Projection Layer proposal skill respecting dealbreaker gates
├── projection-registry/
│   └── SKILL.md         # Updated to register upwork-proposal
├── playbook-orchestrator/
│   └── SKILL.md         # Updated to execute upwork-qualification & proposal projection
└── projection-validator/
    └── SKILL.md         # Updated for independent validation of production status frontmatter

scripts/
└── generate_upwork_playbook.py # Updated runtime script generator for Upwork targets

tests/
├── test_upwork_proposal_generator.py # Unit and integration test suite (10 regression scenarios)
└── golden/
    └── upwork/          # Golden snapshot test outputs
```

**Structure Decision**: Standard repository Skill layout under `skills/` and test suites under `tests/`.

## Plan Phases

### Phase 0: Research & Alignment (Completed)
- Resolved architectural placement (`upwork-qualification` in Runtime, `upwork-proposal` in Projection).
- Defined machine-readable evidence contract (`organisation.id`, `project.id`, `environment`, `production_verified`, `implementation_role`).
- Formulated 15 negative inference rules prohibiting production inference from repo names, metrics, or company names.
- Established cross-organisation and cross-project isolation boundaries.
- Defined dealbreaker gate rules (`UNKNOWN` $\rightarrow$ `DO NOT APPLY`).
- Extended `projection-validator` for independent validation against canonical OKF evidence frontmatter.

### Phase 1: Design & Contracts (Completed)
- Updated `data-model.md` defining OKF EvidenceCard YAML frontmatter schema, `upwork-qualification.yaml` schema, and Markdown presentation schemas.
- Updated `contracts/` defining Skill contracts for qualification (`qualification-skill-contract.md`), proposal projection (`proposal-projection-contract.md`), and validation (`validation-contract.md`).
- Updated `quickstart.md` defining runnable validation scenarios across all 10 regression test cases.

### Phase 2: Tasks & Implementation (Pending `/speckit-tasks`)
- Task breakdown for `skills/evidence-card-generator/SKILL.md` frontmatter schema update.
- Task breakdown for `skills/upwork-qualification/SKILL.md` predicate implementation.
- Task breakdown for `skills/upwork-proposal/SKILL.md` dealbreaker gate handling.
- Task breakdown for `scripts/generate_upwork_playbook.py` updates.
- Task breakdown for `skills/projection-validator/SKILL.md` independent verification updates.
- Task breakdown for `tests/test_upwork_proposal_generator.py` (10 regression scenarios).
