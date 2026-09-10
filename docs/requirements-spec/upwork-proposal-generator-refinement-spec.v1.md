Requirements Refinement Specification

Upwork Qualification & Proposal Projection — V1

Repository: ideas-to-life/interview-playbook-generator
Feature: Upwork opportunity qualification and proposal generation
Status: Requirements refinement for /specify
Version: V1 — Minimum Viable Capability
Implementation: Coding agent
Governance: Existing CAS + SLDC
Primary objective: Add Upwork proposal generation as a governed projection of canonical career evidence, with an explicit qualification gate and human approval boundary.

⸻

1. Refinement Objective

Refine the existing Upwork Proposal Generation specification so that implementation:

1. conforms to the repository’s actual four-layer architecture;
2. reuses existing opportunity analysis and OKF evidence;
3. introduces no parallel career/evidence model;
4. makes qualification an explicit Runtime Layer decision;
5. makes proposal generation a Projection Layer capability;
6. establishes qualification as a hard downstream control boundary;
7. keeps evidence provenance internal to the system rather than polluting client-facing proposal prose;
8. avoids prescribing implementation mechanisms before repository discovery;
9. integrates with the existing orchestrator, projection registry and validation mechanisms;
10. follows CAS principles of bounded, scoped, traceable processing;
11. follows the repository’s SLDC process;
12. preserves a human-review boundary before any Upwork submission.

⸻

2. Architectural Baseline

The implementation MUST conform to the existing four-layer architecture:

┌───────────────────────────────────────────┐
│  1. KNOWLEDGE LAYER                       │
│                                           │
│  Canonical career evidence / OKF          │
│  out/okf/                                 │
└──────────────────┬────────────────────────┘
                   │
                   │ governed evidence
                   ▼
┌───────────────────────────────────────────┐
│  2. RUNTIME LAYER                         │
│                                           │
│  Opportunity Analysis                     │
│  Upwork Qualification                     │
│  Validation Reports                       │
│  out/<target>/runtime/                    │
└──────────────────┬────────────────────────┘
                   │
                   │ qualified target context
                   ▼
┌───────────────────────────────────────────┐
│  3. COACHING LAYER                        │
│                                           │
│  Existing opportunity-aware strategy      │
│  and gap analysis where applicable        │
└──────────────────┬────────────────────────┘
                   │
                   │ strategy/context
                   ▼
┌───────────────────────────────────────────┐
│  4. PROJECTION LAYER                      │
│                                           │
│  Upwork proposal                          │
│  Screening answers                        │
│  Work-sample recommendations              │
│  out/<target>/                            │
└──────────────────┬────────────────────────┘
                   │
                   ▼
┌───────────────────────────────────────────┐
│  VALIDATION                               │
│                                           │
│  projection-validator                     │
│  brand-validator where applicable         │
└───────────────────────────────────────────┘
                   │
                   ▼
              HUMAN REVIEW
                   │
                   ▼
          HUMAN UPWORK SUBMISSION

The feature MUST be implemented as an extension of this architecture, not as a separate proposal-generation pipeline.

⸻

3. Core Architectural Principle

The fundamental model is:

Canonical Career Evidence
          +
Target Opportunity
          +
Opportunity Analysis
          +
Qualification Decision
          ↓
    Upwork Projection

The generated proposal is a projection, not a new source of truth.

The feature MUST NOT create:

* a second career database;
* a second evidence model;
* a second opportunity-analysis mechanism;
* an independent candidate identity;
* an unrestricted historical career scan.

⸻

4. Responsibility Boundaries

The implementation MUST preserve the following conceptual responsibilities.

Opportunity Analysis

Answers:

What does the client want?

It identifies:

* client problem;
* desired outcome;
* hard requirements;
* preferred requirements;
* technical requirements;
* buying signals;
* screening questions;
* evaluation criteria.

The existing opportunity-analyzer SHOULD be reused.

⸻

Qualification

Answers:

Should this opportunity be pursued based on what can honestly be demonstrated?

Qualification produces an explicit:

APPLY
CONDITIONAL
DO NOT APPLY

decision.

Qualification is a Runtime Layer decision.

⸻

Proposal Projection

Answers:

Given a qualified opportunity, how should the candidate present the strongest relevant evidence?

Proposal generation is a Projection Layer responsibility.

It produces client-facing material.

⸻

Validation

Answers:

Is the resulting projection consistent with the governing evidence and output constraints?

Existing validation capabilities SHOULD be extended rather than duplicated.

⸻

5. Qualification Is a Control Boundary

The qualification result MUST become an explicit control boundary for all downstream proposal generation.

