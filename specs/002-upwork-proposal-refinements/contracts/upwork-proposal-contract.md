# Upwork Proposal Projection Contract (V2.1)

**Skill Name**: `upwork-proposal`  
**Layer**: Projection Layer  
**Input Requirements**:
- `out/<target-slug>/runtime/upwork-qualification.yaml`
- `out/okf/` canonical knowledge graph

**Output Artifacts**:
- `out/<target-slug>/upwork-qualification-report.md` (Clean client-facing proposal prose)
- `out/<target-slug>/upwork-evidence-gaps.md` (Companion evidence gap report & candidate confirmation questions)
- `out/<target-slug>/upwork-screening-answers.md` (Evidence-backed responses to screening questions)
- `out/<target-slug>/upwork-work-samples.md` (Up to 3 recommended work samples with project type tags)

## Projection Rules

1. **Clean Client Prose**: Proposal prose (`upwork-qualification-report.md`) MUST be free of internal tags, footnotes, or diagnostic markers.
2. **Partially Supported Handling**: Proposal prose MAY include the verified, evidence-backed aspects of `PARTIALLY_SUPPORTED` requirements while omitting or explicitly qualifying unsupported aspects. Unsupported aspects MUST NEVER be asserted as established fact.
3. **Screening Answers**: Unresolved screening questions MUST NOT fabricate yes/no answers or invented metrics. They emit evidence-safe qualified answers or candidate review items.
4. **Work Samples**: Recommended work samples MUST be independently evidence-backed and explicitly labeled (e.g. `personal_project`, `prototype_innovation`, `client_production`).
5. **Readiness Header**: Proposal header MUST accurately state submission readiness (`SUBMISSION_READY` vs `HUMAN_REVIEW_REQUIRED`).
