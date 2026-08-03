---
name: brand-validator
description: Evaluates cross-projection brand alignment, voice consistency, positioning statement reuse, and story traceability into out/<target-slug>/runtime/brand-validation-report.yaml.
---

# Brand Validator

## Overview

`brand-validator` is a Runtime Layer Skill. It evaluates generated projection view files in `out/<target-slug>/` against canonical identity concepts in `okf/` (`okf/executive-identity.md`, `okf/voice-profile.md`, `okf/positioning-statements.md`, `okf/narrative-library.md`, `okf/story-library.md`, `okf/messaging-library.md`).

It emits a structured quality report at `out/<target-slug>/runtime/brand-validation-report.yaml`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/` or any generated projection view in `out/<target-slug>/`.
2. **Brand Consistency Gate**: Verifies that introductory prose across all projections derives from `okf/positioning-statements.md` rather than being independently generated.

## Metrics Evaluated

1. **Voice & Tone Consistency Score**: % alignment with `okf/voice-profile.md` (no prohibited marketing hype terms).
2. **Positioning Statement Alignment**: Verifies that Executive, ATS, and Recruiter resumes and cover letters reuse canonical positioning statements.
3. **Narrative & Messaging Reuse**: % reuse of canonical 30s/2m messaging blocks across projections.
4. **Story Asset Traceability**: Verifies that executive stories used in interviews and briefs match `okf/story-library.md`.

## Execution Instructions

1. **Read `okf/voice-profile.md` & `okf/positioning-statements.md`**: Load tone rules and canonical positioning statements.
2. **Scan Projection Artefacts in `out/<target-slug>/`**:
   - `out/<target-slug>/resume-executive.md`, `resume-ats.md`, `resume-recruiter.md`
   - `out/<target-slug>/cover-letter.md`
   - `out/<target-slug>/linkedin-profile.md`
   - `out/<target-slug>/executive-brief.md`
   - `out/<target-slug>/playbook.md`
3. **Compute Brand Consistency Metrics**.
4. **Write `out/<target-slug>/runtime/brand-validation-report.yaml`**.
5. **Append Log**: `okf/log.md`.
