# Runtime Qualification Skill Contract: `upwork-qualification` (V2.0)

## Overview

`upwork-qualification` is a Runtime Layer Skill. It evaluates target opportunity requirements against canonical OKF evidence to produce an authoritative qualification decision and machine-readable execution context at `out/<target-slug>/runtime/upwork-qualification.yaml`.

---

## Input & Output Declarations

- **Inputs**:
  - `config/config.yaml`
  - `out/<target-slug>/runtime/opportunity-analysis.yaml`
  - `out/okf/evidence/*.md` (Canonical Evidence Cards with V2.0 frontmatter metadata)
  - `out/okf/employment-records.yaml`
- **Outputs**:
  - `out/<target-slug>/runtime/upwork-qualification.yaml`
  - `okf/log.md` (append entry)

---

## Machine-Readable Predicate Contract

The qualification engine MUST evaluate the deterministic predicate:

$$\text{PERSONAL\_PRODUCTION\_IMPLEMENTATION\_EXPERIENCE}(E, R) \iff$$

$$\big(E.\text{organisation.id} == R.\text{target\_organisation\_id} \lor R.\text{organisation\_bound} == \text{ANY}\big)$$
$$\land \big(E.\text{project.id} == R.\text{target\_project\_id} \lor R.\text{project\_bound} == \text{ANY}\big)$$
$$\land \big(E.\text{environment} == \text{production} \land E.\text{production\_verified} == \text{true}\big)$$
$$\land \big(E.\text{implementation\_role} \in \{\text{lead\_architect}, \text{sole\_developer}, \text{contributor}\}\big)$$

---

## Prohibited Negative Inferences (FR-08)

The skill MUST NOT infer `production_verified: true` from:
1. Employment relationship alone
2. Employer name
3. Repository name (e.g. `pca-productionagents-a2a`)
4. Directory or file paths
5. Markdown prose words ("production", "deployed", "operational")
6. Technology names
7. Evaluation metrics / latency tables
8. Personal projects (`organisation.id: personal-cas`)
9. Prototype / lab / innovation titles

---

## Qualification Gate Semantics

| `production_status` | Requirement Type | `decision` | `proposal_generation` | Required Action |
| :--- | :--- | :--- | :--- | :--- |
| `verified_production` | Hard / Dealbreaker | `APPLY` | `allowed` | Render submission-ready proposal |
| `unknown` | Explicit Dealbreaker | `DO NOT APPLY` | `blocked` | Render Gate Report only |
| `unknown` | Non-Dealbreaker | `CONDITIONAL` | `allowed_with_conditions` | Attach `[OPEN CONDITION]` prompt |
| `verified_non_production` | Hard / Dealbreaker | `DO NOT APPLY` | `blocked` | Render Gate Report only |
