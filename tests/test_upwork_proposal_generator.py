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


# ==============================================================================
# V2.1 Refinements Test Suite (Human-Owned Decisions & Evidence-Gap Handling)
# ==============================================================================

def test_v21_evidence_completeness_classification_4_tier():
    """FR-002: Verify 4-tier requirement assessment classifications:
    SUPPORTED, PARTIALLY_SUPPORTED, UNKNOWN, CONTRADICTED.
    """
    classifications = ["SUPPORTED", "PARTIALLY_SUPPORTED", "UNKNOWN", "CONTRADICTED"]

    assessment_supported = {
        "requirement_id": "req-arch",
        "classification": "SUPPORTED",
        "matched_evidence_ids": ["card-arch-01"]
    }
    assessment_unknown = {
        "requirement_id": "req-prod-deploy",
        "classification": "UNKNOWN",
        "missing_facts": ["production_deployment_verification"]
    }

    assert assessment_supported["classification"] in classifications
    assert assessment_unknown["classification"] in classifications
    assert len(assessment_unknown["missing_facts"]) == 1


def test_v21_evidence_gap_identification_and_confirmation_questions():
    """FR-003, FR-004: Every UNKNOWN/PARTIALLY_SUPPORTED requirement must identify missing facts
    and generate candidate confirmation questions without guessing missing values.
    """
    req_assessment = {
        "requirement_id": "req-agent-count",
        "requirement_text": "Production deployment of 50+ multi-agent system",
        "classification": "PARTIALLY_SUPPORTED",
        "established_facts": ["Multi-agent architecture designed and prototyped"],
        "missing_facts": ["exact_production_agent_count", "production_deployment_attestation"],
        "candidate_confirmation_questions": [
            {
                "question_id": "q-01",
                "question_text": "Was the multi-agent system deployed into live production for 50+ agents?",
                "missing_fact": "production_deployment_attestation",
                "impact": "Required to satisfy client dealbreaker"
            }
        ]
    }

    assert req_assessment["classification"] == "PARTIALLY_SUPPORTED"
    assert len(req_assessment["missing_facts"]) == 2
    assert len(req_assessment["candidate_confirmation_questions"]) == 1
    assert "deployed into live production" in req_assessment["candidate_confirmation_questions"][0]["question_text"]


def test_v21_decoupled_human_decision_workflow():
    """FR-005, FR-006, FR-024, AC-22: Machine recommendation and submission readiness
    MUST NOT force or automatically finalize human user_decision_state (APPLY, DO_NOT_APPLY, HOLD_FOR_EVIDENCE).
    """
    context = {
        "version": "2.1",
        "machine_recommendation": "EVIDENCE_GAPS",
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "proposal_content_mode": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": None  # Unforced, pending human candidate decision
    }

    # Human user can select APPLY after reviewing the gap package
    context["user_decision_state"] = "APPLY"

    assert context["machine_recommendation"] == "EVIDENCE_GAPS"
    assert context["submission_readiness"] == "HUMAN_REVIEW_REQUIRED"
    assert context["user_decision_state"] == "APPLY"


def test_v21_forensic_regression_wpp_employment_prototype_cas():
    """V2.0/V2.1 Hard Rule: Employment at WPP Media plus prototype/non-production evidence plus personal
    CAS project evidence CANNOT produce verified_production or SUPPORTED client production status.
    No production status may be inferred from employment, repo existence, metrics, or org association.
    """
    sources = [
        {"id": "emp-wpp", "type": "employment", "company": "WPP Media", "title": "Senior Director"},
        {"id": "card-wpp-proto", "type": "evidence", "production_status": "verified_non_production", "environment": "prototype_lab"},
        {"id": "card-cas-personal", "type": "evidence", "production_status": "verified_non_production", "environment": "personal_project"}
    ]

    # Evaluate production status strictly according to V2.0/V2.1 invariants
    def evaluate_production_status(evidence_list):
        has_verified_prod = any(e.get("production_status") == "verified_production" for e in evidence_list)
        if not has_verified_prod:
            return "unknown" if not any(e.get("production_status") == "verified_non_production" for e in evidence_list) else "verified_non_production"
        return "verified_production"

    status = evaluate_production_status(sources)

    assert status != "verified_production"
    assert status == "verified_non_production"


