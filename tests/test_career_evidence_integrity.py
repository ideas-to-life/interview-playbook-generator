# tests/test_career_evidence_integrity.py
"""Automated test suite for Career History Evidence Integrity (P0 Refinement)."""

import os
import pytest
from scripts.employment_validator import (
    load_canonical_employment_records,
    validate_employment_history,
)


def test_canonical_employment_records_exist_and_valid():
    """Verify out/okf/employment-records.yaml exists and contains mandatory fields."""
    records = load_canonical_employment_records("out/okf/employment-records.yaml")
    assert len(records) >= 3

    employers = [r["employer"] for r in records]
    assert "WPP Media" in employers
    assert "BBC Studios" in employers
    assert "British American Tobacco" in employers

    wpp = next(r for r in records if r["employer"] == "WPP Media")
    assert wpp["start_date"] == "Dec 2025"
    assert wpp["end_date"] is None
    assert wpp["title"] == "Senior Director, Agentic AI Systems Architecture"

    bbc = next(r for r in records if r["employer"] == "BBC Studios")
    assert bbc["start_date"] == "Nov 2021"
    assert bbc["end_date"] == "Nov 2025"
    assert bbc["title"] == "Lead Enterprise Architect"

    bat = next(r for r in records if r["employer"] == "British American Tobacco")
    assert bat["start_date"] == "2011"
    assert bat["end_date"] == "2021"


def test_employment_validator_passes_on_valid_canonical_projection():
    """Verify validator passes on a valid resume projection matching canonical evidence."""
    valid_content = """
# ALEXANDRE DE VASCONCELOS FRANCO
Enterprise Architect | Architecture Governance | AI Transformation

## PROFESSIONAL EXPERIENCE

### WPP Media — London, UK
**Senior Director, Agentic AI Systems Architecture** | *Dec 2025 – Present*
* Defined architecture strategy for Prototyping & Innovation Agentic AI.

### BBC Studios — London, UK
**Lead Enterprise Architect** | *Nov 2021 – Nov 2025*
* Led the redesign of the Enterprise Architecture operating model.

### British American Tobacco — London, UK
**Enterprise Architect & Global Solution Architect** | *2011 – 2021*
* Established enterprise architecture governance.
"""
    result = validate_employment_history(valid_content)
    assert result["status"] == "PASS"
    assert len(result["violations"]) == 0


def test_employment_validator_rejects_fabricated_wpp_date_2022():
    """Verify validator flags fabricated WPP start date (2022 - Present instead of Dec 2025 - Present)."""
    invalid_content = """
### WPP Media — London, UK
**Enterprise Architect & AI Practice Lead** | *2022 – Present*
* Defined architecture strategy.
"""
    result = validate_employment_history(invalid_content)
    assert result["status"] == "FAIL"
    assert any("WPP" in v.get("reason", "") or "WPP" in v.get("employer", "") for v in result["violations"])


def test_employment_validator_rejects_fabricated_bbc_dates_2020_2022():
    """Verify validator flags fabricated BBC Studios period (2020 - 2022 instead of Nov 2021 - Nov 2025)."""
    invalid_content = """
### BBC Studios — London, UK
**Principal Enterprise Cloud Architect** | *2020 – 2022*
* Led enterprise architecture.
"""
    result = validate_employment_history(invalid_content)
    assert result["status"] == "FAIL"
    assert any("BBC" in v.get("reason", "") or "BBC" in v.get("employer", "") for v in result["violations"])


def test_employment_validator_rejects_unsupported_title_substitution():
    """Verify validator flags target-aligned title substitution 'Enterprise Architect & AI Practice Lead'."""
    invalid_content = """
### WPP Media — London, UK
**Enterprise Architect & AI Practice Lead**
* Defined architecture strategy.
"""
    result = validate_employment_history(invalid_content)
    assert result["status"] == "FAIL"
    assert any("title" in v.get("reason", "").lower() or "title" in v.get("type", "").lower() for v in result["violations"])


def test_employment_validator_rejects_unsupported_role_split_bat_rd():
    """Verify validator flags fabricated role split 'BAT R&D (2016-2020)'."""
    invalid_content = """
### British American Tobacco R&D
**Head of Enterprise Architecture & Systems** | *2016 – 2020*
* Led BAT R&D architecture.
"""
    result = validate_employment_history(invalid_content)
    assert result["status"] == "FAIL"
    assert len(result["violations"]) > 0


def test_head_of_ea_career_evidence_integrity_regression():
    """Full Head of Enterprise Architecture regression assertion."""
    fabricated_run_content = """
### WPP Media
**Enterprise Architect & AI Practice Lead**
*2022 – Present*

### BBC Studios
**Principal Enterprise Cloud Architect**
*2020 – 2022*

### British American Tobacco R&D
**Head of Enterprise Architecture & Systems**
*2016 – 2020*
"""
    result = validate_employment_history(fabricated_run_content)
    assert result["status"] == "FAIL"
    assert len(result["violations"]) >= 3
