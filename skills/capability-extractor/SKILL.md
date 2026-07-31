---
name: capability-extractor
description: Groups evidence cards and themes into Capability concepts and indexes them in okf/capabilities/.
---

# Capability Extractor

## Overview

`capability-extractor` reads `okf/evidence/*.md`, `okf/themes/*.md`, and `okf/signature-themes.md` (if present) to produce `Capability` concepts at `okf/capabilities/<slug>.md` and an index at `okf/capabilities/index.md`. Each capability is a stable mid-level abstraction between achievements and themes.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every claim body line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. All `[evidence]` lines require `[^source-id]` footnotes.

## Input & Output Contracts

- **Inputs**: `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md` (if present).
- **Outputs**:
  - `okf/capabilities/index.md` (type: `Index`)
  - `okf/capabilities/<slug>.md` (type: `Capability`, one per capability)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: Capability
title: "<Capability Title>"
description: "<one-sentence summary>"
tags: [<tags>]
generated: { by: "capability-extractor", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# Definition
[inference] <one-paragraph description of what this capability means for the candidate>.

# Primary Evidence
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <why this is the strongest demonstration>.
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <why this is the strongest demonstration>.

# Supporting Evidence
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <how this reinforces the capability>.

# Additional Evidence
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <how this extends the capability into adjacent areas>.

# Demonstrated in achievements
- [Achievement: <title>](../achievements/<slug>.md)

# Mapped to themes
- [Theme: <title>](../themes/<slug>.md)

# Evidence strength
[inference] <High | Moderate | Low> based on breadth and depth of primary + supporting evidence.
```

## Algorithmic Notes

- Group by topical affinity. Aim for 5–15 capabilities total; ≤15 is a hard cap.
- Each capability must be grounded in ≥2 sources (evidence cards or themes).
- Evidence ranking is deterministic, based on: organisational impact, strategic significance, breadth of capability, confidence.
- Primary tier must contain ≥1 evidence card. Supporting and Additional tiers may be empty if evidence is thin.
- The `Evidence strength` field is intrinsic (R7). Opportunity alignment is NOT computed here — it is computed at view time in `opportunity-alignment-view`.

## Execution Instructions

1. **Load evidence and themes**: Read every `okf/evidence/*.md` and `okf/themes/*.md`.
2. **Cluster**: Group by topical affinity. Reject any cluster with <2 sources.
3. **Rank**: Order evidence within each cluster by impact/sigificance/breadth/confidence.
4. **Write each capability node** with the tiered schema above.
5. **Write the index**: `okf/capabilities/index.md` lists every capability by title and slug.
6. **Append log**: `okf/log.md`.

## Stop-and-Ask

- Fewer than 5 evidence cards → exit and tell the user to run earlier Skills first.
- Target opportunity is in a markedly different domain → ask whether to proceed.
