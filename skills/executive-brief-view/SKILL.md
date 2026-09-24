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
3. **Immutable Career Timeline**: Any background career summary or timeline references to employer names, job titles, or employment dates must strictly match `out/<target-slug>/runtime/canonical-selection.yaml` (and `okf/employment-records.yaml`).
4. **Full Canonical Context Invariant**: The generator MUST load the complete, untruncated `out/<target-slug>/runtime/canonical-selection.yaml` (including education, certifications, and languages) into context.
5. **Cross-Opportunity Isolation Invariant**: The generator MUST NEVER read, inspect, or use prior opportunity directories under `out/<other-target-slug>/`. Derive all context strictly from canonical OKF and active opportunity runtime files.
6. **Target Terminology Evidence Boundary**: Unevidenced target-position keywords must never be presented as candidate capabilities or past experience.

## Execution Instructions

1. **Read Shared Execution Context & Canonical Selection**: Read `out/<target-slug>/runtime/opportunity-analysis.yaml` and load 100% of `out/<target-slug>/runtime/canonical-selection.yaml` into context. Extract target company, role, interviewer, and hiring goals. DO NOT inspect other opportunity directories.
2. **Read Canonical OKF Knowledge**: Read `okf/executive-identity.md`, `okf/positioning-statements.md`, `okf/story-library.md`, `okf/interview-strategy.md`, and `okf/knowledge-gaps.md`.
3. **Render Executive Brief (`out/<target-slug>/executive-brief.md`)**.
4. **Append Log**: `okf/log.md`.
