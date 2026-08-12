# PR: Implement Identity Protection Refinement & Automated Regression Test Suite

## Summary of Changes

This Pull Request implements the requirements specified in [`docs/requirements-spec/refinement-spec-run-ea-cloud.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/docs/requirements-spec/refinement-spec-run-ea-cloud.md) to ensure target-role tailoring:
1. **Preserves candidate canonical identity**: Adapts emphasis, terminology, and evidence to the target opportunity without letting the target job title, terminology, or capability emphasis redefine the candidate’s primary professional archetype (`Enterprise Architect / Transformation & AI Advisor`).
2. **Prevents over-positioning**: Prevents adjacent or transferable experience (e.g. CCoE governance or cloud modernisation) from being promoted into unsupported primary expertise or leadership titles (e.g. claiming 15+ years CCoE leadership or "CCoE Leader" as a primary professional title).
3. **Enforces evidence fidelity**: Caps claim strength and duration based strictly on source evidence in `okf/`.

---

## Key Deliverables

### 1. Specification & Governing Principles
- **[`docs/superpowers/specs/2026-08-12-identity-protection-refinement-spec.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/docs/superpowers/specs/2026-08-12-identity-protection-refinement-spec.md)**: Feature specification detailing the 6 core areas, 5-tier classification rules, duration/leadership integrity rules, and identity drift validation mechanism.
- **[`AGENTS.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/AGENTS.md)**: Updated permanent governing principles with the Identity Preservation Invariant:
  $$ \text{Projected Identity} = \text{Canonical Professional Identity} + \text{Target-Relevant Emphasis} - \text{Irrelevant Detail} $$
  *(Tailor the expression of the candidate to the opportunity, never the identity of the candidate to the opportunity).*

### 2. Skill Instruction & Schema Updates
- **[`skills/archetype-classifier/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/archetype-classifier/SKILL.md)**: Added explicit distinction between `candidate_archetype`, `target_role_archetype`, and `projection_positioning` in `archetype-analysis.yaml`. Enforces that the target archetype must never replace the candidate's canonical primary identity.
- **[`skills/projection-strategy-generator/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/projection-strategy-generator/SKILL.md)**: Implemented 5-tier capability classification (`CORE`, `STRONG`, `RELEVANT`, `ADJACENT`, `GAP`), duration integrity constraints (prohibiting unbacked duration claims like "15+ years building CCoEs"), and leadership verb strength integrity (`led`, `established`, `designed`, `contributed to`, `advised`, `supported`).
- **[`skills/resume-projection/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/resume-projection/SKILL.md)**: Defined strict headline priority (`Canonical Identity` $\rightarrow$ `Differentiators` $\rightarrow$ `Target Terminology` $\rightarrow$ `Keywords`) and executive summary hierarchy (`EA` $\rightarrow$ `Transformation/Governance` $\rightarrow$ `Cloud Modernisation` $\rightarrow$ `AI`).
- **[`skills/archetype-fit-validator/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/archetype-fit-validator/SKILL.md)**: Added `identity_drift` finding type and schema to flag over-positioning when target title displaces candidate archetype or unsupported duration/leadership claims are made.

### 3. Automated Test & Regression Suite
- **[`tests/test_ea_cloud_refinement_regression.py`](file:///Users/avfranco/GitHub/interview-playbook-generator/tests/test_ea_cloud_refinement_regression.py)**: 9 comprehensive automated tests verifying:
  - Canonical identity protection & archetype distinction.
  - 5-tier capability classification constraint rules.
  - Duration and leadership integrity prohibitions.
  - Headline priority validation rules.
  - Executive summary hierarchy preservation.
  - Post-generation `identity_drift` validation detection.

---

## Verification Results

All 85 unit, integration, and lint tests pass cleanly:

```bash
pytest
============================== 85 passed in 1.24s ==============================
```

```bash
pytest tests/test_lint.py
============================== 7 passed in 0.03s ===============================
```

---

## How to Test

1. Switch to branch: `git checkout feature/identity-protection-refinement`
2. Run pytest suite: `pytest`
3. Run the specific EA Cloud regression test suite: `pytest tests/test_ea_cloud_refinement_regression.py`
