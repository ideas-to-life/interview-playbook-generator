---
name: executive-brief-view
description: Walks the whole bundle to produce a 10-minute pre-interview brief at out/<target-slug>/executive-brief.md.
---

# Executive Brief View

## Overview

`executive-brief-view` is a Projection Layer Skill. It reads canonical OKF knowledge and shared opportunity context (`out/<target-slug>/runtime/opportunity-analysis.yaml`) to compile a high-density 10-minute pre-interview preparation document at `out/<target-slug>/executive-brief.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Word Budget**: Maximum 1,200 words total across 11 standard sections.

## Execution Instructions

1. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**: Extract target company, role, interviewer, and hiring goals.
2. **Read Canonical OKF Knowledge**: Read `okf/executive-identity.md`, `okf/positioning-statements.md`, `okf/story-library.md`, `okf/interview-strategy.md`, and `okf/knowledge-gaps.md`.
3. **Render Executive Brief (`out/<target-slug>/executive-brief.md`)**.
4. **Append Log**: `okf/log.md`.
