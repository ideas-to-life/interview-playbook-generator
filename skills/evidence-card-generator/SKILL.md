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

## Execution Instructions

1. **Read Achievements**: Load each concept in `okf/achievements/`.
2. **Build STAR Evidence Cards**: Structure into Situation, Actions, Results, Lessons, Competencies, Questions, and Supporting artefacts.
3. **Run Classification Scan**: Verify every non-heading non-empty body line has a valid classification prefix.
4. **Append Log**: Log changes to `okf/log.md`.
