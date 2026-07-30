Design Refinements (v0.4 Review)

Status: Accepted architectural refinements following Sprint 3 design review.

These refinements clarify the separation between canonical career knowledge, coaching intelligence and presentation artefacts while preserving the additive philosophy of Sprint 3.

⸻

R1. Introduce explicit architectural layers

Motivation

The current design occasionally mixes canonical knowledge, interview coaching and presentation concerns.

Separating these layers makes Sprint 4 significantly simpler while reinforcing the OKF Bundle as the single source of truth.

⸻

Updated architecture

Portfolio
        │
Knowledge Extraction
        │
────────────────────────────────────────────
Knowledge Layer (Canonical)
────────────────────────────────────────────
Evidence Card
Achievement
Capability
Theme
Signature Achievement
Executive Behaviour Profile
        │
────────────────────────────────────────────
Coaching Layer (Derived)
────────────────────────────────────────────
Interview Strategy
Story Catalogue
Conversation Coaching
Conversation Reminders
Question Mapping
        │
────────────────────────────────────────────
Projection Layer (Views)
────────────────────────────────────────────
Interview Playbook
Interview Cheatsheet
Executive Brief
Opportunity Alignment

The layers have different responsibilities.

Knowledge Layer

Persistent.

Opportunity-independent.

Version-controlled.

Coaching Layer

Derived from canonical knowledge plus target opportunity.

Regenerated every execution.

Never treated as source material.

Projection Layer

Pure presentation.

Views only.

No business logic.

⸻

R2. Canonical knowledge must remain opportunity-independent

Motivation

Opportunity-specific information should never become part of the OKF Bundle.

Otherwise every interview changes canonical knowledge.

This violates the source-of-truth principle.

⸻

Updated principle

The OKF Bundle stores only reusable career knowledge.

Opportunity-specific interpretation shall be generated dynamically.

It shall never be persisted as canonical knowledge.

⸻

Evidence Card changes

Remove

opportunity_relevance:

from the canonical schema.

Instead compute relevance inside:

* Opportunity Alignment View
* Interview Strategy
* Executive Brief

The result may be cached during execution but must not become part of the bundle.

⸻

R3. Capability model refinement

Capabilities should become stable career assets.

Each Capability should explicitly rank supporting evidence.

Replace

Evidence

with

Primary Evidence
Supporting Evidence
Additional Evidence

The ranking is deterministic.

It is based on:

* organisational impact
* strategic significance
* breadth of capability
* confidence

This ranking becomes reusable across all future projections.

⸻

R4. Conversation Hook

Extend EvidenceCard.

Current

transition_sentence:

New

conversation_hook:
transition_sentence:

Purpose:

conversation_hook

Natural way to begin discussing the evidence.

Example

“This reminds me of a programme we delivered at BBC…”

transition_sentence

Natural way to leave the story.

Example

“That experience naturally led into my work establishing AI governance.”

Together they support conversational flow.

⸻

R5. Behaviour Profile simplification

The Behaviour Profile should distinguish between mandatory and optional dimensions.

Core dimensions

* Leadership Style
* Communication Style
* Decision Style
* Delivery Style

These should always be generated.

Optional dimensions

* Stakeholder Style
* Collaboration Style
* Executive Presence

Generated only when sufficient evidence exists.

Otherwise omitted.

This avoids creating weak or repetitive sections.

⸻

R6. Executive Brief enhancement

Introduce a short coaching section.

Interview Mindset

Maximum five bullets.

Example

* Curious
* Collaborative
* Outcome-focused
* Executive
* Commercial

This section contains coaching only.

No evidence.

⸻

R7. Capability relevance

Capabilities are opportunity-independent.

Rename

Opportunity relevance

to

Evidence strength

Opportunity alignment is calculated later.

Capabilities therefore remain stable across opportunities.

⸻

R8. Dynamic opportunity alignment

Opportunity alignment becomes a runtime computation.

Pipeline

Canonical Bundle
+
Target Opportunity
↓
Opportunity Analysis
↓
Interview Strategy
↓
Executive Brief
↓
Opportunity Alignment View

The canonical bundle is never modified.

⸻

R9. Projection contract

Every projection shall satisfy the following contract.

Inputs

* Canonical Bundle
* Target Opportunity
* Configuration

Outputs

* Presentation artefact

Constraints

* Read-only access to canonical bundle
* No mutation
* No persistence
* Fully reproducible

⸻

R10. Architecture principle

Add the following load-bearing principle near the beginning of the specification.

The OKF Bundle contains only canonical career knowledge. Opportunity-specific interpretation, coaching intelligence and presentation artefacts are always derived at execution time and are never persisted as canonical knowledge.

⸻

R11. Sprint 4 compatibility

These refinements intentionally prepare the architecture for Sprint 4.

Future projections including:

* Resume
* Cover Letter
* LinkedIn
* Executive Biography
* Consulting Proposal

will consume the same canonical knowledge without introducing additional opportunity-specific state into the bundle.

⸻

Expected architectural outcome

With these refinements, the architecture becomes cleaner and more extensible:

                    Portfolio
                        │
                Knowledge Extraction
                        │
                 Canonical OKF Bundle
                        │
        ┌───────────────┴───────────────┐
        │                               │
 Target Opportunity              Configuration
        │                               │
        └───────────────┬───────────────┘
                        │
                Coaching Intelligence
                        │
        ┌───────────────┴─────────────────────────────┐
        │                 │              │            │
 Interview Playbook   Executive Brief   Resume   Future Projections
