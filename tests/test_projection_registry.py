# tests/test_projection_registry.py
import os
import yaml
import pytest

GOLDEN = "tests/golden/projection-registry/projection-registry.yaml"


def test_skill_exists():
    path = "skills/projection-registry/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: projection-registry" in content


def test_golden_projection_registry_schema():
    assert os.path.exists(GOLDEN)
    with open(GOLDEN, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("version") == "0.4"
    assert "registered_projections" in data
    projections = data["registered_projections"]
    assert isinstance(projections, list)
    assert len(projections) >= 6

    names = [p["name"] for p in projections]
    assert "resume-projection" in names
    assert "cover-letter-projection" in names
    assert "linkedin-projection" in names
    assert "opportunity-alignment-view" in names
    assert "executive-brief-view" in names
    assert "playbook-assembler" in names
