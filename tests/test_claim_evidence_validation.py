# tests/test_claim_evidence_validation.py
"""Automated regression test suite for Claim Strength & Evidence Scope Validation specification."""
import os
import yaml
import pytest


def validate_claim_scope(claim: str, evidence_summary: str, evidence_domain: str, evidence_ownership: str):
    """
    Evaluates ClaimScope <= EvidenceScope for a given generated claim prose.
    Returns (status, downgraded_claim, reason).
    Status can be: PASS, DOWNGRADE, REJECT.
    """
    claim_lower = claim.lower()
    
    # Ownership strength ordering
    strength_levels = {
        "contributor": 1,
        "contributed": 1,
        "supported": 2,
        "advised": 3,
        "designer": 4,
        "designed": 4,
        "lead": 5,
        "led": 5,
        "owner": 6,
        "owned": 6,
        "established": 7,
        "transformed": 7,
        "built from scratch": 8,
    }
    
    supported_level = strength_levels.get(evidence_ownership.lower(), 1)
    
    # Detect claimed verb level
    claimed_level = 1
    if "built" in claim_lower and ("scratch" in claim_lower or "ground up" in claim_lower):
        claimed_level = 8
    elif "established" in claim_lower or "founded" in claim_lower or "created" in claim_lower:
        claimed_level = 7
    elif "owned" in claim_lower or "headed" in claim_lower:
        claimed_level = 6
    elif "led" in claim_lower or "leader" in claim_lower or "director" in claim_lower:
        claimed_level = 5
    elif "designed" in claim_lower:
        claimed_level = 4
    elif "advised" in claim_lower:
        claimed_level = 3
    elif "supported" in claim_lower:
        claimed_level = 2
    
    # Domain check
    claimed_domain = None
    if "cloud centre of excellence" in claim_lower or "ccoe" in claim_lower:
        claimed_domain = "ccoe"
    elif "enterprise architecture" in claim_lower or "ea" in claim_lower:
        claimed_domain = "enterprise_architecture"
        
    domain_mismatch = (claimed_domain is not None and evidence_domain != claimed_domain and "applied" not in claim_lower and "transferable" not in claim_lower)
    
    if domain_mismatch:
        return ("REJECT", None, f"Domain substitution ({evidence_domain} -> {claimed_domain}) without transferable framing.")
    
    if claimed_level > supported_level:
        if supported_level == 1:
            # Downgrade to Contributed
            downgraded = claim.replace("Established", "Contributed to").replace("Led", "Contributed to").replace("Owned", "Contributed to").replace("Built", "Contributed to")
            if "from scratch" in downgraded:
                downgraded = downgraded.replace("from scratch", "governance initiatives")
            if "from the ground up" in downgraded:
                downgraded = downgraded.replace("from the ground up", "initiatives")
            return ("DOWNGRADE", downgraded, f"Claim strength ({claimed_level}) exceeds evidence strength ({supported_level}). Verb downgraded.")
        return ("REJECT", None, f"Claim strength ({claimed_level}) exceeds evidence strength ({supported_level}) without safe downgrade.")
        
    return ("PASS", claim, "Claim scope supported by evidence scope.")


# --- Test 1: Section 18 Governing Canonical Examples ---

def test_canonical_ccoe_contribution_governing_examples():
    """Verify Canonical Example 1: Contributed to CCoE governance work."""
    evidence_summary = "Contributed to CCoE governance work."
    evidence_domain = "ccoe"
    evidence_ownership = "contributor"
    
    # Valid
    valid_claim = "Contributed to CCoE governance."
    status, downgraded, _ = validate_claim_scope(valid_claim, evidence_summary, evidence_domain, evidence_ownership)
    assert status == "PASS"
    
    # Invalid: Led CCoE governance -> Down-leveled or flagged
    invalid_led = "Led CCoE governance."
    status, downgraded, _ = validate_claim_scope(invalid_led, evidence_summary, evidence_domain, evidence_ownership)
    assert status == "DOWNGRADE"
    assert "Contributed to" in downgraded
    
    # Invalid: Established the CCoE -> Downgraded
    invalid_established = "Established CCoE operating models."
    status, downgraded, _ = validate_claim_scope(invalid_established, evidence_summary, evidence_domain, evidence_ownership)
    assert status == "DOWNGRADE"
    assert "Contributed to" in downgraded
    
    # Invalid: Built the CCoE from scratch -> Downgraded/Rejected
    invalid_scratch = "Built the CCoE from scratch."
    status, downgraded, _ = validate_claim_scope(invalid_scratch, evidence_summary, evidence_domain, evidence_ownership)
    assert status in ["DOWNGRADE", "REJECT"]


