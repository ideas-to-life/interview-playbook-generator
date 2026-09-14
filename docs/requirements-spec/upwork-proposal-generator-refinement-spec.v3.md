Requirements Refinement Brief

Upwork Proposal Generator — Evidence Attribution & Composition Integrity

Feature: Evidence Attribution and Composition Integrity
Target system: interview-playbook-generator
Predecessor: Upwork Proposal Generator V2.1 — Human-Owned Opportunity Decision & Evidence-Gap Handling
Purpose: Prevent projection and qualification logic from overstating candidate ownership, implementation responsibility, production status, or evidence-supported capabilities.

⸻

1. Problem Statement

The current V2.1 pipeline correctly distinguishes several important evidence states, including:

* production_status: unknown
* verified_production
* verified_non_production
* prototype_innovation
* personal_project
* HUMAN_REVIEW_REQUIRED
* EVIDENCE_GAPS

However, regenerated output demonstrates a remaining integrity problem.

Canonical evidence can correctly establish that:

* an enterprise platform existed in production;
* the candidate worked as an architect around that platform;
* the candidate led projects that leveraged the platform;
* those projects were still in implementation when the candidate departed;

while generated projections can nevertheless produce language such as:

“I architected the enterprise multi-agent platform”

or:

“Designed and architected WPP Open / Agentic AI platform, implementing multi-agent coordination…”

Such wording can cause a reader to infer that the candidate personally designed and implemented the underlying production platform.

This is an evidence attribution defect, not merely a prose-quality defect.

The system must preserve the distinction between:

1. what a system/platform did;
2. what an organisation deployed;
3. what the candidate personally designed;
4. what the candidate personally implemented;
5. what the candidate led but did not complete before departure;
6. what the candidate demonstrated only through personal projects or prototypes;
7. what is proposed as future architecture rather than historical experience.

⸻

2. Goals

The refinement shall ensure that generated qualification and proposal artifacts:

* preserve evidence ownership and attribution;
* distinguish platform capability from candidate contribution;
* distinguish production platform status from candidate production implementation;
* prevent evidence from multiple projects/organisations being combined into an unsupported historical claim;
* distinguish historical evidence from proposed future architecture;
* distinguish “safe to present for human review” from “requirement satisfied”;
* expose unresolved evidence rather than silently resolving it;
* maintain useful proposal generation when evidence is incomplete;
* remain compatible with the V2.1 human-owned decision model.

⸻

3. Non-Goals

This refinement does not aim to:

* redesign the OKF;
* change the four-layer architecture;
* introduce a new architectural layer;
* automatically infer missing candidate experience;
* automatically verify external production deployments;
* prohibit the human from submitting a proposal;
* rewrite canonical portfolio evidence;
* introduce Upwork scraping or automated submission;
* solve general natural-language truth verification;
* require every historical claim to be independently proven by external sources.

⸻

4. Core Concepts

The formal specification should define the following distinctions.

4.1 Platform/System Status

Describes the environment or system itself.

Examples:

* production platform;
* prototype;
* internal innovation platform;
* implementation;
* personal project.

This does not automatically establish candidate production implementation experience.

4.2 Candidate Contribution

Describes what the candidate personally did.

Examples:

* architected;
* designed;
* implemented;
* led;
* advised;
* assessed;
* governed;
* integrated;
* recommended evolution;
* contributed to;
* aligned teams/projects with an existing platform.

4.3 Candidate Implementation Status

Describes the state of the candidate’s own work.

Examples:

* production implementation verified;
* implementation in progress at departure;
* prototype;
* proof of concept;
* architecture/advisory only;
* unknown.

4.4 Historical Evidence

Claims about what actually happened during the candidate’s engagement.

4.5 Proposed Approach

Claims about what the candidate would do if engaged.

Historical evidence and proposed architecture must not be conflated.

⸻

5. Functional Requirements

FR-1 — Preserve Evidence Subject and Ownership

The system MUST preserve the subject of an evidence claim when projecting it into qualification or client-facing content.

For example, evidence establishing:

“WPP Open provided multi-agent orchestration”

MUST NOT be transformed into:

“I implemented multi-agent orchestration”

unless candidate-specific implementation evidence independently supports that claim.

The system MUST distinguish at minimum between:

* candidate;
* organisation;
* platform/system;
* project/team;
* proposed future solution.

