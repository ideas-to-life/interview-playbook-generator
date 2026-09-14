# Feature Specification: Upwork Proposal Generator — Evidence Attribution & Composition Integrity

**Feature Branch**: `003-upwork-proposal-refinement`

**Created**: 2026-09-14

**Status**: Draft

**Input**: User description: "/speckit-specify create the formal specification for the requirements refinement @[docs/requirements-spec/upwork-proposal-generator-refinement-spec.v3.md]"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evidence Ownership & Attribution Integrity (Priority: P1)

As an Upwork candidate/consultant whose portfolio contains enterprise architecture advisory experience alongside hands-on personal/prototype projects, I want the system to preserve exact attribution boundaries (distinguishing what a platform did, what an organization deployed, what I personally architected, and what I personally implemented in production) so that client-facing proposals and screening answers never overstate my personal implementation responsibility or production deployment history.

**Why this priority**: Solves the core evidence attribution defect where candidate advisory or architectural leadership around a production platform is inflated into an unsupported claim of personally building, implementing, or deploying that underlying production platform.

**Independent Test**: Process an opportunity requiring personal production implementation against canonical evidence establishing enterprise architecture advisory around a production platform (e.g. WPP Open) and hands-on implementation in a personal project (e.g. CAS). Verify that client-facing proposals and screening answers explicitly present architecture leadership and personal implementation as distinct contexts, never claiming personal production implementation at the enterprise organization.

**Acceptance Scenarios**:

1. **Given** canonical evidence of an enterprise production platform where candidate held an architecture/advisory role, **When** qualification and proposal generation execute, **Then** the candidate's contribution is stated as architecture/advisory, platform production status is noted separately, candidate personal production implementation remains `UNRESOLVED`, and zero client-facing claims assert personal production implementation.
2. **Given** a hard screening question asking "What real company have you personally helped implement a production multi-agent system for?", **When** candidate personal production implementation is unverified, **Then** the generated screening answer explicitly preserves the evidence gap (e.g. stating enterprise architecture leadership around the platform without asserting personal production implementation) rather than producing an affirmative implementation claim followed by a disclaimer.

---

### User Story 2 - Composition Boundary Preservation Across Multiple Sources (Priority: P2)

As a candidate with multi-domain experience across different organizations and projects, I want the system to permit using complementary evidence sources (e.g. WPP for enterprise architecture, BBC for governance, CAS for hands-on agent implementation) without merging them into a single fabricated historical claim (e.g. "I implemented a production multi-agent platform at WPP").

**Why this priority**: Prevents cross-project or cross-organization evidence aggregation from manufacturing historical facts that no single evidence card independently supports.

**Independent Test**: Execute proposal generation for a role requiring enterprise agentic implementation using separate WPP (architecture) and CAS (prototype implementation) evidence cards. Verify that proposal prose describes these as separate complementary contexts rather than conflating them into a single enterprise implementation claim.

**Acceptance Scenarios**:

1. **Given** separate evidence cards for enterprise architecture (Company A) and personal implementation (Project B), **When** composing qualification rationale and proposal prose, **Then** the system presents them as distinct, complementary capability demonstrations and flags any synthesized claim that combines Company A and Project B into a unified historical fact.
2. **Given** a hard requirement for personal production implementation inside an operating company, **When** evaluating evidence composition, **Then** personal projects, prototypes, or theoretical architecture MUST NOT satisfy the hard production requirement through aggregation.

---

### User Story 3 - Historical vs. Proposed Architecture Disambiguation (Priority: P3)

As a candidate presenting technical solutions to prospective clients, I want the system to strictly separate historical experience ("At WPP, I led...") from proposed future architecture ("For your environment, I would implement..."), so that proposed technical approaches or candidate recommendations are never represented as past historical implementations.

**Why this priority**: Prevents forward-looking technical proposals or proposed stack recommendations from leaking into historical experience claims.

**Independent Test**: Generate a proposal specifying a target technology stack (e.g. LangGraph or Temporal) that appears only in the target job description or candidate's proposed approach. Verify that all references to the technology use proposed-approach phrasing ("I would deploy...") and zero references claim historical usage ("I previously deployed...").

**Acceptance Scenarios**:

