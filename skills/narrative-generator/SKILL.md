---
name: narrative-generator
description: Formulates conversational 30-second introduction, 2-minute journey, and 5-minute executive narrative into okf/executive-narrative.md.
---

# Narrative Generator

## Overview

`narrative-generator` reads `okf/portfolio.md`, `okf/signature-themes.md`, and underlying evidence cards to construct conversational executive narrative variants stored in `okf/executive-narrative.md` (`type: Narrative`).

## Hard Rules & Tone

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

- Avoid rigid CV language and listing job titles chronologically.
- Focus on candidate evolution, motivation, core philosophy, and key differentiators.
- All lines must begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.

## Input & Output Contracts

- **Inputs**: `okf/portfolio.md`, `okf/signature-themes.md`, `okf/evidence/*.md`
- **Outputs**:
  - `okf/executive-narrative.md` (type: `Narrative`)
  - `okf/log.md` (append update entry)

## Execution Instructions

1. **Formulate Narrative Length Variants**:
   - **30-Second Elevator Pitch**: High-impact conversational opening hook for recruiters.
   - **2-Minute Career Journey**: Story of transformation and progression without job-title lists.
   - **5-Minute Executive Story**: Deep-dive into architectural philosophy, AI operationalisation, and strategic leadership.
2. **Write `okf/executive-narrative.md`**:
   - Frontmatter: `type: Narrative`, `status: draft`, `sources` array.
   - Sections:
     - `# 30-Second Elevator Pitch`
     - `# 2-Minute Career Journey`
     - `# 5-Minute Executive Narrative`
3. **Append Log**: Append entry to `okf/log.md`.
