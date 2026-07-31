# tests/test_executive_brief_view.py
import os
import re

GOLDEN = "tests/golden/executive-brief-view"


def test_skill_exists():
    path = "skills/executive-brief-view/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: executive-brief-view" in content


def test_golden_has_eleven_sections():
    golden_path = os.path.join(GOLDEN, "executive-brief.md")
    assert os.path.exists(golden_path)
    with open(golden_path) as f:
        content = f.read()
    expected_titles = [
        "Executive Positioning",
        "Top 5 Messages",
        "Three Signature Stories",
        "Executive Behaviour Profile",
        "Conversation Strategy",
        "Risks",
        "Opportunity Watch-outs",
        "Questions to Ask",
        "Conversation Reminders",
        "Interview Mindset",
        "Final Reminders",
    ]
    for title in expected_titles:
        assert title in content, f"Section '{title}' missing from golden"
    headings = [line for line in content.splitlines() if line.startswith("## ")]
    assert len(headings) == 11, f"Expected 11 sections, found {len(headings)}"


def test_golden_word_count_within_budget():
    golden_path = os.path.join(GOLDEN, "executive-brief.md")
    with open(golden_path) as f:
        content = f.read()
    body = content.split("---", 2)[-1]
    words = re.findall(r"\w+", body)
    assert len(words) <= 2500, f"Brief exceeds 2,500-word budget (got {len(words)})"


def test_interview_mindset_no_evidence():
    golden_path = os.path.join(GOLDEN, "executive-brief.md")
    with open(golden_path) as f:
        content = f.read()
    mindset_start = content.find("## 10. Interview Mindset")
    mindset_end = content.find("## 11. Final Reminders")
    mindset_section = content[mindset_start:mindset_end] if mindset_start > 0 and mindset_end > 0 else ""
    assert "[evidence]" not in mindset_section, "Interview Mindset must be pure coaching (R6)"
    bullets = [line for line in mindset_section.splitlines() if line.startswith("[recommendation]")]
    assert len(bullets) <= 5, f"Interview Mindset must have ≤5 bullets, found {len(bullets)}"
