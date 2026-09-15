---
name: upwork-proposal
description: Generates clean executive proposal prose, companion evidence gap reports, screening answers, and work sample recommendations in out/<target-slug>/ based on upwork-qualification runtime context.
---

# Upwork Proposal Projection (V3.1)

## Overview

`upwork-proposal` is a Projection Layer Skill registered in `skills/projection-registry/SKILL.md`. It consumes runtime qualification context (`out/<target-slug>/runtime/upwork-qualification.yaml`) and canonical OKF evidence to project client-facing and human-review artifacts:
- `out/<target-slug>/upwork-qualification-report.md` (Clean client-facing proposal draft)
- `out/<target-slug>/upwork-evidence-gaps.md` (Companion Evidence Gap Report & Candidate Confirmation Questions)
- `out/<target-slug>/upwork-screening-answers.md` (Evidence-backed responses to screening questions)
- `out/<target-slug>/upwork-work-samples.md` (Recommended work samples with explicit project type tags)

In V3.1, proposal generation enforces attribution-bounded prose (bounded formulations such as `led architecture`, `shaped architecture`, `aligned teams`), explicit separation of historical experience from proposed architecture, multi-context capability presentation without fact-merging, and zero hardcoded candidate company or project names (FR-063).

## Hard Rules & Decision Behaviors

1. **Candidate-Agnostic Engine (FR-063)**:
   - Proposal generation rules, templates, and prompts MUST NOT hardcode specific employer names, project names, or candidate career-history facts.
   - All organization names, project names, and evidence attributes are consumed dynamically from canonical OKF evidence and qualification runtime context.
