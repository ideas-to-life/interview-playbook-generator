---
name: playbook-assembler
description: Composes the coaching-oriented Interview Playbook (out/<target-slug>/playbook.md) and 2-page quick reference (out/<target-slug>/interview-cheatsheet.md).
---

# Playbook Assembler

## Overview

`playbook-assembler` is a Projection Layer Skill. It reads canonical OKF knowledge, interview strategy (`okf/interview-strategy.md`), knowledge gaps (`okf/knowledge-gaps.md`), and opportunity analysis (`out/<target-slug>/runtime/opportunity-analysis.yaml`) to assemble:

1. **Interview Playbook** (`out/<target-slug>/playbook.md`): Full executive interview coaching guide.
2. **Interview Cheat Sheet** (`out/<target-slug>/interview-cheatsheet.md`): 2-page rapid-reference document for immediate use during live interviews.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Evidence Grounded**: All coaching advice and story references link to canonical OKF nodes.
3. **Immutable Employment References**: Background summaries, story origins, and career history references must match selected canonical facts in `out/<target-slug>/runtime/canonical-selection.yaml` (and `okf/employment-records.yaml`) exactly.
4. **Unresolved Question Surfacing**: Genuinely unresolved canonical items flagged `[NEEDS CONFIRMATION]` in `canonical-selection.yaml` must be surfaced in coaching notes to prompt the candidate for clarification before interview day.

## Execution Instructions

1. **Read Shared Execution Context & Canonical Selection**: Read `out/<target-slug>/runtime/opportunity-analysis.yaml` and `out/<target-slug>/runtime/canonical-selection.yaml`. Extract target company, role, interviewer, hiring goals, and selected immutable career facts.
2. **Read Canonical OKF Knowledge**: Read `okf/story-library.md`, `okf/interview-strategy.md`, and `okf/knowledge-gaps.md`.
3. **Render Playbook (`out/<target-slug>/playbook.md`)**: Incorporate `[NEEDS CONFIRMATION]` alerts in candidate coaching where applicable.
4. **Render Cheat Sheet (`out/<target-slug>/interview-cheatsheet.md`)**.
5. **Append Log**: `okf/log.md`.
