---
name: archetype-classifier
description: Infers the dominant professional archetype required by a target opportunity based on responsibilities and outcomes rather than job title alone.
---

# Opportunity Archetype Classifier

## Overview

`archetype-classifier` is a Runtime Layer Skill. It reads the target opportunity JD / spec and `out/<target-slug>/runtime/opportunity-analysis.yaml` to infer the dominant professional archetype required by the role.

Job titles can be misleading (e.g. "Head of AI" in an eCommerce agency means `AI Automation Builder`, whereas "Head of AI" in a FTSE 100 enterprise means `Enterprise AI Architect`). `archetype-classifier` prevents archetype mismatches before projection generation.

## Hard Rules

```
NEVER FABRICATE:
- Do NOT infer archetypes based on assumptions not supported by the JD text.
```

Do NOT modify any files in `okf/` or `out/okf/`. Output lives exclusively in `out/<target-slug>/runtime/archetype-analysis.yaml`.

## Input & Output Contracts

- **Inputs**: `config/config.yaml`, target opportunity JD / spec file, `out/<target-slug>/runtime/opportunity-analysis.yaml`.
- **Outputs**:
  - `out/<target-slug>/runtime/archetype-analysis.yaml`
  - `okf/log.md` (append entry)

## Taxonomy of Archetypes

Supported initial taxonomy (extensible):
- `enterprise_architect`: Focus on broad enterprise IT architecture, TOGAF, legacy modernization.
- `enterprise_ai_architect`: Enterprise-wide AI strategy, governance, platforms, regulated industries.
- `ai_coe_architect`: Setting up AI Centers of Excellence, platform enablement, enterprise AI standards.
- `ai_transformation_leader`: Large-scale organizational AI transformation and change management.
- `head_of_ai_enterprise`: Strategic AI leadership for large corporations.
- `head_of_ai_automation`: Operational automation, workflow acceleration, practical tool deployment.
- `ai_automation_builder`: Hands-on development of AI agents, low-code/no-code workflows (n8n, Zapier, Make), API integrations.
- `ai_engineering_leader`: Technical leadership of ML/AI engineering teams building custom LLM apps.
- `ai_product_leader`: AI product strategy, user experience, feature roadmap.
- `ai_strategy_advisory_leader`: Management consulting, executive advising, commercial AI strategy.
- `agency_ai_leader`: Fast-paced client delivery, agency operational context, commercial campaign execution.
- `consulting_ai_leader`: Professional services, client advisory, solution architecture for clients.

## Output Schema (`out/<target-slug>/runtime/archetype-analysis.yaml`)

```yaml
version: "6.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
opportunity_archetype:
  primary: "<primary_archetype_slug>"
  secondary:
    - "<secondary_archetype_slug_1>"
    - "<secondary_archetype_slug_2>"
  confidence: "<high | medium | low>"
  reasoning: >
    Detailed explanation of why this archetype was assigned based on
    expected outcomes and day-to-day responsibilities in the JD.
key_signals:
  expected_outcomes:
    - "<Outcome 1>"
  operating_environment: "<e.g., fast-paced eCommerce agency | regulated enterprise>"
  hands_on_depth_required: "<high | medium | low>"
```

## Execution Instructions

1. Parse target JD and `out/<target-slug>/runtime/opportunity-analysis.yaml`.
2. Analyze day-to-day responsibilities, delivery expectation, team structure, and tooling mentions.
3. Classify primary and secondary professional archetypes from the taxonomy based on responsibilities (ignoring pure title matching).
4. Write `out/<target-slug>/runtime/archetype-analysis.yaml`.
5. Append log entry to `okf/log.md`.
