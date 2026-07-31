# tests/test_cover_letter_projection.py
import os
import re
import pytest

GOLDEN = "tests/golden/cover-letter-projection/cover-letter.md"


def test_skill_exists():
    path = "skills/cover-letter-projection/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: cover-letter-projection" in content


def test_golden_cover_letter_structure_and_length():
    assert os.path.exists(GOLDEN)
    with open(GOLDEN, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.startswith("---")
    assert "title:" in content
    assert "Head of AI" in content
    assert "Vervaunt" in content

    # Check word count constraint (<= 500 words)
    body = content.split("---", 2)[-1]
    words = re.findall(r"\w+", body)
    assert len(words) <= 500, f"Cover letter exceeds 500-word budget (got {len(words)})"
