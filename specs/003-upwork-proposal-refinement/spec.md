# Feature Specification: Upwork Proposal Generator — Evidence Attribution, Composition & Claim Projection Integrity (V3.1)

**Feature Branch**: `003-upwork-proposal-refinement`

**Created**: 2026-09-14

**Status**: Draft

**Input**: User description: "/speckit-specify Candidate-Agnostic Engine refinement: Employer names, project names, technologies, career-history facts, and specific evidence instances MUST NOT be embedded in production implementation logic, schemas, validators, prompts, or generation rules."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upstream Evidence Attribution & Non-Linear Contribution Preservation (Priority: P1)

As an Upwork candidate/consultant whose portfolio contains enterprise architecture advisory experience alongside hands-on personal/prototype projects, I want the system to establish structured evidence attribution upstream (distinguishing subject, candidate contribution, platform production status, candidate implementation status, deployment status, and temporal scope independently) before qualification and proposal projection take place, so that candidate contribution is never treated as a linear responsibility ladder or inflated into an unsupported production deployment claim.

**Why this priority**: Corrects the primary attribution defect upstream before prose generation, ensuring that the final validator only checks for projection consistency rather than attempting to infer semantic truth from generated prose.

**Independent Test**: Process an opportunity requiring personal production implementation against canonical evidence establishing enterprise architecture advisory around a production platform (e.g. `OrgAlpha` platform) and hands-on implementation in a personal project (e.g. `ProjectBeta`). Verify that the qualification context records candidate contribution as architecture/advisory and candidate production deployment as unknown, causing client-facing proposals and screening answers to frame the architecture leadership and prototype coding as distinct, bounded contexts without claiming personal production deployment at the enterprise.

**Acceptance Scenarios**:

1. **Given** canonical evidence of an enterprise production platform where candidate held an architecture/advisory role, **When** attribution interpretation and qualification execute, **Then** `candidate_contribution` is evaluated as `architected`/`advised`, `system_production_status` is evaluated as `verified_production`, `candidate_production_deployment_status` remains `unknown`, and zero client-facing claims assert candidate production deployment.
2. **Given** a candidate who led an enterprise implementation project that was still in progress upon departure (e.g. `ProjectGamma`), **When** qualification and proposal projection execute, **Then** project leadership and architectural design MAY be claimed, but live production deployment or operational status MUST NOT be inferred or claimed.

---

### User Story 2 - Composition Boundary Preservation Across Multiple Contexts (Priority: P2)

As a candidate with multi-domain experience across different organizations and projects, I want the system to permit using complementary evidence sources (e.g. `OrgAlpha` for enterprise architecture, `OrgBeta` for governance, `ProjectGamma` for hands-on agent implementation) to demonstrate broad capabilities, while prohibiting the synthesis of unsupported composite historical facts (e.g. "I implemented a production multi-agent platform at `OrgAlpha` using my `ProjectGamma` architecture").

**Why this priority**: Prevents cross-project or cross-organization evidence aggregation from manufacturing a single requirement-specific historical fact that no individual evidence context independently supports.

**Independent Test**: Execute proposal generation for a role requiring enterprise agentic implementation using separate `OrgAlpha` (architecture) and `ProjectGamma` (prototype implementation) evidence cards. Verify that proposal prose describes these as separate complementary contexts rather than conflating them into a single enterprise production implementation claim.

**Acceptance Scenarios**:

1. **Given** separate evidence cards for enterprise architecture (Company A) and personal project implementation (Project B), **When** evaluating a single historical requirement for personal production implementation in an operating company, **Then** the system classifies the composite evidence as unsupported for that specific historical requirement while permitting its use for multi-context capability presentation.
2. **Given** a target requirement asking for personal production implementation inside a real operating company, **When** evaluating evidence composition, **Then** personal projects, prototypes, laboratories, or theoretical architecture MUST NOT satisfy the hard requirement through aggregation.

---

### User Story 3 - Historical vs. Proposed Architecture Disambiguation (Priority: P3)

As a candidate presenting technical solutions to prospective clients, I want the system to strictly separate historical experience ("At `OrgAlpha`, I led...") from proposed future architecture ("For your environment, I would implement..."), so that proposed technical approaches or candidate recommendations are never represented as past historical implementations.

**Why this priority**: Prevents forward-looking technical proposals or proposed stack recommendations from leaking into historical experience claims.

**Independent Test**: Generate a proposal specifying a target technology stack (e.g. LangGraph, Temporal, or OpenAI Agents SDK) that appears only in the job description or candidate's proposed approach. Verify that all references to the technology use proposed-approach phrasing ("I would deploy...") and zero references claim historical usage ("I previously deployed...").

