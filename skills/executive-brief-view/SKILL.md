---
name: executive-brief-view
description: Walks the whole bundle to produce a 10-minute pre-interview brief at out/executive-brief.md.
---

# Executive Brief View

## Overview

`executive-brief-view` is a projection-layer Skill (R1, R9). It reads the whole bundle and produces `out/executive-brief.md`. Designed for the 10-minute pre-interview window.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Read-only access to the canonical bundle. No mutation. No persistence beyond `out/`. Fully reproducible.

## Projection Contract (R9)

Same as `opportunity-alignment-view`. Inputs: Canonical Bundle + Target Opportunity + Configuration. Output: presentation artefact. Read-only. No mutation.

## Input & Output Contracts

- **Inputs**: `okf/evidence/*`, `okf/themes/*`, `okf/capabilities/*`, `okf/signature-achievements.md`, `okf/interview-strategy.md`, `okf/behaviour-profile.md`, `okf/signature-themes.md`, `okf/executive-narrative.md`, `config/config.yaml`.
- **Outputs**: `out/executive-brief.md`.

## Body Structure (11 sections, ≤2,500 words)

The brief MUST contain these 11 sections, in this order:

1. Executive Positioning
2. Top 5 Messages
3. Three Signature Stories
4. Executive Behaviour Profile — at-a-glance
5. Conversation Strategy
6. Risks
7. Opportunity Watch-outs
8. Questions to Ask
9. Conversation Reminders
10. Interview Mindset (R6 — pure coaching, no evidence, ≤5 bullets)
11. Final Reminders

## Execution Instructions

1. **Walk the bundle** in the order above.
2. **Render each section** according to the schema.
3. **Verify link integrity**: every link to an evidence card, capability, achievement, or theme is a working bundle-relative link.
4. **Word budget**: ≤2,500 words.
5. **Write `out/executive-brief.md`**.
