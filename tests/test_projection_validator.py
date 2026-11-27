"""Unit tests for Unified Deterministic Projection Validator (User Story 3).

Tests:
- T020: Education date/institution verification and automated sanitization (BSc 1988–1991 vs 1995–1999, UMC vs UFRJ)
- T021: Certification audit (FATAL on unverified AWS, Sun SCEA/SCJP)
- T022: Language proficiency audit (FATAL on Spanish Fluent/Full Professional vs Elementary)
- T023: Named technology claims (FATAL on direct unevidenced platform claims, permitted on transferable/gap framing)
"""

from pathlib import Path
import pytest
import yaml

from src.scripts.canonical_models import ProjectionValidationReport
from src.scripts.projection_validator import (
    validate_projection_content,
    sanitize_projection_content,
    validate_opportunity_projections,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_education_date_and_institution_sanitization():
    """T020: Education date mutation (1995–1999) and inflated institution (UFRJ/MSc) are detected and sanitized."""
    corrupted_content = (
        "## Education\n"
        "- **MSc in Computer Science**, Federal University of Rio de Janeiro (1995–1999)\n"
    )

    sanitized, findings = sanitize_projection_content(corrupted_content)

    # Content should be rewritten to canonical truth
    assert "1988–1991" in sanitized or "1988 - 1991" in sanitized
    assert "Universidade de Mogi das Cruzes" in sanitized
    assert "BSc" in sanitized
    assert "UFRJ" not in sanitized
    assert "Federal University of Rio de Janeiro" not in sanitized
    assert "1995" not in sanitized

    # Findings should log SANITIZED severity
    assert len(findings) >= 1
    for f in findings:
        assert f.severity == "SANITIZED"


def test_certification_audit_unverified_certs_fatal():
    """T021: Certifications not in canonical record (AWS, Sun SCEA/SCJP) trigger FATAL findings."""
    valid_content = (
        "## Certifications\n"
        "- TOGAF 9 Certified Enterprise Architect\n"
        "- Certified SAFe® 5 Agilist\n"
    )
    report_valid = validate_projection_content(valid_content)
    assert not any(f.category == "certification" for f in report_valid.findings)

    # Corrupted with AWS and Sun SCEA
    corrupted_content = (
        "## Certifications\n"
        "- AWS Certified Solutions Architect - Professional\n"
        "- Sun Certified Enterprise Architect (SCEA)\n"
        "- TOGAF 9 Certified\n"
    )
    report_corrupted = validate_projection_content(corrupted_content)
    cert_findings = [f for f in report_corrupted.findings if f.category == "certification"]
    
    assert len(cert_findings) >= 1
    assert any("aws" in f.reason.lower() for f in cert_findings)
    assert any("scea" in f.reason.lower() or "sun" in f.reason.lower() for f in cert_findings)
    assert all(f.severity == "FATAL" for f in cert_findings)
    assert report_corrupted.overall_status == "FAILED"


def test_language_proficiency_audit_fatal_on_inflation():
    """T022: Inflating Spanish proficiency beyond Elementary triggers FATAL finding."""
    valid_content = (
        "## Languages\n"
        "- Portuguese: Native\n"
        "- English: Full Professional\n"
        "- Spanish: Elementary proficiency\n"
    )
    report_valid = validate_projection_content(valid_content)
    assert not any(f.category == "language" for f in report_valid.findings)

    corrupted_content = (
        "## Languages\n"
        "- Portuguese: Native\n"
        "- English: Fluent\n"
        "- Spanish: Fluent and bilingual professional proficiency\n"
    )
    report_corrupted = validate_projection_content(corrupted_content)
    lang_findings = [f for f in report_corrupted.findings if f.category == "language"]

    assert len(lang_findings) >= 1
    assert any("spanish" in f.reason.lower() for f in lang_findings)
    assert all(f.severity == "FATAL" for f in lang_findings)
    assert report_corrupted.overall_status == "FAILED"


def test_named_technology_direct_claims_vs_transferable_framing():
    """T023: Direct unevidenced platform claims fail (FATAL); transferable/gap framing passes."""
    # Direct claim - should FAIL with FATAL
    direct_claim_content = (
        "## Core Achievements\n"
        "- Led the implementation of Workday Financials and NetSuite ERP across business units.\n"
        "- Architected end-to-end automated billing integration using Coupa and Concur.\n"
    )
    report_direct = validate_projection_content(direct_claim_content)
    tech_findings = [f for f in report_direct.findings if f.category == "technology"]

    assert len(tech_findings) >= 1
    assert any("workday" in f.reason.lower() for f in tech_findings)
    assert all(f.severity == "FATAL" for f in tech_findings)
    assert report_direct.overall_status == "FAILED"

    # Transferable / Gap framing - should PASS
    transferable_content = (
        "## Strategic Alignment\n"
        "- Evaluated enterprise SaaS architecture patterns comparable to Workday and NetSuite platforms.\n"
        "- Experience with corporate procurement workflows transferable to Coupa and Concur environments.\n"
        "- Gap analysis: While direct Workday administration is an unmatched requirement, demonstrated enterprise integration at global scale.\n"
    )
    report_transferable = validate_projection_content(transferable_content)
    tech_findings_trans = [f for f in report_transferable.findings if f.category == "technology"]
    assert len(tech_findings_trans) == 0


def test_technology_bypass_with_generic_ecosystem_or_pattern_rejected():
    """Generic words like 'ecosystem' or 'pattern' must not exempt direct unevidenced platform claims."""
    bypass_content = (
        "## Key Achievements\n"
        "- Led Workday ecosystem rollout across business units.\n"
        "- Implemented Coupa architecture patterns globally.\n"
    )
    report = validate_projection_content(bypass_content)
    tech_findings = [f for f in report.findings if f.category == "technology" and f.severity == "FATAL"]
    assert len(tech_findings) == 2
    assert report.overall_status == "FAILED"


def test_dynamic_opportunity_analysis_required_vocabulary_enforced():
    """Unevidenced tools from opportunity_analysis.ats_vocabulary.required_job_vocabulary must fail when claimed directly."""
    opp_analysis = {
        "ats_vocabulary": {
            "candidate_evidenced_vocabulary": [{"term": "LeanIX"}],
            "required_job_vocabulary": [{"term": "ServiceNow"}],
        }
    }
    content = (
        "## Experience\n"
        "- Implemented ServiceNow ITSM platform across global operations.\n"
    )
    report = validate_projection_content(content, opportunity_analysis=opp_analysis)
    tech_findings = [f for f in report.findings if f.category == "technology" and f.severity == "FATAL"]
    assert len(tech_findings) == 1
    assert "servicenow" in tech_findings[0].reason.lower()
    assert report.overall_status == "FAILED"


def test_cross_opportunity_isolation_detects_other_slug_reference():
    """References to another opportunity directory under out/ trigger FATAL isolation finding."""
    content = (
        "## Notes\n"
        "Reused summary structure from out/other-role-slug/resume-executive.md.\n"
    )
    report = validate_projection_content(content, target_slug="current-role")
    iso_findings = [f for f in report.findings if f.category == "isolation" and f.severity == "FATAL"]
    assert len(iso_findings) >= 1
    assert report.checks["cross_opportunity_isolation"].status == "FAILED"
    assert report.overall_status == "FAILED"


def test_empty_or_missing_opportunity_dir_fails(tmp_path):
    """Validating a missing or empty opportunity directory must return FAILED, not PASSED."""
    report = validate_opportunity_projections("nonexistent-role", out_root=tmp_path)
    assert report.overall_status == "FAILED"
    assert report.summary.unresolved_defects >= 1


def test_path_traversal_target_slug_rejected(tmp_path):
    """Invalid or path-traversal target_slug values must raise ValueError."""
    with pytest.raises(ValueError):
        validate_opportunity_projections("../etc", out_root=tmp_path)


def test_education_date_sanitization_precision():
    """Education date sanitization must not insert double spaces or corrupt non-education 1995-1999 dates."""
    content = (
        "## Experience\n"
        "- **Developer**, Example Corp (1995–1999)\n"
        "## Education\n"
        "- **BSc in Computer Science**, Universidade de Mogi das Cruzes (1995–1999)\n"
    )
    sanitized, findings = sanitize_projection_content(content)
    assert "( 1988–1991)" not in sanitized
    assert "(1988–1991)" in sanitized
    assert "Example Corp (1995–1999)" in sanitized
    assert len(findings) == 1
