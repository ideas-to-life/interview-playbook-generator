# PR: Implement Claim Strength & Evidence Scope Validation Refinement

## Summary of Changes

This Pull Request implements the refinement specified in [`docs/requirements-spec/refinement-spec-claim-evidence-validation.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/docs/requirements-spec/refinement-spec-claim-evidence-validation.md). It strengthens the Career Projection Generator so that generated claims across resumes, cover letters, and briefs are constrained by the actual ownership, scope, domain, specificity, duration, and seniority supported by canonical evidence in `okf/`.

The system prevents semantic amplification where evidence supporting contribution to a capability is projected as leadership, ownership, or establishment of that capability.

---

## Key Deliverables

### 1. Specification & Governing Principles
- **[`docs/superpowers/specs/2026-08-12-claim-evidence-validation-spec.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/docs/superpowers/specs/2026-08-12-claim-evidence-validation-spec.md)**: Feature specification detailing the 6 core areas, claim strength hierarchy, claim scope vector model ($ClaimScope \le EvidenceScope$), high-risk verb protection, automatic verb downgrading, and validation report schema.
- **[`AGENTS.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/AGENTS.md)**: Added permanent governing principles:
  - **Evidence relevance does not imply evidence equivalence**: A claim may only be generated at the level of ownership, scope, specificity, duration and seniority explicitly supported by its evidence.
  - **No inferred leadership from contribution**: When evidence supports contribution to a capability, the system must not infer leadership, ownership, establishment, or end-to-end responsibility for that capability.
  - **Project relevance aggressively, project responsibility conservatively**.

### 2. Skill Instruction & Schema Updates
- **[`skills/projection-strategy-generator/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/projection-strategy-generator/SKILL.md)**: Added Claim Strength Bounds ($\text{CONTRIBUTED} \rightarrow \text{SUPPORTED} \rightarrow \text{ADVISED} \rightarrow \text{DESIGNED} \rightarrow \text{LED} \rightarrow \text{OWNED} \rightarrow \text{ESTABLISHED}/\text{TRANSFORMED}$) and vector scope limits.
- **[`skills/projection-validator/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/projection-validator/SKILL.md)**: Added Claim Scope & Strength Validation metric ($ClaimScope \le EvidenceScope$) emitting `PASS`, `DOWNGRADE`, and `REJECT` finding statuses.
- **[`skills/archetype-fit-validator/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/archetype-fit-validator/SKILL.md)**: Added checks for Claim Scope Vector violations and unbacked high-risk verbs (`Led`, `Owned`, `Established`, `Built`, `CCoE Leader`) or "from scratch" claims.
- **[`skills/resume-projection/SKILL.md`](file:///Users/avfranco/GitHub/interview-playbook-generator/skills/resume-projection/SKILL.md)**: Added rules for automatic claim verb downgrading (replacing over-strength verbs like "Established CCoE" with "Contributed to CCoE governance") and transferable domain framing (framing adjacent domain experience as *transferable*, e.g., "Applied EA governance experience to CCoE initiatives" instead of domain substitution).

### 3. Automated Test Suite
- **[`tests/test_claim_evidence_validation.py`](file:///Users/avfranco/GitHub/interview-playbook-generator/tests/test_claim_evidence_validation.py)**: Automated regression tests verifying:
  - Section 18 Canonical Governing Examples (CCoE contribution vs establishment; EA operating model to CCoE transferability).
  - Duration integrity & 15+ year duration claim prohibitions.
  - High-risk verb & "from scratch" protection.
  - Automatic verb downgrading and claim rejection rules.
  - Validation report schema emission (`PASS`, `DOWNGRADE`, `REJECT`).

---

## Verification Results

All 94 unit, integration, and lint tests pass cleanly:

```bash
pytest
============================== 94 passed in 1.22s ==============================
```

```bash
pytest tests/test_lint.py
============================== 7 passed in 0.06s ===============================
```

---

## How to Test

1. Switch to branch: `git checkout feature/claim-evidence-validation`
2. Run pytest suite: `pytest`
3. Run claim evidence validation tests: `pytest tests/test_claim_evidence_validation.py`
