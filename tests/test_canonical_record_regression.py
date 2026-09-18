"""Mandatory Regression Test Suite for Canonical Career Record Integration.

Covers Scenarios 1 through 8 corresponding to known forensic audit findings.
"""

import os
import yaml
from pathlib import Path
import pytest

from scripts.canonical_loader import load_canonical_career_record


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_scenario_7_quarantine_exclusion():
    """Scenario 7 - Quarantine Exclusion.
    
    Any document or claim located in mind-palace/quarantine/ must be 100% excluded
    from factual sourcing and OKF sources ingestion.
    """
    sources_dir = REPO_ROOT / "out" / "okf" / "sources"
    if sources_dir.exists():
        for source_file in sources_dir.glob("*.md"):
            content = source_file.read_text(encoding="utf-8")
            assert "quarantine/" not in content.lower(), (
                f"Quarantined content leaked into ingested source: {source_file}"
            )


def test_employment_records_has_no_positions_csv_corruption():
    """Verify that out/okf/employment-records.yaml has no legacy Positions.csv artifacts.
    
    Specifically, corrupted entries like 'Learn-it-all-Do-it-all' must NOT exist,
    and sources must not cite 'positions-csv'.
    """
    emp_path = REPO_ROOT / "out" / "okf" / "employment-records.yaml"
    if not emp_path.exists():
        pytest.skip("out/okf/employment-records.yaml does not exist yet.")

    with open(emp_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    records = data.get("employment_records", [])
    employers = [r.get("employer") for r in records]

    # Legacy artifact check
    assert "Learn-it-all-Do-it-all" not in employers, (
        "Corrupted legacy entry 'Learn-it-all-Do-it-all' found in employment-records.yaml"
    )

    for rec in records:
        sources = rec.get("sources", [])
        assert "positions-csv" not in sources, (
            f"Record for {rec.get('employer')} still cites legacy 'positions-csv' source"
        )
        assert "canonical-career-record" in sources or "canonical/career-record.yaml" in sources, (
            f"Record for {rec.get('employer')} does not cite canonical source"
        )


def test_scenario_1_education_msc_rejected_bsc_preserved():
    """Scenario 1 — Education.
    
    Derived content: MSc, Federal University of Rio de Janeiro.
    Canonical: BSc Computer Science, Universidade de Mogi das Cruzes.
    Expected: MSc / Federal University claim must not appear; BSc must be preserved.
    """
    from scripts.employment_validator import validate_canonical_integrity, sanitize_artefact_content

    conflicting_content = """
# Candidate Profile
## Education
* MSc, Federal University of Rio de Janeiro (2000)
"""
    result = validate_canonical_integrity(conflicting_content)
    assert result["status"] == "FAIL"
    assert any(v["type"] == "unverified_academic_credential" for v in result["violations"])

    sanitized, alerts = sanitize_artefact_content(conflicting_content)
    assert "Federal University of Rio de Janeiro" not in sanitized
    assert "MSc" not in sanitized
    assert "Universidade de Mogi das Cruzes" in sanitized
    assert "BSc Computer Science" in sanitized
    assert len(alerts) >= 1

    clean_result = validate_canonical_integrity(sanitized)
    assert not any(v["type"] == "unverified_academic_credential" for v in clean_result["violations"])


def test_scenario_2_bbc_formal_title_preserved():
    """Scenario 2 — BBC Formal Title.
    
    Derived: Head of Enterprise Architecture & Digital Evolution.
    Canonical: Lead Enterprise Architect - Technology Transformation Group.
    Expected: Formal title is preserved as Lead Enterprise Architect; Head of EA title is rejected.
    """
    from scripts.employment_validator import validate_canonical_integrity, sanitize_artefact_content

    inflated_content = """
### BBC Studios — London, UK
**Head of Enterprise Architecture & Digital Evolution** | *Oct 2021 – Nov 2025*
* Led strategic transformation initiatives.
"""
    result = validate_canonical_integrity(inflated_content)
    assert result["status"] == "FAIL"
    assert any("Head of Enterprise Architecture" in v.get("reason", "") for v in result["violations"])

    sanitized, alerts = sanitize_artefact_content(inflated_content)
    assert "Head of Enterprise Architecture & Digital Evolution" not in sanitized
    assert "Lead Enterprise Architect - Technology Transformation Group" in sanitized

    clean_result = validate_canonical_integrity(sanitized)
    assert clean_result["status"] == "PASS"


def test_scenario_3_bbc_acting_scope_distinguished_from_formal_title():
    """Scenario 3 — BBC Acting Scope.
    
    Scope previously performed by Head of Architecture may be communicated in prose,
    but MUST NOT convert into a formal Head of Architecture title header.
    """
    from scripts.employment_validator import validate_canonical_integrity

    valid_scope_content = """
### BBC Studios — London, UK
**Lead Enterprise Architect** | *Oct 2021 – Nov 2025*
* Exercised operational acting responsibilities previously performed by the Head of Architecture across governance and transformation.
"""
    result = validate_canonical_integrity(valid_scope_content)
    assert result["status"] == "PASS", f"Valid acting scope in prose was rejected: {result['violations']}"

    invalid_title_content = """
### BBC Studios — London, UK
**Head of Enterprise Architecture** | *Oct 2021 – Nov 2025*
* Exercised operational acting responsibilities across governance and transformation.
"""
    invalid_result = validate_canonical_integrity(invalid_title_content)
    assert invalid_result["status"] == "FAIL"
    assert any("Head of Enterprise Architecture" in v.get("reason", "") for v in invalid_result["violations"])


def test_scenario_8_unsupported_enhancement_rejected():
    """Scenario 8 — Unsupported Enhancement.
    
    Canonical: Contributed to / supported architecture governance.
    Generated attempt: Established and led the enterprise architecture governance function.
    Expected: Stronger claim is rejected and sanitized to supported level.
    """
    from scripts.employment_validator import validate_canonical_integrity, sanitize_artefact_content

    inflated_claim_content = """
### BBC Studios — London, UK
**Lead Enterprise Architect** | *Oct 2021 – Nov 2025*
* Established and led the enterprise architecture governance function across the division.
"""
    result = validate_canonical_integrity(inflated_claim_content)
    assert result["status"] == "FAIL"
    assert any(v["type"] == "unsupported_claim_enhancement" for v in result["violations"])

    sanitized, alerts = sanitize_artefact_content(inflated_claim_content)
    assert "Established and led" not in sanitized
    assert "Supported and contributed" in sanitized

    clean_result = validate_canonical_integrity(sanitized)
    assert clean_result["status"] == "PASS"


def test_scenario_4_bat_chronology_preserved():
    """Scenario 4 — BAT Chronology.
    
    Derived content containing an incomplete BAT history (e.g. artificial split 2016–2020)
    must be rejected in favor of the canonical complete chronology (1997–2021).
    """
    from scripts.employment_validator import validate_canonical_integrity
    from scripts.canonical_validator import detect_conflicts_in_text

    record = load_canonical_career_record()
    bat_entries = [c for c in record.career if "British American Tobacco" in c.employer or "BAT" in c.employer or "Souza Cruz" in c.employer]
    assert len(bat_entries) >= 5, "Incomplete BAT canonical career entries"

    # Conflicting / incomplete derived content
    incomplete_derived = """
### British American Tobacco — London, UK
**Enterprise Architect** | *2016 – 2020*
* Led integration architecture.
"""
    # Should detect conflict against canonical BAT dates
    conflicts = detect_conflicts_in_text(incomplete_derived)
    assert any(c["field_type"] == "dates" for c in conflicts)


def test_scenario_5_compugraf_souza_cruz_consulting_relationship():
    """Scenario 5 — Compugraf / Souza Cruz.
    
    Canonical record establishes Compugraf as an external consultancy through which
    work was contracted to Souza Cruz. Generator must not represent them as contradictory
    simultaneous direct employers.
    """
    from scripts.canonical_validator import detect_conflicts_in_text

    record = load_canonical_career_record()
    compugraf_entry = next((c for c in record.career if "Compugraf" in c.employer), None)
    assert compugraf_entry is not None
    assert compugraf_entry.is_consultancy()
    assert compugraf_entry.client == "Souza Cruz"
    assert "contracted to Souza Cruz" in compugraf_entry.display_relationship()

    # Conflicting attempt: simultaneous direct employment
    contradictory_claim = "Employed by Souza Cruz and Compugraf directly as simultaneous direct employment."
    conflicts = detect_conflicts_in_text(contradictory_claim)
    assert any(c["field_type"] == "employer_relationship" and "Compugraf" in c["conflicting_claim"] for c in conflicts)


def test_scenario_6_wpp_mostelli_distinct_timeline_entries():
    """Scenario 6 — WPP / Mostelli.
    
    Canonical record establishes:
    - WPP Media as direct corporate employment (Dec 2025 – Jul 2026);
    - Mostelli as subsequent independent advisory activity (Jul 2026 – Present).
    Generator must preserve the distinction and not merge them.
    """
    from scripts.canonical_validator import detect_conflicts_in_text

    record = load_canonical_career_record()
    wpp_entry = next((c for c in record.career if "WPP" in c.employer), None)
    mostelli_entry = next((c for c in record.career if "Mostelli" in c.employer), None)

    assert wpp_entry is not None
    assert mostelli_entry is not None
    assert wpp_entry.id != mostelli_entry.id
    assert wpp_entry.engagement_type == "direct_employment"
    assert mostelli_entry.engagement_type == "independent_advisory"

    # Conflicting attempt: merging them into one continuous engagement
    merged_claim = "Alexandre held WPP Media & Mostelli merged continuous engagement from 2022 to present."
    conflicts = detect_conflicts_in_text(merged_claim)
    assert any(c["field_type"] == "employer_relationship" and "Mostelli" in c["canonical_fact"] for c in conflicts)


def test_unresolved_canonical_items_safety():
    """Verify unresolved canonical items policy (FR-010).
    
    Resolved questions are safe for external collateral.
    Unresolved questions are excluded from external collateral and flagged [NEEDS CONFIRMATION] in coaching.
    """
    from scripts.canonical_models import UnresolvedQuestion

    record = load_canonical_career_record()

    # Inject a mock unresolved question alongside existing resolved questions to test policy
    record.unresolved_questions.append(
        UnresolvedQuestion(
            id="UNRES-99",
            topic="Hypothetical Unconfirmed Metric",
            question="What was the exact dollar value of cloud savings in 2022?",
            current_status="unresolved",
            notes="Unverified metric from third-party recruiter email."
        )
    )

    # 1. External collateral filtering: only resolved items returned
    external_items = record.filter_unresolved_for_external()
    assert all(q.current_status == "resolved" for q in external_items)
    assert not any(q.id == "UNRES-99" for q in external_items)

    # 2. Coaching collateral filtering: unresolved items surfaced with [NEEDS CONFIRMATION]
    coaching_items = record.filter_unresolved_for_coaching()
    assert len(coaching_items) >= 1
    unres_99_coaching = next(item for item in coaching_items if item["id"] == "UNRES-99")
    assert unres_99_coaching["flag"] == "[NEEDS CONFIRMATION]"
    assert "[NEEDS CONFIRMATION]" in unres_99_coaching["coaching_guidance"]