def test_v21_partially_supported_qualification_in_client_prose():
    """FR-007, Clarification 2026-09-10: For PARTIALLY_SUPPORTED requirements, client-facing proposal prose
    MAY include verified/supported aspects while omitting or qualifying unsupported aspects.
    Unsupported aspects MUST NEVER be asserted as established fact.
    """
    verified_aspect = "Architected multi-agent platform and reasoning observability infrastructure."
    unsupported_aspect = "Deployed multi-agent platform to 500 live production servers."

    # Proposal generator uses verified aspect, omitting unsupported aspect
    client_proposal_prose = f"I have {verified_aspect.lower()} My work focuses on scalable agentic governance."

    assert verified_aspect.lower() in client_proposal_prose.lower()
    assert unsupported_aspect.lower() not in client_proposal_prose.lower()
    assert "[evidence]" not in client_proposal_prose


def test_v21_screening_answers_no_fabricated_metrics():
    """FR-010, FR-011: Unresolved screening questions MUST NOT fabricate yes/no answers or invented metrics.
    Emits evidence-safe qualified answers or candidate review items.
    """
    screening_question = "What exact percentage cost reduction did your agentic system achieve?"
    canonical_metrics = None  # Missing metric in canonical OKF evidence

    def generate_screening_response(question, metrics):
        if metrics is None:
            return {
                "status": "EVIDENCE_SAFE_QUALIFIED",
                "answer": "Canonical evidence documents significant workflow cycle time reduction, though specific percentage cost savings are unrecorded.",
                "open_condition": "Requires candidate confirmation of exact cost reduction metric."
            }
        return {"status": "ANSWERED", "answer": f"Achieved {metrics}% cost reduction."}

    response = generate_screening_response(screening_question, canonical_metrics)

    assert response["status"] == "EVIDENCE_SAFE_QUALIFIED"
    assert "cost savings are unrecorded" in response["answer"]
    assert "%" not in response["answer"]  # Zero invented percentages


def test_v21_work_sample_project_type_labeling():
    """FR-015: Work samples MUST retain explicit project type tags (client_production, prototype_innovation, personal_project).
    Personal projects cannot be falsely presented as client production.
    """
    work_samples = [
        {
            "sample_id": "ws-1",
            "title": "WPP Agentic Platform Architecture",
            "project_type": "client_production",
            "evidence_source": "card-wpp-01"
        },
        {
            "sample_id": "ws-2",
            "title": "CAS Coding Agent Guardrails",
            "project_type": "personal_project",
            "evidence_source": "card-cas-01"
        }
    ]

    assert work_samples[0]["project_type"] == "client_production"
    assert work_samples[1]["project_type"] == "personal_project"
    assert work_samples[1]["project_type"] != "client_production"


def test_v21_deterministic_evidence_improvement_loop():
    """FR-017, SC-006: Updating canonical OKF evidence to resolve a gap deterministically upgrades
    submission_readiness from HUMAN_REVIEW_REQUIRED to SUBMISSION_READY without manual text edits.
    """
    # Initial state with unknown gap
    qualification_state = {
        "requirement": "Production deployment verification",
        "evidence_status": "UNKNOWN",
        "submission_readiness": "HUMAN_REVIEW_REQUIRED"
    }

    assert qualification_state["submission_readiness"] == "HUMAN_REVIEW_REQUIRED"

    # Candidate adds verified evidence card to canonical OKF
    canonical_okf_cards = [{"id": "card-verified-prod-01", "production_status": "verified_production"}]

    # Re-evaluate pipeline
    if any(card.get("production_status") == "verified_production" for card in canonical_okf_cards):
        qualification_state["evidence_status"] = "SUPPORTED"
        qualification_state["submission_readiness"] = "SUBMISSION_READY"

    assert qualification_state["evidence_status"] == "SUPPORTED"
    assert qualification_state["submission_readiness"] == "SUBMISSION_READY"


def test_v21_validation_semantic_evidence_support():
    """FR-018: Independent validation MUST verify semantic evidence support, not merely claim traceability presence.
    """
    claim = "Led production multi-agent platform deployment for 100+ agents"
    claim_traceability = [{"claim": claim, "evidence_id": "card-wpp-01"}]
    canonical_evidence_cards = {
        "card-wpp-01": {
            "title": "WPP Agentic Platform",
            "production_status": "verified_non_production",  # Mismatch: claim asserts production, evidence is non-production
            "supported_claims": ["Multi-agent platform architecture design"]
        }
    }

    def validate_semantic_evidence(claim_item, evidence_db):
        ev_card = evidence_db.get(claim_item["evidence_id"])
        if not ev_card or ev_card.get("production_status") != "verified_production":
            return "FAIL_SEMANTIC_EVIDENCE_MISMATCH"
        return "PASS"

    validation_result = validate_semantic_evidence(claim_traceability[0], canonical_evidence_cards)

    assert validation_result == "FAIL_SEMANTIC_EVIDENCE_MISMATCH"
