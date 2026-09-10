# Quickstart & Validation Guide: Upwork Qualification and Proposal Generator

This guide describes how to run and validate the Upwork qualification and proposal projection feature end-to-end.

---

## 1. Prerequisites

Ensure target opportunity configuration in `config/config.yaml` or target position file specifies `target_type: upwork`:

```yaml
target_slug: "head-of-ai-upwork"
target_type: "upwork"
opportunity_source: "inputs/upwork-job-description.md"
```

Canonical OKF knowledge graph must exist in `out/okf/`.

---

## 2. Test Scenario 1: Reference `DO NOT APPLY` Test Case (Section 35)

### Setup
Target job requires:
> "Personal implementation of a production multi-agent or AI workforce system inside a real operating company."

Candidate evidence contains architecture/governance work in Prototype & Innovation, but no verified production multi-agent implementation inside a real company.

### Execution
Run the orchestrator pipeline:
```bash
/skill playbook-orchestrator
```

### Expected Outcome
1. `out/<target-slug>/runtime/upwork-qualification.yaml` returns `decision: DO NOT APPLY` and `proposal_generation: blocked`.
2. `out/<target-slug>/upwork-proposal.md` contains a concise **Gate Report**:
   - Decision: `DO NOT APPLY`
   - Blocking Requirement: "Personal implementation of production multi-agent system in a real company"
   - Evidence Gap: Prototype/governance evidence present, production implementation absent.
3. No submission-ready proposal or screening answers generated.

---

## 3. Test Scenario 2: Qualified `APPLY` Test Case (Section 36)

### Setup
Target job requires Enterprise AI architecture and governance advisor. Authoritative evidence explicitly supports production architecture, controls, and advisory experience.

### Execution
Run the orchestrator pipeline:
```bash
/skill playbook-orchestrator
```

### Expected Outcome
1. `out/<target-slug>/runtime/upwork-qualification.yaml` returns `decision: APPLY` and `proposal_generation: allowed`.
2. `out/<target-slug>/upwork-proposal.md` contains clean submission-ready proposal text (350-500 words) free of internal `[evidence]` tags or `[^source-id]` footnotes.
3. `out/<target-slug>/runtime/upwork-qualification.yaml` contains `claim_traceability` array verifying 100% of claims.
4. `out/<target-slug>/upwork-screening-answers.md` contains complete answers for all client screening questions.
5. `out/<target-slug>/upwork-work-samples.md` recommends up to 3 evidence-backed work samples.

---

## 4. Test Scenario 3: `CONDITIONAL` Test Case (Section 24)

### Setup
Target job requires specific cloud platform certification or tool tenure that is unverified in portfolio but candidate can confirm.

### Execution
Run the orchestrator pipeline:
```bash
/skill playbook-orchestrator
```

### Expected Outcome
1. `out/<target-slug>/runtime/upwork-qualification.yaml` returns `decision: CONDITIONAL` and `proposal_generation: allowed_with_conditions`.
2. `out/<target-slug>/upwork-proposal.md` displays an `[OPEN CONDITION: <fact>]` banner at top.
3. `out/<target-slug>/upwork-screening-answers.md` attaches explicit `[OPEN CONDITION: <fact>]` tags to affected questions.

---

## 5. Automated Validation & Test Suite

Run pytest to verify qualification rules, evidence integrity, and proposal constraints:

```bash
pytest tests/test_upwork_proposal_generator.py -v
```

Run projection validator:
```bash
/skill projection-validator
```
Inspect `out/<target-slug>/runtime/projection-validation-report.yaml` for validation metrics.
