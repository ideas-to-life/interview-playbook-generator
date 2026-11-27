---
name: signature-theme-miner
description: Identifies recurring professional themes across extracted achievements into okf/signature-themes.md.
---

# Signature Theme Miner

## Overview

`signature-theme-miner` reads all `Achievement` concepts under `okf/achievements/*.md` and synthesizes recurring professional patterns into `okf/signature-themes.md` (`type: Theme`).

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every line in `okf/signature-themes.md` must start with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.

## Input & Output Contracts

- **Inputs**: `okf/achievements/*.md`
- **Outputs**:
  - `okf/signature-themes.md` (type: `Theme`)
  - `okf/log.md` (append update entry)

## Execution Instructions

1. **Analyze Achievements**: Read all concept files under `okf/achievements/`.
2. **Synthesize Recurring Themes**:
   - Identify 3–5 core professional themes that transcend individual project silos.
   - For each theme:
     - Title and theme description.
     - Synthesize multiple supporting achievements and evidence cards.
     - Formulate one executive-level message (conversational, non-CV wording).
3. **Write `okf/signature-themes.md`**:
   - Frontmatter: `type: Theme`, `status: draft`, `sources` array aggregating underlying sources.
   - Body structure per theme:
     - `# Theme: <Title>`
     - `[inference] Executive Message: <Message>`
     - `[evidence] Supporting Evidence: <Achievements & Cards>` [^footnotes]
4. **Append Log**: Append entry to `okf/log.md`.
