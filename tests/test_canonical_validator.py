"""Unit tests for Canonical Validator and Conflict Audit Reporting.

Tests that scripts/canonical_validator.py detects conflicting claims
and produces out/<target-slug>/runtime/canonical-conflict-report.yaml
conforming to specs/005-canonical-record-integration/contracts/canonical-conflict-report-contract.yaml.
"""

from pathlib import Path
import tempfile
import yaml
import pytest

from scripts.canonical_validator import detect_conflicts_in_text, generate_conflict_audit_report


def test_detect_conflicts_in_text_captures_discrepancies():
    sample_text = """
# Secondary CV
- Education: MSc, Federal University of Rio de Janeiro (2000)
- Role: Head of Enterprise Architecture & Digital Evolution at BBC Studios
- Period: WPP Media (2022 – Present)
- Achievement: Established and led the enterprise architecture governance function
"""
    conflicts = detect_conflicts_in_text(sample_text, source_file="secondary_cv.md")
    assert len(conflicts) >= 4

    field_types = [c["field_type"] for c in conflicts]
    assert "degree_level" in field_types
    assert "formal_title" in field_types
    assert "dates" in field_types
    assert "claim_strength" in field_types

    for c in conflicts:
        assert c["action_taken"] == "canonical_override"
        assert c["severity"] in ["high", "medium", "low"]
        assert c["canonical_fact"]


def test_generate_conflict_audit_report_writes_conforming_yaml(tmp_path):
    # Create mock source file
    src_file = tmp_path / "legacy_resume.md"
    src_file.write_text(
        "Alexandre Franco\nMSc, Federal University of Rio de Janeiro\nHead of Enterprise Architecture at BBC",
        encoding="utf-8"
    )

    out_report = tmp_path / "out" / "test-slug" / "runtime" / "canonical-conflict-report.yaml"
    report = generate_conflict_audit_report(
        target_slug="test-slug",
        source_paths=[str(src_file)],
        output_path=str(out_report)
    )

    assert out_report.exists()
    assert report["target_slug"] == "test-slug"
    assert report["total_conflicts"] >= 2
    assert "evaluated_at" in report
    assert isinstance(report["conflicts"], list)

    with open(out_report, "r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)
    assert loaded["total_conflicts"] == report["total_conflicts"]