⸻

FR-2 — Separate Platform Production Status from Candidate Production Experience

A platform being identified as production MUST NOT by itself establish:

candidate_personally_implemented_production_system = true

The qualification engine MUST evaluate production status in relation to the candidate’s specific contribution.

Therefore:

production platform
+
candidate architecture/advisory role
≠
candidate personally implemented production platform

unless the evidence explicitly establishes the latter.

⸻

FR-3 — Preserve Contribution Boundaries

Generated claims MUST accurately reflect the strongest contribution actually supported by evidence.

If evidence establishes that the candidate:

* aligned projects to an existing platform;
* assessed capability gaps;
* recommended architectural evolution;
* led implementation-stage projects;

the system MUST NOT upgrade those contributions to:

* designed the underlying platform;
* implemented the underlying platform;
* deployed the underlying platform;
* operated the underlying platform in production;

without explicit supporting evidence.

⸻

FR-4 — Prevent Contribution Inflation

The generator MUST NOT promote a lower-strength contribution into a stronger implementation claim.

At minimum, the following progression MUST NOT occur without evidence:

advised
  → designed
designed
  → implemented
implemented
  → deployed
deployed
  → production deployment
worked on production platform
  → personally implemented production platform

The system may describe a stronger capability only where the canonical evidence explicitly supports that level.

⸻

FR-5 — Evidence Composition Must Preserve Boundaries

Evidence from multiple sources MAY be used to demonstrate complementary capabilities.

For example:

* WPP → enterprise agentic architecture experience;
* BBC → enterprise AI governance;
* CAS → hands-on agentic implementation and observability.

However, combining these sources MUST NOT create a new historical claim that none of the sources independently establishes.

For example:

WPP architecture experience
+
CAS personal implementation

MUST NOT become:

“I implemented a production multi-agent platform at WPP.”

The generated claim must retain source/project boundaries.

⸻

FR-6 — Evidence Composition for Hard Requirements

For a hard requirement, the qualification engine MUST determine whether the requirement is supported by evidence associated with the required context.

Where the requirement explicitly requires:

personally implemented in production inside a real operating company

personal projects, prototypes, laboratories, theoretical work, or unrelated organisational experience MUST NOT satisfy that requirement through aggregation.

Complementary evidence may demonstrate adjacent capabilities but MUST NOT override the missing hard requirement.

⸻

FR-7 — Work Sample Attribution Integrity

Every generated work sample MUST preserve:

* project identity;
* project type;
* candidate contribution;
* production status where known;
* scope of demonstrated capability.

A work sample marked:

prototype_innovation

or:

personal_project

MUST NOT be described as a production implementation unless separate evidence explicitly supports that production claim for the candidate’s work.

⸻

FR-8 — Historical vs Proposed Architecture

Generated proposals and screening answers MUST distinguish:

Historical evidence

Examples:

“At WPP Media, I led…”

Proposed approach

Examples:

“I would implement…”

“My approach would be…”

“For this environment, I would use…”

Technologies appearing only as proposed solutions MUST NOT be represented as technologies historically implemented by the candidate.

⸻

FR-9 — Safe Historical Language

Where evidence supports architecture but not implementation, generated language SHOULD use appropriately bounded formulations such as:

* “I led the architecture…”
* “I shaped the architecture…”
* “I assessed…”
* “I aligned teams and projects with…”
* “I defined architectural requirements…”
* “I recommended platform evolution…”

rather than automatically using:

* “I built…”
* “I implemented…”
* “I deployed…”
* “I engineered the production platform…”

unless explicitly supported.

⸻

FR-10 — Requirement Satisfaction vs Evidence-Safe Content

The system MUST distinguish:

content safety

from:

requirement satisfaction.

A screening answer may be safe for human review while the candidate still does not have sufficient evidence to satisfy the question.

Therefore:

EVIDENCE_SAFE_QUALIFIED

MUST NOT semantically mean:

“The candidate has qualified for the requirement.”

The specification should establish separate concepts for:

* answer/content can safely be generated;
* evidence supports an affirmative answer;
* evidence is incomplete;
* human confirmation is required.

⸻

FR-11 — Hard Screening Questions

Where a screening question asks for a specific historical fact that is not established, the generated answer MUST NOT imply an affirmative answer.

