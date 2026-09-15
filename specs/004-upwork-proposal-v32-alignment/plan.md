# Implementation Plan: Upwork Proposal Generator — V3.2 Contract Alignment & Fixture Projection Refinement

**Branch**: `004-upwork-proposal-v32-alignment` | **Date**: 2026-09-15 | **Spec**: [`specs/004-upwork-proposal-v32-alignment/spec.md`](spec.md)

**Input**: Feature specification from `specs/004-upwork-proposal-v32-alignment/spec.md`

## Summary

Refines and aligns the offline Upwork proposal generator (`scripts/generate_upwork_biz_systems_playbook.py` and sibling scripts) with the canonical `skills/upwork-proposal/SKILL.md` projection contract. Resolves the forensic finding where `upwork-qualification-report.md` contained a static 3-line verdict stub while the Executive Proposal Cover Letter was misplaced inside `upwork-screening-answers.md`. Ensures `upwork-qualification-report.md` contains the 350–500 word Executive Proposal Cover Letter, `upwork-screening-answers.md` contains screening Q&A only, and header metadata binds dynamically to `out/<target-slug>/runtime/upwork-qualification.yaml`.

---

## Technical Context

**Language/Version**: Python 3.13 / PyYAML / pytest  
**Primary Dependencies**: PyYAML, pytest  
**Storage**: Disk files (`out/<target-slug>/`, `out/<target-slug>/runtime/`, `out/okf/`)  
**Testing**: pytest (`~/.pyenv/shims/pytest -v`)  
**Target Platform**: macOS / Linux CLI runtime  
**Project Type**: CLI application / Python pipeline generator  
**Performance Goals**: Deterministic file generation < 5 seconds  
**Constraints**: Zero fabrication, 100% clean client prose pass, strictly candidate-agnostic engine, 100% pass rate across 151 existing regression tests.  
**Scale/Scope**: 1 generator script (`scripts/generate_upwork_biz_systems_playbook.py`), 1 projection contract (`skills/upwork-proposal/SKILL.md`), 1 validator (`scripts/upwork_validator.py`), 1 test suite (`tests/test_upwork_proposal_generator.py`).  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Principle I: Zero Fabrication & Claim Classification**: PASS. Generated proposal copy remains 100% evidence-grounded and free of unevidenced metrics or candidate production inflation.
2. **Principle II: Footnote Source Attribution & OKF v0.2 Compliance**: PASS. All frontmatter and OKF source references comply with OKF v0.2 spec.
3. **Principle III: Identity Preservation & Expression Tailoring**: PASS. Tailors expression to target opportunity without altering canonical professional identity.
4. **Principle IV: Career History & Evidence Integrity**: PASS. Employment history facts are immutable; candidate-agnostic attribution shift checks enforced.
5. **Principle V: Idempotent Execution & Deterministic Pipeline**: PASS. Idempotent re-runs write updated timestamps cleanly to disk.

---

## Project Structure

### Documentation (this feature)

```text
specs/004-upwork-proposal-v32-alignment/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── upwork-proposal-contract-v32.md
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
scripts/
├── generate_upwork_biz_systems_playbook.py   # Primary offline generator script to update
├── generate_upwork_playbook.py               # Standalone playbook generator reference
├── upwork_validator.py                       # Upwork proposal validation module
└── ingest_portfolio.py                       # Portfolio ingestion script

skills/
├── upwork-proposal/
│   └── SKILL.md                              # Canonical Upwork Proposal Projection Skill
├── upwork-qualification/
│   └── SKILL.md                              # Runtime qualification skill
└── projection-registry/
    └── SKILL.md                              # Projection registry orchestrator

tests/
├── test_upwork_proposal_generator.py          # Regression test suite for Upwork proposals
└── test_v06_success_criteria.py               # Success criteria verification suite
```

**Structure Decision**: Standard repository structure. Modifies `scripts/generate_upwork_biz_systems_playbook.py` and updates test coverage in `tests/test_upwork_proposal_generator.py`.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *N/A* | *No constitution violations* |
