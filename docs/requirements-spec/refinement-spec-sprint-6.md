Sprint 6 Refinement Requirements Specification

Runtime-to-Projection Fit Consistency

Version: 6.1
Status: Proposed
Scope: Sprint 6 acceptance refinement
Priority: High
Driver: Vervaunt golden-test execution

1. Problem Statement

Sprint 6 successfully classified the Vervaunt Head of AI & Automation opportunity as primarily:

AI Automation Builder

and identified material gaps across:

* eCommerce domain experience;
* n8n/Zapier/Shopify tooling;
* agency operating context;
* Enterprise Architecture/governance weighting.

The runtime Opportunity Fit assessment consequently classified the opportunity as a Stretch Fit.

However, downstream opportunity-alignment.md contains:

Workflow Automation — Strong

based primarily on evidence of CAS Architecture-as-Code workflow automation.

The same projection also states that:

custom Python multi-agent orchestration provides engineering foundation for n8n/Zapier.

Although the underlying evidence is valid, the presentation risks converting adjacent/transferable evidence into apparent direct requirement coverage.

This creates inconsistency between Runtime Intelligence and Projection output.

⸻

2. Objective

Ensure that downstream projections faithfully preserve the distinctions established by Runtime Intelligence between:

Direct Evidence
Adjacent Evidence
Transferable Evidence
Learnable Gap
Material Experience Gap

A projection may explain adjacent capability but must never use it to silently upgrade a runtime fit assessment.

⸻

3. Architectural Principle

Add the following principle:

Runtime fit intelligence constrains projection claims. Projections may contextualise or explain a gap, but may not independently upgrade its coverage, confidence, or alignment classification.

The authority hierarchy shall be:

Canonical Evidence
        ↓
Runtime Intelligence
        ↓
Projection Strategy
        ↓
Projection
        ↓
Validation

A downstream layer may become more conservative, but not more optimistic without new evidence.

⸻

4. FR-1 — Evidence Relationship Classification

Runtime Intelligence shall explicitly classify evidence used against an opportunity requirement as one of:

evidence_relationship:
  direct
  adjacent
  transferable
  absent

Definitions:

Direct — Canonical evidence demonstrates substantially the same capability, domain, tooling or operating context required by the opportunity.

Adjacent — Canonical evidence demonstrates a closely related capability but not the requested experience itself.

Transferable — Evidence demonstrates underlying skills reasonably transferable to the requirement, while meaningful contextual differences remain.

Absent — No credible canonical evidence supports the requirement.

⸻

5. FR-2 — Evidence Relationship Must Constrain Alignment

Projection alignment classifications shall respect the evidence relationship.

Default mapping:

Evidence Relationship	Maximum Default Alignment
Direct	Strong
Adjacent	Moderate
Transferable	Transferable
Absent	Gap

A projection shall not classify adjacent or transferable evidence as Strong unless Runtime Intelligence explicitly provides an evidence-backed override.

⸻

6. FR-3 — Preserve Gap Classification

Where Runtime Intelligence identifies a material:

* Domain Gap;
* Tooling Gap;
* Operating-Context Gap;
* Experience Gap;

the projection shall surface that distinction when discussing the corresponding requirement.

For Vervaunt, the desired behaviour is materially equivalent to:

Workflow Automation — Moderate / Transferable
Strong evidence of custom Python, agentic and architecture workflow automation, but limited direct evidence of the low-code/SaaS automation ecosystem emphasised by this opportunity.

Not:

Workflow Automation — Strong

⸻

7. FR-4 — Adjacent Evidence Bridging

Projection Strategy may use adjacent evidence to demonstrate transferability.

Example:

bridge:
  requirement: low_code_workflow_automation
  evidence:
    - python_automation
    - agentic_orchestration
    - architecture_as_code
  relationship: adjacent

The projection may state:

Strong custom Python and agentic orchestration experience provides adjacent automation capability.

It shall not state or imply:

Equivalent n8n/Zapier experience.

⸻

8. FR-5 — Explicit Direct-Evidence Absence

Where named tooling or domain experience is materially important and no direct evidence exists, projections shall state this transparently when relevant.

Preferred formulation:

Direct n8n/Zapier experience is not evidenced in the canonical portfolio.

Acceptable softer formulation for candidate-facing artefacts:

n8n/Zapier represents adjacent rather than directly demonstrated experience.

The system shall avoid defensive or apologetic wording.

⸻

9. FR-6 — No Gap Argumentation

Projections shall not attempt to “argue away” a gap.

The following reasoning pattern shall be prohibited:

No direct evidence of X
        ↓
Candidate has more sophisticated Y
        ↓
Therefore candidate effectively has X

Instead:

No direct evidence of X
        ↓
Relevant adjacent evidence Y exists
        ↓
Transferability is explained
        ↓
Gap remains explicitly classified

This applies particularly to tools, industries and operating contexts.

⸻

10. FR-7 — Alignment View Enhancement

Update the Opportunity Alignment View to distinguish evidence type explicitly.

Recommended structure:

Requirement	Evidence	Evidence Relationship	Alignment
AI Strategy	BBC GenAI strategy	Direct	Strong
Internal AI Tools	EA4ALL / RAI	Direct	Strong
Business Workflow Automation	CAS / Python automation	Adjacent	Moderate
Agency Context	WPP Media	Transferable	Transferable
eCommerce	No direct evidence	Absent	Gap
n8n / Zapier	No direct evidence	Absent	Gap
Shopify ecosystem	No direct evidence	Absent	Gap

Exact rendering may vary, but the semantic distinction is mandatory.

⸻

11. FR-8 — Requirement Decomposition

The system shall avoid combining materially different requirements into a single alignment row when doing so hides gaps.

For example:

