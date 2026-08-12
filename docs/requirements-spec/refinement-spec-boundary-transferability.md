Career Projection Generator — Refinement Requirements Specification

Refinement: Projection Strategy Evidence Boundary & Transferability

1. Objective

Refine the Projection Strategy layer so that target-role requirements cannot be promoted into candidate capabilities unless independently supported by canonical evidence.

The projection strategy must preserve a strict separation between:

1. What the target organisation needs
2. What the candidate has actually demonstrated
3. How the candidate’s demonstrated experience can be positioned as relevant or transferable

This refinement addresses the identified failure mode where:

Target requirement: “Build out a Cloud Centre of Excellence from the ground up”

was transformed into candidate positioning equivalent to:

“Established CCoE frameworks from the ground up.”

The system must instead recognise the relationship as:

Enterprise Architecture operating-model leadership → transferable to CCoE establishment

without representing the target requirement as historical candidate experience.

⸻

2. Root Cause

The investigation established the following provenance:

Raw Portfolio
    ↓
Canonical OKF
    ↓
Target Job Description
    ↓
Runtime Projection Strategy
    ↓
Generated Projection

The raw portfolio and canonical OKF contain no evidence that the candidate established a CCoE.

The target JD contains the requirement:

“Build out a Cloud Centre of Excellence from the ground up.”

The current projection-strategy.yaml subsequently classified:

CCoE governance framework establishment

under lead_with.

This created the semantic bridge:

Target requirement
        ↓
lead_with
        ↓
Candidate positioning

which allowed the projection layer to generate unsupported claims.

The refinement must break this bridge.

⸻

3. Governing Principle

Add the following permanent projection principle:

Target requirements describe what the client needs; candidate evidence describes what the candidate has done. Target requirements must never become candidate evidence or candidate positioning unless independently supported by canonical evidence.

Add the complementary principle:

When target requirements are adjacent to, but not directly evidenced by, candidate experience, the projection must use explicit transferable framing rather than domain substitution.

⸻

4. Three-Layer Semantic Separation

The Projection Strategy model MUST explicitly distinguish:

A. Target Requirement

What the organisation wants the candidate to accomplish.

Example:

Build a Cloud Centre of Excellence from the ground up.

B. Candidate Evidence

What the candidate has actually done.

Example:

Led Enterprise Architecture operating-model redesign.
Established architecture governance.
Contributed to relevant CCoE-related initiatives.

C. Projection Positioning

How the candidate’s evidence should be presented for the opportunity.

Example:

Apply Enterprise Architecture operating-model and
governance experience to the CCoE establishment mandate.

These three concepts MUST NOT be collapsed into a single capability representation.

⸻

5. Projection Strategy Capability Classes

Target capabilities entering the projection strategy MUST be classified according to their relationship to candidate evidence.

At minimum:

DIRECT
STRONG_RELEVANT
RELEVANT
TRANSFERABLE
ADJACENT
GAP

DIRECT

The candidate has explicit evidence demonstrating the target capability.

Allowed treatment:

lead_with
emphasise

STRONG_RELEVANT

The candidate has substantial evidence strongly related to the target capability.

Allowed treatment:

emphasise
support

RELEVANT

The candidate has relevant experience but it is not central to their demonstrated profile.

Allowed treatment:

support

TRANSFERABLE

The candidate has strong evidence in an adjacent discipline that can credibly transfer to the target requirement.

Allowed treatment:

frame_transferability

Must NOT automatically be treated as:

lead_with[target capability]

ADJACENT

The candidate has related but limited evidence.

Allowed treatment:

acknowledge
frame_transferability

GAP

The candidate has insufficient evidence.

Treatment:

do_not_claim

⸻

6. lead_with Semantic Constraint

The meaning of lead_with MUST be restricted.

lead_with means:

Lead with candidate capabilities that are directly supported by canonical evidence and materially relevant to the target opportunity.

It MUST NOT mean:

Lead with whatever capability the target organisation considers most important.

Therefore the following is invalid when unsupported:

lead_with:
  - ccoe_establishment

even when the target JD strongly emphasises CCoE establishment.

The correct strategy may be:

lead_with:
  - enterprise_architecture
  - architecture_operating_model
  - architecture_governance
  - cloud_transformation

with:

transferable:
  - target_capability: ccoe_establishment
    candidate_capabilities:
      - enterprise_architecture_operating_model
      - architecture_governance

The exact schema may follow existing implementation conventions.

⸻

7. Transferability Mapping

For TRANSFERABLE and ADJACENT target capabilities, the strategy MUST explicitly identify:

Target Capability
Candidate Evidence
Relationship
Transferability Rationale
Recommended Framing

Example:

target_capability: ccoe_establishment
candidate_evidence:
  - enterprise_architecture_operating_model
  - architecture_governance
relationship: transferable
rationale:
  Candidate has established and operated enterprise
  architecture governance and operating models that
  provide directly relevant experience for CCoE governance
  and operating-model design.
framing:
  Applied Enterprise Architecture operating-model and
  governance experience to cloud and CCoE-related initiatives.

The target capability itself must not become a historical candidate achievement.

⸻

8. Domain Substitution Prevention

The projection strategy MUST prevent domain substitution.

Examples of prohibited transformations:

Enterprise Architecture
        ↓
Cloud Centre of Excellence
EA governance
        ↓
Cloud governance leadership
Architecture operating model
        ↓
CCoE operating model established

unless the canonical evidence explicitly supports the target domain.

Where evidence is adjacent, use:

EA experience relevant to CCoE

rather than:

CCoE experience

⸻

9. Ownership Boundary

The Projection Strategy layer MUST preserve the ownership level of candidate evidence.

If evidence states:

contributed to

the strategy MUST NOT create:

lead_with

for a target capability requiring:

established
owned
built
led

unless separate evidence supports that ownership level.

The strategy must therefore preserve the distinction between:

target responsibility

and:

candidate historical responsibility.

⸻

10. Target Verb Protection

Target-role verbs must not be transferred to candidate history without evidence.

High-risk target verbs include:

build
establish
create
own
lead
design
transform
launch
found
set up

Example:

Target:

Build out a CCoE from the ground up.

Must not become:

Built a CCoE from the ground up.

unless independently evidenced.

Instead:

Experience establishing enterprise architecture operating models and governance relevant to building out a CCoE.

⸻

11. Evidence-Bound Projection Strategy

Before assigning any target capability to lead_with, the strategy generator MUST verify:

Target capability
        ↓
Candidate evidence exists?
        ↓
Evidence domain matches?
        ↓
Evidence strength sufficient?
        ↓
Evidence ownership sufficient?
        ↓
YES → lead_with
NO  → transferable / relevant / adjacent / gap

This check must happen before projection artefact generation.

⸻

12. Interaction with Claim Strength Validation

The existing Claim Strength & Evidence Scope Validation refinement remains mandatory.

The two controls operate at different stages:

Strategy Boundary

Prevents unsupported target capabilities from entering the projection strategy.

Target requirement
        ↓
Evidence mapping
        ↓
Strategy classification

Claim Strength Validation

Prevents generated language from exceeding the strategy/evidence boundary.

Strategy
        ↓
Generated claim
        ↓
Claim strength validation

Together:

Target
  ↓
Evidence Mapping
  ↓
Projection Strategy Boundary
  ↓
Claim Generation
  ↓
Claim Strength / Evidence Scope Validation
  ↓
Final Artefacts

⸻

13. End-to-End Validation

The existing unit-level claim validation is insufficient by itself.

The implementation MUST add an end-to-end regression check covering:

Target JD
→ Runtime Intelligence
→ Projection Strategy
→ Projection
→ Validation

The regression must inspect all material projection artefacts.

At minimum:

* Executive CV
* ATS CV
* Recruiter CV
* Cover Letter
* LinkedIn Profile
* Executive Brief
* Interview Playbook

The test must ensure that an unsupported target capability cannot reappear in any downstream artefact.

⸻

14. Enterprise Cloud Architect Regression Case

Use the existing Enterprise Cloud Architect opportunity as the primary regression scenario.

Target requirement

Build out a Cloud Centre of Excellence from the ground up.

Canonical candidate evidence

The candidate demonstrates:

* Enterprise Architecture operating-model redesign;
* architecture governance;
* TOGAF;
* LeanIX;
* enterprise transformation;
* cloud-related architecture experience;
* contribution to relevant CCoE-related activities.

The candidate does not demonstrate:

