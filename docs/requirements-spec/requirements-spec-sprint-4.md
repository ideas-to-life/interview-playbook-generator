Sprint 4 Requirements Specification

Career Projection Platform

Version: 4.0
Status: Proposed
Priority: High

⸻

Vision

Transform the Career Intelligence System into a projection platform capable of generating multiple executive artefacts from a single canonical knowledge model.

Sprint 4 introduces the concept of projections.

A projection is a read-only, opportunity-aware representation of canonical career knowledge optimised for a specific communication purpose.

Examples include:

* Executive Resume
* Cover Letter
* LinkedIn Profile
* Recruiter Summary
* Executive Biography

The Interview Playbook becomes the first mature projection.

⸻

Objectives

Sprint 4 shall:

* Introduce a projection architecture.
* Separate opportunity analysis from projection generation.
* Eliminate duplicated reasoning across generators.
* Preserve the OKF Bundle as the only canonical source.
* Reuse coaching and capability intelligence across all projections.

⸻

Scope

Included

* Target Opportunity Analyzer
* Projection contracts
* Resume Projection
* Projection orchestration
* Shared opportunity analysis
* Executive positioning
* ATS optimisation
* Projection quality validation

Excluded

* Website generation
* Proposal generation
* Presentation generation
* Consulting engagement documents
* Multi-opportunity comparison

These remain future roadmap items.

⸻

Guiding Principles

1. Canonical knowledge is immutable

The OKF Bundle is never modified by projections.

All projections consume canonical knowledge.

None persist opportunity-specific interpretation.

⸻

2. Opportunity analysis happens once

Opportunity reasoning shall occur exactly once.

Every projection consumes the same analysis.

No projection performs independent opportunity interpretation.

⸻

3. Projections are views

A projection is not knowledge.

It is a presentation of knowledge.

Deleting a projection never changes the canonical bundle.

⸻

4. Evidence first

Every statement must trace back to:

* Evidence Cards
* Capabilities
* Signature Achievements
* Behaviour Profile

⸻

## 5. Projection SDK

All projections shall implement a common projection contract.

A projection is a pluggable component rather than bespoke pipeline logic.

Each projection shall declare:

- Metadata
- Inputs
- Rendering Rules
- Validation Rules
- Output Schema

New projections should be added by registration rather than architectural modification.

⸻

Architecture

                   Portfolio
                        │
                Knowledge Extraction
                        │
                Canonical OKF Bundle
                        │
                 Target Opportunity
                        │
        ┌───────────────┴───────────────┐
        │                               │
        │      Opportunity Analyzer     │
        │                               │
        └───────────────┬───────────────┘
                        │
                Opportunity Analysis
                        │
        ┌───────────────┼─────────────────────────────┐
        │               │              │              │
 Interview       Executive Resume  Cover Letter  LinkedIn
 Playbook            Projection     Projection    Projection

⸻

Projection SDK Architecture

Projection Registry
↓
Projection Contract
↓
Renderer
↓
Validator
↓
Artefact

Every projection implements the same lifecycle.

The orchestration engine invokes projections through a shared contract, enabling future projections (for example Capability Statement, Speaker Biography or Consulting Proposal) without changing the orchestration pipeline.

⸻

Functional Requirements

FR-1 Target Opportunity Analyzer

Introduce a new pipeline stage.

Input:

* Job Description
* Recruiter Notes
* Company Context
* Hiring Manager Notes
* User Notes

Output:

* Opportunity Analysis

This becomes the shared source for all projections.

⸻

FR-2 Opportunity Analysis Model

Generate a canonical execution artefact containing:

Hiring Goals

Business outcomes expected from the role.

⸻

Executive Positioning

Recommended professional identity.

Examples:

* Enterprise Architect
* Head of AI
* Transformation Director
* Chief Architect

⸻

Capability Priorities

Rank capabilities by importance.

Example:

Enterprise AI Governance      High
Architecture Leadership       High
Operating Model               Medium
Platform Engineering          Medium

⸻

Behaviour Expectations

Identify expected behaviours.

Examples:

* founder mindset
* hands-on
* strategic
* collaborative
* commercial

⸻

ATS Vocabulary

Extract important terminology.

Rank:

* Mandatory
* Strong
* Optional

⸻

Organisational Signals

Capture:

* company maturity
* delivery style
* governance expectations
* culture
* pace

⸻

Risks

Highlight:

* capability gaps
* over-emphasis risks
* terminology risks

⸻

Opportunity Coverage Matrix

The Opportunity Analyzer shall generate a structured coverage assessment for each major hiring requirement.

For every requirement capture:

