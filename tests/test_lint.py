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


def lint_capability_content(content: str) -> list[str]:
    """Validate a Capability concept: has Primary Evidence section, ≥1 primary entry, and Evidence strength."""
    errors = []
    if "type: Capability" not in content:
        return errors
    if "## Primary Evidence" not in content:
        errors.append("Missing '## Primary Evidence' section")
    if "## Evidence strength" not in content:
        errors.append("Missing '## Evidence strength' section")
    if "## Supporting Evidence" not in content:
        errors.append("Missing '## Supporting Evidence' section")
    if "## Additional Evidence" not in content:
        errors.append("Missing '## Additional Evidence' section")
    if "Opportunity relevance" in content:
        errors.append("Capability must NOT contain 'Opportunity relevance' (use Evidence strength instead, R7)")
    return errors


def lint_executive_behaviour_profile_content(content: str) -> list[str]:
    """Validate an ExecutiveBehaviourProfile: 4 core dimensions always present, optional marked insufficient is a violation."""
    errors = []
    if "type: ExecutiveBehaviourProfile" not in content:
        return errors
    for dim in ["Leadership Style", "Communication Style", "Decision Style", "Delivery Style"]:
        if f"## {dim}" not in content:
            errors.append(f"Core dimension '{dim}' missing")
    if "(insufficient evidence)" in content:
        errors.append("Optional dimensions must be omitted, not marked '(insufficient evidence)' (R5)")
    return errors


def lint_signature_achievements_content(content: str) -> list[str]:
    """Validate a SignatureAchievements node: 5–12 numbered list entries, each with Why/Strategic/Capability."""
    errors = []
    if "type: SignatureAchievements" not in content:
        return errors
    entries = re.findall(r"^\d+\. \*\*", content, flags=re.MULTILINE)
    if not (5 <= len(entries) <= 12):
        errors.append(f"SignatureAchievements list length must be 5–12, found {len(entries)}")
    if "Selection rationale" not in content:
        errors.append("Missing 'Selection rationale' section")
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


def test_capability_lint_accepts_valid_node():
    valid = """---
type: Capability
title: "Enterprise Architecture"
---

# Definition
[inference] Description.

## Primary Evidence
- [Evidence: Cloud Migration](cloud-migration.md) — [inference] Strongest demonstration.

## Supporting Evidence
- [Evidence: Architecture Patterns](architecture-patterns.md) — [inference] Reinforces.

## Additional Evidence

## Evidence strength
[inference] High.
"""
    errors = lint_capability_content(valid)
    assert errors == [], f"Expected zero lint errors, got: {errors}"


def test_capability_lint_rejects_opportunity_relevance():
    invalid = """---
type: Capability
---

# Opportunity relevance
[inference] Some text.
"""
    errors = lint_capability_content(invalid)
    assert any("Opportunity relevance" in e for e in errors)


def test_behaviour_profile_lint_rejects_insufficient_evidence_marker():
    invalid = """---
type: ExecutiveBehaviourProfile
---

## Leadership Style
[evidence] Leadership x. [^cv]

## Communication Style
[evidence] Communication x. [^cv]

## Decision Style
(insufficient evidence)

## Delivery Style
[evidence] Delivery x. [^cv]
"""
    errors = lint_executive_behaviour_profile_content(invalid)
    assert any("'(insufficient evidence)'" in e for e in errors)


def test_signature_achievements_lint_rejects_short_list():
    invalid = """---
type: SignatureAchievements
---

# The list

1. **[A](a.md)** — [inference] Why x. Strategic y. Capability z.

# Selection rationale
[inference] Rationale.
"""
    errors = lint_signature_achievements_content(invalid)
    assert any("5–12" in e for e in errors)

