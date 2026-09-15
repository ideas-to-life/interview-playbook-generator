# Upwork Proposal Generator — V3.1 Requirements Refinement Input
## Evidence Attribution, Composition & Claim Projection Integrity

Refine the existing V3 specification for the Upwork Proposal Generator.

This is a requirements refinement, not an implementation specification.

Preserve the existing V2.0/V2.1 architectural and behavioural constraints unless explicitly superseded below.

The primary objective is to correct the remaining attribution/projection defects by ensuring that evidence attribution is established before qualification and proposal projection, rather than asking the final validator to infer truth from generated prose.

---

## 1. Architectural intent

The pipeline MUST preserve the following conceptual flow:

Canonical Evidence
    ↓
Evidence Attribution / Interpretation
    ↓
Qualification
    ↓
Attributed Claims / Projection Context
    ↓
Proposal / Screening / Work Samples
    ↓
Validation & Quality Gate
    ↓
Human Review
    ↓
Human Decision / Submission

Attribution integrity is an upstream concern.

The validator MUST NOT be the primary mechanism for determining whether a historical claim is true. It validates that generated projections remain consistent with structured, evidence-grounded attribution established earlier in the pipeline.

Validation remains cross-cutting and MUST NOT become a fifth architectural layer.

The existing four-layer architecture remains:

- Knowledge
- Runtime
- Coaching
- Projection

---

# 2. Evidence attribution model

## FR-031 — Independent Attribution Dimensions

The system MUST represent candidate contribution, system/platform production status, implementation status, deployment status, and temporal scope as independently assessable dimensions.

The system MUST NOT treat contribution as a universal linear responsibility ladder such as:

advised → designed → implemented → deployed → production

These dimensions are related but not necessarily hierarchical.

For example:

- a candidate may architect a system without implementing it;
- a candidate may implement a prototype without deploying it;
- a candidate may lead implementation performed by a team without personally implementing the system;
- an organisation may deploy a platform without evidence that the candidate personally implemented or deployed it;
- a candidate may operate a production system without having originally designed it.

The qualification model MUST therefore preserve these dimensions independently.

At minimum, production-sensitive assessment MUST distinguish:

- subject
- candidate contribution
- system/platform production status
- candidate implementation status
- candidate production deployment status
- evidence strength
- temporal scope

The implementation MAY use existing schemas, runtime structures, or lightweight intermediate structures. This requirement does not prescribe a new persistent schema.

---

## FR-032 — Subject Preservation

Every historical claim MUST preserve its subject.

Supported subjects include:

- Candidate
- Organisation
- Platform/System
- Project/Team
- Proposed Future Solution

Evidence about one subject MUST NOT be silently transferred to another subject.

Examples of prohibited transformations:

- "WPP Open was a production platform"
  → "I implemented WPP Open in production"

- "The team implemented the system"
  → "I implemented the system"

- "The organisation deployed the platform"
  → "I deployed the platform"

- "The proposed architecture uses LangGraph"
  → "I previously deployed LangGraph"

---

## FR-033 — Candidate Contribution Boundaries

Candidate contribution MUST be represented independently from system/platform status.

Supported contribution descriptions MAY include:

- advised
- assessed
- recommended
- aligned
- shaped architecture
- architected
- designed
- led
- implemented
- deployed
- operated

The system MUST select only contribution descriptions supported by candidate-specific evidence.

A stronger contribution claim MUST NOT be inferred merely because:

- the platform was production;
- the candidate worked for the organisation;
- the candidate held a senior title;
- the candidate led a project;
- the candidate interacted with the platform;
- another team implemented the system;
- the candidate implemented a related personal or prototype system.

---

## FR-034 — No Responsibility-Ladder Inference

The system MUST NOT infer:

implemented from architected;
deployed from implemented;
production deployment from deployment;
candidate implementation from organisation/platform production;
personal implementation from team implementation.

Where evidence establishes only architecture/advisory responsibility, generated historical claims MUST remain bounded to that responsibility.

