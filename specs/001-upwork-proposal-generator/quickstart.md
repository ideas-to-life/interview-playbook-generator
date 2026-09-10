# Quickstart & Runnable Validation Scenarios: Upwork Proposal Generator (V2.0)

## Overview

This guide documents runnable validation scenarios verifying that the `upwork-qualification` runtime skill, `upwork-proposal` projection skill, and `projection-validator` enforcement gate satisfy all V2.0 Evidence Integrity & Production Qualification requirements.

---

## Runnable Validation Scenarios

### Scenario 1: Unverified WPP Production Evidence on Explicit Dealbreaker Requirement (`DO NOT APPLY`)

**Prerequisites**:
- Target specification [`config/target-position/upwork-senior-agentic-ai-architect.md`](config/target-position/upwork-senior-agentic-ai-architect.md) requires *"real company in production"* implementation experience (explicit dealbreaker).
- Canonical evidence card [`wpp-agentic-ai-platform.md`](out/okf/evidence/wpp-agentic-ai-platform.md) has `environment: prototype` and `production_verified: false`.

**Execution Command**:
```bash
pyenv exec python3 scripts/generate_upwork_playbook.py
```

**Expected Outcome**:
- `out/upwork-senior-agentic-ai-architect/runtime/upwork-qualification.yaml`:
  - `decision: "DO NOT APPLY"`
  - `proposal_generation: "blocked"`
  - `hard_requirements[0].production_status: "unknown"` (or `verified_non_production`)
  - `hard_requirements[0].status: "not_met"`
- `out/upwork-senior-agentic-ai-architect/upwork-proposal.md`:
  - Renders a **Gate Report** displaying Decision (`DO NOT APPLY`), Blocking Requirement, Available Evidence, and Evidence Gap.
  - Does NOT contain a submission-ready application proposal draft.
- `out/upwork-senior-agentic-ai-architect/upwork-screening-answers.md`:
  - Does NOT render application drafts for screening questions.

---

### Scenario 2: Verified Production Evidence on Target Organisation (`APPLY`)

**Prerequisites**:
- Canonical evidence card `wpp-agentic-ai-platform.md` updated with `environment: production`, `production_verified: true`, `implementation_role: lead_architect`, and `organisation.id: emp-wpp-media-2`.

**Execution Command**:
```bash
pyenv exec python3 scripts/generate_upwork_playbook.py
```

**Expected Outcome**:
- `out/upwork-senior-agentic-ai-architect/runtime/upwork-qualification.yaml`:
  - `decision: "APPLY"`
  - `proposal_generation: "allowed"`
  - `hard_requirements[0].production_status: "verified_production"`
  - `hard_requirements[0].status: "met"`
- `out/upwork-senior-agentic-ai-architect/upwork-proposal.md`:
  - Renders a 6-part submission-ready clean executive proposal (350-500 words target).
- `out/upwork-senior-agentic-ai-architect/runtime/projection-validation-report.yaml`:
  - `employment_integrity.status: "PASS"`
  - `upwork_validation.status: "PASS"`

---

### Scenario 3: Cross-Organisation Evidence Isolation (`DO NOT APPLY`)

**Prerequisites**:
- Target requirement bound to `organisation.id: emp-wpp-media-2`.
- Canonical evidence includes Personal CAS card (`organisation.id: personal-cas`, `production_verified: true`) and WPP card (`organisation.id: emp-wpp-media-2`, `production_verified: false`).

**Expected Outcome**:
- `upwork-qualification` refuses to pool the Personal CAS production evidence into WPP requirement `req-1`.
- `req-1` production status remains `unknown` for WPP, yielding `decision: "DO NOT APPLY"`.

---

### Scenario 4: Negative Inference Prohibition on Repository Names (`DO NOT APPLY`)

**Prerequisites**:
- Ingested source repository contains path `pca-productionagents-a2a`, but OKF evidence card frontmatter has `production_verified: false`.

**Expected Outcome**:
- `upwork-qualification` ignores `"productionagents"` in repo string.
- `production_status` remains `unknown`, preventing false-positive `verified_production` qualification.

---

## Automated Test Execution

Run the complete regression test suite:

```bash
pyenv exec pytest tests/test_upwork_proposal_generator.py tests/test_projection_validator.py
```

All test cases (including the 10 V2.0 regression scenarios) MUST pass.
