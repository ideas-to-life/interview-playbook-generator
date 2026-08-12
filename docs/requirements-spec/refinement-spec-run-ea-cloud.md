Career Projection Generator — Refinement Requirements Specification

1. Objective

Refine the Career Projection Generator so that target-role tailoring:

* preserves the candidate’s canonical professional identity and career trajectory;
* adapts emphasis, terminology and evidence to the target opportunity;
* does not allow the target job title, terminology or capability emphasis to redefine the candidate’s primary professional archetype;
* prevents adjacent or transferable experience from being promoted into unsupported primary expertise;
* maintains strict evidence fidelity between the canonical knowledge model and generated CV claims.

2. Problem Identified

The Enterprise Cloud Architect / CCoE contract demonstrated a failure mode:

Input reality

* Strong Enterprise Architecture experience
* Strong transformation and governance experience
* Relevant cloud transformation / modernisation experience
* Relevant CCoE-style governance and operating-model experience
* Relevant AI transformation / operationalisation experience
* More limited evidence for hands-on Azure-native implementation

Generated positioning

Enterprise & Cloud Architect | CCoE Leader

with claims such as:

“over 15 years of experience building Cloud Centre of Excellence (CCoE) operating models”

This correctly recognised target-role alignment but over-weighted the target archetype, effectively converting relevant/adjacent capabilities into the candidate’s primary professional identity.

3. Core New Invariant

Implement the following invariant across all projection workflows:

Target-role tailoring may change the emphasis of the candidate’s canonical identity, but must never redefine the candidate’s canonical professional identity.

Formally:

Projected Identity =
    Canonical Professional Identity
    + Target-Relevant Emphasis
    - Irrelevant Detail

It must not become:

Projected Identity =
    Target Job Title
    + Target Terminology
    + Candidate Evidence

4. Canonical Identity Protection

The projection layer MUST treat the canonical Executive Identity / Narrative / Voice as an immutable positioning anchor.

The target opportunity may influence:

* capability emphasis;
* evidence selection;
* achievement ordering;
* terminology;
* summary emphasis;
* headline formulation;
* role-specific keywords.

The target opportunity MUST NOT independently determine:

* primary professional archetype;
* career identity;
* seniority identity;
* dominant career narrative;
* claimed duration of expertise;
* primary domain expertise.

The projection must therefore adapt the canonical identity rather than recreate it.

5. Target Archetype vs Candidate Archetype

Introduce an explicit distinction between:

Candidate Archetype
Target Role Archetype
Projection Positioning

For example:

Candidate Archetype
Enterprise Architect / Transformation & AI Advisor
Target Role Archetype
Enterprise Cloud Architect / CCoE Lead
Projection Positioning
Enterprise Architect specialising in transformation,
governance and cloud modernisation, with relevant
CCoE and AI experience

The target archetype must never automatically replace the candidate archetype.

6. Capability Classification

Before projection, classify target-relevant capabilities against the canonical evidence model into at least:

CORE
STRONG
RELEVANT
ADJACENT
GAP

The projection rules MUST respect this classification.

CORE / STRONG

May be used to:

* shape the headline;
* form primary positioning;
* lead the executive summary;
* anchor experience bullets;
* support strong expertise statements.

RELEVANT

May be used to:

* strengthen target alignment;
* appear in the executive summary;
* support selected experience bullets;
* provide secondary positioning.

ADJACENT

May be used to:

* demonstrate transferable capability;
* establish contextual relevance;
* support a target-role fit argument.

Must not automatically become:

* a primary identity;
* a headline identity;
* a leadership title;
* a long-duration expertise claim.

GAP

Must not be represented as demonstrated experience.

Where useful, gaps may be explicitly characterised as adjacent or transferable capability.

7. Evidence Fidelity Rule

Every generated claim must continue to satisfy:

Claim
→ Evidence Card
→ Signature Achievement / Capability
→ Canonical Narrative
→ Executive Identity
→ Projection

The projection layer must not increase the strength of a claim beyond the strength supported by its source evidence.

Specifically, the system MUST NOT transform:

"relevant experience with X"

into:

"expert in X"

or:

"experience contributing to X"

into:

"led X for 15 years"

unless the canonical evidence explicitly supports that claim.

8. Duration Integrity

Target-role terminology must never cause the generator to infer duration.

For example:

If evidence supports:

experience with CCoE-related governance

the generator MUST NOT infer:

15+ years building CCoEs

unless the canonical evidence explicitly establishes that duration and scope.

Duration claims must always originate from evidence-backed career history.

9. Leadership Integrity

The same rule applies to leadership claims.

The system MUST distinguish between:

* led;
* established;
* designed;
* contributed to;
* advised;
* supported;
* operated within.

Target-role language such as “CCoE Leader”, “Cloud Transformation Lead” or “Azure Architect” must not cause the system to promote a lower-strength evidence category into a leadership claim.

10. Headline Generation Rules

The headline generator must prioritise:

1. Canonical professional identity
2. Strong target-relevant differentiators
3. Relevant target terminology
4. Keywords where useful for ATS/recruiter discoverability

Target job titles may be incorporated only where they remain truthful representations of the candidate’s professional identity.

For example, for the Enterprise Cloud Architect opportunity:

