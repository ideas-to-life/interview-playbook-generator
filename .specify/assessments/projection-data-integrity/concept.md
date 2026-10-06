# Concept: Projection Data Integrity & Provenance Remediation

- **Slug**: projection-data-integrity
- **Created**: 2026-09-24
- **Recommended option**: Option B — Structural Pipeline Boundary & Generalized Deterministic Enforcement

## Options

### Option A — Lightweight Forensic Regressor Patching
- **Sketch**: Add targeted negative checks to `canonical_validator.py` and `employment_validator.py` for known forensic regressors (Workday, NetSuite, Coupa, Concur, BSc 1995–1999, Spanish Fluent, AWS/Sun certifications), combined with added negative prompt instructions across projection skills.
- **Appetite**: small (2–4 days)
- **Trade-offs**: Fast to deliver with zero structural changes to the pipeline; but treats symptoms rather than root causes, violates NFR-03 (No hard-coded forensic-only fixes), and leaves future runs vulnerable whenever new technologies or opportunities appear.
- **Rabbit holes**: Ongoing manual blacklist maintenance as new client tech stacks trigger new hallucinations.

### Option B — Structural Pipeline Boundary & Generalized Deterministic Enforcement
- **Sketch**: Implement the 5-tier information boundary specified in the post-canonical refinement spec: guarantee 100% loading of `canonical-selection.yaml` into projection contexts; isolate opportunity runs by replacing references to prior runs with synthetic/fact-free structural templates; partition ATS vocabulary into target-required versus candidate-evidenced sets so density scoring rewards only verified experience; and expand deterministic post-generation validation across education, certifications, language levels, and named platform experience claims.
- **Appetite**: medium (2–3 weeks)
- **Trade-offs**: Solves all four forensic defect classes at the architectural layer, enforces permanent invariants, and generalizes across all future roles. Requires coordinated touchpoints across runtime context loading, prompt contracts, ATS scoring formulas, validation scripts, and regression tests.
- **Rabbit holes**: Over-engineering technology taxonomies (trying to model all enterprise IT ontology instead of validating claims against canonical evidence).

### Option C — Strict Schema-Constrained AST Projection Engine
- **Sketch**: Replace free-form markdown projection generation with a rigid AST-based compiler. Projections are generated as strictly typed JSON/YAML documents where factual slots (roles, dates, degrees, certifications) are bound programmatically to canonical records, restricting LLM generation exclusively to narrative bullet formulation.
- **Appetite**: large (6–8 weeks)
- **Trade-offs**: Mathematically eliminates factual hallucination by design; but requires an architectural rewrite of all projection skills, introduces brittle document schema maintenance, and compromises executive narrative fluidity and custom layout tailoring.
- **Rabbit holes**: Attempting to model every unique resume layout, multi-role promotion structure, and executive collateral nuance into rigid typed schemas.

## Recommendation

**Option B (Structural Pipeline Boundary & Generalized Deterministic Enforcement)** is strongly recommended.

It resolves the four forensic failure modes at their root causes without resorting to brittle keyword blacklists (Option A) or locking the platform into an inflexible schema compiler (Option C). It fulfills all 20 Functional Requirements (FR-01 through FR-20) and aligns with the core platform invariant: *The generator may select, transform, and present candidate evidence; it may not redefine candidate evidence.*

## Out of Scope (for the recommended option)

- Rebuilding the canonical career record (`mind-palace/canonical/career-record.yaml`) or reconstructing the underlying mind palace.
- Constructing an exhaustive universal taxonomy of all enterprise technologies and software systems.
- Introducing non-deterministic LLM-as-judge adjudicators as primary factual validators.
- Redesigning visual themes, typographic styling, or resume layout aesthetics.

## Assumptions to Validate

- Complete `canonical-selection.yaml` files (including all education, certification, and language sections) can be passed directly into projection contexts without degrading model reasoning or exceeding practical token limits.
- Target JD vocabulary can be deterministically partitioned into "candidate-evidenced" and "target-required" subsets using canonical facts and OKF capability mappings.
- Deterministic regex/AST parsers can accurately extract education, certifications, languages, and platform claims from generated Markdown collateral for automated auditing.
