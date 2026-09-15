---
name: upwork-qualification
description: Evaluates an Upwork target opportunity against canonical OKF evidence to produce a machine-readable qualification assessment and evidence gap context at out/<target-slug>/runtime/upwork-qualification.yaml.
---

# Upwork Opportunity Qualification (V3.1)

## Overview

`upwork-qualification` is a Runtime Layer Skill. It reads the target opportunity analysis (`out/<target-slug>/runtime/opportunity-analysis.yaml`) and canonical OKF evidence (`out/okf/`) to produce an explicit, evidence-grounded qualification context at `out/<target-slug>/runtime/upwork-qualification.yaml`.

In V3.1, candidate contribution is evaluated upstream via 7 independent attribution dimensions and recorded in structured `attributed_historical_claims`. Machine evidence completeness is strictly decoupled from human application decisions across 3 independent state axes (`requirement_qualification_status`, `content_generation_safety`, `user_decision_state`). Per FR-063, all rules, schemas, and prompts are 100% candidate-agnostic.

## Hard Rules

1. **Five Hard Rules & V3.1 Engine Rule (FR-063)**:
   - Never fabricate projects, metrics, team sizes, budgets, technologies, responsibilities, or tenure.
   - Candidate-Agnostic Engine: Schema, prompts, and qualification rules MUST NOT hardcode employer names, project names, or specific candidate identity facts. All evidence attributes are consumed dynamically.
   - Retain all V2.0/V2.1 Evidence Integrity Contract protections against fabrication, implicit production inference, employment-to-production inference, repository-name-to-production inference, metrics-to-production inference, personal-project contamination, cross-organisation evidence composition, and cross-project evidence composition.
2. **7 Independent Attribution Dimensions**:
   - Qualification and attribution MUST track: `subject`, `candidate_contribution`, `system_production_status`, `candidate_implementation_status`, `candidate_production_deployment_status`, `temporal_scope`, and `evidence_strength`.
   - Contribution MUST NOT be treated as a linear responsibility ladder (`advised` → `designed` → `implemented` → `deployed` → `production`).
3. **Cross-Context Composition Boundaries**:
   - `same_context`: Evidence from a single context.
   - `complementary_multi_context`: Multiple contexts aggregated for multi-domain capability presentation.
   - `unsupported_composite`: Disallowed aggregation across separate contexts to satisfy a single historical requirement.
4. **Three Independent State Axes**:
   - `requirement_qualification_status`: `SUPPORTED` | `PARTIALLY_SUPPORTED` | `UNKNOWN` | `CONTRADICTED`
   - `content_generation_safety`: `EVIDENCE_BACKED` | `EVIDENCE_SAFE_BOUNDED` | `HUMAN_REVIEW_REQUIRED`
   - `user_decision_state`: `APPLY` | `DO_NOT_APPLY` | `HOLD_FOR_EVIDENCE` (Unforced, human-owned)
5. **Precision Evidence Gap & Confirmation Questions**:
   - Every requirement classified as `PARTIALLY_SUPPORTED` or `UNKNOWN` MUST extract missing candidate implementation facts and generate target candidate confirmation questions.
6. **Zero Proposal Generation**:
   - `upwork-qualification` MUST NOT generate client-facing proposal prose markdown files (`upwork-qualification-report.md`).

## Taxonomy & Output Schema (`out/<target-slug>/runtime/upwork-qualification.yaml`)