* establishing a CCoE from scratch;
* owning a CCoE;
* leading an end-to-end CCoE establishment programme;
* 15+ years of CCoE specialisation.

⸻

15. Expected Runtime Classification

The runtime SHOULD produce approximately:

Enterprise Architecture
→ DIRECT / CORE
→ lead_with
EA Operating Model
→ DIRECT / CORE
→ lead_with
Architecture Governance
→ DIRECT / CORE
→ lead_with
Cloud Transformation
→ STRONG_RELEVANT
→ emphasise
Legacy Modernisation
→ DIRECT / STRONG_RELEVANT
→ emphasise
CCoE Establishment
→ TRANSFERABLE
→ frame_transferability
Azure Native Implementation
→ ADJACENT
→ acknowledge / frame_transferability

The exact classification labels may follow the existing schema.

The critical requirement is that:

CCoE Establishment MUST NOT appear as an unsupported lead_with candidate capability.

⸻

16. Expected Projection Strategy

The generated strategy should communicate the following conceptual relationship:

Lead with Enterprise Architecture operating-model, governance and transformation leadership; use cloud transformation and modernisation experience to establish relevance; frame CCoE establishment as a transferable application of EA operating-model and governance experience; do not claim prior end-to-end CCoE establishment.

It MUST NOT communicate:

Lead with CCoE establishment.

⸻

17. Expected CV Positioning

Acceptable:

Enterprise Architect with extensive experience shaping architecture operating models, governance and technology transformation, including cloud-related initiatives and CCoE-aligned activities.

Acceptable:

Applied Enterprise Architecture operating-model and governance experience to cloud and CCoE-related initiatives.

Acceptable:

Experience contributing to CCoE-related architecture and governance workstreams.

Not acceptable:

Established a Cloud Centre of Excellence.

Not acceptable:

Built a CCoE from the ground up.

Not acceptable:

Designed and established CCoE frameworks from scratch.

Not acceptable:

CCoE Leader.

Not acceptable:

15+ years of CCoE experience.

⸻

18. Opportunity-Fit Reporting

The opportunity analysis MUST be able to report:

Strong Fit

while simultaneously reporting:

CCoE establishment: Transferable / Adjacent

This is important.

A strong overall fit does not require every individual target capability to be directly evidenced.

The report should explain that the candidate’s strength derives from:

* Enterprise Architecture;
* operating-model design;
* governance;
* transformation;
* modernisation;
* relevant cloud experience;

and that these capabilities provide credible transferability to the CCoE mandate.

⸻

19. No Target Contamination

The implementation MUST ensure that target-role terminology is treated as context, not evidence.

Specifically:

Target JD

may influence:

* terminology;
* keywords;
* prioritisation;
* relevance scoring;
* transferability analysis.

It must NOT independently influence:

* candidate evidence;
* historical achievements;
* ownership;
* duration;
* professional identity;
* demonstrated capability;
* leadership claims.

⸻

20. Acceptance Criteria

Implementation is complete when:

* Target requirements and candidate evidence are represented separately.
* lead_with is restricted to evidence-supported candidate capabilities.
* Target requirements cannot independently become lead_with capabilities.
* TRANSFERABLE and ADJACENT relationships are explicitly supported.
* Transferability mappings identify both target capability and candidate evidence.
* Domain substitution is prevented.
* Target verbs cannot be transferred into candidate history without evidence.
* Ownership boundaries are preserved.
* Claim Strength & Evidence Scope Validation remains active downstream.
* End-to-end validation covers the complete projection pipeline.
* All major generated artefacts are checked for unsupported target-derived claims.
* The Enterprise Cloud Architect regression case classifies CCoE establishment as transferable/adjacent rather than direct/core.
* The same regression case continues to classify the overall opportunity as potentially Strong Fit.
* The generated CV retains Enterprise Architect as the candidate’s primary professional identity.
* No CCoE establishment, ownership or “from scratch” claim appears without explicit evidence.
* Existing tests continue to pass.
* No candidate-specific hard-coded exception is introduced.

⸻

21. Governing Principle

Add this to the permanent Career Projection Generator governance principles:

The target defines the destination; the evidence defines the journey. Projection may explain why the candidate’s demonstrated experience makes the destination credible, but it must never rewrite the journey as though the candidate has already reached it.