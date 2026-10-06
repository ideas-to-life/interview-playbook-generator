# Feature Specification: Canonical Career Record Integration

**Feature Branch**: `005-canonical-record-integration`

**Created**: 2026-09-18

**Status**: Draft

**Input**: User description: "docs/requirements-spec/canonical-record-integration-reqs-spec.v1.md"

## Clarifications

### Session 2026-09-18

- Q: When the platform detects that derived content or secondary documents conflict with canonical career facts, should it generate a structured conflict audit report or simply enforce canonical precedence during projection? → A: Option A (Generate structured conflict audit report at `out/<target-slug>/runtime/canonical-conflict-report.yaml` logging conflicting titles, dates, or credentials for cleanup without blocking execution).
- Q: In which pipeline stage should Activity A (canonical factual selection) be executed and persisted? → A: Option A (Runtime Layer intermediate artifact: Execute factual selection during runtime opportunity analysis, persisting selected canonical entries and IDs to `out/<target-slug>/runtime/canonical-selection.yaml` for all projection skills to consume).
- Q: How should the platform handle the legacy Positions.csv parsing in portfolio-ingestor when canonical/career-record.yaml is present? → A: Option B (Complete removal of `Positions.csv` parsing from `portfolio-ingestor`; all employment records in `out/okf/employment-records.yaml` must originate strictly and exclusively from `career-record.yaml`).
- Q: How should the deterministic validation layer handle detected canonical violations in generated projection artefacts? → A: Option C (Automated sanitization with alert: Automatically rewrite detected invalid phrases in output artefacts back to canonical truth while recording an alert in `projection-validation-report.yaml`).
- Q: Where in config/config.yaml should the canonical career record file location be specified? → A: Option A (Under `candidate` block as `candidate.canonical_record: "canonical/career-record.yaml"`, resolving relative to `candidate.portfolio_dir` by default or supporting an absolute path).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authoritative Career Fact Ingestion & Quarantine Exclusion (Priority: P1)

As a candidate generating tailored career collateral, I need the platform to discover and ingest verified career facts exclusively from the canonical career record, while strictly excluding any quarantined materials, so that outdated or contaminated historical claims are never propagated into my professional collateral.

**Why this priority**: Without an authoritative, unpolluted baseline of professional facts, all downstream generation risks hallucinating or reviving known factual errors.

**Independent Test**: Can be tested by running knowledge ingestion against a portfolio directory containing a canonical record and conflicting quarantined documents, verifying that only canonical facts are ingested and zero quarantined facts enter the factual baseline.

**Acceptance Scenarios**:

1. **Given** a portfolio directory containing `canonical/career-record.yaml` and files in `quarantine/`, **When** the ingestion and fact-loading processes execute, **Then** canonical facts (roles, dates, institutions, certifications) are loaded and all items within `quarantine/` are completely excluded from factual sourcing.
2. **Given** a missing or unparseable canonical career record, **When** generation is requested, **Then** the platform fails fast with a clear diagnostic error and halts execution rather than silently falling back to unverified derived content.

---

### User Story 2 - Strict Canonical Precedence & Title / Qualification Protection (Priority: P1)

As an executive candidate, I need the system to enforce strict precedence for formal job titles, operational scope, and academic qualifications over derived or narrative materials, so that my professional projections remain 100% truthful and protected against title or credential inflation.

**Why this priority**: Title inflation (e.g., transforming a Lead Architect with acting responsibilities into a formal Head of Architecture) and degree inflation (e.g., upgrading a Bachelor's to a Master's) directly compromise executive integrity and recruiter trust.

**Independent Test**: Can be tested with a test case presenting conflicting derived claims (e.g., derived "Head of Enterprise Architecture" vs canonical formal title "Lead Enterprise Architect - Technology Transformation Group" with acting scope), verifying that generated CV and summary outputs preserve the exact formal canonical title and separate operational context.

**Acceptance Scenarios**:

1. **Given** a canonical entry with formal title "Lead Enterprise Architect - Technology Transformation Group" and operational context noting acting responsibilities for the Head of Architecture, **When** generating executive summary or CV entries, **Then** the platform presents the formal title faithfully and never elevates the title to "Head of Enterprise Architecture".
2. **Given** derived secondary content claiming an MSc from the Federal University of Rio de Janeiro and a canonical record establishing a BSc from Universidade de Mogi das Cruzes, **When** generating education sections, **Then** only the canonical BSc is emitted and the derived MSc is completely omitted.
3. **Given** a canonical achievement stating "supported architecture governance", **When** generating accomplishments, **Then** the platform preserves the supported level of contribution and rejects amplification to "established and led the enterprise architecture governance function".

---

### User Story 3 - Chronology, Employment Boundaries & Unresolved Item Safety (Priority: P2)

As a candidate with multi-stage corporate, consulting, and advisory engagements, I need the platform to preserve exact canonical dates, distinct employer relationships, and unresolved item boundaries, so that overlapping or multi-party engagements are accurately represented and unverified claims are not presented as facts.

