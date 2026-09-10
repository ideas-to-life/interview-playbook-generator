---
name: upwork-proposal
description: Generates clean executive proposal prose, companion evidence gap reports, screening answers, and work sample recommendations in out/<target-slug>/ based on upwork-qualification runtime context.
---

# Upwork Proposal Projection (V2.1)

## Overview

`upwork-proposal` is a Projection Layer Skill registered in `skills/projection-registry/SKILL.md`. It consumes runtime qualification context (`out/<target-slug>/runtime/upwork-qualification.yaml`) and canonical OKF evidence to project client-facing and human-review artifacts:
- `out/<target-slug>/upwork-qualification-report.md` (Clean client-facing proposal draft)
- `out/<target-slug>/upwork-evidence-gaps.md` (Companion Evidence Gap Report & Candidate Confirmation Questions)
- `out/<target-slug>/upwork-screening-answers.md` (Evidence-backed responses to screening questions)
- `out/<target-slug>/upwork-work-samples.md` (Recommended work samples with explicit project type tags)

## Hard Rules & Decision Behaviors

1. **Submission Readiness & Human Decision Ownership**:
   - `submission_readiness: SUBMISSION_READY`: All client-facing claims are backed by canonical evidence (`SUPPORTED`).
   - `submission_readiness: HUMAN_REVIEW_REQUIRED`: One or more material requirements are `UNKNOWN` or `PARTIALLY_SUPPORTED`. Indicates machine non-certification while explicitly allowing the human user to choose `user_decision_state: APPLY` and submit after review.
   - `user_decision_state`: Human-controlled enum (`APPLY`, `DO_NOT_APPLY`, `HOLD_FOR_EVIDENCE`). The machine MUST NOT force or finalize this value.
2. **Clean Client-Facing Proposal Prose**:
   - `upwork-qualification-report.md` MUST read as clean, natural professional proposal prose free of visible `[evidence]` tags, `[^source-id]` footnotes, or `[OPEN CONDITION]` banners in the text meant for client submission.
   - For `PARTIALLY_SUPPORTED` requirements, proposal prose MAY include verified, evidence-backed aspects while explicitly omitting or qualifying unsupported aspects. Unsupported aspects MUST NEVER be asserted as established fact.
   - Claim traceability metadata is maintained in `upwork-qualification.yaml` `claim_traceability` array for automated validation by `projection-validator`.
3. **Companion Evidence Gap Report (`upwork-evidence-gaps.md`)**:
   - Generated whenever material gaps exist (`UNKNOWN` or `PARTIALLY_SUPPORTED`).
   - Surfaces requirement text, classification, established facts, missing facts, impact assessment, and explicit candidate confirmation questions.
4. **Screening Answers Rules**:
   - Answer every client question directly first, followed by supporting evidence proof.
   - Unresolved questions MUST NOT fabricate yes/no answers or invented metrics. They emit evidence-safe qualified answers, internal `[OPEN CONDITION: ...]` markers, or candidate review items.
   - Never substitute personal projects or prototypes for required client production experience.
5. **Work Samples Rules**:
   - Recommend up to 3 evidence-backed work samples.
   - Retain explicit project type tags (`personal_project`, `prototype_innovation`, `client_production`).
   - Personal projects and prototype/innovation work MUST remain explicitly identified as such.
6. **Deterministic Evidence Improvement Loop**:
   - When a candidate updates canonical OKF evidence to resolve a gap and re-runs the pipeline, proposal generation MUST deterministically incorporate the new evidence into proposal prose and upgrade `submission_readiness` to `SUBMISSION_READY` without manual prose editing.

## Generated Artifact Formats

### 1. Proposal Artifact (`out/<target-slug>/upwork-qualification-report.md`)

```markdown
# Upwork Proposal: [Target Opportunity Title]

**Submission Readiness**: `SUBMISSION_READY` | `HUMAN_REVIEW_REQUIRED`
**Machine Recommendation**: `STRONG_FIT` | `POTENTIAL_FIT` | `EVIDENCE_GAPS` | `WEAK_FIT` | `CLEAR_MISMATCH`
**User Decision State**: `APPLY` | `DO_NOT_APPLY` | `HOLD_FOR_EVIDENCE` (Human-Owned)
**Proposal Content Mode**: `EVIDENCE_BACKED` | `EVIDENCE_GAPS` | `HUMAN_REVIEW_REQUIRED`
**Word Count**: [Actual Word Count] (Target: 350-500 words)

---

[Render 6-Part Clean Executive Proposal]
1. Opening & Problem Understanding
2. Requirement-to-Proof Mapping (2-4 key matches)
3. Project Snapshots (Context → Action → Operational/Business Relevance, max 3)
4. Proposed Approach (Process → Systems → Automation Candidates → AI vs Deterministic → Controls → Validation)
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
- **Candidate Confirmation Question**: [Question for human candidate review]
```

### 3. Screening Answers (`out/<target-slug>/upwork-screening-answers.md`)

```markdown
# Upwork Screening Answers: [Target Opportunity Title]

## Question 1: [Client Question Text]
**Status**: `ANSWERED` | `EVIDENCE_SAFE_QUALIFIED` | `[OPEN CONDITION: <fact>]`
**Answer**: Direct evidence-backed response, leading with verified facts without fabrication.
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
   - Include V2.1 metadata header.
   - Render clean proposal prose (350-500 words) using `SUPPORTED` evidence and qualifying `PARTIALLY_SUPPORTED` requirements.
3. **Render Companion Evidence Gap Report (`upwork-evidence-gaps.md`)**:
   - If material gaps exist (`UNKNOWN` or `PARTIALLY_SUPPORTED`), render detailed gap report and candidate confirmation questions.
4. **Render Screening Answers (`upwork-screening-answers.md`)**:
   - Produce evidence-safe responses without fabricated metrics or claims.
5. **Render Work Samples (`upwork-work-samples.md`)**:
   - Recommend up to 3 work samples with explicit project type tags.
