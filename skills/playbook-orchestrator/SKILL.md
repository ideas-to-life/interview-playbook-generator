---
name: playbook-orchestrator
description: Primary entry point orchestrating the v0.5 Career Projection Platform pipeline across Knowledge, Runtime, Coaching, and Projection layers.
---

# Playbook Orchestrator

## Overview

The `playbook-orchestrator` is the primary entry point for generating the Career Projection Platform suite (Executive Identity, Story Library, Resumes, Cover Letter, LinkedIn Profile, Interview Playbook, Executive Brief, Opportunity Alignment, Cheat Sheet, and Brand Validation Report). It reads configuration, validates inputs, guides execution across the four-layer pipeline, and ensures all hard rules are upheld.

Outputs are cleanly separated: canonical career knowledge is stored in `out/okf/`, while opportunity-specific runtime context, validation reports, and presentation views are written to `out/<target-slug>/` (derived from `target_opportunity.source` in `config/config.yaml`).

## The Five Hard Rules

1. **Never Fabricate**: Never invent projects, metrics, team sizes, budgets, technologies, responsibilities, or tenure.
2. **Classify Every Claim**: Every non-empty non-heading line in concept bodies must start with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attribute Every Claim**: Every `[evidence]` line must carry a `[^source-id]` footnote pointing to a valid source in frontmatter.
4. **Stop and Ask**: Pause and prompt when required inputs are missing or ambiguous.
5. **Idempotent Re-runs**: Re-running a Skill overwrites its own output directory cleanly.

## Pipeline Execution Order (v0.5 Sprint 5)

```
KNOWLEDGE LAYER (canonical; writes to out/okf/)
 1. portfolio-ingestor
 2. portfolio-analyzer
 3. achievement-extractor
 4. evidence-card-generator        (6 fields + duplicate detection)
 5. behaviour-profile-generator    (okf/behaviour-profile.md)
 6. capability-extractor            (okf/capabilities/<slug>.md)
 7. signature-achievements-curator  (okf/signature-achievements.md)
 8. signature-theme-miner
 9. executive-identity-generator    (okf/executive-identity.md, voice-profile.md, positioning-statements.md)
10. narrative-engine                (okf/narrative-library.md, messaging-library.md)
11. story-engine                    (okf/story-library.md)

RUNTIME LAYER (derived execution context; writes to out/<target-slug>/runtime/)
12. opportunity-analyzer            (out/<target-slug>/runtime/opportunity-analysis.yaml)

COACHING LAYER (derived; reads canonical + opportunity-analysis)
13. interview-strategy-generator
14. knowledge-gaps              (Pre-assembly gate)

PROJECTION LAYER (views; reads canonical + opportunity-analysis; writes to out/<target-slug>/)
15. projection-registry             (Orchestrates registered projections)
    ├── resume-projection           (out/<target-slug>/resume-executive.md, resume-ats.md, resume-recruiter.md)
    ├── cover-letter-projection     (out/<target-slug>/cover-letter.md)
    ├── linkedin-projection         (out/<target-slug>/linkedin-profile.md)
    ├── opportunity-alignment-view  (out/<target-slug>/opportunity-alignment.md)
    ├── executive-brief-view         (out/<target-slug>/executive-brief.md)
    └── playbook-assembler          (out/<target-slug>/playbook.md & out/<target-slug>/interview-cheatsheet.md)
16. projection-validator            (out/<target-slug>/runtime/projection-validation-report.yaml)
17. brand-validator                 (out/<target-slug>/runtime/brand-validation-report.yaml)
```

## Post-Execution Summary

Upon completion, present the final output summary:
- OKF bundle path (`./out/okf/`)
- Target Opportunity Output Subtree (`./out/<target-slug>/`)
- Executive Identity path (`./out/okf/executive-identity.md`)
- Story Library path (`./out/okf/story-library.md`)
- Runtime analysis path (`./out/<target-slug>/runtime/opportunity-analysis.yaml`)
- Executive Resume path (`./out/<target-slug>/resume-executive.md`)
- ATS Resume path (`./out/<target-slug>/resume-ats.md`)
- Recruiter Resume path (`./out/<target-slug>/resume-recruiter.md`)
- Cover Letter path (`./out/<target-slug>/cover-letter.md`)
- LinkedIn Profile path (`./out/<target-slug>/linkedin-profile.md`)
- Playbook view path (`./out/<target-slug>/playbook.md`)
- Executive Brief path (`./out/<target-slug>/executive-brief.md`)
- Opportunity Alignment path (`./out/<target-slug>/opportunity-alignment.md`)
- Interview cheat sheet path (`./out/<target-slug>/interview-cheatsheet.md`)
- Projection Validation report (`./out/<target-slug>/runtime/projection-validation-report.yaml`)
- Brand Validation report (`./out/<target-slug>/runtime/brand-validation-report.yaml`)
- Unverified/Draft section count.
