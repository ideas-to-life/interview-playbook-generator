# Feature Specification: Human-Owned Opportunity Decision & Evidence-Gap Handling (Upwork Proposal Generator V2.1)

**Feature Branch**: `002-upwork-proposal-refinements`

**Created**: 2026-09-10

**Status**: Draft

**Input**: User description: "/speckit-specify @[docs/requirements-spec/upwork-proposal-generator-refinements.v2.1.md]"

## Clarifications

### Session 2026-09-10
- Q: When a requirement is classified as PARTIALLY_SUPPORTED, how should client-facing proposal prose handle the supported versus unsupported aspects of that requirement? → A: Option A — Permit using the supported aspects of PARTIALLY_SUPPORTED requirements in client-facing prose while explicitly omitting or qualifying unsupported aspects, ensuring no unverified assertion is presented as fact.
- Q: Does labelling an artifact as HUMAN_REVIEW_REQUIRED indicate that the machine cannot certify submission readiness, while still permitting the human candidate to choose APPLY and submit the proposal after review? → A: Option A — Yes, HUMAN_REVIEW_REQUIRED signifies machine non-certification due to unresolved material conditions, but the human candidate retains full authority to set user_decision_state: APPLY and submit after review.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evidence-Safe Proposal & Review Generation for Incomplete Evidence (Priority: P1)

As an Upwork candidate/consultant, when I evaluate an opportunity that has material evidence gaps (such as unknown production status or unrecorded quantitative metrics), I want the system to generate a complete, evidence-safe proposal draft and human review package without fabricating claims or auto-blocking output generation, so that I receive actionable proposal drafts and explicit gap analyses.

**Why this priority**: Core value of V2.1—decoupling machine evidence integrity from human application decision making so that incomplete canonical evidence does not suppress proposal artifact generation.

**Independent Test**: Execute the pipeline against an opportunity with an UNKNOWN production requirement. Verify that `upwork-qualification.yaml` surfaces the gap, client-facing proposal draft contains zero fabricated production assertions, the review package exposes missing facts, and proposal status is set to `HUMAN_REVIEW_REQUIRED`.

**Acceptance Scenarios**:

1. **Given** an opportunity with an `UNKNOWN` material requirement (e.g. production deployment verification), **When** qualification and proposal generation execute, **Then** an evidence-safe proposal draft and review package are produced, the missing requirement is classified as `UNKNOWN` with candidate confirmation questions, and zero fabricated assertions exist.
2. **Given** an explicit client production dealbreaker with `UNKNOWN` evidence, **When** proposal generation executes, **Then** the proposal draft does NOT claim production experience, the dealbreaker is surfaced in review artifacts as an unresolved condition, and the package is marked `HUMAN_REVIEW_REQUIRED`.

---

### User Story 2 - Human-Owned Decision Workflow & State Separation (Priority: P2)

As a candidate evaluating Upwork jobs, I want the system to provide machine fit recommendations (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`) while explicitly preserving final application decision states (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`) for me to decide, so that the machine acts as an evidence-governed copilot rather than an autonomous gatekeeper.

**Why this priority**: Ensures the system never makes irreversible application decisions on behalf of the user, keeping the candidate in total control of application submission.

**Independent Test**: Process an opportunity with multiple evidence gaps. Verify the system outputs recommendation `EVIDENCE_GAPS` alongside rationale, while maintaining `user_decision_state` as a distinct human-owned field without aborting artifact generation.

**Acceptance Scenarios**:

1. **Given** an opportunity qualification run, **When** runtime and projection artifacts are generated, **Then** machine recommendations are recorded with clear evidence rationale, while `user_decision_state` remains unforced and distinct from machine evidence classifications.
2. **Given** a recommendation of `EVIDENCE_GAPS`, **When** the candidate reviews the package, **Then** the system presents structured confirmation questions without performing any automatic application submission.

---

### User Story 3 - Evidence Improvement Loop & Deterministic Regeneration (Priority: P3)

As a candidate who has confirmed a missing career fact after review, I want to update my canonical OKF evidence and re-run the pipeline so that the proposal is deterministically regenerated into a `SUBMISSION_READY` artifact without requiring manual prose editing.

**Why this priority**: Enables continuous career knowledge capture and proposal refinement as missing facts are formally documented in the canonical knowledge graph.

**Independent Test**: Add verified evidence for a previously unknown requirement to canonical OKF evidence, re-run `playbook-orchestrator` / `upwork-proposal`, and verify that requirement classification updates to `SUPPORTED`, proposal prose incorporates the evidence, and status upgrades to `SUBMISSION_READY`.

**Acceptance Scenarios**:

