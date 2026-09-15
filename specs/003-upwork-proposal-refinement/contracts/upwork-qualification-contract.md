# Interface Contract: Upwork Qualification (V3.1)

## Overview

Defines the execution interface and runtime contract for the `upwork-qualification` skill in V3.1.

---

## Inputs

1. **Target Opportunity Analysis**: `out/<target-slug>/runtime/opportunity-analysis.yaml`
2. **Canonical OKF Knowledge Graph**:
   - `out/okf/evidence-cards/*.md`
   - `out/okf/signature-achievements.md`
   - `out/okf/capabilities/*.md`

---

## Outputs

- **Upwork Qualification Context**: `out/<target-slug>/runtime/upwork-qualification.yaml`

---

## Qualification Assessment Protocol

For each client requirement in `opportunity-analysis.yaml`:

1. **Extract Evidence Candidates**: Match against canonical OKF evidence cards.
2. **Assess Independent Attribution Dimensions**:
   - Determine `subject` (`candidate`, `organisation`, `platform_system`, `project_team`, `proposed_solution`).
   - Determine `candidate_contribution` (`advised`, `assessed`, `recommended`, `aligned`, `shaped_architecture`, `architected`, `designed`, `led`, `implemented`, `deployed`, `operated`).
   - Determine `system_production_status` (`verified_production`, `verified_non_production`, `prototype`, `unknown`).
   - Determine `candidate_implementation_status` (`verified_production`, `implementation_in_progress`, `prototype`, `architecture_only`, `unknown`).
   - Determine `candidate_production_deployment_status` (`verified_production`, `unverified`, `not_applicable`).
3. **Classify Composition Boundary**:
   - `same_context`: Single project context.
   - `complementary_multi_context`: Multiple contexts for complementary capability presentation.
   - `unsupported_composite`: Disallowed aggregation across separate contexts for single requirement satisfaction.
4. **Assign 3 Independent State Axes**:
   - `requirement_qualification_status`: `SUPPORTED` | `PARTIALLY_SUPPORTED` | `UNKNOWN` | `CONTRADICTED`
   - `content_generation_safety`: `EVIDENCE_BACKED` | `EVIDENCE_SAFE_BOUNDED` | `HUMAN_REVIEW_REQUIRED`
   - `user_decision_state`: `APPLY` | `DO_NOT_APPLY` | `HOLD_FOR_EVIDENCE` (Unforced, human-owned)
5. **Generate Precision Candidate Confirmation Questions**:
   - For any unresolved candidate implementation fact, formulate target confirmation question.
