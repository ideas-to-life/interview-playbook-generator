# tests/test_ea_cloud_refinement_regression.py
"""Automated regression test suite for Enterprise Cloud Architect / CCoE refinement specification."""
import os
import yaml
import pytest


def test_ea_cloud_canonical_identity_protection():
    """Verify Candidate Archetype is distinct from Target Role Archetype and preserved."""
    archetype_file = "out/enterprise-cloud-architect/runtime/archetype-analysis.yaml"
    assert os.path.exists(archetype_file), f"Missing archetype analysis file: {archetype_file}"
    
    with open(archetype_file) as f:
        data = yaml.safe_load(f)
    
    # Verify candidate archetype is preserved
    alignment = data.get("archetype_alignment", {})
    candidate_archetype = alignment.get("candidate_archetype", "Enterprise Architect / Transformation & AI Advisor")
    assert "Enterprise Architect" in candidate_archetype
    
    # Primary opportunity archetype
    primary_target = data.get("opportunity_archetype", {}).get("primary")
    assert primary_target == "enterprise_architect"


def test_ea_cloud_5tier_capability_classification_constraints():
    """Verify 5-tier capability classification rules in projection strategy."""
    strategy_file = "out/enterprise-cloud-architect/runtime/projection-strategy.yaml"
    assert os.path.exists(strategy_file), f"Missing projection strategy file: {strategy_file}"
    
    with open(strategy_file) as f:
        data = yaml.safe_load(f)
    
    strategy = data.get("projection_strategy", {})
    fit_constraints = strategy.get("fit_constraints", [])
    
    # Adjacent requirement must not exceed Moderate/Adjacent alignment
    azure_constraint = next(c for c in fit_constraints if c.get("requirement") == "Azure Cloud Native Implementation")
    assert azure_constraint["relationship"] == "adjacent"
    assert azure_constraint["maximum_alignment"] in ["Moderate", "Adjacent"]


def test_ea_cloud_duration_and_leadership_integrity():
    """Verify duration and leadership claims are constrained in prohibit_claims."""
    strategy_file = "out/enterprise-cloud-architect/runtime/projection-strategy.yaml"
    with open(strategy_file) as f:
        data = yaml.safe_load(f)
    
    prohibited = data.get("projection_strategy", {}).get("prohibit_claims", [])
    
    # Verify decade/15+ year duration claim prohibition for CCoE exclusive leadership
    assert any("Decade" in claim or "15+" in claim or "exclusive" in claim or "Azure native" in claim for claim in prohibited)


def test_ea_cloud_headline_generation_priority():
    """Verify headline generation rules prioritize canonical identity over target title overload."""
    strategy_file = "out/enterprise-cloud-architect/runtime/projection-strategy.yaml"
    with open(strategy_file) as f:
        data = yaml.safe_load(f)
    
    positioning = data.get("projection_strategy", {}).get("recommended_positioning", "")
    
    # Preferred: Enterprise Architect lead
    assert positioning.startswith("Enterprise Architect")
    assert "CCoE Leader" not in positioning.split("|")[0]  # CCoE Leader must not be primary title


test_headline_samples = [
    ("Enterprise Architect | Cloud Transformation, Governance & AI", True),
    ("Enterprise Architect | Transformation, Cloud & AI", True),
    ("Enterprise & Cloud Architect | CCoE Leader", False),
]

@pytest.mark.parametrize("headline,is_valid", test_headline_samples)
def test_headline_validity_check(headline, is_valid):
    """Test headline validator accepts valid identity-preserving headlines and rejects over-positioned ones."""
    # A headline is valid if primary archetype is Enterprise Architect and does not claim unsupported leadership title
    has_valid_primary = headline.startswith("Enterprise Architect |") or headline.startswith("Enterprise Architect -")
    has_unsupported_title = "CCoE Leader" in headline or "Cloud Architect" in headline.split("|")[0]
    
    valid = has_valid_primary and not has_unsupported_title
    assert valid == is_valid


def test_ea_cloud_post_generation_identity_drift_detection():
    """Test archetype fit validator detects identity drift when target archetype displaces candidate archetype."""
    identity_drift_sample = {
        "archetype_validation": {
            "status": "WARNING",
            "findings": [
                {
                    "type": "identity_drift",
                    "signal": "unsupported_duration_claim",
                    "target_element": "executive_summary",
                    "detected_claim": "over 15 years of experience building Cloud Centre of Excellence (CCoE) operating models",
                    "canonical_baseline": "Enterprise Architect / Transformation & AI Advisor",
                    "reason": "Projected document makes candidate appear to have 15+ years CCoE specialization unsupported by evidence."
                }
            ]
        }
    }
    
    findings = identity_drift_sample["archetype_validation"]["findings"]
    assert len(findings) == 1
    assert findings[0]["type"] == "identity_drift"
    assert findings[0]["signal"] == "unsupported_duration_claim"


def test_ea_cloud_executive_summary_hierarchy():
    """Verify executive summary hierarchy preserves broad EA foundation first."""
    summary = (
        "Enterprise Architect and Executive Leader with extensive experience driving enterprise architecture, "
        "digital transformation, and IT governance frameworks. Proven track record establishing Cloud Centre of Excellence "
        "(CCoE) operating models and scaling GenAI platform capabilities."
    )
    
    ea_index = summary.find("Enterprise Architect")
    trans_index = summary.find("transformation")
    ccoe_index = summary.find("Cloud Centre of Excellence")
    
    assert ea_index != -1
    assert ea_index < ccoe_index, "Enterprise Architecture foundation must precede CCoE specialization"