Conceptually:

Opportunity
     │
     ▼
Opportunity Analysis
     │
     ▼
Qualification
     │
     ├── DO NOT APPLY ──► Proposal blocked
     │
     ├── CONDITIONAL ───► Proposal allowed with conditions
     │
     └── APPLY ─────────► Proposal allowed
                              │
                              ▼
                       Evidence Mapping
                              │
                              ▼
                       Proposal Projection

The proposal projection MUST NOT override the qualification result.

A persuasive proposal must never be able to convert:

DO NOT APPLY → APPLY

or:

CONDITIONAL → APPLY

without an explicit new qualification result.

⸻

6. Machine-Readable Qualification Semantics

The qualification result MUST include explicit downstream generation semantics.

Conceptually:

decision: DO NOT APPLY
proposal_generation: blocked
decision: CONDITIONAL
proposal_generation: allowed_with_conditions
decision: APPLY
proposal_generation: allowed

The exact schema SHOULD follow existing repository contracts.

⸻

7. Qualification Taxonomy

Requirements SHALL be classified as:

direct
adjacent
transferable
absent

Evidence strength SHALL be classified as:

strong
moderate
weak

Production status SHALL distinguish, where relevant:

verified_production
verified_non_production
unknown
not_applicable

The implementation MUST preserve these distinctions through downstream processing.

It MUST NOT silently transform:

adjacent → direct
transferable → direct
unknown → verified_production

⸻

8. Qualification Decision Rules

APPLY

APPLY MAY be returned only when:

* all explicit hard requirements are adequately supported;
* required experience is supported by authoritative evidence;
* no material evidence contradiction exists;
* no material claim would require fabrication or substantive overstatement.

⸻

CONDITIONAL

CONDITIONAL SHALL be returned when:

* the opportunity may be a legitimate fit;
* one or more material facts remain unresolved;
* the missing information could reasonably be confirmed by the candidate.

The qualification artifact MUST identify the exact unresolved facts.

⸻

DO NOT APPLY

DO NOT APPLY SHALL be returned when:

* an explicit hard requirement is clearly absent;
* authoritative evidence contradicts the requirement;
* satisfying the requirement would require fabrication;
* the client explicitly excludes the type of experience represented by the available evidence.

DO NOT APPLY is an expected business decision, not an execution failure.

⸻

9. Production Evidence Integrity

This is a mandatory hard rule.

The system MUST distinguish production implementation from:

* personal projects;
* prototypes;
* proof-of-concepts;
* demonstrations;
* architecture exercises;
* laboratories;
* theoretical knowledge;
* innovation work where production status is not explicitly established.

If the client requires:

personally implemented in production for a real company

then only authoritative evidence establishing all relevant dimensions may satisfy the requirement.

The system MUST NOT infer production status from:

* technical sophistication;
* architecture complexity;
* technology names;
* similarity to production systems;
* job title;
* seniority;
* personal projects.

⸻

10. Evidence Integrity

The system MUST never fabricate or silently infer:

* clients;
* employers;
* projects;
* production status;
* agent counts;
* workflow counts;
* team sizes;
* financial results;
* percentages;
* business outcomes;
* technologies;
* responsibilities;
* ownership;
* architecture scope;
* implementation scope.

Where evidence is incomplete, the system MUST surface the gap.

⸻

11. Qualification Evidence vs Projection Evidence

The implementation MUST distinguish two related but different activities.

Qualification evidence

Used to determine:

Is the opportunity legitimately pursuable?

This evidence establishes whether requirements are met.

Projection evidence

Used to determine:

What evidence should be presented to the client?

Projection evidence selects the strongest relevant material within the boundaries established by qualification.

The proposal generator MUST NOT use persuasive evidence selection to bypass qualification.

⸻

12. Evidence Retrieval

Evidence retrieval MUST prioritize authoritative, distilled OKF material.

Preferred order:

1. Evidence Cards;
2. Signature Achievements;
3. Capabilities;
4. Story Library;
5. Executive Identity;
6. Messaging / Narrative material;
7. target-specific evidence where authoritative and appropriate.

The implementation SHOULD use existing repository mechanisms for evidence retrieval where available.

It MUST NOT perform unrestricted repository-wide historical scanning merely to find supporting claims.

Processing should follow the established CAS principle:

bounded, relevant, incremental and governed input selection.

⸻

13. Evidence Traceability

Material generated claims MUST remain traceable internally to their canonical evidence.

Conceptually:

Client Requirement
        ↓
Qualification Decision
        ↓
Evidence
        ↓
Generated Claim

The system should be able to answer:

Why did the system make this qualification decision?

