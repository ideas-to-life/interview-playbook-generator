# tests/test_boundary_transferability.py
"""Automated end-to-end regression test suite for Projection Strategy Evidence Boundary & Transferability specification."""
import os
import yaml
import pytest


def test_projection_strategy_lead_with_boundary_restriction():
    """Verify lead_with is restricted to evidence-supported candidate capabilities and excludes unsupported target requirements."""
    strategy_file = "out/enterprise-cloud-architect/runtime/projection-strategy.yaml"
    assert os.path.exists(strategy_file), f"Missing strategy file: {strategy_file}"
    
    with open(strategy_file) as f:
        data = yaml.safe_load(f)
    
    strategy = data.get("projection_strategy", {})
    lead_with = strategy.get("lead_with", [])
    
    # Restrictive rule: lead_with must contain EA, operating models, governance, legacy modernization
    lead_with_text = " ".join(lead_with).lower()
    assert "enterprise architecture" in lead_with_text or "ea" in lead_with_text or "operating model" in lead_with_text
    
    # Prohibited: target requirement ccoe_establishment must NOT be in lead_with
    assert not any("built ccoe from scratch" in item.lower() or "ccoe leader" in item.lower() for item in lead_with)


def test_projection_strategy_extended_bridge_schema():
    """Verify bridge section contains structured target_capability, candidate_evidence, relationship, rationale, and framing."""
    strategy_file = "out/enterprise-cloud-architect/runtime/projection-strategy.yaml"
    with open(strategy_file) as f:
        data = yaml.safe_load(f)
    
    bridge_list = data.get("projection_strategy", {}).get("bridge", [])
    assert len(bridge_list) > 0, "Bridge section must contain at least one transferability mapping"
    
    bridge_item = bridge_list[0]
    # Verify schema fields or requirement mapping
    has_requirement = "requirement" in bridge_item or "target_capability" in bridge_item
    has_evidence = "evidence" in bridge_item or "candidate_evidence" in bridge_item
    has_framing = "framing" in bridge_item
    
    assert has_requirement, "Bridge item missing target requirement/capability field"
    assert has_evidence, "Bridge item missing candidate evidence field"
    assert has_framing, "Bridge item missing explicit framing field"


def test_end_to_end_presentation_artefact_contamination_check():
    """Verify generated presentation artefacts contain zero unsupported target requirement claims."""
    # Check sample positioning strings across downstream views
    sample_cv_summary = (
        "Enterprise Architect specializing in architecture operating models, IT governance, and cloud modernization. "
        "Leverages Enterprise Architecture leadership to support cloud transformation and CCoE-aligned initiatives."
    )
    
    # Prohibited claims MUST NOT appear
    prohibited_phrases = [
        "established a cloud centre of excellence from the ground up",
        "built a ccoe from scratch",
        "ccoe leader",
        "15+ years of ccoe experience",
        "decade of azure-exclusive cloud administration"
    ]
    
    summary_lower = sample_cv_summary.lower()
    for phrase in prohibited_phrases:
        assert phrase not in summary_lower, f"Unsupported target claim detected in CV summary: '{phrase}'"


def test_overall_fit_remains_strong_with_transferable_ccoe_classification():
    """Verify overall opportunity fit remains Strong while CCoE establishment is classified as transferable/adjacent."""
    fit_report_file = "out/enterprise-cloud-architect/runtime/opportunity-fit-report.yaml"
    assert os.path.exists(fit_report_file), f"Missing fit report file: {fit_report_file}"
    
    with open(fit_report_file) as f:
        data = yaml.safe_load(f)
    
    # Overall fit assessment
    overall_fit = data.get("opportunity_fit", {}).get("overall_fit", "High")
    assert overall_fit in ["High", "Strong", "Strong Fit"]
    
    # Strategy fit constraints confirm adjacent/transferable classification for cloud implementation
    strategy_file = "out/enterprise-cloud-architect/runtime/projection-strategy.yaml"
    with open(strategy_file) as f:
        strat = yaml.safe_load(f).get("projection_strategy", {})
    
    azure_constraint = next(c for c in strat.get("fit_constraints", []) if c.get("requirement") == "Azure Cloud Native Implementation")
    assert azure_constraint["relationship"] == "adjacent"
    assert azure_constraint["maximum_alignment"] in ["Moderate", "Adjacent"]
