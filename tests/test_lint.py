import re
import pytest

VALID_PREFIXES = ("[evidence]", "[inference]", "[recommendation]", "[assumption]")

def lint_okf_concept_content(content: str) -> list[str]:
    """
    Validates an OKF concept markdown string against the project's classification and provenance rules.
    Returns a list of error strings.
    """
    errors = []
    lines = content.splitlines()
    
    # Separate frontmatter from body
    in_frontmatter = False
    body_lines = []
    frontmatter_count = 0
    
    for i, line in enumerate(lines, 1):
        if line.strip() == "---":
            frontmatter_count += 1
            if frontmatter_count == 1:
                in_frontmatter = True
                continue
            elif frontmatter_count == 2:
                in_frontmatter = False
                continue
        
        if not in_frontmatter:
            body_lines.append((i, line))
            
    for line_num, line in body_lines:
        stripped = line.strip()
        # Skip empty lines, headers, footnotes, blockquotes, horizontal rules, or source links
        if (not stripped or stripped.startswith("#") or stripped.startswith("[^") 
                or stripped.startswith(">") or stripped == "---" or stripped.startswith("Source concept")):
            continue
        
        # If line starts with a list bullet "- " or "* ", check if the content after bullet is a claim
        target_line = stripped
        if stripped.startswith("- ") or stripped.startswith("* "):
            bullet_content = stripped[2:].strip()
            # If bullet item is a list item or link (not starting with classification prefix), skip it
            if not any(bullet_content.startswith(prefix) for prefix in VALID_PREFIXES):
                continue
            target_line = bullet_content
        
        # Check classification marker
        if not any(target_line.startswith(prefix) for prefix in VALID_PREFIXES):
            errors.append(f"Line {line_num}: Line missing valid classification prefix ({VALID_PREFIXES}): '{stripped}'")
            continue
            
        # If evidence, check for footnote attribution
        if target_line.startswith("[evidence]") and "[^" not in target_line:
            errors.append(f"Line {line_num}: [evidence] claim missing [^source-id] footnote attribution: '{stripped}'")

            
    return errors


def test_lint_valid_concept():
    valid_markdown = """---
type: Achievement
title: Migration
sources:
  - id: cv-2024
---

# Situation

[evidence] Multi-region cloud migration completed. [^cv-2024]
[inference] Required alignment across distributed regional teams.
[recommendation] Highlight cutover protocol in interview.
[assumption] Team size was approximately 10.
"""
    errors = lint_okf_concept_content(valid_markdown)
    assert errors == [], f"Expected zero lint errors, got: {errors}"


def test_lint_missing_classification():
    invalid_markdown = """---
type: Achievement
---

# Situation

Unclassified claim line without marker.
"""
    errors = lint_okf_concept_content(invalid_markdown)
    assert len(errors) == 1
    assert "Line missing valid classification prefix" in errors[0]


def test_lint_missing_footnote_on_evidence():
    invalid_markdown = """---
type: Achievement
---

# Situation

[evidence] Migration finished without unplanned downtime.
"""
    errors = lint_okf_concept_content(invalid_markdown)
    assert len(errors) == 1
    assert "missing [^source-id] footnote attribution" in errors[0]
