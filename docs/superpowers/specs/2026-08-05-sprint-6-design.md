# Sprint 6 Specification: Opportunity Archetype & Market-Fit Intelligence

## 1. Objective

Evolve the Career Intelligence Platform from assessing simple requirement coverage to assessing **Opportunity Archetype & Market Fit**. The platform must answer: *"What kind of professional is this organization actually trying to hire, and does the canonical evidence demonstrate that archetype?"*

This prevents misleadingly high alignment scores when a profile has high requirement coverage (e.g. AI architecture) but an archetype mismatch (e.g. Enterprise AI Architect vs. hands-on AI Automation Builder in an eCommerce agency).

## 2. Tech Stack & Dependencies

- **Runtime**: Markdown skill files (`skills/<skill-name>/SKILL.md`), YAML schema definitions, and Python evaluation scripts.
- **Testing**: `pytest`, `pyyaml`, Python 3.10+
- **Data Formats**: YAML for runtime execution context, Markdown for canonical OKF documents and executive projections.

## 3. Commands

- **Run Full Pipeline**: `/skill playbook-orchestrator` (or `python scripts/run_pipeline.py`)
- **Run Unit & Integration Tests**: `pytest`
- **Run Sprint 6 Golden Criteria Tests**: `pytest tests/test_v06_success_criteria.py`
- **Run Lint Checks**: `pytest tests/test_lint.py`

## 4. Project Structure

```
skills/
├── archetype-classifier/           → FR-1: Classifies primary/secondary professional archetype
├── archetype-fit-evaluator/        → FR-2, FR-3, FR-8, FR-9: Evaluates 4 fit dimensions & selection recommendation
├── gap-classifier/                 → FR-4, FR-5: Categorises gaps (7 types) and severity/recoverability
├── projection-strategy-generator/  → FR-7: Generates runtime projection-strategy.yaml
├── archetype-fit-validator/        → FR-6, FR-19: Enforces anti-overpositioning guardrails
├── market-feedback-evaluator/      → FR-10, FR-11, FR-12, FR-13, FR-14: Processes market feedback & compares predictions
└── playbook-orchestrator/          → Extended to orchestrate Sprint 6 Skills

out/<target-slug>/runtime/
├── opportunity-analysis.yaml       → Standard requirement analysis
├── archetype-analysis.yaml         → FR-1: Target opportunity archetype taxonomy output
├── gap-analysis.yaml               → FR-4, FR-5: Classified gaps and severities
├── projection-strategy.yaml        → FR-7: Shared strategy for downstream projections
├── opportunity-fit-report.yaml     → FR-8, FR-9: Multidimensional matrix & selection recommendation
└── projection-validation-report.yaml → Extended with archetype overpositioning checks

evaluation/
└── opportunities/                  → FR-10: Market feedback capture YAML files (e.g. vervaunt-head-of-ai.yaml)

tests/
├── fixtures/                       → Test fixtures for Vervaunt and AI CoE opportunities
└── test_v06_success_criteria.py    → Golden test suite verifying Vervaunt & AI CoE regression
```

## 5. Code & Skill Style

- **Skill Documents (`SKILL.md`)**: Must begin with standard YAML frontmatter (`name`, `description`). Must contain explicit input/output contracts, schema definitions, and execution instructions.
- **YAML Output Layout**: Clean, human-readable YAML with clear top-level keys.
- **Python Tests**: Declarative assertion functions with descriptive failure messages.

```python
# Example test style for Sprint 6
def test_vervaunt_archetype_classification():
    analysis = load_yaml("out/vervaunt-head-of-ai/runtime/archetype-analysis.yaml")
    assert analysis["opportunity_archetype"]["primary"] in [
        "ai_automation_builder",
        "agency_ai_leader",
    ]
    assert analysis["opportunity_archetype"]["confidence"] in ["high", "medium"]
```

## 6. Testing Strategy

1. **Unit Tests**:
   - Verify YAML schemas for `archetype-analysis.yaml`, `gap-analysis.yaml`, `projection-strategy.yaml`, `opportunity-fit-report.yaml`, and `market-feedback.yaml`.
   - Verify `anti-overpositioning-guardrail` correctly triggers warnings when claims exceed evidence.
2. **Golden Integration Tests (`test_v06_success_criteria.py`)**:
   - **Vervaunt Fixture**: System independently identifies `ai_automation_builder` / `agency_ai_leader` archetype with gaps in eCommerce, Shopify, n8n/Zapier, yielding `Moderate` archetype fit *prior* to receiving market feedback.
   - **AI CoE Fixture (Regression)**: System identifies `enterprise_ai_architect` / `ai_coe_architect` archetype with `Strong` fit, proving the platform does not penalise Enterprise Architecture when that archetype is actually desired.

## 7. Boundaries

- **Always**:
  - Preserve OKF canonical bundle immutability (`okf/` and `out/okf/`).
  - Distinguish genuine experience gaps from positioning gaps.
  - Require evidence attribution (`[^source-id]`) for claims.
- **Ask First**:
  - Modifying canonical OKF schema or existing Sprint 1–5 skill output schemas.
  - Adding external Python package dependencies beyond `pytest` and `pyyaml`.
- **Never**:
  - Fabricate missing experience or metrics to compensate for archetype gaps.
  - Allow market feedback to automatically mutate canonical career knowledge or identity.
  - Treat high Brand/Projection Validation scores as equivalent to high Hiring Alignment.

## 8. Success Criteria (Reframed Requirements)

- [ ] **SC-1 (Archetype Classification)**: `archetype-classifier` output classifies primary & secondary archetypes based on role responsibilities rather than job title alone.
- [ ] **SC-2 (4-Dimension Fit Model)**: `archetype-fit-evaluator` assesses fit across Capability, Domain, Ecosystem/Tooling, and Operating-Context.
- [ ] **SC-3 (Gap & Severity Classification)**: `gap-classifier` categorises all identified gaps into 7 categories and assigns materiality, confidence, and recoverability.
- [ ] **SC-4 (Projection Strategy)**: `projection-strategy-generator` emits `projection-strategy.yaml` defining `lead_with`, `de_emphasise`, `bridge`, and `prohibit_claims`.
- [ ] **SC-5 (Anti-Overpositioning Guardrail)**: `archetype-fit-validator` flags overpositioning warnings when projections claim experience not backed by canonical evidence for the target archetype.
- [ ] **SC-6 (Market Feedback Evaluation)**: `market-feedback-evaluator` compares captured hiring feedback (`evaluation/opportunities/*.yaml`) against predictions without mutating canonical knowledge.
- [ ] **SC-7 (Golden Test - Vervaunt)**: Given the Vervaunt JD and pre-feedback candidate portfolio, system rates archetype fit as `Moderate` and flags eCommerce/Shopify/n8n gaps.
- [ ] **SC-8 (Golden Test - AI CoE Regression)**: Given an Enterprise AI CoE JD, system rates archetype fit as `Strong` and confirms high alignment for Enterprise Architecture & governance.

## 9. Open Questions

- None at present.
