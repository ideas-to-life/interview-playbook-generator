# Proposal Projection Skill Contract: `upwork-proposal` (V2.0)

## Overview

`upwork-proposal` is a Projection Layer Skill registered in `skills/projection-registry/SKILL.md`. It reads runtime qualification context (`out/<target-slug>/runtime/upwork-qualification.yaml`) and canonical OKF evidence to project client-facing artifacts in `out/<target-slug>/`:
- `out/<target-slug>/upwork-proposal.md`
- `out/<target-slug>/upwork-screening-answers.md`
- `out/<target-slug>/upwork-work-samples.md`

---

## Control Boundary Semantics

1. **`proposal_generation: blocked` (`DO NOT APPLY`)**:
   - MUST NOT render a submission-ready application proposal.
   - MUST render a concise **Gate Report** in `upwork-proposal.md` displaying: Decision (`DO NOT APPLY`), Blocking Requirement, Available Evidence, Evidence Gap, Decision Rationale, and What Would Change Decision.
   - MUST NOT render application drafts for `upwork-screening-answers.md`.

2. **`proposal_generation: allowed_with_conditions` (`CONDITIONAL`)**:
   - Renders a proposal draft with a prominent `[OPEN CONDITION: <fact>]` banner listing facts requiring candidate confirmation.
   - Attaches explicit `[OPEN CONDITION: <fact>]` tags to affected screening answers.

3. **`proposal_generation: allowed` (`APPLY`)**:
   - Renders submission-ready 6-part proposal (350-500 words target).
   - Proposal text is rendered clean of visible `[evidence]` tags or `[^source-id]` footnotes for direct Upwork submission.
   - Machine-readable traceability maintained in `upwork-qualification.yaml` `claim_traceability` array.

---

## Work Samples Selection Boundary

Recommends up to 3 work samples. Work samples MUST match qualification status and MUST NOT describe prototype, lab, or personal projects as production experience.
