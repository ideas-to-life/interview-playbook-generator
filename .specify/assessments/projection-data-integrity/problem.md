# Problem Definition: Projection Data Integrity & Provenance Remediation

- **Slug**: projection-data-integrity
- **Created**: 2026-09-24
- **Inputs used**: intake.md | `docs/requirements-spec/refinement-spec-post-canonical-record-integration.v1.md`

## Problem Statement

Executive candidate projection generation produces factual hallucinations, qualification inflations, and cross-run data contamination when target job keywords and historical opportunity outputs leak into candidate claims. This compromises the candidate's professional credibility and violates the platform's core invariant that candidate identity and evidence must remain immutable during tailoring.

## Affected Users & Stakeholders

- **Users**: Candidate (Alexandre Franco) — bears acute reputational and career risk if tailored executive collateral (resumes, cover letters, briefs) fabricates credentials, mutates academic dates, inflates proficiencies, or claims unevidenced enterprise platforms during executive vetting and background checks.
- **Stakeholders**: Hiring Executives & Recruiters — require an accurate, verifiable representation of the candidate's actual scope and background, free from artificial keyword stuffing or misleading platform experience claims.
- **Stakeholders**: Pipeline Engineers & AI System Operators — need clear, deterministic enforcement boundaries where invalid candidate claims trigger deterministic validation failures before outputs are presented or utilized.

## Goals

- Eliminate factual fabrication and qualification inflation across all projection outputs (education dates/degrees, certifications, language proficiencies, formal titles, and direct technology claims).
- Prevent target job description requirements and keyword optimization incentives from being transformed into unevidenced candidate experience.
- Enforce strict context isolation so that previous opportunity projections cannot contaminate active or future opportunity generation runs.
- Guarantee that complete canonical selection facts are actively present in generation context, eliminating reliance on model inference for omitted qualifications.
- Provide deterministic, automated post-generation validation that fails definitively upon detecting any contradiction against canonical records.

## Non-Goals

- Rebuilding or replacing the existing canonical career record (`mind-palace/canonical/career-record.yaml`).
- Eliminating legitimate resume tailoring, thematic emphasis, or articulation of transferable architecture capabilities.
- Redesigning visual layouts, typographical styles, or markdown formatting templates.
- Expanding the canonical record into an exhaustive repository of every granular project detail or generic IT concept.

## Success Metrics

- **Zero Credential Hallucinations**: 0% occurrence of unverified certifications (e.g. AWS, Sun SCEA/SCJP), inflated language ratings, or altered education dates in generated projections (baseline: multiple detected in September 2026 diagnostic).
- **Zero Unevidenced Platform Claims**: 0 instances of unevidenced JD platforms (e.g. Workday, NetSuite, Coupa, Concur) claimed as direct candidate experience (baseline: 4 unevidenced platforms claimed in Tenth AI run).
- **Zero Cross-Opportunity Factual Contamination**: 0% data leakage from prior opportunity outputs into new opportunity generation, verified under regression scenarios (baseline: context leakage observed from prior run collateral).
- **100% Deterministic Forensic Pass Rate**: All 10 diagnostic regression scenarios (Scenario 1 through Scenario 10 in the requirements spec) execute deterministically with zero false passes (baseline: unautomated or partially covered by regex rules).

## Cost of Inaction

If left unaddressed, the platform continues to generate collateral that fails background checks, introduces disqualifying credential discrepancies in executive interviews, and fundamentally violates the platform's core operating principle ("Never Fabricate"), rendering the system unusable for high-stakes executive job applications.

## Open Questions

- [NEEDS CLARIFICATION: How should deterministic projection factual validation be structured across existing tools (`canonical_validator.py`, `employment_validator.py`, `projection-validator`) without duplicating parsing or fragmenting error reports?]
- [NEEDS CLARIFICATION: What canonical source or taxonomy will define "supported named technologies" to prevent false positives when candidates mention ubiquitous or transferable tooling?]
- [NEEDS CLARIFICATION: How should the ATS scoring formula in `opportunity-analyzer` / `projection-validator` be adjusted to penalize unevidenced keyword insertion without depressing scores for genuine transferable architecture mapping?]
- [NEEDS CLARIFICATION: Where will synthetic/fact-free structural templates reside, and what migration is needed for skills currently referencing historical projection artifacts?]
