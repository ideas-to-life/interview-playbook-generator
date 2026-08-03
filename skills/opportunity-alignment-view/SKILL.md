---
name: opportunity-alignment-view
description: Walks the canonical bundle to produce a theme-by-theme opportunity alignment view at out/<target-slug>/opportunity-alignment.md.
---

# Opportunity Alignment View

## Overview

`opportunity-alignment-view` is a Projection Layer Skill. It maps the candidate's canonical OKF capabilities and signature achievements against the target opportunity requirements in `out/<target-slug>/runtime/opportunity-analysis.yaml` to produce a detailed alignment matrix at `out/<target-slug>/opportunity-alignment.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Canonical Links**: Every alignment section MUST link back to canonical OKF capability and evidence card nodes.

## Execution Instructions

1. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**: Extract coverage matrix and capability priorities.
2. **Read Canonical OKF Knowledge**: Read `okf/capabilities/*.md` and `okf/evidence/*.md`.
3. **Render Opportunity Alignment Matrix (`out/<target-slug>/opportunity-alignment.md`)**.
4. **Append Log**: `okf/log.md`.
