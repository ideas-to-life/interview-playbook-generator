# Interface Contract: Upwork Validation (V3.1)

## Overview

Defines the validation contract enforced by `scripts/upwork_validator.py` as a cross-cutting quality gate.

---

## Inputs

- `out/<target-slug>/upwork-qualification-report.md`
- `out/<target-slug>/upwork-screening-answers.md`
- `out/<target-slug>/upwork-work-samples.md`
- `out/<target-slug>/runtime/upwork-qualification.yaml`

---

## Outputs

- `out/<target-slug>/runtime/upwork-validation-report.yaml`

---

## Validation Checks Performed

1. **Attribution Shift Validation (FR-052, FR-053)**: Detects unsupported transitions (platform → candidate, team → candidate, architecture → implementation, prototype → production, proposed → historical, context A → context B).
2. **Production Claim Validation (FR-054)**: Verifies that client-facing claims of candidate production implementation possess matching candidate production deployment evidence (`candidate_production_deployment_status == verified_production`).
3. **Evidence Composition Validation (FR-055)**: Flags attempts to satisfy a single historical requirement by combining separate evidence contexts into an unsupported composite assertion.
4. **Screening / Qualification Consistency Validation (FR-056)**: Fails any package where a screening answer asserts an affirmative historical claim for an unresolved requirement (`PARTIALLY_SUPPORTED`, `UNKNOWN`, `CONTRADICTED`).
5. **Work Sample Narrative Consistency Validation (FR-057)**: Verifies consistency across `project_type`, `production_status`, `candidate_contribution`, and summary narrative.
6. **Assertion-Then-Disclaimer Validation (FR-049)**: Detects prohibited patterns of assertive claims followed by disclaimers.
7. **Clean Prose Validation**: Ensures zero internal diagnostic tags or footnotes leak into client-facing proposal prose.
