---
name: upwork-proposal
description: Generates clean executive proposal prose, screening answers, and work sample recommendations in out/<target-slug>/ based on upwork-qualification runtime context.
---

# Upwork Proposal Projection

## Overview

`upwork-proposal` is a Projection Layer Skill registered in `skills/projection-registry/SKILL.md`. It consumes runtime qualification context (`out/<target-slug>/runtime/upwork-qualification.yaml`) and canonical OKF evidence to project client-facing artifacts:
- `out/<target-slug>/upwork-proposal.md`
- `out/<target-slug>/upwork-screening-answers.md`
- `out/<target-slug>/upwork-work-samples.md`

## Hard Rules & Decision Behaviors

1. **Gate Compliance (`proposal_generation`)**:
   - `proposal_generation: blocked` (`DO NOT APPLY`):
     - `upwork-proposal.md` MUST NOT contain a submission-ready application proposal.
     - `upwork-proposal.md` MUST render a concise **Gate Report** displaying: Decision (`DO NOT APPLY`), Blocking Requirement(s), Available Evidence, Evidence Gap, Decision Rationale, and What Would Change Decision.
     - `upwork-screening-answers.md` MUST NOT be generated as an application draft.
   - `proposal_generation: allowed_with_conditions` (`CONDITIONAL`):
     - `upwork-proposal.md` renders a proposal draft with a prominent `[OPEN CONDITION: <fact>]` banner listing facts requiring candidate confirmation.
     - `upwork-screening-answers.md` attaches explicit `[OPEN CONDITION: <fact>]` tags to affected questions.
   - `proposal_generation: allowed` (`APPLY`):
     - Renders submission-ready `upwork-proposal.md` (350-500 words target).
2. **Clean Client-Facing Proposal Prose**:
   - `upwork-proposal.md` MUST read as clean, natural professional proposal prose free of visible `[evidence]` tags or `[^source-id]` footnotes in the output text, making it directly copy-pasteable into Upwork.
   - Traceability metadata is maintained in `upwork-qualification.yaml` `claim_traceability` array for validation by `projection-validator`.
3. **Screening Answers Rules**:
   - Answer every client question directly first, followed by supporting evidence proof.
   - Never substitute personal projects for required client production experience.
   - Never manufacture metrics or counts.
4. **Work Samples Rules**:
   - Recommend up to 3 evidence-backed work samples.
   - Confidential internal material MUST NOT be recommended for external submission.

## Generated Artifact Formats

### 1. Proposal Artifact (`out/<target-slug>/upwork-proposal.md`)

```markdown
# Upwork Proposal: [Target Opportunity Title]

**Qualification Status**: `APPLY` | `CONDITIONAL` | `DO NOT APPLY`
**Proposal Control State**: `allowed` | `allowed_with_conditions` | `blocked`
**Word Count**: [Actual Word Count] (Target: 350-500 words)

[If CONDITIONAL: Display Open Conditions Banner]
[If DO NOT APPLY: Render Gate Report]

[If APPLY: Render 6-Part Clean Executive Proposal]
1. Opening & Problem Understanding
2. Requirement-to-Proof Mapping (2-4 key matches)
3. Project Snapshots (Context → Action → Operational/Business Relevance, max 3)
4. Proposed Approach (Process → Systems → Automation Candidates → AI vs Deterministic → Controls → Validation)
5. Smart Questions (3-5 strategic questions)
6. Call to Action (Scoping discussion invitation)
```

### 2. Screening Answers (`out/<target-slug>/upwork-screening-answers.md`)

```markdown
# Upwork Screening Answers: [Target Opportunity Title]

## Question 1: [Client Question Text]
**Status**: `ANSWERED` | `[OPEN CONDITION: <fact>]`
**Answer**: Direct answer leading with clear response, followed by evidence proof.
```

### 3. Work Samples (`out/<target-slug>/upwork-work-samples.md`)

```markdown
# Recommended Work Samples: [Target Opportunity Title]

## 1. [Sample Title]
- **Supports Requirement**: [Requirement text]
- **Demonstrated Capability**: [Capability text]
- **Evidence Source**: [card-id]
- **Summary**: Approved external description.
```

## Execution Instructions

1. **Read Qualification Runtime Context**: Load `out/<target-slug>/runtime/upwork-qualification.yaml` and check `proposal_generation` control state.
2. **Handle `proposal_generation: blocked`**: Generate Gate Report in `upwork-proposal.md` and exit.
3. **Handle `proposal_generation: allowed_with_conditions` / `allowed`**:
   - Render `upwork-proposal.md` (clean prose, 350-500 words target).
   - Render `upwork-screening-answers.md` for all screening questions.
   - Render `upwork-work-samples.md` recommending up to 3 work samples.