**Why this priority**: Preserving accurate employer relationships (e.g., consultancy contracting vs direct employment) and guarding against inventing answers for unresolved career questions ensures factual defensibility during background checks and executive interviews.

**Independent Test**: Can be tested by running factual projection across known historical relationships (e.g., Compugraf as consultancy contracted to Souza Cruz; WPP Media direct employment vs Mostelli independent advisory), verifying that roles are not merged or conflated.

**Acceptance Scenarios**:

1. **Given** a canonical record designating Compugraf as an external consultancy contracted to Souza Cruz, **When** generating career history, **Then** the relationship is presented as consulting through Compugraf rather than two simultaneous direct employers.
2. **Given** direct corporate employment at WPP Media followed by independent advisory work at Mostelli, **When** projecting chronology, **Then** the platform maintains distinct timeline entries and does not merge them into a single continuous engagement.
3. **Given** an entry in the canonical record's `unresolved_questions` section, **When** generating projections, **Then** unresolved items are never presented as established facts, while resolved items (`current_status: resolved`) are safely integrated.

---

### User Story 4 - Factual Selection vs Narrative Projection Separation (Priority: P2)

As a candidate applying for diverse executive opportunities, I need the platform to separate factual selection (choosing which true canonical facts match the target role) from narrative projection (formatting and tailoring the presentation), so that tailoring never invents or alters factual claims.

**Why this priority**: Decoupling what is true from how it is phrased allows aggressive alignment to target opportunities while preserving a zero-fabrication boundary.

**Independent Test**: Can be tested by generating two distinct projections (e.g., a Board-level CV vs a hands-on Consulting proposal) from the same canonical record, verifying that both express different emphasis and selections but share identical underlying facts, dates, and titles.

**Acceptance Scenarios**:

1. **Given** a target opportunity emphasizing digital transformation governance, **When** factual selection runs, **Then** it selects canonical entries matching the opportunity without modifying their underlying factual attributes.
2. **Given** selected canonical facts, **When** narrative projection runs, **Then** the output optimizes readability, structure, and professional tone without altering tenure, scope, title, or metrics.

---

### Edge Cases

- **Malformed Canonical Record**: If `career-record.yaml` contains invalid syntax or missing required top-level sections, the pipeline halts immediately with an explicit validation error.
- **Quarantine Path Ingestion Attempt**: If a legacy or secondary configuration attempts to include a file located within `quarantine/`, the source discovery engine rejects the file and logs an exclusion warning.
- **Conflicting Derived Dates**: If a secondary document lists an employment end date differing from the canonical record, the canonical date unconditionally supersedes the derived date.
- **Unresolved Question Handling Across Collateral**: When an opportunity touches upon an item in `unresolved_questions` that is not marked `resolved`, the platform unconditionally omits the claim from external-facing projections (Resumes, Cover Letters, Proposals, LinkedIn profiles), while explicitly surfacing it in internal coaching materials (Interview Playbook, Interview Cheat Sheet, Knowledge Gaps) with a clear `[NEEDS CONFIRMATION]` flag.
- **Concurrent Canonical Roles**: When two canonical engagements overlap chronologically (e.g., concurrent advisory board and principal consulting), the platform preserves both distinct roles with their respective engagement types without fabricating artificial gaps or merges.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The platform MUST discover and load the canonical career record from a centralized configuration path specified in `config/config.yaml` as `candidate.canonical_record` (defaulting to `canonical/career-record.yaml` relative to `candidate.portfolio_dir`, with support for an explicit absolute path override).
- **FR-002**: The platform MUST treat the canonical career record as the highest-authority source for professional facts, superseding all secondary documents, derived content, AI-generated content, and LLM inference.
- **FR-003**: The platform MUST enforce read-only access to the canonical career record, ensuring no generation step, agent, or skill modifies, appends to, or updates `career-record.yaml`.
- **FR-004**: The platform MUST fail fast with an explicit error and halt execution if the canonical career record is missing, unreadable, or syntactically invalid, and MUST NOT silently fall back to derived content.
- **FR-005**: The platform MUST strictly exclude all content within `quarantine/` from being used as a source for professional facts, achievements, credentials, or chronology.
- **FR-006**: The platform MUST distinguish formal employment titles (`formal_title`) from operational context (`operational_scope`, `responsibilities_scope`, `acting_responsibilities`), ensuring formal titles are never modified, combined, or inflated into senior leadership titles not explicitly established in the canonical record.
- **FR-007**: The platform MUST use canonical education and certification records as immutable facts, prohibiting degree upgrades, institution substitutions, or unevidenced qualification claims.
- **FR-008**: The platform MUST enforce canonical employment dates, preventing chronological shortening, extension, missing month inference, or role merging.
- **FR-009**: The platform MUST preserve distinct employer and engagement classifications (direct employment, consultancy/contracting, independent advisory, concurrent engagements).
- **FR-010**: The platform MUST distinguish canonical items marked `current_status: resolved` from genuinely unresolved questions, unconditionally omitting unresolved items from external-facing collateral (CVs, cover letters, proposals, LinkedIn profiles) while surfacing them in internal coaching materials (Interview Playbook, Cheat Sheet, Knowledge Gaps) flagged with `[NEEDS CONFIRMATION]` for candidate verification.
- **FR-011**: The platform MUST decouple factual selection (Activity A) from narrative projection (Activity B) by executing factual selection during runtime opportunity analysis and persisting selected canonical entries to `out/<target-slug>/runtime/canonical-selection.yaml`, ensuring downstream projection skills consume immutable selected facts without independent re-interpretation or fabrication.
- **FR-012**: The platform MUST restrict achievement and responsibility claims to the level of ownership, scope, and impact explicitly supported by the canonical record, rejecting unevidenced transformation of contribution into leadership or enterprise-wide ownership.
- **FR-013**: The platform MUST retain internal traceability references to canonical record identifiers (e.g., `CAR-xx`, `EDU-xx`, `CERT-xx`) within `canonical-selection.yaml` and derived runtime models to support provenance and validation.
- **FR-014**: The platform MUST enforce canonical fact precedence across all generated projection types (CVs, cover letters, LinkedIn profiles, proposals, interview playbooks, executive briefs).
- **FR-015**: The platform MUST execute automated regression tests verifying that known forensic failure cases (Scenario 1 through Scenario 8) are definitively resolved and cannot recur.
- **FR-016**: The platform MUST generate a structured conflict audit report (`out/<target-slug>/runtime/canonical-conflict-report.yaml`) whenever derived content or secondary documents conflict with canonical career facts, detailing the contradictory claims, affected source files, and canonical overrides to support knowledge cleanup without blocking pipeline execution.
- **FR-017**: The platform MUST generate `out/okf/employment-records.yaml` strictly and exclusively from `canonical/career-record.yaml`, completely removing legacy parsing of `Positions.csv` from `portfolio-ingestor` to prevent unverified or contaminated records from entering canonical employment records.
- **FR-018**: The platform MUST automatically sanitize any detected discrepancies (mutated dates, inflated titles, unverified degrees) in generated projection artefacts by rewriting them back to the canonical truth, while logging an explicit alert in `out/<target-slug>/runtime/projection-validation-report.yaml`.

