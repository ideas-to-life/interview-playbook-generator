# Implementation Research: Projection Data Integrity & Provenance Remediation

**Feature**: `006-projection-data-integrity`  
**Date**: 2026-09-24  
**Status**: Completed  

---

## 1. Unified Deterministic Validator Architecture

### Decision
Consolidate post-generation factual auditing into a unified deterministic validator script `scripts/projection_validator.py` (incorporating and superseding the regex checks in `scripts/employment_validator.py`), which validates all generated collateral in `out/<target-slug>/` against `canonical-selection.yaml` and `career-record.yaml`. The validator emits a single comprehensive machine-readable report at `out/<target-slug>/runtime/projection-validation-report.yaml`.

### Rationale
- Unifies disparate checks (employment facts, education, certifications, language proficiencies, unevidenced platform claims) into a single deterministic execution.
- Avoids fragmented execution and duplicate AST/Markdown parsing across multiple scripts.
- Distinctly separates canonical conflict detection (`canonical-conflict-report.yaml`, which audits secondary sources) from projection factual integrity validation (`projection-validation-report.yaml`, which audits generated outputs).
- Fulfills FR-018 and FR-019 without creating overlapping or contradictory reports.

### Alternatives Considered
- *Extend `employment_validator.py` in-place*: Kept the legacy name but broadened its scope to technologies, education, and certs. Rejected because the filename `employment_validator.py` is semantically misleading for general credential and technology validation.
- *Separate modular validator scripts per domain*: Maintained separate scripts for education, certs, and tech stack. Rejected due to redundant Markdown file reading and fragmented exit codes.

---

## 2. Technology Evidence Boundary & ATS Vocabulary Partitioning

### Decision
1. **Multi-Tier Technology Evidence Boundary**:
   - **Tier 1 (Authoritative Canonical)**: Technologies explicitly evidenced in `career-record.yaml` (e.g. in operational scope, responsibilities, or verified accomplishments).
   - **Tier 2 (Canonical Knowledge Layer)**: Technologies evidenced in verified OKF capability cards (`out/okf/capabilities/`) or signature achievements (`out/okf/signature-achievements.md`).
2. **ATS Vocabulary Partitioning in `opportunity-analyzer`**:
   - Every extracted ATS keyword from the target job description is evaluated against the combined Tier 1 and Tier 2 candidate evidence.
   - Keywords matching candidate evidence are categorized into `candidate_evidenced_vocabulary`.
   - Keywords lacking candidate evidence are categorized into `required_job_vocabulary` (unmatched requirements / explicit gaps).
3. **ATS Density Scoring**:
   - Density calculation awards credit exclusively for matches within `candidate_evidenced_vocabulary`.
   - Matches against unevidenced keywords receive 0% credit.
   - If an unevidenced keyword is claimed as direct candidate experience in generated text, it triggers an integrity defect that causes a hard validation failure.

### Rationale
- Completely eliminates the optimization incentive to hallucinate client tech stacks (e.g., Workday, NetSuite, Coupa, Concur) into candidate bullets.
- Preserves candidate ability to legitimately discuss target tools in an explicit gap, adjacent experience, or transferable architecture context without penalty.
- Generalizes across all enterprise software tools without relying on hard-coded blacklists (NFR-03).

### Alternatives Considered
- *Hard-coded canary list (blocking only Workday, NetSuite, Coupa, Concur)*: Rejected because it fails to protect against future unseen target technologies (NFR-03).
- *Strict manual allowlist*: Rejected because maintaining a static technology whitelist would require human edits for every novel tool or library.

---

## 3. Complete Canonical-Selection Context Injection & Isolation

### Decision
1. **Full File Context Injection**:
   - Update prompt generation in all projection skills (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `opportunity-alignment-view`, `executive-brief-view`, `playbook-assembler`) to inject the entire `canonical-selection.yaml` verbatim into the prompt context.
   - Enforce an invariant test ensuring that selections beyond line 50 (specifically education dates 1988–1991, certifications, languages) are present in the loaded context payload.
