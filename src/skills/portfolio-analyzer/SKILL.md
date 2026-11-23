---
name: portfolio-analyzer
description: Analyzes ingested portfolio sources to construct high-level coverage maps and signature theme summaries.
---

# Portfolio Analyzer

## Overview

`portfolio-analyzer` reads all `Source` concepts in `okf/sources/*` and synthesizes `okf/portfolio.md` (`type: PortfolioAnalysis`), mapping domain coverage, portfolio depth, and candidate positioning themes.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every line in `okf/portfolio.md` must start with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.

## Input & Output Contracts

- **Inputs**: `okf/sources/index.md`, `okf/sources/*.md`
- **Outputs**:
  - `okf/portfolio.md` (type: `PortfolioAnalysis`)
  - `okf/log.md` (append update entry)

## Execution Instructions

1. **Read Ingested Sources**: Load `okf/sources/index.md` and all concept files under `okf/sources/`.
2. **Analyze Portfolio Depth**:
   - Identify core domain pillars (e.g. Enterprise Architecture, Generative AI, Cloud Migration).
   - Evaluate evidence density per pillar.
3. **Write `okf/portfolio.md`**:
   - Frontmatter: `type: PortfolioAnalysis`, `status: draft`, `sources` array aggregating all ingested source IDs.
   - Body sections:
     - `# Executive Summary`: Inferred candidate archetype and primary strengths.
     - `# Domain Coverage Map`: Evidence-backed domain areas and sources.
     - `# Strengths & Portfolio Gaps`: Explicitly highlight thin areas as `[inference]` or `[assumption]`.
4. **Append Log**: Append entry to `okf/log.md`.
