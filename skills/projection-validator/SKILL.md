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

## Execution Instructions

1. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**.
2. **Scan Projection Artefacts in `out/<target-slug>/`**.
3. **Compute Quality Metrics**.
4. **Write `out/<target-slug>/runtime/projection-validation-report.yaml`**.
5. **Append Log**: `okf/log.md`.
