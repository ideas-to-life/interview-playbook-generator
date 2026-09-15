# Design Spec: Opportunity-Scoped Pipeline Outputs (`out/<target-slug>/`)

> **Version:** 0.5+  
> **Status:** APPROVED  
> **Author:** Alexandre Franco & Antigravity AI Pair Programmer  
> **Date:** 2026-08-03  

---

## 1. Context & Motivation

Currently, every execution of the Career Projection Platform pipeline writes runtime analysis, validation reports, and presentation views directly into the root `out/` directory (`out/runtime/opportunity-analysis.yaml`, `out/resume-executive.md`, etc.). When the user runs the pipeline for a new target opportunity, the outputs from the previous target opportunity are overwritten.

This design specification establishes **opportunity-scoped output directories** under `out/<target-slug>/`, persisting opportunity-specific execution context, validation reports, and presentation views per target opportunity while keeping `out/okf/` as the shared canonical career knowledge graph.

---

## 2. Core Architecture & Directory Layout

### 2.1 Shared Canonical Knowledge Graph (`out/okf/`)
Canonical career knowledge (Achievements, STAR Evidence Cards, Capabilities, Signature Achievements, Executive Identity, Voice Profile, Positioning Statements, Story Library, Messaging Library) is independent of any target opportunity. It remains stored in the shared directory:
```
out/okf/
├── achievements/
├── capabilities/
├── evidence/
├── executive-identity.md
├── voice-profile.md
├── positioning-statements.md
├── narrative-library.md
├── story-library.md
├── messaging-library.md
├── behaviour-profile.md
└── log.md
```

### 2.2 Opportunity-Scoped Execution & View Subtree (`out/<target-slug>/`)
Every target opportunity derives a unique URL/file slug from `target_opportunity.source` (e.g., `evidence/target-position/senior-architect-vallum` -> `senior-architect-vallum` or `inputs/head-of-ai.pdf` -> `head-of-ai`).

All opportunity-specific runtime execution context, validation reports, and presentation projection views are written to `out/<target-slug>/`:

```
out/<target-slug>/
├── runtime/
│   ├── opportunity-analysis.yaml
│   ├── projection-validation-report.yaml
│   └── brand-validation-report.yaml
├── resume-executive.md
├── resume-ats.md
├── resume-recruiter.md
├── cover-letter.md
├── linkedin-profile.md
├── opportunity-alignment.md
├── executive-brief.md
├── playbook.md
└── interview-cheatsheet.md
```

---

## 3. Target Slug Derivation Logic

The target opportunity slug `<target-slug>` is derived deterministically from `target_opportunity.source` in `config/config.yaml`:

1. Strip path directory prefixes and file extensions from `target_opportunity.source`:
   - `evidence/target-position/senior-architect-vallum` -> `senior-architect-vallum`
   - `inputs/head-of-ai.pdf` -> `head-of-ai`
   - `evidence/target-position/head-of-ai-vervaunt.md` -> `head-of-ai-vervaunt`
2. Sanitize to lowercase alphanumeric characters and single hyphens.
3. Fall back to `default-opportunity` if `target_opportunity.source` is absent.
4. Optional override: If `target_opportunity.slug` is explicitly provided in `config/config.yaml`, use it directly.

---

## 4. Affected Skills

The following Skills will be updated to consume and produce paths under `out/<target-slug>/`:

| Layer | Skill | Updated Output Path |
|---|---|---|
| **Runtime** | `opportunity-analyzer` | `out/<target-slug>/runtime/opportunity-analysis.yaml` |
| **Coaching** | `interview-strategy-generator` | Reads `out/<target-slug>/runtime/opportunity-analysis.yaml` |
| **Coaching** | `knowledge-gaps` | Reads `out/<target-slug>/runtime/opportunity-analysis.yaml` |
| **Projection** | `projection-registry` | Orchestrates projections into `out/<target-slug>/` |
| **Projection** | `resume-projection` | `out/<target-slug>/resume-executive.md`, `resume-ats.md`, `resume-recruiter.md` |
| **Projection** | `cover-letter-projection` | `out/<target-slug>/cover-letter.md` |
| **Projection** | `linkedin-projection` | `out/<target-slug>/linkedin-profile.md` |
| **Projection** | `opportunity-alignment-view` | `out/<target-slug>/opportunity-alignment.md` |
| **Projection** | `executive-brief-view` | `out/<target-slug>/executive-brief.md` |
| **Projection** | `playbook-assembler` | `out/<target-slug>/playbook.md`, `out/<target-slug>/interview-cheatsheet.md` |
| **Runtime** | `projection-validator` | `out/<target-slug>/runtime/projection-validation-report.yaml` |
| **Runtime** | `brand-validator` | `out/<target-slug>/runtime/brand-validation-report.yaml` |
| **Orchestration**| `playbook-orchestrator` | Orchestrates execution and summarizes `out/<target-slug>/` outputs |

---

## 5. Idempotency & Overwrite Policy

Re-running `playbook-orchestrator` for the same `target_opportunity.source` will cleanly overwrite `out/<target-slug>/` for that specific target opportunity, leaving other target opportunity directories (e.g. `out/head-of-ai/` vs `out/senior-architect-vallum/`) intact.