For example:

“What real company have you personally helped implement a production multi-agent system for?”

If personal production implementation is not established, the answer MUST explicitly preserve the evidence gap.

The system MUST NOT produce:

“I implemented X in production…”

followed by a qualification disclaimer.

The qualification status and the wording of the answer must be semantically consistent.

⸻

FR-12 — Evidence-Gap Language Must Not Contradict the Claim

A statement such as:

“Live production deployment attestation is unrecorded”

MUST NOT appear after a preceding assertion that effectively claims the production implementation as fact.

The system MUST avoid contradictory structures such as:

I architected the production platform.
...
Production deployment is unverified.

Instead, the claim itself must be bounded:

I led architecture work around an enterprise agentic-AI platform.
The canonical evidence does not establish that I personally implemented
the underlying platform in live production.

⸻

FR-13 — Candidate Confirmation Questions

Candidate confirmation questions MUST target the precise unresolved fact.

The system SHOULD prefer:

“Did you personally implement and deploy any multi-agent system into live production at WPP Media?”

over a broader question such as:

“Was WPP Open deployed into production?”

when the client’s requirement concerns the candidate’s personal implementation.

⸻

FR-14 — Evidence Traceability

For significant historical claims, the runtime qualification artifact MUST retain sufficient provenance to establish:

* claim;
* evidence source;
* organisation/project;
* candidate contribution;
* production status;
* whether the claim is historical or proposed.

The projection layer MUST be able to trace the client-facing claim back to the evidence that supports the candidate-specific attribution.

⸻

FR-15 — No Semantic Upgrade Through Narrative Generation

Narrative generation MUST NOT add unsupported responsibility merely because a source contains related technical capabilities.

For example, evidence that a platform contained:

* multi-agent coordination;
* state persistence;
* agent-to-agent communication;
* reasoning observability;

does not independently establish that the candidate personally implemented each capability.

The generated narrative MUST preserve that distinction.

⸻

6. Qualification Requirements

FR-16 — Candidate-Specific Production Assessment

For production-sensitive requirements, qualification MUST evaluate at least:

system_production_status
candidate_contribution
candidate_implementation_status
candidate_production_deployment_status
evidence_strength

The final classification MUST be based on the candidate-specific facts required by the opportunity.

⸻

FR-17 — Production Requirement State

Where a hard requirement requires personal production implementation and the evidence establishes only enterprise architecture around a production platform, the requirement MUST remain unresolved/partially supported.

It MUST NOT become:

fully_met

merely because the surrounding platform is known to be production.

⸻

FR-18 — Cross-Project Capability Demonstration

The system MAY use personal projects to demonstrate technical depth when the candidate lacks equivalent production evidence.

For example:

WPP → enterprise agentic architecture
CAS → hands-on agent implementation
BBC → governance

But the resulting wording MUST describe these as separate evidence contexts.

⸻

7. Proposal Requirements

FR-19 — Proposal Must Remain Useful Under Evidence Gaps

An evidence gap MUST NOT unnecessarily prevent generation of a useful human-review proposal.

The proposal may:

* demonstrate adjacent strengths;
* acknowledge the relevant gap;
* distinguish production experience from prototype/personal experience;
* describe a proposed implementation approach;
* invite discussion.

However, it MUST NOT fabricate or imply the missing experience.

⸻

FR-20 — Opening Positioning

Where a hard production requirement is unresolved, the proposal opening MUST NOT position the candidate as having definitively satisfied that requirement.

It MAY position the candidate around strongly supported adjacent strengths such as:

* enterprise agentic architecture;
* AI governance;
* architecture leadership;
* orchestration;
* observability;
* human approval controls;
* durable-state architecture.

⸻

8. Validation Requirements

FR-21 — Attribution Validation

The validator MUST detect or flag generated claims where candidate ownership appears stronger than the underlying evidence.

At minimum, validation should identify potential transitions involving:

* platform → candidate;
* organisation → candidate;
* team → candidate;
* proposed → historical;
* prototype → production;
* architecture → implementation;
* implementation → deployment.

The specification should not mandate a particular implementation technique for semantic detection.

⸻

FR-22 — Production Claim Validation

A client-facing historical statement containing a production implementation claim MUST have corresponding candidate-specific production evidence.

The fact that an evidence card describes a production platform is insufficient.

