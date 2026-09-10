# Phase 0 Research: Upwork Qualification, Evidence Integrity Controls, and Proposal Generator

## 1. Skill Layout and Architecture Integration

### Decision
Implement two discrete Skills conforming strictly to the repository's 4-layer architecture:
1. `skills/upwork-qualification/SKILL.md` (Runtime Layer): Consumes canonical OKF knowledge and `opportunity-analysis.yaml` to perform qualification evaluation and emit `out/<target-slug>/runtime/upwork-qualification.yaml`.
2. `skills/upwork-proposal/SKILL.md` (Projection Layer): Registered in `skills/projection-registry/SKILL.md`. Consumes qualification results and OKF evidence to project `upwork-proposal.md`, `upwork-screening-answers.md`, and `upwork-work-samples.md`.

### Rationale
- Strictly preserves the architectural boundary between decision (Runtime Layer qualification) and expression (Projection Layer proposal rendering).
- Enables `playbook-orchestrator` to automatically run `upwork-proposal` whenever `target_type: upwork` is set in the target opportunity configuration.

---

## 2. Evidence Integrity Contract & Machine-Readable Provenance

### Decision
Extend the canonical OKF `EvidenceCard` YAML frontmatter schema (`out/okf/evidence/<slug>.md`) with structured, machine-readable metadata keys:
- `organisation.id`: Reference to `out/okf/employment-records.yaml` ID (e.g. `emp-wpp-media-2`), `personal-cas`, or `mostelli-advisory`.
- `project.id`: Unique slug keying the specific system/project (e.g. `wpp-open-pca`).
- `environment`: `production` | `staging` | `prototype` | `lab` | `personal` | `unknown`.
- `production_verified`: Boolean (`true` | `false`).
- `implementation_role`: `lead_architect` | `sole_developer` | `contributor` | `advisor` | `evaluator` | `none`.
- `provenance.source_id` & `provenance.source_type`: `production_telemetry` | `release_notes` | `client_signoff` | `repo_code` | `eval_harness` | `resume_claim`.

### Rationale
- Forensic analysis of the first real execution revealed that `upwork-qualification` performed ungrounded prose text inferences, treating employment at WPP + repo naming (`pca-productionagents-a2a`) + evaluation latency tables + personal CAS project guardrails as proof of WPP production deployment.
- Requiring explicit machine-readable frontmatter metadata ensures qualification predicates evaluate deterministically without relying on text heuristics or LLM guessing.

---

## 3. Negative Inference Rules & Prohibited Paths

### Decision
Explicitly prohibit the qualification runtime engine from inferring `production_verified: true` or `environment: production` from any of the following 15 negative inference paths (FR-08):
1. Employment relationship (`employment-records.yaml` entry)
2. Employer name (e.g. "WPP Media", "BBC Studios")
3. Repository name (e.g. `pca-productionagents-a2a`)
4. Directory/folder name (e.g. `/production/`, `/deploy/`)
5. Free-text "production" in markdown prose
6. Free-text "deployed" in markdown prose
7. Free-text "operational" in markdown prose
8. Technology choice (e.g. OpenAI SDK, Temporal, Supabase, Postgres)
9. Evaluation test metrics or benchmark tables (e.g. "Latency <30s", "Success Rate >99%")
10. High success rates
11. Latency measurements
12. CI/CD workflow files
13. Production-like system architecture
14. Personal side projects (`organisation.id: personal-cas`)
15. Prototype, lab, or innovation project titles

### Rationale
- Prevents false-positive qualifications caused by surface-level text or repository conventions.

---

## 4. Cross-Organisation and Cross-Project Isolation Boundaries

### Decision
Enforce strict evidence composition boundaries for requirement-to-evidence joins:
$$\text{ValidJoin}(C_1, C_2) \iff \big(C_1.\text{organisation.id} == C_2.\text{organisation.id}\big) \land \big(C_1.\text{project.id} == C_2.\text{project.id}\big)$$
- **Cross-Organisation Isolation (FR-15)**: Evidence from Company B or Personal/CAS projects CANNOT satisfy Company A production implementation requirements.
- **Cross-Project Isolation (FR-16)**: Production evidence from Project X at Company A CANNOT satisfy a production requirement for Project Y at Company A.
- **Personal Project Isolation (FR-17)**: Personal projects (`personal-cas`) MAY satisfy general capability requirements, but CANNOT satisfy employer-specific production implementation requirements.

---

## 5. Qualification Gate Semantics & Dealbreaker Hard Gates

### Decision
Classify hard requirements and control semantics (`proposal_generation`):
- `VERIFIED_PRODUCTION` + compatible implementation role $\rightarrow$ `APPLY` (`proposal_generation: allowed`).
- `VERIFIED_NON_PRODUCTION` $\rightarrow$ `DO NOT APPLY` (`proposal_generation: blocked`).
- `UNKNOWN` on explicit dealbreaker requirements ("If you have not already done this in production, do not apply") $\rightarrow$ **`DO NOT APPLY`** (`proposal_generation: blocked`). `UNKNOWN` MUST NEVER yield `CONDITIONAL` or `APPLY` for dealbreaker gates.
- `UNKNOWN` on non-dealbreaker requirements $\rightarrow$ `CONDITIONAL` (`proposal_generation: allowed_with_conditions`) with an explicit `[OPEN CONDITION: <fact>]` prompt requiring candidate verification.

---

## 6. Client-Facing Proposal vs. Internal Provenance Separation

### Decision
Separation of client-facing prose and internal claim provenance:
- **`upwork-proposal.md`**: Rendered as clean, natural professional proposal prose free of visible `[evidence]` tags or `[^source-id]` footnotes, ready for direct copy-pasting into Upwork.
- **`out/<target-slug>/runtime/upwork-qualification.yaml`**: Stores full machine-readable claim traceability (`claim_traceability` array mapping each claim line to its evidence ID, classification, and footnote source).
- **`projection-validator`**: Independently re-evaluates qualification claims against canonical OKF evidence frontmatter metadata (`production_verified`, `environment`, `organisation.id`, `project.id`).

---

## 7. Artifact Storage and File Conventions

### Decision
Store intermediate machine-readable runtime data in `out/<target-slug>/runtime/` and rendered Markdown views in `out/<target-slug>/`:
- `out/<target-slug>/runtime/upwork-qualification.yaml` (YAML format, includes `proposal_generation` and `claim_traceability`)
- `out/<target-slug>/upwork-proposal.md` (Clean Markdown format, 350-500 words target)
- `out/<target-slug>/upwork-screening-answers.md` (Markdown format, direct answers + evidence proof)
- `out/<target-slug>/upwork-work-samples.md` (Markdown format, max 3 samples)
- `out/<target-slug>/runtime/projection-validation-report.yaml` (Updated by `projection-validator`)