---

## FR-035 — Production Status Separation

The system MUST independently track:

- system/platform production status;
- candidate implementation status;
- candidate production deployment status.

`system_production_status = verified_production`

MUST NOT imply:

`candidate_production_deployment_status = verified_production`

Likewise, employment by an organisation operating a production platform MUST NOT establish that the candidate personally implemented that production platform.

---

# 3. Attribution-aware intermediate representation

## FR-036 — Attributed Historical Claims

Before client-facing projection, historical claims MUST be represented in an attribution-aware intermediate form or equivalent runtime structure.

Each historical claim MUST retain, where applicable:

- claim identifier
- subject
- organisation
- project/system/platform
- candidate contribution
- system/platform production status
- candidate implementation status
- candidate production deployment status
- temporal scope
- evidence strength
- evidence card identifiers
- source document identifiers
- claim type: historical or proposed

The implementation MAY determine the exact schema and persistence location during planning.

The requirement is that attribution information exists BEFORE prose projection and is not reconstructed solely from the final prose.

---

## FR-037 — Provenance Preservation

Every generated historical claim in qualification artifacts and client-facing artifacts MUST remain traceable to canonical evidence through the attribution-aware representation.

Minimum provenance MUST identify:

- the supporting evidence;
- the subject of the evidence;
- the organisation/project/system context;
- candidate contribution;
- production status where relevant;
- temporal scope;
- whether the claim is historical or proposed.

Provenance MUST NOT be reconstructed only after prose generation.

---

## FR-038 — Claim Derivation Boundary

Client-facing historical claims MUST be derived from attribution-aware structured claims or equivalent governed projection context.

The proposal generator MUST NOT independently synthesize historical claims by freely combining raw evidence cards.

The projection layer MAY compose multiple individually supported claims into a broader capability statement, but each underlying historical fact MUST retain its original attribution and context.

---

# 4. Cross-source composition

## FR-039 — Capability Composition Without Historical Fabrication

Evidence from multiple contexts MAY be combined to demonstrate complementary capabilities.

For example:

- WPP Media → enterprise agentic-AI architecture;
- BBC Studios → enterprise AI governance;
- CAS → hands-on AI implementation.

The system MAY generate a capability-level statement such as:

"My experience combines enterprise agentic-AI architecture, enterprise AI governance, and hands-on implementation through independent AI systems work."

However, it MUST NOT merge those contexts into a new historical fact unsupported by any individual context.

For example, the following MUST NOT be generated without explicit evidence:

"I implemented a production multi-agent platform at WPP using the architecture I developed in CAS."

---

## FR-040 — Single-Fact Requirement Boundary

When evaluating a requirement that asks for a specific historical fact, the evidence supporting that fact MUST come from a context that independently establishes the required attributes.

Evidence aggregation MUST NOT satisfy a single historical production requirement by combining:

- organisation A production status;
- organisation B architecture experience;
- personal project implementation;
- theoretical knowledge.

This is particularly important for requirements such as:

"Personally designed and implemented an AI system inside a real operating company in production."

---

## FR-041 — Composition Boundary Classification

The system SHOULD distinguish at least:

- same-context evidence;
- complementary multi-context evidence;
- unsupported composite evidence.

Complementary multi-context evidence is valid for capability presentation.

Unsupported composite evidence MUST NOT be used to establish a historical qualification fact.

The implementation MAY determine the exact representation of this classification.

---

# 5. Historical versus proposed architecture

## FR-042 — Temporal / Intent Separation

Historical experience and proposed future architecture MUST remain explicitly distinct.

Historical claims MUST describe what the candidate actually did.

Proposed architecture MUST describe what the candidate recommends, would implement, or proposes for the client's environment.

Technology appearing only in:

- the job description;
- proposed architecture;
- candidate recommendation;
- future implementation approach

MUST NOT be represented as historical experience.

---

## FR-043 — Proposed Technology Boundary

