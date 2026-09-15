# Data Model Specification: Upwork Proposal Generator (V3.1)

## Overview

This document specifies the intermediate entities, runtime data structures, enums, and state transitions for V3.1 Evidence Attribution, Composition & Claim Projection Integrity.

---

## 1. Core Runtime Schema (`out/<target-slug>/runtime/upwork-qualification.yaml`)

```yaml
version: "3.1"
generated_at: "2026-09-15T09:30:00Z"
target_slug: "upwork-senior-agentic-ai-architect"
opportunity_title: "Senior Agentic AI Architect"

# 1. Machine Advisory Recommendation & Content Mode
machine_recommendation: "STRONG_FIT | POTENTIAL_FIT | EVIDENCE_GAPS | WEAK_FIT | CLEAR_MISMATCH"
recommendation_rationale: "Enterprise architecture experience verified at OrgAlpha; personal production implementation unverified."

proposal_content_mode: "EVIDENCE_BACKED | EVIDENCE_SAFE_BOUNDED | HUMAN_REVIEW_REQUIRED"
submission_readiness: "SUBMISSION_READY | HUMAN_REVIEW_REQUIRED"

# 2. Human User Decision State (Human Sovereignty)
user_decision_state: "APPLY | DO_NOT_APPLY | HOLD_FOR_EVIDENCE"

# 3. Attributed Historical Claims (Candidate-Agnostic Generic Schema)
attributed_historical_claims:
  - claim_id: "claim-org-alpha-arch"
    subject: "candidate"
    organisation: "OrgAlpha"            # Consumed dynamically from canonical evidence
    project_system_platform: "SystemAlpha" # Consumed dynamically from canonical evidence
    candidate_contribution: "architected | advised | led"
    system_production_status: "verified_production"
    candidate_implementation_status: "architecture_only"
    candidate_production_deployment_status: "unverified"
    temporal_scope: "historical"
    evidence_strength: "strong"
    evidence_card_ids:
      - "card-01"
    source_ids:
      - "source-01"
    claim_text_template: "Led architecture and alignment for agentic AI platform initiatives at OrgAlpha."

  - claim_id: "claim-proj-beta-impl"
    subject: "candidate"
    organisation: "Personal Architecture Lab"
    project_system_platform: "ProjectBeta"
    candidate_contribution: "implemented"
    system_production_status: "prototype"
    candidate_implementation_status: "verified_prototype"
    candidate_production_deployment_status: "not_applicable"
    temporal_scope: "historical"
    evidence_strength: "strong"
    evidence_card_ids:
      - "card-02"
    source_ids:
      - "source-02"
    claim_text_template: "Implemented hands-on multi-agent coordination and observability in personal architecture lab."

# 4. Multi-Axis Requirement Assessments
requirement_assessments:
  - requirement_id: "req-prod-impl"
    requirement_text: "Must have personally designed and implemented AI systems inside a real operating company in production."
    is_dealbreaker: true
    
    # 3 Independent State Axes
    requirement_qualification_status: "PARTIALLY_SUPPORTED" # SUPPORTED | PARTIALLY_SUPPORTED | UNKNOWN | CONTRADICTED
    content_generation_safety: "EVIDENCE_SAFE_BOUNDED"     # EVIDENCE_BACKED | EVIDENCE_SAFE_BOUNDED | HUMAN_REVIEW_REQUIRED
    
    # Independent Attribution Dimensions
    subject: "candidate"
    candidate_contribution: "architected"
    system_production_status: "verified_production"
    candidate_implementation_status: "architecture_only"
    candidate_production_deployment_status: "unverified"
    evidence_strength: "moderate"
    
    composition_classification: "complementary_multi_context" # same_context | complementary_multi_context | unsupported_composite
    
    established_facts:
      - "Enterprise architecture leadership at OrgAlpha"
      - "Hands-on prototype multi-agent implementation in ProjectBeta"
    missing_facts:
      - "candidate_personal_production_deployment_verification"
      
    matched_evidence_ids:
      - "card-01"
      - "card-02"
      
    candidate_confirmation_questions:
      - question_id: "q-org-alpha-prod"
        question_text: "Did you personally implement and deploy any multi-agent system into live production at OrgAlpha?"
        missing_fact: "candidate_personal_production_deployment_verification"
        impact: "Resolves candidate production deployment status for enterprise requirement."

# 5. Evidence Gap Registry
evidence_gaps:
  - gap_id: "gap-01"
    requirement_id: "req-prod-impl"
    missing_fact: "candidate_personal_production_deployment_verification"
    confirmation_question: "Did you personally implement and deploy any multi-agent system into live production at OrgAlpha?"

# 6. Provenance & Claim Traceability
claim_traceability:
  - claim_id: "claim-org-alpha-arch"
    claim: "Led architecture for enterprise agentic AI initiatives at OrgAlpha."
    evidence_id: "card-01"
    classification: "evidence"
    source_reference: "inputs/cv.pdf"
```

---

## 2. Enums & State Definitions

### Requirement Qualification Status Enum
- `SUPPORTED`: Direct canonical evidence supports candidate personal satisfaction of requirement.
- `PARTIALLY_SUPPORTED`: Canonical evidence supports adjacent or partial capabilities, but specific requested details remain unverified.
- `UNKNOWN`: Canonical evidence does not establish requirement status.
- `CONTRADICTED`: Canonical evidence conflicts with requirement.

### Content Generation Safety Enum
- `EVIDENCE_BACKED`: 100% of generated claims are backed by verified canonical evidence.
- `EVIDENCE_SAFE_BOUNDED`: Proposal/screening answer is generated using bounded formulations without claiming unverified assertions. Safe for human review.
- `HUMAN_REVIEW_REQUIRED`: Machine non-certification due to unresolved material conditions.

### Human User Decision State Enum
- `APPLY`: Candidate decides to submit application.
- `DO_NOT_APPLY`: Candidate decides to skip application.
- `HOLD_FOR_EVIDENCE`: Candidate holds application pending canonical evidence update.

### Composition Boundary Classification Enum
- `same_context`: Evidence originates from the same project/organization.
- `complementary_multi_context`: Evidence from separate projects demonstrates complementary strengths (valid for broad capability statements).
- `unsupported_composite`: Attempting to satisfy a single historical requirement by merging separate contexts (invalid for requirement qualification).

---

## 3. Data Validation Rules

1. **Candidate Agnosticism Rule (FR-063)**:
   Schemas, validators (`upwork_validator.py`), and prompts MUST NOT hardcode employer names, project names, or specific evidence strings. Production code evaluates metadata attributes (`subject`, `candidate_contribution`, `system_production_status`, `candidate_production_deployment_status`, `project_type`).
2. **Production Disambiguation Rule**:
   `system_production_status == verified_production` AND `candidate_contribution in [architected, advised, led]` DOES NOT SET `candidate_production_deployment_status = verified_production`.
3. **Anti-Inflation Rule**:
   `candidate_contribution` CANNOT be set to a value stronger than canonical evidence card `candidate_role`.
4. **Screening Consistency Rule**:
   If `requirement_qualification_status != SUPPORTED`, screening answers MUST NOT assert affirmative historical claims.
5. **Assertion-Then-Disclaimer Rule**:
   Prose generation MUST NOT produce an affirmative historical claim followed by a qualifying disclaimer.
