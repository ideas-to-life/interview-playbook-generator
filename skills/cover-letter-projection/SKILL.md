---
name: cover-letter-projection
description: Generates a 1-page executive cover letter from canonical OKF knowledge, Executive Identity, and shared opportunity analysis.
---

# Cover Letter Projection

## Overview

`cover-letter-projection` is a Projection Layer Skill. It reads the canonical OKF bundle (`okf/`, including `okf/messaging-library.md` and `okf/story-library.md`) and the shared execution context at `out/<target-slug>/runtime/opportunity-analysis.yaml` to generate a 1-page executive cover letter at `out/<target-slug>/cover-letter.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Canonical Positioning**: Adapt opening paragraph from `okf/messaging-library.md` (`30-Second Introduction`). Do NOT generate independent positioning prose.
3. **Length Constraint**: Strictly maximum 1 page (≤500 words).
4. **Traceable**: Grounded in canonical OKF evidence cards and signature achievements.

## Section Structure

1. **Header & Date**: Candidate contact & target company details.
2. **Motivation & Executive Positioning**: Adapted from `okf/messaging-library.md`.
3. **Strategic Alignment**: How core capabilities match target priorities.
4. **Selected Evidence**: Highlighting 2–3 key stories from `okf/story-library.md`.
5. **Closing & Value Proposition**: 90-day execution promise and call to action.

## Execution Instructions

1. **Read `okf/messaging-library.md` & `okf/story-library.md`**: Extract canonical 30s intro and executive story assets.
2. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**: Extract company, role_title, hiring_goals, capability_priorities, and coverage_matrix.
3. **Render Cover Letter (`out/<target-slug>/cover-letter.md`)**.
4. **Append Log**: `okf/log.md`.
