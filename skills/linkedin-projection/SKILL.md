---
name: linkedin-projection
description: Generates LinkedIn profile optimization sections from canonical Executive Identity, voice guidelines, and shared opportunity analysis.
---

# LinkedIn Projection

## Overview

`linkedin-projection` is a Projection Layer Skill. It reads the canonical OKF bundle (`okf/`, including `okf/executive-identity.md`, `okf/voice-profile.md`, and `okf/positioning-statements.md`) and the shared execution context at `out/<target-slug>/runtime/opportunity-analysis.yaml` to generate an optimized LinkedIn profile specification at `out/<target-slug>/linkedin-profile.md`.

Unlike ATS resumes which prioritize exact keyword density for parsing engines, LinkedIn projections prioritize professional credibility, executive authority, and personal brand impact.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Canonical Positioning**: Adapt About Section directly from `okf/executive-identity.md` and `okf/positioning-statements.md`. Do NOT generate independent positioning prose.
3. **Voice Consistency**: Follow tone rules in `okf/voice-profile.md`.

## Section Structure

1. **Headline Variations**: Adapted from `okf/positioning-statements.md` (max 220 characters).
2. **About / Summary**: Adapted from `okf/executive-identity.md` (max 2,600 characters).
3. **Featured Section**: Key case studies, portfolio links, and architecture publications.
4. **Experience Refinements**: High-impact bullet refinements for current and prior roles.

## Execution Instructions

1. **Read `okf/executive-identity.md` & `okf/positioning-statements.md`**: Extract canonical positioning.
2. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**: Extract capability priorities.
3. **Render LinkedIn Profile Optimization (`out/<target-slug>/linkedin-profile.md`)**.
4. **Append Log**: `okf/log.md`.
