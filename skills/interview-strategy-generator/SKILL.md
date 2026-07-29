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

- **Inputs**: `okf/evidence/*.md`, `okf/signature-themes.md`, target opportunity source file.
- **Outputs**:
  - `okf/interview-strategy.md` (type: `InterviewStrategy`)
  - `okf/log.md` (append entry)

## Execution Instructions

1. **Parse Target Opportunity & Stage Context**: Analyze requirements, role title, company context, and interview stage (Recruiter, Hiring Manager, Executive).
2. **Rank Evidence Cards**: Rank every Evidence Card into one of 4 tiers:
   - `Primary Story`
   - `Supporting Story`
   - `Optional Story`
   - `Do Not Use`
   Based on relevance, uniqueness, evidence strength, target role requirements, and interview stage.
3. **Formulate Coaching Guidance**:
   - What should the candidate lead with?
   - What should the candidate avoid?
   - Which three flagship stories must be remembered?
   - Which key achievements differentiate the candidate?
   - What concerns might arise and how to address them?
4. **Write `okf/interview-strategy.md`** (Max 4 pages concise coaching document).
5. **Append Log**: Append update to `okf/log.md`.
