# Upwork Validation Contract (V2.1)

**Skill Name**: `projection-validator` (Upwork Extension)  
**Layer**: Evaluation Layer  
**Input Requirements**:
- `out/<target-slug>/` generated Upwork proposal artifacts
- `out/<target-slug>/runtime/upwork-qualification.yaml`

**Output Path**: `out/<target-slug>/runtime/projection-validation-report.yaml`

## Automated Validation Checks

1. **Zero Fabrication Pass**: Verify that no unverified claim, metric, production assertion, or technology present in client prose lacks entry in `claim_traceability` or canonical evidence.
2. **Clean Text Pass**: Verify zero leakage of internal footnote tags (`[^...]`), evidence classification tags (`[evidence]`), or `[OPEN CONDITION]` diagnostic markers into `upwork-qualification-report.md`.
3. **Contradiction Pass**: Verify that no requirement classified as `CONTRADICTED` is presented as met in client-facing prose.
4. **Readiness Alignment Pass**: Verify that if any material requirement is `UNKNOWN` or `PARTIALLY_SUPPORTED`, `submission_readiness` in `upwork-qualification.yaml` and header in `upwork-qualification-report.md` are set to `HUMAN_REVIEW_REQUIRED`.
