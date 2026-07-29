---
name: playbook-orchestrator
description: Primary entry point driving the Sprint 2 end-to-end Interview Playbook & Cheat Sheet pipeline across all Skills.
---

# Playbook Orchestrator

## Overview

The `playbook-orchestrator` is the primary entry point for generating the Interview Playbook and Interview Cheat Sheet. It reads configuration, validates inputs, guides execution across the pipeline, and ensures all five hard rules are upheld.

## The Five Hard Rules

1. **Never Fabricate**: Never invent projects, metrics, team sizes, budgets, technologies, responsibilities, or tenure.
2. **Classify Every Claim**: Every non-empty non-heading line in concept bodies must start with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attribute Every Claim**: Every `[evidence]` line must carry a `[^source-id]` footnote pointing to a valid source in frontmatter.
4. **Stop and Ask**: Pause and prompt when required inputs are missing or ambiguous.
5. **Idempotent Re-runs**: Re-running a Skill overwrites its own output directory cleanly.

## Pipeline Execution Order (v0.2 Sprint 2)

```
1. portfolio-ingestor
2. portfolio-analyzer
3. achievement-extractor
4. evidence-card-generator
5. signature-theme-miner       (New in v0.2: okf/signature-themes.md)
6. narrative-generator         (New in v0.2: okf/executive-narrative.md)
7. interview-strategy-generator(Updated v0.2: coaching & story ranking)
8. knowledge-gaps              (Pre-assembly gate)
9. playbook-assembler          (Produces out/playbook.md & out/interview-cheatsheet.md)
```

## Post-Execution Summary

Upon completion, present the final output summary:
- OKF bundle path (`./out/okf/`)
- Playbook view path (`./out/playbook.md`)
- Interview cheat sheet path (`./out/interview-cheatsheet.md`)
- Unverified/Draft section count.
