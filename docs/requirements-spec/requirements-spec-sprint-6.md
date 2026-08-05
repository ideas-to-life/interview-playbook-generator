Sprint 6 Requirements Specification

Opportunity Archetype & Market-Fit Intelligence

Version: 6.0
Status: Proposed
Priority: High
Primary driver: Real-world hiring feedback from the Vervaunt Head of AI & Automation process

1. Problem statement

The Career Intelligence Platform currently assesses opportunity alignment primarily through requirements, capabilities, evidence coverage and executive positioning.

The Vervaunt process demonstrated an important limitation.

The platform generated high-quality, evidence-backed projections and reported:

* Projection Validation: 98.2%
* Brand Validation: 99%
* strong opportunity alignment

However, subsequent hiring-team feedback identified three material concerns:

* insufficient eCommerce/agency-specific experience;
* limited evidence of hands-on automation tooling such as n8n, Zapier and the Shopify ecosystem;
* a profile perceived as substantially more Enterprise Architecture/governance-oriented than practical AI automation execution.

The platform therefore correctly assessed requirement coverage, but insufficiently assessed candidate archetype fit.

Sprint 6 shall address this gap.

⸻

2. Vision

Enable the platform to answer a new question before generating projections:

What kind of professional is this organisation actually trying to hire, and does the canonical evidence demonstrate that archetype?

The system must distinguish between opportunities that may share similar titles but represent materially different professional archetypes.

For example:

Head of AI
│
├── Enterprise AI Leader
├── AI Transformation Leader
├── AI Automation Builder
├── AI Engineering Leader
├── AI Product Leader
└── AI Consulting / Agency Leader

Job title similarity must never be treated as evidence of opportunity similarity.

⸻

3. Objectives

Sprint 6 shall:

* introduce Opportunity Archetype classification;
* distinguish capability fit from archetype fit;
* identify domain and ecosystem dependencies;
* distinguish genuine experience gaps from positioning gaps;
* detect when projections are attempting to compensate for weak evidence;
* incorporate external hiring feedback into evaluation;
* improve opportunity-selection intelligence;
* prevent misleadingly high alignment scores;
* improve projection strategy without compromising canonical identity.

⸻

4. Architectural principle

Add the following principle:

Projection quality cannot compensate for weak archetype evidence. The platform shall identify material opportunity-fit gaps before determining projection strategy.

The architecture becomes:

Canonical Career Knowledge
          │
          ↓
    Executive Identity
          │
          │
Target Opportunity
          │
          ↓
Opportunity Intelligence
          │
          ├── Requirement Analysis
          ├── Archetype Classification       ← NEW
          ├── Domain Analysis                ← NEW
          ├── Tool/Ecosystem Analysis        ← NEW
          ├── Evidence Fit
          └── Gap Classification             ← NEW
          │
          ↓
   Projection Strategy
          │
          ↓
      Projections
          │
          ↓
      Validation
          │
          ↓
 Real-World Feedback                         ← NEW

⸻

5. FR-1 — Opportunity Archetype Classifier

Extend the Opportunity Analyzer with explicit archetype classification.

The classifier shall infer the dominant professional archetype required by the opportunity.

Initial taxonomy may include:

* Enterprise Architect
* Enterprise AI Architect
* AI CoE Architect
* AI Transformation Leader
* Head of AI — Enterprise
* Head of AI — Automation
* AI Automation Builder
* AI Engineering Leader
* AI Product Leader
* AI Strategy / Advisory Leader
* Agency AI Leader
* Consulting AI Leader

The taxonomy shall remain extensible.

Output

opportunity_archetype:
  primary: ai_automation_builder
  secondary:
    - agency_ai_leader
    - head_of_ai
  confidence: high

Classification must be derived from responsibilities and expected outcomes, not job title alone.

⸻

6. FR-2 — Archetype Evidence Profile

Canonical knowledge shall be evaluated against the target archetype.

Example:

archetype_fit:
  target: ai_automation_builder
  strengths:
    - agentic_ai_architecture
    - hands_on_ai_prototyping
    - ai_operationalisation
  partial:
    - workflow_automation
  gaps:
    - ecommerce_delivery
    - shopify_ecosystem
    - n8n
    - zapier
  overall: moderate

This is runtime intelligence.

It must not modify the OKF Bundle.

⸻

7. FR-3 — Experience Dimension Model

Opportunity analysis shall distinguish at least four different dimensions of fit.

Capability fit

Can the candidate perform the underlying capability?

Example:

AI architecture.

Domain fit

Has the candidate demonstrated experience in the relevant business domain?

Example:

eCommerce.

Ecosystem/tooling fit

Has the candidate demonstrated experience with technologies explicitly important to the opportunity?

