---
name: projection-validator
description: Evaluates generated projection artefacts across evidence coverage, capability alignment, ATS vocabulary density, and readability, generating out/runtime/projection-validation-report.yaml.
---

# Projection Validator

## Overview

`projection-validator` is a Runtime Layer Skill. It audits all generated projection view files in `out/` against `out/runtime/opportunity-analysis.yaml` and canonical `okf/` evidence, emitting a structured quality report at `out/runtime/projection-validation-report.yaml`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/` or any generated projection view in `out/`.
2. **Deterministic Quality Flywheel**: Calculates objective metrics for evidence traceability, ATS term inclusion, capability coverage, and readability.

## Metrics Evaluated

1. **Evidence Traceability**: Percentage of non-heading lines backed by OKF evidence cards or footnotes.
2. **Capability Alignment Score**: Ratio of prioritized capabilities represented in projections.
3. **ATS Vocabulary Coverage**: Coverage percentage of `mandatory` and `strong` terms from `out/runtime/opportunity-analysis.yaml`.
4. **Length & Budget Compliance**: Verifies page/word count budget constraints (e.g. Cover Letter ≤ 500 words, Executive Brief ≤ 2,500 words).

## Execution Instructions

1. **Read `out/runtime/opportunity-analysis.yaml`**: Load ATS vocabulary, capability priorities, and coverage matrix.
2. **Scan Projection Artefacts in `out/`**:
   - `out/resume-executive.md`, `out/resume-ats.md`, `out/resume-recruiter.md`
   - `out/cover-letter.md`
   - `out/linkedin-profile.md`
   - `out/executive-brief.md`
   - `out/opportunity-alignment.md`
   - `out/playbook.md`
3. **Compute Metrics & Validation Scores**.
4. **Write `out/runtime/projection-validation-report.yaml`**.
5. **Append Log**: `okf/log.md`.