and:

What evidence supports this generated claim?

This traceability SHOULD be represented in machine-readable/runtime structures where appropriate.

⸻

14. Client-Facing Proposal vs Internal Provenance

This refinement explicitly separates:

Internal provenance

May contain:

* evidence identifiers;
* source references;
* claim classifications;
* validation metadata;
* confidence;
* relationship classification;
* production status.

Client-facing proposal

Must read as a natural, professional Upwork proposal.

The generated proposal MUST NOT mechanically expose internal metadata such as:

[evidence]
[inference]
[recommendation]
[^source-id]

unless a specific output format explicitly requires it.

The validator SHOULD verify provenance internally rather than requiring provenance markup to appear in client-facing prose.

⸻

15. Proposal Strategy

Proposal strategy remains a conceptual stage, but MUST NOT become an unnecessary independent data layer unless repository discovery establishes that such a layer already exists or is architecturally justified.

It should determine:

* strongest client buying signals;
* strongest evidence matches;
* evidence risks;
* positioning;
* relevant project examples;
* work samples;
* screening-answer approach;
* proposal emphasis.

Where possible, this strategy SHOULD remain internal to the projection workflow rather than generating another persistent artifact.

⸻

16. Proposal Projection

For APPLY, the projection SHOULD produce:

upwork-proposal.md
upwork-screening-answers.md
upwork-work-samples.md

The exact filenames MAY be adjusted if repository conventions dictate otherwise, but the three logical outputs are required.

⸻

17. Proposal Structure

Unless the client specifies a different structure, the proposal should contain:

1. Opening
    * demonstrate understanding of the client’s problem;
    * avoid generic application language.
2. Requirement-to-proof mapping
    * strongest 2–4 requirement/evidence matches.
3. Project snapshots
    * no more than three;
    * context → action → relevance.
4. Approach
    * process;
    * systems/data;
    * automation candidates;
    * deterministic automation vs AI vs agentic vs human;
    * architecture;
    * integration;
    * controls;
    * validation.
5. Smart questions
    * normally 3–5;
    * demonstrate understanding.
6. CTA
    * invite a focused discussion.

The structure is a default projection pattern, not an inflexible template.

⸻

18. Proposal Length

The default target is:

350–500 words

This is a target, not an unconditional validation failure.

Client-specific or platform-specific constraints take precedence.

The generator SHOULD optimise in this order:

1. relevance;
2. evidence;
3. clarity;
4. concision.

If a client imposes a hard limit, that limit becomes authoritative.

⸻

19. Screening Answers

Every explicit client screening question SHOULD receive a corresponding answer when proposal generation is permitted.

Rules:

1. answer the question directly;
2. support with evidence where appropriate;
3. do not evade difficult questions;
4. acknowledge missing evidence;
5. never substitute personal projects for required production experience;
6. never manufacture metrics or counts.

For CONDITIONAL, any answer dependent on unresolved information MUST explicitly identify:

[OPEN CONDITION: <fact>]

The marker is an internal/user-review mechanism and MUST NOT be confused with evidence provenance.

For DO NOT APPLY, submission-ready screening answers MUST NOT be generated.

⸻

20. Work-Sample Selection

The projection SHOULD recommend up to three relevant work samples.

Selection should follow:

Client Requirement
       ↓
Capability Demonstrated
       ↓
Available Evidence
       ↓
Strongest Appropriate Artifact

Each recommendation SHOULD identify:

* artifact;
* requirement supported;
* capability demonstrated;
* evidence basis.

Confidential or unauthorised internal material MUST NOT be recommended for external submission.

⸻

21. DO NOT APPLY Output

When qualification returns DO NOT APPLY:

proposal_generation: blocked

The system MUST NOT produce a submission-ready proposal.

It SHOULD produce a concise gate report containing:

* decision;
* blocking requirement;
* available evidence;
* evidence gap;
* rationale;
* what would change the decision.

This behaviour is intentional.

⸻

22. CONDITIONAL Output

When qualification returns CONDITIONAL:

proposal_generation: allowed_with_conditions

The system MAY produce a draft if doing so does not require unsupported claims.

The draft MUST clearly expose each unresolved condition.

The system MUST NOT present a conditional fact as established fact.

⸻

23. APPLY Output

When qualification returns APPLY:

proposal_generation: allowed

The system MAY generate:

* submission-ready proposal;
* screening answers;
* work-sample recommendations.

All factual claims remain bounded by canonical evidence.

⸻

24. Runtime Artifact

The qualification result SHALL be persisted as runtime context.

Default path:

out/<target-slug>/runtime/upwork-qualification.yaml