1. **Given** a technology or architectural pattern specified in the proposed solution section, **When** proposal projection and validation execute, **Then** the technology is exclusively framed with prospective modal verbs ("would", "propose to"), and validation flags any historical implementation claim referencing that technology without canonical evidence.

---

### User Story 4 - Strict Multi-Axis Validation & Screening Consistency (Priority: P4)

As a candidate reviewing generated application packages, I want automated validation checks to detect attribution inflation, invalid evidence composition, screening answer contradictions, and work sample misclassifications before presenting artifacts for review.

**Why this priority**: Provides an automated quality gate ensuring zero compliance failures or contradictory statements reach the candidate or client.

**Independent Test**: Run `upwork-validator` against a proposal package. Verify that any transition from platform-capability to candidate-ownership, any contradiction between screening answers and qualification status, or any prototype work sample presented as production deployment is detected and marked as a validation failure.

**Acceptance Scenarios**:

1. **Given** a generated screening answer claiming personal production implementation alongside an `upwork-qualification.yaml` status of `UNRESOLVED` for that same fact, **When** validation executes, **Then** `upwork-validator` fails screening consistency validation and surfaces the contradiction in `upwork-validation-report.yaml`.
2. **Given** a work sample with `project_type: prototype_innovation`, **When** proposal projection generates work sample summaries, **Then** the narrative MUST describe the work as a prototype/innovation project and validation MUST fail if the summary asserts live production deployment.

---

### Edge Cases

- **Incomplete Implementation at Departure**: What happens when a candidate led an enterprise project (e.g. PCA) that was still in active implementation when the candidate departed? The system MUST permit claiming project leadership, architecture design, and implementation management, but MUST NOT claim live production deployment or operational production status for the candidate's work.
- **Contradictory Claim & Disclaimer Positioning**: How does the system handle proposals where an evidence gap exists? The system MUST NOT generate a strong historical claim (e.g. "I architected the production platform") followed by a disclaimer ("Production deployment is unverified"). The claim itself MUST be bounded upfront (e.g. "I led architecture work around an enterprise agentic AI platform; canonical evidence does not establish personal live production implementation").
- **Safe Screening Answer vs. Requirement Qualification**: How is screening question safety handled when evidence is incomplete? The answer MAY be generated safely for human review (`content_safety: EVIDENCE_SAFE`), but the requirement qualification status MUST remain `UNRESOLVED` / `PARTIALLY_SUPPORTED`, and candidate confirmation questions MUST target the precise missing personal implementation fact.

## Requirements *(mandatory)*

### Functional Requirements

#### Core Attribution & Capability Integrity (FR-001 - FR-009)
- **FR-001 (Evidence Subject & Ownership Preservation)**: The system MUST preserve the explicit subject of every evidence claim (Candidate, Organisation, Platform/System, Project/Team, Proposed Future Solution) across qualification and projection. Evidence of platform/system capability MUST NOT be transformed into a claim of candidate implementation without independent candidate-specific evidence.
- **FR-002 (Platform vs Candidate Production Disambiguation)**: The classification of a platform/system as `production` MUST NOT automatically infer `candidate_personally_implemented_production_system = true`. Qualification MUST evaluate platform production status and candidate contribution as distinct dimensions.
- **FR-003 (Contribution Boundary Preservation)**: The system MUST constrain candidate contribution claims to the strongest level supported by canonical evidence (e.g. `aligned`, `assessed`, `recommended`, `architected`, `led`). Contributions MUST NOT be upgraded to `designed`, `implemented`, `deployed`, or `operated` without explicit evidence.
- **FR-004 (Anti-Inflation Progression)**: The pipeline MUST enforce strict non-inflation rules preventing progression up the responsibility ladder: `advised` → `designed` → `implemented` → `deployed` → `production deployment`, and `worked on production platform` → `personally implemented production platform`.
- **FR-005 (Cross-Source Evidence Composition Boundaries)**: While complementary evidence from multiple sources MAY be combined to demonstrate multi-domain capabilities (e.g. enterprise architecture + hands-on prototyping), evidence composition MUST NOT synthesize a new unified historical claim (e.g. enterprise production implementation) that no single source independently supports.
- **FR-006 (Hard Requirement Evidence Scope)**: When a target requirement explicitly demands personal production implementation inside an operating company, aggregation across personal projects, prototypes, laboratories, theoretical architecture, or unrelated organizational roles MUST NOT satisfy the requirement.
- **FR-007 (Work Sample Attribution Integrity)**: Work samples MUST retain explicit metadata attributes (`project_identity`, `project_type`, `candidate_contribution`, `production_status`). Work samples marked `prototype_innovation` or `personal_project` MUST NOT be described as production implementations.
- **FR-008 (Historical vs Proposed Architecture Disambiguation)**: The system MUST enforce clear syntactic and semantic boundaries between historical evidence ("At WPP, I led...") and proposed approach ("For your environment, I would implement..."). Proposed solutions MUST NOT be represented as past historical implementations.
- **FR-009 (Safe Bounded Formulation)**: Where evidence supports architecture or advisory leadership but not personal implementation, the system MUST use bounded formulations ("led architecture", "shaped architecture", "aligned teams") rather than implementation action verbs ("built", "implemented", "deployed", "engineered").

