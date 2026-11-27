---
name: archetype-fit-evaluator
description: Evaluates multidimensional candidate fit across Capability, Domain, Tooling, and Operating-Context, producing a selection recommendation and archetype fit analysis.
---

# Archetype Fit Evaluator & Decision Support

## Overview

`archetype-fit-evaluator` is a Runtime Layer Skill. It combines target archetype analysis (`archetype-analysis.yaml`), gap analysis (`gap-analysis.yaml`), and canonical evidence to construct a comprehensive multidimensional fit report.

It replaces simplistic generic alignment scores with an analytical breakdown across four experience dimensions and surfaces an explicit Opportunity Selection Recommendation (`Strong Fit`, `Good Fit`, `Stretch Fit`, `Adjacent Fit`, `Weak Fit`).

## Hard Rules

```
NEVER FABRICATE:
- Do NOT collapse low domain or tooling scores into high capability scores to inflate fit.
```

Do NOT modify `okf/` canonical bundle. Output lives exclusively in `out/<target-slug>/runtime/opportunity-fit-report.yaml`.

## Experience Dimension Model (FR-3)

1. **Capability Fit**: Can the candidate perform the underlying technical/leadership capability? (e.g. AI architecture, enterprise governance).
2. **Domain Fit**: Has the candidate demonstrated experience in the specific business domain? (e.g. eCommerce, Retail, Financial Services).
3. **Ecosystem/Tooling Fit**: Has the candidate demonstrated hands-on experience with explicitly required technologies? (e.g. Shopify, n8n, Zapier).
4. **Operating-Context Fit**: Has the candidate worked successfully in the expected organizational culture and scale? (e.g. lean entrepreneurial agency vs. global enterprise).

## Selection Recommendation Classifications (FR-9)

- `Strong Fit`: High alignment across all 4 dimensions. Minimal competitive risk.
- `Good Fit`: Solid alignment with minor addressable positioning or evidence gaps.
- `Stretch Fit`: Strong capability fit but notable domain/tooling gaps; high interview preparation required.
- `Adjacent Fit`: Strong adjacent skills; role represents a diagonal shift.
- `Weak Fit`: Critical unrecoverable domain/operating-context gaps; apply only with low expectations.

## Output Schema (`out/<target-slug>/runtime/opportunity-fit-report.yaml`)

```yaml
version: "6.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
opportunity_fit_assessment:
  overall_fit: "<High | Moderate-High | Moderate | Low-Moderate | Low>"
  archetype_fit: "<Strong | Good | Stretch | Adjacent | Weak>"
  primary_archetype_matched: "<archetype_slug>"
  primary_concern: "> Detailed narrative explaining key gaps or mismatch signals."

experience_dimensions:
  capability_fit:
    rating: "<High | Medium | Low>"
    summary: "<Summary of capability alignment>"
  domain_fit:
    rating: "<High | Medium | Low>"
    summary: "<Summary of domain experience>"
  ecosystem_tooling_fit:
    rating: "<High | Medium | Low>"
    summary: "<Summary of specific tool experience>"
  operating_context_fit:
    rating: "<High | Medium | Low>"
    summary: "<Summary of organizational context fit>"

dimensional_matrix:
  - dimension: "AI Architecture"
    rating: "High"
  - dimension: "eCommerce Domain"
    rating: "Low"
  - dimension: "n8n / Zapier / Shopify"
    rating: "Low"

selection_recommendation:
  classification: "<Strong Fit | Good Fit | Stretch Fit | Adjacent Fit | Weak Fit>"
  rationale: "> Clear explanation of why this recommendation was assigned."
  risk_profile:
    competitive_disadvantages:
      - "<Disadvantage 1>"
    interview_risks:
      - "<Risk 1>"
    addressable_positioning_issues:
      - "<Issue 1>"

learning_opportunities:
  - subject: "<Tool or Skill, e.g. n8n / Zapier>"
    materiality: "High"
    recommendation: "Optional practical experiment to build familiarisation."
```

## Execution Instructions

1. Read `okf/` evidence nodes, `out/<target-slug>/runtime/archetype-analysis.yaml`, and `gap-analysis.yaml`.
2. Evaluate evidence against each of the 4 fit dimensions independently.
3. Construct the dimensional matrix.
4. Calculate overall fit rating and archetype fit classification.
5. Formulate selection recommendation and risk profile.
6. Identify advisory learning opportunities for `learnable` gaps.
7. Write `out/<target-slug>/runtime/opportunity-fit-report.yaml`.
8. Append log entry to `okf/log.md`.