Preferred:

Enterprise Architect | Cloud Transformation, Governance & AI

or:

Enterprise Architect | Transformation, Cloud & AI

Avoid:

Enterprise & Cloud Architect | CCoE Leader

unless the canonical evidence explicitly establishes that as a genuine professional identity.

11. Executive Summary Generation

The executive summary should preserve the candidate’s career trajectory while changing emphasis.

For the tested opportunity, the intended hierarchy is:

Enterprise Architecture
        ↓
Transformation & Governance
        ↓
Cloud Modernisation
        ↓
AI

rather than:

Cloud
        ↓
CCoE
        ↓
Azure
        ↓
Enterprise Architecture
        ↓
AI

The summary should communicate:

* broad Enterprise Architecture foundation;
* transformation and governance leadership;
* relevant cloud modernisation experience;
* relevant CCoE / architecture operating-model experience;
* AI as an additional differentiator.

12. Target Vocabulary Control

Target terminology should be used for alignment, not identity substitution.

The system MAY adopt terminology from the target description when it accurately maps to canonical evidence.

However:

Keyword match must never override evidence hierarchy.

For example, frequent target references to “Azure” must not cause Azure to become more prominent than Enterprise Architecture simply because it appears more frequently in the job description.

13. Opportunity Analysis vs Projection

Preserve the existing architectural separation:

Canonical Knowledge Model
          ↓
Shared Opportunity Analysis
          ↓
Projection

Opportunity Analysis determines:

* capability alignment;
* evidence strength;
* gaps;
* target requirements;
* terminology;
* weighting.

Projection determines:

* how the existing identity should be expressed for this opportunity.

Projection MUST NOT independently reinterpret the candidate’s professional identity.

14. Fit Assessment Must Remain Independent

The system should be able to conclude:

Strong Fit

while simultaneously concluding:

Target archetype is not the candidate’s primary professional identity.

These are not contradictory.

For example:

Overall Fit: Strong
Enterprise Architecture: Very Strong
Transformation/Governance: Very Strong
Cloud/CCoE: Strong / Relevant
Azure hands-on implementation: Moderate / Adjacent
AI: Relevant
Primary Candidate Identity:
Enterprise Architect / Transformation & AI Advisor
Target Role:
Enterprise Cloud Architect / CCoE

This distinction should be preserved in generated outputs.

15. Contradiction Check

Add a post-generation validation rule:

Does the projected CV make the candidate appear to have a materially different primary professional identity from the canonical identity?

If YES:

* flag the projection;
* identify the identity drift;
* regenerate the affected positioning elements;
* preserve target-relevant evidence while restoring the canonical archetype.

Potential detection signals include:

* headline dominated by target-specific title;
* target domain appearing as the candidate’s primary profession;
* unsupported leadership titles;
* unsupported duration claims;
* target-specific expertise appearing more strongly than canonical expertise;
* disappearance of canonical differentiators.

16. Over-Positioning Detection

Introduce an explicit Positioning Drift / Over-Positioning check.

Example:

Target asks:
Cloud + CCoE + Azure
Canonical profile:
EA + Transformation + Governance + AI
Generated:
Cloud + CCoE + Azure + EA + AI

The system should identify this as potential drift when target capabilities displace the canonical hierarchy.

Desired result:

EA + Transformation + Governance
        ↓
Cloud / CCoE
        ↓
AI

17. Regression Test

Add the current Enterprise Cloud Architect / CCoE opportunity as a mandatory regression test case.

The test should verify that the generated projection:

* retains Enterprise Architecture as the primary identity;
* retains transformation/governance as core positioning;
* recognises cloud/CCoE as strong relevant experience;
* does not claim 15+ years of CCoE experience;
* does not claim unsupported Azure implementation leadership;
* does not use “CCoE Leader” as a primary identity;
* acknowledges Azure hands-on implementation as adjacent/moderate where appropriate;
* retains AI as a relevant differentiator;
* produces a strong but truthful target-aligned CV.

18. Acceptance Criteria

The refinement is complete when:

* Canonical professional identity remains immutable during projection.
* Target-role archetype is explicitly distinguished from candidate archetype.
* Target terminology cannot independently redefine professional identity.
* CORE/STRONG/RELEVANT/ADJACENT/GAP capability classifications affect allowable positioning strength.
* Duration claims remain evidence-backed.
* Leadership claims remain evidence-backed.
* Headline generation preserves canonical identity.
* Executive summary preserves canonical career trajectory.
* Target-specific keywords can improve alignment without overriding identity.
* Opportunity Analysis remains separate from Projection.
* Projection cannot independently invent or strengthen claims.
* Post-generation identity-drift validation is implemented.
* Enterprise Cloud Architect / CCoE case passes as a regression test.
* The resulting CV can be strongly targeted to the role without making the candidate appear to be a different professional.

19. Governing Principle

Add this as a permanent Career Projection Generator principle:

Tailor the expression of the candidate to the opportunity, never the identity of the candidate to the opportunity.

And, importantly, this should sit alongside the existing evidence precedes claims principle rather than replace it.

The two together give us the stronger rule:

Evidence determines what Alexandre can credibly claim; canonical identity determines who Alexandre is; the target opportunity determines which of those truths should be emphasised.