```yaml
version: "3.1"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
opportunity_title: "<Opportunity Title>"

# 1. Machine Advisory Recommendation & Content Safety
machine_recommendation: "STRONG_FIT | POTENTIAL_FIT | EVIDENCE_GAPS | WEAK_FIT | CLEAR_MISMATCH"
recommendation_rationale: "<Detailed explanation of evidence strengths and gaps>"

proposal_content_mode: "EVIDENCE_BACKED | EVIDENCE_SAFE_BOUNDED | HUMAN_REVIEW_REQUIRED"
submission_readiness: "SUBMISSION_READY | HUMAN_REVIEW_REQUIRED"

# 2. Human User Decision State (Unforced, human-controlled sovereignty)
user_decision_state: "APPLY | DO_NOT_APPLY | HOLD_FOR_EVIDENCE"

# 3. Attributed Historical Claims (Candidate-Agnostic Generic Schema)
attributed_historical_claims:
  - claim_id: "claim-01"
    subject: "candidate | organisation | platform_system | project_team | proposed_solution"
    organisation: "<Organisation Name>"
    project_system_platform: "<Project/System Name>"
    candidate_contribution: "advised | assessed | recommended | aligned | shaped_architecture | architected | designed | led | implemented | deployed | operated"
    system_production_status: "verified_production | verified_non_production | prototype | unknown | not_applicable"
    candidate_implementation_status: "verified_production | implementation_in_progress | prototype | architecture_only | unknown"
    candidate_production_deployment_status: "verified_production | unverified | not_applicable"
    temporal_scope: "historical | proposed"
    evidence_strength: "strong | moderate | weak"
    evidence_card_ids:
      - "card-01"
    source_ids:
      - "source-01"
    claim_text_template: "<Generic evidence-grounded claim template>"

# 4. Multi-Axis Requirement Assessments
requirement_assessments:
  - requirement_id: "req-1"
    requirement_text: "<Client requirement text>"
    is_dealbreaker: true
    
    # 3 Independent State Axes
    requirement_qualification_status: "SUPPORTED | PARTIALLY_SUPPORTED | UNKNOWN | CONTRADICTED"
    content_generation_safety: "EVIDENCE_BACKED | EVIDENCE_SAFE_BOUNDED | HUMAN_REVIEW_REQUIRED"
    
    # Independent Attribution Dimensions
    subject: "candidate"
    candidate_contribution: "architected"
    system_production_status: "verified_production"
    candidate_implementation_status: "architecture_only"
    candidate_production_deployment_status: "unverified"
    evidence_strength: "strong | moderate | weak"
    
    composition_classification: "same_context | complementary_multi_context | unsupported_composite"
    
    missing_facts:
      - "candidate_personal_production_deployment_verification"
    established_facts:
      - "Enterprise architecture leadership"
    matched_evidence_ids:
      - "card-01"
    candidate_confirmation_questions:
      - question_id: "q-1"
        question_text: "<Target confirmation question for candidate>"
        missing_fact: "candidate_personal_production_deployment_verification"
        impact: "<Impact on requirement satisfaction>"
    rationale: "<Detailed rationale>"

# Deprecated V2.0 Compat Fields (Preserved for backwards compatibility)
classification: "SUPPORTED | PARTIALLY_SUPPORTED | UNKNOWN | CONTRADICTED"
decision: "APPLY | CONDITIONAL | DO NOT APPLY"
proposal_generation: "allowed | allowed_with_conditions | blocked"

client_buying_signals:
  - id: "signal-1"
    signal: "<Buying signal>"
    importance: "high | medium | low"

evidence_gaps:
  - gap_id: "gap-1"
    requirement_id: "req-1"
    missing_fact: "candidate_personal_production_deployment_verification"
    confirmation_question: "<Confirmation question>"

claim_traceability:
  - claim: "<Claim statement>"
    evidence_id: "card-01"
    classification: "evidence | inference | recommendation"
    source_reference: "inputs/cv.pdf"
```

## Execution Logic

1. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**: Extract client requirements, screening questions, buying signals, and coverage matrix.
2. **Retrieve Authoritative OKF Evidence**: Load evidence cards (`out/okf/evidence-cards/`), signature achievements (`out/okf/signature-achievements.md`), and capabilities (`out/okf/capabilities/`).
3. **Assess Requirement Evidence Completeness**:
   - For each material requirement, classify as `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED`.
   - Distinguish production status (`verified_production`, `verified_non_production`, `unknown`). Do NOT infer production status from employment at WPP or personal projects in CAS.
4. **Extract Missing Facts & Generate Confirmation Questions**:
   - For every `PARTIALLY_SUPPORTED` or `UNKNOWN` requirement, identify specific `missing_facts` and generate candidate confirmation questions.
5. **Determine Machine Recommendation & Submission Readiness**:
   - `submission_readiness: SUBMISSION_READY` if all client-facing claims are `SUPPORTED` and all material conditions resolved.
   - `submission_readiness: HUMAN_REVIEW_REQUIRED` if 1+ material requirements are `UNKNOWN` or `PARTIALLY_SUPPORTED`.
   - Set `proposal_content_mode` (`EVIDENCE_BACKED`, `EVIDENCE_GAPS`, `HUMAN_REVIEW_REQUIRED`).
6. **Preserve Unforced Human Decision State**:
   - Record `user_decision_state` as pending candidate input (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`).
7. **Populate Claim Traceability & Write Context**:
   - Build `claim_traceability` array and write `out/<target-slug>/runtime/upwork-qualification.yaml`.
