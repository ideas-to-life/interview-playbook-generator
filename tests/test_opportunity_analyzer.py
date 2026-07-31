# tests/test_opportunity_analyzer.py
import os
import yaml
import pytest

GOLDEN = "tests/golden/opportunity-analyzer/opportunity-analysis.yaml"


def test_skill_exists():
    path = "skills/opportunity-analyzer/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: opportunity-analyzer" in content


def test_golden_opportunity_analysis_schema():
    assert os.path.exists(GOLDEN)
    with open(GOLDEN, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("version") == "0.4"
    assert "target_opportunity" in data
    assert "hiring_goals" in data
    assert "executive_positioning" in data
    assert "capability_priorities" in data
    assert "behaviour_expectations" in data
    assert "ats_vocabulary" in data
    assert "coverage_matrix" in data

    # Check ATS Vocabulary buckets
    ats = data["ats_vocabulary"]
    assert "mandatory" in ats
    assert "strong" in ats
    assert "optional" in ats

    # Check Coverage Matrix structure
    matrix = data["coverage_matrix"]
    assert isinstance(matrix, list)
    assert len(matrix) >= 2
    for entry in matrix:
        assert "requirement" in entry
        assert "coverage" in entry
        assert "confidence" in entry
        assert "primary_evidence" in entry
        assert "capabilities" in entry