1. **Given** updated canonical evidence resolving a prior gap, **When** the proposal pipeline is re-executed, **Then** the generator deterministically incorporates the new evidence into proposal prose and elevates the status to `SUBMISSION_READY` if all client claims are satisfied.
2. **Given** a candidate who has not yet updated canonical evidence, **When** re-running, **Then** the proposal remains evidence-safe with unresolved conditions explicitly marked as `HUMAN_REVIEW_REQUIRED`.

---

### Edge Cases

- **Contradicted Requirements**: What happens when canonical evidence explicitly contradicts a requirement (e.g. `verified_non_production`)? The system MUST surface the contradiction clearly in the review package, allow proposal draft generation based on other valid experience, but MUST NEVER generate client-facing prose claiming satisfaction of the contradicted requirement.
- **Screening Questions with Missing Facts**: How are screening questions answered when canonical evidence is `UNKNOWN`? The system MUST NOT generate fabricated yes/no answers or invented metrics. It MUST produce evidence-safe qualified answers, internal `[OPEN CONDITION: ...]` markers, or candidate confirmation items.
- **Cross-Organisation / Cross-Project Composition**: How does the system handle requirements that span multiple projects or personal projects? Strict V2.0 isolation remains active; personal projects cannot satisfy client production requirements, and experience from separate organisations cannot be composed to fabricate a single unified client production claim.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (V2.0 Contract Preservation)**: The system MUST preserve all Evidence Integrity Contract V2.0 rules, architectural invariants, and protections against fabrication, implicit production inference, employment-to-production inference, repository-name-to-production inference, metrics-to-production inference, personal-project contamination, cross-organisation evidence composition, and cross-project evidence composition.
- **FR-002 (Evidence Completeness Classification)**: The system MUST classify each material opportunity requirement independently into one of four mandatory statuses: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNKNOWN`, or `CONTRADICTED`.
- **FR-003 (Evidence Gap Identification)**: For every material requirement classified as `PARTIALLY_SUPPORTED` or `UNKNOWN`, the system MUST identify the exact missing fact (e.g. production status, implementation role, agent count, business outcome, technology, scale) without guessing or inferring missing values.
- **FR-004 (Human Confirmation Questions)**: The system MUST generate explicit internal confirmation questions for `UNKNOWN` or `PARTIALLY_SUPPORTED` requirements that can reasonably be confirmed by the candidate, without assuming the missing fact is true.
- **FR-005 (Decoupled Evidence & Decision)**: Evidence completeness classifications MUST be strictly decoupled from application decisions. An `UNKNOWN` classification MUST NOT automatically assert candidate unqualification or suppress proposal/review artifact generation.
- **FR-006 (Human-Owned Final Decision State)**: The system MUST support explicit human user decision states (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`) and machine recommendations (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`). The machine MUST NOT automatically force or finalize the user's decision state.
- **FR-007 (Evidence-Safe Proposal Generation)**: Proposal generation MUST be permitted even when material evidence gaps exist, provided client-facing prose is constructed exclusively from `SUPPORTED` evidence and non-fabricated opportunity framing. For `PARTIALLY_SUPPORTED` requirements, client-facing proposal prose MAY include the verified, evidence-backed aspects of the requirement while explicitly omitting or qualifying the unsupported aspects. `UNKNOWN` or unsupported aspects of `PARTIALLY_SUPPORTED` evidence MUST NEVER be presented as established fact.
- **FR-008 (Handling Unsupported Dealbreakers)**: Explicit client dealbreakers with `UNKNOWN` or `PARTIALLY_SUPPORTED` evidence MUST be surfaced prominently as evidence gaps in review artifacts, while allowing evidence-safe proposal generation that visibly omits or qualifies unsupported assertions.
- **FR-009 (Contradicted Requirement Protection)**: If evidence is `CONTRADICTED`, the system MUST NOT generate client-facing prose claiming satisfaction of the requirement, but MAY generate evidence-gap analysis and safe proposal drafts based on other supported experience.
- **FR-010 (Screening Question Integrity)**: Screening questions MUST be answered using only `SUPPORTED` evidence. For unresolved questions, the system MUST NOT generate fabricated yes/no or quantitative answers, emitting instead evidence-safe qualified answers, internal `[OPEN CONDITION: ...]` markers, or candidate confirmation items.
- **FR-011 (Quantitative Claim Integrity)**: Quantitative claims (agent counts, workflow counts, percentages, dollar figures, latency, business impact) MUST satisfy V2.0 evidence requirements; unavailable quantitative facts MUST be surfaced as gaps rather than invented.
- **FR-012 (Proposal Content Modes)**: Proposal generation MUST support explicit content modes: `EVIDENCE_BACKED` (all claims supported), `EVIDENCE_GAPS` (proposal generated with unresolved requirements), and `HUMAN_REVIEW_REQUIRED` (contains explicit unresolved conditions requiring user review).
- **FR-013 (Evidence Gap Report & Review Package)**: The system MUST generate a structured Evidence Gap Report and Human Review Package detailing requirements, evidence status, what is established, what is missing, human confirmation questions, and risk assessment for decision support.
- **FR-014 (Internal vs Client-Facing Boundary)**: The system MUST maintain a strict separation between client-facing proposal prose and internal evidence-gap/human-confirmation diagnostics. Internal provenance markers or diagnostic tags MUST NOT leak into client-facing outputs.
- **FR-015 (Work Sample Selection Integrity)**: Work samples MAY be recommended when evidence gaps exist provided each work sample is independently evidence-backed. Work samples MUST NOT be falsely presented as satisfying unresolved production dealbreakers, and personal/prototype projects MUST retain explicit labelling.
- **FR-016 (Submission Readiness Labelling)**: Proposal artifacts MUST be labelled `SUBMISSION_READY` only when all client-facing claims are evidence-backed and material conditions resolved. Artifacts with unresolved material requirements MUST be labelled `HUMAN_REVIEW_REQUIRED` (indicating machine non-certification). The `HUMAN_REVIEW_REQUIRED` label MUST NOT restrict or block the human candidate from setting `user_decision_state: APPLY` and submitting the proposal after review.
- **FR-017 (Deterministic Evidence Improvement Loop)**: The pipeline MUST support deterministic regeneration: when a candidate updates canonical OKF evidence following gap review, re-running the pipeline MUST incorporate new evidence into generated artifacts without requiring manual prose editing.
- **FR-018 (Validation & Failure Rules)**: Independent validation (`projection-validator`) MUST verify that no `UNKNOWN`, `PARTIALLY_SUPPORTED`, or `CONTRADICTED` claim is presented as established fact. Validation MUST fail any artifact containing unsupported client-facing claims.
- **FR-019 (Auditability)**: Machine-readable context (`upwork-qualification.yaml`) MUST retain complete provenance explaining requirement classifications, evidence mappings, generated confirmation questions, validation checks, and recommendation factors.

### Key Entities *(include if feature involves data)*

- **RequirementEvidenceAssessment**: Entity capturing a material opportunity requirement, its classification (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNKNOWN`, `CONTRADICTED`), missing facts, matched canonical OKF evidence IDs, and candidate confirmation questions.
- **UpworkQualificationContext**: The machine-readable YAML model stored at `out/<target-slug>/runtime/upwork-qualification.yaml`, containing requirement assessments, machine fit recommendation, evidence gaps, confirmation questions, content mode, and submission readiness status.
- **UpworkHumanReviewPackage**: The comprehensive review bundle comprising `upwork-qualification-report.md`, `upwork-evidence-gaps.md`, `upwork-screening-answers.md`, and `upwork-work-samples.md` generated for human evaluation.
- **UserDecisionState**: Human-controlled decision enum (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`) recorded independently from machine recommendation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% prevention of fabricated claims, fabricated metrics, and unverified production assertions across all generated client-facing proposal prose and screening answers.
- **SC-002**: 100% of opportunities with material evidence gaps successfully produce evidence-safe proposal drafts and review packages labelled `HUMAN_REVIEW_REQUIRED` without crashing or auto-blocking output generation.
- **SC-003**: 100% of material requirement gaps (`PARTIALLY_SUPPORTED` or `UNKNOWN`) are accompanied by explicit missing-fact definitions and candidate confirmation questions in `upwork-evidence-gaps.md` and `upwork-qualification.yaml`.
- **SC-004**: Zero leakage of internal diagnostic tags, footnote markers, or `[OPEN CONDITION]` markers into client-facing proposal prose files.
- **SC-005**: 100% pass rate on regression test suite preserving all V2.0 evidence integrity invariants (R-01 through R-14).
- **SC-006**: Successful deterministic pipeline execution updating `HUMAN_REVIEW_REQUIRED` artifacts to `SUBMISSION_READY` upon incorporation of verified canonical evidence without manual text edits.

## Assumptions

- **A-001**: The existing V2.0 qualification gate (`upwork-qualification`) and proposal projection (`upwork-proposal`) skills in `skills/` will be updated/extended to implement V2.1 logic rather than creating duplicate skills.
- **A-002**: The target opportunity schema, OKF v0.2 knowledge graph, and `projection-validator` infrastructure remain the underlying baseline architecture.
- **A-003**: Candidates interact with generated packages via standard file viewing and editing of canonical OKF evidence files (e.g. adding evidence cards or updating achievements in `okf/`) before triggering pipeline re-runs.
