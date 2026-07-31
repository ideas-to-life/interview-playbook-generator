# tests/test_behaviour_profile.py
import os


def test_skill_exists():
    path = "skills/behaviour-profile-generator/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: behaviour-profile-generator" in content


def test_golden_has_four_core_dimensions():
    golden = "tests/golden/behaviour-profile/behaviour-profile.md"
    assert os.path.exists(golden)
    with open(golden) as f:
        content = f.read()
    for dim in ["Leadership Style", "Communication Style", "Decision Style", "Delivery Style"]:
        assert f"## {dim}" in content, f"Core dimension '{dim}' missing from golden"
    assert "## Collaboration Style" not in content, "Collaboration Style should be omitted (R5)"
    assert "## Executive Presence" not in content, "Executive Presence should be omitted (R5)"
    assert "(insufficient evidence)" not in content, "Optional dimensions must be omitted, not marked insufficient (R5)"
