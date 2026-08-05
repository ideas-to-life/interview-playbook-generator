---
name: playbook-orchestrator
description: Primary entry point orchestrating the v0.6 Career Projection Platform pipeline across Knowledge, Runtime, Coaching, Projection, and Evaluation layers.
---

# Playbook Orchestrator

## Overview

The `playbook-orchestrator` is the primary entry point for generating the Career Projection Platform suite (Executive Identity, Story Library, Resumes, Cover Letter, LinkedIn Profile, Interview Playbook, Executive Brief, Opportunity Alignment, Cheat Sheet, Projection Strategy, Opportunity Fit Report, and Validation Reports). It reads configuration, validates inputs, guides execution across the five-layer pipeline, and ensures all hard rules are upheld.

Outputs are cleanly separated: canonical career knowledge is stored in `out/okf/`, while opportunity-specific runtime context, validation reports, and presentation views are written to `out/<target-slug>/` (derived from `target_opportunity.source` in `config/config.yaml`). Evaluation artifacts reside in `evaluation/opportunities/`.

## Pre-Flight Configuration & Validation Protocol

Before executing pipeline steps, perform this Pre-Flight Check:

1. **Locate Configuration**: Check for `config/config.yaml` in the workspace root.
2. **Validate Required Fields**:
   - `candidate.name`
   - `candidate.portfolio_dir` (default: `evidence/` or `inputs/`)
   - `target_opportunity.source` (path to target JD / position spec, e.g. `evidence/target-position/senior-architect-vallum`)
3. **Execution Gate**:
   - **IF `config/config.yaml` EXISTS AND `target_opportunity.source` IS SPECIFIED**: Immediately proceed through Step 1 to Step 22. **DO NOT ask the user any questions, DO NOT prompt to create config/config.yaml, and DO NOT ask for a job description file.**
   - **ONLY IF `config/config.yaml` IS MISSING OR `target_opportunity.source` IS EMPTY**: Trigger the stop-and-ask protocol to request the target opportunity file path from the user.

## The Five Hard Rules

1. **Never Fabricate**: Never invent projects, metrics, team sizes, budgets, technologies, responsibilities, or tenure.
2. **Classify Every Claim**: Every non-empty non-heading line in concept bodies must start with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attribute Every Claim**: Every `[evidence]` line must carry a `[^source-id]` footnote pointing to a valid source in frontmatter.
4. **Stop and Ask**: Pause and prompt ONLY when required inputs (`config/config.yaml` or `target_opportunity.source`) are missing or unparseable.
5. **Idempotent Re-runs**: Re-running a Skill overwrites its own output directory cleanly.

## Pipeline Execution Order (v0.6 Sprint 6)

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

RUNTIME INTELLIGENCE LAYER (derived execution context; writes to out/<target-slug>/runtime/)
12. opportunity-analyzer            (out/<target-slug>/runtime/opportunity-analysis.yaml)
13. archetype-classifier            (out/<target-slug>/runtime/archetype-analysis.yaml)
14. gap-classifier                  (out/<target-slug>/runtime/gap-analysis.yaml)
15. archetype-fit-evaluator         (out/<target-slug>/runtime/opportunity-fit-report.yaml)
16. projection-strategy-generator   (out/<target-slug>/runtime/projection-strategy.yaml)

COACHING LAYER (derived; reads canonical + opportunity-analysis)
17. interview-strategy-generator
18. knowledge-gaps                  (Pre-assembly gate)

PROJECTION & VALIDATION LAYER (views & reports; writes to out/<target-slug>/)
19. projection-registry             (Orchestrates registered projections)
    ├── resume-projection           (out/<target-slug>/resume-executive.md, resume-ats.md, resume-recruiter.md)
    ├── cover-letter-projection     (out/<target-slug>/cover-letter.md)
    ├── linkedin-projection         (out/<target-slug>/linkedin-profile.md)
    ├── opportunity-alignment-view  (out/<target-slug>/opportunity-alignment.md)
    ├── executive-brief-view         (out/<target-slug>/executive-brief.md)
    └── playbook-assembler          (out/<target-slug>/playbook.md & out/<target-slug>/interview-cheatsheet.md)
20. projection-validator            (out/<target-slug>/runtime/projection-validation-report.yaml)
21. archetype-fit-validator        (out/<target-slug>/runtime/projection-validation-report.yaml overpositioning check)
22. brand-validator                 (out/<target-slug>/runtime/brand-validation-report.yaml)

EVALUATION LAYER (learning & feedback; writes to evaluation/opportunities/)
23. market-feedback-evaluator      (evaluation/opportunities/<target-slug>-evaluation.yaml)
```

## Post-Execution Summary

Upon completion, present the final output summary:
- OKF bundle path (`./out/okf/`)
- Target Opportunity Output Subtree (`./out/<target-slug>/`)
- Archetype Analysis (`./out/<target-slug>/runtime/archetype-analysis.yaml`)
- Gap Analysis (`./out/<target-slug>/runtime/gap-analysis.yaml`)
- Opportunity Fit Report (`./out/<target-slug>/runtime/opportunity-fit-report.yaml`)
- Projection Strategy (`./out/<target-slug>/runtime/projection-strategy.yaml`)
- Resumes & Cover Letter (`./out/<target-slug>/`)
- Playbook & Brief (`./out/<target-slug>/`)
- Validation Reports (`./out/<target-slug>/runtime/`)
- Market Evaluation (`./evaluation/opportunities/`)
