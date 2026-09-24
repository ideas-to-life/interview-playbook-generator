# Quickstart Guide: Projection Data Integrity & Provenance Validation

This guide provides runnable instructions to execute and verify the projection data integrity and provenance remediation end-to-end.

---

## 1. Prerequisites

- Python 3.10+
- Repository dependencies installed (`pytest`, `pyyaml`)
- Valid canonical career record at `canonical/career-record.yaml` (or configured `candidate.canonical_record` in `config/config.yaml`)

---

## 2. Running Deterministic Projection Validation

To run the unified post-generation factual validator across an opportunity output directory:

```bash
python3 scripts/projection_validator.py <target-slug>
```

### Example: Audit Tenth AI Opportunity
```bash
python3 scripts/projection_validator.py tenth-ai-lead-enterprise-architect
```

### Expected Output
- Generates `out/tenth-ai-lead-enterprise-architect/runtime/projection-validation-report.yaml`.
- Returns exit code `0` if all candidate claims match canonical truth (or if repairable discrepancies were sanitized in-place).
- Returns exit code `1` if fatal integrity defects (such as fabricated direct platform experience) are detected.

---

## 3. Running the Forensic Regression Suite

To execute all 10 diagnostic regression scenarios defined in the requirements specification:

```bash
pytest tests/test_forensic_remediation_regression.py -v
```

### Test Scenarios Covered
1. **Scenario 1 (`test_complete_canonical_selection_loading`)**: Verifies that education, certifications, and languages located beyond line 50 of `canonical-selection.yaml` are loaded into model prompt context.
2. **Scenario 2 (`test_education_date_contradiction_rejected`)**: Deliberately injects `BSc 1995–1999` and verifies validation failure / automated sanitization to `1988–1991`.
3. **Scenario 3 (`test_certification_invention_rejected`)**: Injects `AWS Certified Solutions Architect`, `Sun SCEA`, and `Sun SCJP`, verifying validation rejection.
4. **Scenario 4 (`test_language_inflation_rejected`)**: Injects `Spanish: Fluent` when canonical is `Elementary`, verifying validation rejection.
5. **Scenario 5 (`test_target_jd_platform_leakage_prevented`)**: Target JD includes Workday, NetSuite, Coupa, Concur; verifies generated resume makes zero direct experience claims for those tools.
6. **Scenario 6 (`test_previous_projection_contamination_blocked`)**: Places corrupted candidate claims in `out/lseg-director-enterprise-architecture/` and proves they cannot enter `out/tenth-ai-lead-enterprise-architect/`.
7. **Scenario 7 (`test_opportunity_runtime_isolation`)**: Verifies that generating two different target opportunities in sequential order produces mutually isolated, clean outputs.
8. **Scenario 8 (`test_unsupported_named_technology_rejected`)**: Injects arbitrary unsupported enterprise software and verifies failure.
9. **Scenario 9 (`test_transferable_framing_allowed`)**: Verifies that mentioning target tools strictly in an explicit gap or transferable architecture context does not trigger a false-positive failure.
10. **Scenario 10 (`test_canonical_precedence_over_secondary`)**: Verifies that when auxiliary sources conflict with `career-record.yaml`, canonical truth unconditionally wins.

---

## 4. Validating ATS Vocabulary Partitioning

Run `opportunity-analyzer` on a target job description and inspect the emitted partition:

```bash
python3 -c "
import yaml
with open('out/tenth-ai-lead-enterprise-architect/runtime/opportunity-analysis.yaml') as f:
    data = yaml.safe_load(f)
assert 'candidate_evidenced_vocabulary' in data['ats_vocabulary']
assert 'required_job_vocabulary' in data['ats_vocabulary']
print('ATS Vocabulary Partitioning: Verified')
"
```