2. **Submission Readiness & Human Decision Ownership**:
   - `submission_readiness: SUBMISSION_READY`: All client-facing claims are backed by canonical evidence (`SUPPORTED`).
   - `submission_readiness: HUMAN_REVIEW_REQUIRED`: One or more material requirements are `UNKNOWN` or `PARTIALLY_SUPPORTED`. Indicates machine non-certification while explicitly allowing the human user to choose `user_decision_state: APPLY` and submit after review.
   - `user_decision_state`: Human-controlled enum (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`). The machine MUST NOT force or finalize this value.
3. **Clean Bounded Client-Facing Proposal Prose**:
   - `upwork-qualification-report.md` MUST read as clean, natural professional proposal prose free of visible `[evidence]` tags, `[^source-id]` footnotes, or `[OPEN CONDITION]` banners.
   - Prose MUST match upstream attribution context (`candidate_contribution` = `architected` $\rightarrow$ "led architecture", "shaped strategy"; `implemented` $\rightarrow$ "built", "implemented").
   - **No Assertion-Then-Disclaimer Pattern (FR-049)**: The system MUST NOT generate an affirmative historical claim followed by a disclaimer (e.g. "I architected the production platform. Live deployment is unknown"). The primary claim itself MUST be bounded upfront.
4. **Historical vs. Proposed Architecture Separation (FR-042, FR-043)**:
   - Historical experience (what candidate did) and proposed architecture (what candidate recommends) MUST remain distinct.
   - Technologies specified in proposed solutions (e.g., LangGraph, OpenAI Agents SDK, Temporal) MUST be framed with prospective modal verbs ("would deploy", "propose to implement") and MUST NOT be represented as past historical implementations without independent evidence.
5. **Cross-Source Composition & Multi-Context Presentation (FR-039, FR-040)**:
   - Complementary evidence from separate contexts MAY be presented together to demonstrate multi-domain capability, but MUST NOT be merged into a single composite historical fact for a specific requirement.
6. **Screening Answers Rules (FR-047, FR-048)**:
   - Answers are derived from 3 independent state axes (`requirement_qualification_status`, `content_generation_safety`, `user_decision_state`).
   - For `PARTIALLY_SUPPORTED` or `UNKNOWN` facts, answers MUST NOT assert the fact affirmatively, emitting instead bounded formulations with precision candidate confirmation questions targeting the specific missing implementation fact.
7. **Work Samples Rules (FR-050, FR-051)**:
   - Recommend up to 3 evidence-backed work samples.
   - Retain explicit project type tags (`personal_project`, `prototype_innovation`, `client_production`).
   - Work sample narrative MUST align with metadata (`project_type`, `candidate_contribution`, `demonstrated_capability`).

## Generated Artifact Formats

### 1. Proposal Artifact (`out/<target-slug>/upwork-qualification-report.md`)

```markdown
# Upwork Proposal: [Target Opportunity Title]

**Submission Readiness**: `SUBMISSION_READY` | `HUMAN_REVIEW_REQUIRED`
**Machine Recommendation**: `STRONG_FIT` | `POTENTIAL_FIT` | `EVIDENCE_GAPS` | `WEAK_FIT` | `CLEAR_MISMATCH`
**User Decision State**: `APPLY` | `DO_NOT_APPLY` | `HOLD_FOR_EVIDENCE` (Human-Owned)
**Proposal Content Mode**: `EVIDENCE_BACKED` | `EVIDENCE_SAFE_BOUNDED` | `HUMAN_REVIEW_REQUIRED`
**Word Count**: [Actual Word Count] (Target: 350-500 words)

---

[Render 6-Part Clean Executive Proposal]
1. Opening & Problem Understanding
2. Requirement-to-Proof Mapping (2-4 key matches, using bounded attribution phrasing)
3. Project Snapshots (Context → Action → Operational/Business Relevance, max 3)
4. Proposed Approach (Process → Systems → Automation Candidates → AI vs Deterministic → Controls → Validation; prospective modal verbs for proposed stack)
5. Smart Questions (3-5 strategic questions)
6. Call to Action (Scoping discussion invitation)
```

### 2. Evidence Gap Report (`out/<target-slug>/upwork-evidence-gaps.md`)

```markdown
# Upwork Evidence Gap Report: [Target Opportunity Title]

**Submission Readiness**: `HUMAN_REVIEW_REQUIRED`
**Machine Recommendation**: `EVIDENCE_GAPS`

## Requirement Evidence Gaps

### 1. [Requirement Text]
- **Status**: `UNKNOWN` | `PARTIALLY_SUPPORTED` | `CONTRADICTED`
- **Established Facts**: [Facts supported by canonical evidence]
- **Missing Facts**: [Specific facts not established in canonical evidence]
- **Candidate Confirmation Question**: [Target confirmation question for candidate review]
```

### 3. Screening Answers (`out/<target-slug>/upwork-screening-answers.md`)

```markdown
# Upwork Screening Answers: [Target Opportunity Title]

## Question 1: [Client Question Text]
**Status**: `ANSWERED` | `EVIDENCE_SAFE_QUALIFIED` | `[OPEN CONDITION: <fact>]`
**Answer**: Direct evidence-backed response, leading with verified facts and bounded attribution without fabrication.
```

### 4. Work Samples (`out/<target-slug>/upwork-work-samples.md`)

```markdown
# Recommended Work Samples: [Target Opportunity Title]

## 1. [Sample Title]
- **Project Type**: `client_production` | `prototype_innovation` | `personal_project`
- **Supports Requirement**: [Requirement text]
- **Demonstrated Capability**: [Capability text]
- **Evidence Source**: [card-id]
- **Summary**: Approved external description.
```

## Execution Instructions

1. **Read Qualification Runtime Context**: Load `out/<target-slug>/runtime/upwork-qualification.yaml`.
2. **Render Clean Client Proposal Prose (`upwork-qualification-report.md`)**:
   - Include V3.1 metadata header.
   - Render clean proposal prose (350-500 words) using `SUPPORTED` evidence and qualifying `PARTIALLY_SUPPORTED` requirements with bounded attribution phrasing.
   - Use prospective modal verbs ("would", "propose to") for proposed solution technologies.
3. **Render Companion Evidence Gap Report (`upwork-evidence-gaps.md`)**:
   - If material gaps exist (`UNKNOWN` or `PARTIALLY_SUPPORTED`), render detailed gap report and target candidate confirmation questions.
4. **Render Screening Answers (`upwork-screening-answers.md`)**:
   - Produce evidence-safe responses derived from qualification state axes without fabricated metrics or unevidenced historical assertions.
5. **Render Work Samples (`upwork-work-samples.md`)**:
   - Recommend up to 3 work samples with explicit project type tags aligned with production metadata.
