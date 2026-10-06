# Decision: Projection Data Integrity & Provenance Remediation

- **Slug**: projection-data-integrity
- **Decided**: 2026-09-24
- **Verdict**: go
- **Artifacts reviewed**: intake.md | problem.md | concept.md | `docs/requirements-spec/refinement-spec-post-canonical-record-integration.v1.md`

## Scorecard

| Criterion | Rating | Justification |
|-----------|--------|---------------|
| Problem validity | strong | The September 2026 diagnostic demonstrated reproducible, critical integrity defects where unevidenced target platforms and mutated credentials were generated in executive collateral. |
| Evidence strength | strong | Supported by an exhaustive forensic diagnostic and a 972-line requirements specification with concrete failing cases (Tenth AI and LSEG runs). |
| Value vs. inaction | strong | Inaction risks disqualification in executive hiring processes, failed background checks, and destroys the platform's core "Never Fabricate" guarantee. |
| Feasibility / appetite | strong | Option B is scoped to a 2–3 week medium appetite, building systematically upon existing canonical loaders, selectors, and validators. |
| Strategic fit | strong | Directly upholds foundational project governance: Canonical Career Record Precedence, Identity Preservation Invariant, and Target Requirements != Candidate Evidence. |
| Risk posture | strong | Critical risks (such as over-engineering tech taxonomies or breaking valid narrative tailoring) are identified and mitigated through clear scope boundaries and deterministic validators. |

## Verdict & Rationale

**Verdict: GO**

The evidence base and requirements for this remediation are exceptionally strong and mature. The integrity defects identified in the diagnostic (partial canonical context loading, cross-opportunity artifact leakage, unevidenced platform claiming driven by ATS keyword scoring, and incomplete post-generation validation) pose an existential risk to the platform's credibility. Option B (Structural Pipeline Boundary & Generalized Deterministic Enforcement) provides a balanced, robust architecture that permanently eliminates these failure modes while preserving legitimate executive tailoring and transferable skills presentation.

## If go — Handoff to `/speckit-specify`

- **Problem**: Executive projection generation produces credential hallucinations, platform experience fabrication, and cross-run data contamination when target job keywords and historical opportunity outputs leak into candidate claims.
- **Chosen approach**: Option B — Structural Pipeline Boundary & Generalized Deterministic Enforcement (5-tier information boundary, complete canonical-selection context injection, fact-free synthetic structural templates, evidence-partitioned ATS scoring, and deterministic post-generation validation across education, certifications, languages, and unevidenced platform claims).
- **In scope / out of scope**:
  - *In scope*: Full loading of `canonical-selection.yaml` into projection contexts; complete cross-opportunity runtime isolation; partitioning ATS vocabulary into target-required vs. candidate-evidenced sets; deterministic post-generation validation covering education (dates/degrees), certifications, languages, employment facts, and unevidenced named platforms; 10 deterministic regression scenarios.
  - *Out of scope*: Rebuilding the canonical career record (`career-record.yaml`); building an exhaustive universal IT taxonomy; non-deterministic LLM-as-judge validators; visual styling or layout overhauls.
- **Success metrics**:
  - 0% occurrence of unverified certifications, altered academic dates, or inflated language proficiencies.
  - 0 unevidenced platform claims (e.g. Workday, NetSuite, Coupa, Concur) generated as candidate experience.
  - 0 cross-opportunity factual data leaks.
  - 100% deterministic pass rate across all 10 forensic regression scenarios.
- **Carried-forward open questions**:
  - How should deterministic projection factual validation be unified across `canonical_validator.py`, `employment_validator.py`, and `projection-validator` without duplicate reporting?
  - What canonical baseline or whitelist representation will define "supported named technologies" to avoid false positives on transferable skills?
  - How will ATS scoring in `opportunity-analyzer` and `projection-validator` balance keyword coverage penalties for unevidenced terms against rewards for transferable architecture capabilities?
  - Where will synthetic fact-free structural templates reside, and how will projection skill prompts be refactored to eliminate references to historical opportunity outputs?
