# Feature Specification: Projection Data Integrity & Provenance Remediation

- **Feature Branch**: `006-projection-data-integrity`
- **Created**: 2026-09-24
- **Status**: Draft
- **Input**: User description: "Remediate projection data integrity defects and enforce canonical provenance boundaries based on the September 2026 forensic diagnostic"

## Clarifications

### Session 2026-09-24

- Q: How should deterministic projection factual validation be structured across the pipeline? → A: Option A (Unified Deterministic Validator: Consolidate post-generation factual auditing into a unified validator expanding `employment_validator.py` or `projection_factual_validator.py` that checks education, certifications, languages, employment facts, and unevidenced platform claims in one pass, emitting a unified machine-readable `out/<target-slug>/runtime/projection-validation-report.yaml`).
- Q: When the unified post-generation validator detects a discrepancy, how should it handle the failure? → A: Option A (Hybrid Sanitization & Failure Gate: Automatically sanitize repairable canonical facts such as dates, titles, formal degrees, and certification lists back to canonical truth while recording alerts in `projection-validation-report.yaml`; treat un-sanitizable discrepancies—such as fabricated direct platform experience bullets—as hard validation failures that halt completion).
- Q: How should the system determine whether a named technology or platform is candidate-evidenced? → A: Option A (Multi-Tier Resolution: Validate technologies against `career-record.yaml` as highest precedence, supplemented by verified OKF capability nodes and evidence cards in `out/okf/`).
- Q: How should ATS density scoring handle unevidenced keywords claimed in candidate experience? → A: Option A (Zero-Credit + Hard Defect: Unevidenced terms earn 0% ATS density credit; claiming them directly as candidate experience triggers an integrity defect and fails the validation gate).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Canonical Context Injection & Context Isolation (Priority: P1)

As an executive candidate generating tailored career collateral, I need the projection generation engine to load the complete canonical factual selection (including education, certifications, languages, and employment history) and strictly isolate the run from prior opportunity outputs, so that my qualifications are never omitted, hallucinated, or contaminated by unrelated past applications.

**Why this priority**: If authoritative candidate facts are truncated or previous application outputs enter the model context, downstream skills hallucinate missing dates/credentials or bleed prior opportunity context into new collateral.

**Independent Test**: Can be tested by generating collateral from a canonical selection where credentials appear past line 50, and where a prior opportunity directory contains deliberately corrupted facts, verifying that all selected facts are preserved and zero corrupted facts leak into the output.

**Acceptance Scenarios**:

1. **Given** a `canonical-selection.yaml` where education (BSc 1988–1991), certifications, and language proficiencies appear beyond the initial 50 lines, **When** projection generation executes, **Then** all sections are fully loaded into context and no dates or qualifications are omitted or hallucinated.
2. **Given** a previous opportunity directory (`out/<other-target-slug>/`) containing divergent candidate claims or structural examples, **When** generating a new opportunity projection, **Then** the generator reads zero files from the previous opportunity directory.
3. **Given** a projection skill requiring formatting guidance, **When** the skill loads structural examples, **Then** it consumes only fact-free synthetic templates with neutral placeholder content.

---

### User Story 2 - Evidence-Aware Opportunity Analysis & ATS Scoring (Priority: P1)

As an executive candidate targeting roles with specific platform requirements (e.g. Workday, NetSuite, Coupa, Concur), I need the opportunity analysis and ATS scoring systems to separate target job requirements from candidate evidence, so that optimization algorithms do not reward fabricating direct experience with tools I have not used.

**Why this priority**: ATS density scoring currently creates an artificial incentive to insert unsupported keywords into candidate experience bullets, leading directly to platform experience fabrication.

**Independent Test**: Can be tested with a target job description requiring unevidenced enterprise platforms, verifying that the analyzer partitions vocabulary into "required" versus "candidate-evidenced", scores density exclusively on evidenced matches, and treats direct unevidenced tool claims as validation failures.

**Acceptance Scenarios**:

1. **Given** a target job description requiring specific enterprise platforms (e.g., Workday, Coupa) and candidate evidence demonstrating general enterprise architecture and integration capability without direct tool usage, **When** opportunity analysis executes, **Then** the platforms are categorized strictly as `required_job_vocabulary` and marked as unevidenced requirements/gaps.
2. **Given** unmatched job requirements, **When** narrative projection skills formulate application collateral, **Then** the platforms are referenced only through explicit gap framing, adjacent experience, or transferable architecture capabilities, and never claimed as direct candidate experience.
3. **Given** a projection achieving keyword matches, **When** ATS density scoring is calculated, **Then** the scoring model awards points only for candidate-evidenced keywords and assigns a defect penalty for any direct candidate claim containing unevidenced terms.

---

### User Story 3 - Comprehensive Deterministic Post-Generation Factual Validation (Priority: P1)

