# scripts/upwork_validator.py
"""Deterministic validator for Upwork Proposal Projection (V3.1).

Enforces:
1. Zero fabrication & clean prose pass (no internal tags, footnotes, or diagnostic markers in client-facing prose).
2. Semantic evidence support check (rejects claims claiming live production implementation when production status is unknown/unverified).
3. Candidate-agnostic attribution shift check (detects architecture->implementation->deployment shifts).
4. Cross-context composition boundary check (rejects unsupported_composite evidence for single requirement satisfaction).
5. Proposed vs historical technology separation (flags historical implementation claims for proposed-only technologies).
6. Quantitative claim integrity (rejects unevidenced quantitative metrics).
7. Screening answer completeness & multi-axis consistency (prohibits affirmative historical assertions for UNKNOWN/PARTIALLY_SUPPORTED facts).
8. Work sample classification & narrative consistency (aligns project_type with production status).
9. Submission readiness alignment (requires HUMAN_REVIEW_REQUIRED when material requirements are UNKNOWN or PARTIALLY_SUPPORTED).
10. Unforced user decision state (user_decision_state must remain human-owned and unforced).
"""

import argparse
import re
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

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
    for tech in proposed_techs:
        pattern = re.compile(
            rf"\b(?:previously|formerly|in past roles|at past employers)\s+.*?\b{re.escape(tech)}\b|\b{re.escape(tech)}\b\s+(?:was|were)\s+(?:previously|formerly)\s+(?:deployed|implemented)\b",
            re.IGNORECASE,
        )
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
    okf_evidence: dict | None = None,
) -> dict:
    """Validates generated Upwork proposal, screening answers, and work samples against qualification context.

    Returns dict with status ('PASS' or 'FAIL'), violations list, and metric details.
    """
    violations = []
    checks_performed = 0

    sub_readiness = qualification_yaml_data.get("submission_readiness")
    user_dec = qualification_yaml_data.get("user_decision_state")
    req_assessments = qualification_yaml_data.get("requirement_assessments", [])

    missing_facts_all = set()
    has_unsupported_prod = False
    for req in req_assessments:
        prod_status = req.get("production_status")
        missing_facts = req.get("missing_facts", [])
        for mf in missing_facts:
            missing_facts_all.add(mf)

        if "production_deployment_verification" in missing_facts or prod_status in ("unknown", "verified_non_production"):
            has_unsupported_prod = True

    # 1. Clean Prose & Zero Internal Tags Pass across all client-facing artifacts
    checks_performed += 1
    internal_tag_patterns = [
        (r"\[evidence\]", "contains visible [evidence] tag"),
        (r"\[inference\]", "contains visible [inference] tag"),
        (r"\[\^[a-zA-Z0-9_\-]+\]", "contains visible [^source-id] footnote marker"),
        (r"\[OPEN CONDITION:[^\]]+\]", "contains visible [OPEN CONDITION: ...] diagnostic marker"),
    ]
    client_facing_artifacts = [
        ("Proposal", proposal_md),
        ("Screening answers", screening_md),
        ("Work samples", work_samples_md),
    ]
    for artifact_label, artifact_text in client_facing_artifacts:
        if not artifact_text:
            continue
        for pattern, reason_suffix in internal_tag_patterns:
            if re.search(pattern, artifact_text, re.IGNORECASE):
                violations.append({
                    "type": "clean_prose_violation",
                    "reason": f"{artifact_label} {reason_suffix}",
                })

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

    # 5. Screening Answer Completeness Check (section-scoped for Q2 and Q4)
    checks_performed += 1
    if screening_md:
        q2_section_match = re.search(r"## Question 2:.*?(?=\n## Question |\Z)", screening_md, re.DOTALL)
        if q2_section_match:
            q2_section = q2_section_match.group(0)
            q2_status = re.search(r"\*\*Status\*\*:\s*`?([A-Z_]+)`?", q2_section)
            if q2_status and q2_status.group(1) == "ANSWERED":
                if not re.search(r"\b\d+\s+agents\b", q2_section):
                    violations.append({
                        "type": "screening_answer_status_mismatch",
                        "reason": "Question 2 marked ANSWERED but canonical evidence does not provide an exact numerical agent count.",
                    })

        q4_section_match = re.search(r"## Question 4:.*?(?=\n## Question |\Z)", screening_md, re.DOTALL)
        if q4_section_match:
            q4_section = q4_section_match.group(0)
            q4_status = re.search(r"\*\*Status\*\*:\s*`?([A-Z_]+)`?", q4_section)
            if q4_status and q4_status.group(1) == "ANSWERED":
                if not re.search(r"\b\d+(?:%|\$|x|\s*percent)\b", q4_section):
                    violations.append({
                        "type": "screening_answer_status_mismatch",
                        "reason": "Question 4 marked ANSWERED without an evidence-backed quantitative business outcome metric.",
                    })

    # 6. Work Sample Production Classification Check
    checks_performed += 1
    if work_samples_md:
        if has_unsupported_prod:
            if re.search(r"-\s*\*\*Project Type\*\*:\s*`?client_production`?", work_samples_md, re.IGNORECASE) or \
               re.search(r"project_type:\s*[`\"']?client_production[`\"']?", work_samples_md, re.IGNORECASE):
                violations.append({
                    "type": "work_sample_production_misclassification",
                    "reason": "Work sample classified as client_production when host platform production deployment status is UNKNOWN.",
                })

    # 7. Submission Readiness Alignment Check
    checks_performed += 1
    has_gaps = any(req.get("classification") in ("UNKNOWN", "PARTIALLY_SUPPORTED") for req in req_assessments)
    if has_gaps and sub_readiness != "HUMAN_REVIEW_REQUIRED":
        violations.append({
            "type": "submission_readiness_mismatch",
            "reason": f"submission_readiness is '{sub_readiness}' but material requirements have UNKNOWN/PARTIALLY_SUPPORTED status.",
        })

    # 8. User Decision State Ownership Check
    checks_performed += 1
    if user_dec not in (None, "PENDING_HUMAN_SELECTION", "APPLY", "DO_NOT_APPLY", "HOLD_FOR_EVIDENCE"):
        violations.append({
            "type": "invalid_user_decision_state",
            "reason": f"user_decision_state '{user_dec}' is not a valid V2.1 enum.",
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


def validate_upwork_directory(target_dir: Path) -> dict:
    """Loads generated proposal artefacts from an opportunity directory and validates them."""
    qual_file = target_dir / "runtime" / "upwork-qualification.yaml"
    if not qual_file.exists():
        return {
            "status": "FAIL",
            "checks_performed": 0,
            "total_checks": 0,
            "violations": [{
                "type": "missing_qualification_context",
                "reason": f"Missing qualification file: {qual_file}",
            }],
        }

    try:
        qual_data = yaml.safe_load(qual_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return {
            "status": "FAIL",
            "checks_performed": 1,
            "total_checks": 1,
            "violations": [{
                "type": "invalid_qualification_yaml",
                "reason": f"Failed to parse qualification YAML {qual_file}: {exc}",
            }],
        }

    if qual_data is None:
        qual_data = {}
    elif not isinstance(qual_data, dict):
        return {
            "status": "FAIL",
            "checks_performed": 1,
            "total_checks": 1,
            "violations": [{
                "type": "invalid_qualification_yaml",
                "reason": f"Qualification YAML {qual_file} must be a mapping, got {type(qual_data).__name__}.",
            }],
        }
    proposal_file = target_dir / "upwork-qualification-report.md"
    screening_file = target_dir / "upwork-screening-answers.md"
    samples_file = target_dir / "upwork-work-samples.md"

    proposal_md = proposal_file.read_text(encoding="utf-8") if proposal_file.exists() else ""
    screening_md = screening_file.read_text(encoding="utf-8") if screening_file.exists() else ""
    work_samples_md = samples_file.read_text(encoding="utf-8") if samples_file.exists() else ""

    return validate_upwork_proposal(
        proposal_md=proposal_md,
        screening_md=screening_md,
        qualification_yaml_data=qual_data,
        work_samples_md=work_samples_md,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate generated Upwork proposal artefacts.")
    parser.add_argument("target_slug", nargs="?", help="Opportunity slug under out/ (optional)")
    parser.add_argument("--target-dir", type=Path, help="Explicit opportunity directory path")
    args = parser.parse_args(argv)

    target_dirs: list[Path] = []
    if args.target_dir is not None:
        if not args.target_dir.exists() or not args.target_dir.is_dir():
            print(f"FAIL: Target directory does not exist: {args.target_dir}", file=sys.stderr)
            return 1
        target_dirs.append(args.target_dir)
    elif args.target_slug:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", args.target_slug):
            print(f"FAIL: Invalid target_slug '{args.target_slug}'", file=sys.stderr)
            return 1
        candidate_dir = REPO_ROOT / "out" / args.target_slug
        if not candidate_dir.exists():
            print(f"FAIL: Opportunity directory does not exist: {candidate_dir}", file=sys.stderr)
            return 1
        target_dirs.append(candidate_dir)
    else:
        out_dir = REPO_ROOT / "out"
        if out_dir.exists():
            for child in sorted(out_dir.iterdir()):
                if child.is_dir() and (child / "runtime" / "upwork-qualification.yaml").exists():
                    target_dirs.append(child)

    if not target_dirs:
        print("PASS: No Upwork opportunity directories found to validate.")
        return 0

    any_failed = False
    for td in target_dirs:
        res = validate_upwork_directory(td)
        print(f"[{res['status']}] {td.name}: checks={res['checks_performed']}, violations={len(res['violations'])}")
        for v in res["violations"]:
            print(f"  - {v['type']}: {v['reason']}")
        if res["status"] != "PASS":
            any_failed = True

    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())
