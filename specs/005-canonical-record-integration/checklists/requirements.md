# Specification Quality Checklist: Canonical Career Record Integration

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-09-18
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- Clarifications resolved (Session 2026-09-18):
  1. Unresolved questions: Unconditionally omitted from external collateral (CVs, cover letters, proposals, LinkedIn profiles); surfaced in internal coaching materials with `[NEEDS CONFIRMATION]`.
  2. Conflict reporting: Emit structured conflict audit report at `out/<target-slug>/runtime/canonical-conflict-report.yaml` logging discrepancies for future cleanup without blocking execution.
  3. Factual selection stage: Executed during runtime opportunity analysis, persisting selected canonical entries (`CAR-xx`, `EDU-xx`) to `out/<target-slug>/runtime/canonical-selection.yaml`.
  4. Legacy parsing: Complete deprecation and removal of `Positions.csv` parsing from `portfolio-ingestor`; all employment records in `out/okf/employment-records.yaml` originate strictly from `career-record.yaml`.
  5. Validation action on discrepancies: Automated sanitization rewrites offending text in generated output back to canonical truth while recording an alert in `projection-validation-report.yaml`.
  6. Configuration path: Centralized under `candidate.canonical_record: "canonical/career-record.yaml"` in `config/config.yaml`.
- All quality criteria pass (16/16 items). Specification is fully verified and ready for `/speckit-plan`.