**Acceptance Scenarios**:

1. **Given** a technology or architectural pattern specified in the proposed solution section, **When** proposal projection and validation execute, **Then** the technology is exclusively framed with prospective modal verbs ("would", "propose to"), and validation flags any historical implementation claim referencing that technology without canonical evidence.

---

### User Story 4 - Strict Multi-Axis State Control & Screening Answer Integrity (Priority: P4)

As a candidate reviewing generated application packages, I want automated validation checks and screening question generators to operate on three strictly independent state axes (`requirement_qualification`, `content_generation_safety`, and `human_decision`), ensuring that screening answers never generate affirmative historical claims for unresolved requirements and never introduce assertion-then-disclaimer patterns.

**Why this priority**: Eliminates contradictory screening answers and ensures machine non-certification (`HUMAN_REVIEW_REQUIRED`) surfaces transparent review items without overriding human application decision sovereignty.

**Independent Test**: Run proposal and screening generation for an unresolved requirement. Verify that `requirement_qualification` is `PARTIALLY_SUPPORTED` / `UNKNOWN`, `content_generation_safety` is `EVIDENCE_SAFE_BOUNDED`, screening answers present bounded context with precise candidate confirmation questions, and zero assertion-then-disclaimer prose patterns exist.

**Acceptance Scenarios**:

1. **Given** a requirement classified as `PARTIALLY_SUPPORTED` or `UNKNOWN`, **When** screening answer generation executes, **Then** the generated answer MUST NOT assert the unresolved fact affirmatively, producing instead a bounded formulation with candidate confirmation prompts.
2. **Given** a generated proposal artifact, **When** validating prose structure, **Then** the validator MUST fail any pattern that makes an assertive historical claim followed by a disclaimer (e.g. "I architected the production platform at `OrgAlpha`. Live production deployment is unknown").

---

### Golden Regression Scenarios (External Test Fixtures)

> **Candidate-Agnostic Note**: Specific candidate entities (WPP, CAS, PCA) exist ONLY in external test dataset fixtures. Production engine code, schemas, and validators MUST NOT hardcode these specific names.

#### Golden Scenario 1 — WPP + CAS Attribution Regression Fixture (FR-058)
- **Given**:
  - Enterprise context (e.g. WPP): Enterprise production platform exists; candidate contributed architecture leadership, alignment, assessment, and recommendations around agentic AI initiatives; candidate personal implementation or live production deployment of the platform is NOT established.
  - Personal Lab context (e.g. CAS): Candidate personally implemented AI/agentic systems in candidate's personal architecture laboratory (CAS); CAS is a personal project, not an enterprise production deployment.
  - Requirement: "Must have personally designed and implemented AI systems inside a real operating company in production."
- **Then**:
  - System MUST NOT generate any equivalent of: "I architected [Enterprise Platform]", "I implemented [Enterprise Platform]", "I deployed the enterprise multi-agent platform", "I built a production multi-agent platform at [Enterprise]", or "I personally implemented [Enterprise]'s production agentic platform".
  - System SHOULD generate generic bounded statements distinguishing enterprise architecture/advisory experience, personal lab implementation experience, and explicit unresolved status regarding personal production implementation inside an operating company.

#### Golden Scenario 2 — Project In Progress at Departure Fixture (FR-059)
- **Given**: Candidate led an enterprise project (e.g. PCA) that was still in active implementation when the candidate departed the organization.
- **Then**: System MAY claim project leadership, architecture leadership, design, and work performed prior to departure, but MUST NOT infer or claim successful production deployment, live operational status, post-departure completion, or candidate personal production deployment.

---

### Edge Cases

- **Assertion-Then-Disclaimer Anti-Pattern**: How does the system handle proposals where an evidence gap exists? The system MUST NOT generate an assertive historical claim followed by a disclaimer ("I architected the production platform. Live deployment is unknown"). The primary claim itself MUST be bounded upfront ("I led architecture work around an enterprise agentic AI platform; canonical evidence does not establish personal live production deployment").
- **Safe Answer vs. Requirement Qualification**: How is screening question safety handled when evidence is incomplete? The answer MAY be generated safely for human review (`content_generation_safety: EVIDENCE_SAFE_BOUNDED`), but requirement qualification MUST remain `PARTIALLY_SUPPORTED` or `UNKNOWN`, and candidate confirmation questions MUST target the precise missing personal implementation fact.

