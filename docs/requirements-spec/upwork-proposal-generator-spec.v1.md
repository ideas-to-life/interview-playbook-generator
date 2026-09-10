Requirements Specification

Upwork Proposal Generation — V1

Feature: Upwork opportunity qualification and proposal generation
Repository: ideas-to-life/interview-playbook-generator
Status: Proposed
Version: V1 / Minimum Viable Capability
Implementation owner: Coding agent
Governance: Existing CAS + SLDC workflow
Primary objective: Add Upwork proposal generation as a governed projection of the existing Career Knowledge / OKF evidence, with explicit qualification gates and human approval.

## Clarifications

### Session 2026-09-10
- Q: Should Upwork qualification and proposal generation be integrated into the standard pipeline orchestrator as runtime and projection skills, or invoked as a standalone skill? → A: Option A - Register a runtime qualification skill (`upwork-qualification`) in the Runtime Layer and add `upwork-proposal` to `projection-registry` so it runs automatically via `playbook-orchestrator` when `target_type: upwork`.
- Q: How should screening answers be generated when the qualification gate returns a CONDITIONAL decision? → A: Option A - Generate screening answers with explicit `[OPEN CONDITION: <fact>]` markers for any response dependent on unverified information.
- Q: Should the qualification gate output be stored as machine-readable YAML in runtime context while proposal outputs are generated as Markdown documents? → A: Option A - Machine-readable YAML at `out/<target-slug>/runtime/upwork-qualification.yaml` and Markdown files (`upwork-qualification-report.md`, `upwork-screening-answers.md`, `upwork-work-samples.md`) in `out/<target-slug>/`.
- Q: Should the existing projection-validator skill be extended to evaluate Upwork proposals and screening answers as part of the standard evaluation layer? → A: Option A - Extend existing `projection-validator` to parse and validate Upwork proposal artifacts and record validation results in `out/<target-slug>/runtime/projection-validation-report.yaml`.

⸻

1. Purpose

Extend the Interview Playbook Generator so that an Upwork opportunity can be processed through a governed workflow:

Upwork Job Description
        │
        ▼
Opportunity Analysis
        │
        ▼
Qualification Gate
        │
        ├── DO NOT APPLY ──► Stop
        │
        ├── CONDITIONAL ───► Candidate confirmation
        │
        └── APPLY
              │
              ▼
       Evidence Mapping
              │
              ▼
       Proposal Strategy
              │
              ▼
       Proposal Package
              │
              ▼
         Human Review

The feature must reuse the repository’s existing career evidence and projection architecture rather than creating a separate career knowledge base.

The generated proposal is an output projection of governed career evidence, not a new source of truth.

⸻

2. Problem Statement

The current system is primarily oriented toward traditional employment opportunities and interview-playbook generation.

Upwork proposals introduce several additional requirements:

* proposals are significantly shorter and more commercially focused;
* clients frequently provide explicit screening questions;
* clients may define hard disqualifying requirements;
* evidence must be mapped directly to the client’s requirements;
* work samples should be selected deliberately;
* proposal generation must distinguish between demonstrated experience and transferable capability;
* unsupported claims are particularly damaging in a marketplace context;
* some opportunities should result in DO NOT APPLY, rather than a persuasive proposal.

The system therefore needs a qualification stage before proposal generation.

⸻

3. Goals

V1 shall:

1. Accept an Upwork opportunity as a target opportunity.
2. Analyse the opportunity using the existing opportunity-analysis capability.
3. Identify explicit hard requirements and disqualifiers.
4. Compare those requirements against canonical career evidence.
5. Produce an explicit qualification decision:
    * APPLY
    * CONDITIONAL
    * DO NOT APPLY
6. Identify the strongest evidence matches.
7. Identify material evidence gaps.
8. Generate a concise proposal when appropriate.
9. Generate answers to Upwork screening questions.
10. Recommend appropriate work samples.
11. Preserve evidence integrity throughout the process.
12. Integrate with the existing CAS/SLDC lifecycle.
13. Stop at human review rather than automating Upwork submission.

