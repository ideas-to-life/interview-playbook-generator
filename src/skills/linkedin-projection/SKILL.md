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
4. **Immutable Experience Headers**: Experience section employer names, job titles, and employment dates must strictly match selected canonical facts in `out/<target-slug>/runtime/canonical-selection.yaml` (and `okf/employment-records.yaml`).
5. **Full Canonical Context Invariant**: The generator MUST load the complete, untruncated `out/<target-slug>/runtime/canonical-selection.yaml` (including all education, certifications, and languages beyond line 50) into model context.
6. **Cross-Opportunity Isolation Invariant**: The generator MUST NEVER read, inspect, or use prior opportunity directories under `out/<other-target-slug>/` for structure or styling. Use only the fact-free synthetic structural template in `templates/projections/linkedin-profile.template.md`.
7. **Target Terminology Evidence Boundary**: Unevidenced target-position keywords (e.g., Workday, NetSuite, Coupa, Concur) must NEVER be claimed as direct candidate experience. They may only appear in explicit gap or transferable architecture framing.

## Section Structure

1. **Headline Variations**: Adapted from `okf/positioning-statements.md` (max 220 characters).
2. **About / Summary**: Adapted from `okf/executive-identity.md` (max 2,600 characters).
3. **Featured Section**: Key case studies, portfolio links, and architecture publications.
4. **Experience Refinements**: High-impact bullet refinements for current and prior roles.
5. **Education & Certifications**: Canonical academic degrees and certifications strictly adhering to `canonical-selection.yaml`.

## Execution Instructions

1. **Read Shared Execution Context**: Read `out/<target-slug>/runtime/opportunity-analysis.yaml`. Extract capability priorities, keywords.
2. **Load Complete Canonical Selection**: Load 100% of `out/<target-slug>/runtime/canonical-selection.yaml` verbatim into context (including education, certifications, and languages).
3. **Load Fact-Free Synthetic Template**: Read `templates/projections/linkedin-profile.template.md` for formatting and structure. DO NOT inspect other opportunity directories.
4. **Read Canonical OKF Knowledge**: Read `okf/executive-identity.md`, `okf/voice-profile.md`, & `okf/positioning-statements.md` to extract canonical positioning.
5. **Render LinkedIn Profile Optimization (`out/<target-slug>/linkedin-profile.md`)**: Ensure alignment with voice guidelines and factual boundaries.
6. **Append Log**: `okf/log.md`.
