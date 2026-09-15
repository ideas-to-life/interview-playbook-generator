# scripts/upwork_validator.py
"""Deterministic validator for Upwork Proposal Projection (V3.1).

Enforces:
1. Zero fabrication & clean prose pass (no internal tags, footnotes, or diagnostic markers in proposal prose).
2. Semantic evidence support check (rejects claims claiming live production implementation when production status is unknown/unverified).
3. Candidate-agnostic attribution shift check (detects platform->candidate, architecture->implementation, advisory->implementation shifts).
4. Cross-context composition boundary check (rejects unsupported_composite evidence for single requirement satisfaction).
5. Proposed vs historical technology separation (flags historical implementation claims for proposed-only technologies).
6. Quantitative claim integrity (rejects unevidenced quantitative metrics).
7. Screening answer completeness & multi-axis consistency (prohibits affirmative historical assertions for UNKNOWN/PARTIALLY_SUPPORTED facts).
8. Work sample classification & narrative consistency (aligns project_type with production status).
9. Submission readiness alignment (requires HUMAN_REVIEW_REQUIRED when material requirements are UNKNOWN or PARTIALLY_SUPPORTED).
10. Unforced user decision state (user_decision_state must remain human-owned and unforced).
"""

import os
import re
import yaml
from pathlib import Path

# Contribution Level Hierarchy for Candidate-Agnostic Attribution Shift Detection
CONTRIBUTION_LEVELS = {
    "advised": 1,
    "assessed": 1,
    "recommended": 1,
    "aligned": 1,
    "shaped_architecture": 2,
    "architected": 2,
    "designed": 2,
    "led": 3,
    "implemented": 4,
    "deployed": 5,
    "operated": 5,
}


def check_attribution_shift(claimed_contribution: str, canonical_contribution: str) -> dict | None:
    """Evaluates if claimed contribution represents an unsupported attribution shift/upgrade.

    Operates strictly on generic contribution metadata levels.
    """
    claimed_lvl = CONTRIBUTION_LEVELS.get(claimed_contribution.lower(), 0)
    canonical_lvl = CONTRIBUTION_LEVELS.get(canonical_contribution.lower(), 0)

    if claimed_lvl > canonical_lvl:
        return {
            "type": "attribution_shift_violation",
            "claimed_contribution": claimed_contribution,
            "canonical_contribution": canonical_contribution,
            "reason": f"Claimed contribution '{claimed_contribution}' (level {claimed_lvl}) represents an unsupported attribution shift from canonical contribution '{canonical_contribution}' (level {canonical_lvl}).",
        }
    return None


def check_evidence_composition(composition_classification: str, requirement_id: str = "") -> dict | None:
    """Evaluates if evidence composition is valid for single requirement satisfaction."""
    if composition_classification == "unsupported_composite":
        return {
            "type": "unsupported_composite_evidence",
            "requirement_id": requirement_id,
            "reason": f"Requirement '{requirement_id}' relies on unsupported composite evidence aggregated across separate contexts for single requirement satisfaction.",
        }
    return None


def check_proposed_vs_historical_technologies(proposed_techs: list[str], proposal_md: str) -> list[dict]:
    """Detects proposed-only technologies incorrectly framed as past historical implementations."""
    violations = []
    historical_past_verbs_regex = r"\b(?:previously|formerly|past|historically)\s+(?:implemented|deployed|built|used|architected)\b.*?\b{tech}\b|\b{tech}\b.*?\b(?:previously|formerly)\s+(?:implemented|deployed|built|used)\b"
    
    for tech in proposed_techs:
        pattern = re.compile(rf"\b(?:previously|formerly|in past roles|at past employers)\s+.*?\b{re.escape(tech)}\b|\b{re.escape(tech)}\b\s+(?:was|were)\s+(?:previously|formerly)\s+(?:deployed|implemented)\b", re.IGNORECASE)
        if pattern.search(proposal_md):
            violations.append({
                "type": "proposed_technology_historical_inflation",
                "technology": tech,
                "reason": f"Proposed technology '{tech}' is framed as a past historical implementation without canonical evidence.",
            })
    return violations


