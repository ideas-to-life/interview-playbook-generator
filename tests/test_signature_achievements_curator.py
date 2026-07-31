# tests/test_signature_achievements_curator.py
import os
import pytest

GOLDEN = "tests/golden/signature-achievements-curator"


def test_skill_exists():
    path = "skills/signature-achievements-curator/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: signature-achievements-curator" in content


def test_achievement_fixtures_exist():
    fixture_dir = "tests/fixtures/portfolio_minimal"
    expected = [
        "achievements-cloud-migration.md",
        "achievements-architecture-patterns.md",
        "achievements-ai-coe-build.md",
        "achievements-decision-log-practice.md",
        "achievements-stakeholder-management.md",
    ]
    for name in expected:
        assert os.path.exists(os.path.join(fixture_dir, name)), f"Missing fixture {name}"


def test_golden_node_exists():
    assert os.path.isdir(GOLDEN)
    assert os.path.exists(os.path.join(GOLDEN, "signature-achievements.md"))
    with open(os.path.join(GOLDEN, "signature-achievements.md")) as f:
        content = f.read()
    assert "type: SignatureAchievements" in content
    assert "Selection rationale" in content
    for i in range(1, 6):
        assert f"{i}. **" in content, f"List item {i} not found"