As a candidate submitting executive applications, I need an automated, deterministic post-generation validation pass that audits all generated collateral against canonical truth, so that any discrepancy in education, certifications, language proficiency, employment history, or direct technology experience halts completion immediately.

**Why this priority**: Non-deterministic LLM evaluation and partial regex audits fail to catch subtle date mutations or unevidenced platform claims before documents reach recruiters and hiring executives.

**Independent Test**: Can be tested by passing deliberately mutated collateral (e.g., BSc 1995–1999, Spanish Fluent, AWS Certified, direct Workday implementation claims) to the post-generation validator and confirming deterministic failure with machine-readable diagnostic details.

**Acceptance Scenarios**:

1. **Given** generated collateral stating graduation dates conflicting with canonical truth (e.g., BSc 1995–1999 instead of 1988–1991), **When** validation executes, **Then** the validator fails the build and emits an explicit diagnostic record.
2. **Given** generated collateral claiming certifications absent from canonical records (e.g., AWS Solutions Architect, Sun SCEA, Sun SCJP), **When** validation executes, **Then** validation fails immediately.
3. **Given** generated collateral claiming elevated language proficiency (e.g., Spanish Fluent when canonical is Elementary), **When** validation executes, **Then** validation fails with a proficiency inflation error.
4. **Given** generated collateral claiming direct hands-on implementation of unevidenced target platforms, **When** validation executes, **Then** validation fails identifying the unevidenced technology claim.

---

### User Story 4 - Forensic Regression Test Suite & Invariant Verification (Priority: P2)

As a system maintainer, I need an automated regression suite encapsulating the 10 diagnostic failure scenarios from the September 2026 Tenth AI forensic audit, so that future prompt refinements or skill additions can never reintroduce information leakage or credential hallucinations.

**Why this priority**: Guarantees long-term architectural stability and verifies that fixes generalize beyond hard-coded canary terms.

**Independent Test**: Execute the automated regression suite across all 10 scenarios and verify 100% deterministic pass rate across varied opportunity inputs.

**Acceptance Scenarios**:

1. **Given** the 10 forensic regression scenarios (Scenario 1: Complete canonical selection; Scenario 2: Education contradiction; Scenario 3: Certification invention; Scenario 4: Language inflation; Scenario 5: JD platform leakage; Scenario 6: Previous projection contamination; Scenario 7: Opportunity isolation; Scenario 8: Unsupported technology claim; Scenario 9: Target keyword as requirement; Scenario 10: Canonical precedence), **When** the regression test suite runs, **Then** all 10 scenarios pass deterministically.

---

### Edge Cases

