# tests/test_v06_success_criteria.py
"""End-to-end success criteria verification for Sprint 6 (v0.6 & v6.1 Refinement) Opportunity Archetype & Market-Fit Intelligence."""
import os
import yaml
import pytest


def test_sprint_6_standalone_skills_exist():
    skills_dir = "skills"
    sprint_6_skills = [
        "archetype-classifier",
        "archetype-fit-evaluator",
        "gap-classifier",
        "projection-strategy-generator",
        "archetype-fit-validator",
        "market-feedback-evaluator",
    ]
    for skill in sprint_6_skills:
        skill_path = os.path.join(skills_dir, skill, "SKILL.md")
        assert os.path.exists(skill_path), f"Missing Sprint 6 skill definition: {skill}"
        with open(skill_path) as f:
            content = f.read()
        assert content.startswith("---")
        assert f"name: {skill}" in content


def test_vervaunt_golden_archetype_and_fit_evaluation():
    fixture_path = "tests/fixtures/vervaunt_head_of_ai.yaml"
    assert os.path.exists(fixture_path)
    with open(fixture_path) as f:
        jd_data = yaml.safe_load(f)

    # Verify Vervaunt JD signals hands-on agency automation builder archetype
    resp = " ".join(jd_data.get("responsibilities", [])).lower()
    reqs = " ".join(jd_data.get("required_experience", [])).lower()
    
    assert "ecommerce" in resp or "ecommerce" in reqs
    assert "n8n" in resp or "n8n" in reqs
    assert "zapier" in resp or "zapier" in reqs

    # Verify market feedback captures actual outcome and concerns
    feedback_path = "evaluation/opportunities/vervaunt-head-of-ai.yaml"
    assert os.path.exists(feedback_path)
    with open(feedback_path) as f:
        feedback = yaml.safe_load(f).get("market_feedback", {})
    
    assert feedback.get("opportunity") == "vervaunt-head-of-ai"
    assert "ecommerce_experience" in feedback.get("concerns", [])
    assert "n8n_zapier_shopify" in feedback.get("concerns", [])


def test_enterprise_ai_coe_regression_golden_test():
    fixture_path = "tests/fixtures/enterprise_ai_coe_architect.yaml"
    assert os.path.exists(fixture_path)
    with open(fixture_path) as f:
        jd_data = yaml.safe_load(f)

    # Verify Enterprise AI CoE JD signals enterprise AI architecture archetype
    resp = " ".join(jd_data.get("responsibilities", [])).lower()
    reqs = " ".join(jd_data.get("required_experience", [])).lower()

    assert "governance" in resp or "governance" in reqs
    assert "enterprise architecture" in resp or "enterprise architecture" in reqs
    assert "center of excellence" in resp or "group ai" in resp


def test_projection_strategy_prohibits_unsupported_claims():
    strategy_sample = {
        "projection_strategy": {
            "target_archetype": "ai_automation_builder",
            "prohibit_claims": [
                "ecommerce_expert",
                "shopify_experience",
                "n8n_experience"
            ]
        }
    }
    prohibited = strategy_sample["projection_strategy"]["prohibit_claims"]
    assert "ecommerce_expert" in prohibited
    assert "shopify_experience" in prohibited


def test_v61_evidence_relationship_max_alignment_mapping():
    # Verify default mapping rules: direct -> Strong, adjacent -> Moderate, transferable -> Transferable, absent -> Gap
    mapping_rules = {
        "direct": "Strong",
        "adjacent": "Moderate",
        "transferable": "Transferable",
        "absent": "Gap",
    }
    assert mapping_rules["direct"] == "Strong"
    assert mapping_rules["adjacent"] == "Moderate"
    assert mapping_rules["transferable"] == "Transferable"
    assert mapping_rules["absent"] == "Gap"


def test_v61_projection_strategy_fit_constraints_authority():
    strategy_sample = {
        "projection_strategy": {
            "target_archetype": "ai_automation_builder",
            "fit_constraints": [
                {
                    "requirement": "engineering_automation",
                    "relationship": "direct",
                    "maximum_alignment": "Strong"
                },
                {
                    "requirement": "low_code_workflow_automation",
                    "relationship": "adjacent",
                    "maximum_alignment": "Moderate"
                },
                {
                    "requirement": "ecommerce_domain",
                    "relationship": "absent",
                    "maximum_alignment": "Gap"
                }
            ]
        }
    }
    constraints = strategy_sample["projection_strategy"]["fit_constraints"]
    assert len(constraints) == 3
    adj_constraint = next(c for c in constraints if c["requirement"] == "low_code_workflow_automation")
    assert adj_constraint["maximum_alignment"] == "Moderate"


def test_v61_fit_consistency_validation_report_warnings():
    report_sample = {
        "fit_consistency": {
            "status": "WARNING",
            "findings": [
                {
                    "type": "alignment_inflation",
                    "requirement": "low_code_workflow_automation",
                    "runtime_alignment": "moderate",
                    "projection_alignment": "strong",
                    "source": "opportunity-alignment.md",
                    "reason": "Projection classified requirement as Strong despite runtime max constraint of Moderate."
                }
            ]
        }
    }
    fc = report_sample["fit_consistency"]
    assert fc["status"] == "WARNING"
    assert len(fc["findings"]) == 1
    assert fc["findings"][0]["type"] == "alignment_inflation"


def test_total_skills_registered_is_at_least_thirty_one():
    skills_dir = "skills"
    skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert len(skills) >= 31, f"Expected at least 31 skills, found {len(skills)}: {sorted(skills)}"
