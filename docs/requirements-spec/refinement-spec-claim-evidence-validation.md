Refinement: Claim Strength & Evidence Scope Validation

1. Objective

Strengthen the Career Projection Generator so that generated CV claims are constrained not only by evidence relevance, but by the actual scope, strength, ownership, specificity, duration and seniority supported by that evidence.

The system must prevent semantic amplification where evidence that supports contribution to a capability is projected as leadership, ownership or establishment of that capability.

This refinement is intended to generalise across all target roles and must not introduce target- or candidate-specific exceptions.

⸻

2. Problem Statement

The current implementation correctly validates whether generated claims have related evidence, but evidence relevance alone is insufficient.

Example failure:

Canonical evidence:
Contributed to CCoE-related architecture/governance activities
as part of a broader architecture team.
Generated claim:
Established Cloud Centre of Excellence operating models.
Generated claim:
Built EA and Cloud Centre of Excellence frameworks from scratch.
Generated positioning:
CCoE Leader

The generated claims are thematically related to the evidence but materially exceed its supported scope.

The system therefore needs to distinguish:

Evidence relevance
≠
Evidence equivalence

A claim is valid only when the evidence supports the specific meaning and strength of the claim.

⸻

3. New Governing Principle

Add the following permanent principle to the projection governance model:

Evidence relevance does not imply evidence equivalence. A claim may only be generated at the level of ownership, scope, specificity, duration and seniority explicitly supported by its evidence.

Add the following complementary rule:

When evidence supports contribution to a capability, the system must not infer leadership, ownership, establishment, or end-to-end responsibility for that capability.

⸻

4. Claim Strength Model

Introduce an explicit claim-strength model.

At minimum, distinguish:

CONTRIBUTED
SUPPORTED
ADVISED
DESIGNED
LED
OWNED
ESTABLISHED
TRANSFORMED

The exact vocabulary may follow existing schema conventions, but the implementation must preserve the semantic distinction between these levels.

Strength ordering

Where applicable, treat the levels as progressively stronger claims:

CONTRIBUTED
    ↓
SUPPORTED
    ↓
ADVISED
    ↓
DESIGNED
    ↓
LED
    ↓
OWNED
    ↓
ESTABLISHED / TRANSFORMED

The system MUST NOT automatically promote a lower-strength evidence item into a higher-strength claim.

⸻

5. Evidence Scope Dimensions

Every material generated claim must be evaluated against the following dimensions.

5.1 Ownership

Determine the highest ownership level supported by evidence:

Participant
Contributor
Advisor
Designer
Lead
Owner
Established / Accountable

A claim must not exceed the evidence-supported ownership level.

Example:

Evidence:
Contributed to CCoE governance
Allowed:
Contributed to CCoE governance
Not allowed:
Led CCoE governance
Not allowed:
Established CCoE governance

⸻

5.2 Scope

Determine the supported scope:

Task
Workstream
Project
Programme
Function
Organisation
Enterprise
Multi-enterprise

A project-level contribution must not become an enterprise-wide ownership claim unless explicitly evidenced.

⸻

5.3 Domain

Determine the domain to which the evidence actually applies.

Examples:

Enterprise Architecture
Cloud
CCoE
AI
Governance
Technology Strategy
Data
Security
Transformation

Conceptual adjacency must not be treated as domain equivalence.

Example:

Evidence:
Established Enterprise Architecture governance.
Not automatically equivalent to:
Established Cloud Centre of Excellence governance.

The projection may describe the EA experience as transferable to CCoE governance, but must not rewrite the original domain as CCoE.

⸻

5.4 Specificity

Classify whether the evidence supports:

General capability
Specific discipline
Specific operating model
Specific framework
Specific technology
Specific implementation

The system must not increase specificity without evidence.

Example:

Evidence:
Cloud governance experience.
Allowed:
Cloud governance experience.
Potentially allowed:
Experience contributing to CCoE-related governance.
Not allowed without evidence:
Designed an Azure CCoE operating model.

⸻

5.5 Duration

Claims involving duration must be explicitly supported.

Allowed:

5+ years of Enterprise Architecture experience

only where the canonical career evidence supports that duration.

The system must never infer:

15+ years of CCoE experience

from a collection of CCoE-related activities spanning a broader 15-year architecture career.

Duration applies to the specific capability, not merely the surrounding career period.

⸻

5.6 Seniority

Determine the evidence-supported seniority:

Practitioner
Contributor
Senior Contributor
Lead
Principal / Strategic
Executive / Accountable

The system must not infer leadership or accountability solely from the candidate’s overall seniority.

For example:

Senior Enterprise Architect

does not automatically mean:

CCoE Leader

if the evidence shows contribution to CCoE initiatives rather than ownership.

⸻

6. Claim Scope Vector

Where technically appropriate, represent claim scope internally as a structured vector:

ClaimScope {
    strength
    ownership
    scope
    domain
    specificity
    duration
    seniority
}

The generated claim must be considered valid only if its scope is less than or equal to the evidence-supported scope across all material dimensions.

Conceptually:

ClaimScope ≤ EvidenceScope

Where a material dimension exceeds evidence support:

PASS     → claim supported
DOWNGRADE → claim can be weakened to supported level
REJECT   → claim cannot be safely expressed

⸻

7. Claim Validation Pipeline

Extend the existing validation pipeline to:

Generated Claim
       ↓
Evidence Retrieval
       ↓
Evidence Relevance Check
       ↓
Evidence Scope Analysis
       ↓
Claim Strength Analysis
       ↓
Scope Comparison
       ↓
PASS / DOWNGRADE / REJECT

The existing evidence coverage and integrity mechanisms must remain in place.

The new validation layer supplements them rather than replacing them.

⸻

8. Downgrade Behaviour

Where a claim is directionally correct but too strong, the system SHOULD automatically downgrade it rather than immediately reject it.

Example:

Generated:
Established CCoE operating models.

Evidence:

Contributed to CCoE-related governance activities.

Possible downgrade:

Contributed to CCoE-related governance and
operating-model initiatives.

Another example:

Generated:
Led cloud transformation governance.

Evidence:

Contributed to cloud transformation governance.

Downgrade to:

Contributed to cloud transformation governance.

The downgrade must preserve target relevance without overstating responsibility.

⸻

9. Rejection Behaviour

Reject the claim entirely where no defensible lower-strength formulation exists.

Examples:

Evidence:
Participated in an Azure transformation programme.
Claim:
Established an Azure Centre of Excellence from scratch.
Result:
REJECT
Evidence:
Contributed to AI governance.
Claim:
Owned enterprise-wide AI governance strategy.
Result:
REJECT

The system should then select an alternative evidence-backed claim.

⸻

10. Target Terminology Protection

Target terminology MUST NOT increase claim strength.

The target description may contain terms such as:

* CCoE Leader
* Azure Architect
* Cloud Strategy Lead
* AI Transformation Director
* Data Governance Lead

The presence or frequency of these terms must not cause the generator to promote evidence to the corresponding ownership or expertise level.

Target terminology may influence:

* keyword selection;
* terminology alignment;
* capability emphasis;
* ordering;
* discoverability.

It must not influence:

* evidence strength;
* ownership;
* duration;
* seniority;
* scope.

⸻

11. Cross-Domain Transferability

The system SHOULD explicitly support truthful transferability statements.

Where evidence comes from an adjacent domain, the projection may express:

Relevant transferable experience

rather than converting the adjacent domain into the target domain.

Example:

Evidence:
Established Enterprise Architecture governance frameworks.
Target:
Cloud Centre of Excellence.
Allowed:
Applied Enterprise Architecture governance experience
to cloud and CCoE-related initiatives.
Not allowed:
Established a Cloud Centre of Excellence.

This distinction is essential for senior candidates whose experience frequently transfers across adjacent disciplines.

⸻

12. Leadership Claim Protection

Introduce explicit validation for leadership verbs and titles.

High-risk terms include:

Led
Owned
Established
Built
Founded
Created
Directed
Headed
Accountable for
CCoE Leader
Practice Lead
Programme Director

These terms require evidence at an appropriate ownership and seniority level.

The system must not infer leadership solely from:

* senior job title;
* seniority;
* participation in a leadership team;
* participation in a programme;
* contribution to a workstream.

⸻

13. “From Scratch” Claim Protection

Claims containing concepts equivalent to:

from scratch
built from the ground up
established from inception
created the function
created the practice
set up the CoE

must receive enhanced validation.

Such claims require explicit evidence of:

* initiation;
* ownership;
* establishment responsibility;
* sufficient scope.

If the evidence only supports contribution to an already-existing initiative, the claim MUST be rejected or downgraded.

⸻

14. Professional Identity Interaction

This refinement must remain compatible with the previous Candidate Identity Protection refinement.