- **Partial or Truncated Canonical Selection**: If a projection script attempts to read only a partial slice of `canonical-selection.yaml` (e.g. head/tail slicing), context loading fails immediately before model invocation.
- **Sequential Multi-Target Execution**: When generating collateral for Target A followed immediately by Target B in the same session, Target B's context must be completely clean and free of Target A artifacts or memory.
- **Legitimate Transferable Framing vs Direct Claim**: When a candidate resume mentions a target platform strictly in a transferable architectural context (e.g., "Led enterprise ERP integration strategy across SAP, with transferable applicability to Workday environments"), the validator must recognize the transferable framing and not falsely flag it as a fabricated direct experience claim.
- **Informal Coursework vs Formal Certification**: When training or courses (e.g., Cloud architecture seminars) appear in narrative text, the validator must verify they are not labeled with formal certification credentials (e.g., "Certified Solutions Architect").
- **Zero-Overlap Opportunities**: When a target job has minimal technology overlap with the candidate's portfolio, the system must produce an honest transferable capability analysis rather than force-fitting target tools into candidate experience.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The platform MUST load the complete, untruncated `canonical-selection.yaml` into the projection-generation context, ensuring all selected employment records, education, certifications, and languages are available to the model.
- **FR-002**: The platform MUST enforce `canonical-selection.yaml` as the supreme authoritative source for controlled candidate facts during projection, unconditionally overriding any conflicting secondary or derived input.
- **FR-003**: The platform MUST strictly prohibit active opportunity generation runs from reading generated artefacts or runtime contexts from any other opportunity directory (`out/<other-target-slug>/*`).
- **FR-004**: All structural and formatting examples provided to projection skills MUST reside in versioned, fact-free synthetic templates containing neutral placeholder data rather than historical candidate outputs.
- **FR-005**: The opportunity analysis model MUST explicitly separate extracted target job requirements from candidate-supported capabilities, classifying unevidenced terms as job-only vocabulary.
- **FR-006**: ATS vocabulary MUST be partitioned into at least `required_job_vocabulary` (all target terms) and `candidate_evidenced_vocabulary` (terms supported by candidate evidence in `career-record.yaml` as highest precedence, or verified OKF capability nodes and evidence cards in `out/okf/`).
- **FR-007**: ATS density scoring MUST award points exclusively for candidate-evidenced keywords (0% credit for unevidenced terms). Claiming unevidenced terms directly in candidate experience MUST be classified as an integrity defect that triggers a hard validation failure.
- **FR-008**: When a target requirement lacks candidate evidence, projection skills MUST represent the requirement strictly as an explicit gap, adjacent experience, or transferable capability, and NEVER as established candidate experience.
- **FR-009**: Post-generation validation MUST verify all education claims (institution, degree title, degree level, start year, and end year) against canonical education records, failing if dates or institutions conflict.
- **FR-010**: Post-generation validation MUST verify all certification claims against canonical certification records, failing if any generated certification is absent from canonical truth.
- **FR-011**: Post-generation validation MUST verify generated foreign language proficiencies against canonical language records, failing if generated proficiency exceeds canonical level.
- **FR-012**: Post-generation validation MUST enforce canonical employment facts (employers, formal titles, approved aliases, employment dates, and engagement types), failing if operational responsibilities are elevated to formal titles.
- **FR-013**: Post-generation validation MUST verify that any specific candidate-experience claim involving a named technology platform is supported by candidate evidence in `career-record.yaml` or verified OKF capability nodes and evidence cards in `out/okf/`, failing if unsupported.
- **FR-014**: The platform MUST include automated regression tests verifying that false facts placed in a prior opportunity projection cannot enter subsequent opportunity projections.
- **FR-015**: The platform MUST include automated regression tests verifying that target JD platforms absent from candidate evidence are never claimed as direct experience in generated resumes.
- **FR-016**: The platform MUST enforce one-way information flow, guaranteeing that generated projections cannot write back to canonical records (`mind-palace/canonical/` or `out/okf/`).
- **FR-017**: The platform MUST ensure total isolation between distinct opportunity runtimes regardless of execution order.
- **FR-018**: Post-generation validation MUST execute deterministically via a unified factual validator that audits education, certifications, languages, employment facts, and unevidenced platform claims in a single consolidated pass, emitting a unified machine-readable validation report at `out/<target-slug>/runtime/projection-validation-report.yaml`. The validator MUST automatically sanitize repairable canonical facts (dates, titles, formal degrees, certification lists) back to canonical truth with recorded alerts, and MUST halt completion with an explicit validation failure if un-sanitizable discrepancies (such as fabricated direct platform experience claims) are detected.
- **FR-019**: The platform MUST clearly distinguish between canonical conflict detection (`canonical-conflict-report.yaml`) and projection factual integrity validation (`projection-validation-report.yaml`), ensuring a clean conflict report is not misconstrued as full factual validation.
- **FR-020**: The platform MUST preserve rich supporting professional knowledge (methodologies, architectural patterns, demonstrated approaches) in projections, requiring canonical verification only for controlled factual claims (roles, dates, degrees, certifications, languages, direct tool ownership).

---

### Key Entities

- **CanonicalSelection**: Authoritative candidate facts selected for an opportunity, containing complete employment records, education, certifications, and languages.
- **EvidencePartitionedVocabulary**: Target job vocabulary partitioned into `required_job_vocabulary` and `candidate_evidenced_vocabulary`.
- **SyntheticStructuralTemplate**: Fact-free, neutral template illustrating layout, length, and structure without candidate data.
- **ProjectionFactualValidationReport**: Structured machine-readable report recording verification results across education, certifications, languages, employment facts, and named technology claims.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0% occurrence of unverified certifications (e.g. AWS, Sun SCEA/SCJP), inflated language proficiencies, or altered education dates in generated projections.
- **SC-002**: 0 instances of unevidenced target platforms (e.g. Workday, NetSuite, Coupa, Concur) claimed as direct candidate experience across all generated collateral.
- **SC-003**: 0 cross-opportunity factual data leaks when executing multi-opportunity generation workflows.
- **SC-004**: 100% of canonical selection facts (including credentials and languages located beyond line 50) successfully loaded into generation context.
- **SC-005**: 100% deterministic pass rate across all 10 diagnostic regression scenarios (Scenarios 1 through 10 in the regression suite).
- **SC-006**: 100% of validation failures produce structured, explainable reports identifying the generated claim, the authoritative canonical value, and the specific failure reason.

---

## Assumptions

- Candidate portfolio records in `career-record.yaml` and `out/okf/` contain sufficient evidence to evaluate whether a platform is candidate-evidenced.
- Synthetic structural templates can provide sufficient structural guidance for ATS and executive formatting without referencing real candidate outputs.
- Transferable architecture positioning (explaining general applicability to a client's tech stack) can be cleanly distinguished by validator rules from direct hands-on tool claims.
