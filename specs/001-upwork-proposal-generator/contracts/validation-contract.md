# Validation Contract: Upwork Evaluation Extension

## Purpose
Specifies the validation contract implemented by `skills/projection-validator/SKILL.md` when validating Upwork projection outputs.

## Evaluated Artifacts
- `out/<target-slug>/upwork-proposal.md`
- `out/<target-slug>/upwork-screening-answers.md`
- `out/<target-slug>/runtime/upwork-qualification.yaml`

## Verification Checks
1. **Zero Fabrication & Internal Provenance Pass**:
   - Inspect `out/<target-slug>/runtime/upwork-qualification.yaml` `claim_traceability` array to verify that 100% of claims in `upwork-proposal.md` link to valid canonical evidence cards (`[^source-id]`).
   - Confirm client-facing `upwork-proposal.md` contains zero unparsed internal metadata tags (`[evidence]`, `[inference]`).
2. **Word Count Compliance**:
   - For `APPLY` status proposals, word count must be within configured bounds (default 350-500 words).
3. **DO NOT APPLY Enforcement**:
   - If `upwork-qualification.yaml` decision is `DO NOT APPLY` (`proposal_generation: blocked`), `upwork-proposal.md` must contain the Gate Report header and zero submission-ready application text.
4. **CONDITIONAL Tag Enforcement**:
   - If `upwork-qualification.yaml` decision is `CONDITIONAL` (`proposal_generation: allowed_with_conditions`), `upwork-proposal.md` and `upwork-screening-answers.md` must include explicit `[OPEN CONDITION: ...]` tags for unverified items.
5. **Output Target**:
   - Validation metrics appended to `out/<target-slug>/runtime/projection-validation-report.yaml`.
