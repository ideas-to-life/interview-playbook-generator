---
name: behaviour-profile-generator
description: Builds an ExecutiveBehaviourProfile with 4 core dimensions always present and 3 optional dimensions only when sufficient evidence.
---

# Behaviour Profile Generator

## Overview

`behaviour-profile-generator` reads `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md` (if present), and the target opportunity from `config/config.yaml` to produce a single `ExecutiveBehaviourProfile` concept at `okf/behaviour-profile.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every claim body line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. All `[evidence]` lines require `[^source-id]` footnotes. Optional dimensions are omitted when evidence is thin — they are NEVER marked `(insufficient evidence)` (R5).

## Input & Output Contracts

- **Inputs**: `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md` (if present), `config/config.yaml` (target_opportunity).
- **Outputs**:
  - `okf/behaviour-profile.md` (type: `ExecutiveBehaviourProfile`)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: ExecutiveBehaviourProfile
title: "Executive Behaviour Profile"
description: "Inferred executive behaviour profile. Core dimensions always generated; optional dimensions included only when sufficient evidence exists."
tags: [behaviour, profile, executive]
generated: { by: "behaviour-profile-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# Core dimensions

## Leadership Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: <supporting reasoning>.

## Communication Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: <supporting reasoning>.

## Decision Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: <supporting reasoning>.

## Delivery Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: <supporting reasoning>.

# Optional dimensions

## Stakeholder Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: <supporting reasoning>.

## Summary
[inference] Core dimensions were generated. Optional dimensions included or omitted based on evidence. Sections omitted are surfaced to `okf/knowledge-gaps.md`.
```

## Dimension Rules (R5)

- **Core (always generated)**: Leadership Style, Communication Style, Decision Style, Delivery Style.
- **Optional (only when sufficient evidence exists; otherwise OMITTED)**: Stakeholder Style, Collaboration Style, Executive Presence.
- **Optional sections are never marked `(insufficient evidence)`** — they are omitted entirely.

## Execution Instructions

1. **Load evidence, themes, signature-themes.**
2. **Infer each core dimension**: 3–7 `[evidence]` lines (each citing a source) followed by 1–3 `[inference]` lines with a `> Reasoning:` blockquote.
3. **For each optional dimension**: emit the section only if ≥2 evidence lines can be cited. Otherwise omit.
4. **Append log**: `okf/log.md`.

## Stop-and-Ask

- Fewer than 3 evidence cards → exit.
