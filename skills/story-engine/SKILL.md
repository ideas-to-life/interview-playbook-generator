---
name: story-engine
description: Converts STAR Evidence Cards into a single consolidated canonical executive story library at okf/story-library.md.
---

# Story Engine

## Overview

`story-engine` is a Knowledge Layer Skill. It walks the canonical evidence card library in `okf/evidence/*.md` and formats each card into an executive story in a single consolidated document: `okf/story-library.md`.

Each executive story follows a standardized 8-part structure:
1. **Situation**
2. **Challenge**
3. **Decision**
4. **Actions**
5. **Outcome**
6. **Business Value**
7. **Conversation Hook**
8. **Transition Sentence**

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Canonical**: `okf/story-library.md` is a single consolidated OKF concept (`type: StoryLibrary`) stored in `okf/`.
2. **Classified**: Every non-heading statement line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attributed**: Every `[evidence]` line MUST carry a `[^source-id]` footnote.

## Execution Instructions

1. **Read `okf/evidence/*.md`**: Parse all canonical evidence cards.
2. **Format Reusable Executive Stories**: Convert each evidence card into the 8-part story structure.
3. **Write Consolidated Library (`okf/story-library.md`)**.
4. **Append Log**: `okf/log.md`.
