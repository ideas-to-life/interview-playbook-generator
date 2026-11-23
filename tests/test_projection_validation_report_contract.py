"""Contract test for ProjectionValidationReport schema conforming to
specs/006-projection-data-integrity/contracts/projection-validation-report-contract.yaml.
"""

import os
from pathlib import Path
import pytest
import yaml

from src.scripts.canonical_models import (
    ProjectionValidationReport,
    ValidationSummary,
    ValidationFinding,
    CheckDetail,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = REPO_ROOT / "specs/006-projection-data-integrity/contracts/projection-validation-report-contract.yaml"


def test_contract_file_exists():
    assert CONTRACT_PATH.exists(), f"Contract file not found at {CONTRACT_PATH}"


def test_projection_validation_report_schema_contract():
    report = ProjectionValidationReport(
        target_slug="tenth-ai-lead-enterprise-architect",
        evaluated_at="2026-09-24T12:00:00Z",
        overall_status="PASSED_WITH_SANITIZATION",
        validator_version="1.0.0",
        summary=ValidationSummary(
            total_files_audited=3,
            total_findings=2,
            sanitized_count=2,
            unresolved_defects=0,
        ),
        checks={
            "education": CheckDetail(status="SANITIZED", details="Auto-sanitized graduation date to 1988-1991"),
            "certifications": CheckDetail(status="PASSED", details="All certifications match canonical"),
            "languages": CheckDetail(status="PASSED", details="All language proficiencies valid"),
            "employment_chronology": CheckDetail(status="SANITIZED", details="Sanitized BBC title"),
            "technology_claims": CheckDetail(status="PASSED", details="No unevidenced platform claims"),
            "cross_opportunity_isolation": CheckDetail(status="PASSED", details="Zero contamination detected"),
        },
        findings=[
            ValidationFinding(
                source_file="resume-executive.md",
                category="education",
                severity="SANITIZED",
                generated_claim="1995–1999",
                canonical_baseline="1988–1991",
                reason="Education graduation date conflicted with canonical career record",
                action_taken="sanitized_in_place",
            ),
            ValidationFinding(
                source_file="resume-ats.md",
                category="employment",
                severity="SANITIZED",
                generated_claim="Head of Enterprise Architecture",
                canonical_baseline="Lead Enterprise Architect - Technology Transformation Group",
                reason="Title inflated beyond approved canonical aliases",
                action_taken="sanitized_in_place",
            ),
        ],
    )

    data = report.to_dict()

    # Verify top-level structure per contract
    assert "report_metadata" in data
    assert "summary" in data
    assert "checks" in data
    assert "findings" in data

    # Verify report_metadata fields
    meta = data["report_metadata"]
    assert meta["target_slug"] == "tenth-ai-lead-enterprise-architect"
    assert meta["overall_status"] in ["PASSED", "FAILED", "PASSED_WITH_SANITIZATION"]
    assert meta["validator_version"] == "1.0.0"

    # Verify summary fields
    summary = data["summary"]
    assert summary["total_files_audited"] == 3
    assert summary["total_findings"] == 2
    assert summary["sanitized_count"] == 2
    assert summary["unresolved_defects"] == 0

    # Verify checks
    checks = data["checks"]
    for required_check in [
        "education",
        "certifications",
        "languages",
        "employment_chronology",
        "technology_claims",
        "cross_opportunity_isolation",
    ]:
        assert required_check in checks
        assert checks[required_check]["status"] in ["PASSED", "FAILED", "SANITIZED"]

    # Verify findings
    findings = data["findings"]
    assert len(findings) == 2
    for f in findings:
        assert f["category"] in ["education", "certification", "language", "employment", "technology", "isolation"]
        assert f["severity"] in ["FATAL", "SANITIZED", "WARNING"]
        assert f["action_taken"] in ["sanitized_in_place", "validation_failure_block", "warning_logged"]
        assert len(f["generated_claim"]) > 0
        assert len(f["reason"]) > 0


def test_validate_projection_content_conforms_to_contract_checks():
    """Actual validate_projection_content() output must emit the 6 contract check keys."""
    from src.scripts.projection_validator import validate_projection_content

    report = validate_projection_content("## Summary\n- Enterprise Architect\n")
    data = report.to_dict()
    checks = data["checks"]

    for required_check in [
        "education",
        "certifications",
        "languages",
        "employment_chronology",
        "technology_claims",
        "cross_opportunity_isolation",
    ]:
        assert required_check in checks, f"Missing contract check key: {required_check}"
        assert checks[required_check]["status"] in ["PASSED", "FAILED", "SANITIZED"]


def test_validate_opportunity_projections_preserves_sanitization_findings(tmp_path):
    """validate_opportunity_projections() must preserve Stage 1 SANITIZED findings in the emitted report."""
    from src.scripts.projection_validator import validate_opportunity_projections

    slug = "sanitization-test-role"
    opp_dir = tmp_path / slug
    opp_dir.mkdir(parents=True)
    resume_path = opp_dir / "resume-executive.md"
    resume_path.write_text(
        "## Education\n"
        "- **MSc in Computer Science**, Federal University of Rio de Janeiro (1995–1999)\n",
        encoding="utf-8",
    )

    report = validate_opportunity_projections(slug, auto_sanitize=True, out_root=tmp_path)

    updated = resume_path.read_text(encoding="utf-8")
    assert "Universidade de Mogi das Cruzes" in updated
    assert "1988–1991" in updated
    assert "1995" not in updated

    assert report.overall_status == "PASSED_WITH_SANITIZATION"
    assert report.summary.sanitized_count >= 1
    assert report.checks["education"].status == "SANITIZED"
    assert len(report.findings) >= 1

    report_yaml = opp_dir / "runtime" / "projection-validation-report.yaml"
    assert report_yaml.exists()
    persisted = yaml.safe_load(report_yaml.read_text(encoding="utf-8"))
    assert persisted["report_metadata"]["overall_status"] == "PASSED_WITH_SANITIZATION"
    assert persisted["summary"]["sanitized_count"] >= 1
    assert len(persisted["findings"]) >= 1
