# Proposal Projection Skill Contract: `upwork-proposal`

## Purpose
The `upwork-proposal` Skill is a Projection Layer Skill registered in `skills/projection-registry/SKILL.md`. It generates tailored Upwork proposals, screening answers, and work sample recommendations.

## Inputs
- **Qualification Result**: `out/<target-slug>/runtime/upwork-qualification.yaml`
- **Target Opportunity Analysis**: `out/<target-slug>/runtime/opportunity-analysis.yaml`
- **Canonical Knowledge**: `out/okf/` (Evidence Cards, Executive Identity, Narrative Library, Story Library)

## Outputs
- `out/<target-slug>/upwork-qualification-report.md` (Clean prose ready for submission)
- `out/<target-slug>/upwork-screening-answers.md`
- `out/<target-slug>/upwork-work-samples.md`

## Behavior Rules by Decision State
1. **`DO NOT APPLY` State (`proposal_generation: blocked`)**:
   - `upwork-qualification-report.md` MUST NOT contain a submission-ready application proposal.
   - It MUST contain a concise Gate Report listing: Decision (`DO NOT APPLY`), Blocking Requirement(s), Available Evidence, Evidence Gap, and What Would Change Decision.
   - `upwork-screening-answers.md` MUST NOT be generated as an application draft.
2. **`CONDITIONAL` State (`proposal_generation: allowed_with_conditions`)**:
   - `upwork-qualification-report.md` may render a draft proposal provided unsupported claims are excluded.
   - It MUST display an `[OPEN CONDITION: <fact>]` banner at the top listing the exact facts requiring candidate confirmation.
   - `upwork-screening-answers.md` MUST attach `[OPEN CONDITION: <fact>]` tags to any answer relying on unverified context.
3. **`APPLY` State (`proposal_generation: allowed`)**:
   - Renders submission-ready `upwork-qualification-report.md` (350-500 words target) as clean, natural professional prose (no `[evidence]` tags or `[^source-id]` footnotes in visible proposal text).
   - Traceability metadata is maintained in `upwork-qualification.yaml` and frontmatter.

## Projection Registry Interface
`upwork-proposal` satisfies the standard Projection Contract:
```yaml
name: "upwork-proposal"
layer: "projection"
target_type: "upwork"
active_if: "target_type == 'upwork'"
outputs:
  - "upwork-qualification-report.md"
  - "upwork-screening-answers.md"
  - "upwork-work-samples.md"
```