A proposed technology such as LangGraph, Temporal, Redis, Supabase, Salesforce APIs, Shopify APIs, MCP, or OpenAI Agents SDK MAY be used in a proposed solution.

Its presence in the proposed solution MUST NOT establish historical experience with that technology.

Historical usage requires independent canonical evidence.

---

# 6. Qualification and content safety

## FR-044 — Independent State Axes

The system MUST maintain three distinct concepts.

### Requirement qualification

- SUPPORTED
- PARTIALLY_SUPPORTED
- UNKNOWN
- CONTRADICTED

### Content generation safety

- EVIDENCE_BACKED
- EVIDENCE_SAFE_BOUNDED
- HUMAN_REVIEW_REQUIRED

### Human decision

- APPLY
- DO_NOT_APPLY
- HOLD_FOR_EVIDENCE

These states MUST NOT be conflated.

In particular:

`EVIDENCE_SAFE_BOUNDED`

does not mean:

`SUPPORTED`

and:

`HUMAN_REVIEW_REQUIRED`

does not mean:

`DO_NOT_APPLY`.

The human remains the ultimate decision-maker.

---

## FR-045 — Evidence Gap Utility

Evidence gaps MUST NOT automatically suppress proposal generation.

Where a hard requirement is unresolved, the system MAY still generate:

- evidence-safe adjacent positioning;
- supported capability statements;
- proposed architecture;
- relevant work samples;
- precise candidate confirmation questions.

The system MUST NOT generate unsupported affirmative claims merely to make the proposal appear stronger.

---

## FR-046 — Opening Positioning

When a material production requirement remains unresolved, the proposal opening MUST position the candidate around verified adjacent strengths.

It MUST NOT imply that the unresolved requirement has been satisfied.

---

# 7. Screening answers

## FR-047 — Screening Fidelity

Screening answers MUST be derived from the same attribution-aware qualification context as the proposal.

If a historical fact is `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED`, the screening answer MUST NOT assert that fact affirmatively.

The answer MAY provide bounded context and explicitly surface the unresolved fact for human confirmation.

---

## FR-048 — Precision Confirmation

Confirmation questions MUST target the missing candidate-specific fact.

For example:

"Did you personally implement and deploy the WPP system into live production?"

is appropriate.

"Was WPP Open deployed?"

is insufficient when the unresolved fact concerns the candidate's personal implementation.

---

## FR-049 — No Assertion-Then-Disclaimer Pattern

The system MUST NOT generate:

1. an affirmative historical claim; followed by
2. a disclaimer that the claim is actually unverified.

The claim itself MUST be bounded.

For example, this pattern is prohibited:

"I architected the production multi-agent platform at WPP. Live production implementation is unverified."

A bounded formulation is required instead:

"I led architecture work around an enterprise agentic-AI platform at WPP; canonical evidence does not establish that I personally implemented or deployed the platform into live production."

---

# 8. Work samples

## FR-050 — Work Sample Attribution

Every work sample MUST preserve:

- project identity;
- project type;
- candidate contribution;
- production status;
- demonstrated capability.

A personal project, prototype, innovation initiative, laboratory, PoC, or incomplete implementation MUST NOT be described as a production deployment.

---

## FR-051 — Work Sample Capability Separation

A work sample MAY demonstrate relevant technical capability without satisfying a production requirement.

For example, a personal multi-agent implementation MAY demonstrate hands-on engineering capability while remaining insufficient evidence for:

"Personally implemented a production multi-agent system inside an operating company."

The generator MUST preserve that distinction.

---

# 9. Validation responsibilities

## FR-052 — Validation as Projection Integrity Check

`upwork-validator` MUST validate generated artifacts against the structured qualification and attribution context.

It SHOULD NOT be the sole source of semantic truth.

Validation MUST check whether projection has introduced unsupported changes such as:

- platform → candidate;
- organisation → candidate;
- team → candidate;
- architecture → implementation;
- prototype → production;
- proposed → historical;
- one context → another context.

---

