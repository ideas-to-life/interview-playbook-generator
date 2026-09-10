---
name: upwork-proposal-generator
description: Generates a copy/paste-ready Upwork proposal, screening answers, and work-sample recommendations from a qualified opportunity and canonical evidence.
---

# Upwork Proposal Generator

## Purpose

Projection Skill for Upwork applications. It converts a qualified opportunity into a concise application package while preserving evidence integrity.

Outputs:
- `out/<target-slug>/upwork-proposal.md`
- `out/<target-slug>/upwork-screening-answers.md`
- `out/<target-slug>/upwork-work-samples.md`

This Skill is manual-first. It does not browse, scrape, submit, message, boost, or automate browser actions on Upwork.

## Hard Rules

```
NEVER FABRICATE:
- Projects, metrics, clients, production status
- Technologies, responsibilities, outcomes, scope or ownership
```

1. Read `out/<target-slug>/runtime/upwork-qualification.yaml` first.
2. `DO NOT APPLY` means no submission-ready proposal. Produce a gate report instead.
3. `CONDITIONAL` may produce a draft only when no unsupported factual claim is required; mark the open condition clearly.
4. `APPLY` produces a submission-ready proposal.
5. Never convert `adjacent`, `transferable`, or `unknown` evidence into direct experience.
6. Never claim production usage unless canonical evidence establishes it.
7. Never claim a client technology merely because it appears in the job description.
8. Re-running the Skill replaces its own output files.

## Inputs

Read:
1. `config/config.yaml`
2. `target_opportunity.source`
3. `out/<target-slug>/runtime/opportunity-analysis.yaml`
4. `out/<target-slug>/runtime/upwork-qualification.yaml`
5. Relevant canonical OKF evidence, prioritising evidence cards, stories, signature achievements, capabilities, executive identity and messaging library.
6. Any target-specific evidence referenced by qualification.

## Main proposal

Before drafting:
1. Identify the client's 2–3 strongest buying signals.
2. Identify the candidate's 2–3 strongest direct evidence matches.
3. Identify hard screening questions.
4. Select only claims whose ownership, scope, technology and production status are supported.
5. Select up to three evidence-backed work samples.

Target approximately 350–500 words unless the client requires otherwise.

Structure:
1. **Opening** — first two lines demonstrate understanding of the client's problem.
2. **Requirement-to-proof mapping** — 2–4 strongest matches with concrete evidence.
3. **Project snapshots** — no more than three concise examples.
4. **Approach** — process → systems/data → automation vs AI vs human → architecture/integration → build → validation → scale.
5. **Smart questions** — 3–5 useful discovery questions.
6. **CTA** — propose starting with one concrete process or problem.

## Screening answers

Answer every client application question directly. Answer first, then give evidence. State limitations where relevant. Never substitute personal projects for real-company production experience when the client explicitly requires production experience.

## Work samples

Recommend up to three attachments. For each provide the sample, supported requirement, demonstrated capability and evidence/source. Do not recommend confidential internal material unless already approved for external use.

## Positioning

Position Alexandre as an Enterprise Architect & AI Transformation Advisor who can understand the business problem, determine what should and should not be automated, design the appropriate architecture, and then go hands-on to build and validate the solution.

Use seniority through specificity, not biography. Avoid generic enthusiasm, buzzword stacking, long career history, unsupported claims, invented metrics, or pretending to be a low-code specialist when the evidence supports custom/API engineering.

## Output: `upwork-proposal.md`

For `APPLY`, output only the copy/paste-ready proposal body.

For `CONDITIONAL`, output a clearly labelled draft followed by an `OPEN CONDITION` section listing the exact fact that must be confirmed.

For `DO NOT APPLY`, output:

```markdown
# Upwork Application Gate

**Decision:** DO NOT APPLY

## Blocking requirement

<client requirement>

## Evidence gap

<what the canonical evidence establishes and why it does not satisfy the requirement>

## What would change the decision

<specific evidence needed, if any>
```

## Output: `upwork-screening-answers.md`

```markdown
# Upwork Screening Answers

## 1. <question>
<answer>

## 2. <question>
<answer>
```

If `DO NOT APPLY`, state that screening answers were not generated because the application is blocked by an explicit requirement.

## Output: `upwork-work-samples.md`

```markdown
# Recommended Upwork Work Samples

1. **<sample>**
   - Supports: <requirement>
   - Demonstrates: <capability>
   - Source: <evidence/source>
```

Only include samples supported by qualification evidence.

## Marketplace boundary

The Skill ends at human review. Upwork actions remain user-controlled through an approved interface.

## Completion

Append a concise entry to `okf/log.md` if that logging convention is active.