eCommerce / Tooling

should be decomposed where evidence differs:

eCommerce Domain
n8n / Zapier Automation
Shopify Ecosystem

Similarly, generic:

Workflow Automation

should distinguish where relevant:

Engineering-led Automation
Business Workflow Automation
Low-code/SaaS Automation

Requirement decomposition shall be opportunity-driven rather than universally hard-coded.

⸻

12. FR-9 — Projection Strategy Authority

projection-strategy.yaml shall become the authoritative constraint contract for downstream projections.

At minimum, it shall expose:

fit_constraints:
  - requirement: low_code_workflow_automation
    relationship: adjacent
    maximum_alignment: moderate
  - requirement: ecommerce
    relationship: absent
    maximum_alignment: gap
  - requirement: agency_context
    relationship: transferable
    maximum_alignment: transferable

All relevant projections must consume these constraints.

⸻

13. FR-10 — Projection Fit Consistency Validation

Extend archetype-fit-validator / projection validation to compare projection claims against Runtime Intelligence.

Validation shall detect:

Alignment inflation

Runtime:

Moderate

Projection:

Strong

Evidence inflation

Runtime:

Adjacent

Projection implies:

Direct

Gap disappearance

Runtime identifies:

Tooling Gap

Projection omits or contradicts the gap in a section explicitly assessing tooling fit.

Unsupported equivalence

Projection treats adjacent technology or domain experience as equivalent to the target requirement.

⸻

14. FR-11 — Validation Findings

Violations shall produce actionable findings.

Example:

fit_consistency:
  status: FAILED
  findings:
    - type: alignment_inflation
      requirement: workflow_automation
      runtime_alignment: moderate
      projection_alignment: strong
      source: opportunity-alignment.md

Warnings may be used where wording is ambiguous rather than contradictory.

⸻

15. FR-12 — Validation Scope

Fit-consistency validation shall apply primarily to projections that make explicit opportunity-fit claims, including:

* Opportunity Alignment;
* Executive Brief;
* Recruiter Resume;
* Cover Letter;
* Interview Playbook.

Not every gap must appear in every projection.

For example, an Executive Resume does not need to advertise every missing tool.

However, no projection may contradict the runtime assessment.

This distinction is important:

Preserve truth does not mean repeat every weakness everywhere.

⸻

16. FR-13 — Vervaunt Golden-Test Enhancement

Extend the existing Vervaunt golden fixture.

The test shall verify that the generated Opportunity Alignment View does not classify low-code/business workflow automation as Strong solely from CAS/Python/agentic evidence.

Expected semantics:

Engineering automation       Strong
Business workflow automation Moderate / Transferable
n8n/Zapier                    Gap
Shopify                       Gap
eCommerce                     Gap
Agency context                Transferable

Exact wording is not required.

Semantic equivalence is.

⸻

17. FR-14 — AI CoE Regression Protection

The refinement must not globally downgrade adjacent capabilities.

For the Enterprise AI CoE fixture, where canonical evidence directly supports:

* Enterprise Architecture;
* AI governance;
* architecture roadmap/target state;
* agentic architecture;
* programme-scale transformation;

these areas must remain eligible for Strong alignment.

The purpose of v6.1 is precision, not conservatism.

⸻

18. FR-15 — No Canonical Changes

This refinement shall require no changes to canonical OKF knowledge solely to satisfy opportunity-fit rendering.

The problem exists between:

Runtime Intelligence
        ↓
Projection Strategy
        ↓
Projection

and must be solved there.

Canonical evidence shall only change if genuinely new source evidence is discovered.

⸻

19. Non-Functional Requirements

The refinement shall:

* preserve Sprint 6 separation of concerns;
* remain evidence-first;
* avoid hard-coded Vervaunt-specific logic;
* operate across arbitrary opportunities;
* maintain deterministic constraints where practical;
* preserve existing Projection SDK contracts where possible;
* retain backward compatibility with Sprint 5 projections;
* introduce no autonomous modification of canonical knowledge.

⸻

20. Acceptance Criteria

v6.1 is complete when a clean Vervaunt run produces internally consistent conclusions across:

Archetype Analysis
Gap Analysis
Opportunity Fit Report
Projection Strategy
Opportunity Alignment
Projection Validation

The platform should be able to say simultaneously:

Alexandre has strong hands-on engineering-led AI automation evidence.

and:

Alexandre has limited direct evidence of the n8n/Zapier/Shopify-oriented business automation ecosystem required by this opportunity.

Both statements are true.

The system must preserve both without collapsing one into the other.

⸻

21. Golden Acceptance Scenario

Given:

* the original Vervaunt opportunity;
* the canonical portfolio;
* no recruiter feedback supplied to Runtime Intelligence;

the platform shall independently produce a result materially equivalent to:

Stretch Fit. Strong AI architecture, custom AI tooling and engineering-led automation capability, with transferable agency experience. Material direct-evidence gaps remain in eCommerce, Shopify and low-code business automation tooling such as n8n/Zapier.

No downstream projection may materially contradict this conclusion.

⸻

22. Regression Scenario

Given the Enterprise AI CoE opportunity, the same pipeline shall recognise direct evidence for Enterprise Architecture, AI architecture, governance and programme-scale transformation and shall not downgrade these merely because v6.1 introduces stricter evidence relationship rules.

⸻

23. Deliverables

* Evidence Relationship classification
* Fit Constraint model
* Updated Projection Strategy Generator
* Updated Opportunity Alignment projection
* Requirement decomposition rules
* Projection Fit Consistency Validator
* Alignment-inflation detection
* Evidence-inflation detection
* Gap-disappearance detection
* Updated Vervaunt golden fixture/tests
* AI CoE regression tests
* Updated Sprint 6 design documentation
