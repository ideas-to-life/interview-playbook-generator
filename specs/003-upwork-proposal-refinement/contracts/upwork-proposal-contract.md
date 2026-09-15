# Interface Contract: Upwork Proposal Projection (V3.1)

## Overview

Defines the projection contract for generating client-facing proposals, screening answers, work sample recommendations, and evidence gap reports from V3.1 qualification context.

---

## Inputs

- `out/<target-slug>/runtime/upwork-qualification.yaml`
- `out/okf/` evidence graph

---

## Output Artifacts

1. **Executive Proposal**: `out/<target-slug>/upwork-qualification-report.md`
2. **Evidence Gap Report**: `out/<target-slug>/upwork-evidence-gaps.md`
3. **Screening Answers**: `out/<target-slug>/upwork-screening-answers.md`
4. **Work Samples**: `out/<target-slug>/upwork-work-samples.md`

---

## Projection Projection Rules

1. **Clean Prose Rule**: Proposal draft (`upwork-qualification-report.md`) must contain zero visible `[evidence]` tags, `[^source-id]` footnotes, or `[OPEN CONDITION]` diagnostic markers.
2. **Opening Positioning Rule**: If a production dealbreaker is unresolved, opening statements position candidate strengths around verified adjacent capabilities (e.g. enterprise agentic architecture leadership) without claiming requirement satisfaction.
3. **No Assertion-Then-Disclaimer Rule**: Primary claims must be bounded upfront. Prohibits assertive claims followed by disclaimers.
4. **Screening Fidelity Rule**: Screening answers must not assert affirmative historical claims for `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED` facts.
5. **Work Sample Metadata Rule**: Personal/prototype work samples must retain explicit project type labels (`personal_project`, `prototype_innovation`).
