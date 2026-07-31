# tests/test_v03_success_criteria.py
"""End-to-end checks for v0.3 success criteria (spec §8)."""
import os
import re
import subprocess
import sys


def test_pipeline_version_bumped():
    with open("config/config.example.yaml") as f:
        content = f.read()
    assert 'version: "0.3"' in content


def test_no_opportunity_relevance_field_in_golden():
    """No canonical evidence card in the golden subtree carries opportunity_relevance."""
    golden_evidence = "tests/golden"
    found = []
    for root, _, files in os.walk(golden_evidence):
        for fn in files:
            if fn.endswith(".md"):
                path = os.path.join(root, fn)
                with open(path) as f:
                    if "opportunity_relevance" in f.read():
                        found.append(path)
    assert found == [], f"Canonical nodes must NOT carry opportunity_relevance (R2), found in: {found}"


def test_view_files_no_type_field():
    """view files in tests/golden/ must not have a `type:` frontmatter key."""
    forbidden = []
    for root, _, files in os.walk("tests/golden"):
        for fn in files:
            if fn.endswith(".md"):
                path = os.path.join(root, fn)
                with open(path) as f:
                    content = f.read()
                if content.startswith("---"):
                    end = content.find("---", 3)
                    frontmatter = content[:end]
                    if "executive-brief-view" in path or "opportunity-alignment-view" in path:
                        if "type:" in frontmatter:
                            forbidden.append(path)
    assert forbidden == [], f"View files must NOT have `type:` frontmatter: {forbidden}"


def test_behaviour_profile_golden_has_no_insufficient_evidence():
    golden = "tests/golden/behaviour-profile/behaviour-profile.md"
    assert os.path.exists(golden)
    with open(golden) as f:
        assert "(insufficient evidence)" not in f.read(), "R5 violated"


def test_executive_brief_golden_has_eleven_sections():
    golden = "tests/golden/executive-brief-view/executive-brief.md"
    assert os.path.exists(golden)
    with open(golden) as f:
        content = f.read()
    headings = [line for line in content.splitlines() if line.startswith("## ")]
    assert len(headings) == 11, f"Expected 11 sections, got {len(headings)}"


def test_executive_brief_word_count_within_budget():
    golden = "tests/golden/executive-brief-view/executive-brief.md"
    with open(golden) as f:
        content = f.read()
    body = content.split("---", 2)[-1]
    words = re.findall(r"\w+", body)
    assert len(words) <= 2500, f"Executive Brief exceeds 2,500-word budget (got {len(words)})"


def test_oracle_full_test_suite():
    """Run the entire test suite and verify no tests fail."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Tests failed:\n{result.stdout}\n{result.stderr}"