⸻

4. Non-Goals

V1 shall not:

* scrape Upwork;
* automatically search Upwork;
* automatically submit proposals;
* automate browser interaction with Upwork;
* send Upwork messages;
* automatically purchase Connects;
* automatically boost proposals;
* create or maintain an independent career evidence database;
* infer employment history from arbitrary web content;
* invent metrics;
* infer production experience from prototypes;
* convert personal projects into client-production experience;
* automatically decide to apply without the qualification gate;
* replace the existing OKF evidence model.

The system ends at a human-reviewable application package.

⸻

5. Architectural Principle

The new feature shall follow this principle:

Upwork proposal generation is a projection over governed career evidence and target-opportunity context.

The architecture should therefore reuse:

Canonical Career Evidence
        +
Target Opportunity
        +
Opportunity Analysis
        ↓
Upwork-specific projection

It must not create a parallel representation of the user’s career history.

⸻

6. Repository Discovery Requirement

Before making implementation changes, the coding agent MUST inspect the repository.

It shall identify:

* existing directory structure;
* configuration conventions;
* Skill conventions;
* existing Runtime Layer Skills;
* existing Projection Skills;
* opportunity-analysis implementation;
* OKF structures;
* evidence-card structures;
* target-position conventions;
* output conventions;
* logging conventions;
* validation/test conventions;
* CAS-related conventions;
* SLDC workflow conventions.

The coding agent must adapt to existing conventions rather than introducing competing patterns.

No implementation should begin until this discovery step is complete.

The agent should explicitly identify:

Which existing component should be extended, reused, or composed rather than duplicated?

⸻

7. V1 Capability Model

The feature should consist conceptually of four stages.

Stage A — Opportunity qualification

Determine whether the opportunity is compatible with the available evidence.

Stage B — Evidence mapping

Map requirements and buying signals to authoritative evidence.

Stage C — Proposal strategy

Determine:

* positioning;
* evidence hierarchy;
* relevant examples;
* work samples;
* questions;
* risks;
* messaging emphasis.

Stage D — Proposal projection

Generate:

* proposal;
* screening answers;
* work-sample recommendations.

These stages may be implemented as separate Skills or as extensions to existing Skills, depending on repository conventions.

⸻

8. Qualification Gate

The qualification gate is the most important new capability.

The system shall classify requirements using:

direct
adjacent
transferable
absent

And evidence strength using:

strong
moderate
weak

Where relevant, production status shall distinguish:

verified_production
verified_non_production
unknown
not_applicable

⸻

9. Qualification Decisions

9.1 APPLY

APPLY may only be returned when:

* all explicit hard requirements are adequately supported;
* there is no material evidence-integrity concern;
* no required claim would need to be fabricated or materially overstated.

9.2 CONDITIONAL

CONDITIONAL shall be used when:

* the opportunity may fit;
* one or more material facts are unresolved;
* the missing information could reasonably be supplied or confirmed by the candidate.

The system must state exactly what needs confirmation.

9.3 DO NOT APPLY

DO NOT APPLY shall be returned when:

* a hard requirement is clearly absent;
* available evidence contradicts the requirement;
* satisfying the requirement would require fabrication;
* the client explicitly excludes the type of experience represented by the available evidence.

The system must stop proposal generation.

⸻

10. Hard Evidence-Integrity Rules

These rules are mandatory.

The system must never fabricate or infer:

* clients;
* projects;
* employers;
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

Production experience

The system must never treat:

* a personal project;
* a prototype;
* an architecture exercise;
* a demonstration;
* a laboratory;
* a proof of concept;
* theoretical knowledge;
* prototype-and-innovation work without verified production evidence

as equivalent to production implementation.

If an Upwork client explicitly states:

“You must have personally implemented this in production for a real company.”

then only authoritative evidence explicitly establishing that condition may satisfy the requirement.

⸻

11. Evidence Relationship Model

The system shall preserve the distinction between:

Direct

The evidence explicitly demonstrates the requested capability.

Adjacent

