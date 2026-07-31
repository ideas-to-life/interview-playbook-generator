# tests/test_opportunity_alignment_view.py
import os
import re

GOLDEN = "tests/golden/opportunity-alignment-view"


def test_skill_exists():
    path = "skills/opportunity-alignment-view/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: opportunity-alignment-view" in content


def test_golden_view_exists():
    assert os.path.isdir(GOLDEN)
    golden_path = os.path.join(GOLDEN, "opportunity-alignment.md")
    assert os.path.exists(golden_path)
    with open(golden_path) as f:
        content = f.read()
    assert content.startswith("---")
    frontmatter_end = content.find("---", 3)
    assert frontmatter_end > 0
    frontmatter = content[:frontmatter_end]
    assert "type:" not in frontmatter, "View file must NOT have a `type:` frontmatter key"
    assert "title:" in frontmatter
    assert "description:" in frontmatter
    theme_blocks = [line for line in content.splitlines() if line.startswith("## ")]
    assert 5 <= len(theme_blocks) <= 8, f"Expected 5–8 themes, found {len(theme_blocks)}"


def test_golden_links_resolve():
    golden_path = os.path.join(GOLDEN, "opportunity-alignment.md")
    with open(golden_path) as f:
        content = f.read()
    links = re.findall(r"\]\(\.\./okf/[^)]+\)", content)
    assert len(links) > 0, "Expected at least one bundle-relative link"
