# Research & Architecture Decisions: Canonical Career Record Integration

**Feature**: `005-canonical-record-integration`  
**Status**: Completed  
**Date**: 2026-09-18  

This document consolidates architectural research, design decisions, and technology selections for integrating `canonical/career-record.yaml` as the authoritative professional facts source across the Interview Playbook Generator.

---

## 1. Canonical Record Discovery & Loading

### Decision
Implement a shared Python module `scripts/canonical_loader.py` that discovers, validates, and loads `career-record.yaml`. Configuration is centralized in `config/config.yaml` under `candidate.canonical_record` (defaulting to `canonical/career-record.yaml` relative to `candidate.portfolio_dir`). The loader treats the file as strictly read-only and fails fast (<5s) with an explicit error if the record is missing or syntactically invalid.

### Rationale
- Centralizes discovery and parsing in a single reusable module rather than duplicating YAML-loading logic across multiple skills or scripts.
- Satisfies requirements V01, V02, V03, FR-001, FR-003, and FR-004.
- Allows portability if `mind-palace` is relocated or mounted in different directories.

### Alternatives Considered
- *Hardcoding the path*: Rejected because it couples scripts to local absolute paths and breaks across machines.
- *Convention-only without config*: Rejected because explicit configuration in `config/config.yaml` is clearer for enterprise workflows.

---

## 2. Quarantine Directory Exclusion

### Decision
Update `scripts/ingest_portfolio.py` to enforce a strict directory exclusion list during `os.walk` file discovery, unconditionally skipping any directory named `quarantine` or paths matching `*/quarantine/*`.

### Rationale
- The forensic audit identified that contaminated historical claims (e.g., MSc Rio de Janeiro, unverified roles) resided in legacy documents now moved to `quarantine/`.
- Ensuring `portfolio-ingestor` excludes this folder structurally prevents contaminated text from being ingested as OKF Source nodes (`out/okf/sources/`).
- Satisfies requirement FR-005, SC-003, and Scenario 7.

### Alternatives Considered
- *Relying on LLM prompt instructions*: Rejected by requirement specification Section 14 ("This exclusion must be enforced rather than relying on prompts to tell the LLM not to use it").
- *Deleting quarantine files*: Rejected because quarantined files must remain for historical and forensic reference.

---

## 3. Deprecation of `Positions.csv` & Ingestion of `employment-records.yaml`

### Decision
Completely deprecate and remove `Positions.csv` parsing from `scripts/ingest_portfolio.py`. Instead, `portfolio-ingestor` reads `canonical/career-record.yaml` to populate `out/okf/employment-records.yaml` with verified formal titles, exact employment dates, direct/consultancy employer classifications, operational scope, and approved aliases.

### Rationale
- `Positions.csv` was the direct vector that introduced corrupted records into `employment-records.yaml` (such as article titles like "Learn-it-all-Do-it-all" being treated as employer companies).
- Sourcing `employment-records.yaml` directly from `career-record.yaml` ensures the canonical career record is the single source of truth for the entire OKF Knowledge Layer.
- Satisfies FR-017 and user decision from Clarification Question 3.

### Alternatives Considered
- *Dual-sourcing / Merging*: Rejected because merging with corrupted CSV records creates conflicts and violates canonical precedence.

---

## 4. Separation of Factual Selection (Activity A) and Narrative Projection (Activity B)

### Decision
Decouple factual selection from narrative writing by introducing an intermediate runtime artifact: `out/<target-slug>/runtime/canonical-selection.yaml`.
- **Activity A (Factual Selection)**: Executed by `opportunity-analyzer` (or a dedicated helper `scripts/canonical_selector.py`), evaluating target opportunity requirements against canonical entries and selecting the relevant subset. Each selected entry retains its canonical identifier (`CAR-xx`, `EDU-xx`, `CERT-xx`), formal title, and verified scope.
- **Activity B (Projection)**: Downstream projection skills (resumes, cover letters, LinkedIn profiles, playbooks) consume `canonical-selection.yaml` as immutable factual input, restricting LLM operations to emphasis, structuring, and narrative phrasing.