### Key Entities *(include if feature involves data)*

- **CanonicalCareerRecord**: The root authoritative structure representing the candidate's verified career history, education, certifications, and unresolved questions.
- **CareerEntry**: A discrete professional engagement containing immutable formal title, employer, dates, engagement type (direct, consulting, advisory), operational scope, acting responsibilities, and verified accomplishments.
- **EducationEntry**: A verified academic credential containing degree level, field of study, institution, location, and dates.
- **CertificationEntry**: A verified professional qualification containing credential name, issuing authority, and validity dates.
- **UnresolvedQuestion**: A recorded factual ambiguity with explicit status tracking (`resolved` vs `unresolved`), preventing premature factual claims.
- **CanonicalSelectionRecord**: A runtime data model persisted at `out/<target-slug>/runtime/canonical-selection.yaml` mapping target opportunity requirements to selected canonical entries, preserving canonical IDs (`CAR-xx`, `EDU-xx`, `CERT-xx`), formal titles, exact dates, and verified scopes for all projection skills.
- **CanonicalConflictReport**: A runtime audit artefact documenting discrepancies between canonical facts and secondary/derived content, listing the source location, conflicting claim, canonical resolution, and severity.
- **SourcePrecedenceHierarchy**: The ordered authority model establishing: (1) Canonical Career Record > (2) Authoritative Primary Source Data > (3) Trusted Knowledge Content > (4) Derived/Narrative Content > (5) AI-Generated Content > (6) LLM Inference.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of generated professional collateral (CVs, summaries, proposals, profiles) utilize verified canonical facts for all job titles, employers, dates, and qualifications without discrepancy.
- **SC-002**: Zero occurrences of known forensic regressions (e.g., MSc Federal University of Rio de Janeiro, inflated Head of Enterprise Architecture title, merged Compugraf/Souza Cruz relationships) across all regression test suites and end-to-end runs.
- **SC-003**: 100% of files residing within `quarantine/` directories are filtered out and rejected from the factual ingestion pipeline.
- **SC-004**: Pipeline execution halts with an exit error within 5 seconds when presented with an invalid or missing canonical record, preventing any fallback generation on unverified data.
- **SC-005**: 100% of candidate achievements and responsibilities reflect verified canonical ownership levels, with zero unevidenced elevations from contribution to leadership.
- **SC-006**: Generated projection outputs preserve readability, relevance, and role-tailoring quality without material degradation of executive impact.

## Assumptions

- The canonical career record at `mind-palace/canonical/career-record.yaml` is maintained and curated through human-controlled knowledge management prior to generator execution.
- Existing derived content in `mind-palace/knowledge/` and `mind-palace/derived-content/` remains available for contextual framing, terminology, and domain methods, provided it does not contradict canonical facts.
- The pipeline configuration in `config/config.yaml` can specify the canonical record location either as a relative path to `portfolio_dir` or as a distinct configuration key.
- Backward compatibility is maintained for all existing generator output formats (Markdown files for CVs, proposals, playbooks).
