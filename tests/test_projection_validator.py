# tests/test_projection_validator.py
import os
import yaml
import pytest

GOLDEN = "tests/golden/projection-validator/projection-validation-report.yaml"


def test_skill_exists():
    path = "skills/projection-validator/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: projection-validator" in content


def test_golden_validation_report_schema():
    assert os.path.exists(GOLDEN)
    with open(GOLDEN, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("version") == "0.4"
    assert data.get("overall_status") == "PASSED"
    assert "metrics" in data
    assert "evaluated_projections" in data

    metrics = data["metrics"]
    assert "evidence_traceability" in metrics
    assert "capability_alignment" in metrics
    assert "ats_vocabulary_coverage" in metrics
    assert "length_budget_compliance" in metrics