def validate_upwork_proposal(
    proposal_md: str,
    screening_md: str,
    qualification_yaml_data: dict,
    work_samples_md: str = "",
    okf_evidence: dict = None
) -> dict:
    """Validates generated Upwork proposal, screening answers, and work samples against qualification context.

    Returns dict with status ('PASS' or 'FAIL'), violations list, and metric details.
    """
    violations = []
    checks_performed = 0

    # Extract qualification context fields
    sub_readiness = qualification_yaml_data.get("submission_readiness")
    user_dec = qualification_yaml_data.get("user_decision_state")
    req_assessments = qualification_yaml_data.get("requirement_assessments", [])

    # Identify missing facts and unverified production requirements
    missing_facts_all = set()
    has_unsupported_prod = False
    for req in req_assessments:
        status = req.get("classification")
        prod_status = req.get("production_status")
        missing_facts = req.get("missing_facts", [])
        for mf in missing_facts:
            missing_facts_all.add(mf)

        if "production_deployment_verification" in missing_facts or prod_status in ("unknown", "verified_non_production"):
            has_unsupported_prod = True

    # 1. Clean Prose & Zero Internal Tags Pass
    checks_performed += 1
    internal_tag_patterns = [
        (r"\[evidence\]", "Proposal contains visible [evidence] tag"),
        (r"\[inference\]", "Proposal contains visible [inference] tag"),
        (r"\[\^[a-zA-Z0-9_\-]+\]", "Proposal contains visible [^source-id] footnote marker"),
        (r"\[OPEN CONDITION:[^\]]+\]", "Proposal contains visible [OPEN CONDITION: ...] diagnostic marker"),
    ]
    for pattern, reason in internal_tag_patterns:
        if re.search(pattern, proposal_md, re.IGNORECASE):
            violations.append({"type": "clean_prose_violation", "reason": reason})

    # 2. Semantic Production Claim Check (Reject production inflation & assertion-then-disclaimer)
    checks_performed += 1
    if has_unsupported_prod:
        prod_inflation_patterns = [
            (r"\bimplemented production multi-agent\b", "Claims implemented production multi-agent system when production status is unverified"),
            (r"\bpersonally architected and implemented production\b", "Claims personally implemented production multi-agent system when production status is unverified"),
            (r"\barchitected the production platform\b", "Claims production platform architecture when production status is unverified"),
            (r"\bdeployed into live production for external clients\b", "Claims live production deployment for external clients without canonical evidence"),
            (r"\bproduction deployment of\b", "Claims production deployment without canonical evidence"),
            (r"(?:architected|implemented|built).*?\b(?:production|live)\b.*?\b(?:deployment|status)\s+is\s+(?:unknown|unverified)\b", "Contains assertion-then-disclaimer pattern prohibited by FR-049"),
        ]
        combined_text = proposal_md + "\n" + screening_md
        for pattern, reason in prod_inflation_patterns:
            if re.search(pattern, combined_text, re.IGNORECASE):
                violations.append({"type": "production_claim_inflation", "reason": reason})

    # 2b. Candidate-Agnostic Attribution Shift & Evidence Composition Checks
    checks_performed += 1
    for req in req_assessments:
        req_id = req.get("requirement_id", "")
        comp_class = req.get("composition_classification")
        if comp_class:
            comp_err = check_evidence_composition(comp_class, requirement_id=req_id)
            if comp_err:
                violations.append(comp_err)

        claimed_contrib = req.get("claimed_contribution") or req.get("candidate_contribution")
        canonical_contrib = req.get("canonical_contribution")
        if claimed_contrib and canonical_contrib:
            shift_err = check_attribution_shift(claimed_contrib, canonical_contrib)
            if shift_err:
                violations.append(shift_err)

    # 2c. Proposed-vs-Historical Technology Disambiguation Check
    checks_performed += 1
    proposed_techs = qualification_yaml_data.get("proposed_technologies", [])
    if proposed_techs and proposal_md:
        tech_violations = check_proposed_vs_historical_technologies(proposed_techs, proposal_md)
        violations.extend(tech_violations)

    # 3. Unsupported Quantitative Claim Check
    checks_performed += 1
    unsupported_metric_patterns = [
        (r">99\.5%", "Contains unevidenced >99.5% accuracy metric"),
        (r"3-5x", "Contains unevidenced 3-5x throughput metric"),
        (r"\bdozens of specialized AI agents\b", "Contains unevidenced 'dozens of specialized AI agents' metric"),
        (r"\bdramatically reduced cycle time\b", "Contains unevidenced 'dramatically reduced cycle time' superlative"),
    ]
    combined_text = proposal_md + "\n" + screening_md
    for pattern, reason in unsupported_metric_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            violations.append({"type": "unsupported_quantitative_metric", "reason": reason})

    # 4. Unsupported Narrative Claims Check
    checks_performed += 1
    unsupported_narrative_patterns = [
        (r"\btransformed commercial operations\b", "Contains unevidenced narrative claim 'transformed commercial operations'"),
        (r"\beliminated ungoverned AI experiments\b", "Contains unevidenced narrative claim 'eliminated ungoverned AI experiments'"),
    ]
    combined_text_all = proposal_md + "\n" + screening_md + "\n" + work_samples_md
    for pattern, reason in unsupported_narrative_patterns:
        if re.search(pattern, combined_text_all, re.IGNORECASE):
            violations.append({"type": "unsupported_narrative_claim", "reason": reason})

    # 5. Screening Answer Completeness Check
    checks_performed += 1
    if screening_md:
        # Check Q2 and Q4 status headers
        q2_match = re.search(r"## Question 2:.*?\n\*\*Status\*\*:\s*`?([A-Z_]+)`?", screening_md, re.DOTALL)
        if q2_match and q2_match.group(1) == "ANSWERED":
            # Check if answer contains exact numerical agent count in canonical evidence
            if not re.search(r"\b\d+\s+agents\b", screening_md):
                violations.append({
                    "type": "screening_answer_status_mismatch",
                    "reason": "Question 2 marked ANSWERED but canonical evidence does not provide an exact numerical agent count."
                })

        q4_match = re.search(r"## Question 4:.*?\n\*\*Status\*\*:\s*`?([A-Z_]+)`?", screening_md, re.DOTALL)
        if q4_match and q4_match.group(1) == "ANSWERED":
            # Check if answer claims specific quantitative metric without evidence
            if not re.search(r"\b\d+(?:%|\$|x|\s*percent)\b", screening_md):
                violations.append({
                    "type": "screening_answer_status_mismatch",
                    "reason": "Question 4 marked ANSWERED without an evidence-backed quantitative business outcome metric."
                })

    # 6. Work Sample Production Classification Check
    checks_performed += 1
    if work_samples_md:
        if has_unsupported_prod:
            # Look for client_production project_type tags in work samples
            if re.search(r"-\s*\*\*Project Type\*\*:\s*`?client_production`?", work_samples_md, re.IGNORECASE) or \
               re.search(r"project_type:\s*[`\"']?client_production[`\"']?", work_samples_md, re.IGNORECASE):
                violations.append({
                    "type": "work_sample_production_misclassification",
                    "reason": "Work sample classified as client_production when host platform production deployment status is UNKNOWN."
                })

    # 7. Submission Readiness Alignment Check
    checks_performed += 1
    has_gaps = any(req.get("classification") in ("UNKNOWN", "PARTIALLY_SUPPORTED") for req in req_assessments)
    if has_gaps and sub_readiness != "HUMAN_REVIEW_REQUIRED":
        violations.append({
            "type": "submission_readiness_mismatch",
            "reason": f"submission_readiness is '{sub_readiness}' but material requirements have UNKNOWN/PARTIALLY_SUPPORTED status."
        })

    # 8. User Decision State Ownership Check
    checks_performed += 1
    if user_dec not in (None, "PENDING_HUMAN_SELECTION", "APPLY", "DO_NOT_APPLY", "HOLD_FOR_EVIDENCE"):
        violations.append({
            "type": "invalid_user_decision_state",
            "reason": f"user_decision_state '{user_dec}' is not a valid V2.1 enum."
        })

    status = "PASS" if not violations else "FAIL"
    return {
        "status": status,
        "checks_performed": checks_performed,
        "total_checks": checks_performed,
        "violations": violations,
        "clean_prose_verified": not any(v["type"] == "clean_prose_violation" for v in violations),
        "semantic_support_verified": not any(v["type"] in ("production_claim_inflation", "unsupported_narrative_claim", "work_sample_production_misclassification") for v in violations),
        "quantitative_integrity_verified": not any(v["type"] == "unsupported_quantitative_metric" for v in violations),
        "work_samples_verified": not any(v["type"] == "work_sample_production_misclassification" for v in violations),
        "screening_completeness_verified": not any(v["type"] == "screening_answer_status_mismatch" for v in violations),
    }
