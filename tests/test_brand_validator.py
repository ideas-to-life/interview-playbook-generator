# tests/test_brand_validator.py
import os
import yaml
import pytest

GOLDEN = "tests/golden/brand-validator/brand-validation-report.yaml"


def test_skill_exists():
    path = "skills/brand-validator/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: brand-validator" in content


def test_golden_brand_validation_report_schema():
    assert os.path.exists(GOLDEN)
    with open(GOLDEN, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("version") == "0.5"
    assert data.get("brand_alignment_status") == "PASSED"
    assert "metrics" in data
    assert "evaluated_projections" in data

    metrics = data["metrics"]
    assert "voice_tone_consistency" in metrics
    assert "positioning_statement_alignment" in metrics
    assert "narrative_messaging_reuse" in metrics
    assert "story_asset_traceability" in metrics


def test_employment_validation_brand_integration():
    from scripts.employment_validator import validate_employment_history
    content = "### BBC Studios\n**Lead Enterprise Architect**\n*Oct 2021 – Nov 2025*"
    res = validate_employment_history(content)
    assert res["status"] == "PASS"


