---
name: upwork-qualification
description: Evaluates an Upwork target opportunity against canonical OKF evidence to produce a machine-readable qualification assessment and evidence gap context at out/<target-slug>/runtime/upwork-qualification.yaml.
---

# Upwork Opportunity Qualification (V2.1)

## Overview

`upwork-qualification` is a Runtime Layer Skill. It reads the target opportunity analysis (`out/<target-slug>/runtime/opportunity-analysis.yaml`) and canonical OKF evidence (`out/okf/`) to produce an explicit, evidence-grounded qualification context at `out/<target-slug>/runtime/upwork-qualification.yaml`.

In V2.1, machine evidence completeness is strictly decoupled from human application decisions. Incomplete or unknown evidence DOES NOT automatically abort proposal generation; instead, the machine surfaces explicit evidence gaps and candidate confirmation questions, emitting an advisory `machine_recommendation` while leaving `user_decision_state` under human control.

## Hard Rules

1. **Five Hard Rules & V2.0 Contract Preservation**:
   - Never fabricate projects, metrics, team sizes, budgets, technologies, responsibilities, or tenure.
   - Retain all V2.0 Evidence Integrity Contract protections against fabrication, implicit production inference, employment-to-production inference, repository-name-to-production inference, metrics-to-production inference, personal-project contamination, cross-organisation evidence composition, and cross-project evidence composition.
   - Forensic Case Preservation: Employment at an organisation (e.g. WPP Media) plus prototype/non-production evidence plus personal project evidence (e.g. CAS) CANNOT produce `verified_production` or `SUPPORTED` client production status.
2. **Production Evidence Integrity**:
   - Production status MUST NOT be inferred from employment, repository existence, metrics, deployment-like terminology, or organisational association.
   - Personal projects, prototypes, labs, architecture exercises, proofs of concept, or innovation work MUST NOT satisfy explicit client requirements for production implementation inside a real operating company.
   - Production status MUST distinguish: `verified_production`, `verified_non_production`, `unknown`, `not_applicable`.
3. **4-Tier Requirement Completeness Taxonomy**:
   - Requirements MUST be classified as:
     - `SUPPORTED`: Direct canonical evidence supports the requirement for client-facing use.
     - `PARTIALLY_SUPPORTED`: Canonical evidence supports a meaningful portion of the requirement, but missing specific requested details.
     - `UNKNOWN`: Canonical evidence does not establish whether the requirement is met.
     - `CONTRADICTED`: Canonical evidence explicitly conflicts with or contradicts the requirement.
4. **Decoupled Human Decision Ownership**:
   - The machine emits an advisory `machine_recommendation` (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`).
   - The final `user_decision_state` (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`) is strictly human-owned and MUST NOT be forced or automatically set by the machine.
5. **Evidence Gap & Confirmation Question Extraction**:
   - Every requirement classified as `PARTIALLY_SUPPORTED` or `UNKNOWN` MUST extract the exact missing facts (e.g., production status, role, metrics, technologies) and generate explicit candidate confirmation questions without guessing or assuming the missing fact is true.
6. **Zero Proposal Generation**:
   - `upwork-qualification` MUST NOT generate client-facing proposal prose markdown files (`upwork-qualification-report.md`).

## Taxonomy & Output Schema (`out/<target-slug>/runtime/upwork-qualification.yaml`)

```yaml
version: "2.1"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
opportunity_title: "<Opportunity Title>"

# Machine Advisory Recommendation (Decoupled from human decision)
machine_recommendation: "STRONG_FIT | POTENTIAL_FIT | EVIDENCE_GAPS | WEAK_FIT | CLEAR_MISMATCH"
recommendation_rationale: "<Detailed explanation of evidence strengths and gaps>"

# Proposal Content Mode & Submission Readiness
proposal_content_mode: "EVIDENCE_BACKED | EVIDENCE_GAPS | HUMAN_REVIEW_REQUIRED"
submission_readiness: "SUBMISSION_READY | HUMAN_REVIEW_REQUIRED"

# Human User Decision State (Unforced, human-controlled)
user_decision_state: "APPLY | DO_NOT_APPLY | HOLD_FOR_EVIDENCE"

# Deprecated V2.0 Compat Fields (Preserved for backwards compatibility)
decision: "APPLY | CONDITIONAL | DO NOT APPLY"
proposal_generation: "allowed | allowed_with_conditions | blocked"

client_buying_signals:
  - id: "signal-1"
    signal: "<Buying signal>"
    importance: "high | medium | low"

requirement_assessments:
  - requirement_id: "req-1"
    requirement_text: "<Client requirement text>"
    classification: "SUPPORTED | PARTIALLY_SUPPORTED | UNKNOWN | CONTRADICTED"
    is_dealbreaker: true
    relationship: "direct | adjacent | transferable | absent"
    evidence_strength: "strong | moderate | weak"
    production_status: "verified_production | verified_non_production | unknown | not_applicable"
    missing_facts:
      - "production_deployment_verification"
    established_facts:
      - "Multi-agent architecture design"
    matched_evidence_ids:
      - "card-01"
    candidate_confirmation_questions:
      - question_id: "q-1"
        question_text: "<Confirmation question for candidate>"
        missing_fact: "production_deployment_verification"
        impact: "<Impact on requirement satisfaction>"
    rationale: "<Detailed rationale>"

evidence_gaps:
  - gap_id: "gap-1"
    requirement_id: "req-1"
    missing_fact: "production_deployment_verification"
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
