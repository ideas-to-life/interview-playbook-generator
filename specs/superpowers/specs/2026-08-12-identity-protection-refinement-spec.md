# Spec: Identity Protection & Canonical Archetype Refinement

## Objective

Refine the Career Projection Platform so that target-role tailoring:
1. Preserves the candidate’s canonical professional identity (`Enterprise Architect / Transformation & AI Advisor`) and career trajectory;
2. Adapts emphasis, terminology, and evidence to the target opportunity without letting the target job title, terminology, or capability emphasis redefine the candidate’s primary professional archetype;
3. Prevents adjacent or transferable experience from being promoted into unsupported primary expertise or leadership titles;
4. Enforces 5-tier capability classification (`CORE`, `STRONG`, `RELEVANT`, `ADJACENT`, `GAP`);
5. Validates against Identity Drift / Over-Positioning in post-generation checks;
6. Enforces regression testing on the `enterprise-cloud-architect` (Enterprise Cloud Architect / CCoE) case.

## Governing Principles

1. **Evidence precedes claims**: Evidence determines what Alexandre can credibly claim.
2. **Canonical identity protection**: Canonical identity determines who Alexandre is; the target opportunity determines which of those truths should be emphasised.
3. **Core Invariant**:
   `Projected Identity = Canonical Professional Identity + Target-Relevant Emphasis - Irrelevant Detail`
   (Tailor the expression of the candidate to the opportunity, never the identity of the candidate to the opportunity).

## Tech Stack & Commands

- **Language / Framework**: Python 3.13, Pytest, YAML, Markdown Skills specification.
- **Commands**:
  ```bash
  Test: pytest
  Lint: python -m pytest tests/test_lint.py
  Single Test: pytest tests/test_ea_cloud_refinement_regression.py
  ```

## Project Structure & Touched Files

```
skills/
├── archetype-classifier/SKILL.md         → Refine archetype classification logic
├── projection-strategy-generator/SKILL.md → Support 5-tier classification & identity protection constraints
├── headline-generator / resume-projection/SKILL.md → Explicit headline & exec summary identity protection rules
├── archetype-fit-validator/SKILL.md      → Add Identity Drift & Over-Positioning detection rules
└── playbook-orchestrator/SKILL.md       → Integrate post-generation identity drift check & fallback

AGENTS.md                                → Add governing principles
docs/superpowers/specs/2026-08-12-identity-protection-refinement-spec.md → This specification document
tests/test_ea_cloud_refinement_regression.py → Mandatory regression test for Enterprise Cloud Architect / CCoE
```

## Capability Classification Rules (5-Tier)

1. **CORE / STRONG**: Primary positioning, headline framing, lead executive summary, anchor experience bullets.
2. **RELEVANT**: Secondary positioning, executive summary support, targeted experience bullets.
3. **ADJACENT**: Demonstrates transferable capability & context. MUST NOT become primary identity, headline title, leadership title, or long-duration claim.
4. **GAP**: MUST NOT be represented as demonstrated experience.

## Identity Drift & Post-Generation Validation

Post-generation validation rule (`archetype-fit-validator`):
- Checks if projected CV or headline makes the candidate appear to have a materially different primary professional identity (e.g., claiming 15+ years CCoE leadership or "Enterprise & Cloud Architect | CCoE Leader" when canonical identity is EA / Transformation Advisor).
- When Identity Drift is detected: Emits a `WARNING` or `FAIL` status in `archetype-fit-validator` findings with actionable diagnosis (`identity_drift` finding type, specifying detected signal and affected positioning elements) so runtime/orchestrator can flag or re-trigger positioning regeneration while preserving target-relevant evidence.
- Potential detection signals include:
  - Headline dominated by target title displacing candidate archetype
  - Target domain appearing as primary profession
  - Unsupported leadership titles (e.g. "CCoE Leader" vs "contributed to / advised")
  - Unsupported duration claims (e.g. 15+ years in target domain)
  - Target-specific expertise outranking canonical core expertise
  - Disappearance of canonical differentiators

## Testing Strategy

- **Unit & Integration Tests**: `pytest` test suite verifying:
  - Candidate Archetype vs Target Archetype explicit separation in `archetype-analysis.yaml` & `projection-strategy.yaml`.
  - Headline generator rule compliance.
  - Duration and leadership integrity checks.
  - Identity drift detector detection of over-positioning.
- **Regression Test**: `tests/test_ea_cloud_refinement_regression.py` testing the `enterprise-cloud-architect` opportunity context.

## Success Criteria

1. Canonical professional identity remains immutable during projection.
2. Target role archetype is explicitly distinguished from candidate archetype (`Candidate Archetype`, `Target Role Archetype`, `Projection Positioning`).
3. 5-tier classification (`CORE`, `STRONG`, `RELEVANT`, `ADJACENT`, `GAP`) strictly enforced.
4. Duration claims remain evidence-backed (no inferring 15+ years from target terminology).
5. Leadership claims remain evidence-backed (led vs designed vs advised vs supported).
6. Headline generation prioritizes: 1) Canonical identity, 2) Strong target differentiators, 3) Relevant terminology, 4) Keywords.
7. Post-generation identity drift validation detects over-positioning.
8. Enterprise Cloud Architect / CCoE case passes as a mandatory regression test.

## Boundaries

- **Always do**: Run `pytest` before any commit; ground every claim in canonical OKF evidence.
- **Ask first**: Schema alterations to `okf/` canonical bundle files.
- **Never do**: Fabricate experience, tenure, metrics, or titles; allow target job descriptions to redefine candidate's primary archetype.
