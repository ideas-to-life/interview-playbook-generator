---
name: evidence-card-generator
description: Converts Achievement concepts into structured, reusable STAR EvidenceCard nodes.
---

# Evidence Card Generator

## Overview

`evidence-card-generator` transforms `okf/achievements/*.md` into interview-ready `EvidenceCard` concepts stored in `okf/evidence/<slug>.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every claim body line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. All `[evidence]` lines require `[^source-id]` footnotes.

## Input & Output Contracts

- **Inputs**: `okf/achievements/*.md`
- **Outputs**:
  - `okf/evidence/<slug>.md` (type: `EvidenceCard`)
  - `okf/evidence/index.md` (type: `Index`)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: EvidenceCard
title: "<Title>"
description: "<Summary>"
tags: [<tags>]
generated: { by: "evidence-card-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
conversation_hook: "<single sentence in second-person imperative, how to enter the story>"
transition_sentence: "<single sentence in second-person imperative, how to leave the story>"
organisational_impact: "[inference] <intrinsic impact statement>"
strategic_significance: "[inference] <intrinsic strategic-significance statement>"
recency: "<YYYY-MM or YYYY-MM-DD>"
duplicates_of: []  # populated by the duplicate-detection pass
---

# Situation
[evidence] ... [^source-id]

# Actions
[evidence] ... [^source-id]
[inference] ...

# Results
[evidence] ... [^source-id]
[assumption] ...

# Lessons
[inference] ...
[recommendation] ...

# Competencies demonstrated
- <Competency 1>
- <Competency 2>

# Possible interview questions
- <Question 1>
- <Question 2>

# Supporting artefacts
- [<Source Title>](../sources/<slug>.md)

# Confidence level
<High | Medium | Low>
```

If a value is missing in source, the corresponding field is left as `[recommendation] <placeholder>` and the missing value is surfaced to `okf/knowledge-gaps.md`.

## Execution Instructions

1. **Read Achievements**: Load each concept in `okf/achievements/`.
2. **Build STAR Evidence Cards**: Structure into Situation, Actions, Results, Lessons, Competencies, Questions, and Supporting artefacts.
3. **Run Classification Scan**: Verify every non-heading non-empty body line has a valid classification prefix.
4. **Duplicate-detection pass**: After all cards are generated, scan every pair (new, existing) for source overlap (shared `sources[].id`) AND token overlap (≥40% on Situation + Actions sections). For each pair that matches both criteria, set `duplicates_of: [<existing-slug>]` on the new card, leave `status: draft`, and append a one-line entry to `okf/knowledge-gaps.md` listing the duplicate for user review.
5. **Append Log**: Log changes to `okf/log.md`.
