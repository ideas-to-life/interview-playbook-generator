---
name: signature-achievements-curator
description: Curates a ranked list of 5–12 Achievement nodes on intrinsic properties.
---

# Signature Achievements Curator

## Overview

`signature-achievements-curator` reads `okf/achievements/*.md`, `okf/capabilities/*.md`, and `okf/themes/*.md` to produce a curated list of `SignatureAchievements` at `okf/signature-achievements.md`. The list is ranked STRICTLY on intrinsic properties — opportunity-aware reordering happens at view time.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every claim body line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. All `[evidence]` lines require `[^source-id]` footnotes.

## Input & Output Contracts

- **Inputs**: `okf/achievements/*.md`, `okf/capabilities/*.md`, `okf/themes/*.md`.
- **Outputs**:
  - `okf/signature-achievements.md` (type: `SignatureAchievements`)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: SignatureAchievements
title: "Signature Achievements"
description: "Curated list of 5–12 achievements ranked on intrinsic properties."
tags: [achievements, signature]
generated: { by: "signature-achievements-curator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# The list

1. **[<title>](../achievements/<slug>.md)** — [inference] **Why:** <reason>. **Strategic:** <strategic dimension>. **Capability:** <capability anchored>.
2. **[<title>](../achievements/<slug>.md)** — [inference] **Why:** <reason>. **Strategic:** <strategic dimension>. **Capability:** <capability anchored>.

# Selection rationale
[inference] The list ranks on intrinsic properties: strategic significance + organisational impact + capability breadth + recency + confidence. NO opportunity-specific state is encoded in the canonical node (R2, R10). Opportunity-aware reordering happens at view time in `out/opportunity-alignment.md`.
```

Algorithmic notes: composite score over `strategic_significance + organisational_impact + capability_breadth + recency + confidence`. List length 5–12. If fewer than 5 achievements exist, exit. If more than 12 produce non-trivial scores, keep the strongest 10 and document the rest as "honourable mentions" in the rationale section.

## Execution Instructions

1. **Load achievements, capabilities, themes**.
2. **Score**: For each achievement, compute the composite score on intrinsic properties.
3. **Sort**: Highest score first.
4. **Write** the ranked list and the rationale section.
5. **Append log**: `okf/log.md`.

## Stop-and-Ask

- Fewer than 5 achievements → exit.
