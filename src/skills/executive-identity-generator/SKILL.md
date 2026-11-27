---
name: executive-identity-generator
description: Synthesises canonical executive identity, voice profile, and positioning statements into okf/executive-identity.md, okf/voice-profile.md, and okf/positioning-statements.md.
---

# Executive Identity Generator

## Overview

`executive-identity-generator` is a Knowledge Layer Skill. It reads ingested portfolio sources, evidence cards, capabilities, and signature themes to produce three canonical OKF concept documents in `okf/`:

1. **Executive Identity** (`okf/executive-identity.md`): Core executive positioning, leadership philosophy, transformation philosophy, AI philosophy, consulting philosophy, and professional values.
2. **Voice Profile** (`okf/voice-profile.md`): Communication tone guidelines (calm, collaborative, executive), encouraged vocabulary, and prohibited marketing buzzwords.
3. **Positioning Statements** (`okf/positioning-statements.md`): Standardised positioning statement variants (Executive, Advisory, Technical Executive).

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Canonical**: These documents become part of the immutable `okf/` bundle.
2. **Classified**: Every non-heading statement line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attributed**: Every `[evidence]` line MUST carry a `[^source-id]` footnote.

## Execution Instructions

1. **Read Canonical Bundle**: Read `okf/evidence/*.md`, `okf/capabilities/*.md`, `okf/signature-themes.md`, and `okf/sources/*.md`.
2. **Synthesise `okf/executive-identity.md`**: Extract core philosophies and values.
3. **Synthesise `okf/voice-profile.md`**: Define tone, encouraged terms, and prohibited hype words.
4. **Synthesise `okf/positioning-statements.md`**: Formulate Executive, Advisory, and Technical Executive variants.
5. **Append Log**: `okf/log.md`.
