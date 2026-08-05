---
name: projection-strategy-generator
description: Generates a shared runtime projection strategy determining what to lead with, de-emphasise, bridge, and prohibit across downstream projections.
---

# Projection Strategy Generator

## Overview

`projection-strategy-generator` is a Runtime Layer Skill. It acts as an explicit intelligence bridge between Opportunity/Archetype Analysis and downstream document projections (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `executive-brief-view`).

It ensures that executive projections do not overposition the candidate or invent unbacked expertise, while providing clear direction on how to highlight legitimate strengths and frame adjacent evidence.

## Hard Rules

```
NEVER FABRICATE:
- Claims listed in `prohibit_claims` MUST NOT be made in any generated resume, letter, or brief.
```

Do NOT modify `okf/` canonical bundle. Output lives exclusively in `out/<target-slug>/runtime/projection-strategy.yaml`.

## Input & Output Contracts

- **Inputs**: `okf/` bundle, `out/<target-slug>/runtime/opportunity-analysis.yaml`, `out/<target-slug>/runtime/archetype-analysis.yaml`, `out/<target-slug>/runtime/gap-analysis.yaml`, `out/<target-slug>/runtime/opportunity-fit-report.yaml`.
- **Outputs**:
  - `out/<target-slug>/runtime/projection-strategy.yaml`
  - `okf/log.md` (append entry)

## Output Schema (`out/<target-slug>/runtime/projection-strategy.yaml`)

```yaml
version: "6.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
projection_strategy:
  target_archetype: "<primary_archetype_slug>"
  recommended_positioning: "<Positioning statement aligned with archetype without overclaiming>"
  lead_with:
    - "<Strength or achievement 1 to lead with>"
    - "<Strength or achievement 2 to lead with>"
  de_emphasise:
    - "<Area to de-emphasise, e.g. heavy enterprise governance when targeting lean agency>"
  bridge:
    - "<Adjacent experience that legitimately bridges to role requirements>"
  prohibit_claims:
    - "<Prohibited claim 1, e.g. eCommerce direct experience>"
    - "<Prohibited claim 2, e.g. Shopify native developer>"
    - "<Prohibited claim 3, e.g. n8n expert>"
  gap_handling_notes:
    - "<Guidance on how projections should handle visible gaps cleanly>"
```

## Execution Instructions

1. Parse target archetype, classified gaps, and multidimensional fit assessment.
2. Determine key strengths to **lead with** based on verified canonical evidence.
3. Identify areas to **de-emphasise** (e.g. downplaying heavy enterprise architecture when applying for a lean automation builder role).
4. Identify legitimate **bridges** (adjacent experiences like WPP agency collaboration or CAS automation systems).
5. Compile **prohibit_claims** list for missing domain, tooling, or experience gaps.
6. Write `out/<target-slug>/runtime/projection-strategy.yaml`.
7. Append log entry to `okf/log.md`.
