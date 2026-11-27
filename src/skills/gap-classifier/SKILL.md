---
name: gap-classifier
description: Categorises material candidate gaps into 7 distinct types and assesses materiality, confidence, and recoverability.
---

# Gap Classifier & Severity Model

## Overview

`gap-classifier` is a Runtime Layer Skill. It evaluates missing alignment points between canonical career knowledge and target opportunity requirements, categorising each gap into a precise category and assigning materiality and recoverability.

This prevents renderers and resume projections from attempting to "wordplay around" fundamental experience or domain gaps that cannot be solved by positioning alone.

## Hard Rules

```
NEVER FABRICATE:
- Do NOT reclassify a genuine experience/domain gap as a positioning gap to mask missing background.
```

Do NOT modify `okf/` canonical bundle. Output lives exclusively in `out/<target-slug>/runtime/gap-analysis.yaml`.

## Input & Output Contracts

- **Inputs**: `okf/` bundle, `out/<target-slug>/runtime/opportunity-analysis.yaml`, `out/<target-slug>/runtime/archetype-analysis.yaml`.
- **Outputs**:
  - `out/<target-slug>/runtime/gap-analysis.yaml`
  - `okf/log.md` (append entry)

## Gap Categories (FR-4)

- `evidence_gap`: Candidate likely has experience, but portfolio sources lack explicit evidence/metrics.
- `experience_gap`: Candidate lacks direct experience in the core requirement area.
- `domain_gap`: Candidate lacks experience in the specific business domain (e.g. eCommerce, Healthcare, FinTech).
- `tooling_gap`: Candidate lacks hands-on experience with specific required technologies (e.g. Shopify, n8n, Zapier).
- `positioning_gap`: Candidate has strong evidence, but current messaging emphasizes an orthogonal identity (e.g. Enterprise EA vs. Hands-on Automation).
- `terminology_gap`: Candidate uses synonymous or equivalent domain terms rather than job-specific terms.
- `operating_context_gap`: Candidate has worked in different organizational scales/cultures (e.g. global corporate vs. startup agency).

## Severity & Recoverability Model (FR-5)

Each gap receives:
- **Materiality**: `high` (dealbreaker/core requirement), `medium` (important secondary requirement), `low` (nice-to-have).
- **Confidence**: `high`, `medium`, `low`.
- **Recoverability**:
  - `projection`: Can be addressed directly by adjusting resume/letter positioning strategy.
  - `adjacent_evidence`: Can be bridged using closely related, transferable canonical evidence.
  - `learnable`: Rapidly addressable through self-directed study or a quick practical experiment.
  - `experience_required`: Hard requirement that can only be satisfied by multi-year direct experience.
  - `unknown`: Insufficient context to determine.

## Output Schema (`out/<target-slug>/runtime/gap-analysis.yaml`)

```yaml
version: "6.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
classified_gaps:
  - id: "gap-1"
    subject: "<Subject / Skill / Domain>"
    type: "<evidence_gap | experience_gap | domain_gap | tooling_gap | positioning_gap | terminology_gap | operating_context_gap>"
    materiality: "<high | medium | low>"
    confidence: "<high | medium | low>"
    recoverability: "<projection | adjacent_evidence | learnable | experience_required | unknown>"
    reasoning: "> Explanation of why this gap was classified with this type and recoverability."
    recommended_action: "<Actionable guidance for coaching or projection logic>"
summary:
  total_gaps: 0
  critical_unrecoverable_gaps: 0
  addressable_gaps: 0
```

## Execution Instructions

1. Compare canonical evidence in `okf/` against target opportunity requirements.
2. For each requirement with non-full coverage, analyze the nature of the gap.
3. Categorise into one of the 7 gap categories.
4. Evaluate materiality, confidence, and recoverability.
5. Write `out/<target-slug>/runtime/gap-analysis.yaml`.
6. Append log entry to `okf/log.md`.
