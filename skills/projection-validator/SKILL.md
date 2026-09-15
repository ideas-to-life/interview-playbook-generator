---
name: projection-validator
description: Evaluates generated projection artefacts across evidence coverage, capability alignment, ATS vocabulary density, and readability, generating out/<target-slug>/runtime/projection-validation-report.yaml.
---

# Projection Validator

## Overview

`projection-validator` is a Runtime Layer Skill. It evaluates generated projection view files in `out/<target-slug>/` against canonical OKF knowledge and shared opportunity context (`out/<target-slug>/runtime/opportunity-analysis.yaml`).

It emits a structured quality report at `out/<target-slug>/runtime/projection-validation-report.yaml`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/` or any generated projection view.

## Metrics Evaluated

1. **Evidence Coverage Score**: % of claims in projections tracing to `okf/` evidence.
2. **Capability Alignment Score**: Alignment of highlighted experience with target capability priorities.
3. **Claim Scope & Strength Validation**: Verifies $\text{ClaimScope} \le \text{EvidenceScope}$ across Ownership, Scope, Domain, Specificity, Duration, and Seniority. Reports `PASS`, `DOWNGRADE`, or `REJECT` status for evaluated claims.
4. **ATS Vocabulary Density**: % of mandatory and strong ATS keywords present in `resume-ats.md`.
5. **Readability & Word Count**: Word count budget compliance across projections.
6. **Employment History Evidence Integrity**: Deterministically evaluates generated projection views against `okf/employment-records.yaml` using `scripts/employment_validator.py`. Reports `PASS` or `FAIL` status with explicit violation trace.
7. **Upwork Proposal & Provenance Validation (V2.1)**:
   - **Semantic Evidence Support Check**: Verify that 100% of client-facing claims have actual semantic evidence support in canonical OKF evidence cards, not merely an entry in `claim_traceability`.
   - **Zero Fabrication & Clean Prose Pass**: Confirm client-facing `upwork-qualification-report.md` is 100% free of internal tags (`[evidence]`, `[inference]`), footnotes (`[^source-id]`), or `[OPEN CONDITION]` diagnostic markers.
   - **Contradiction & Production Inflation Pass**: Reject any client-facing claim asserting satisfaction of a requirement classified as `CONTRADICTED`, or claiming `verified_production` when production status is `unknown` or `verified_non_production`.
   - **Submission Readiness Alignment**: Confirm that `submission_readiness` is set to `HUMAN_REVIEW_REQUIRED` whenever 1+ material requirements are `UNKNOWN` or `PARTIALLY_SUPPORTED`.
   - **Word Count Budget**: Validate proposal word count (350–500 words target).

## Execution Instructions

1. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**.
2. **Scan Projection Artefacts in `out/<target-slug>/`** (including `upwork-qualification-report.md`, `upwork-screening-answers.md`, `upwork-work-samples.md` when present).
3. **Compute Quality Metrics** (including Upwork internal provenance and gate compliance).
4. **Write `out/<target-slug>/runtime/projection-validation-report.yaml`**.
5. **Append Log**: `okf/log.md`.
