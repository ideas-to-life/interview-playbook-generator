# tests/test_v05_success_criteria.py
"""End-to-end success criteria verification for Sprint 5 (v0.5) Executive Narrative & Personal Brand Engine."""
import os
import yaml
import pytest


def test_executive_identity_canonical_nodes_exist():
    golden_dir = "tests/golden/executive-identity"
    for filename in ["executive-identity.md", "voice-profile.md", "positioning-statements.md"]:
        path = os.path.join(golden_dir, filename)
        assert os.path.exists(path), f"Missing canonical identity file: {filename}"
        with open(path) as f:
            content = f.read()
        assert content.startswith("---")
        assert "type:" in content


def test_narrative_and_messaging_libraries_exist():
    golden_dir = "tests/golden/narrative-engine"
    for filename in ["narrative-library.md", "messaging-library.md"]:
        path = os.path.join(golden_dir, filename)
        assert os.path.exists(path), f"Missing canonical narrative library file: {filename}"


def test_story_library_is_single_consolidated_document():
    path = "tests/golden/story-engine/story-library.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "type: StoryLibrary" in content
    assert "Situation:" in content
    assert "Outcome:" in content


def test_brand_validation_report_status():
    path = "tests/golden/brand-validator/brand-validation-report.yaml"
    assert os.path.exists(path)
    with open(path) as f:
        data = yaml.safe_load(f)
    assert data.get("version") == "0.5"
    assert data.get("brand_alignment_status") == "PASSED"
    assert data.get("overall_brand_score") >= 95.0


def test_total_skills_registered_is_twenty_five():
    skills_dir = "skills"
    skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert len(skills) == 25, f"Expected 25 skills, found {len(skills)}: {sorted(skills)}"
