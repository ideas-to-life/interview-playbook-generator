# tests/test_resume_projection.py
import os
import pytest

GOLDEN_DIR = "tests/golden/resume-projection"


def test_skill_exists():
    path = "skills/resume-projection/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: resume-projection" in content


def test_golden_resume_variants_exist():
    assert os.path.isdir(GOLDEN_DIR)
    expected_variants = [
        "resume-executive.md",
        "resume-ats.md",
        "resume-recruiter.md",
    ]
    for filename in expected_variants:
        filepath = os.path.join(GOLDEN_DIR, filename)
        assert os.path.exists(filepath), f"Missing golden resume variant: {filename}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            assert content.startswith("---")
            assert "title:" in content
