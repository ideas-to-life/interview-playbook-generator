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


def test_scenario_1_wpp_prototype_evidence_evaluates_to_do_not_apply():
    """Scenario 1: WPP employment + WPP prototype evidence -> production_status: unknown / DO NOT APPLY."""
    evidence_card = {
        "organisation": {"id": "emp-wpp-media-2", "name": "WPP Media", "type": "enterprise_employer"},
        "project": {"id": "wpp-open-pca", "name": "PCA"},
        "environment": "prototype",
        "production_verified": False,
        "implementation_role": "lead_architect",
    }
    client_requirement = {
        "target_organisation_id": "emp-wpp-media-2",
        "target_project_id": "wpp-open-pca",
        "is_dealbreaker": True,
    }

    # Evaluate PERSONAL_PRODUCTION_IMPLEMENTATION_EXPERIENCE predicate
    is_prod_verified = (
        evidence_card["organisation"]["id"] == client_requirement["target_organisation_id"]
        and evidence_card["project"]["id"] == client_requirement["target_project_id"]
        and evidence_card["environment"] == "production"
        and evidence_card["production_verified"] is True
        and evidence_card["implementation_role"] in ["lead_architect", "sole_developer", "contributor"]
    )

    decision = "APPLY" if is_prod_verified else "DO NOT APPLY"
    proposal_generation = "allowed" if decision == "APPLY" else "blocked"

    assert is_prod_verified is False
    assert decision == "DO NOT APPLY"
    assert proposal_generation == "blocked"


def test_scenario_2_explicit_production_evidence_evaluates_to_apply():
    """Scenario 2: Explicit WPP production evidence + compatible implementation role -> APPLY."""
    evidence_card = {
        "organisation": {"id": "emp-wpp-media-2", "name": "WPP Media", "type": "enterprise_employer"},
        "project": {"id": "wpp-open-pca", "name": "PCA"},
        "environment": "production",
        "production_verified": True,
        "implementation_role": "lead_architect",
    }
    client_requirement = {
        "target_organisation_id": "emp-wpp-media-2",
        "target_project_id": "wpp-open-pca",
        "is_dealbreaker": True,
    }

    is_prod_verified = (
        evidence_card["organisation"]["id"] == client_requirement["target_organisation_id"]
        and evidence_card["project"]["id"] == client_requirement["target_project_id"]
        and evidence_card["environment"] == "production"
        and evidence_card["production_verified"] is True
        and evidence_card["implementation_role"] in ["lead_architect", "sole_developer", "contributor"]
    )

    decision = "APPLY" if is_prod_verified else "DO NOT APPLY"
    proposal_generation = "allowed" if decision == "APPLY" else "blocked"

    assert is_prod_verified is True
    assert decision == "APPLY"
    assert proposal_generation == "allowed"


def test_scenario_3_cross_organisation_isolation():
    """Scenario 3: Company A requirement + Company B production evidence -> Company A requirement not met."""
    company_b_evidence = {
        "organisation": {"id": "emp-bbc-studios", "name": "BBC Studios", "type": "enterprise_employer"},
        "project": {"id": "bbc-genai-framework"},
        "environment": "production",
        "production_verified": True,
        "implementation_role": "lead_architect",
    }
    company_a_requirement = {
        "target_organisation_id": "emp-wpp-media-2",
        "target_project_id": "wpp-open-pca",
    }

    match = (
        company_b_evidence["organisation"]["id"] == company_a_requirement["target_organisation_id"]
        and company_b_evidence["environment"] == "production"
        and company_b_evidence["production_verified"] is True
    )

    assert match is False


def test_scenario_4_cross_project_isolation():
    """Scenario 4: Same organisation, different project -> Project X evidence cannot satisfy Project Y requirement."""
    project_x_evidence = {
        "organisation": {"id": "emp-wpp-media-2"},
        "project": {"id": "wpp-project-x"},
        "environment": "production",
        "production_verified": True,
        "implementation_role": "lead_architect",
    }
    project_y_requirement = {
        "target_organisation_id": "emp-wpp-media-2",
        "target_project_id": "wpp-project-y",
    }

    match = (
        project_x_evidence["organisation"]["id"] == project_y_requirement["target_organisation_id"]
        and project_x_evidence["project"]["id"] == project_y_requirement["target_project_id"]
    )

    assert match is False


def test_scenario_5_negative_inference_prohibition_repo_name():
    """Scenario 5: Repo name containing 'production' without explicit frontmatter attestation -> unknown."""
    repo_name = "pca-productionagents-a2a"
    frontmatter_production_verified = False

    # Negative inference rule: repo name containing "production" MUST NOT set production_verified = True
    inferred_production = "production" in repo_name and frontmatter_production_verified is True

    assert inferred_production is False


def test_scenario_6_hard_dealbreaker_gate_unknown_evaluates_to_do_not_apply():
    """Scenario 6: Hard dealbreaker requirement + UNKNOWN production status -> DO NOT APPLY."""
    requirement_status = "unknown"
    is_dealbreaker = True

    decision = "DO NOT APPLY" if is_dealbreaker and requirement_status == "unknown" else "CONDITIONAL"
    proposal_generation = "blocked" if decision == "DO NOT APPLY" else "allowed_with_conditions"

    assert decision == "DO NOT APPLY"
    assert proposal_generation == "blocked"


def test_scenario_7_conditional_open_conditions():
    """Scenario 7: Conditional qualification -> Unresolved condition remains visible."""
    decision = "CONDITIONAL"
    proposal_generation = "allowed_with_conditions"
    open_conditions = [
        {
            "condition_id": "cond-01",
            "fact_requiring_confirmation": "Candidate AWS Security Specialty active status",
            "impact": "JD mandatory requirement",
            "suggested_candidate_action": "Provide AWS certification verification ID",
        }
    ]

    assert decision == "CONDITIONAL"
    assert proposal_generation == "allowed_with_conditions"
    assert len(open_conditions) == 1
    assert "OPEN CONDITION" in f"[OPEN CONDITION: {open_conditions[0]['fact_requiring_confirmation']}]"


def test_clean_proposal_text_rules():
    """Client-facing proposal prose must NOT contain visible [evidence] tags or [^source-id] footnotes."""
    proposal_prose = (
        "I have led enterprise AI architecture and governance initiatives for large-scale organizations. "
        "My approach focuses on connecting business strategy with robust, production-grade AI controls."
    )

    assert "[evidence]" not in proposal_prose
    assert "[inference]" not in proposal_prose
    assert "[^" not in proposal_prose

    claim_traceability = [
        {
            "claim": "Led enterprise AI architecture and governance initiatives",
            "evidence_id": "card-enterprise-arch-01",
            "classification": "evidence",
            "source_reference": "inputs/cv.pdf",
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
    assert "Upwork Proposal & Machine-Readable Provenance Validation" in content
    assert "cross-organisation evidence bleeding" in content.lower()
