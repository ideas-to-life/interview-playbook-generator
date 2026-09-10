# Qualification Skill Contract: `upwork-qualification`

## Purpose
The `upwork-qualification` Skill is a Runtime Layer Skill responsible for evaluating an Upwork target opportunity against canonical OKF evidence to produce a deterministic qualification decision and explicit `proposal_generation` control state.

## Inputs
- **Target Opportunity Analysis**: `out/<target-slug>/runtime/opportunity-analysis.yaml`
- **Canonical Evidence**: `out/okf/evidence-cards/`, `out/okf/signature-achievements.md`, `out/okf/capabilities/`
- **Target Config**: `config/config.yaml` or target position metadata (`target_type: upwork`)

## Output
- **Qualification Artifact**: `out/<target-slug>/runtime/upwork-qualification.yaml`

## Behavior Rules
1. **Hard Requirements Check**: Scan all explicit client hard requirements in `opportunity-analysis.yaml`.
2. **Evidence Relationship Mapping**: Assign relationship (`direct`, `adjacent`, `transferable`, `absent`) and production status (`verified_production`, `verified_non_production`, `unknown`).
3. **Decision Evaluation & Control Semantics**:
   - `DO NOT APPLY` (`proposal_generation: blocked`): If any hard requirement is `absent`, unsupported, or requires treating non-production work as client production implementation.
   - `CONDITIONAL` (`proposal_generation: allowed_with_conditions`): If hard requirements are met except for unverified facts that candidate can confirm.
   - `APPLY` (`proposal_generation: allowed`): If all hard requirements are supported by verified evidence.
4. **Claim Traceability**: Write `claim_traceability` mapping each claim line to its evidence ID and source.
5. **No Proposal Writing**: `upwork-qualification` MUST NOT write proposal prose or markdown text files.
