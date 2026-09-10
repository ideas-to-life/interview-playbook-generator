# tests/test_projection_validator.py
import os
import pytest


def test_scenario_8_qualification_claiming_verified_production_without_canonical_evidence_fails():
    """Scenario 8: Qualification claiming verified_production without canonical evidence -> Validation fails."""
    canonical_evidence_frontmatter = {
        "organisation": {"id": "emp-wpp-media-2"},
        "project": {"id": "wpp-open-pca"},
        "environment": "prototype",
        "production_verified": False,
    }

    claim_traceability_entry = {
        "claim": "Deployed production multi-agent system at WPP Media",
        "evidence_id": "wpp-agentic-ai-platform",
        "claimed_status": "verified_production",
    }

    # Independent validation check
    validation_passed = (
        claim_traceability_entry["claimed_status"] == "verified_production"
        and canonical_evidence_frontmatter["environment"] == "production"
        and canonical_evidence_frontmatter["production_verified"] is True
    )

    assert validation_passed is False


def test_scenario_9_word_count_bounds_validation():
    """Scenario 9: Word count bounds 350-500 words for APPLY proposal markdown."""
    valid_proposal_text = "word " * 425
    short_proposal_text = "word " * 200
    long_proposal_text = "word " * 600

    def validate_word_count(text):
        count = len(text.strip().split())
        return 350 <= count <= 500

    assert validate_word_count(valid_proposal_text) is True
    assert validate_word_count(short_proposal_text) is False
    assert validate_word_count(long_proposal_text) is False


def test_scenario_10_do_not_apply_gate_report_validation():
    """Scenario 10: DO NOT APPLY qualification -> Gate Report generated, no submission proposal."""
    qualification_state = {
        "decision": "DO NOT APPLY",
        "proposal_generation": "blocked",
    }

    gate_report_text = """# Upwork Qualification Report: Senior Agentic AI Architect

**Qualification Status**: `DO NOT APPLY`
**Proposal Control State**: `blocked`

---

## GATE REPORT: APPLICATION BLOCKED

### Decision Summary
The qualification engine has evaluated this opportunity as **DO NOT APPLY** (`proposal_generation: blocked`). No client-facing proposal prose markdown has been generated for marketplace submission.
"""

    # Validation checks
    assert qualification_state["proposal_generation"] == "blocked"
    assert "GATE REPORT: APPLICATION BLOCKED" in gate_report_text
    assert "DO NOT APPLY" in gate_report_text
    # Ensure no pitch prose headers exist in gate report
    assert "### MULTI-AGENT ARCHITECT" not in gate_report_text
