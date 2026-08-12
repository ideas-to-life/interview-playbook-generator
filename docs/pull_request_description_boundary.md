# PR: Implement Projection Strategy Evidence Boundary & Transferability Refinement

## Summary of Changes

This Pull Request implements the refinement specified in [`docs/requirements-spec/refinement-spec-boundary-transferability.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/docs/requirements-spec/refinement-spec-boundary-transferability.md). It refines the Projection Strategy layer so that target-role requirements cannot be promoted into candidate capabilities unless independently supported by canonical evidence.

The system enforces a strict 3-layer semantic separation:
1. **Target Requirement**: What the organisation needs (e.g. `ccoe_establishment`).
2. **Candidate Evidence**: What the candidate has actually demonstrated (e.g. `enterprise_architecture_operating_model`).
3. **Projection Positioning**: How demonstrated experience is framed (e.g. "Apply EA operating-model and governance experience to CCoE-aligned initiatives").

---

## Key Deliverables

### 1. Specification & Governing Principles
- **[`docs/superpowers/specs/2026-08-12-projection-strategy-boundary-spec.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/docs/superpowers/specs/2026-08-12-projection-strategy-boundary-spec.md)**: Feature specification detailing 3-layer semantic separation, restrictive `lead_with` rules, extended `bridge` schema, domain substitution prevention, and end-to-end validation.
- **[`AGENTS.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/AGENTS.md)**: Added permanent governing principles:
  - **Target requirements vs Candidate evidence**: Target requirements describe what the client needs; candidate evidence describes what the candidate has done. Target requirements must never become candidate evidence or candidate positioning unless independently supported by canonical evidence.
  - **Transferable framing over domain substitution**: When target requirements are adjacent to, but not directly evidenced by, candidate experience, the projection must use explicit transferable framing rather than domain substitution.
  - **Journey vs Destination Invariant**: The target defines the destination; the evidence defines the journey. Projection may explain why the candidate’s demonstrated experience makes the destination credible, but it must never rewrite the journey as though the candidate has already reached it.

### 2. Skill Instruction & Schema Updates
- **[`skills/projection-strategy-generator/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/projection-strategy-generator/SKILL.md)**:
  - Restricted `lead_with` strictly to evidence-supported candidate capabilities (`DIRECT` or `STRONG_RELEVANT`).
  - Extended `bridge` schema in `projection-strategy.yaml` mapping `target_capability`, `candidate_evidence`, `relationship`, `rationale`, and `framing`.
- **[`skills/archetype-fit-validator/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/archetype-fit-validator/SKILL.md)**: Added checks for Target Requirement Contamination in `lead_with` and domain substitution.

### 3. Automated End-to-End Test Suite
- **[`tests/test_boundary_transferability.py`](file:///Users/avfranco/GitHub/interview-playbook-generator/tests/test_boundary_transferability.py)**: Automated end-to-end tests verifying:
  - `lead_with` restricted to evidence-supported candidate capabilities.
  - Extended `bridge` schema mappings (`target_capability`, `candidate_evidence`, `relationship`, `rationale`, `framing`).
  - Contamination check asserting zero unsupported target-derived claims across presentation view files.
  - Enterprise Cloud Architect regression verifying CCoE establishment is classified as `TRANSFERABLE` / `ADJACENT` while overall fit remains `Strong Fit`.

---

## Verification Results

All 98 unit, integration, and lint tests pass cleanly:

```bash
pytest
============================== 98 passed in 1.87s ==============================
```

```bash
pytest tests/test_lint.py
============================== 7 passed in 0.04s ===============================
```

---

## How to Test

1. Switch to branch: `git checkout feature/projection-strategy-boundary`
2. Run pytest suite: `pytest`
3. Run boundary transferability tests: `pytest tests/test_boundary_transferability.py`