#### Qualification & Decision Taxonomy (FR-010 - FR-017)
- **FR-010 (Content Safety vs Requirement Qualification Decoupling)**: The qualification model MUST decouple content safety from requirement qualification. An answer marked safe for human review MUST NOT imply requirement qualification. The system MUST maintain separate fields for `content_generation_safety` (`EVIDENCE_BACKED`, `EVIDENCE_SAFE_BOUNDED`, `HUMAN_REVIEW_REQUIRED`) and `requirement_qualification_status` (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNKNOWN`, `CONTRADICTED`).
- **FR-011 (Screening Answer Evidence Fidelity)**: Screening questions requiring unverified historical facts MUST NOT generate affirmative implementation claims. Unresolved questions MUST produce bounded, evidence-safe answers that explicitly acknowledge the evidence boundary alongside candidate confirmation prompts.
- **FR-012 (Non-Contradictory Claim Formulation)**: Client-facing prose MUST NOT make an assertive historical claim followed by a qualifying disclaimer in the same artifact. The primary claim itself MUST be formulated with appropriate boundaries from the start.
- **FR-013 (Precision Candidate Confirmation Questions)**: Generated confirmation questions MUST target the specific unresolved candidate implementation fact (e.g. "Did you personally implement and deploy the system at WPP Media?") rather than general platform facts ("Was the platform deployed?").
- **FR-014 (Candidate-Specific Production Assessment Model)**: Qualification for production-sensitive requirements MUST evaluate five mandatory dimensions: `system_production_status`, `candidate_contribution`, `candidate_implementation_status`, `candidate_production_deployment_status`, and `evidence_strength`.
- **FR-015 (Production Requirement Unresolved State)**: If a requirement demands personal production implementation and evidence establishes only architecture/advisory around a production platform, `requirement_qualification_status` MUST remain `PARTIALLY_SUPPORTED` or `UNKNOWN`; it MUST NOT be classified as `SUPPORTED`.
- **FR-016 (Explicit Multi-Context Capability Presentation)**: When presenting complementary capabilities across separate projects (e.g. enterprise architecture at WPP, hands-on agent coding in CAS), proposal prose MUST explicitly present them as separate, distinct evidence contexts.
- **FR-017 (Full Provenance Traceability)**: Every generated historical claim in `upwork-qualification.yaml` and client-facing artifacts MUST maintain complete provenance metadata linking the claim to candidate contribution, organization/project, evidence card IDs, production status, and claim temporal scope (historical vs proposed).

#### Proposal & Human-in-the-Loop Integration (FR-018 - FR-020)
- **FR-018 (Proposal Utility Under Evidence Gaps)**: Evidence gaps MUST NOT suppress proposal generation. Proposals MAY highlight strongly supported adjacent strengths, frame proposed technical solutions, acknowledge missing facts transparently, and invite client discussion, while strictly omitting unverified claims.
- **FR-019 (Opening Positioning Alignment)**: Opening proposal statements for opportunities with unresolved production dealbreakers MUST position candidate strengths around verified adjacent capabilities (e.g. enterprise architecture leadership, AI governance, agentic design patterns) rather than claiming satisfaction of the unresolved production dealbreaker.
- **FR-020 (Human Decision Model Sovereignty)**: Machine qualification findings (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`) and status labels (`HUMAN_REVIEW_REQUIRED`) MUST NOT restrict or override human user decision states (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`). The user remains the ultimate decision-maker.

#### Validation & Quality Controls (FR-021 - FR-025)
- **FR-021 (Attribution Shift Validation)**: `upwork-validator` MUST scan generated prose and flag any unsupported attribution shift (e.g. platform → candidate, team → candidate, organization → candidate, architecture → implementation, prototype → production, proposed → historical).
- **FR-022 (Production Claim Validation)**: Every client-facing assertion of production implementation MUST be validated against candidate-specific production evidence (`candidate_production_deployment_status == verified_production`). General platform production status is insufficient to pass validation.
- **FR-023 (Evidence Composition Validation)**: Validator MUST flag any client-facing claim that attempts to satisfy a single historical requirement by combining evidence cards from separate contexts into an unsupported composite assertion.
- **FR-024 (Screening Answer & Qualification Consistency Validation)**: Validator MUST detect and fail any package where a screening answer asserts an affirmative historical fact while `upwork-qualification.yaml` records `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED` for that same fact.
- **FR-025 (Work Sample Metadata & Narrative Consistency Validation)**: Validator MUST verify mutual consistency across `project_type`, `production_status`, `demonstrated_capability`, and summary narrative for all included work samples.

### Key Entities *(include if feature involves data)*

- **CandidateContributionProfile**: Schema entity capturing candidate-specific role (`architect`, `advisor`, `lead`, `implementer`), candidate implementation status (`verified_production`, `implementation_in_progress`, `prototype`, `architecture_only`, `unknown`), and contribution boundaries.
- **RequirementAttributionAssessment**: Schema entity within `upwork-qualification.yaml` evaluating `system_production_status`, `candidate_contribution`, `candidate_implementation_status`, `candidate_production_deployment_status`, `evidence_strength`, `content_generation_safety`, and `requirement_qualification_status`.
- **EvidenceCompositionBoundary**: Metadata rule defining valid and invalid combinations of evidence cards across projects, preventing unauthorized cross-context aggregation.
- **UpworkQualificationContextV3**: Machine-readable context at `out/<target-slug>/runtime/upwork-qualification.yaml` tracking multi-axis requirement assessments, attribution provenance, candidate confirmation questions, machine recommendations, and human decision state.
- **UpworkValidationReportV3**: Validation output at `out/<target-slug>/runtime/upwork-validation-report.yaml` logging checks for attribution shifts, production evidence grounding, composition boundaries, screening consistency, and work sample alignment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 (Zero Attribution Inflation)**: 100% prevention of candidate attribution inflation (upgrading architecture/advisory to implementation, or platform production status to candidate production implementation) across all generated client-facing proposal prose, screening answers, and work sample summaries.
- **SC-002 (Zero Unverified Cross-Source Aggregation)**: 100% detection and prevention of synthesized historical claims that merge separate project contexts into an unsupported composite assertion.
- **SC-003 (Screening Answer Consistency)**: 100% semantic consistency between screening answers, qualification statuses, and evidence gap reports—zero affirmative implementation answers generated for unresolved requirements.
- **SC-004 (Proposal Generation Utility)**: 100% of opportunities with evidence gaps generate actionable, evidence-safe proposals positioning candidate strengths around verified adjacent capabilities and proposed technical approaches without auto-blocking output.
- **SC-005 (Validation Pass Rate & Coverage)**: 100% pass rate on automated validator rules checking attribution boundaries, production evidence grounding, screening consistency, and work sample metadata alignment.
- **SC-006 (V2.0/V2.1 Regression Compliance)**: 100% preservation of four-layer architecture, OKF v0.2 graph structure, human decision sovereignty, and bounded evidence retrieval rules.

## Assumptions

- **A-001**: Upwork qualification (`skills/upwork-qualification/`), proposal projection (`skills/upwork-proposal/`), and validator (`scripts/upwork_validator.py`) skills will be refined in-place to implement V3.0 attribution and composition rules.
- **A-002**: The underlying OKF v0.2 knowledge graph (`out/okf/`) and target opportunity analysis schema (`out/<target-slug>/runtime/opportunity-analysis.yaml`) remain the canonical data sources.
- **A-003**: Human users interact with generated packages by inspecting `upwork-qualification-report.md`, `upwork-evidence-gaps.md`, and `upwork-validation-report.yaml`, updating canonical evidence in `okf/` as needed before initiating deterministic pipeline re-runs.