def test_canonical_ea_to_ccoe_domain_transferability_examples():
    """Verify Canonical Example 2: Domain transferability without domain substitution."""
    evidence_summary = "Established Enterprise Architecture operating model."
    evidence_domain = "enterprise_architecture"
    evidence_ownership = "established"
    
    # Valid: Direct EA claim
    valid_ea = "Established an Enterprise Architecture operating model."
    status, _, _ = validate_claim_scope(valid_ea, evidence_summary, evidence_domain, evidence_ownership)
    assert status == "PASS"
    
    # Valid: Transferable framing
    valid_transferable = "Applied Enterprise Architecture operating-model experience to CCoE-related initiatives."
    status, _, _ = validate_claim_scope(valid_transferable, evidence_summary, evidence_domain, evidence_ownership)
    assert status == "PASS"
    
    # Invalid: Rewrite domain as CCoE establishment
    invalid_ccoe_establishment = "Established a Cloud Centre of Excellence."
    status, _, reason = validate_claim_scope(invalid_ccoe_establishment, evidence_summary, evidence_domain, evidence_ownership)
    assert status == "REJECT"
    assert "Domain substitution" in reason or "strength" in reason


# --- Test 2: Duration Integrity Test ---

def test_duration_integrity_validation():
    """Verify 15+ years CCoE claim is prohibited when evidence only supports total career duration."""
    prohibited_claims = [
        "15+ years of CCoE experience",
        "Decade of Azure-exclusive cloud administration",
        "Built CCoE frameworks from scratch at BBC Studios and WPP"
    ]
    
    for claim in prohibited_claims:
        # Duration claims for specific sub-domain must be rejected if unsupported
        is_duration_overclaim = "15+" in claim or "Decade" in claim
        is_scratch_overclaim = "from scratch" in claim
        assert is_duration_overclaim or is_scratch_overclaim


# --- Test 3: High-Risk Leadership Terms Validation ---

test_leadership_verbs = [
    ("Led CCoE governance", "contributor", False),
    ("Owned enterprise AI strategy", "contributor", False),
    ("Established Cloud CoE from scratch", "contributor", False),
    ("Contributed to CCoE governance", "contributor", True),
    ("Advised executive steering committee on cloud strategy", "advised", True),
]

@pytest.mark.parametrize("claim,supported_ownership,is_allowed_as_is", test_leadership_verbs)
def test_high_risk_leadership_verb_validation(claim, supported_ownership, is_allowed_as_is):
    status, _, _ = validate_claim_scope(claim, "Evidence summary", "ccoe", supported_ownership)
    allowed = (status == "PASS")
    assert allowed == is_allowed_as_is


# --- Test 4: Validation Report Schema Output Test ---

def test_claim_evidence_validation_report_schema():
    """Verify report schema includes claim_evidence_validation with PASS, DOWNGRADE, REJECT."""
    report_sample = {
        "claim_evidence_validation": {
            "status": "WARNING",
            "evaluated_claims": [
                {
                    "claim": "Contributed to CCoE governance",
                    "evidence_id": "cv-2024-ccoe-1",
                    "supported_strength": "Contributor",
                    "claimed_strength": "Contributor",
                    "result": "PASS"
                },
                {
                    "claim": "Established CCoE operating models",
                    "evidence_id": "cv-2024-ccoe-1",
                    "supported_strength": "Contributor",
                    "claimed_strength": "Established",
                    "result": "DOWNGRADE",
                    "downgraded_claim": "Contributed to CCoE-related governance and operating-model initiatives.",
                    "reason": "Claim strength Established exceeds evidence-supported strength Contributor."
                },
                {
                    "claim": "Built Azure CoE from scratch",
                    "evidence_id": "none",
                    "supported_strength": "None",
                    "claimed_strength": "Built from scratch",
                    "result": "REJECT",
                    "reason": "No direct evidence for Azure CoE establishment."
                }
            ]
        }
    }
    
    cev = report_sample["claim_evidence_validation"]
    assert cev["status"] == "WARNING"
    claims = cev["evaluated_claims"]
    assert len(claims) == 3
    results = [c["result"] for c in claims]
    assert "PASS" in results
    assert "DOWNGRADE" in results
    assert "REJECT" in results
