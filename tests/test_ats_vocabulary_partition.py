"""Unit tests for ATS vocabulary partitioning logic (User Story 2).

Verifies that target opportunity keywords are correctly partitioned into:
1. candidate_evidenced_vocabulary (grounded in career-record.yaml or OKF)
2. required_job_vocabulary (unsupported client tools / enterprise platforms)
"""

from pathlib import Path
import pytest

from scripts.canonical_models import (
    ATSVocabularyPartition,
    ATSEvidencedTerm,
    ATSRequiredJobTerm,
)
from scripts.canonical_loader import load_canonical_career_record
from scripts.canonical_selector import (
    partition_ats_vocabulary,
    classify_term_evidence,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_classify_term_evidence_tier1_career_record():
    """Canonical terms from career record are resolved to Tier 1."""
    record = load_canonical_career_record()
    
    # "Enterprise Architecture" is in identity.professional_domains
    res = classify_term_evidence("Enterprise Architecture", canonical_record=record)
    assert res is not None
    assert res.evidence_source == "career_record"
    assert "career-record.yaml" in res.evidence_ref

    # "LeanIX" is mentioned in BBC Studios operational scope
    res_leanix = classify_term_evidence("LeanIX", canonical_record=record)
    assert res_leanix is not None
    assert res_leanix.evidence_source == "career_record"

    # "TOGAF" is in certifications
    res_togaf = classify_term_evidence("TOGAF", canonical_record=record)
    assert res_togaf is not None
    assert res_togaf.evidence_source == "career_record"


def test_classify_term_evidence_unsupported_platforms():
    """Platforms absent from career record and OKF return None (unevidenced)."""
    record = load_canonical_career_record()

    for unevidenced_tool in ["Workday", "NetSuite", "Coupa", "Concur"]:
        res = classify_term_evidence(unevidenced_tool, canonical_record=record)
        assert res is None, f"{unevidenced_tool} should be unevidenced in candidate canonical record"


def test_partition_ats_vocabulary_complete():
    """Partitioning a mixed set of target terms correctly separates evidenced vs unevidenced."""
    record = load_canonical_career_record()

    target_terms = [
        "Enterprise Architecture",
        "Workday",
        "LeanIX",
        "Coupa",
        "TOGAF",
        "NetSuite",
    ]

    partition = partition_ats_vocabulary(target_terms, canonical_record=record)

    assert isinstance(partition, ATSVocabularyPartition)
    
    evidenced_terms = [t.term for t in partition.candidate_evidenced_vocabulary]
    required_terms = [t.term for t in partition.required_job_vocabulary]

    assert "Enterprise Architecture" in evidenced_terms
    assert "LeanIX" in evidenced_terms
    assert "TOGAF" in evidenced_terms

    assert "Workday" in required_terms
    assert "Coupa" in required_terms
    assert "NetSuite" in required_terms

    # Check scoring rules conform to contract
    rules = partition.scoring_rules
    assert rules["evidenced_credit_multiplier"] == 1.0
    assert rules["unevidenced_credit_multiplier"] == 0.0
    assert rules["unevidenced_direct_claim_penalty"] == "integrity_defect_failure"

    # Check framing recommendation for required terms
    for req in partition.required_job_vocabulary:
        assert req.status == "unmatched_requirement_gap"
        assert req.recommended_framing in ["explicit_gap", "transferable_capability", "adjacent_experience"]