### Rationale
- Eliminates the failure mode where individual projection prompts hallucinate or inflate titles and dates to fit the job description.
- Preserves full internal traceability (`CAR-xx`, `EDU-xx`) without forcing IDs into user-facing copy.
- Satisfies FR-011, FR-013, NFR01 (Determinism), and user decision from Clarification Question 2.

### Alternatives Considered
- *Decentralized selection inside each skill prompt*: Rejected because LLMs independently selecting facts produce inconsistent chronologies, titles, and metrics across different collateral for the same target opportunity.

---

## 5. Conflict Audit Reporting

### Decision
Implement a conflict detection utility in `scripts/canonical_validator.py` that scans secondary documents, derived OKF nodes, and selected context against canonical facts. Discrepancies are written to `out/<target-slug>/runtime/canonical-conflict-report.yaml`, recording:
- Target slug and execution timestamp
- Source file path containing the conflicting claim
- Nature of conflict (title inflation, date mutation, unverified degree, scope conflation)
- Canonical truth vs conflicting claim
- Resolution applied (canonical override)

### Rationale
- Satisfies FR-016 and user decision from Clarification Question 1.
- Provides actionable visibility into contaminated secondary files in `mind-palace` so they can be cleaned or quarantined without halting the pipeline.

### Alternatives Considered
- *Silent override without reporting*: Rejected because it leaves underlying data quality issues invisible.
- *Hard failure on any detected conflict*: Rejected because legacy documents frequently contain outdated wording; blocking execution prevents generating collateral.

---

## 6. Deterministic Validation & Automated Sanitization

### Decision
Upgrade `scripts/employment_validator.py` and integrate it into `projection-validator`:
1. Expand validation scope from employment history to include academic credentials (degrees, institutions) and certifications.
2. If a projection output contains a discrepancy against canonical facts (e.g. "Head of Enterprise Architecture" instead of "Lead Enterprise Architect", or "MSc Federal University of Rio de Janeiro" instead of "BSc Universidade de Mogi das Cruzes"), the validator performs **automated sanitization**:
   - Replaces the offending string with the canonical formal fact in the output markdown file.
   - Logs an alert in `out/<target-slug>/runtime/projection-validation-report.yaml`.
   - Records the sanitization in the pipeline audit log.

### Rationale
- Satisfies FR-014, FR-018, SC-002, and user decision from Clarification Question 4.
- Provides a deterministic release safety net that guarantees 100% factual fidelity even if an LLM projection step slips up.

### Alternatives Considered
- *Hard pipeline failure*: Rejected by user decision in favor of automated repair with explicit alerting.
- *Report-only warnings*: Rejected because leaving invalid titles/degrees in executive collateral destroys credibility.

---

## 7. Mandatory Regression Testing Matrix

### Decision
Implement `tests/test_canonical_record_regression.py` covering all 8 mandatory forensic regression scenarios:
1. **Scenario 1 (Education)**: Assert BSc Mogi das Cruzes is emitted; MSc Federal University of Rio de Janeiro is 100% absent.
2. **Scenario 2 (BBC Formal Title)**: Assert formal title is "Lead Enterprise Architect - Technology Transformation Group"; "Head of Enterprise Architecture" title is rejected/sanitized.
3. **Scenario 3 (BBC Acting Scope)**: Assert acting scope can be described as operational responsibility, but formal title is never elevated.
4. **Scenario 4 (BAT Chronology)**: Assert complete canonical chronology for BAT is preserved; incomplete secondary chronology overridden.
5. **Scenario 5 (Compugraf / Souza Cruz)**: Assert Compugraf is represented as consultancy contracted to Souza Cruz; not simultaneous direct employers.
6. **Scenario 6 (WPP / Mostelli)**: Assert distinct separation between WPP Media (direct corporate employment) and Mostelli (independent advisory).
7. **Scenario 7 (Quarantine)**: Assert files in `quarantine/` are never ingested as sources or facts.
8. **Scenario 8 (Unsupported Enhancement)**: Assert "supported architecture governance" is not amplified to "established and led the enterprise architecture governance function".

### Rationale
- Directly addresses Section 25 of the requirement specification and ensures zero recurrence of known forensic findings.
