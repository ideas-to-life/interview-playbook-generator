---
name: opportunity-alignment-view
description: Walks the canonical bundle to produce a theme-by-theme opportunity alignment view at out/opportunity-alignment.md.
---

# Opportunity Alignment View

## Overview

`opportunity-alignment-view` is a projection-layer Skill (R1, R9). It reads the canonical bundle (evidence, themes, capabilities, signature-achievements) and the target opportunity from `config/config.yaml`, and produces `out/opportunity-alignment.md`. It performs the Opportunity Analysis at view time — NOT in the canonical bundle.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Read-only access to the canonical bundle. No mutation. No persistence beyond `out/`. Fully reproducible.

## Projection Contract (R9)

- **Inputs**: Canonical Bundle + Target Opportunity + Configuration.
- **Outputs**: `out/opportunity-alignment.md` (presentation artefact).
- **Constraints**: Read-only. No mutation. Out-only persistence. Reproducible.

## Input & Output Contracts

- **Inputs**: `okf/evidence/*`, `okf/themes/*`, `okf/capabilities/*`, `okf/signature-achievements.md`, `config/config.yaml` (target_opportunity).
- **Outputs**: `out/opportunity-alignment.md`.

Note: per OKF v0.2 §11, the `type` frontmatter is required only on concept files. The view file at `out/` carries only `title` and `description`.

## Body Structure (3000–5000 words)

```markdown
---
title: "Opportunity Alignment — <Role> at <Company>"
description: "Theme-by-theme mapping of role requirements to candidate evidence."
generated: { by: "opportunity-alignment-view", at: "<ISO-8601>" }
status: draft
---

# Coverage summary
[inference] <one-paragraph summary of how the candidate's evidence covers the role themes>.

# Theme-by-theme mapping

## <Theme 1>
[evidence] <requirement from JD>. [^source-id]
[inference] <why it matters>.
- [Evidence: <title>](../okf/evidence/<slug>.md)
- [Capability: <title>](../okf/capabilities/<slug>.md)
- **Alignment strength**: [inference] <High | Moderate | Low>.
[recommendation] Lead with: <emphasis>.
[recommendation] Avoid over-explaining: <avoid>.

(Repeat for 5–8 themes.)

# Signature Achievement mapping
[inference] <which signature achievements are most relevant for this opportunity — computed at view time, not encoded in the canonical node (R2)>.
```

## Execution Instructions

1. **Read target opportunity** from `config/config.yaml`.
2. **Walk the canonical bundle**: evidence, themes, capabilities, signature-achievements.
3. **Compute alignment** dynamically for each role theme (5–8 themes).
4. **Write `out/opportunity-alignment.md`**.