## FR-053 — Attribution Shift Validation

The validator MUST detect defined attribution-shift regression patterns in generated artifacts.

The validator MAY use deterministic rules, structured claim comparison, controlled lexical checks, or other mechanisms appropriate to the repository architecture.

The requirements MUST NOT prescribe a regex-only semantic implementation.

---

## FR-054 — Production Claim Validation

Any client-facing assertion that the candidate personally implemented or deployed a production system MUST require candidate-specific production evidence.

Verified production status of the underlying platform or organisation is insufficient.

---

## FR-055 — Evidence Composition Validation

The validator MUST detect unsupported historical composites where separate evidence contexts are used to establish a single requirement-specific historical fact that no context independently supports.

It MUST continue to allow valid capability-level composition across contexts.

---

## FR-056 — Screening / Qualification Consistency

The validator MUST fail a package where a screening answer makes an affirmative historical assertion that conflicts with the corresponding qualification status.

For a requirement classified as:

- PARTIALLY_SUPPORTED
- UNKNOWN
- CONTRADICTED

the validator MUST flag affirmative claims asserting the unresolved fact as established.

---

## FR-057 — Work Sample Consistency

The validator MUST verify consistency between:

- project type;
- production status;
- candidate contribution;
- demonstrated capability;
- generated work sample narrative.

Prototype/personal/incomplete work MUST NOT be presented as verified production deployment.

---

# 10. Golden regression scenario

## FR-058 — WPP + CAS Attribution Regression

The implementation MUST include a deterministic regression scenario representing the following evidence state:

### WPP context

- WPP Open is an existing enterprise production platform.
- Candidate worked in WPP Media Prototype & Innovation.
- Candidate contributed architecture leadership, alignment, assessment, and recommendations around agentic-AI initiatives/platform evolution.
- Candidate's personal implementation of the underlying production platform is NOT established.
- Candidate's personal production deployment of that platform is NOT established.

### CAS context

- Candidate personally implemented AI/agentic systems in the candidate's own architecture laboratory.
- CAS is a personal project and is not evidence of enterprise production deployment.

### Target requirement

"Must have personally designed and implemented AI systems inside a real operating company in production."

The system MUST NOT generate any equivalent of:

- "I architected WPP Open."
- "I implemented WPP Open."
- "I deployed the WPP multi-agent platform."
- "I built a production multi-agent platform at WPP."
- "I personally implemented WPP's production agentic platform."

The system SHOULD be capable of generating bounded statements distinguishing:

- WPP enterprise architecture/advisory experience;
- BBC governance experience where relevant;
- CAS hands-on implementation experience;
- unresolved evidence regarding personal production implementation inside an operating company.

This scenario MUST be included as a regression test for qualification, proposal projection, screening answers, work samples, and validation.

---

# 11. Incomplete implementation regression

## FR-059 — Project In Progress at Departure

Where canonical evidence establishes that the candidate led or architected an enterprise project that was still being implemented when the candidate departed:

The system MAY claim:

- project leadership;
- architecture leadership;
- design;
- implementation leadership/management where explicitly supported;
- architectural decisions;
- work performed before departure.

The system MUST NOT infer:

- successful production deployment;
- live operational status;
- post-departure implementation completion;
- candidate personal production deployment.

---

# 12. Human decision sovereignty

## FR-060 — Human Decision Preservation

Machine recommendation, qualification state, evidence gaps, or validation findings MUST NOT silently overwrite human decision state.

The machine MAY recommend:

- STRONG_FIT
- POTENTIAL_FIT
- EVIDENCE_GAPS
- WEAK_FIT
- CLEAR_MISMATCH

but human decision remains:

- APPLY
- DO_NOT_APPLY
- HOLD_FOR_EVIDENCE

`HUMAN_REVIEW_REQUIRED` indicates that the machine cannot certify submission readiness. It MUST NOT prevent a human from choosing APPLY after review.

---

# 13. Requirements on implementation freedom

