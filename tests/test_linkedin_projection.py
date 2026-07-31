# tests/test_linkedin_projection.py
import os
import pytest

GOLDEN = "tests/golden/linkedin-projection/linkedin-profile.md"


def test_skill_exists():
    path = "skills/linkedin-projection/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: linkedin-projection" in content


def test_golden_linkedin_profile_sections():
    assert os.path.exists(GOLDEN)
    with open(GOLDEN, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.startswith("---")
    assert "title:" in content
    assert "Professional Headlines" in content
    assert "About Section" in content
    assert "Featured Section Highlights" in content
    assert "Experience Section Refinements" in content
