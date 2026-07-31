# tests/test_narrative_engine.py
import os
import pytest

GOLDEN_DIR = "tests/golden/narrative-engine"


def test_skill_exists():
    path = "skills/narrative-engine/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: narrative-engine" in content


def test_golden_narrative_libraries_exist():
    assert os.path.isdir(GOLDEN_DIR)
    expected_files = [
        "narrative-library.md",
        "messaging-library.md",
    ]
    for fn in expected_files:
        filepath = os.path.join(GOLDEN_DIR, fn)
        assert os.path.exists(filepath), f"Missing golden narrative library file: {fn}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            assert content.startswith("---")
            assert "type:" in content
