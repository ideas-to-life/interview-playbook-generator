"""Contract test for ATS vocabulary partition schema conforming to
specs/006-projection-data-integrity/contracts/ats-vocabulary-partition-contract.yaml.
"""

from pathlib import Path
import pytest
import yaml

from scripts.canonical_models import (
    ATSVocabularyPartition,
    ATSEvidencedTerm,
    ATSRequiredJobTerm,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = REPO_ROOT / "specs/006-projection-data-integrity/contracts/ats-vocabulary-partition-contract.yaml"


def test_ats_contract_file_exists():
    assert CONTRACT_PATH.exists(), f"Contract file not found at {CONTRACT_PATH}"


def test_ats_vocabulary_partition_schema_contract():
    partition = ATSVocabularyPartition(
        candidate_evidenced_vocabulary=[
            ATSEvidencedTerm(
                term="Enterprise Architecture",
                evidence_source="career_record",
                evidence_ref="career-record.yaml#emp-wpp-2025",
            ),
            ATSEvidencedTerm(
                term="SAP",
                evidence_source="okf_capability",
                evidence_ref="cap-enterprise-integration",
            ),
        ],
        required_job_vocabulary=[
            ATSRequiredJobTerm(
                term="Workday",
                status="unmatched_requirement_gap",
                recommended_framing="transferable_capability",
            ),
            ATSRequiredJobTerm(
                term="Coupa",
                status="unmatched_requirement_gap",
                recommended_framing="adjacent_experience",
            ),
        ],
        scoring_rules={
            "evidenced_credit_multiplier": 1.0,
            "unevidenced_credit_multiplier": 0.0,
            "unevidenced_direct_claim_penalty": "integrity_defect_failure",
        },
    )

    data = partition.to_dict()

    # Top level fields
    assert "candidate_evidenced_vocabulary" in data
    assert "required_job_vocabulary" in data
    assert "scoring_rules" in data

    # Evidenced vocabulary
    evidenced = data["candidate_evidenced_vocabulary"]
    assert len(evidenced) == 2
    for item in evidenced:
        assert "term" in item
        assert item["evidence_source"] in ["career_record", "okf_capability", "okf_evidence_card"]
        assert "evidence_ref" in item

    # Required job vocabulary
    required = data["required_job_vocabulary"]
    assert len(required) == 2
    for item in required:
        assert "term" in item
        assert item["status"] == "unmatched_requirement_gap"
        assert item["recommended_framing"] in ["explicit_gap", "transferable_capability", "adjacent_experience"]

    # Scoring rules
    rules = data["scoring_rules"]
    assert rules["evidenced_credit_multiplier"] >= 1.0
    assert rules["unevidenced_credit_multiplier"] <= 0.0
    assert rules["unevidenced_direct_claim_penalty"] == "integrity_defect_failure"
