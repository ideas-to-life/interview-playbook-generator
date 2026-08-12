---
name: archetype-fit-validator
description: Evaluates generated projection documents for anti-overpositioning guardrails and runtime-to-projection fit consistency (alignment inflation, evidence inflation, gap disappearance).
---

# Archetype Fit & Fit-Consistency Validator

## Overview

`archetype-fit-validator` is a Validation Layer Skill. It evaluates generated projection documents against canonical evidence, `out/<target-slug>/runtime/opportunity-analysis.yaml`, and `projection-strategy.yaml`.

Its primary rule: **Runtime fit intelligence constrains projection claims.** A downstream projection may become more conservative, but never more optimistic than the maximum alignment permitted by `fit_constraints`.

## Hard Rules

```
NEVER FABRICATE:
- Downstream projections that inflate alignment, transform adjacent evidence into direct coverage, or attempt to "argue away" gaps produce FIT CONSISTENCY WARNING findings.
```

Do NOT modify `okf/` canonical bundle. Output appends to `out/<target-slug>/runtime/projection-validation-report.yaml`.

## Fit-Consistency & Identity-Drift Validation Checks (v6.1 FR-10, FR-11, FR-12)

The validator evaluates projections against 5 key fit consistency & identity preservation axes:

1. **Alignment Inflation**: Runtime specifies `maximum_alignment: Moderate` (or `Gap`), but projection classifies requirement as `Strong`.
2. **Evidence Inflation**: Runtime classifies relationship as `adjacent` or `transferable`, but projection asserts or implies `direct` experience.
3. **Gap Disappearance**: Runtime identifies a material gap, but projection omits or contradicts the gap in a section explicitly assessing that requirement.
4. **Unsupported Equivalence**: Projection uses prohibited gap argumentation patterns (e.g., claiming custom Python multi-agent orchestration is equivalent to n8n/Zapier mastery).
5. **Identity Drift / Over-Positioning**: Projected document makes candidate appear to have a materially different primary professional identity from canonical identity (e.g. headline dominated by target title displacing candidate archetype, target domain appearing as primary profession, unsupported leadership titles like "CCoE Leader", or unsupported duration claims like "15+ years building CCoEs").

## Validation Scope (FR-12)

Fit-consistency validation applies to projections that make explicit fit claims:
- `out/<target-slug>/opportunity-alignment.md`
- `out/<target-slug>/executive-brief.md`
- `out/<target-slug>/resume-recruiter.md`
- `out/<target-slug>/cover-letter.md`
- `out/<target-slug>/playbook.md`

*(Note: Resume variants do not need to advertise every missing tool, but must not make false direct claims).*

## Output Report Schema (`out/<target-slug>/runtime/projection-validation-report.yaml`)

```yaml
version: "6.1"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
archetype_validation:
  status: "<PASSED | WARNING | FAIL>"
  overpositioning_score: 95.0
  findings:
    - type: "identity_drift"
      signal: "<headline_drift | domain_displacement | unsupported_leadership_title | unsupported_duration_claim>"
      target_element: "<headline | executive_summary | professional_experience>"
      detected_claim: "<Claim text, e.g. 15+ years building Cloud Centre of Excellence operating models>"
      canonical_baseline: "<Canonical archetype, e.g. Enterprise Architect / Transformation & AI Advisor>"
      reason: "> Projected document makes candidate appear to have target archetype as primary profession."

fit_consistency:
  status: "<PASSED | WARNING>"
  findings:
    - type: "<alignment_inflation | evidence_inflation | gap_disappearance | unsupported_equivalence | identity_drift>"
      requirement: "<requirement_slug>"
      runtime_alignment: "<moderate | gap>"
      projection_alignment: "<strong | direct>"
      source: "<document_name, e.g. opportunity-alignment.md>"
      reason: "> Downstream projection classified requirement as Strong despite runtime max constraint of Moderate."
```

## Execution Instructions

1. Load `okf/` canonical bundle, `out/<target-slug>/runtime/projection-strategy.yaml`, and generated projection files.
2. Cross-reference ratings and claims in projections against `fit_constraints`.
3. Check for alignment inflation, evidence inflation, gap disappearance, and unsupported equivalence.
4. Append `fit_consistency` findings and status to `out/<target-slug>/runtime/projection-validation-report.yaml`.
5. Append log entry to `okf/log.md`.
