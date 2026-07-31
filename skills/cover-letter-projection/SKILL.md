---
name: cover-letter-projection
description: Generates a 1-page executive cover letter from canonical OKF knowledge and shared opportunity analysis.
---

# Cover Letter Projection

## Overview

`cover-letter-projection` is a Projection Layer Skill. It reads the canonical OKF bundle (`okf/`) and the shared execution context at `out/runtime/opportunity-analysis.yaml` to generate a 1-page executive cover letter at `out/cover-letter.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Length Constraint**: Strictly maximum 1 page (≤500 words).
3. **Traceable**: Grounded in canonical OKF evidence cards and signature achievements.

## Section Structure

1. **Header & Date**: Candidate contact & target company details.
2. **Motivation & Executive Positioning**: Direct hook addressing target role hiring goals.
3. **Strategic Alignment**: How core capabilities match target priorities.
4. **Selected Evidence**: Highlighting 2–3 key signature achievements.
5. **Closing & Value Proposition**: 90-day execution promise and call to action.

## Execution Instructions

1. **Read `out/runtime/opportunity-analysis.yaml`**: Extract company, role_title, hiring_goals, executive_positioning, capability_priorities, and coverage_matrix.
2. **Walk Canonical Knowledge**: Read `okf/evidence/*.md` and `okf/signature-achievements.md`.
3. **Render Cover Letter (`out/cover-letter.md`)**.
4. **Append Log**: `okf/log.md`.
