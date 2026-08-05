---
name: projection-strategy-generator
description: Generates a shared runtime projection strategy determining what to lead with, de-emphasise, bridge, prohibit, and maximum alignment constraints across downstream projections.
---

# Projection Strategy Generator

## Overview

`projection-strategy-generator` is a Runtime Layer Skill. It acts as an explicit intelligence bridge between Opportunity/Archetype Analysis and downstream document projections (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `executive-brief-view`, `opportunity-alignment-view`).

In v6.1, `projection-strategy.yaml` serves as the **authoritative constraint contract** for downstream projections. Downstream projections may become more conservative, but never more optimistic than the maximum alignment permitted by `fit_constraints`.

## Hard Rules

```
NEVER FABRICATE:
- Claims listed in `prohibit_claims` MUST NOT be made in any generated resume, letter, or brief.
- Downstream projections MUST NOT exceed the `maximum_alignment` specified in `fit_constraints`.
```

Do NOT modify `okf/` canonical bundle. Output lives exclusively in `out/<target-slug>/runtime/projection-strategy.yaml`.

## Input & Output Contracts

- **Inputs**: `okf/` bundle, `out/<target-slug>/runtime/opportunity-analysis.yaml`, `out/<target-slug>/runtime/archetype-analysis.yaml`, `out/<target-slug>/runtime/gap-analysis.yaml`, `out/<target-slug>/runtime/opportunity-fit-report.yaml`.
- **Outputs**:
  - `out/<target-slug>/runtime/projection-strategy.yaml`
  - `okf/log.md` (append entry)

## Output Schema (`out/<target-slug>/runtime/projection-strategy.yaml`)

```yaml
version: "6.1"
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
    - requirement: "<Requirement slug>"
      evidence: ["<evidence-slug-1>", "<evidence-slug-2>"]
      relationship: "<adjacent | transferable>"
      framing: "<Clear framing statement highlighting transferability without overclaiming>"
  prohibit_claims:
    - "<Prohibited claim 1, e.g. eCommerce direct experience>"
    - "<Prohibited claim 2, e.g. Shopify native developer>"
    - "<Prohibited claim 3, e.g. n8n expert>"
  
  # Authoritative constraint contract (v6.1 FR-9)
  fit_constraints:
    - requirement: "<Requirement name/slug>"
      relationship: "<direct | adjacent | transferable | absent>"
      maximum_alignment: "<Strong | Moderate | Transferable | Gap>"
```

## Alignment Constraint Mapping Rules (v6.1 FR-2)

| Evidence Relationship | Maximum Default Alignment |
| :--- | :--- |
| `direct` | `Strong` |
| `adjacent` | `Moderate` |
| `transferable` | `Transferable` |
| `absent` | `Gap` |

A downstream projection shall NOT classify adjacent or transferable evidence as `Strong` unless Runtime Intelligence explicitly provides an evidence-backed override.

## Execution Instructions

1. Parse target archetype, classified gaps, evidence relationships, and multidimensional fit assessment.
2. Formulate key strengths to **lead with** based on verified canonical evidence.
3. Identify areas to **de-emphasise**.
4. Construct **bridge** definitions for adjacent or transferable evidence.
5. Compile **prohibit_claims** list.
6. Generate **fit_constraints** mapping every requirement to its evidence relationship and maximum allowed alignment.
7. Write `out/<target-slug>/runtime/projection-strategy.yaml`.
8. Append log entry to `okf/log.md`.
