# Phase 0 Research & Technical Context: Upwork Proposal Generator V2.1

## Architectural Overview & Baseline Analysis

The Upwork Proposal Generator V2.1 feature extends the existing V2.0 Evidence Integrity pipeline by introducing **Human-Owned Opportunity Decisions** and **Evidence-Gap Handling**.

### Key Findings & Decisions

#### 1. Decoupling Truthfulness (Machine) from Decision (Human)
- **Decision**: The machine qualification gate (`upwork-qualification`) MUST NOT automatically block artifact generation or set irreversible `DO_NOT_APPLY` decisions when evidence is incomplete or unknown.
- **Rationale**: Real candidate career evidence is naturally incomplete. The system operates as an evidence-governed decision-support copilot.
- **Implementation**: Machine outputs a fit recommendation (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`), while `user_decision_state` (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`) remains unforced and owned by the candidate.

#### 2. Four-Tier Requirement Evidence Classification
- **Decision**: Replace binary met/unmet classifications with four canonical statuses:
  - `SUPPORTED`: Direct canonical evidence establishes the requirement for client-facing use.
  - `PARTIALLY_SUPPORTED`: Canonical evidence supports a meaningful portion of the requirement, but missing specific details.
  - `UNKNOWN`: Canonical evidence does not establish whether the requirement is met.
  - `CONTRADICTED`: Canonical evidence explicitly conflicts with or contradicts the requirement.
- **Rationale**: Provides fine-grained granularity required to isolate missing facts and render evidence-safe prose.

#### 3. Client-Facing Prose vs Internal Diagnostics Boundary
- **Decision**: Client-facing proposal prose (`upwork-qualification-report.md`) MUST be generated cleanly without internal footnotes, tag markers, or `[OPEN CONDITION]` banners embedded in text meant for Upwork submission.
- **Rationale**: Keeps submission text directly copy-pasteable while storing claim traceability and gap diagnostics in runtime YAML (`upwork-qualification.yaml`) and companion review artifacts (`upwork-evidence-gaps.md`).
- **PARTIALLY_SUPPORTED Rule**: Client-facing prose MAY include the verified, evidence-backed aspects of `PARTIALLY_SUPPORTED` requirements while explicitly omitting or qualifying unsupported aspects. Unsupported aspects MUST NEVER be asserted as fact.

#### 4. Submission Readiness Labelling
- **Decision**: Artifact packages are labelled either:
  - `SUBMISSION_READY`: All client-facing claims are evidence-backed and all material conditions resolved.
  - `HUMAN_REVIEW_REQUIRED`: Material evidence gaps exist. Indicates machine non-certification while explicitly allowing the human user to choose `APPLY` and submit after review.

#### 5. Evidence Improvement Loop & Deterministic Regeneration
- **Decision**: When a candidate reviews `upwork-evidence-gaps.md`, supplies missing facts in canonical OKF files (e.g., adding an evidence card or updating achievements in `okf/`), and re-runs the orchestrator, the pipeline MUST deterministically re-evaluate the opportunity and update the proposal prose into `SUBMISSION_READY` without manual text edits.

## Technology Stack & Dependencies

- **Runtime Environment**: Python 3.11+ / Antigravity AGY Agent Execution Context
- **Knowledge Store**: OKF v0.2 Knowledge Catalog (`out/okf/`)
- **Runtime Schema**: YAML 1.2 (`out/<target-slug>/runtime/upwork-qualification.yaml`)
- **Prose Render Engine**: Markdown / Diátaxis format
- **Validation Framework**: Pytest / `projection-validator` / `brand-validator`

## Alternatives Considered & Rejected

| Alternative | Rationale for Rejection |
|-------------|-------------------------|
| Binary gating (`APPLY` vs `DO_NOT_APPLY` hard stop) | Replaced in V2.1 because incomplete evidence suppressed useful proposal and review artifact generation. |
| Automatic prompt LLM guessing of missing metrics/counts | Rejected due to Constitution Rule I (Zero Fabrication). |
| Embedding visible footnote tags in client proposal text | Rejected because client-facing Upwork text must be cleanly copy-pasteable without internal diagnostic tags. |
| Autonomous application submission | Rejected due to Non-Goal NG-01/NG-02 and Constitution Rule III/V (Human ownership of final decision). |