The rules operate at different levels:

Identity Protection

Determines:

Who is the candidate?

Claim Strength / Evidence Scope

Determines:

What can the candidate truthfully claim about their experience?

Target Projection

Determines:

Which truthful capabilities should be emphasised for this opportunity?

Therefore:

Canonical Identity
        ↓
Evidence
        ↓
Claim Strength / Scope
        ↓
Target-Relevant Emphasis
        ↓
Projected CV

The target opportunity must never bypass the evidence-scope layer.

⸻

15. Validation Report

Extend the projection validation report with a section such as:

## Claim Strength & Evidence Scope Validation

For material claims, report:

Claim	Evidence	Supported Strength	Claim Strength	Result
CCoE governance contribution	CCoE governance workstream	Contributor	Contributor	PASS
CCoE operating model leadership	EA operating-model evidence	Adjacent	Leader	DOWNGRADE
Established CCoE from scratch	No direct evidence	None	Established	REJECT

The exact presentation may follow existing reporting conventions.

The report should make it possible to diagnose why a claim was downgraded or rejected.

⸻

16. Regression Test — Enterprise Cloud Architect / CCoE

Use the current Enterprise Cloud Architect opportunity as the primary regression test.

Canonical evidence scenario

The candidate:

* has extensive Enterprise Architecture experience;
* has established and operated EA governance / operating-model capabilities;
* has contributed to CCoE-related activities;
* has contributed to specific areas of cloud governance / transformation;
* has not established a CCoE from the ground up;
* has not been the overall CCoE owner;
* has relevant but not necessarily deep hands-on Azure implementation experience.

Expected claims

The projection MAY say:

Enterprise Architect with experience contributing to cloud and CCoE-related governance initiatives.

It MAY say:

Applied Enterprise Architecture operating-model and governance experience to cloud transformation initiatives.

It MAY say:

Experience contributing to CCoE-related architecture and governance workstreams.

Prohibited claims

The projection MUST NOT say:

Established a Cloud Centre of Excellence.

Built a CCoE from the ground up.

CCoE Leader.

Built CCoE frameworks from scratch at BBC Studios and WPP.

15+ years of CCoE experience.

unless explicit canonical evidence is subsequently added that genuinely supports those claims.

⸻

17. Acceptance Criteria

Implementation is complete when all of the following are satisfied:

* Evidence relevance and evidence equivalence are explicitly distinguished.
* Claim strength is explicitly evaluated.
* Ownership is explicitly evaluated.
* Scope is explicitly evaluated.
* Domain is explicitly evaluated.
* Specificity is explicitly evaluated.
* Duration is explicitly evaluated.
* Seniority is explicitly evaluated.
* Generated claim scope cannot exceed evidence scope.
* Claims can be automatically downgraded where appropriate.
* Unsupported claims are rejected.
* Target terminology cannot increase claim strength.
* Leadership claims receive explicit ownership validation.
* “From scratch” / establishment claims receive enhanced validation.
* Adjacent-domain evidence can be expressed as transferable experience without domain substitution.
* Validation reporting identifies claim/evidence mismatches.
* The Enterprise Cloud Architect / CCoE regression case passes.
* No candidate-specific exception is introduced.
* Existing projection tests continue to pass.
* Existing Candidate Identity Protection behaviour remains intact.

⸻

18. Governing Example

Use this as the canonical conceptual test for the implementation:

Evidence:
"Contributed to CCoE governance work."
Valid:
"Contributed to CCoE governance."
Invalid:
"Led CCoE governance."
Invalid:
"Owned CCoE governance."
Invalid:
"Established the CCoE."
Invalid:
"Built the CCoE from scratch."

And:

Evidence:
"Established Enterprise Architecture operating model."
Valid:
"Established an Enterprise Architecture operating model."
Potentially valid:
"Applied Enterprise Architecture operating-model
experience to CCoE-related initiatives."
Invalid:
"Established a Cloud Centre of Excellence."

The distinction must be semantic, not merely keyword-based.

⸻

19. Final Design Principle

Add this to the permanent projection governance principles:

Project relevance aggressively, but project responsibility conservatively.

And the complete chain should now be:

Canonical identity determines who the candidate is. Evidence determines what the candidate has done. Claim-strength validation determines how strongly that experience may be stated. Target relevance determines what should be emphasised.

This gives the Career Projection Generator the right balance between competitive positioning and professional credibility.