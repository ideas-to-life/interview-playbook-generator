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

1. **`critical`**: Target opportunity requires a core skill or experience completely absent in portfolio evidence, or an unresolved canonical career ambiguity touches a core role requirement.
2. **`moderate`**: Evidence exists but lacks metrics or concrete outcome figures, or unresolved canonical questions exist on secondary achievements.
3. **`minor`**: Secondary requirement or nice-to-have documentation missing.

## Execution Instructions

1. **Evaluate Requirements Coverage**: Map each JD/role requirement to evidence cards.
2. **Identify Missing Evidence & Assumptions**: Uncover missing metrics or unverified `[assumption]` tags.
3. **Incorporate Canonical Unresolved Questions (FR-010)**: Query `unresolved_questions` from canonical record (`CanonicalCareerRecord.filter_unresolved_for_coaching()`). Any unresolved item must be registered as a knowledge gap flagged `[NEEDS CONFIRMATION]` so it is resolved before external presentation.
4. **Emit `okf/knowledge-gaps.md`**:
   - Frontmatter: `type: KnowledgeGap`, `status: draft`.
   - Sections:
     - `# Critical Gaps`
     - `# Moderate Gaps`
     - `# Minor Gaps & Recommended Portfolio Improvements`
     - `# Canonical Verification Gaps ([NEEDS CONFIRMATION])`
5. **Enforce Gate**: If `critical` gaps exist and `pipeline.fail_on_severe_gaps` is `true`, signal the orchestrator to pause.
6. **Append Log**: Log updates in `okf/log.md`.