Example:

Shopify, n8n, Zapier.

Operating-context fit

Has the candidate worked successfully in the expected organisational environment?

Example:

small entrepreneurial agency versus global enterprise.

These dimensions must not be collapsed into one generic alignment score.

⸻

8. FR-4 — Gap Classification

Every material gap shall be classified.

Supported categories:

Evidence Gap
Experience Gap
Domain Gap
Tooling Gap
Positioning Gap
Terminology Gap
Operating-Context Gap

This distinction is essential.

For example:

eCommerce

Domain Gap

The platform should not attempt to rewrite around it.

Enterprise Architecture-heavy positioning

Positioning Gap

Potentially addressable through projection strategy.

n8n / Zapier / Shopify

Tooling Gap

Unless canonical evidence exists elsewhere.

⸻

9. FR-5 — Gap Severity

Each gap shall receive:

* materiality;
* confidence;
* recoverability.

Example:

gap:
  type: tooling_gap
  subject: n8n
  materiality: high
  confidence: high
  recoverability: learnable

Possible recoverability values:

projection
adjacent_evidence
learnable
experience_required
unknown

This prevents the renderer from treating all gaps as wording problems.

⸻

10. FR-6 — Anti-Overpositioning Guardrail

Introduce a critical new validation rule.

A projection shall never position the candidate more strongly than canonical evidence permits.

For example, Sprint 5 produced:

“Head of AI / Enterprise AI Architect”

and:

“ideal executive leader to build Vervaunt’s production AI practice.”

Those statements may be strategically attractive, but they risk exceeding what the evidence supports for the specific archetype.

The validator shall detect:

* unsupported identity elevation;
* unsupported domain expertise;
* unsupported tooling expertise;
* excessive transformation of adjacent experience into direct experience.

Recommended validation result:

overpositioning:
  status: warning
  reason: >
    Strong enterprise AI evidence but limited canonical
    evidence for ecommerce automation delivery.

⸻

11. FR-7 — Projection Strategy

Introduce an explicit runtime object between Opportunity Analysis and Projection.

Opportunity Analysis
        ↓
Projection Strategy
        ↓
Projection

Projection Strategy determines:

* what to lead with;
* what to de-emphasise;
* what adjacent evidence may legitimately bridge;
* what gaps must remain visible;
* what claims are prohibited;
* recommended professional positioning.

Example:

projection_strategy:
  lead_with:
    - hands_on_ai_building
    - wpp_agency_adjacency
    - cas_automation
  de_emphasise:
    - enterprise_governance
    - operating_model_detail
  bridge:
    - agency_experience
  prohibit_claims:
    - ecommerce_expert
    - shopify_experience
    - n8n_experience

This becomes a shared input to all projections.

⸻

12. FR-8 — Opportunity Fit Assessment

Replace simplistic overall alignment with a multidimensional assessment.

Example:

Dimension	Assessment
Core capability	High
AI architecture	High
Hands-on AI	High
Workflow automation	Medium
Agency context	Medium
eCommerce	Low
Shopify ecosystem	Low
n8n/Zapier	Low
Executive leadership	High

The platform may then derive:

Overall opportunity fit: Moderate–High
Archetype fit: Moderate
Primary concern:
The opportunity appears to prioritise an AI Automation
Builder archetype more heavily than an Enterprise AI
Leader archetype.

That is substantially more informative than “High alignment”.

⸻

13. FR-9 — Opportunity Selection Recommendation

Introduce a decision-support output.

Possible classifications:

Strong Fit
Good Fit
Stretch Fit
Adjacent Fit
Weak Fit

The system must explain why.

It shall not recommend against applying merely because gaps exist.

Instead it should identify whether the gaps are likely to be:

* competitive disadvantages;
* interview risks;
* addressable positioning issues;
* genuine experience requirements.

⸻

14. FR-10 — Market Feedback Capture

Introduce a structured feedback object.

Example:

market_feedback:
  opportunity: vervaunt-head-of-ai
  stage:
    recruiter_shortlist
  outcome:
    paused
  positive:
    - profile_well_aligned
    - strong_overall_experience
  concerns:
    - ecommerce_experience
    - agency_experience
    - n8n_zapier_shopify
    - enterprise_governance_weighting

This is not canonical career evidence.

It belongs in a separate learning/evaluation layer.

⸻

15. FR-11 — Feedback-to-Prediction Evaluation

The platform shall compare hiring feedback against its original predictions.

For example:

Predicted:
High alignment
Actual feedback:
Moderate archetype alignment
Missed signals:
eCommerce
Shopify
n8n/Zapier
agency operating context

This becomes an evaluation mechanism for the platform itself.

Crucially, feedback must not automatically modify canonical knowledge or future scoring rules.

