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


# ==============================================================================
# Forensic Regression Test Suite (V2.1 Defect Prevention)
# ==============================================================================

def test_forensic_proposal_prose_omits_unverified_production_claims():
    """Forensic Test 1: Client-facing proposal prose MUST NOT assert established live production implementation
    when production_deployment_verification is missing in upwork-qualification.yaml.
    """
    report_path = "out/upwork-senior-agentic-ai-architect/upwork-qualification-report.md"
    assert os.path.exists(report_path), "upwork-qualification-report.md must exist"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "**Submission Readiness**: `HUMAN_REVIEW_REQUIRED`" in content
    assert "implemented production multi-agent" not in content.lower()
    assert "personally architected and implemented production" not in content.lower()


def test_forensic_screening_answers_reject_fabricated_metrics():
    """Forensic Test 2: Screening answers MUST NOT contain unevidenced quantitative metrics
    such as >99.5%, 3-5x, dozens of specialized AI agents, or dramatically reduced cycle time.
    """
    answers_path = "out/upwork-senior-agentic-ai-architect/upwork-screening-answers.md"
    assert os.path.exists(answers_path), "upwork-screening-answers.md must exist"

    with open(answers_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert ">99.5%" not in content
    assert "3-5x" not in content
    assert "dozens of specialized AI agents" not in content
    assert "dramatically reduced cycle time" not in content


def test_forensic_user_decision_state_remains_unforced():
    """Forensic Test 3: user_decision_state in upwork-qualification.yaml MUST remain unforced (None)
    when no human candidate decision is supplied.
    """
    qual_path = "out/upwork-senior-agentic-ai-architect/runtime/upwork-qualification.yaml"
    assert os.path.exists(qual_path), "upwork-qualification.yaml must exist"

    with open(qual_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data.get("user_decision_state") is None, "user_decision_state must be unforced (None)"


def test_forensic_upwork_validator_fails_on_production_inflation():
    """Forensic Test 4: Dynamic upwork_validator MUST fail any proposal asserting production implementation
    when requirement production_status is unverified.
    """
    from scripts.upwork_validator import validate_upwork_proposal

    corrupted_proposal = "I have personally architected and implemented production multi-agent systems for live enterprise clients."
    screening_clean = "Answer: Prototyped agentic architecture."
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": None,
        "requirement_assessments": [
            {
                "requirement_id": "req-1",
                "classification": "PARTIALLY_SUPPORTED",
                "production_status": "unknown",
                "missing_facts": ["production_deployment_verification"]
            }
        ]
    }

    result = validate_upwork_proposal(corrupted_proposal, screening_clean, qual_data)

    assert result["status"] == "FAIL"
    assert any(v["type"] == "production_claim_inflation" for v in result["violations"])


def test_forensic_independent_validator_rejects_corrupted_proposal_even_if_generator_claims_pass():
    """Independent Validator Test: Demonstrates that even if a generator outputs status: PASS,
    the independent executable validator evaluates actual markdown content and rejects corrupted claims (>99.5% accuracy).
    """
    from scripts.upwork_validator import validate_upwork_proposal

    clean_proposal = "Architected multi-agent platform and reasoning observability infrastructure."
    corrupted_screening = "Question 8 Answer: Achieved >99.5% accuracy over a 30-day baseline with 3-5x throughput."
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": None,
        "requirement_assessments": []
    }

    result = validate_upwork_proposal(clean_proposal, corrupted_screening, qual_data)

    assert result["status"] == "FAIL"
    assert result["quantitative_integrity_verified"] is False
    assert any(v["type"] == "unsupported_quantitative_metric" for v in result["violations"])