The evidence demonstrates a closely related capability but not the exact requested capability.

Transferable

The evidence demonstrates underlying architectural or engineering capability that could reasonably transfer to the requirement.

Absent

No credible evidence has been identified.

These distinctions must remain visible to the proposal-generation stage.

The generator must never silently convert:

adjacent → direct
transferable → direct
unknown → direct

⸻

12. Opportunity Inputs

The feature shall accept an opportunity containing at minimum:

title
description
client requirements
preferred capabilities
screening questions
target context

The existing target-opportunity mechanism should be reused where possible.

A target-specific configuration should contain the opportunity source and any metadata required by the existing pipeline.

The coding agent should determine the precise schema based on the repository’s current configuration model.

⸻

13. Opportunity Analysis

The feature should reuse the existing opportunity-analysis capability.

The Upwork-specific processing should consume its output rather than independently re-parsing the opportunity wherever possible.

The analysis should identify:

* client problem;
* desired outcome;
* hard requirements;
* preferred requirements;
* buying signals;
* technical requirements;
* screening questions;
* likely evaluation criteria;
* potential evidence gaps.

⸻

14. Evidence Retrieval

Evidence retrieval should prioritize authoritative, distilled OKF material.

Priority should generally be:

1. evidence cards;
2. signature achievements;
3. capability evidence;
4. story library;
5. executive identity;
6. messaging/projection material;
7. target-specific evidence.

The system should not perform an unrestricted historical scan when adequate canonical evidence already exists.

This follows the established scoped-ingestion principle:

bounded, relevant, incremental and governed input selection.

⸻

15. Evidence Mapping

For each significant requirement, the qualification stage should produce a mapping conceptually equivalent to:

requirement:
status:
relationship:
evidence_strength:
production_status:
evidence:
rationale:

Example:

requirement: "Production multi-agent implementation for a real company"
status: "not_met"
relationship: "absent"
evidence_strength: "weak"
production_status: "verified_non_production"
evidence:
  - "WPP Media agentic AI architecture work"
rationale: >
  Evidence establishes agentic AI architecture and governance work
  in Prototype & Innovation, but does not establish production
  multi-agent implementation.

The exact schema may differ if an existing repository contract already covers this concept.

⸻

16. Proposal Strategy

For qualified opportunities, the system shall determine:

Client priorities

Identify the 2–3 strongest buying signals.

Candidate evidence

Identify the 2–3 strongest direct evidence matches.

Evidence risks

Identify claims that must be avoided or carefully qualified.

Positioning

Determine how the candidate should be positioned for the particular opportunity.

For this project, the preferred positioning is generally:

Enterprise Architect & AI Transformation Advisor who can connect business problems, architecture, governance and hands-on implementation.

However, the system should not hard-code this wording if existing identity/messaging mechanisms already provide it.

⸻

17. Proposal Structure

Unless the client specifies another format, the proposal should follow:

1. Opening

The first 1–2 sentences should demonstrate understanding of the client’s problem.

Avoid:

“I’m excited to apply…”

2. Requirement-to-proof mapping

Present the strongest 2–4 matches between client requirements and evidence.

3. Project snapshots

Use no more than three.

Each should communicate:

context
→ what was done
→ operational/business relevance

Only use supported facts.

4. Approach

Explain how the candidate would approach the client’s problem.

Typical sequence:

process
→ systems/data
→ automation candidates
→ AI vs deterministic automation vs human
→ architecture
→ integration
→ controls
→ implementation
→ validation

5. Smart questions

Normally 3–5 questions.

Questions should demonstrate understanding rather than merely request information.

6. CTA

Invite a short discussion focused on a concrete problem/process.

⸻

18. Proposal Length

Default target:

350–500 words

The client-specific instructions take precedence.

If the platform or client imposes a hard character limit, the generator must respect it.

The generator should prioritize:

1. relevance;
2. evidence;
3. clarity;
4. concision.

⸻

19. Screening Questions

The system must generate a separate screening-answer artifact.

Every client question must be answered.

Rules:

