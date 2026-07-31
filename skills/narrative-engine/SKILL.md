---
name: narrative-engine
description: Formulates canonical career narratives and messaging libraries into okf/narrative-library.md and okf/messaging-library.md.
---

# Narrative Engine

## Overview

`narrative-engine` is a Knowledge Layer Skill. It synthesises canonical professional journeys and reusable messaging blocks into `okf/` concepts:

1. **Narrative Library** (`okf/narrative-library.md`): Canonical journeys (Career Journey, Transformation Journey, AI Journey, Leadership Journey, Architecture Journey).
2. **Messaging Library** (`okf/messaging-library.md`): Reusable 30s pitch, 2m executive introduction, career summary block, and philosophy blocks.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Canonical**: Stored in `okf/` as immutable long-lived assets.
2. **Classified**: Every non-heading statement line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attributed**: Every `[evidence]` line MUST carry a `[^source-id]` footnote.

## Execution Instructions

1. **Read Canonical Bundle**: Read `okf/executive-identity.md`, `okf/evidence/*.md`, and `okf/capabilities/*.md`.
2. **Synthesise `okf/narrative-library.md`**: Formulate 5 canonical journey narratives.
3. **Synthesise `okf/messaging-library.md`**: Formulate 30s pitch, 2m introduction, and summary blocks.
4. **Append Log**: `okf/log.md`.