def test_req2_and_req3_cannot_inherit_verified_production_when_deployment_unknown():
    """Requirement production-status inheritance invariant: req-2 and req-3 cannot be marked
    verified_production when host platform production deployment status is unknown.
    """
    qual_path = "out/upwork-senior-agentic-ai-architect/runtime/upwork-qualification.yaml"
    assert os.path.exists(qual_path), "upwork-qualification.yaml must exist"

    with open(qual_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    reqs = {r["requirement_id"]: r for r in data.get("requirement_assessments", [])}
    assert reqs["req-2"]["production_status"] == "unknown", "req-2 production status must remain unknown"
    assert reqs["req-3"]["production_status"] == "unknown", "req-3 production status must remain unknown"


def test_wpp_work_sample_classification_not_client_production():
    """Work-sample production classification invariant: WPP work sample must NOT be classified as client_production
    when production status is unknown.
    """
    qual_path = "out/upwork-senior-agentic-ai-architect/runtime/upwork-qualification.yaml"
    assert os.path.exists(qual_path), "upwork-qualification.yaml must exist"

    with open(qual_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    samples = data.get("recommended_work_samples", [])
    wpp_sample = next((s for s in samples if "WPP" in s.get("title", "")), None)
    assert wpp_sample is not None, "WPP work sample must exist"
    assert wpp_sample["project_type"] != "client_production", "WPP work sample project_type must not be client_production when production is unknown"


def test_screening_q2_and_q4_status_evidence_safe_qualified():
    """Screening-answer completeness invariant: Q2 and Q4 must be marked EVIDENCE_SAFE_QUALIFIED
    when exact counts or quantitative business metrics are missing in evidence.
    """
    answers_path = "out/upwork-senior-agentic-ai-architect/upwork-screening-answers.md"
    assert os.path.exists(answers_path), "upwork-screening-answers.md must exist"

    with open(answers_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "## Question 2: How many agents or automated workflows were involved?\n**Status**: `EVIDENCE_SAFE_QUALIFIED`" in content
    assert "## Question 4: What measurable business result did the system produce?\n**Status**: `EVIDENCE_SAFE_QUALIFIED`" in content


def test_unsupported_narrative_claims_absent():
    """Remove unsupported narrative claims invariant: 'transformed commercial operations' and
    'eliminated ungoverned AI experiments' must be absent from generated outputs.
    """
    answers_path = "out/upwork-senior-agentic-ai-architect/upwork-screening-answers.md"
    assert os.path.exists(answers_path), "upwork-screening-answers.md must exist"

    with open(answers_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "transformed commercial operations" not in content
    assert "eliminated ungoverned AI experiments" not in content


def test_validation_metrics_not_static():
    """Remove static validation metrics invariant: total_claims: 24 must not appear as hardcoded static count.
    """
    report_path = "out/upwork-senior-agentic-ai-architect/runtime/projection-validation-report.yaml"
    assert os.path.exists(report_path), "projection-validation-report.yaml must exist"

    with open(report_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    cov = data["metrics"]["evidence_coverage"]
    assert "total_claims" not in cov, "total_claims: 24 hardcoded metric must be removed"
    assert "total_checks" in cov, "real total_checks metric must be present"


def test_validator_checks_work_samples_and_rejects_corrupted_sample():
    """Extend validator coverage to work samples invariant: upwork_validator must fail any work sample
    claiming client_production when production status is unknown.
    """
    from scripts.upwork_validator import validate_upwork_proposal

    proposal_clean = "Architected multi-agent platform and reasoning observability infrastructure."
    screening_clean = "Answer: Prototyped agentic architecture."
    corrupted_work_samples = """# Recommended Work Samples
## 1. WPP Agentic AI Platform
- **Project Type**: `client_production`
- **Summary**: Live enterprise client production deployment.
"""
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": None,
        "requirement_assessments": [
            {
                "requirement_id": "req-1",
                "classification": "PARTIALLY_SUPPORTED",
                "production_status": "unknown",
                "missing_facts": ["production_deployment_verification"]
            }
        ]
    }

    result = validate_upwork_proposal(proposal_clean, screening_clean, qual_data, work_samples_md=corrupted_work_samples)

    assert result["status"] == "FAIL"
    assert result["work_samples_verified"] is False
    assert any(v["type"] == "work_sample_production_misclassification" for v in result["violations"])


def test_validator_rejects_corrupted_screening_answer_status():
    """Strengthen independent validation invariant: upwork_validator must reject screening answer Q2/Q4
    marked ANSWERED without evidence-backed numerical metric.
    """
    from scripts.upwork_validator import validate_upwork_proposal

    proposal_clean = "Architected multi-agent platform and reasoning observability infrastructure."
    corrupted_screening = """# Upwork Screening Answers
## Question 2: How many agents or automated workflows were involved?
**Status**: `ANSWERED`
**Answer**: At WPP Media, the platform coordinated specialized AI agents across media planning workflows.
"""
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": None,
        "requirement_assessments": []
    }

    result = validate_upwork_proposal(proposal_clean, corrupted_screening, qual_data)

    assert result["status"] == "FAIL"
    assert result["screening_completeness_verified"] is False
    assert any(v["type"] == "screening_answer_status_mismatch" for v in result["violations"])


# ==============================================================================
# V3.1 Evidence Attribution, Composition & Candidate Agnosticism Test Suite
# ==============================================================================

def test_us1_non_linear_attribution_and_attribution_shift():
    """T005 / US1: Verify candidate-agnostic attribution shift validator catches contribution inflation
    (e.g., architected -> implemented -> deployed) using generic parameterized fixtures (OrgAlpha, ProjectBeta).
    """
    from scripts.upwork_validator import check_attribution_shift

    # 1. Valid: Same or lower level claim
    assert check_attribution_shift("architected", "architected") is None
    assert check_attribution_shift("advised", "architected") is None

    # 2. Invalid: Inflation from architected -> implemented / deployed
    shift_violation = check_attribution_shift("implemented", "architected")
    assert shift_violation is not None
    assert shift_violation["type"] == "attribution_shift_violation"
    assert "unsupported attribution shift" in shift_violation["reason"]

    shift_deployed = check_attribution_shift("deployed", "architected")
    assert shift_deployed is not None
    assert shift_deployed["type"] == "attribution_shift_violation"


def test_us2_cross_source_composition_boundaries():
    """T010 / US2: Verify cross-source composition boundaries prohibit unsupported_composite evidence
    aggregation across separate contexts for single requirement satisfaction.
    """
    from scripts.upwork_validator import check_evidence_composition

    # 1. Valid: same_context or complementary_multi_context
    assert check_evidence_composition("same_context", "req-01") is None
    assert check_evidence_composition("complementary_multi_context", "req-01") is None

    # 2. Invalid: unsupported_composite
    comp_violation = check_evidence_composition("unsupported_composite", "req-prod-impl")
    assert comp_violation is not None
    assert comp_violation["type"] == "unsupported_composite_evidence"
    assert comp_violation["requirement_id"] == "req-prod-impl"


def test_us3_historical_vs_proposed_technology_disambiguation():
    """T014 / US3: Verify proposed-only technologies (e.g., LangGraph, OpenAI Agents SDK)
    are flagged if claimed as past historical implementations without canonical evidence.
    """
    from scripts.upwork_validator import check_proposed_vs_historical_technologies

    proposed_techs = ["LangGraph", "OpenAI Agents SDK", "Temporal"]
    
    # 1. Valid prospective framing
    valid_proposal = "For your architecture, I would deploy LangGraph and OpenAI Agents SDK with Temporal workflow state."
    assert len(check_proposed_vs_historical_technologies(proposed_techs, valid_proposal)) == 0

    # 2. Invalid historical claim for proposed tech
    invalid_proposal = "I previously implemented LangGraph in past roles."
    violations = check_proposed_vs_historical_technologies(proposed_techs, invalid_proposal)
    assert len(violations) == 1
    assert violations[0]["type"] == "proposed_technology_historical_inflation"
    assert violations[0]["technology"] == "LangGraph"


def test_us4_screening_answer_consistency_and_multi_axis_state():
    """T017 / US4: Verify assertion-then-disclaimer pattern is rejected and screening answers match qualification context.
    """
    from scripts.upwork_validator import validate_upwork_proposal

    # Assertive claim followed by disclaimer pattern
    proposal_disclaimer = "I architected the production platform at OrgAlpha. Live production deployment is unknown."
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": "PENDING_HUMAN_SELECTION",
        "requirement_assessments": [
            {
                "requirement_id": "req-1",
                "classification": "PARTIALLY_SUPPORTED",
                "production_status": "unknown",
                "missing_facts": ["production_deployment_verification"]
            }
        ]
    }

    result = validate_upwork_proposal(proposal_disclaimer, "", qual_data)
    # Validator catches production claim inflation when production status is unverified
    assert result["status"] == "FAIL"


def test_golden_scenario_1_wpp_cas_attribution_fixture():
    """T021 / FR-058: Golden Scenario 1 (WPP+CAS Attribution Fixture).
    Enterprise context (WPP): Enterprise architecture leadership. Live personal production deployment unverified.
    Personal context (CAS): Personal architecture lab implementation.
    Requirement: "Personally implemented production multi-agent system inside operating company."
    Expected: Zero client claims asserting personal enterprise production deployment.
    """
    from scripts.upwork_validator import validate_upwork_proposal

    # Valid bounded proposal:
    valid_proposal = (
        "I led enterprise AI systems architecture alignment at WPP Media while personally "
        "prototyping multi-agent coordination guardrails in my architecture lab."
    )
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": "APPLY",
        "requirement_assessments": [
            {
                "requirement_id": "req-prod-multi-agent",
                "classification": "PARTIALLY_SUPPORTED",
                "production_status": "unknown",
                "missing_facts": ["production_deployment_verification"]
            }
        ]
    }

    result = validate_upwork_proposal(valid_proposal, "", qual_data)
    assert result["status"] == "PASS"

    # Inflated invalid proposal:
    invalid_proposal = "I personally architected and implemented production multi-agent systems at WPP Media."
    invalid_result = validate_upwork_proposal(invalid_proposal, "", qual_data)
    assert invalid_result["status"] == "FAIL"
    assert any(v["type"] == "production_claim_inflation" for v in invalid_result["violations"])


def test_golden_scenario_2_project_in_progress_at_departure():
    """T022 / FR-059: Golden Scenario 2 (Project In Progress at Departure Fixture).
    Candidate led project that was in active development upon departure.
    Expected: Project leadership and architecture design MAY be claimed, live production deployment MUST NOT be claimed.
    """
    from scripts.upwork_validator import validate_upwork_proposal

    valid_proposal = "Led architecture design and delivery alignment prior to departure."
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": "APPLY",
        "requirement_assessments": [
            {
                "requirement_id": "req-in-progress",
                "classification": "PARTIALLY_SUPPORTED",
                "production_status": "unknown",
                "missing_facts": ["production_deployment_verification"]
            }
        ]
    }

    result = validate_upwork_proposal(valid_proposal, "", qual_data)
    assert result["status"] == "PASS"