* answer the question first;
* provide evidence second;
* do not evade difficult questions;
* explicitly acknowledge missing evidence;
* do not substitute personal projects for required production experience;
* do not manufacture numbers;
* under CONDITIONAL status, attach an explicit `[OPEN CONDITION: <fact>]` tag to any answer relying on unverified candidate context.

For an opportunity with an explicit hard production requirement that is not satisfied, screening answers should not be generated as if the candidate were applying.

⸻

20. Work Samples

The system should recommend up to three work samples.

Selection should be based on:

client requirement
        ↓
capability demonstrated
        ↓
available evidence
        ↓
strongest relevant artifact

Each recommendation should state:

sample
supports requirement
demonstrates capability
evidence source

Confidential internal material must not be recommended unless it is already approved for external use.

⸻

21. Output Model

V1 requires the following explicit output paths adhering to repository conventions:

Machine-readable qualification output:
`out/<target-slug>/runtime/upwork-qualification.yaml`

Human-readable Markdown proposal outputs:
`out/<target-slug>/upwork-qualification-report.md`
`out/<target-slug>/upwork-screening-answers.md`
`out/<target-slug>/upwork-work-samples.md`

⸻

22. Qualification Output Contract

Minimum conceptual schema:

version: "1.0"
target:
decision: "APPLY | CONDITIONAL | DO NOT APPLY"
confidence: "HIGH | MEDIUM | LOW"
client_buying_signals:
  - ...
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
  - ...
proposal_risks:
  - ...
missing_evidence:
  - ...
recommended_work_samples:
  - ...
rationale:

The coding agent must determine whether an existing repository contract should be extended rather than creating a duplicate schema.

⸻

23. DO NOT APPLY Behaviour

When qualification returns:

DO NOT APPLY

the proposal generator must not produce a submission-ready proposal.

It should instead produce a concise gate report containing:

Decision
Blocking requirement
Available evidence
Evidence gap
What would change the decision

This is a deliberate product behaviour, not an error condition.

⸻

24. CONDITIONAL Behaviour

When qualification returns:

CONDITIONAL

the generator may produce a draft only if doing so does not require unsupported factual claims.

The output must clearly identify:

OPEN CONDITION

and the exact fact requiring confirmation.

⸻

25. APPLY Behaviour

When qualification returns:

APPLY

the proposal generator may produce:

* submission-ready proposal;
* screening answers;
* work-sample recommendations.

All factual claims remain constrained by canonical evidence.

⸻

26. CAS Integration

The feature must follow the existing CAS principles.

In particular:

Explicit project-scoped input

The target opportunity should be an explicit scoped input to the workflow.

Governed processing

The workflow should use an explicit allowlist of relevant evidence rather than recursively ingesting the career repository.

Traceability

A generated claim should be traceable to its evidence source.

Conceptually:

Client Requirement
        ↓
Qualification Decision
        ↓
Evidence
        ↓
Proposal Claim

This should make it possible to answer:

“Why did the system say this?”

and:

“What evidence supports this statement?”

Continuous feedback

The proposal is not the end of the learning loop.

Future candidate feedback can eventually inform:

opportunity
→ qualification
→ proposal
→ outcome
→ learning
→ refined strategy

V1 does not need to automate this feedback loop, but its design should not prevent it.

⸻

27. SLDC Integration

The implementation must follow the repository’s existing Software Lifecycle Development conventions.

The coding agent should:

1. inspect existing development workflow;
2. create an appropriate feature branch;
3. establish/change architecture decisions where required;
4. implement the smallest coherent change;
5. add/update tests;
6. run validation;
7. inspect generated outputs;
8. document relevant decisions;
9. provide implementation evidence;
10. only then prepare the change for integration.

The feature must not bypass existing governance mechanisms merely because it is a content-generation feature.

⸻

28. ADR Requirement

The coding agent should determine whether the feature requires an ADR.

At minimum, an ADR should be considered for:

Upwork proposals as a governed projection over canonical career evidence rather than an independent evidence source.

