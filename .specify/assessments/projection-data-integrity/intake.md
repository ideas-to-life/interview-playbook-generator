# Idea Intake: Projection Data Integrity & Provenance Remediation

- **Slug**: projection-data-integrity
- **Created**: 2026-09-24
- **Source**: `docs/requirements-spec/refinement-spec-post-canonical-record-integration.v1.md`
- **Type**: fix

## Idea (as captured)

Quoted from [`docs/requirements-spec/refinement-spec-post-canonical-record-integration.v1.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/docs/requirements-spec/refinement-spec-post-canonical-record-integration.v1.md):

> **Purpose:** Remediate the forensic defects identified in the September 2026 projection-data diagnostic  
> **Scope:** Projection generation, runtime context assembly, ATS vocabulary handling, cross-opportunity isolation, and projection validation
>
> The forensic diagnostic of the Tenth AI Lead Enterprise Architect generation established four distinct integrity defects:
>
> 1. Target-job-description keywords can be transformed into unsupported candidate claims through ATS-density optimisation.
> 2. Previous opportunity projections can enter the active generation context and contaminate subsequent projections.
> 3. `canonical-selection.yaml` can be only partially loaded, leaving authoritative candidate facts outside the model context.
> 4. Projection validation does not systematically verify generated candidate facts against canonical facts.
>
> This specification defines the requirements to remediate those defects.
>
> The objective is to establish a reliable information-flow boundary:
>
> ```text
> canonical facts
>       ↓
> canonical selection
>       ↓
> complete candidate context
>       ↓
> evidence-aware opportunity analysis
>       ↓
> projection
>       ↓
> validation
> ```
>
> with the following prohibited flows:
>
> ```text
> previous projection ──X──► candidate facts
> target JD keyword ──X──► candidate capability
> partial canonical selection ──X──► projection
> generated projection ──X──► canonical / knowledge
> ```
>
> Core principle:
> > The generator may select, transform and present candidate evidence. It may not redefine candidate evidence.

## Restated

Establish strict information-flow boundaries, complete canonical context loading, cross-opportunity isolation, and deterministic post-generation validation so that target job keywords and prior projection outputs cannot fabricate, inflate, or mutate candidate facts (education, certifications, language proficiency, employment history, and named technologies).

## Origin & Context

- **Raised by**: Alexandre Franco (Enterprise Architect / Candidate & System Architect)
- **Trigger**: Forensic diagnostic of the `tenth-ai-lead-enterprise-architect` generation run (September 2026), which uncovered title inflation, unevidenced platform experience claims (Workday, NetSuite, Coupa, Concur) driven by ATS keyword scoring, BSc degree graduation date hallucinations, unverified certifications (AWS, Sun SCEA/SCJP), and cross-opportunity contamination from prior runs (e.g. `lseg-director-enterprise-architecture`).

## First-Glance Unknowns

- [NEEDS CLARIFICATION: How should deterministic projection factual validation be structured across existing tools (`canonical_validator.py`, `employment_validator.py`, `projection-validator`) without duplicating parsing or fragmenting error reports?]
- [NEEDS CLARIFICATION: What canonical source or taxonomy will define "supported named technologies" to prevent false positives when candidates mention ubiquitous or transferable tooling?]
- [NEEDS CLARIFICATION: How should the ATS scoring formula in `opportunity-analyzer` / `projection-validator` be adjusted to penalize unevidenced keyword insertion without depressing scores for genuine transferable architecture mapping?]
- [NEEDS CLARIFICATION: Where will synthetic/fact-free structural templates reside, and what migration is needed for skills currently referencing historical projection artifacts?]
