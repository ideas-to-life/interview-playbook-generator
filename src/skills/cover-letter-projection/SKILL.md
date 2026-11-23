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
5. **Immutable Employment References**: Any references to current or former roles, employers, job titles, or dates must match selected canonical facts in `out/<target-slug>/runtime/canonical-selection.yaml` (and `okf/employment-records.yaml`) exactly. Never inflate titles or approximate dates.
6. **Full Canonical Context Invariant**: The generator MUST load the complete, untruncated `out/<target-slug>/runtime/canonical-selection.yaml` (including all education, certifications, and languages beyond line 50) into model context.
7. **Cross-Opportunity Isolation Invariant**: The generator MUST NEVER read, inspect, or use prior opportunity directories under `out/<other-target-slug>/` for structure or styling. Use only the fact-free synthetic structural template in `templates/projections/cover-letter.template.md`.
8. **Target Terminology Evidence Boundary**: Unevidenced target-position keywords (e.g., Workday, NetSuite, Coupa, Concur) must NEVER be claimed as direct candidate experience. They may only appear in explicit gap or transferable architecture framing.

## Section Structure

1. **Header & Date**: Candidate contact & target company details.
2. **Motivation & Executive Positioning**: Adapted from `okf/messaging-library.md`.
3. **Strategic Alignment**: How core capabilities match target priorities.
4. **Selected Evidence**: Highlighting 2–3 key stories from `okf/story-library.md`.
5. **Closing & Value Proposition**: 90-day execution promise and call to action.

## Execution Instructions

1. **Read Shared Execution Context**: Read `out/<target-slug>/runtime/opportunity-analysis.yaml`. Extract company, role_title, hiring_goals, capability_priorities, coverage_matrix.
2. **Load Complete Canonical Selection**: Load 100% of `out/<target-slug>/runtime/canonical-selection.yaml` verbatim into context (including education, certifications, and languages).
3. **Load Fact-Free Synthetic Template**: Read `templates/projections/cover-letter.template.md` for formatting and structure. DO NOT inspect other opportunity directories.
4. **Read Canonical OKF Knowledge**: Read `okf/messaging-library.md` & `okf/story-library.md` to extract canonical 30s intro and executive story assets.
5. **Render Cover Letter (`out/<target-slug>/cover-letter.md`)**: Ensure max 1 page (≤500 words) strictly obeying factual boundaries.
6. **Append Log**: `okf/log.md`.
