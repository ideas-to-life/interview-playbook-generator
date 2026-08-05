---
name: opportunity-alignment-view
description: Walks the canonical bundle and runtime strategy to produce a theme-by-theme opportunity alignment view at out/<target-slug>/opportunity-alignment.md.
---

# Opportunity Alignment View

## Overview

`opportunity-alignment-view` is a Projection Layer Skill. It maps the candidate's canonical OKF capabilities and signature achievements against the target opportunity requirements in `out/<target-slug>/runtime/opportunity-analysis.yaml` and `projection-strategy.yaml` to produce a detailed alignment matrix at `out/<target-slug>/opportunity-alignment.md`.

In v6.1, `opportunity-alignment-view` explicitly displays evidence relationships (`direct`, `adjacent`, `transferable`, `absent`), respects the `maximum_alignment` constraints from `projection-strategy.yaml`, and decomposes generic requirements to prevent adjacent evidence from masking gaps.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Read-only**: Never modify any concept file in `okf/`.
2. **Canonical Links**: Every alignment section MUST link back to canonical OKF capability and evidence card nodes.
3. **Respect Fit Constraints (v6.1 FR-2, FR-9)**: Alignment ratings in `opportunity-alignment.md` MUST NOT exceed the `maximum_alignment` specified in `projection-strategy.yaml`.

## Requirement Decomposition Rules (v6.1 FR-8)

To prevent combining materially different requirements into a single alignment row that hides gaps:
- **Workflow Automation** is decomposed into:
  - `Engineering-led Automation` (e.g. CAS / Python / custom orchestration)
  - `Business Workflow Automation` (e.g. operational process automation)
  - `Low-code / SaaS Automation` (e.g. n8n / Zapier)
- **eCommerce & Tooling** is decomposed into:
  - `eCommerce Domain Experience`
  - `Shopify Ecosystem`
  - `n8n / Zapier Automation`

## Alignment Matrix Layout Schema (`out/<target-slug>/opportunity-alignment.md`)

```markdown
# Opportunity Alignment: [Role Title] at [Company]

## Overview & Alignment Summary
[Executive alignment narrative adhering to projection strategy positioning]

## Requirement Alignment Matrix

| Requirement | Primary Canonical Evidence | Evidence Relationship | Alignment Rating |
| :--- | :--- | :--- | :--- |
| **AI Strategy & Governance** | BBC GenAI Strategy, RAI Framework | Direct | Strong |
| **Engineering-led Automation** | CAS Architecture-as-Code, Python Multi-Agent Systems | Direct | Strong |
| **Business Workflow Automation** | CAS Automation | Adjacent | Moderate |
| **Low-code Automation (n8n/Zapier)** | No direct evidence | Absent | Gap |
| **Shopify Ecosystem** | No direct evidence | Absent | Gap |
| **eCommerce Domain** | No direct evidence | Absent | Gap |
| **Agency Operating Context** | WPP Media Client Operations | Transferable | Transferable |

## Detailed Requirement Analysis

### 1. Engineering-led Automation vs Low-code SaaS Automation
- **Status**: Moderate / Transferable Overall
- **Direct Evidence**: Strong evidence of custom Python, agentic systems, and architecture workflow automation.
- **Adjacent Context**: Custom Python multi-agent orchestration provides engineering foundation for workflow logic.
- **Explicit Gap Note**: Direct hands-on experience with low-code SaaS automation platforms (n8n/Zapier) is not evidenced in the canonical portfolio and represents an adjacent capability rather than a demonstrated direct skill.
```

## Execution Instructions

1. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml` and `projection-strategy.yaml`**.
2. **Decompose Requirements**: Apply decomposition rules to broad requirements.
3. **Map Evidence & Relationships**: Assign `direct`, `adjacent`, `transferable`, or `absent` per decomposed row.
4. **Apply Alignment Cap**: Ensure no rating exceeds `maximum_alignment` from `fit_constraints`.
5. **Render Markdown File**: Save to `out/<target-slug>/opportunity-alignment.md`.
6. **Append Log**: `okf/log.md`.