## Requirements *(mandatory)*

### Functional Requirements

#### 1. Architectural Flow & Upstream Attribution Intent
- **FR-030 (Upstream Attribution Pipeline Flow)**: The pipeline MUST enforce the upstream conceptual flow: Canonical Evidence → Evidence Attribution / Interpretation → Qualification → Attributed Claims / Projection Context → Proposal / Screening / Work Samples → Validation & Quality Gate → Human Review → Human Decision / Submission. Attribution integrity MUST be established upstream prior to qualification and projection.
- **FR-030a (Cross-Cutting Validation Boundary)**: Validation MUST operate as a cross-cutting quality gate verifying projection consistency against structured attribution context, and MUST NOT become a fifth architectural layer or primary truth-inferring engine. The core architecture remains strictly 4 layers: Knowledge, Runtime, Coaching, Projection.

#### 2. Independent Attribution Dimensions & Subject Preservation
- **FR-031 (Independent Attribution Dimensions)**: Qualification and attribution MUST represent `subject`, `candidate_contribution`, `system_production_status`, `candidate_implementation_status`, `candidate_production_deployment_status`, `evidence_strength`, and `temporal_scope` as independently assessable dimensions, without treating contribution as a linear responsibility ladder (`advised` → `designed` → `implemented` → `deployed` → `production`).
- **FR-032 (Subject Preservation)**: Every historical claim MUST preserve its subject (`Candidate`, `Organisation`, `Platform/System`, `Project/Team`, `Proposed Future Solution`). Evidence regarding one subject MUST NOT be silently transferred to another subject.
- **FR-033 (Candidate Contribution Boundaries)**: Candidate contribution MUST be represented independently from system production status. Supported contributions (`advised`, `assessed`, `recommended`, `aligned`, `shaped_architecture`, `architected`, `designed`, `led`, `implemented`, `deployed`, `operated`) MUST be selected strictly based on candidate-specific evidence.
- **FR-034 (No Responsibility-Ladder Inference)**: The system MUST NOT infer `implemented` from `architected`, `deployed` from `implemented`, `production deployment` from `deployment`, `candidate implementation` from `organisation production`, or `personal implementation` from `team implementation`.
- **FR-035 (Production Status Separation)**: The system MUST independently track `system_production_status` and `candidate_production_deployment_status`. `system_production_status = verified_production` MUST NOT imply `candidate_production_deployment_status = verified_production`.

#### 3. Attribution-Aware Intermediate Representation & Provenance
- **FR-036 (Attributed Historical Claims)**: Before client-facing projection, historical claims MUST be represented in an attribution-aware intermediate form or equivalent runtime structure retaining `claim_id`, `subject`, `organisation`, `project_system_platform`, `candidate_contribution`, `system_production_status`, `candidate_implementation_status`, `candidate_production_deployment_status`, `temporal_scope`, `evidence_strength`, `evidence_card_ids`, `source_ids`, and `claim_type` (`historical` vs `proposed`).
- **FR-037 (Provenance Preservation)**: Every historical claim in qualification and client-facing artifacts MUST remain fully traceable to canonical evidence through attribution metadata. Provenance MUST NOT be reconstructed solely from generated prose.
- **FR-038 (Claim Derivation Boundary)**: Client-facing historical claims MUST be derived from attribution-aware structured claims or equivalent context. The proposal generator MUST NOT independently synthesize historical claims by freely combining raw evidence cards.

#### 4. Cross-Source Composition & Single-Fact Boundaries
- **FR-039 (Capability Composition Without Historical Fabrication)**: Complementary evidence from multiple contexts MAY be combined to demonstrate multi-domain capabilities (e.g. enterprise architecture + AI governance + hands-on prototyping), but MUST NOT be merged into a single historical fact unsupported by any individual context.
- **FR-040 (Single-Fact Requirement Boundary)**: When evaluating a requirement asking for a specific historical fact (e.g. personal production implementation in an operating company), the evidence supporting that fact MUST come from a context that independently establishes all required attributes.
- **FR-041 (Composition Boundary Classification)**: The system MUST distinguish `same_context evidence`, `complementary multi-context evidence`, and `unsupported composite evidence`. Unsupported composite evidence MUST NOT be used to satisfy a historical qualification requirement.

#### 5. Historical vs. Proposed Architecture & Technology Boundaries
- **FR-042 (Temporal & Intent Separation)**: Historical experience (what candidate did) and proposed architecture (what candidate recommends/would implement) MUST remain explicitly distinct.
- **FR-043 (Proposed Technology Boundary)**: Technologies appearing only in job descriptions, proposed architecture, or candidate recommendations (e.g. LangGraph, Temporal, Redis, Supabase, OpenAI Agents SDK) MUST NOT be represented as past historical implementations without independent canonical evidence.

