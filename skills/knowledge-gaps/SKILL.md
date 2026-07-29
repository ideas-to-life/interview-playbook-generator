---
name: knowledge-gaps
description: Evaluates whole bundle against target opportunity to produce a KnowledgeGap report as a pre-assembly gate.
---

# Knowledge Gaps (Pre-Assembly Gate)

## Overview

`knowledge-gaps` walks the entire OKF bundle, comparing candidate evidence against target opportunity requirements. It produces `okf/knowledge-gaps.md` (`type: KnowledgeGap`) and serves as a pre-assembly quality gate.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every line in `okf/knowledge-gaps.md` must start with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.

## Input & Output Contracts

- **Inputs**: Entire OKF bundle (`okf/sources/*`, `okf/achievements/*`, `okf/evidence/*`, `okf/interview-strategy.md`) and target opportunity source.
- **Outputs**:
  - `okf/knowledge-gaps.md` (type: `KnowledgeGap`)
  - `okf/log.md` (append entry)

## Severity Buckets

1. **`critical`**: Target opportunity requires a core skill or experience completely absent in portfolio evidence.
2. **`moderate`**: Evidence exists but lacks metrics or concrete outcome figures.
3. **`minor`**: Secondary requirement or nice-to-have documentation missing.

## Execution Instructions

1. **Evaluate Requirements Coverage**: Map each JD/role requirement to evidence cards.
2. **Identify Missing Evidence & Assumptions**: Uncover missing metrics or unverified `[assumption]` tags.
3. **Emit `okf/knowledge-gaps.md`**:
   - Frontmatter: `type: KnowledgeGap`, `status: draft`.
   - Sections:
     - `# Critical Gaps`
     - `# Moderate Gaps`
     - `# Minor Gaps & Recommended Portfolio Improvements`
4. **Enforce Gate**: If `critical` gaps exist and `pipeline.fail_on_severe_gaps` is `true`, signal the orchestrator to pause.
5. **Append Log**: Log updates in `okf/log.md`.