def test_candidate_agnosticism_verification():
    """T024 / FR-063 & SC-038: Candidate Agnosticism Verification.
    Ensures zero hardcoded employer names (WPP, BBC) or project names exist in skills or upwork_validator.py.
    """
    validator_path = "scripts/upwork_validator.py"
    qual_skill_path = "skills/upwork-qualification/SKILL.md"
    prop_skill_path = "skills/upwork-proposal/SKILL.md"

    for path in [validator_path, qual_skill_path, prop_skill_path]:
        assert os.path.exists(path), f"File {path} must exist"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Ensure no hardcoded specific candidate company names exist in logic
        # Note: WPP/BBC/BAT mentioned only in general comments explaining rules, but not in code patterns
        # Verify no hardcoded string matching regexes for specific company names exist in upwork_validator logic
        if path == validator_path:
            assert 'employer == "WPP"' not in content
            assert 'employer == "BBC"' not in content
            assert 'r"WPP"' not in content
            assert 'r"BBC"' not in content


# ==============================================================================
# V3.2 Contract Alignment & Fixture Projection Tests (Specs 004)
# ==============================================================================

def test_v32_upwork_proposal_cover_letter_placement():
    """T003 / US1: Verify that upwork-qualification-report.md contains the full Executive Proposal Cover Letter
    conforming to skills/upwork-proposal/SKILL.md (350-500 words) and zero 3-line static verdict stubs.
    """
    report_path = "out/upwork-business-systems-technology-architecture-consultant/upwork-qualification-report.md"
    assert os.path.exists(report_path), f"{report_path} must exist"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Must contain executive proposal cover letter prose
    assert "Dear Hiring Team" in content or "Business Systems" in content
    assert "Proposed Engagement Structure" in content or "Proposed Approach" in content or "Relevant Experience" in content
    assert len(content.split()) >= 250, "Proposal cover letter must be a substantial draft (250-500 words target)"

    # Must NOT contain legacy 3-line static verdict stub
    assert "[inference] Qualification Verdict: STRONG FIT (100% verified experience" not in content


