---
name: upwork-qualification
description: Evaluates an Upwork target opportunity against canonical OKF evidence to produce a machine-readable qualification decision at out/<target-slug>/runtime/upwork-qualification.yaml.
---

# Upwork Opportunity Qualification

## Overview

`upwork-qualification` is a Runtime Layer Skill. It reads the target opportunity analysis (`out/<target-slug>/runtime/opportunity-analysis.yaml`) and canonical OKF evidence (`out/okf/`) to produce an explicit qualification decision and control state at `out/<target-slug>/runtime/upwork-qualification.yaml`.

The qualification gate evaluates whether an opportunity can be pursed credibly without fabrication or production inflation.

## Hard Rules

1. **Five Hard Rules Compliance**:
   - Never fabricate projects, metrics, team sizes, budgets, technologies, responsibilities, or tenure.
   - Preserves 4-layer architectural boundaries.
2. **Production Evidence Integrity & Contract V2.0 Predicate**:
   - Qualification MUST evaluate candidate evidence using the deterministic `PERSONAL_PRODUCTION_IMPLEMENTATION_EXPERIENCE` predicate:
     $$\text{PERSONAL\_PRODUCTION\_IMPLEMENTATION\_EXPERIENCE}(E, R) \iff$$
     $$\big(E.\text{organisation.id} = R.\text{target\_organisation\_id} \lor R.\text{organisation\_bound} = \text{ANY}\big)$$
     $$\land \big(E.\text{project.id} = R.\text{target\_project\_id} \lor R.\text{project\_bound} = \text{ANY}\big)$$
     $$\land \big(E.\text{environment} = \text{production} \land E.\text{production\_verified} = \text{true}\big)$$
     $$\land \big(E.\text{implementation\_role} \in \{\text{lead\_architect}, \text{sole\_developer}, \text{contributor}\}\big)$$
   - Both matching `organisation.id` AND matching `project.id` are MANDATORY for system/project-specific production implementation requirements.
   - Personal projects (`organisation.id: personal-cas`), prototypes, labs, architecture exercises, or unverified resume claims MUST NOT satisfy explicit client requirements for production implementation inside a commercial enterprise.
3. **15 Prohibited Inference Rules (Negative Constraints)**:
   The engine MUST NOT infer `production_verified = true` from any of:
   1. Employment relationship or title
   2. Employer name
   3. Repository name (e.g. `pca-productionagents-a2a`)
   4. Directory/folder name
   5. "production" in free-text prose
   6. "deployed" in free-text prose
   7. "operational" in free-text prose
   8. Technology selection
   9. Evaluation metrics
   10. High success rate
   11. Low latency benchmarks
   12. CI/CD or architecture diagrams
   13. Case study slide decks
   14. Personal CAS project evidence
   15. Unverified resume claims
4. **Cross-Organisation & Cross-Project Isolation**:
   - Evidence from Company B cannot satisfy Company A production requirements.
   - Evidence from Project X cannot satisfy Project Y requirements, even within the same organisation.
5. **Dealbreaker Hard Gate & Control Semantics**:
   - Explicit dealbreaker requirement ("If you have not already done this in production, do not apply") + `UNKNOWN` or `VERIFIED_NON_PRODUCTION` status $\rightarrow$ `decision: DO NOT APPLY` (`proposal_generation: blocked`).
   - `UNKNOWN` status for an explicit dealbreaker requirement MUST NEVER evaluate to `CONDITIONAL` or `APPLY`.
   - Control semantics:
     - `APPLY` $\rightarrow$ `proposal_generation: allowed`
     - `CONDITIONAL` $\rightarrow$ `proposal_generation: allowed_with_conditions`
     - `DO NOT APPLY` $\rightarrow$ `proposal_generation: blocked`
6. **Zero Proposal Generation**:
   - `upwork-qualification` MUST NOT generate client-facing proposal prose markdown files (`upwork-qualification-report.md`).

## Taxonomy & Schema

Requirements are classified as:
- **Relationship**: `direct` | `adjacent` | `transferable` | `absent`
- **Evidence Strength**: `strong` | `moderate` | `weak`
- **Production Status**: `verified_production` | `verified_non_production` | `unknown` | `not_applicable`

## Output Schema (`out/<target-slug>/runtime/upwork-qualification.yaml`)

```yaml
version: "2.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
decision: "APPLY | CONDITIONAL | DO NOT APPLY"
proposal_generation: "allowed | allowed_with_conditions | blocked"
confidence: "HIGH | MEDIUM | LOW"
overall_rationale: "<Detailed explanation>"

client_buying_signals:
  - id: "signal-1"
    signal: "<Buying signal>"
    importance: "high | medium | low"

hard_requirements:
  - requirement_id: "req-1"
    requirement: "<Client hard requirement>"
    status: "met | partially_met | not_met"
    relationship: "direct | adjacent | transferable | absent"
    evidence_strength: "strong | moderate | weak"
    production_status: "verified_production | verified_non_production | unknown | not_applicable"
    evidence_sources:
      - "card-01"
    rationale: "<Rationale>"

preferred_requirements:
  - requirement_id: "pref-1"
    requirement: "<Preferred requirement>"
    relationship: "direct | adjacent | transferable | absent"
    evidence_strength: "strong | moderate | weak"
    evidence_sources:
      - "card-02"

strongest_evidence_matches:
  - requirement_id: "req-1"
    evidence_card_id: "card-01"
    relevance_summary: "<Relevance>"

open_conditions:
  - condition_id: "cond-1"
    fact_requiring_confirmation: "<Fact>"
    impact: "<Impact>"
    suggested_candidate_action: "<Action>"

proposal_risks:
  - risk_id: "risk-1"
    claim_to_avoid_or_qualify: "<Risk>"
    reasoning: "<Reasoning>"

recommended_work_samples:
  - sample_id: "ws-1"
    title: "<Sample Title>"
    supports_requirement: "<Requirement>"
    demonstrates_capability: "<Capability>"
    evidence_source: "card-01"

claim_traceability:
  - claim: "<Claim statement>"
    evidence_id: "card-01"
    classification: "evidence | inference | recommendation"
    source_reference: "inputs/cv.pdf"
```

## Execution Logic

1. **Read `out/<target-slug>/runtime/opportunity-analysis.yaml`**: Extract client requirements, screening questions, buying signals, and initial coverage matrix.
2. **Retrieve Authoritative OKF Evidence**: Load evidence cards (`out/okf/evidence-cards/`), signature achievements (`out/okf/signature-achievements.md`), and capabilities (`out/okf/capabilities/`).
3. **Map Requirements to Evidence**:
   - For each requirement, determine relationship (`direct`, `adjacent`, `transferable`, `absent`) and production status (`verified_production`, `verified_non_production`, `unknown`).
4. **Evaluate Qualification Gate**:
   - **DO NOT APPLY (`proposal_generation: blocked`)**:
     - Explicit hard requirement is `absent`, unsupported, or requires treating prototype/lab work as client production implementation inside a real operating company.
   - **CONDITIONAL (`proposal_generation: allowed_with_conditions`)**:
     - Requirements are potentially met, but 1+ material facts require candidate verification. List explicit `open_conditions`.
   - **APPLY (`proposal_generation: allowed`)**:
     - All hard requirements are supported by verified authoritative evidence without fabrication.
5. **Populate Claim Traceability**:
   - Build `claim_traceability` array mapping each projected claim to its source OKF evidence card ID and file path.
6. **Write `out/<target-slug>/runtime/upwork-qualification.yaml`**.
