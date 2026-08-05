---
name: market-feedback-evaluator
description: Evaluates real-world hiring feedback against initial platform predictions, maintaining separate market-fit scores without mutating canonical career knowledge.
---

# Market Feedback Evaluator & Prediction Accuracy

## Overview

`market-feedback-evaluator` is an Evaluation Layer Skill. It ingests real-world market feedback captured in `evaluation/opportunities/<target-slug>.yaml` and compares it against original platform predictions (`opportunity-fit-report.yaml`).

It evaluates how accurately the platform predicted hiring outcome concerns (such as archetype mismatches or missing tooling experience) and generates feedback accuracy analytics.

## Hard Rules

```
NEVER FABRICATE:
- Market feedback is evaluation evidence. It MUST NOT autonomously modify canonical career knowledge (okf/), opportunity-scoring rules, or executive identity.
```

## Input & Output Contracts

- **Inputs**: `evaluation/opportunities/<target-slug>.yaml`, `out/<target-slug>/runtime/opportunity-fit-report.yaml`, `out/<target-slug>/runtime/archetype-analysis.yaml`.
- **Outputs**:
  - `evaluation/opportunities/<target-slug>-evaluation.yaml`
  - `okf/log.md` (append entry)

## Feedback Schema (`evaluation/opportunities/<target-slug>.yaml`)

```yaml
market_feedback:
  opportunity: "vervaunt-head-of-ai"
  stage: "recruiter_shortlist"
  outcome: "paused"
  positive:
    - "profile_well_aligned"
    - "strong_overall_experience"
  concerns:
    - "ecommerce_experience"
    - "agency_experience"
    - "n8n_zapier_shopify"
    - "enterprise_governance_weighting"
```

## Evaluation Output Schema (`evaluation/opportunities/<target-slug>-evaluation.yaml`)

```yaml
version: "6.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
prediction_evaluation:
  predicted_archetype: "ai_automation_builder"
  predicted_overall_fit: "Moderate"
  actual_outcome: "paused"
  prediction_accuracy: "High" # Platform correctly anticipated concerns prior to feedback
  confirmed_signals:
    - "eCommerce domain gap correctly identified"
    - "n8n/Zapier/Shopify tooling gap correctly identified"
    - "Enterprise governance over-weighting risk correctly flagged"
  missed_signals: []
  external_validation_scores:
    evidence_integrity: 98.5
    brand_consistency: 99.0
    projection_quality: 98.2
    opportunity_fit: 68.0
    archetype_fit: 62.0
```

## Execution Instructions

1. Load `evaluation/opportunities/<target-slug>.yaml` and corresponding runtime fit report.
2. Cross-reference market concerns against flagged gaps in `gap-analysis.yaml` and `opportunity-fit-report.yaml`.
3. Compute prediction accuracy score and identify confirmed vs missed signals.
4. Output separate validation scores (distinguishing 99% Brand Score from ~62% Archetype Fit Score).
5. Write evaluation summary to `evaluation/opportunities/<target-slug>-evaluation.yaml`.
6. Append log entry to `okf/log.md`.
