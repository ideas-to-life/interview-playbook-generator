"""Contract tests for Canonical Selection Record.

Validates that out/<target-slug>/runtime/canonical-selection.yaml adheres to
specs/005-canonical-record-integration/contracts/canonical-selection-contract.yaml.
"""

from pathlib import Path
import re
import yaml
import pytest

from scripts.canonical_selector import select_canonical_facts


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_canonical_selection_contract_conformance(tmp_path):
    out_file = tmp_path / "out" / "test-opportunity" / "runtime" / "canonical-selection.yaml"
    selection = select_canonical_facts(
        target_slug="test-opportunity",
        output_path=str(out_file)
    )

    assert out_file.exists()
    assert selection["target_slug"] == "test-opportunity"
    assert "generated_at" in selection
    assert selection["canonical_source"] == "canonical/career-record.yaml"

    # Validate selected roles
    roles = selection.get("selected_roles", [])
    assert len(roles) >= 4
    for r in roles:
        assert re.match(r"^CAR-[0-9]+$", r["canonical_id"])
        assert r["employer"]
        assert r["formal_title"]
        assert r["start_date"]
        assert r["engagement_type"] in ["direct_employment", "consultancy", "independent_advisory"]
        assert r["status"] in ["current", "former"]
        assert "operational_scope" in r
        assert "relevance_rationale" in r

    # Validate selected education
    education = selection.get("selected_education", [])
    assert len(education) >= 1
    for edu in education:
        assert re.match(r"^EDU-[0-9]+$", edu["canonical_id"])
        assert edu["institution"]
        assert edu["degree_name"]
        assert edu["degree_level"]

    # Validate selected certifications
    certs = selection.get("selected_certifications", [])
    assert len(certs) >= 1
    for cert in certs:
        assert re.match(r"^CERT-[0-9]+$", cert["canonical_id"])
        assert cert["name"]
        assert cert["issuing_body"]

    # Validate unresolved items if present
    for unres in selection.get("unresolved_items_flagged", []):
        assert re.match(r"^UNRES-[0-9]+$", unres["canonical_id"])
        assert unres["topic"]
        assert unres["question"]
        assert unres["confirmation_flag"] == "[NEEDS CONFIRMATION]"


def test_complete_canonical_selection_beyond_line_50(tmp_path):
    """Scenario 1: Verify that facts beyond line 50 of canonical selection are fully available."""
    out_file = tmp_path / "out" / "tenth-ai-lead-enterprise-architect" / "runtime" / "canonical-selection.yaml"
    selection = select_canonical_facts(
        target_slug="tenth-ai-lead-enterprise-architect",
        output_path=str(out_file)
    )

    with open(out_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Must exceed 50 lines to prove facts reside beyond arbitrary truncation boundaries
    assert len(lines) > 50, f"Expected selection file to exceed 50 lines, got {len(lines)}"

    # Find line numbers of education, certifications, and languages
    education_line = None
    certifications_line = None
    languages_line = None

    for idx, line in enumerate(lines, 1):
        if "selected_education:" in line:
            education_line = idx
        elif "selected_certifications:" in line:
            certifications_line = idx
        elif "selected_languages:" in line:
            languages_line = idx

    assert education_line is not None and education_line > 50, (
        f"Expected selected_education to reside beyond line 50, found at line {education_line}"
    )

    # Verify that the complete selection contains the exact canonical facts
    edu = selection["selected_education"][0]
    assert edu["institution"] == "Universidade de Mogi das Cruzes"
    assert edu["start_year"] == 1988
    assert edu["end_year"] == 1991

    # Verify certifications and languages exist in selection
    assert len(selection["selected_certifications"]) >= 1
    assert len(selection["selected_languages"]) >= 3
    spanish = next((l for l in selection["selected_languages"] if l["language"].lower() == "spanish"), None)
    assert spanish is not None
    assert "elementary" in spanish["proficiency"].lower()

