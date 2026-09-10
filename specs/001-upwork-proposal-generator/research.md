# Phase 0 Research: Upwork Qualification and Proposal Generator

## 1. Skill Layout and Architecture Integration

### Decision
Implement two discrete Skills conforming strictly to the repository's 4-layer architecture:
1. `skills/upwork-qualification/SKILL.md` (Runtime Layer): Consumes canonical OKF knowledge and `opportunity-analysis.yaml` to perform qualification evaluation and emit `out/<target-slug>/runtime/upwork-qualification.yaml`.
2. `skills/upwork-proposal/SKILL.md` (Projection Layer): Registered in `skills/projection-registry/SKILL.md`. Consumes qualification results and OKF evidence to project `upwork-proposal.md`, `upwork-screening-answers.md`, and `upwork-work-samples.md`.

### Rationale
- Strictly preserves the architectural boundary between decision (Runtime Layer qualification) and expression (Projection Layer proposal rendering).
- Enables `playbook-orchestrator` to automatically run `upwork-proposal` whenever `target_type: upwork` is set in the target opportunity configuration.

---

## 2. Qualification Taxonomy and Decision Rules

### Decision
Adopt explicit 4-tier requirement mapping and 3-tier evidence classification:
- **Requirement Relationship**: `direct` | `adjacent` | `transferable` | `absent`
- **Evidence Strength**: `strong` | `moderate` | `weak`
- **Production Status**: `verified_production` | `verified_non_production` | `unknown` | `not_applicable`
- **Control Semantics (`proposal_generation`)**:
  - `APPLY` → `proposal_generation: allowed`: All hard requirements satisfied with verified evidence.
  - `CONDITIONAL` → `proposal_generation: allowed_with_conditions`: Unverified facts flagged as open conditions.
  - `DO NOT APPLY` → `proposal_generation: blocked`: Hard requirement absent or requires non-production to production conversion; halts submission proposal generation and renders gate report.

### Rationale
- Enforces Core Principle I (Zero Fabrication) and Core Principle IV (Career History Integrity).
- Prevents personal projects, prototypes, or labs from satisfying explicit client production implementation requirements.

---

## 3. Client-Facing Proposal vs. Internal Provenance Separation

### Decision
Separation of client-facing prose and internal claim provenance:
- **`upwork-proposal.md`**: Rendered as clean, natural professional proposal prose free of visible `[evidence]` tags or `[^source-id]` footnotes, ready for direct copy-pasting into Upwork.
- **`out/<target-slug>/runtime/upwork-qualification.yaml`**: Stores full machine-readable claim traceability (`claim_traceability` array mapping each claim line to its evidence ID, classification, and footnote source).
- **`projection-validator`**: Validates 100% evidence attribution and claim classification by inspecting internal runtime context (`upwork-qualification.yaml`) and frontmatter metadata, rather than requiring visible tags in client-facing text.

### Rationale
- Preserves high-credibility marketplace communication without exposing internal platform tags to external clients.
- Maintains automated governance, zero fabrication enforcement, and strict evidence tracing.

---

## 4. Artifact Storage and File Conventions

### Decision
Store intermediate machine-readable runtime data in `out/<target-slug>/runtime/` and rendered Markdown views in `out/<target-slug>/`:
- `out/<target-slug>/runtime/upwork-qualification.yaml` (YAML format, includes `proposal_generation` and `claim_traceability`)
- `out/<target-slug>/upwork-proposal.md` (Clean Markdown format, 350-500 words target)
- `out/<target-slug>/upwork-screening-answers.md` (Markdown format, direct answers + evidence proof; `[OPEN CONDITION]` tags under CONDITIONAL)
- `out/<target-slug>/upwork-work-samples.md` (Markdown format, max 3 samples)
- `out/<target-slug>/runtime/projection-validation-report.yaml` (Updated by `projection-validator`)

---

## 5. Evaluation and Quality Gate Extension

### Decision
Extend `skills/projection-validator/SKILL.md` to parse and validate `upwork-proposal.md` and `upwork-screening-answers.md`.
Validation rules include:
1. **Internal Provenance & Attribution Pass**: Inspect `upwork-qualification.yaml` to ensure 100% of proposal claims link to valid canonical evidence cards (`[^source-id]`).
2. **Word Count Target**: Verify proposal length stays within requested bounds (default 350-500 words).
3. **Open Condition Verification**: Ensure `CONDITIONAL` artifacts contain explicit `[OPEN CONDITION: <fact>]` tags.
4. **Gate Compliance**: Verify `DO NOT APPLY` status prevents submission-ready proposal output.
