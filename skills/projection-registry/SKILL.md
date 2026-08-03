---
name: projection-registry
description: Discovers, registers, and executes active projection Skills through a standardized Projection Contract interface.
---

# Projection Registry & SDK

## Overview

The `projection-registry` is a Runtime Layer Skill responsible for registering and orchestrating all projection Skills (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `executive-brief-view`, `opportunity-alignment-view`, `playbook-assembler`).

It enforces the **Projection Contract**, ensuring every projection is a pluggable, read-only, opportunity-aware presentation view over canonical knowledge, scoped under `out/<target-slug>/`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

1. **Canonical Immutability**: Projections MUST NOT write to or mutate any concept file inside `okf/`.
2. **Single Opportunity Analysis**: Projections MUST NOT re-derive opportunity analysis; they consume `out/<target-slug>/runtime/opportunity-analysis.yaml`.
3. **Pluggable Architecture**: Adding a new projection requires registering its contract rather than modifying orchestrator architecture.

## Projection Contract Interface

Every registered projection Skill implements:

- **Metadata**:
  - `name`: Unique identifier (e.g. `resume-projection`)
  - `version`: "0.5"
  - `target_audience`: Primary persona (e.g. `Executive`, `Recruiter`, `ATS`)
- **Inputs**:
  - Canonical OKF Bundle (`okf/`)
  - Shared Opportunity Analysis (`out/<target-slug>/runtime/opportunity-analysis.yaml`)
  - Projection Config (`config/config.yaml`)
- **Outputs**:
  - Presentation Artefact(s) in `out/<target-slug>/`
  - Validation metrics for `projection-validator`

## Execution Instructions

1. **Discover Registered Projections**: Scan `skills/` for registered projection contracts.
2. **Validate Input Availability**: Confirm `okf/` bundle and `out/<target-slug>/runtime/opportunity-analysis.yaml` exist.
3. **Execute Registered Projections**:
   - `resume-projection` ➔ `out/<target-slug>/resume-executive.md`, `out/<target-slug>/resume-ats.md`, `out/<target-slug>/resume-recruiter.md`
   - `cover-letter-projection` ➔ `out/<target-slug>/cover-letter.md`
   - `linkedin-projection` ➔ `out/<target-slug>/linkedin-profile.md`
   - `opportunity-alignment-view` ➔ `out/<target-slug>/opportunity-alignment.md`
   - `executive-brief-view` ➔ `out/<target-slug>/executive-brief.md`
   - `playbook-assembler` ➔ `out/<target-slug>/playbook.md`, `out/<target-slug>/interview-cheatsheet.md`
4. **Log State**: Write registration log to `out/<target-slug>/runtime/projection-registry.yaml`.
5. **Append Log**: `okf/log.md`.
