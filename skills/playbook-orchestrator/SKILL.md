---
name: playbook-orchestrator
description: Primary entry point driving the Sprint 3 end-to-end Executive Interview Coaching & Playbook pipeline across all Skills.
---

# Playbook Orchestrator

## Overview

The `playbook-orchestrator` is the primary entry point for generating the Interview Playbook, Executive Brief, Opportunity Alignment, and Interview Cheat Sheet. It reads configuration, validates inputs, guides execution across the pipeline, and ensures all five hard rules are upheld.

## The Five Hard Rules

1. **Never Fabricate**: Never invent projects, metrics, team sizes, budgets, technologies, responsibilities, or tenure.
2. **Classify Every Claim**: Every non-empty non-heading line in concept bodies must start with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attribute Every Claim**: Every `[evidence]` line must carry a `[^source-id]` footnote pointing to a valid source in frontmatter.
4. **Stop and Ask**: Pause and prompt when required inputs are missing or ambiguous.
5. **Idempotent Re-runs**: Re-running a Skill overwrites its own output directory cleanly.

## Pipeline Execution Order (v0.3 Sprint 3)

```
1.  portfolio-ingestor
2.  portfolio-analyzer
3.  achievement-extractor
4.  evidence-card-generator        (Extended: 6 new fields + duplicate detection)
5.  behaviour-profile-generator    (New: okf/behaviour-profile.md)
6.  capability-extractor            (New: okf/capabilities/<slug>.md)
7.  signature-achievements-curator  (New: okf/signature-achievements.md)
8.  signature-theme-miner
9.  narrative-generator
10. interview-strategy-generator   (Extended: Opportunity Analysis + Story→Question)
11. knowledge-gaps              (Pre-assembly gate)
12. opportunity-alignment-view      (New: out/opportunity-alignment.md)
13. executive-brief-view           (New: out/executive-brief.md)
14. playbook-assembler          (Produces out/playbook.md & out/interview-cheatsheet.md)
```

## Post-Execution Summary

Upon completion, present the final output summary:
- OKF bundle path (`./out/okf/`)
- Playbook view path (`./out/playbook.md`)
- Executive Brief path (`./out/executive-brief.md`)
- Opportunity Alignment path (`./out/opportunity-alignment.md`)
- Interview cheat sheet path (`./out/interview-cheatsheet.md`)
- Unverified/Draft section count.

