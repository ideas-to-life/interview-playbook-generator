# Research & Architectural Decisions: Upwork Proposal Generator (V3.1)

## Overview

This document records the architectural research, decision rationale, and evaluation of technical placement options for implementing V3.1 Evidence Attribution, Composition & Claim Projection Integrity.

---

## Decision 1: Architectural Placement of Attribution Integrity

### Question
Where should attribution interpretation (evaluating subject, candidate contribution, system production status, candidate implementation status, deployment status, and temporal scope) be performed in the pipeline?

### Decision
Attribution interpretation MUST be established **upstream** in the Runtime Layer (`upwork-qualification` skill / runtime context builder) BEFORE prose projection and qualification assessment take place.

### Rationale
- **Upstream vs Downstream**: Previously (in V2.1), prose generators independently synthesized text from raw cards, leaving `upwork-validator` to infer whether generated prose over-stated candidate attribution. This led to prose-level attribution leaks.
- **Role of Validator**: In V3.1, `upwork-validator` acts as a cross-cutting quality gate verifying that generated prose is consistent with structured, evidence-grounded attribution established upstream. It does not infer primary truth from prose.
- **Layer Boundary**: Validation remains a cross-cutting check across Runtime and Projection layers, preserving the canonical 4-layer architecture (Knowledge, Runtime, Coaching, Projection).

### Alternatives Evaluated
1. *Post-hoc Prose Validation (V2.1 approach)*: Relying entirely on regex or LLM checks in `upwork-validator` to detect attribution inflation after prose is generated. **Rejected**: Failed to prevent subtle prose inflation; validator was forced to act as the primary truth engine.
2. *Knowledge Layer Schema Overhaul*: Modifying all canonical OKF `EvidenceCard` schemas in `out/okf/` to include V3.1 attribution fields. **Rejected**: Violates canonical OKF specification (`GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md`) and over-complicates shared target-agnostic OKF knowledge nodes.

---

## Decision 2: Schema Strategy & Intermediate Representation (FR-061 Non-Prescription)

### Question
Should V3.1 introduce a new global persistent schema (e.g. `CandidateContributionProfile`), or extend existing runtime structures (`upwork-qualification.yaml`)?

### Decision
Extend `upwork-qualification.yaml` runtime schema with an attribution-aware intermediate claim structure (`attributed_historical_claims` and enhanced multi-axis `requirement_assessments`), leaving OKF canonical cards intact.

### Rationale
- **FR-061 Non-Prescription**: Section 13 of V3.1 explicitly mandates avoiding premature global schema creation. Extending existing governed runtime context at `out/<target-slug>/runtime/upwork-qualification.yaml` satisfies all 7 attribution dimensions (`subject`, `candidate_contribution`, `system_production_status`, `candidate_implementation_status`, `candidate_production_deployment_status`, `evidence_strength`, `temporal_scope`) without introducing redundant data stores.
- **Idempotency & Clean Disk Writes**: The runtime file is cleanly overwritten on every `upwork-qualification` run, keeping execution deterministic and idempotent.

---

## Decision 3: Three Independent State Axes Architecture (FR-044)

### Question
How should qualification status, content generation safety, and human decision state be modeled to prevent state conflation?

### Decision
Model three explicitly decoupled state enums in `upwork-qualification.yaml`:
1. `requirement_qualification_status`: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNKNOWN`, `CONTRADICTED`
2. `content_generation_safety`: `EVIDENCE_BACKED`, `EVIDENCE_SAFE_BOUNDED`, `HUMAN_REVIEW_REQUIRED`
3. `user_decision_state`: `APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`

### Rationale
- Prevents semantic confusion where `EVIDENCE_SAFE_BOUNDED` was mistaken for `SUPPORTED`, or `HUMAN_REVIEW_REQUIRED` was treated as `DO_NOT_APPLY`.
- `EVIDENCE_SAFE_BOUNDED` allows generating a useful proposal draft for human review using bounded phrasing without implying that missing evidence is verified.
- Keeps final submission decision (`user_decision_state`) strictly in human hands (Human Sovereignty principle).

---

## Decision 4: Cross-Source Evidence Composition Rules (FR-039 - FR-041)

### Question
How should the system handle multi-source evidence (e.g. WPP enterprise architecture, BBC governance, CAS personal lab)?

### Decision
Classify evidence composition into three distinct categories:
1. `same_context_evidence`: Card belongs to the target organization/project context.
2. `complementary_multi_context_evidence`: Cards demonstrate complementary strengths across separate contexts (permitted for capability-level positioning).
3. `unsupported_composite_evidence`: Combining separate contexts to satisfy a single historical requirement (prohibited from satisfying requirement qualification).

---

## Decision 5: Non-Linear Contribution Assessment (FR-031, FR-034)

### Question
How to prevent contribution inflation without forcing a linear hierarchy?

### Decision
Evaluate `candidate_contribution` against explicit candidate-specific evidence cards. Prohibit automatic ladder leaps (`advised` → `designed` → `implemented` → `deployed` → `production`).

---

## Decision 6: Candidate-Agnostic Engine & Parameterized Test Fixtures (FR-063, SC-038)

### Question
How should candidate-specific entities (e.g., WPP, BBC, CAS, PCA) be handled across production code, prompts, schemas, validators, and tests?

### Decision
Production engine code (`skills/upwork-qualification/`, `skills/upwork-proposal/`), schemas, prompts, and validator logic (`scripts/upwork_validator.py`) MUST remain 100% candidate-agnostic. Employer names, project names, and candidate identity facts MUST NOT be hardcoded in production rules or regexes.
- Candidate-specific scenarios (such as WPP/CAS) exist ONLY as external test data fixtures or parameterized pytest datasets.
- Unit and integration tests SHOULD use synthetic or parameterized organization and project fixtures (e.g. `OrgAlpha`, `ProjectBeta`, `SystemGamma`) to demonstrate generic, candidate-agnostic attribution logic.

### Rationale
- Preserves the platform's core identity principle: The engine is a general-purpose career projection runtime for any candidate. Hardcoding specific employer names or project names in validation scripts or prompt instructions breaks generic reusability.
- Ensures `upwork_validator.py` evaluates semantic metadata attributes (`candidate_contribution`, `candidate_production_deployment_status`, `project_type`) rather than grepping for specific company strings.