- Coverage (High / Medium / Low)
- Confidence (Strong / Moderate / Weak)
- Supporting Capabilities
- Primary Evidence
- Risks

This matrix becomes a shared input to every projection.

⸻

FR-3 Projection Contract

Every projection must satisfy:

Inputs

* Canonical Bundle
* Opportunity Analysis
* Projection Configuration

Outputs

* Presentation artefact

Constraints

* Read-only
* Reproducible
* Evidence-backed
* No canonical mutations

⸻

Projection Interface

Metadata
- Projection Name
- Version
- Target Audience

Inputs
- Canonical Bundle
- Opportunity Analysis
- Projection Configuration

Processing
- Read-only access
- No canonical mutations
- Evidence-backed reasoning

Outputs
- Projection Artefact
- Validation Report

⸻

FR-4 Resume Projection

Replace Resume Writer.

Generate:

* Executive Resume
* ATS Resume
* Recruiter Resume

All consume identical opportunity analysis.

⸻

Resume principles

Prioritise:

* strongest evidence
* executive outcomes
* capability progression
* leadership
* measurable impact

Do not:

* duplicate interview content
* invent achievements
* over-optimise keywords

⸻

FR-5 Cover Letter Projection

Generate:

Executive cover letter.

Sections:

* Motivation
* Alignment
* Selected Evidence
* Closing

Maximum:

One page.

⸻

FR-6 LinkedIn Projection

Generate:

* Headline
* About
* Featured summary
* Experience refinements

Optimised for:

Professional credibility rather than ATS.

⸻

FR-7 Projection Configuration

Allow projections to specify:

Audience

Examples:

* Recruiter
* Hiring Manager
* Founder
* Executive

Tone

Examples:

* Executive
* Technical
* Commercial

Length

Examples:

* One page
* Two pages
* Extended

⸻

FR-8 Shared Capability Weighting

All projections consume identical capability rankings.

No projection computes its own weighting.

⸻

FR-9 Shared Behaviour Profile

Behaviour Profile is consumed by:

* Resume
* Cover Letter
* Interview Playbook
* LinkedIn

It is generated once.

⸻

FR-10 Shared Validation

Create projection validation.

Verify:

* Evidence coverage
* Capability alignment
* ATS coverage
* Executive positioning
* Readability
* Traceability

⸻

FR-11 Projection Registry

Introduce a Projection Registry responsible for discovering, registering and executing available projections.

The registry shall:

- expose available projections
- validate projection contracts
- execute projections through a common interface
- support future projection extensions without orchestration changes

⸻

Projection Layer

Introduce:

Projection
↓
Configuration
↓
Renderer
↓
Validation
↓
Artefact

Each projection shares the same lifecycle.

⸻

Knowledge Flow

Evidence
↓
Achievements
↓
Capabilities
↓
Themes
↓
Behaviour Profile
↓
Executive Narrative
↓
Opportunity Analysis
↓
Projection

⸻

Non-Functional Requirements

NFR-1

No duplicated opportunity reasoning.

⸻

NFR-2

No duplicated capability weighting.

⸻

NFR-3

All projections remain reproducible.

⸻

NFR-4

Every sentence must trace back to canonical evidence.

⸻

NFR-5

Projection generation should remain deterministic where practical.

⸻

Success Criteria

Sprint 4 is complete when:

* Opportunity Analysis is generated once and reused by all projections.
* Resume generation becomes a projection rather than a standalone workflow.
* Cover Letter and LinkedIn projections reuse the same canonical knowledge.
* All projections share validation and evidence traceability.
* The OKF Bundle remains immutable throughout the pipeline.
* Adding a new projection requires configuration rather than architectural redesign.

⸻

Deliverables

* Target Opportunity Analyzer Skill
* Opportunity Analysis schema
* Projection Contract
* Resume Projection
* Cover Letter Projection
* LinkedIn Projection
* Shared Projection Validation
* Updated orchestration pipeline
* Regression tests
* Golden artefacts
* Projection SDK
* Projection Registry
* Opportunity Coverage Matrix
* Projection Validation Report

⸻

## Architectural Principles

The following principles govern the Career Projection Platform:

- The OKF Bundle is the single canonical source of career knowledge.
- Opportunity Analysis is generated exactly once per opportunity.
- Projections are read-only views over canonical knowledge.
- Coaching and presentation never modify canonical knowledge.
- Every generated statement must remain traceable to evidence.
- New projections should be introduced by implementing the Projection Contract and registering with the Projection Registry rather than modifying the orchestration pipeline.

This architecture follows the Open/Closed Principle by remaining open for extension while remaining closed for modification.
