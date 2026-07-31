---
name: linkedin-projection
description: Generates LinkedIn profile optimization sections (Headline, About, Featured, Experience) from canonical OKF knowledge and shared opportunity analysis.
---

# LinkedIn Projection

## Overview

`linkedin-projection` is a Projection Layer Skill. It reads the canonical OKF bundle (`okf/`) and the shared execution context at `out/runtime/opportunity-analysis.yaml` to generate an optimized LinkedIn profile specification at `out/linkedin-profile.md`.

Unlike ATS resumes which prioritize exact keyword density for parsing engines, LinkedIn projections prioritize professional credibility, executive authority, and personal brand impact.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Traceable**: Grounded in canonical OKF evidence cards, capabilities, and executive narrative.

## Section Structure

1. **Headline Variations**: Concise executive headlines (max 220 characters).
2. **About / Summary**: First-person executive narrative (max 2,600 characters).
3. **Featured Section**: Key case studies, portfolio links, and architecture publications.
4. **Experience Refinements**: High-impact bullet refinements for current and prior roles.

## Execution Instructions

1. **Read `out/runtime/opportunity-analysis.yaml`**: Extract `executive_positioning` and `capability_priorities`.
2. **Walk Canonical Knowledge**: Read `okf/executive-narrative.md`, `okf/evidence/*.md`, and `okf/capabilities/*.md`.
3. **Render LinkedIn Profile Optimization (`out/linkedin-profile.md`)**.
4. **Append Log**: `okf/log.md`.