It should contain, conceptually:

version:
target:
decision:
proposal_generation:
confidence:
client_buying_signals:
hard_requirements:
  - requirement:
    status:
    relationship:
    evidence_strength:
    production_status:
    evidence:
    rationale:
preferred_requirements:
  - requirement:
    relationship:
    evidence_strength:
    evidence:
strongest_evidence_matches:
proposal_risks:
missing_evidence:
open_conditions:
recommended_work_samples:
rationale:

The coding agent MUST inspect existing contracts before introducing a new schema.

If an existing schema can be extended cleanly, it SHOULD be extended rather than duplicated.

⸻

25. Output Artifacts

For permitted proposal generation:

out/<target-slug>/upwork-proposal.md
out/<target-slug>/upwork-screening-answers.md
out/<target-slug>/upwork-work-samples.md

For DO NOT APPLY, the proposal artifact MUST NOT be represented as submission-ready output.

The implementation SHOULD follow existing output lifecycle and overwrite/idempotency conventions.

⸻

26. Orchestration

The feature SHOULD integrate with:

* existing target-opportunity mechanism;
* Runtime Layer;
* playbook-orchestrator;
* projection-registry;
* projection-validator.

Conceptually:

target_type: upwork
        │
        ▼
playbook-orchestrator
        │
        ▼
opportunity-analyzer
        │
        ▼
upwork qualification
        │
        ▼
qualification artifact
        │
        ▼
projection-registry
        │
        ▼
upwork proposal projection

The exact integration mechanism MUST be determined through repository discovery.

The implementation MUST NOT assume that a new Skill is required if an existing component can cleanly support the responsibility.

⸻

27. Skill Boundaries

The conceptual separation is:

Runtime qualification capability

opportunity
    +
canonical evidence
    ↓
qualification

It owns the qualification decision and runtime artifact.

It MUST NOT generate the final proposal.

Projection capability

qualified opportunity
    +
approved evidence boundary
    ↓
proposal package

It owns client-facing proposal projection.

It MUST consume qualification state and MUST NOT override it.

Whether these responsibilities require exactly two new Skills MUST be determined by repository discovery.

⸻

28. Repository Discovery Before Implementation

Before changing implementation files, the coding agent MUST inspect:

* current directory structure;
* Skill conventions;
* Runtime Layer Skills;
* Projection Layer Skills;
* opportunity-analyzer;
* projection-registry;
* playbook-orchestrator;
* projection-validator;
* OKF structures;
* evidence-card mechanisms;
* target opportunity configuration;
* output conventions;
* test conventions;
* logging/validation conventions;
* architecture documentation;
* existing CAS/SLDC guidance.

The agent MUST determine:

What existing components can be extended, composed or reused instead of duplicated?

Implementation details MUST follow repository evidence rather than assumptions in this requirements document.

⸻

29. No Implementation Prescriptions Without Evidence

The requirements MUST NOT prescribe:

* Python data structures;
* YAML parser implementation;
* Jinja templates;
* specific helper functions;
* exact source-code files;
* exact Skill implementation mechanism;
* additional frameworks;
* additional dependencies;

unless repository discovery demonstrates that they are consistent with the existing architecture.

The coding agent is responsible for determining the smallest coherent implementation consistent with the repository.

⸻

30. CAS Compliance

The implementation MUST follow established CAS principles.

Explicit scoped input

The target opportunity must be an explicit workflow input.

Bounded evidence

Only relevant canonical evidence should be loaded.

Governed processing

The system must use controlled evidence selection rather than unrestricted historical ingestion.

Traceability

Generated decisions and claims must have an explainable evidence basis.

Incremental evolution

The feature should introduce the smallest coherent change needed to establish the capability.

⸻

31. SLDC Compliance

The implementation MUST follow the repository’s established SLDC process.

The coding agent should:

1. inspect the repository;
2. confirm architectural placement;
3. identify required changes;
4. establish/update ADRs where justified;
5. implement the smallest coherent increment;
6. add tests;
7. execute validation;
8. inspect generated artifacts;
9. update relevant documentation;
10. report implementation evidence;
11. prepare the change for integration.

The feature must not bypass existing lifecycle or governance mechanisms because it is primarily a content-generation capability.

⸻

32. ADR Requirement

An ADR SHOULD be added only if repository discovery determines that the architectural decision is new.

The principal architectural decision to capture, if not already covered, is:

Upwork proposals are governed projections over canonical career evidence and target-opportunity context, with qualification as an explicit Runtime Layer gate.

Do not create duplicate ADRs where an existing decision already covers this.

⸻

33. Validation Architecture

