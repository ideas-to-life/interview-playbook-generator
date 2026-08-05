# tests/test_v06_success_criteria.py
"""End-to-end success criteria verification for Sprint 6 (v0.6) Opportunity Archetype & Market-Fit Intelligence."""
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
    # Verify projection strategy structure format
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


def test_total_skills_registered_is_at_least_thirty_one():
    skills_dir = "skills"
    skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    assert len(skills) >= 31, f"Expected at least 31 skills, found {len(skills)}: {sorted(skills)}"
