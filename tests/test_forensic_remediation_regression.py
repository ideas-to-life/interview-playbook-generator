"""Forensic Remediation Regression Suite (User Story 4).

Covers all 10 diagnostic failure scenarios identified in the September 2026
Tenth AI Lead Enterprise Architect forensic diagnostic:

- Scenario 1: Complete Canonical Selection Loading
- Scenario 2: Education Date Contradiction Remediated
- Scenario 3: Certification Invention Rejected (AWS, Sun SCEA/SCJP)
- Scenario 4: Language Inflation Rejected (Spanish Fluent vs Elementary)
- Scenario 5: Target JD Platform Leakage Prevented (ATS Partitioning)
- Scenario 6: Previous Projection Contamination Blocked (Zero Prior Run Reads)
- Scenario 7: Opportunity Runtime Isolation (Order-Independent Clean Context)
- Scenario 8: Unsupported Technology Direct Claim Rejected (FATAL Failure)
- Scenario 9: Transferable Framing Permitted (Architectural Applicability)
- Scenario 10: Canonical Precedence & Immutability (Read-Only Authority)
"""

from pathlib import Path
import tempfile
import pytest
import yaml

from scripts.canonical_loader import load_canonical_career_record
from scripts.canonical_selector import (
    select_canonical_facts,
    partition_ats_vocabulary,
    classify_term_evidence,
)
from scripts.canonical_models import (
    ProjectionValidationReport,
    ATSVocabularyPartition,
)
from scripts.projection_validator import (
    validate_projection_content,
    sanitize_projection_content,
    validate_opportunity_projections,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


# ==============================================================================
# Phase 6 / T028: Scenarios 1–3
# ==============================================================================

def test_scenario_1_complete_canonical_selection_loading():
    """Scenario 1: 100% of canonical facts (including facts beyond line 50) are loaded."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_yaml = Path(tmp_dir) / "canonical-selection.yaml"
        record = select_canonical_facts("scenario-1-target", output_path=str(out_yaml))

        with open(out_yaml, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) > 50, "canonical-selection.yaml must contain full context beyond line 50"

        # Education beyond line 50
        assert "selected_education" in record
        assert len(record["selected_education"]) >= 1
        mogi_edu = record["selected_education"][0]
        assert "Mogi das Cruzes" in mogi_edu["institution"]
        assert mogi_edu["start_year"] == 1988
        assert mogi_edu["end_year"] == 1991

        # Certifications beyond line 50
        assert "selected_certifications" in record
        cert_names = [c["name"] for c in record["selected_certifications"]]
        assert any("TOGAF" in c for c in cert_names)

        # Languages beyond line 50
        assert "selected_languages" in record
        lang_dict = {l["language"]: l["proficiency"] for l in record["selected_languages"]}
        assert "Portuguese" in lang_dict
        assert "English" in lang_dict
        assert "Spanish" in lang_dict


def test_scenario_2_education_date_contradiction_remediated():
    """Scenario 2: Education date contradiction (BSc 1995–1999 vs 1988–1991) is remediated."""
    mutated_resume = (
        "## Education\n"
        "- **BSc in Computer Science**, Universidade de Mogi das Cruzes (1995–1999)\n"
    )

    sanitized, findings = sanitize_projection_content(mutated_resume)
    assert "1988–1991" in sanitized or "1988 - 1991" in sanitized
    assert "1995" not in sanitized
    assert any(f.category == "education" and f.severity == "SANITIZED" for f in findings)


def test_scenario_3_certification_invention_rejected():
    """Scenario 3: Hallucinated certifications (AWS, Sun SCEA/SCJP) cause FATAL failure."""
    corrupted_resume = (
        "## Professional Qualifications\n"
        "- AWS Certified Solutions Architect - Professional\n"
        "- Sun Certified Enterprise Architect (SCEA)\n"
        "- Sun Certified Java Programmer (SCJP)\n"
    )

    report = validate_projection_content(corrupted_resume)
    assert report.overall_status == "FAILED"
    fatal_certs = [f for f in report.findings if f.category == "certification" and f.severity == "FATAL"]
    assert len(fatal_certs) >= 2


# ==============================================================================
# Phase 6 / T029: Scenarios 4–6
# ==============================================================================

def test_scenario_4_language_inflation_rejected():
    """Scenario 4: Inflating Spanish from Elementary to Fluent/Professional causes FATAL failure."""
    inflated_resume = (
        "## Languages\n"
        "- Portuguese (Native)\n"
        "- English (Full Professional)\n"
        "- Spanish (Fluent & Bilingual Professional)\n"
    )

    report = validate_projection_content(inflated_resume)
    assert report.overall_status == "FAILED"
    lang_findings = [f for f in report.findings if f.category == "language" and f.severity == "FATAL"]
    assert len(lang_findings) >= 1
    assert any("spanish" in f.reason.lower() for f in lang_findings)


def test_scenario_5_target_jd_platform_leakage_prevented():
    """Scenario 5: Target JD enterprise platforms are partitioned into required_job_vocabulary."""
    target_jd_terms = [
        "Enterprise Architecture",
        "Workday",
        "NetSuite",
        "Coupa",
        "Concur",
        "LeanIX",
    ]

    partition = partition_ats_vocabulary(target_jd_terms)
    evidenced = [t.term for t in partition.candidate_evidenced_vocabulary]
    required = [t.term for t in partition.required_job_vocabulary]

    assert "Workday" in required
    assert "NetSuite" in required
    assert "Coupa" in required
    assert "Concur" in required

    assert "Enterprise Architecture" in evidenced
    assert "LeanIX" in evidenced

    assert partition.scoring_rules["evidenced_credit_multiplier"] == 1.0
    assert partition.scoring_rules["unevidenced_credit_multiplier"] == 0.0


def test_scenario_6_previous_projection_contamination_blocked():
    """Scenario 6: Active opportunity skills cannot read collateral from other opportunities."""
    skill_files = [
        REPO_ROOT / "skills" / "resume-projection" / "SKILL.md",
        REPO_ROOT / "skills" / "cover-letter-projection" / "SKILL.md",
        REPO_ROOT / "skills" / "linkedin-projection" / "SKILL.md",
        REPO_ROOT / "skills" / "opportunity-alignment-view" / "SKILL.md",
        REPO_ROOT / "skills" / "executive-brief-view" / "SKILL.md",
    ]

    for sf in skill_files:
        content = sf.read_text(encoding="utf-8")
        assert "Cross-Opportunity Isolation Invariant" in content
        assert "templates/projections/" in content or "canonical-selection.yaml" in content
        assert "out/<other-target-slug>" not in content or "NEVER read, inspect, or use prior opportunity" in content


# ==============================================================================
# Phase 6 / T030: Scenarios 7–10
# ==============================================================================

def test_scenario_7_opportunity_runtime_isolation():
    """Scenario 7: Corrupted files in prior target opportunity directory do not pollute new opportunity."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_root = Path(tmp_dir) / "out"
        opp_a = out_root / "target-a" / "runtime"
        opp_b = out_root / "target-b" / "runtime"

        opp_a.mkdir(parents=True)
        opp_b.mkdir(parents=True)

        # Pollute Target A with corrupted claims
        (opp_a / "canonical-selection.yaml").write_text("corrupted_claim: Workday Expert\n", encoding="utf-8")

        # Run selection cleanly for Target B
        record_b = select_canonical_facts("target-b", output_path=str(opp_b / "canonical-selection.yaml"))

        # Verify Target B contains pure canonical facts without leakage from A
        content_b = (opp_b / "canonical-selection.yaml").read_text(encoding="utf-8")
        assert "corrupted_claim" not in content_b
        assert "Workday Expert" not in content_b
        assert len(record_b["selected_roles"]) >= 1


def test_scenario_8_unsupported_technology_claim_rejected():
    """Scenario 8: Claiming direct implementation of unevidenced client platform causes FATAL failure."""
    fabricated_resume = (
        "## Key Initiatives\n"
        "- Led the global deployment of Workday Financials and Coupa Procurement across 12 countries.\n"
    )

    report = validate_projection_content(fabricated_resume)
    assert report.overall_status == "FAILED"
    tech_findings = [f for f in report.findings if f.category == "technology" and f.severity == "FATAL"]
    assert len(tech_findings) >= 1
    assert any("workday" in f.reason.lower() for f in tech_findings)


def test_scenario_9_transferable_framing_permitted():
    """Scenario 9: Referencing client platforms in transferable or gap context passes validation."""
    transferable_resume = (
        "## Enterprise Architecture Strategy\n"
        "- Directed enterprise-wide ERP and finance integration architectures comparable to Workday and NetSuite.\n"
        "- Evaluated source-to-pay procurement operating models analogous to Coupa environments.\n"
        "- Recognized gap: Direct administrative experience in Workday is adjacent; core competency lies in integration governance.\n"
    )

    report = validate_projection_content(transferable_resume)
    tech_findings = [f for f in report.findings if f.category == "technology" and f.severity == "FATAL"]
    assert len(tech_findings) == 0


def test_scenario_10_canonical_precedence_and_immutability():
    """Scenario 10: Canonical career record is strictly read-only and unconditionally supersedes secondary inputs."""
    record = load_canonical_career_record()

    # Canonical career record loaded read-only
    assert hasattr(record, "career")
    assert len(record.career) >= 1

    # BBC formal title precedence
    bbc = record.get_career_entry("CAR-03")
    assert bbc is not None
    assert bbc.formal_title == "Lead Enterprise Architect - Technology Transformation Group"
    assert "Head of Architecture" in bbc.acting_responsibilities[0]

    # Content with inflated title gets sanitized back to canonical formal title
    inflated_view = (
        "### BBC Studios\n"
        "**Head of Enterprise Architecture**\n"
    )
    sanitized, alerts = sanitize_projection_content(inflated_view)
    assert "Lead Enterprise Architect - Technology Transformation Group" in sanitized
    assert "Head of Enterprise Architecture" not in sanitized