⸻

FR-23 — Evidence Composition Validation

The validator MUST flag cases where a hard requirement is supported only through a combination of evidence sources whose contexts do not jointly establish the required fact.

Example:

WPP architecture
+
CAS personal project
=
NOT sufficient evidence for
personal WPP production implementation

⸻

FR-24 — Screening Consistency Validation

The validator MUST detect inconsistencies between:

* screening answer;
* qualification status;
* evidence gap;
* production status.

A screening answer MUST NOT make an affirmative historical claim where the corresponding qualification remains unresolved for the same fact.

⸻

FR-25 — Work Sample Consistency Validation

The validator MUST check that:

* project_type;
* production status;
* demonstrated capability;
* summary narrative

are mutually consistent.

⸻

9. Human Decision Model

The existing V2.1 principle remains unchanged:

The user is the ultimate decision maker.

The machine owns:

* evidence integrity;
* truthful attribution;
* provenance;
* qualification analysis;
* identification of evidence gaps.

The human owns:

* whether to confirm an unresolved fact;
* whether to hold;
* whether to apply;
* whether to submit.

A machine finding of HUMAN_REVIEW_REQUIRED MUST NOT prohibit human submission.

⸻

10. Acceptance Scenarios

The formal /speckit-specify output should include scenarios at least covering the following.

Scenario A — Production platform, architecture role

Given:

* platform is production;
* candidate architected/aligned work around it;
* candidate implementation of underlying platform is not established;

When generating qualification and proposal content,

Then:

* platform production status may be stated;
* candidate architecture contribution may be stated;
* candidate production implementation MUST remain unresolved;
* no personal production implementation claim is generated.

⸻

Scenario B — Production platform + personal prototype

Given:

* WPP demonstrates enterprise architecture;
* CAS demonstrates hands-on multi-agent implementation;
* neither establishes personal WPP production implementation;

Then:

* both may be used as complementary evidence;
* the sources remain explicitly separated;
* no combined WPP production implementation claim is generated.

⸻

Scenario C — Project led but incomplete at departure

Given:

* candidate led PCA;
* project was still in implementation when candidate departed;

Then:

* leadership and architecture contribution may be claimed;
* production deployment MUST NOT be claimed;
* project may be used as implementation-stage evidence.

⸻

Scenario D — Verified candidate production implementation

Given explicit canonical evidence that the candidate personally implemented and deployed a multi-agent system into live production at a real operating company,

Then:

* the relevant production requirement may be classified as satisfied;
* client-facing historical content may make the corresponding production implementation claim;
* provenance must identify the supporting evidence.

⸻

Scenario E — Proposed technology

Given a technology appears only in the proposed architecture,

Then:

* it may appear in “I would…” / “proposed approach” content;
* it MUST NOT appear as historical implementation experience.

⸻

Scenario F — Safe answer but unresolved requirement

Given:

* a screening question requires personal production implementation;
* evidence is incomplete;

Then:

* the system may generate an evidence-safe human-review answer;
* the answer MUST NOT imply affirmative qualification;
* qualification remains unresolved;
* human confirmation is explicitly surfaced.

⸻

Scenario G — Work sample is prototype

Given:

project_type = prototype_innovation

Then:

* the work sample may demonstrate technical capability;
* it MUST NOT describe the work as a production deployment without separate supporting evidence.

⸻

11. Regression Requirements

The implementation MUST preserve all existing V2.0/V2.1 guarantees, including:

* four architectural layers;
* cross-cutting validation;
* human-owned decision state;
* APPLY / CONDITIONAL / DO NOT APPLY semantics where applicable;
* evidence-gap handling;
* bounded evidence retrieval;
* deterministic/idempotent generation;
* target scoping;
* no unrestricted history scanning;
* no Upwork scraping;
* no browser automation;
* no automated submission.

The new refinement MUST NOT regress the recently corrected source-level production classifications.

⸻

12. Key Acceptance Criterion

The most important acceptance criterion is:

The system must never transform evidence that establishes a candidate’s work around an existing production platform into an unsupported claim that the candidate personally designed, implemented, or deployed that production platform.

A second equally important criterion is:

Evidence from separate contexts may demonstrate complementary capabilities, but aggregation must never manufacture a historical fact that no individual evidence context establishes.

⸻
