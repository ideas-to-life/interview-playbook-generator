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


def test_golden_resume_variants_exist_and_clean():
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
            lines = content.strip().splitlines()

        # Presentation view files in out/ are clean markdown (no frontmatter, no OKF tags)
        assert not content.startswith("---"), f"{filename} should not start with YAML frontmatter"
        assert "[recommendation]" not in content, f"{filename} should not contain OKF tags"
        assert "[inference]" not in content, f"{filename} should not contain OKF tags"
        assert "[evidence]" not in content, f"{filename} should not contain OKF tags"
        assert "[Evidence:" not in content, f"{filename} should not contain OKF evidence links"

        # Check full document scope
        assert len(lines) >= 50, f"{filename} should be a full resume (>=50 lines), found {len(lines)}"
        assert "SUMMARY" in content.upper()
        assert "EXPERIENCE" in content.upper()
        assert "SKILLS" in content.upper() or "COMPETENCIES" in content.upper()
        assert "WPP" in content
        assert "BBC Studios" in content
        assert "British American Tobacco" in content or "BAT" in content
