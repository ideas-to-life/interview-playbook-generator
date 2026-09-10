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
2. **Production Evidence Integrity**:
   - Personal projects, prototypes, labs, architecture exercises, proof-of-concepts, or innovation work MUST NOT satisfy explicit client requirements for production implementation inside a real company.
   - Production status MUST distinguish `verified_production`, `verified_non_production`, `unknown`, `not_applicable`.
3. **Control Boundary Enforcement**:
   - Output includes `proposal_generation` control semantics:
     - `APPLY` → `proposal_generation: allowed`
     - `CONDITIONAL` → `proposal_generation: allowed_with_conditions`
     - `DO NOT APPLY` → `proposal_generation: blocked`
4. **Zero Proposal Generation**:
   - `upwork-qualification` MUST NOT generate client-facing proposal prose markdown files (`upwork-qualification-report.md`).

## Taxonomy & Schema

Requirements are classified as:
- **Relationship**: `direct` | `adjacent` | `transferable` | `absent`
- **Evidence Strength**: `strong` | `moderate` | `weak`
- **Production Status**: `verified_production` | `verified_non_production` | `unknown` | `not_applicable`

## Output Schema (`out/<target-slug>/runtime/upwork-qualification.yaml`)

```yaml
version: "1.0"
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
