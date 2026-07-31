# tests/test_capability_extractor.py
import os
import pytest
import filecmp
import shutil

GOLDEN = "tests/golden/capability-extractor"


def test_capability_skill_exists():
    path = "skills/capability-extractor/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: capability-extractor" in content


def test_fixtures_evidence_cards_exist():
    fixture_dir = "tests/fixtures/portfolio_minimal"
    expected = [
        "evidence-cloud-migration.md",
        "evidence-architecture-patterns.md",
        "evidence-ai-coe-build.md",
        "evidence-decision-log-practice.md",
        "evidence-stakeholder-management.md",
    ]
    for name in expected:
        assert os.path.exists(os.path.join(fixture_dir, name)), f"Missing fixture {name}"


def test_capability_golden_subtree_exists():
    assert os.path.isdir(GOLDEN), f"Golden subtree missing at {GOLDEN}"
    assert os.path.exists(os.path.join(GOLDEN, "index.md"))


def test_capability_golden_snapshot(tmp_path):
    expected = GOLDEN
    assert os.path.isdir(expected)
    expected_files = set(os.listdir(expected))
    assert "index.md" in expected_files
    assert len(expected_files) >= 5, f"Expected ≥5 capabilities (index + 4 min), got {len(expected_files)}"
    assert len(expected_files) <= 16, f"Expected ≤15 capabilities, got {len(expected_files)}"

