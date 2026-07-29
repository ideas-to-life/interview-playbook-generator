---
name: playbook-assembler
description: Composes the coaching-oriented Interview Playbook (out/playbook.md) and 2-page quick reference (out/interview-cheatsheet.md).
---

# Playbook Assembler

## Overview

`playbook-assembler` walks all nodes in the populated OKF graph to generate two human-readable coaching artefacts:
1. `out/playbook.md` — The coaching-oriented Interview Playbook.
2. `out/interview-cheatsheet.md` — The 2-page quick reference cheat sheet for immediate pre-interview review (< 10 minutes).

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

- Avoid reproducing rigid CV wording (e.g., prefer "Enterprise Architect specialising in operationalising AI" over formal corporate job titles).
- Render only Primary and Supporting stories in main text; STAR library moves to Appendix.
- Trust badges (`[draft]`, `[machine-confirmed]`, `[human-reviewed]`) are rendered for every section header.

## Input & Output Contracts

- **Inputs**: Entire OKF bundle (`okf/portfolio.md`, `okf/signature-themes.md`, `okf/executive-narrative.md`, `okf/achievements/*`, `okf/evidence/*`, `okf/interview-strategy.md`, `okf/knowledge-gaps.md`).
- **Outputs**:
  - `out/playbook.md` (Coaching-oriented Interview Playbook)
  - `out/interview-cheatsheet.md` (2-page Interview Cheat Sheet)
  - `okf/log.md` (append entry)

## Playbook Structure (v0.2 Coaching Order)

1. Executive Summary [draft]
2. 30-Second Pitch [draft]
3. 2-Minute Career Story [draft]
4. Why This Role & Strategic Fit [draft]
5. Top Differentiators [draft]
6. Top Three Stories to Remember [draft]
7. Likely Recruiter Questions & Suggested Answers [draft]
8. Questions to Ask the Interviewer [draft]
9. Knowledge Gaps & Potential Red Flags [draft]
10. Appendix: Primary & Supporting STAR Evidence Library [draft]

## Interview Cheat Sheet Structure (Max 2 Pages)

1. Elevator Pitch
2. Top Five Core Messages
3. Three Stories to Remember
4. Likely Recruiter Questions & Suggested Answers
5. Questions to Ask Us
6. Red Flags / Things Not To Forget
