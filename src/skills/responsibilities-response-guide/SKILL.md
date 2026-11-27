---
name: responsibilities-response-guide
description: >-
  Use this on-demand skill when the user asks to generate spoken-ready answers
  or a rapid-fire response table for each responsibility in a target opportunity
  specification, formatted with frameworks from config/conversation-structures.md
  and persisted to out/<target-slug>/responsibilities-response-guide.md.
---

# Responsibilities Response Guide

## Overview

`responsibilities-response-guide` is an **on-demand** Projection Layer Skill (invoked separately when requested, not run automatically inside `playbook-orchestrator`). It maps each responsibility in scope from the active target opportunity specification (`config/config.yaml` -> `target_opportunity.source`) to both a structured, spoken-ready first-person response and a rapid-fire single-sentence summary table, written in the candidate's executive voice and persisted to `out/<target-slug>/responsibilities-response-guide.md`.

## Hard Rules

```text
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-Only Canonical Layer**: Never modify files in `okf/` or `out/okf/`.
2. **Full Canonical Context**: Load 100% of `out/<target-slug>/runtime/canonical-selection.yaml` into context. Preserve immutable employers, formal titles, exact dates, education, certifications, and language proficiencies.
3. **Cross-Opportunity Isolation**: Never read, inspect, or copy from `out/<other-target-slug>/`.
4. **Factual & Prototype Boundaries**:
   - Preserve explicit stage boundaries (e.g., WPP Media initiatives `buyer-agent-ch`, PCA, and ProductionBoards remained prototype/implementation stage and were not deployed to production during tenure).
   - Never inflate BBC Studios formal titles (`Lead Enterprise Architect - Technology Transformation Group`, `Lead Enterprise Architect - Commercial System`).
   - Enforce `out/<target-slug>/runtime/projection-strategy.yaml` `fit_constraints` and `prohibit_claims`; be transparent and non-defensive on `Gap`, `Adjacent`, and `Transferable` requirements.
5. **Voice & Tone**: Write in first-person ("I"), calm executive authority, problem-first systems thinking ("put the why and what before the how"), British English (`organisations`, `visualisations`, `licences`, `prioritise`, `modernisation`), avoiding marketing hype.
6. **Validator Regex Hygiene**: Avoid forbidden strings anywhere in prose (`MSc`, `UFRJ`, `Head of Enterprise Architecture`, `Head of Architecture`, `AWS Certified`, `Sun Certified`, `Workday`, `NetSuite`, `Coupa`, `Concur`), avoid single-line multi-language strings that combine `Native` and `Spanish`, and avoid standalone `**Title**` lines under repeated employer headings.

## Inputs

- `config/config.yaml` and active `target_opportunity.source` JD file
- `config/conversation-structures.md`
- `out/okf/voice-profile.md` and `<candidate.portfolio_dir>/derived-content/about/about.md` (when present)
- `out/<target-slug>/runtime/canonical-selection.yaml` (100% loaded)
- `out/<target-slug>/runtime/projection-strategy.yaml`
- `out/okf/evidence/*.md`

## Output Structure (`out/<target-slug>/responsibilities-response-guide.md`)

1. **`## Quick-Reference Index`**: Markdown table mapping `#`, `Responsibility in Scope`, `Structure Used`, and `Primary Canonical Anchor`.
2. **`## Rapid-Fire Single-Sentence Responses`**: N-row markdown table (`| # | Responsibility in Scope | Single-Sentence Response |`) where every response is **strictly one sentence** (~25–40 words, one terminal period, no internal sentence-ending punctuation such as `e.g.` or `etc.`).
3. **Numbered Detailed Responses (`## 1.` .. `## N.`)**: One section per responsibility in scope (~100–160 words each), structured using the best-fit framework from `config/conversation-structures.md`:
   - *Problem–Solution–Benefit* (`Problem`, `Solution`, `Benefit`)
   - *PREP* (`Point`, `Reason`, `Example`, `Point`)
   - *STAR* (`Situation`, `Task`, `Action`, `Result`)
   - *ADD* (`Answer`, `Detail`, `Describe`)
   - *Comparison–Contrast–Conclusion* (`Comparison`, `Contrast`, `Conclusion`)
   - *What–So What–Now What* (`What`, `So What`, `Now What`)

## Execution & Verification

1. Extract all responsibilities in scope verbatim from `target_opportunity.source`.
2. Load `canonical-selection.yaml`, `projection-strategy.yaml`, `voice-profile.md` (plus `about.md` if present), `out/okf/evidence/*.md`, and `config/conversation-structures.md`.
3. Write `out/<target-slug>/responsibilities-response-guide.md`.
4. Verify with `./.venv/bin/python3`:
   - `src.scripts.projection_validator.validate_projection_content` returns `PASSED` (`0` findings).
   - `src.scripts.employment_validator.validate_canonical_integrity` returns `PASS` (`0` violations).
   - `src.scripts.canonical_validator.detect_conflicts_in_text` returns `0` conflicts.
   - Every JD responsibility has both a rapid-fire single-sentence row (exactly 1 terminal period) and a numbered structured section.