#### 6. Qualification Taxonomy & Three Independent State Axes
- **FR-044 (Independent State Axes)**: The system MUST maintain three strictly decoupled state axes:
  1. `requirement_qualification`: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNKNOWN`, `CONTRADICTED`
  2. `content_generation_safety`: `EVIDENCE_BACKED`, `EVIDENCE_SAFE_BOUNDED`, `HUMAN_REVIEW_REQUIRED`
  3. `human_decision`: `APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`
  `EVIDENCE_SAFE_BOUNDED` does NOT mean `SUPPORTED`, and `HUMAN_REVIEW_REQUIRED` does NOT mean `DO_NOT_APPLY`.
- **FR-045 (Evidence Gap Proposal Utility)**: Evidence gaps MUST NOT auto-suppress proposal generation. Proposals MAY present adjacent positioning, supported capabilities, proposed architecture, relevant work samples, and confirmation questions without fabricating claims.
- **FR-046 (Opening Positioning Alignment)**: Opening statements for opportunities with unresolved production dealbreakers MUST position candidate strengths around verified adjacent capabilities rather than claiming requirement satisfaction.

#### 7. Screening Answers & Prose Patterns
- **FR-047 (Screening Answer Fidelity)**: Screening answers MUST be derived from attribution-aware qualification context. For `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED` facts, answers MUST NOT assert the fact affirmatively.
- **FR-048 (Precision Confirmation Questions)**: Candidate confirmation questions MUST target the specific missing candidate implementation fact (e.g. "Did you personally implement and deploy the system at [Organization] into live production?") rather than general platform facts ("Was [Platform] deployed?").
- **FR-049 (No Assertion-Then-Disclaimer Pattern)**: The system MUST NOT generate an affirmative historical claim followed by a disclaimer. The primary claim itself MUST be bounded upfront.

#### 8. Work Samples & Attribution Integrity
- **FR-050 (Work Sample Attribution)**: Work samples MUST preserve `project_identity`, `project_type`, `candidate_contribution`, `production_status`, and `demonstrated_capability`. Prototypes, personal projects, or incomplete projects MUST NOT be described as production deployments.
- **FR-051 (Work Sample Capability Separation)**: Personal/prototype projects MAY demonstrate technical capability without satisfying production deployment requirements inside operating companies.

#### 9. Validation Responsibilities & Quality Gates
- **FR-052 (Validation as Projection Integrity Check)**: `upwork-validator` MUST validate generated artifacts against structured qualification and attribution context. Validator checks for introduced attribution shifts (platform → candidate, team → candidate, architecture → implementation, prototype → production, proposed → historical, context A → context B).
- **FR-053 (Attribution Shift Validation)**: Validator MUST detect defined attribution shift regression patterns using generic, candidate-agnostic structured claim comparison or lexical rules without hardcoding specific employer or project names.
- **FR-054 (Production Claim Validation)**: Any client-facing assertion of candidate production implementation MUST require candidate-specific production evidence. Platform production status alone is insufficient.
- **FR-055 (Evidence Composition Validation)**: A defined attribution integrity violation MUST prevent the package from being considered validation-passing/submission-ready.
- **FR-056 (Screening & Qualification Consistency Validation)**: Validator MUST fail any package where a screening answer asserts an affirmative historical claim while qualification records `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED`.
- **FR-057 (Work Sample Narrative Consistency Validation)**: Validator MUST verify consistency between `project_type`, `production_status`, `candidate_contribution`, `demonstrated_capability`, and generated summary narrative.

#### 10. Human Sovereignty & Implementation Non-Prescription
- **FR-060 (Human Decision Sovereignty)**: Machine recommendations (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`) and status labels (`HUMAN_REVIEW_REQUIRED`) MUST NOT overwrite human user decision state (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`).
- **FR-061 (Non-Prescriptive Data Model Boundary)**: Requirements specify required information, invariants, and behaviour. The specification MUST NOT prematurely prescribe a conceptual intermediate representation or runtime structure schemas (such as a global `CandidateContributionProfile`) unless repository discovery during implementation planning (`/speckit-plan`) proves existing OKF EvidenceCards and runtime structures are insufficient.
- **FR-062 (Preserve Existing V2.0/V2.1 Constraints)**: The pipeline MUST preserve all V2.0/V2.1 constraints (4 architectural layers, cross-cutting validation, OKF v0.2 graph, bounded evidence retrieval, idempotent generation, maximum 3 work samples, zero fabrication, no Upwork scraping, no browser automation, no automated submission).

#### 11. Candidate-Agnostic Engine & Parameterized Test Fixtures
- **FR-063 (Candidate-Agnostic Engine Rule)**: The proposal-generation system MUST be candidate-agnostic. Employer names (e.g. WPP, BBC), project names (e.g. WPP Open, CAS, PCA), technologies, career-history facts, and specific evidence instances MUST NOT be embedded in production implementation logic, schemas, validators, prompts, or generation rules. Candidate-specific information MUST be consumed exclusively from canonical evidence and opportunity inputs at runtime. Candidate-specific scenarios (such as WPP/CAS) MAY exist only as external regression fixtures or test data. Regression tests MUST demonstrate the general rule rather than encode the candidate’s identity as a special case. Where practical, attribution and composition tests SHOULD use synthetic or parameterized organizations and projects (e.g. `OrgAlpha`, `ProjectBeta`, `SystemGamma`) so that passing tests demonstrates generic behavior.

## Key Entities *(include if feature involves data)*

- **AttributedHistoricalClaim**: Intermediate representation or runtime structure capturing `claim_id`, `subject`, `organisation`, `project_system_platform`, `candidate_contribution`, `system_production_status`, `candidate_implementation_status`, `candidate_production_deployment_status`, `temporal_scope`, `evidence_strength`, `evidence_card_ids`, `source_ids`, and `claim_type`.
- **RequirementAttributionAssessment**: Entity within `upwork-qualification.yaml` evaluating multi-axis requirement alignment, attribution provenance, candidate confirmation questions, and independent state classifications.
- **UpworkQualificationContextV3**: Machine-readable context at `out/<target-slug>/runtime/upwork-qualification.yaml` tracking requirement assessments, attribution provenance, machine fit recommendations, content safety modes, and human decision state.
- **UpworkValidationReportV3**: Validation output at `out/<target-slug>/runtime/upwork-validation-report.yaml` logging checks for attribution shifts, production evidence grounding, composition boundaries, screening consistency, and work sample alignment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-031 (Attribution Regression Coverage)**: 100% of defined attribution regression scenarios (including WPP+CAS FR-058 and In-Progress FR-059 test fixtures) MUST generate correctly bounded output or fail validation—zero silent attribution shifts permitted.
- **SC-032 (Production Attribution Integrity)**: 100% of defined production-sensitive regression scenarios MUST prevent system/platform production status from being transformed into candidate personal production implementation.
- **SC-033 (Cross-Context Composition Integrity)**: 100% of defined cross-source regression scenarios MUST prevent unsupported historical composites while permitting valid capability-level multi-context presentation.
- **SC-034 (Screening Answer Consistency)**: 100% of defined screening regression scenarios MUST prevent affirmative historical answers where the corresponding requirement fact is `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED`.
- **SC-035 (Historical / Proposed Separation)**: 100% of defined historical-vs-proposed regression scenarios MUST prevent proposed technologies or approaches from being represented as past historical experience without canonical evidence.
- **SC-036 (Evidence-Gap Proposal Utility)**: Opportunities with unresolved evidence MUST remain capable of generating evidence-safe, actionable proposal artifacts when proposal generation is permitted by qualification and human-decision state. Evidence gaps MUST NOT independently suppress otherwise permitted proposal generation.
- **SC-037 (V2.0/V2.1 Regression Suite Passing)**: 100% of existing V2.0/V2.1 regression test suites MUST continue to pass cleanly.
- **SC-038 (Candidate Agnosticism Verification)**: Zero employer names, project names, or specific candidate evidence strings hardcoded within production code (`skills/`, `scripts/upwork_validator.py`, or generation prompts). 100% of attribution and validation rules operate on generic metadata attributes.

## Assumptions

- **A-001**: Implementation details regarding exact schemas, intermediate file structures, and validator mechanics will be determined during `/speckit-plan` after inspecting existing codebase structures.
- **A-002**: Upwork qualification (`skills/upwork-qualification/`), proposal projection (`skills/upwork-proposal/`), and validator (`scripts/upwork_validator.py`) will be updated in-place to support V3.1 attribution and composition rules.
- **A-003**: The underlying OKF v0.2 knowledge graph (`out/okf/`) and target opportunity analysis schema (`out/<target-slug>/runtime/opportunity-analysis.yaml`) remain the canonical baseline data sources.