It is evaluation evidence requiring review.

⸻

16. FR-12 — External Validation Score

Internal quality scores must remain separate from market-fit scores.

Do not combine:

Projection Quality
98%

with:

Opportunity Fit
72%

They measure different things.

The platform shall maintain at least:

Evidence Integrity
Brand Consistency
Projection Quality
Opportunity Fit
Archetype Fit

A 99% Brand Score therefore cannot imply 99% hiring alignment.

⸻

17. FR-13 — Learning Opportunity Detection

Where a gap is classified as learnable, the system may identify it as a development opportunity.

Example:

n8n / Zapier
Classification:
Tooling Gap
Materiality:
High for this opportunity
Career relevance:
Potentially useful
Recommendation:
Optional practical experiment rather than
repositioning professional identity.

This must remain advisory.

The platform must not distort career strategy around a single vacancy.

⸻

18. FR-14 — Opportunity Archetype Comparison

Allow the system to explain why apparently similar opportunities differ.

For example:

Head of AI — Vervaunt
        │
AI Automation Builder
Agency / eCommerce
Hands-on workflow automation
        │
        ≠
        │
Enterprise AI CoE Architect
        │
Enterprise Architecture Leader
AI governance + platforms
Regulated enterprise
Programme-scale architecture

This is particularly valuable when deciding which opportunities deserve investment.

⸻

19. Validation enhancements

Introduce an Archetype Fit Validator.

It shall check:

* archetype classification confidence;
* evidence support;
* domain alignment;
* tooling alignment;
* operating-context alignment;
* projection overreach;
* unsupported bridging.

A projection may pass Brand Validation while receiving an Archetype Fit warning.

That is expected behaviour.

⸻

20. New runtime artefacts

I would keep these outside out/okf/.

out/runtime/
├── opportunity-analysis.yaml
├── archetype-analysis.yaml
├── projection-strategy.yaml
├── opportunity-fit-report.yaml
├── projection-validation-report.yaml
└── brand-validation-report.yaml

Market feedback should probably live separately:

evaluation/
└── opportunities/
    └── vervaunt-head-of-ai.yaml

That distinction matters because feedback is neither canonical knowledge nor current runtime context.

⸻

21. Non-functional requirements

The implementation shall:

* preserve OKF immutability;
* never manufacture missing experience;
* distinguish adjacent from direct experience;
* maintain traceability for every fit judgement;
* avoid overfitting to one hiring outcome;
* keep archetype taxonomy extensible;
* treat recruiter feedback as evaluation evidence, not truth;
* preserve idempotent execution.

⸻

22. Acceptance criteria

Sprint 6 is successful when, given the same Vervaunt opportunity and the pre-feedback canonical knowledge, the system independently identifies something materially equivalent to:

Strong AI architecture and transformation capability, with credible hands-on agentic-system evidence. However, the opportunity appears to favour an AI Automation Builder / Agency AI archetype. Evidence for eCommerce, Shopify and low-code automation tooling is limited, creating a material competitive gap.

And importantly, it should identify that before seeing the recruiter feedback.

That’s the golden test for this sprint.

⸻

23. Regression test

The second golden test should be the AI CoE opportunity.

The system should distinguish it from Vervaunt and produce something closer to:

Primary archetype:
Enterprise AI / AI CoE Architect
Enterprise Architecture:
Strong
AI architecture:
Strong
Governance:
Strong
Programme-scale transformation:
Strong
Regulated environment:
Strong
Archetype Fit:
Strong

This prevents Sprint 6 from learning the wrong lesson and simply penalising Enterprise Architecture/governance.

⸻

24. Deliverables

* Opportunity Archetype Classifier
* Archetype taxonomy
* Experience Dimension Model
* Gap Classifier
* Gap Severity Model
* Projection Strategy
* Anti-Overpositioning Guardrail
* Opportunity Fit Report
* Archetype Fit Validator
* Market Feedback schema
* Feedback-to-Prediction Evaluator
* Vervaunt golden evaluation fixture
* AI CoE regression fixture
* Updated Opportunity Analyzer
* Updated Projection Validator
* Unit and integration tests

25. Sprint 6 Architectural Outcome

Sprint 6 evolves the Career Intelligence Platform from assessing requirement alignment to assessing opportunity archetype and market fit.

The resulting intelligence flow is:

Canonical Knowledge
        ↓
Executive Identity
        ↓
Opportunity Archetype
        ↓
Fit Intelligence
        ↓
Projection Strategy
        ↓
Projections
        ↓
Market Evaluation

Market feedback shall be treated as evaluation evidence rather than canonical truth. It must not autonomously modify canonical career knowledge, opportunity-scoring rules, or executive identity.