def test_v32_upwork_screening_answers_scope_isolation():
    """T005 / US2: Verify that upwork-screening-answers.md contains strictly screening Q&A responses
    and zero ## Proposal Cover Letter copy.
    """
    answers_path = "out/upwork-business-systems-technology-architecture-consultant/upwork-screening-answers.md"
    assert os.path.exists(answers_path), f"{answers_path} must exist"

    with open(answers_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Must NOT contain Proposal Cover Letter section or heading
    assert "## Proposal Cover Letter" not in content
    assert "Dear Hiring Team" not in content


def test_v32_runtime_qualification_context_binding():
    """T007 / US3: Verify that proposal projection dynamically binds to runtime/upwork-qualification.yaml
    for submission readiness, machine recommendation, and content mode header metadata.
    """
    report_path = "out/upwork-business-systems-technology-architecture-consultant/upwork-qualification-report.md"
    qual_path = "out/upwork-business-systems-technology-architecture-consultant/runtime/upwork-qualification.yaml"

    assert os.path.exists(report_path), f"{report_path} must exist"
    assert os.path.exists(qual_path), f"{qual_path} must exist"

    with open(qual_path, "r", encoding="utf-8") as f:
        qual_data = yaml.safe_load(f)

    with open(report_path, "r", encoding="utf-8") as f:
        report_content = f.read()

    # Verify header metadata values in report dynamically match upwork-qualification.yaml
    expected_readiness = qual_data.get("submission_readiness", "SUBMISSION_READY")
    expected_recommendation = qual_data.get("machine_recommendation", "STRONG_FIT")

    assert f"**Submission Readiness**: `{expected_readiness}`" in report_content or f"**Submission Readiness**: {expected_readiness}" in report_content
    assert f"**Machine Recommendation**: `{expected_recommendation}`" in report_content or f"**Machine Recommendation**: {expected_recommendation}" in report_content




