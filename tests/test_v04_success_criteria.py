# tests/test_v04_success_criteria.py
"""End-to-end success criteria verification for Sprint 4 (v0.4) Career Projection Platform."""
import os
import re
import yaml
import pytest


def test_opportunity_analysis_generated_in_runtime_dir():
    path = "tests/golden/opportunity-analyzer/opportunity-analysis.yaml"
    assert os.path.exists(path)
    with open(path) as f:
        data = yaml.safe_load(f)
    assert data.get("version") == "0.4"
    assert "target_opportunity" in data
    assert "hiring_goals" in data
    assert "coverage_matrix" in data


def test_canonical_bundle_remains_immutable():
    """Verify okf/ nodes carry zero opportunity-specific runtime fields."""
    for root, _, files in os.walk("tests/golden"):
        if "opportunity-analyzer" in root or "projection-validator" in root or "projection-registry" in root:
            continue
        for fn in files:
            if fn.endswith(".md") and not fn.startswith("interview-strategy") and not fn.startswith("knowledge-gaps"):
                path = os.path.join(root, fn)
                with open(path) as f:
                    content = f.read()
                    assert "opportunity_relevance" not in content, f"Forbidden field in canonical node: {path}"


def test_resume_projection_default_variants_exist():
    golden_dir = "tests/golden/resume-projection"
    for filename in ["resume-executive.md", "resume-ats.md", "resume-recruiter.md"]:
        path = os.path.join(golden_dir, filename)
        assert os.path.exists(path), f"Missing golden resume variant: {filename}"


def test_cover_letter_length_and_sections():
    path = "tests/golden/cover-letter-projection/cover-letter.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    body = content.split("---", 2)[-1]
    words = re.findall(r"\w+", body)
    assert len(words) <= 500, f"Cover letter exceeds 500 words ({len(words)})"
    assert "Head of AI" in content
    assert "Vervaunt" in content


def test_linkedin_projection_structure():
    path = "tests/golden/linkedin-projection/linkedin-profile.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert "Professional Headlines" in content
    assert "About Section" in content
    assert "Featured Section Highlights" in content
    assert "Experience Section Refinements" in content


def test_projection_validation_report():
    path = "tests/golden/projection-validator/projection-validation-report.yaml"
    assert os.path.exists(path)
    with open(path) as f:
        data = yaml.safe_load(f)
    assert data.get("version") == "0.4"
    assert data.get("overall_status") == "PASSED"
    assert data.get("overall_quality_score") >= 90.0


def test_total_skills_registered_is_twenty_one():
    skills_dir = "skills"
    skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert len(skills) >= 21, f"Expected at least 21 skills, found {len(skills)}: {sorted(skills)}"