2. **Strict Cross-Opportunity Isolation**:
   - Skills are prohibited from reading, searching, or globbing any directory under `out/<other-target-slug>/`.
   - Remove any legacy prompt references that suggest reading prior opportunity projections as formatting or stylistic templates.
3. **Synthetic Fact-Free Structural Templates**:
   - Establish dedicated, neutral structural templates under `templates/projections/` (e.g., `resume-executive.template.md`, `resume-ats.template.md`, `cover-letter.template.md`).
   - These templates contain synthetic placeholder data (e.g. "Acme Corp", "2018–2021", "Enterprise Platform Migration") demonstrating structure, headings, section order, and density without candidate-specific facts.

### Rationale
- Truncation or partial file reading was the root cause of graduation date hallucination (1995–1999 vs 1988–1991) in the Tenth AI generation.
- Cross-opportunity references caused prior opportunity data (e.g. LSEG) to contaminate active generation context.
- Synthetic templates decouple formatting guidance from real candidate facts.

### Alternatives Considered
- *AST-based JSON schema generation*: Generating projections as rigid typed JSON schemas. Rejected as high-complexity/high-friction for executive markdown collateral (Option C in Concept).

---

## 4. Hybrid Sanitization and Failure Gate Protocol

### Decision
The post-generation validator implements a two-stage hybrid remediation model:
1. **Automated Sanitization (Stage 1 - Repairable Facts)**:
   - For repairable canonical contradictions with known 1-to-1 canonical replacements (e.g., mutating 1995–1999 to 1988–1991, BBC title inflation to canonical Lead Enterprise Architect, degree level inflation from MSc to BSc, language proficiency inflation from Fluent to Elementary): automatically sanitize the output file back to canonical truth and log an alert in `projection-validation-report.yaml`.
2. **Hard Validation Failure (Stage 2 - Un-sanitizable Direct Claims)**:
   - For fabricated direct experience claims involving unevidenced technologies (e.g., "Led Workday integration", "Implemented NetSuite ERP"), the validator cannot guess what true experience was intended. The validator flags an integrity error, marks the report status as `FAILED`, and exits with code 1, halting pipeline completion and preventing document delivery.

### Rationale
- Preserves autonomous pipeline self-healing for deterministic credential/tenure details while maintaining an uncompromising hard stop against fabricated experience narratives.
- Aligns `AGENTS.md` Principle 14 (Automated Sanitization) with Refinement Spec Section 20 (FR-18: known canonical contradictions must fail rather than produce passive warnings).

### Alternatives Considered
- *Strict Fail-Fast on all discrepancies*: Required human or model regeneration for minor date typos. Rejected as inefficient when canonical ground truth is already available for deterministic replacement.
- *Pure Sanitization (auto-redacting unevidenced bullets)*: Attempting to automatically delete fabricated sentences. Rejected because deleting narrative bullets silently alters document layout and page budget without model awareness.

---

## 5. Automated Regression Test Architecture

### Decision
Implement a dedicated pytest suite `tests/test_forensic_remediation_regression.py` executing all 10 diagnostic scenarios defined in Section 24 of the requirements spec:
1. Scenario 1: Complete canonical selection (>50 lines context check).
2. Scenario 2: Education contradiction (BSc date mismatch).
3. Scenario 3: Certification invention (AWS, Sun SCEA/SCJP).
4. Scenario 4: Language inflation (Spanish Elementary -> Fluent).
5. Scenario 5: JD platform leakage (unevidenced Workday/NetSuite/Coupa/Concur in candidate experience).
6. Scenario 6: Previous projection contamination (corrupted prior opportunity isolation).
7. Scenario 7: Opportunity isolation (cross-run keyword immutability).
8. Scenario 8: Unsupported technology claim (arbitrary non-evidenced tool claim failure).
9. Scenario 9: Target keyword as requirement (valid gap/transferable framing does not fail).
10. Scenario 10: Canonical contradiction precedence (canonical selection overrides secondary conflicting sources).

### Rationale
- Directly validates the acceptance gate (Section 28) and guarantees that the Tenth AI diagnostic failure modes can never reoccur.
