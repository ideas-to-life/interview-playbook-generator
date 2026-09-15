# Upwork Qualification Skill Contract (V2.1)

**Skill Name**: `upwork-qualification`  
**Layer**: Runtime Layer  
**Input Requirements**:
- `out/<target-slug>/runtime/opportunity-analysis.yaml`
- `out/okf/` canonical knowledge graph

**Output Path**: `out/<target-slug>/runtime/upwork-qualification.yaml`

## Execution Protocol

1. Read opportunity analysis and canonical evidence nodes.
2. Evaluate each client requirement against canonical evidence and classify into: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNKNOWN`, `CONTRADICTED`.
3. Identify missing facts and construct candidate confirmation questions for `UNKNOWN` or `PARTIALLY_SUPPORTED` requirements.
4. Calculate machine recommendation (`STRONG_FIT`, `POTENTIAL_FIT`, `EVIDENCE_GAPS`, `WEAK_FIT`, `CLEAR_MISMATCH`).
5. Determine proposal content mode (`EVIDENCE_BACKED`, `EVIDENCE_GAPS`, `HUMAN_REVIEW_REQUIRED`) and submission readiness (`SUBMISSION_READY`, `HUMAN_REVIEW_REQUIRED`).
6. Write structured output YAML without generating client prose files.
