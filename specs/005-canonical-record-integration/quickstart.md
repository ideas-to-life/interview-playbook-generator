# Quickstart Validation Guide: Canonical Career Record Integration

**Feature**: `005-canonical-record-integration`  
**Status**: Ready for Validation  
**Date**: 2026-09-18  

This guide defines end-to-end verification steps to validate that canonical career facts are loaded, quarantine is excluded, title/degree inflation is prevented, and all 8 forensic regression scenarios pass.

---

## 1. Prerequisites

1. Ensure the Python virtual environment is activated:
   ```bash
   source .venv/bin/activate
   ```
2. Confirm the canonical career record is present:
   ```bash
   ls -la /Users/avfranco/GitHub/mind-palace/canonical/career-record.yaml
   ```
3. Verify dependencies:
   ```bash
   pip install pytest pyyaml
   ```

---

## 2. Validation Scenarios

### Step 1: Verify Canonical Career Record Discovery & Validation
Execute the canonical loader to confirm schema validity, zero-latency parsing, and fail-fast behavior:

```bash
python3 scripts/canonical_loader.py
```
**Expected Outcome**:
- Exits with status `0`.
- Outputs: `Canonical record loaded successfully: 11 career entries, 2 education records, 5 certifications`.

Test fail-fast on malformed/missing record:
```bash
python3 scripts/canonical_loader.py --test-missing
```
**Expected Outcome**:
- Immediately halts with exit code `1` within <1s: `FATAL: Canonical career record not found or invalid YAML. Refusing to fallback on unverified data.`

---

### Step 2: Validate Quarantine Exclusion & Employment Ingestion
Run portfolio ingestion:

```bash
python3 scripts/ingest_portfolio.py
```

**Expected Outcome**:
1. Zero quarantined files in `out/okf/sources/`:
   ```bash
   grep -rn "quarantine" out/okf/sources/ || echo "Quarantine clean!"
   ```
2. `out/okf/employment-records.yaml` generated exclusively from `career-record.yaml`:
   - No article titles (e.g. `Learn-it-all-Do-it-all` is absent).
   - Contains formal BBC title `Lead Enterprise Architect - Technology Transformation Group`.
   - Distinct entries for Compugraf (consultancy) and Souza Cruz (client).

---

### Step 3: Run the Forensic Regression Test Suite
Execute the dedicated regression test suite covering Scenarios 1 through 8:

```bash
pytest -v tests/test_canonical_record_regression.py
```

**Expected Outcome**:
- All 8 scenarios pass:
  - `test_scenario_1_education_msc_refutation`: PASS
  - `test_scenario_2_bbc_formal_title_preservation`: PASS
  - `test_scenario_3_bbc_acting_scope_distinction`: PASS
  - `test_scenario_4_bat_complete_chronology`: PASS
  - `test_scenario_5_compugraf_souza_cruz_relationship`: PASS
  - `test_scenario_6_wpp_mostelli_distinction`: PASS
  - `test_scenario_7_quarantine_exclusion`: PASS
  - `test_scenario_8_unsupported_enhancement_rejection`: PASS

---

### Step 4: Validate Factual Selection & Conflict Audit Artifacts
Run runtime analysis against a target opportunity:

```bash
python3 scripts/canonical_selector.py --target lseg-director-enterprise-architecture
```

**Expected Outcome**:
1. `out/lseg-director-enterprise-architecture/runtime/canonical-selection.yaml` is created with mapped `CAR-xx` IDs.
2. `out/lseg-director-enterprise-architecture/runtime/canonical-conflict-report.yaml` logs detected discrepancies from secondary files without halting execution.

---

### Step 5: Validate Projection Generation & Automated Sanitization
Generate an executive resume and verify deterministic validation:

```bash
python3 scripts/employment_validator.py out/lseg-director-enterprise-architecture/resume-executive.md
```

**Expected Outcome**:
- Validation report shows `status: PASS`.
- If any simulated discrepancy was introduced in draft copy, automated sanitization rewrote the text to the canonical fact and logged an alert in `out/lseg-director-enterprise-architecture/runtime/projection-validation-report.yaml`.