Existing projection-validator SHOULD be extended rather than replaced or duplicated.

Validation should cover at least:

Qualification

* hard requirement handling;
* production status;
* evidence relationship;
* decision correctness;
* conditional state.

Evidence integrity

* unsupported claims;
* fabricated metrics;
* production-status inflation;
* personal-project substitution;
* technology equivalence errors;
* missing evidence.

Proposal

* qualification gate compliance;
* factual claim traceability;
* client constraint compliance;
* proposal structure;
* word-count target where applicable.

Screening

* question coverage;
* evidence integrity;
* open-condition handling.

Work samples

* evidence origin;
* requirement relevance;
* external-usage suitability.

⸻

34. Provenance Validation

The validator SHOULD validate provenance from internal structured data or an established repository mechanism.

It MUST NOT require client-facing prose to contain provenance syntax merely to satisfy the validator.

The quality gate is:

Generated Claim
      ↓
Canonical Evidence
      ↓
Valid relationship
      ↓
Valid production status
      ↓
Allowed projection

not:

Generated Claim
      ↓
Visible metadata tags

⸻

35. Test Scenarios

V1 MUST include at least three qualification paths.

Scenario A — APPLY

Authoritative evidence explicitly establishes:

real company
+
personally implemented
+
production
+
requested capability

Expected:

decision: APPLY
proposal_generation: allowed

⸻

Scenario B — CONDITIONAL

Evidence is potentially sufficient but one material fact remains unresolved.

Expected:

decision: CONDITIONAL
proposal_generation: allowed_with_conditions

and the unresolved fact is explicit.

⸻

Scenario C — DO NOT APPLY

The client explicitly requires production implementation.

Available evidence establishes only non-production/prototype/personal/innovation experience.

Expected:

decision: DO NOT APPLY
proposal_generation: blocked

This scenario is mandatory because it tests the central integrity rule.

⸻

36. Test Integrity

Tests MUST cover decision semantics and evidence-integrity boundaries.

“Complete test coverage” means that the critical behavioural paths are covered, particularly:

* APPLY;
* CONDITIONAL;
* DO NOT APPLY;
* unsupported claims;
* production-status distinction;
* qualification gate enforcement;
* screening-answer conditions;
* work-sample evidence.

It does not require an arbitrary literal percentage of source-code coverage unless that is already a repository standard.

⸻

37. Determinism and Idempotency

The workflow SHOULD respect existing repository conventions for deterministic execution and output regeneration.

Given:

same opportunity
+
same canonical evidence
+
same configuration

repeated execution SHOULD regenerate equivalent outputs and SHOULD NOT create uncontrolled accumulation of derived artifacts.

The implementation must follow existing idempotency conventions rather than inventing a separate mechanism.

⸻

38. Non-Goals

V1 explicitly excludes:

* Upwork scraping;
* opportunity discovery;
* browser automation;
* automated proposal submission;
* Upwork messaging;
* Connects purchasing;
* proposal boosting;
* autonomous application decisions without qualification;
* independent career evidence storage;
* automatic conversion of prototypes into production claims;
* marketplace analytics;
* automated proposal experimentation;
* autonomous marketplace interaction.

The workflow ends at:

Generated Package
      ↓
Human Review
      ↓
Human Submission

⸻

39. Future Compatibility

The architecture SHOULD leave room for later capabilities such as:

Opportunity Discovery
       ↓
Qualification
       ↓
Proposal
       ↓
Submission
       ↓
Outcome
       ↓
Learning
       ↓
Improved Qualification / Projection

V1 must not implement those later stages.

⸻

40. Definition of Done

The feature is complete only when:

Repository discovery
        ↓
Architectural alignment
        ↓
Requirements mapped to existing components
        ↓
Qualification implemented
        ↓
Qualification gate validated
        ↓
Evidence integrity validated
        ↓
Proposal projection implemented
        ↓
Screening projection implemented
        ↓
Work-sample projection implemented
        ↓
Registry/orchestrator integration validated
        ↓
Projection validation extended
        ↓
CAS compliance verified
        ↓
SLDC compliance verified
        ↓
Human-review boundary verified
        ↓
Generated artifacts inspected
        ↓
Implementation evidence reported

The feature must demonstrate that the system can refuse to generate a persuasive application when the evidence does not support the client’s requirements.

⸻

41. Final Design Principle

The purpose of the capability is not:

Generate as many Upwork proposals as possible.

It is:

Identify the opportunities that can be pursued credibly, then generate the strongest evidence-grounded projection for those opportunities.

That principle should govern both the qualification logic and the proposal-generation design.

⸻