If an existing architectural decision already establishes this projection strategy, reuse it rather than creating a duplicate ADR.

⸻

29. Skill Design

The implementation shall register a runtime qualification skill (`upwork-qualification`) in the Runtime Layer and add an Upwork projection skill (`upwork-proposal`) to `projection-registry` so that it is automatically executed via `playbook-orchestrator` when `target_type: upwork` is set.

Conceptually, two discrete responsibilities are enforced:

Qualification Skill (`upwork-qualification`)

Responsible for:

opportunity
→ requirements
→ evidence
→ qualification

It must produce the runtime qualification artifact and must not write the proposal.

Proposal Projection Skill (`upwork-proposal`)

Registered with `projection-registry`. Responsible for:

qualified opportunity
+
evidence
→ proposal package

It must consume the runtime qualification artifact and must not override qualification decisions.

If repository inspection shows these responsibilities can be cleanly incorporated into existing Skills without creating unnecessary fragmentation, the agent should prefer that design.

⸻

30. Separation of Concerns

The implementation must maintain this boundary:

Opportunity Analysis
        │
        ▼
Qualification
        │
        ▼
Proposal Strategy
        │
        ▼
Proposal Projection

Do not combine all four into a single large prompt/Skill.

The qualification result should be an explicit intermediate artifact.

This is important because qualification is a decision, whereas proposal generation is a projection.

⸻

31. Human-in-the-Loop Boundary

The V1 workflow ends here:

Generated proposal
        ↓
Human review
        ↓
Human submission

The system must not autonomously:

* submit;
* message;
* modify Upwork profile;
* purchase Connects;
* interact with the Upwork UI.

The human remains accountable for the final marketplace action.

⸻

32. Configuration

The coding agent shall inspect the existing target-position/configuration mechanism and extend it minimally.

A target opportunity should be able to declare:

opportunity source
target type = upwork

and any other metadata required by the existing pipeline.

Do not introduce a second configuration mechanism if the existing target-position mechanism can support this.

⸻

33. Validation Requirements

V1 must include automated and deterministic validation integrated into the existing Evaluation Layer (`projection-validator`).

`projection-validator` shall be extended to validate generated Upwork proposal artifacts (`upwork-qualification-report.md`, `upwork-screening-answers.md`) and append results to `out/<target-slug>/runtime/projection-validation-report.yaml`.

At minimum, tests and validation rules should cover:

Qualification

Case A — fully supported

Expected:

APPLY

Case B — unresolved requirement

Expected:

CONDITIONAL

Case C — explicit production requirement with only prototype evidence

Expected:

DO NOT APPLY

Evidence integrity

Verify that:

* unsupported metrics are rejected;
* unknown production status cannot become verified production;
* personal projects cannot satisfy explicit client-production requirements;
* adjacent technologies are not silently treated as identical;
* missing evidence is surfaced.

Proposal generation

Verify that:

* DO NOT APPLY prevents submission-ready proposal generation;
* CONDITIONAL identifies its open condition;
* APPLY produces the expected artifacts;
* screening questions are all answered;
* proposal output remains within requested constraints where applicable.

Work samples

Verify that recommendations originate from available evidence.

⸻

34. Acceptance Criteria

The feature is complete when all of the following are true.

AC-01 — Opportunity ingestion

An Upwork opportunity can be represented using the repository’s established target-opportunity mechanism.

AC-02 — Qualification

The system produces an explicit qualification decision.

AC-03 — Hard gate

An explicit client hard requirement cannot be silently bypassed.

AC-04 — Evidence integrity

Every material proposal claim can be traced to authoritative evidence.

AC-05 — Production integrity

Prototype/personal/non-production evidence cannot satisfy an explicit production requirement.

AC-06 — Conditional state

Unresolved but potentially resolvable requirements produce CONDITIONAL.

AC-07 — Do-not-apply state

Unsupported hard requirements produce DO NOT APPLY.

AC-08 — Proposal generation

Qualified opportunities produce a concise proposal.

AC-09 — Screening answers

Client screening questions produce corresponding answers.

