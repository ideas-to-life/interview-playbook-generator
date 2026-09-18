# Implementation Plan: Canonical Career Record Integration

**Branch**: `005-canonical-record-integration` | **Date**: 2026-09-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/005-canonical-record-integration/spec.md`

---

## Summary

Integrate `mind-palace/canonical/career-record.yaml` as the supreme authoritative source of professional facts for the Interview Playbook Generator. The technical approach:
1. Centralize canonical discovery and loading in a shared module (`scripts/canonical_loader.py`) configured via `candidate.canonical_record` in `config/config.yaml`.
2. Structurally exclude `quarantine/` directories from `portfolio-ingestor` (`scripts/ingest_portfolio.py`), preventing contaminated legacy data from entering `out/okf/sources/`.
3. Deprecate and remove legacy `Positions.csv` parsing, deriving `out/okf/employment-records.yaml` directly and exclusively from `career-record.yaml`.
4. Decouple factual selection (Activity A) from narrative projection (Activity B) by producing an intermediate runtime artifact `out/<target-slug>/runtime/canonical-selection.yaml` that locks selected `CAR-xx`, `EDU-xx`, and `CERT-xx` entries before projection skills execute.
5. Generate an explicit conflict audit report (`out/<target-slug>/runtime/canonical-conflict-report.yaml`) whenever secondary documents contain conflicting claims.
6. Enhance deterministic validation with automated sanitization (`scripts/employment_validator.py` and `projection-validator`), repairing output discrepancies back to canonical facts with alert logging.
7. Implement an automated regression test suite (`tests/test_canonical_record_regression.py`) covering all 8 mandatory forensic failure scenarios.

---

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: PyYAML (`yaml`), pytest (for test automation)  
**Storage**: File-based structured YAML (`canonical/career-record.yaml`, `out/okf/employment-records.yaml`, `out/<target-slug>/runtime/*.yaml`) and OKF Markdown documents  
**Testing**: pytest (`tests/test_canonical_record_regression.py`, `tests/test_career_evidence_integrity.py`)  
**Target Platform**: macOS / Linux CLI runtime environment  
**Project Type**: Knowledge Processing & Executive Projection Pipeline (CAS Skills framework)  
**Performance Goals**: Canonical record parsing in <500ms; fail-fast halting on missing/malformed records in <1s; full validation gate in <5s  
**Constraints**:
- Read-only access to `career-record.yaml`; zero generation feedback into the canonical record
- Zero fabrication: never invent numbers, titles, metrics, or credentials
- Quarantined documents 100% excluded from factual sourcing  
**Scale/Scope**: 1 canonical record (~25 roles, 5 degrees/certs, unresolved questions), ~15 downstream projection skills/views, 8 mandatory regression scenarios  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle / Gate | Compliance Status | Analysis & Enforcement |
|---|---|---|
| **I. Zero Fabrication & Claim Classification** | **PASS** | Canonical record establishes verified factual boundary; unevidenced claims prohibited; unresolved items omitted from external collateral. |
| **II. Footnote Attribution & OKF v0.2 Compliance** | **PASS** | All canonical entries maintain primary evidence citations (`CAR-xx`, `EDU-xx`); OKF v0.2 frontmatter preserved. |
| **III. Identity Preservation & Expression Tailoring** | **PASS** | Tailors expression and emphasis to target role while canonical identity remains immutable. Activity A (factual selection) strictly separated from Activity B (projection). |
| **IV. Career History & Evidence Integrity** | **PASS** | Job titles, employer relationships (e.g. Compugraf/Souza Cruz), dates, degrees (BSc vs MSc), and operational scopes are immutable. Unsupported role inflation prohibited. |
| **V. Idempotent Execution & Deterministic Pipeline** | **PASS** | Factual selection is persisted to `canonical-selection.yaml`; re-runs cleanly overwrite outputs; fast fail on missing inputs. |
| **Pre-Assembly & Release Quality Gates** | **PASS** | Automated validation with sanitization ensures zero unverified claims reach final collateral; regression suite enforces all 8 forensic scenarios. |

---

## Project Structure

### Documentation (this feature)

```text
specs/005-canonical-record-integration/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Architecture decisions & research
├── data-model.md        # Entity definitions & validation rules
├── quickstart.md        # End-to-end verification guide
├── contracts/           # Runtime YAML schema contracts
│   ├── canonical-selection-contract.yaml
│   └── canonical-conflict-report-contract.yaml
└── checklists/
    └── requirements.md  # Quality checklist (16/16 passing)
```

### Source Code (repository root)

```text
config/
└── config.yaml                          # Add candidate.canonical_record path

scripts/
├── canonical_loader.py                  # NEW: Discovery, validation & loading of career-record.yaml
├── canonical_selector.py                # NEW: Activity A factual selection -> canonical-selection.yaml
├── canonical_validator.py               # NEW: Conflict detection -> canonical-conflict-report.yaml
├── ingest_portfolio.py                  # MODIFIED: Enforce quarantine filter & generate employment-records.yaml from canonical
└── employment_validator.py              # MODIFIED: Include education/cert checks & automated sanitization

skills/
├── portfolio-ingestor/SKILL.md          # MODIFIED: Instruction updates for canonical record & quarantine exclusion
├── opportunity-analyzer/SKILL.md        # MODIFIED: Emit canonical-selection.yaml
├── projection-validator/SKILL.md        # MODIFIED: Wire automated sanitization & conflict logging
└── resume-projection/SKILL.md           # MODIFIED: Grounding strictly in canonical-selection.yaml

tests/
├── test_canonical_record_regression.py  # NEW: 8 mandatory regression scenarios (Scenarios 1-8)
└── test_career_evidence_integrity.py    # MODIFIED: Assert against canonical career record
```

**Structure Decision**: Single repository CLI & pipeline architecture. Reusable helper modules reside in `scripts/`, pipeline skill instructions in `skills/`, and test coverage in `tests/`.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No constitutional violations. All designs adhere strictly to zero-fabrication, immutable evidence integrity, and modular architectural layering.*
