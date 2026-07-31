---
name: resume-projection
description: Generates executive, ATS, and recruiter resume variants from canonical OKF knowledge and shared opportunity analysis.
---

# Resume Projection

## Overview

`resume-projection` is a Projection Layer Skill. It reads the canonical OKF bundle (`okf/`) and the shared execution context at `out/runtime/opportunity-analysis.yaml` to generate tailored resume projection variants in `out/`:

1. **Executive Resume** (`out/resume-executive.md`): Strategic positioning, 2 pages, capability progression, high-impact leadership outcomes.
2. **ATS Resume** (`out/resume-ats.md`): Structured standard headers, explicit ATS vocabulary keyword placement, clear reverse-chronological format.
3. **Recruiter Resume** (`out/resume-recruiter.md`): 1-page high-density executive summary briefing for talent acquisition.

By default, all three variants are generated. If `config/config.yaml` specifies `projections.resume.variant`, only the selected variant is generated.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **No Duplicated Reasoning**: Consume capability priorities and ATS vocabulary from `out/runtime/opportunity-analysis.yaml`.
3. **Evidence-backed**: Every achievement, role description, and metric must trace back to canonical OKF evidence cards or achievements.

## Execution Instructions

1. **Read `out/runtime/opportunity-analysis.yaml`**: Extract `executive_positioning`, `capability_priorities`, `ats_vocabulary`, and `coverage_matrix`.
2. **Walk Canonical Knowledge**: Read `okf/evidence/*.md`, `okf/achievements/*.md`, `okf/capabilities/*.md`, and `okf/behaviour-profile.md`.
3. **Render Executive Resume (`out/resume-executive.md`)**:
   - Executive Summary aligned with `executive_positioning`
   - Core Capability Pillars mapped to `capability_priorities`
   - Selected Signature Achievements with quantifiable impact
   - Experience History (reverse-chronological)
4. **Render ATS Resume (`out/resume-ats.md`)**:
   - Explicit keyword density incorporating `ats_vocabulary.mandatory` and `ats_vocabulary.strong`
   - Standard section headings (Summary, Core Competencies, Professional Experience, Education)
5. **Render Recruiter Resume (`out/resume-recruiter.md`)**:
   - 1-page high-impact briefing highlighting executive positioning, top 3 signature achievements, and contact summary.
6. **Append Log**: `okf/log.md`.
