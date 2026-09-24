# Implementation Plan: Projection Data Integrity & Provenance Remediation

**Branch**: `006-projection-data-integrity` | **Date**: 2026-09-24 | **Spec**: [specs/006-projection-data-integrity/spec.md](spec.md)

**Input**: Feature specification from `specs/006-projection-data-integrity/spec.md`

## Summary

Remediate the four integrity defects established in the September 2026 forensic diagnostic of the Tenth AI generation by implementing a strict 5-tier information-flow boundary:
1. Ensure complete, untruncated loading of `canonical-selection.yaml` (including education, certifications, and languages beyond line 50) into projection model context.
2. Enforce strict cross-opportunity runtime isolation and replace historical projection references with synthetic fact-free structural templates.
3. Partition ATS vocabulary in `opportunity-analyzer` into `candidate_evidenced_vocabulary` and `required_job_vocabulary`, removing optimization incentives to claim unevidenced client platforms.
4. Implement a unified deterministic validator in `scripts/projection_validator.py` executing a hybrid remediation model (automated sanitization of repairable canonical facts + hard build failure on un-sanitizable direct claims), outputting `out/<target-slug>/runtime/projection-validation-report.yaml`.
5. Establish a 10-scenario regression test suite in `tests/test_forensic_remediation_regression.py`.

## Technical Context

**Language/Version**: Python 3.10+ / Markdown / YAML  
**Primary Dependencies**: `pyyaml`, `pytest`  
**Storage**: File-based structured YAML (`canonical/career-record.yaml`, `out/<target-slug>/runtime/*.yaml`) and OKF Markdown documents (`out/okf/`, `out/<target-slug>/*.md`)  
**Testing**: `pytest` (`tests/test_forensic_remediation_regression.py`)  
**Target Platform**: macOS / Linux (POSIX CLI / Python runtime)  
**Project Type**: CLI / Multi-Agent Projection Pipeline & Deterministic Validation Framework  
**Performance Goals**: <5s execution for full deterministic validation audit; <1s context preparation  
**Constraints**: Read-only access to canonical facts; zero cross-opportunity leakage; zero fabrication; idempotent re-runs  
**Scale/Scope**: 10 diagnostic regression scenarios; ~15 projection artifacts per opportunity; full canonical selection loading (>50 lines, education, certs, languages, career)  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status | Notes |
|---|---|---|---|
| **I. Zero Fabrication & Absolute Claim Classification** | Are unevidenced technologies, dates, titles, and credentials prevented from entering projections? | **PASS** | ATS scoring rewards only verified terms; direct unevidenced claims trigger hard validation failure. |
| **II. Footnote Source Attribution & OKF v0.2 Compliance** | Are source attribution footnotes and OKF v0.2 compliance maintained? | **PASS** | Validates against canonical records and verified OKF cards without altering footnote bindings. |
| **III. Identity Preservation & Expression Tailoring** | Does tailoring alter expression while preserving canonical identity? | **PASS** | Target JD terms are partitioned as requirements/gaps; canonical identity is never redefined. |
| **IV. Career History & Evidence Integrity** | Are employers, formal titles, dates, degrees, and certifications protected against alteration? | **PASS** | Post-generation validator verifies and sanitizes education dates (1988–1991), titles, certs, and languages. |
| **V. Idempotent Execution & Deterministic Pipeline** | Is execution deterministic, idempotent, and backed by automated gates? | **PASS** | Validation runs deterministically in Python without LLM nondeterminism; output files touch disk cleanly. |

## Project Structure

### Documentation (this feature)

```text
specs/006-projection-data-integrity/
├── plan.md              # This implementation plan
├── research.md          # Architectural research & design decisions
├── data-model.md        # Entity definitions & validation lifecycle
├── quickstart.md        # End-to-end execution & validation guide
├── contracts/
│   ├── projection-validation-report-contract.yaml # Report schema
│   └── ats-vocabulary-partition-contract.yaml     # ATS vocabulary schema
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
scripts/
├── projection_validator.py             # NEW: Unified deterministic factual validator & sanitizer
├── canonical_selector.py              # ENHANCED: Full canonical selection context generation
├── canonical_loader.py                # Preserved: Read-only career-record.yaml loader
└── employment_validator.py            # Preserved/Refactored to delegate to projection_validator

templates/projections/
├── resume-executive.template.md       # NEW: Fact-free synthetic structural template
├── resume-ats.template.md             # NEW: Fact-free synthetic structural template
├── cover-letter.template.md           # NEW: Fact-free synthetic structural template
└── linkedin-profile.template.md       # NEW: Fact-free synthetic structural template

skills/
├── opportunity-analyzer/SKILL.md      # UPDATED: Evidence-partitioned ATS vocabulary
├── resume-projection/SKILL.md         # UPDATED: Full canonical context loading & synthetic templates
├── cover-letter-projection/SKILL.md   # UPDATED: Full canonical context loading & synthetic templates
├── linkedin-projection/SKILL.md       # UPDATED: Full canonical context loading & synthetic templates
└── projection-validator/SKILL.md      # UPDATED: Invoke scripts/projection_validator.py

tests/
├── test_forensic_remediation_regression.py # NEW: 10 diagnostic failure scenarios
└── test_canonical_selection_contract.py    # UPDATED: Verify >50 lines context loading
```

**Structure Decision**: The implementation enhances existing pipeline scripts in `scripts/`, introduces neutral structural templates in `templates/projections/`, updates skill prompt contracts in `skills/`, and adds a dedicated regression test module in `tests/`.

## Complexity Tracking

*No constitutional violations identified. Complexity remains minimal and adheres to existing Python/YAML pipeline architecture.*
