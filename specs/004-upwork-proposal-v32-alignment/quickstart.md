# Quickstart & Verification Guide: Upwork Proposal Generator (V3.2 Alignment)

## Overview

Provides end-to-end instructions for running the V3.2 Upwork proposal generation pipeline and verifying artifact compliance against contracts and regression test suites.

---

## Execution Instructions

### 1. Ingest Portfolio & Run Playbook Generator

```bash
# Ingest candidate portfolio sources
~/.pyenv/shims/python3 scripts/ingest_portfolio.py

# Run playbook generator for Upwork target opportunity
~/.pyenv/shims/python3 scripts/generate_upwork_biz_systems_playbook.py
```

---

## Artifact Verification

### 2. Verify Output File Locations & Modification Timestamps

```bash
ls -la out/upwork-business-systems-technology-architecture-consultant/
```

Confirm the presence of:
- `upwork-qualification-report.md` (Executive Proposal Cover Letter, 350–500 words)
- `upwork-screening-answers.md` (Screening Q&A responses only)
- `upwork-work-samples.md` (Work samples with project type tags)
- `upwork-evidence-gaps.md` (Evidence gap report)

---

### 3. Verify Proposal Content & Clean Prose

```bash
# Verify upwork-qualification-report.md contains Executive Proposal Cover Letter (not 3-line stub)
head -n 30 out/upwork-business-systems-technology-architecture-consultant/upwork-qualification-report.md

# Verify upwork-screening-answers.md contains NO proposal cover letter section
grep -i "Proposal Cover Letter" out/upwork-business-systems-technology-architecture-consultant/upwork-screening-answers.md || echo "Pass: No proposal cover letter in screening answers"
```

---

### 4. Run Automated Test Suite

```bash
# Execute full pytest suite including Upwork validator and regression tests
~/.pyenv/shims/pytest -v
```

Expected output: `151 passed` (or 151+ passed).
