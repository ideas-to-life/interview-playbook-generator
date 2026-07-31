---
name: resume-projection
description: Generates executive, ATS, and recruiter resume variants from canonical OKF knowledge, Executive Identity, and shared opportunity analysis.
---

# Resume Projection

## Overview

`resume-projection` is a Projection Layer Skill. It reads the canonical OKF bundle (`okf/`, including `okf/positioning-statements.md`), and the shared execution context at `out/runtime/opportunity-analysis.yaml` to generate tailored resume projection variants in `out/`:

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
2. **Canonical Positioning**: Adapt introductory summary directly from `okf/positioning-statements.md` (`Executive Variant`). Do NOT generate independent positioning prose.
3. **Evidence-backed**: Every achievement, role description, and metric must trace back to canonical OKF evidence cards or achievements.

## Execution Instructions

1. **Read `okf/positioning-statements.md`**: Adapt canonical `Executive Variant`.
2. **Read `out/runtime/opportunity-analysis.yaml`**: Extract `capability_priorities`, `ats_vocabulary`, and `coverage_matrix`.
3. **Walk Canonical Knowledge**: Read `okf/evidence/*.md`, `okf/achievements/*.md`, `okf/capabilities/*.md`, and `okf/behaviour-profile.md`.
4. **Render Executive Resume (`out/resume-executive.md`)**.
5. **Render ATS Resume (`out/resume-ats.md`)**.
6. **Render Recruiter Resume (`out/resume-recruiter.md`)**.
7. **Append Log**: `okf/log.md`.