## FR-061 — No Premature Schema Prescription

The requirements MUST describe required information, invariants, and behaviour rather than prematurely prescribing new persistent schemas.

In particular, the specification SHOULD NOT require a global `CandidateContributionProfile` unless repository discovery during planning demonstrates that such an entity is necessary.

The implementation plan MUST inspect existing:

- OKF EvidenceCards;
- qualification runtime structures;
- projection context;
- claim/provenance structures;
- validator structures;

before introducing new persistent schemas.

---

# 14. Regression compatibility

## FR-062 — Preserve Existing V2.0/V2.1 Constraints

The refinement MUST preserve existing validated behaviour including:

- four-layer architecture: Knowledge, Runtime, Coaching, Projection;
- Validation as cross-cutting quality gate;
- OKF v0.2 graph structure;
- bounded/scoped evidence retrieval;
- no unrestricted historical scans;
- deterministic/idempotent generation;
- qualification states and human decision sovereignty;
- proposal utility under evidence gaps;
- maximum three work samples;
- no fabricated metrics, clients, employers, projects, production status, agent counts, responsibilities, ownership, scope, or outcomes;
- no Upwork scraping;
- no browser automation;
- no automated Upwork submission.

---

# 15. Success criteria

Replace absolute claims of universal semantic prevention with testable acceptance criteria.

## SC-031 — Attribution Regression Coverage

100% of defined attribution regression scenarios MUST either:

- generate correctly bounded output; or
- fail validation.

No defined regression scenario may silently generate an unsupported candidate-attribution shift.

## SC-032 — Production Attribution Integrity

100% of defined production-sensitive regression scenarios MUST prevent system/platform production status from being transformed into candidate personal production implementation.

## SC-033 — Cross-Context Integrity

100% of defined cross-source regression scenarios MUST prevent unsupported historical composites while permitting valid capability-level composition.

## SC-034 — Screening Consistency

100% of defined screening regression scenarios MUST prevent affirmative historical answers where the corresponding requirement fact is PARTIALLY_SUPPORTED, UNKNOWN, or CONTRADICTED.

## SC-035 — Historical / Proposed Separation

100% of defined historical-vs-proposed regression scenarios MUST prevent proposed technologies or approaches from being represented as historical experience without canonical evidence.

## SC-036 — Evidence-Gap Utility

Opportunities with unresolved evidence MUST remain capable of generating evidence-safe, actionable proposal artifacts unless an existing explicit rule otherwise prevents generation.

## SC-037 — V2.0/V2.1 Regression Compliance

The complete existing V2.0/V2.1 regression suite MUST continue to pass.

---

# 16. Implementation guidance for /speckit-plan

The resulting formal specification MUST leave implementation decisions open where repository discovery is required.

During planning, inspect the existing architecture and determine the smallest coherent implementation boundary.

In particular, determine whether attribution-aware claims should be represented using:

- existing OKF EvidenceCards;
- qualification runtime structures;
- projection context;
- a lightweight claim/provenance representation;
- or a new schema.

Do not create a new global canonical model merely because the requirements mention attribution.

Prefer extending existing governed structures where they can express the required semantics without ambiguity.

The implementation SHOULD follow the existing CAS/SLDC discipline:

1. inspect current architecture and conventions;
2. identify the correct architectural placement;
3. define the smallest coherent change;
4. add/update ADRs only where architectural decisions warrant them;
5. implement deterministic/idempotent behaviour;
6. add focused regression tests first around the attribution failure;
7. validate generated artifacts;
8. inspect outputs;
9. verify V2.0/V2.1 regression compatibility;
10. document implementation evidence.

---

# 17. Critical design principle

The central invariant of this refinement is:

Evidence establishes facts.
Attribution establishes who did what, where, and when.
Qualification determines whether those facts satisfy a requirement.
Projection expresses those qualified facts to the client.
Validation verifies that projection did not alter their meaning.
Human review remains the final decision authority.

No downstream stage may manufacture information that was not established upstream.
