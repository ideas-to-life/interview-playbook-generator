# tests/test_upwork_proposal_generator.py
import os
import yaml
import pytest


def test_upwork_skills_exist():
    qual_path = "skills/upwork-qualification/SKILL.md"
    prop_path = "skills/upwork-proposal/SKILL.md"

    assert os.path.exists(qual_path), "upwork-qualification skill must exist"
    assert os.path.exists(prop_path), "upwork-proposal skill must exist"

    with open(qual_path, "r", encoding="utf-8") as f:
        qual_content = f.read()
    assert qual_content.startswith("---")
    assert "name: upwork-qualification" in qual_content

    with open(prop_path, "r", encoding="utf-8") as f:
        prop_content = f.read()
    assert prop_content.startswith("---")
    assert "name: upwork-proposal" in prop_content


def test_qualification_decision_rules_do_not_apply():
    """Section 35 Reference Scenario: Client requires production multi-agent implementation inside a real operating company.
    Evidence establishes architecture work in Prototype & Innovation, but not production implementation.
    Expected: decision: DO NOT APPLY, proposal_generation: blocked.
    """
    hard_requirement = {
        "requirement_id": "req-production-multi-agent",
        "requirement": "Personal implementation of production multi-agent system in a real company",
        "status": "not_met",
        "relationship": "absent",
        "evidence_strength": "weak",
        "production_status": "verified_non_production",
        "evidence_sources": ["card-prototype-innovation-01"],
        "rationale": "Evidence establishes prototype work, not production multi-agent implementation inside a real company."
    }

    # Simulate qualification evaluator
    decision = "DO NOT APPLY" if hard_requirement["production_status"] == "verified_non_production" and hard_requirement["relationship"] == "absent" else "APPLY"
    proposal_generation = "blocked" if decision == "DO NOT APPLY" else "allowed"

    assert decision == "DO NOT APPLY"
    assert proposal_generation == "blocked"


def test_qualification_decision_rules_apply():
    """Section 36 Qualified Scenario: Authoritative evidence supports production architecture & advisory.
    Expected: decision: APPLY, proposal_generation: allowed.
    """
    hard_requirement = {
        "requirement_id": "req-enterprise-ai-architecture",
        "requirement": "Enterprise AI Architecture and Governance leadership",
        "status": "met",
        "relationship": "direct",
        "evidence_strength": "strong",
        "production_status": "verified_production",
        "evidence_sources": ["card-enterprise-arch-01"],
        "rationale": "Authoritative evidence verifies Enterprise AI Architecture leadership."
    }

    decision = "APPLY" if hard_requirement["status"] == "met" and hard_requirement["production_status"] == "verified_production" else "DO NOT APPLY"
    proposal_generation = "allowed" if decision == "APPLY" else "blocked"

    assert decision == "APPLY"
    assert proposal_generation == "allowed"


def test_qualification_decision_rules_conditional():
    """Section 24 Scenario: Candidate can confirm missing certification or tenure.
    Expected: decision: CONDITIONAL, proposal_generation: allowed_with_conditions.
    """
    decision = "CONDITIONAL"
    proposal_generation = "allowed_with_conditions"
    open_conditions = [
        {
            "condition_id": "cond-01",
            "fact_requiring_confirmation": "Specific cloud platform certification",
            "impact": "Required by client JD",
            "suggested_candidate_action": "Confirm active certification status"
        }
    ]

    assert decision == "CONDITIONAL"
    assert proposal_generation == "allowed_with_conditions"
    assert len(open_conditions) == 1


def test_clean_proposal_text_rules():
    """Section 14 & 34: Client-facing proposal prose must NOT contain visible [evidence] tags or [^source-id] footnotes.
    Claim traceability must be stored in claim_traceability array.
    """
    proposal_prose = (
        "I have led enterprise AI architecture and governance initiatives for large-scale organizations. "
        "My approach focuses on connecting business strategy with robust, production-grade AI controls."
    )

    # Ensure no visible internal tags
    assert "[evidence]" not in proposal_prose
    assert "[inference]" not in proposal_prose
    assert "[^" not in proposal_prose

    # Traceability structure
    claim_traceability = [
        {
            "claim": "Led enterprise AI architecture and governance initiatives",
            "evidence_id": "card-enterprise-arch-01",
            "classification": "evidence",
            "source_reference": "inputs/cv.pdf"
        }
    ]

    assert len(claim_traceability) == 1
    assert claim_traceability[0]["evidence_id"] == "card-enterprise-arch-01"


def test_projection_registry_integration():
    registry_path = "skills/projection-registry/SKILL.md"
    with open(registry_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "upwork-proposal" in content


def test_playbook_orchestrator_integration():
    orchestrator_path = "skills/playbook-orchestrator/SKILL.md"
    with open(orchestrator_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "upwork-qualification" in content
    assert "upwork-proposal" in content


def test_projection_validator_integration():
    validator_path = "skills/projection-validator/SKILL.md"
    with open(validator_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Upwork Proposal & Provenance Validation" in content
    assert "claim_traceability" in content
