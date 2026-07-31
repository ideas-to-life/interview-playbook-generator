# tests/test_executive_identity.py
import os
import pytest

GOLDEN_DIR = "tests/golden/executive-identity"


def test_skill_exists():
    path = "skills/executive-identity-generator/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: executive-identity-generator" in content


def test_golden_executive_identity_files_exist():
    assert os.path.isdir(GOLDEN_DIR)
    expected_files = [
        "executive-identity.md",
        "voice-profile.md",
        "positioning-statements.md",
    ]
    for fn in expected_files:
        filepath = os.path.join(GOLDEN_DIR, fn)
        assert os.path.exists(filepath), f"Missing golden identity file: {fn}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            assert content.startswith("---")
            assert "type:" in content