AC-10 — Work samples

Relevant evidence-backed work samples can be recommended.

AC-11 — Human approval

The system produces artifacts for human review and performs no Upwork submission.

AC-12 — CAS compliance

Inputs are scoped and governed; the workflow does not perform unrestricted career-history ingestion.

AC-13 — SLDC compliance

The implementation follows the repository’s established development, validation and governance workflow.

AC-14 — Reproducibility

Running the workflow again with the same inputs and unchanged evidence replaces/regenerates the relevant projection outputs deterministically enough to support comparison and validation.

⸻

35. Current Reference Scenario for Testing

The following opportunity should be used as a representative qualification test case during implementation.

The client requires:

Personal implementation of a production multi-agent or AI workforce system inside a real operating company.

Available evidence includes:

* enterprise agentic-AI architecture work;
* agentic architecture standards and governance;
* MCP architecture;
* observability architecture;
* prototype-and-innovation work;
* enterprise AI governance;
* custom Python/API automation;
* personal AI architecture laboratory.

However, current authoritative evidence does not establish production multi-agent implementation inside a real operating company.

Therefore the expected result is:

DO NOT APPLY

This test is important because it validates the central feature principle:

The system must prefer an honest rejection over a persuasive but unsupported proposal.

⸻

36. Example Qualified Scenario

The implementation should also contain a positive test fixture where authoritative evidence explicitly establishes:

real company
+
personally implemented
+
production
+
requested capability

The expected result should be:

APPLY

The fixture must be synthetic or based only on existing authorised evidence; the coding agent must not invent a real career claim.

⸻

37. Future Extensions — Explicitly Out of V1

The architecture should leave room for:

Opportunity discovery

Upwork
→ candidate opportunities
→ qualification

Historical proposal analytics

proposals
→ views
→ interviews
→ hires
→ learning

Proposal experimentation

Compare:

* positioning;
* opening;
* evidence selection;
* proposal length;
* work samples.

Automated work-sample assembly

Generate a curated attachment package automatically.

Human feedback loop

Capture:

candidate review
→ correction
→ evidence refinement
→ future proposals

Approved marketplace integration

Potential future integration with an officially supported/API-based marketplace workflow may be considered separately.

None of these should be implemented as part of V1.

⸻

38. Implementation Guardrails

The coding agent must not:

* create a second OKF;
* duplicate existing evidence;
* duplicate opportunity analysis;
* scan the entire repository by default;
* invent missing evidence;
* make production assumptions;
* introduce unnecessary frameworks;
* introduce browser automation;
* create a generic “AI proposal writer” disconnected from evidence;
* bypass existing CAS controls;
* bypass existing SLDC controls;
* merge changes without validation.

The implementation should favour:

smallest coherent change that establishes a governed Upwork proposal projection.

⸻

39. Deliverables Expected from the Coding Agent

The coding agent should return:

Implementation

The required repository changes.

Architecture

A concise explanation of:

* components changed;
* new components;
* data flow;
* integration points.

Evidence

References to:

* tests;
* validation output;
* generated qualification;
* generated proposal fixture(s).

Governance

Any:

* ADRs;
* CAS changes;
* configuration changes;
* contracts.

Limitations

Explicitly identify anything not implemented in V1.

Final status

IMPLEMENTED
VALIDATED
READY FOR REVIEW

or, if blocked:

BLOCKED

with the precise reason.

⸻

40. Definition of Done

The feature should be considered Done only when:

Repository conventions inspected
        ↓
Architecture confirmed
        ↓
Requirements mapped to existing components
        ↓
Implementation completed
        ↓
Qualification gate validated
        ↓
Evidence integrity validated
        ↓
Proposal generation validated
        ↓
Screening answers validated
        ↓
Work samples validated
        ↓
CAS/SLDC compliance verified
        ↓
Human-review boundary verified
        ↓
Implementation evidence reported

The final principle for this feature is:

The generator’s job is not to maximise the number of proposals submitted. Its job is to maximise the quality and credibility of opportunities pursued.
