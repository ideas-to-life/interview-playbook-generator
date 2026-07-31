# tests/test_story_engine.py
import os
import pytest

GOLDEN = "tests/golden/story-engine/story-library.md"


def test_skill_exists():
    path = "skills/story-engine/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: story-engine" in content


def test_golden_story_library_structure():
    assert os.path.exists(GOLDEN)
    with open(GOLDEN, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.startswith("---")
    assert "type: StoryLibrary" in content
    assert "Situation:" in content
    assert "Challenge:" in content
    assert "Decision:" in content
    assert "Actions:" in content
    assert "Outcome:" in content
    assert "Business Value:" in content
    assert "Conversation Hook:" in content
    assert "Transition Sentence:" in content
