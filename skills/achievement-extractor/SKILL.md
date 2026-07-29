---
name: achievement-extractor
description: Extracts evidence-grounded achievements from portfolio sources into OKF Achievement nodes.
---

# Achievement Extractor

## Overview

`achievement-extractor` reads `okf/sources/*` and identifies distinct career achievements, creating individual `Achievement` nodes under `okf/achievements/<slug>.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects (named programmes, products, systems)
- Metrics (percentages, dollar figures, counts)
- Team sizes
- Budgets
- Technologies (named tools, languages, platforms)
- Responsibilities
- Tenure (start/end dates when not in source)
```

If a value is not explicitly stated in a source:
1. Re-check all sources.
2. If missing, write as `[assumption]` with a clear placeholder marker.
3. Mark concept `status: draft`.

Every line must be classified (`[evidence]`, `[inference]`, `[recommendation]`, `[assumption]`) and `[evidence]` lines must carry `[^source-id]` footnotes.

## Input & Output Contracts

- **Inputs**: `okf/sources/*.md`
- **Outputs**:
  - `okf/achievements/<slug>.md` (type: `Achievement`)
  - `okf/achievements/index.md` (type: `Index`)
  - `okf/log.md` (append entry)

## Execution Instructions

1. **Extract Achievements**: Scan source text for concrete activities, architectural decisions, migrations, and leadership outcomes.
2. **Format Achievement Concept**:
   - Frontmatter: `type: Achievement`, `title`, `description`, `tags`, `status: draft`, `sources` list matching original sources.
   - Body structure:
     - `# Situation`: Context and problem statement.
     - `# Actions`: Specific candidate actions.
     - `# Results`: Verifiable outcomes.
3. **Validate Rules**: Reject any non-heading, non-empty line missing a marker. Ensure all evidence lines include `[^source-id]` footnotes.
4. **Append Log**: Record updates in `okf/log.md`.
