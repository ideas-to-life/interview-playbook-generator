# Data Model & Schema Definitions: Upwork Qualification, Evidence Integrity, and Proposal Generator

## 1. OKF `EvidenceCard` Schema Extension (Knowledge Layer)

Machine-readable metadata contract added to OKF `EvidenceCard` concept frontmatter in `out/okf/evidence/<slug>.md`:

**Migration Invariant**: Metadata fields MUST be populated strictly from explicit source evidence for each individual card. Any field value not directly evidenced in source documents for that specific card MUST be set to `unknown` (or `production_verified: false`). Zero contextual inheritance or inference from parent employment records or project folders is permitted.

```yaml
---
type: EvidenceCard
id: "wpp-agentic-ai-platform"
title: "WPP Media Enterprise Agentic AI Platform Strategy"
description: "Formulated architecture strategy, reusable AI foundations, and governance frameworks for enterprise agentic systems."
tags: [agentic-ai, llm-platform, ai-governance, enterprise-architecture]
status: verified

# Machine-Readable Provenance & Identity Contract (v2.0)
organisation:
  id: "emp-wpp-media-2"             # Resolves to employment-records.yaml ID or "personal-cas"
  name: "WPP Media"
  type: "enterprise_employer"        # enterprise_employer | advisory_client | personal_project | academic

project:
  id: "wpp-open-pca"                # Unique system/project identifier slug
  name: "Polonium Consumer Agents (PCA)"

environment: "prototype"             # production | staging | prototype | lab | personal | unknown
production_verified: false          # true | false
production_evidence_type: "none"    # telemetry | release_notes | client_signoff | attested_claim | none
implementation_role: "lead_architect"# lead_architect | sole_developer | contributor | advisor | evaluator | none

provenance:
  primary_source_id: "cv-2026"
  source_type: "resume_claim"        # production_telemetry | release_notes | client_signoff | repo_code | eval_harness | resume_claim

sources:
  - id: cv-2026
    resource: "career-history/Alexandre Franco Resume.pdf"
    title: "Alexandre Franco Resume"
---
```

---

## 2. Machine-Readable Qualification Schema (`out/<target-slug>/runtime/upwork-qualification.yaml`)

```yaml
version: "2.0"
generated_at: "2026-09-10T12:57:00+01:00"
target_slug: "upwork-senior-agentic-ai-architect"
decision: "APPLY | CONDITIONAL | DO NOT APPLY"
proposal_generation: "allowed | allowed_with_conditions | blocked"
confidence: "HIGH | MEDIUM | LOW"
overall_rationale: "Detailed qualification rationale statement."

client_buying_signals:
  - id: "signal-1"
    signal: "Requires proven production experience building multi-agent systems for real operating companies."
    importance: "high"

hard_requirements:
  - requirement_id: "req-1"
    requirement: "Production multi-agent system implementation inside a real operating company"
    is_dealbreaker: true              # true if client explicitly states "do not apply without this"
    target_organisation_id: "emp-wpp-media-2"
    target_project_id: "wpp-open-pca"
    status: "met | partially_met | not_met"
    relationship: "direct | adjacent | transferable | absent"
    evidence_strength: "strong | moderate | weak"
    production_status: "verified_production | verified_non_production | unknown"
    evidence_sources:
      - "wpp-agentic-ai-platform"
    rationale: "Evidence establishes agentic AI architecture at WPP Media in prototype environment, but does not explicitly verify live production deployment."

preferred_requirements:
  - requirement_id: "pref-1"
    requirement: "OpenAI Agents SDK / LangGraph / MCP"
    relationship: "direct"
    evidence_strength: "strong"
    evidence_sources:
      - "wpp-agentic-ai-platform"

strongest_evidence_matches:
  - requirement_id: "req-1"
    evidence_card_id: "wpp-agentic-ai-platform"
    relevance_summary: "Architected multi-agent platform strategy at WPP Media."

open_conditions:
  - condition_id: "cond-1"
    fact_requiring_confirmation: "Can candidate confirm live commercial production deployment of WPP PCA platform?"
    impact: "Determines whether req-1 meets verified production criteria."
    suggested_candidate_action: "Provide production release note or telemetry source."

proposal_risks:
  - risk_id: "risk-1"
    claim_to_avoid_or_qualify: "Native Shopify / Salesforce SDK mastery"
    reasoning: "Candidate experience is in enterprise API architecture; frame as custom API strength."

recommended_work_samples:
  - sample_id: "ws-1"
    title: "Agentic AI Platform Architecture (WPP Media)"
    supports_requirement: "Multi-agent orchestration"
    demonstrates_capability: "agentic-ai-architecture"
    evidence_source: "wpp-agentic-ai-platform"

claim_traceability:
  - claim: "Architected multi-agent platform strategy at WPP Media."
    evidence_id: "wpp-agentic-ai-platform"
    classification: "evidence"
    source_reference: "out/okf/evidence/wpp-agentic-ai-platform.md"
```

---

## 3. Human-Readable Presentation View Schemas (`out/<target-slug>/`)

### 3.1 Proposal Document (`out/<target-slug>/upwork-proposal.md`)
- **Header Block**: Qualification status (`APPLY` / `CONDITIONAL` / `DO NOT APPLY`), control state (`allowed` / `allowed_with_conditions` / `blocked`), actual word count.
- **DO NOT APPLY State**: Gate Report displaying Decision (`DO NOT APPLY`), Blocking Requirement, Available Evidence, Evidence Gap, What Would Change Decision.
- **CONDITIONAL State**: Open Condition Banner listing explicit facts requiring candidate confirmation.
- **APPLY State**: 6-part clean proposal prose free of inline metadata tags (Opening, Requirement-to-Proof Mapping, Project Snapshots, Approach, Smart Questions, CTA).

### 3.2 Screening Answers (`out/<target-slug>/upwork-screening-answers.md`)
- **Per-Question Block**: Question title, Status (`ANSWERED` / `[OPEN CONDITION: <fact>]`), Answer (direct response leading with clear facts, followed by evidence proof).

### 3.3 Work Samples (`out/<target-slug>/upwork-work-samples.md`)
- **Per-Sample Block**: Sample Title, Supports Requirement, Demonstrated Capability, Evidence Source, Approved Summary.
