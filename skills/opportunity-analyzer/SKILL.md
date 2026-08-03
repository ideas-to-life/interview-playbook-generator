---
name: opportunity-analyzer
description: Parses the target opportunity spec and generates the shared execution context at out/<target-slug>/runtime/opportunity-analysis.yaml.
---

# Target Opportunity Analyzer

## Overview

`opportunity-analyzer` is a Runtime Layer Skill. It reads the target opportunity configuration and JD from `config/config.yaml`, auto-derives the target opportunity slug `<target-slug>` from `target_opportunity.source` (e.g. `evidence/target-position/senior-architect-vallum` -> `senior-architect-vallum`), and generates a single structured YAML file at `out/<target-slug>/runtime/opportunity-analysis.yaml`.

This artefact is generated **once** per pipeline run and serves as the single source of opportunity reasoning consumed by all downstream projections (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `interview-strategy-generator`, `executive-brief-view`, `opportunity-alignment-view`, `playbook-assembler`).

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Do NOT modify any files in the canonical `okf/` bundle. The OKF bundle contains only canonical career knowledge. `out/<target-slug>/runtime/opportunity-analysis.yaml` is a derived runtime execution context stored in the opportunity-scoped directory.

## Target Slug Derivation

The target opportunity slug `<target-slug>` is derived as follows:
1. Parse `target_opportunity.source` from `config/config.yaml`.
2. Extract the file or folder basename (e.g., `evidence/target-position/senior-architect-vallum.md` -> `senior-architect-vallum`).
3. Sanitize to lowercase alphanumeric characters and single hyphens.
4. Optional override: If `target_opportunity.slug` is provided in `config/config.yaml`, use it directly.

## Input & Output Contracts

- **Inputs**: `config/config.yaml` (target_opportunity declarations), `target_opportunity.source` (JD / role spec).
- **Outputs**:
  - `out/<target-slug>/runtime/opportunity-analysis.yaml`
  - `okf/log.md` (append entry)

## Concept Schema & Structure (`out/<target-slug>/runtime/opportunity-analysis.yaml`)

```yaml
version: "0.5"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
target_opportunity:
  company: "<Company>"
  role_title: "<Role Title>"
  industry: "<Industry>"
  interviewer: "<Interviewer>"

hiring_goals:
  - "<Hiring Goal 1>"
  - "<Hiring Goal 2>"

executive_positioning: "<Recommended professional positioning sentence>"

capability_priorities:
  - capability: "<Capability Title 1>"
    priority: "<High | Medium | Low>"

behaviour_expectations:
  - "<Behaviour Expectation 1>"
  - "<Behaviour Expectation 2>"

ats_vocabulary:
  mandatory:
    - "<Term 1>"
  strong:
    - "<Term 2>"
  optional:
    - "<Term 3>"

organisational_signals:
  company_maturity: "<Maturity>"
  delivery_style: "<Style>"
  governance_expectations: "<Expectations>"

risks:
  - "<Risk 1>"

coverage_matrix:
  - requirement: "<Requirement>"
    coverage: "<High | Medium | Low>"
    confidence: "<Strong | Moderate | Weak>"
    primary_evidence: ["<slug-1>", "<slug-2>"]
    capabilities: ["<capability-slug>"]
```

## Execution Instructions

1. **Read `config/config.yaml`**: Parse `target_opportunity` settings, target file path, and derive `<target-slug>`.
2. **Read Target Opportunity Source**: Parse JD, recruiter notes, and hiring manager context.
3. **Extract Hiring Goals & Positioning**: Formulate hiring goals and executive positioning.
4. **Rank Capability Priorities**: Map capabilities from `okf/capabilities/` to target role importance.
5. **Extract ATS Vocabulary**: Categorise key terminology into `mandatory`, `strong`, and `optional`.
6. **Build Opportunity Coverage Matrix**: Map major hiring requirements to OKF evidence slugs and capabilities.
7. **Write `out/<target-slug>/runtime/opportunity-analysis.yaml`**.
8. **Append Log**: `okf/log.md`.
