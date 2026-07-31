---
name: interview-strategy-generator
description: Generates targeted interview positioning, narrative strategy, story rankings, and objection handling coaching in okf/interview-strategy.md.
---

# Interview Strategy Generator

## Overview

`interview-strategy-generator` reads `okf/evidence/*`, `okf/signature-themes.md`, and the target opportunity spec to produce a concise, actionable coaching document at `okf/interview-strategy.md` (`type: InterviewStrategy`, max 4 pages).

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

All strategy claims must be tagged `[inference]` or `[recommendation]`, grounded in `[evidence]` from underlying Evidence Cards.

## Input & Output Contracts

- **Inputs**: `okf/evidence/*.md`, `okf/signature-themes.md`, active target opportunity source file declared in `target_opportunity.source` of `config/config.yaml`.
- **Outputs**:
  - `okf/interview-strategy.md` (type: `InterviewStrategy`)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: InterviewStrategy
title: "Interview Strategy"
description: "Coaching strategy for the target opportunity. Regenerated every run."
tags: [strategy, coaching]
generated: { by: "interview-strategy-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# Opportunity Analysis

## <Theme 1>
[evidence] <requirement from JD>. [^source-id]
[inference] <why it matters>.
- [Evidence: <title>](../evidence/<slug>.md)
- **Alignment strength**: [inference] <High | Moderate | Low>.
[recommendation] Lead with: <emphasis>.
[recommendation] Avoid over-explaining: <avoidance>.

(Repeat for 5–8 themes.)

# Story-to-Question Mapping

## <Question 1>
[recommendation] Primary story: [Evidence: <title>](../evidence/<slug>.md).
[inference] Supporting evidence: [Evidence: <title>](../evidence/<slug>.md).
[recommendation] Alternative story: [Evidence: <title>](../evidence/<slug>.md).

(Repeat for 10–15 questions.)

# Coaching Guidance
[inference] Lead with: <lead>.
[recommendation] Avoid: <avoid>.
[inference] Flagship stories: ...
[inference] Differentiators: ...
[inference] Objections and mitigations: ...
```

## Execution Instructions

This Skill produces **coaching-layer output** (R1, R8). It reads the canonical bundle + target opportunity and produces `okf/interview-strategy.md`, which is regenerated every run and never treated as canonical knowledge.

1. **Parse Target Opportunity & Stage Context**: Read `config/config.yaml` to identify the active `target_opportunity.source` file path, role title, company, interviewer, and stage context. Analyze requirements and context directly from that specified target opportunity file.
2. **Rank Evidence Cards** into 4 tiers: `Primary Story`, `Supporting Story`, `Optional Story`, `Do Not Use`. Based on relevance, uniqueness, evidence strength, target role requirements, and interview stage.
3. **Opportunity Analysis (R8):** For each major interview theme (5–8 themes), emit a block with `[evidence]` requirement from JD, `[inference]` why it matters, supporting evidence links, alignment strength, `[recommendation]` what to emphasise, `[recommendation]` what to avoid over-explaining.
4. **Story-to-Question Mapping (R3):** For each anticipated question (10–15), emit a block with Primary story (`[recommendation]`), Supporting evidence (`[inference]`), Alternative story (`[recommendation]`). The Primary story is selected from the `Capability.Primary Evidence` tier when one matches.
5. **Formulate Coaching Guidance**: lead with, avoid, flagship stories, differentiators, objections.
6. **Write `okf/interview-strategy.md`** (max 4 pages).
7. **Append Log**: `okf/log.md`.
