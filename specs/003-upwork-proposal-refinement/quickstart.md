# Quickstart Validation Guide: Upwork Proposal Generator (V3.1)

## Overview

This guide describes how to run and validate the V3.1 Evidence Attribution, Composition & Claim Projection Integrity refinement across qualification, proposal projection, screening generation, and validation passes.

---

## Prerequisites

1. Active python environment with pytest and PyYAML installed.
2. Target position configuration in `config/target-position/upwork-senior-agentic-ai-architect.md` or `config/target-position/upwork-business-systems-technology-architecture-consultant.md`.
3. Canonical OKF evidence graph in `out/okf/`.

---

## 1. Running the Pipeline End-to-End

To execute qualification, proposal generation, and validation for an Upwork opportunity target:

```bash
python3 scripts/generate_upwork_playbook.py --target upwork-senior-agentic-ai-architect
```

Or for business systems architecture consultant:

```bash
python3 scripts/generate_upwork_biz_systems_playbook.py
```

---

## 2. Running Automated Regression Tests

To run the full Pytest regression suite verifying candidate-agnostic attribution boundaries, production claim grounding, composition rules, screening consistency, and V2.0/V2.1 backwards compatibility:

```bash
pytest tests/test_upwork_proposal_generator.py -v
```

---

## 3. Validating Candidate-Agnostic & Fixture Scenarios

### Candidate-Agnostic Production Assessment (FR-063, SC-038)
1. Verify that `scripts/upwork_validator.py` and skill prompts contain zero hardcoded employer or project names (e.g. no literal string matching for "WPP" or "CAS" in production logic).
2. Confirm validation logic evaluates generic metadata fields (`candidate_contribution`, `system_production_status`, `candidate_production_deployment_status`).

### Golden Scenario 1 — Enterprise Architecture vs. Personal Lab Test Fixture (FR-058)
1. Execute qualification against test dataset containing enterprise production platform architecture evidence (`OrgAlpha`) and personal lab coding evidence (`ProjectBeta`).
2. Inspect `out/upwork-senior-agentic-ai-architect/runtime/upwork-qualification.yaml`.
3. Verify `candidate_contribution: architected` for enterprise platform, `candidate_production_deployment_status: unverified`, and `requirement_qualification_status: PARTIALLY_SUPPORTED`.
4. Inspect generated `upwork-qualification-report.md` and `upwork-screening-answers.md`.
5. Confirm zero instances of unverified production deployment claims.

### Golden Scenario 2 — Project In Progress at Departure Test Fixture (FR-059)
1. Execute qualification for enterprise project evidence in active implementation upon departure.
2. Confirm candidate claims architecture leadership and design before departure, but zero assertions of live production deployment.

---

## 4. Validating Output Artifacts

- **Qualification Context**: `out/<target-slug>/runtime/upwork-qualification.yaml`
- **Proposal Draft**: `out/<target-slug>/upwork-qualification-report.md`
- **Evidence Gap Report**: `out/<target-slug>/upwork-evidence-gaps.md`
- **Screening Answers**: `out/<target-slug>/upwork-screening-answers.md`
- **Work Samples**: `out/<target-slug>/upwork-work-samples.md`
- **Validation Report**: `out/<target-slug>/runtime/upwork-validation-report.yaml`
