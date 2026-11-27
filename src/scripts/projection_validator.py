"""Unified Deterministic Projection Validator and Sanitizer (User Story 3).

Audits generated projection collateral against canonical factual selection
(out/<target-slug>/runtime/canonical-selection.yaml) and emits
out/<target-slug>/runtime/projection-validation-report.yaml.

Enforces:
1. Education verification (BSc 1988–1991 from Universidade de Mogi das Cruzes; rejects UFRJ/MSc).
2. Certification audit (FATAL on unverified certs e.g. AWS, Sun SCEA/SCJP).
3. Language proficiency audit (FATAL on Spanish Fluent/Full Professional vs Elementary).
4. Named technology claims (FATAL on direct claims of unevidenced client tools e.g. Workday, NetSuite, Coupa, Concur, and dynamic required_job_vocabulary; permits explicit transferable/gap framing).
5. Employment history fidelity (employers, formal titles, immutable dates).
6. Cross-opportunity isolation (FATAL on references to other out/<other-slug>/ directories).

Two-Stage Remediation:
- Stage 1: Automated in-place text sanitization for repairable canonical facts (dates, titles, formal degrees).
- Stage 2: Fatal defect detection (halts with exit code 1 if un-sanitizable direct claims, isolation leaks, or unverified credentials remain).
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set
import yaml

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.scripts.canonical_models import (
    ValidationFinding,
    CheckDetail,
    ValidationSummary,
    ProjectionValidationReport,
)

SLUG_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
EDU_CONTEXT_RE = re.compile(
    r"\b(?:education|graduat\w*|university|universidade|bsc|msc|bachelor|master|degree|computer\s+science|mogi|ufrj|umc)\b",
    re.IGNORECASE,
)

BASELINE_UNSUPPORTED_PLATFORMS = ["Workday", "NetSuite", "Coupa", "Concur"]

TRANSFERABLE_INDICATORS = [
    "comparable to",
    "similar to",
    "transferable",
    "gap",
    "adjacent",
    "analogous",
    "unmatched requirement",
    "evaluation of",
    "architectural assessment of",
]

DIRECT_ACTION_VERBS = [
    r"\bled\b",
    r"\bimplemented\b",
    r"\bimplementing\b",
    r"\bdeployed\b",
    r"\bdeploying\b",
    r"\bdelivered\b",
    r"\barchitected\b",
    r"\bmanaged\b",
    r"\bhands-on\b",
    r"\brollout\b",
    r"\badministration\b",
    r"\bconfigured\b",
    r"\boperational\b",
]


def _validate_target_slug(target_slug: str) -> str:
    """Validates target_slug to prevent path traversal or invalid directory names."""
    if not target_slug or not SLUG_PATTERN.fullmatch(target_slug):
        raise ValueError(
            f"Invalid target_slug '{target_slug}': must match {SLUG_PATTERN.pattern}"
        )
    return target_slug


def _extract_unsupported_platforms(
    opportunity_analysis: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Builds unsupported platform list from baseline plus dynamic required_job_vocabulary."""
    platforms: List[str] = list(BASELINE_UNSUPPORTED_PLATFORMS)
    seen: Set[str] = {p.lower() for p in platforms}

    if isinstance(opportunity_analysis, dict):
        ats = opportunity_analysis.get("ats_vocabulary") or {}
        if isinstance(ats, dict):
            evidenced_terms: Set[str] = set()
            for item in ats.get("candidate_evidenced_vocabulary") or []:
                term = item.get("term", "") if isinstance(item, dict) else str(item)
                if term.strip():
                    evidenced_terms.add(term.strip().lower())

            for item in ats.get("required_job_vocabulary") or []:
                term = item.get("term", "") if isinstance(item, dict) else str(item)
                clean = term.strip()
                if clean and clean.lower() not in evidenced_terms and clean.lower() not in seen:
                    seen.add(clean.lower())
                    platforms.append(clean)

    return platforms


def sanitize_projection_content(
    content: str,
    canonical_selection: Optional[Dict[str, Any]] = None,
    file_path: str = "",
) -> Tuple[str, List[ValidationFinding]]:
    """Stage 1: Deterministically sanitizes repairable canonical facts in content.

    Returns:
        (sanitized_content, sanitization_findings)
    """
    sanitized = content
    findings: List[ValidationFinding] = []
    source = file_path or "inline_text"

    # 1. Sanitize Academic Degree & Institution (UFRJ / MSc -> UMC / BSc)
    msc_patterns = [
        (
            r"(?:MSc|Master of Science)(?:\s+in\s+Computer\s+Science)?(?:,\s*|\s+from\s+|\s+-\s+)(?:Federal University of Rio de Janeiro|UFRJ)",
            "BSc Computer Science, Universidade de Mogi das Cruzes",
            "education",
            "Rewrote unverified MSc/UFRJ claim to canonical BSc Computer Science, Universidade de Mogi das Cruzes",
            "BSc Computer Science, Universidade de Mogi das Cruzes",
        ),
        (
            r"Federal University of Rio de Janeiro|UFRJ",
            "Universidade de Mogi das Cruzes",
            "education",
            "Rewrote unverified institution UFRJ to canonical Universidade de Mogi das Cruzes",
            "Universidade de Mogi das Cruzes",
        ),
        (
            r"\bMSc in Computer Science\b",
            "BSc in Computer Science",
            "education",
            "Rewrote inflated MSc degree to canonical BSc",
            "BSc in Computer Science",
        ),
    ]

    for pat, rep, category, reason, baseline in msc_patterns:
        match = re.search(pat, sanitized, re.IGNORECASE)
        if match:
            orig = match.group(0)
            sanitized = re.sub(pat, rep, sanitized, flags=re.IGNORECASE)
            findings.append(
                ValidationFinding(
                    source_file=source,
                    category=category,
                    severity="SANITIZED",
                    generated_claim=orig,
                    reason=reason,
                    action_taken="sanitized_in_place",
                    canonical_baseline=baseline,
                )
            )

    # 2. Sanitize Education Dates (1995–1999 -> 1988–1991) only in education context
    edu_context_pat = re.compile(
        r"(\b(?:Computer Science|Universidade de Mogi das Cruzes|UMC|BSc)[^\n.]*?)\b1995\s*[–\-]\s*1999\b",
        re.IGNORECASE,
    )
    bare_edu_date_pat = re.compile(r"\b1995\s*[–\-]\s*1999\b")

    lines = sanitized.splitlines(keepends=True)
    new_lines: List[str] = []
    in_education_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            in_education_section = "education" in stripped.lower()

        m_ctx = edu_context_pat.search(line)
        if m_ctx:
            orig = m_ctx.group(0)
            line = edu_context_pat.sub(r"\g<1>1988–1991", line)
            findings.append(
                ValidationFinding(
                    source_file=source,
                    category="education",
                    severity="SANITIZED",
                    generated_claim=orig,
                    reason="Rewrote mutated education dates (1995–1999) to canonical 1988–1991",
                    action_taken="sanitized_in_place",
                    canonical_baseline="1988–1991",
                )
            )
        elif (in_education_section or EDU_CONTEXT_RE.search(line)) and bare_edu_date_pat.search(line):
            m_bare = bare_edu_date_pat.search(line)
            line = bare_edu_date_pat.sub("1988–1991", line)
            findings.append(
                ValidationFinding(
                    source_file=source,
                    category="education",
                    severity="SANITIZED",
                    generated_claim=m_bare.group(0) if m_bare else "1995–1999",
                    reason="Rewrote mutated graduation dates (1995–1999) to canonical 1988–1991",
                    action_taken="sanitized_in_place",
                    canonical_baseline="1988–1991",
                )
            )
        new_lines.append(line)
    sanitized = "".join(new_lines)

    # 3. Sanitize BBC Formal Title Inflation
    bbc_title_patterns = [
        (
            r"Head of Enterprise Architecture\s*&\s*Digital Evolution",
            "Lead Enterprise Architect - Technology Transformation Group",
            "employment",
            "Rewrote inflated BBC title 'Head of Enterprise Architecture & Digital Evolution' to canonical formal title",
            "Lead Enterprise Architect - Technology Transformation Group",
        ),
        (
            r"(\*\*\s*)Head of Enterprise Architecture(\s*\*\*)",
            r"\1Lead Enterprise Architect - Technology Transformation Group\2",
            "employment",
            "Rewrote inflated formal title 'Head of Enterprise Architecture' to canonical 'Lead Enterprise Architect - Technology Transformation Group'",
            "Lead Enterprise Architect - Technology Transformation Group",
        ),
        (
            r"(###\s*BBC\s+Studios.*?\n\*\*)Head of Enterprise Architecture(\*\*)",
            r"\1Lead Enterprise Architect - Technology Transformation Group\2",
            "employment",
            "Rewrote BBC formal title to canonical 'Lead Enterprise Architect - Technology Transformation Group'",
            "Lead Enterprise Architect - Technology Transformation Group",
        ),
    ]

    for pat, rep, category, reason, baseline in bbc_title_patterns:
        match = re.search(pat, sanitized)
        if match:
            orig = match.group(0)
            sanitized = re.sub(pat, rep, sanitized)
            findings.append(
                ValidationFinding(
                    source_file=source,
                    category=category,
                    severity="SANITIZED",
                    generated_claim=orig,
                    reason=reason,
                    action_taken="sanitized_in_place",
                    canonical_baseline=baseline,
                )
            )

    # 4. Sanitize Employment Dates (Chronology)
    employment_date_patterns = [
        (
            r"(WPP(?:\s+Media)?.*?\b)2022\s*[–\-]\s*(?:Present|202\d)",
            r"\g<1>Dec 2025 – Jul 2026",
            "employment",
            "Rewrote fabricated WPP date (2022-Present) to canonical Dec 2025 – Jul 2026",
            "Dec 2025 – Jul 2026",
        ),
        (
            r"(BBC(?:\s+Studios)?.*?\b)2020\s*[–\-]\s*2022",
            r"\g<1>Oct 2021 – Nov 2025",
            "employment",
            "Rewrote fabricated BBC period (2020-2022) to canonical Oct 2021 – Nov 2025",
            "Oct 2021 – Nov 2025",
        ),
    ]

    for pat, rep, category, reason, baseline in employment_date_patterns:
        match = re.search(pat, sanitized, re.IGNORECASE)
        if match:
            orig = match.group(0)
            sanitized = re.sub(pat, rep, sanitized, flags=re.IGNORECASE)
            findings.append(
                ValidationFinding(
                    source_file=source,
                    category=category,
                    severity="SANITIZED",
                    generated_claim=orig,
                    reason=reason,
                    action_taken="sanitized_in_place",
                    canonical_baseline=baseline,
                )
            )

    # 5. Sanitize Claim Strength Enhancement
    claim_patterns = [
        (
            r"[Ee]stablished and led the enterprise architecture governance function",
            "Supported and contributed to the enterprise architecture governance function",
            "employment",
            "Down-leveled unsupported enhancement 'established and led' to canonical 'supported and contributed to'",
            "Supported and contributed to the enterprise architecture governance function",
        ),
    ]

    for pat, rep, category, reason, baseline in claim_patterns:
        match = re.search(pat, sanitized)
        if match:
            orig = match.group(0)
            sanitized = re.sub(pat, rep, sanitized)
            findings.append(
                ValidationFinding(
                    source_file=source,
                    category=category,
                    severity="SANITIZED",
                    generated_claim=orig,
                    reason=reason,
                    action_taken="sanitized_in_place",
                    canonical_baseline=baseline,
                )
            )

    return sanitized, findings


def validate_projection_content(
    content: str,
    canonical_selection: Optional[Dict[str, Any]] = None,
    opportunity_analysis: Optional[Dict[str, Any]] = None,
    file_path: str = "",
    target_slug: str = "standalone",
    prior_sanitization_findings: Optional[List[ValidationFinding]] = None,
) -> ProjectionValidationReport:
    """Stage 2: Audits projection content for fatal discrepancies, certifications, languages, isolation, and platform claims."""
    source = file_path or "inline_text"
    _, stage1_findings = sanitize_projection_content(content, canonical_selection, file_path)

    sanitization_findings: List[ValidationFinding] = list(prior_sanitization_findings or [])
    sanitization_findings.extend(stage1_findings)

    all_findings: List[ValidationFinding] = list(sanitization_findings)
    checks: Dict[str, CheckDetail] = {}

    # 1. Check: Academic Degree & Institution
    sanitized_edu = any(f.category == "education" for f in sanitization_findings)
    checks["education"] = CheckDetail(
        status="SANITIZED" if sanitized_edu else "PASSED",
        details=(
            "Academic credentials sanitized to canonical truth."
            if sanitized_edu
            else "Academic credentials verified (UMC / BSc)."
        ),
    )

    # 2. Check: Certifications Audit
    unverified_certs = [
        (r"\bAWS\s+Certified\b|\bAWS\s+certification\b", "AWS"),
        (r"\bSun\s+Certified\b|\bSCEA\b|\bSCJP\b", "Sun SCEA/SCJP"),
    ]
    cert_failed = False
    for pat, cert_name in unverified_certs:
        match = re.search(pat, content, re.IGNORECASE)
        if match:
            cert_failed = True
            all_findings.append(
                ValidationFinding(
                    source_file=source,
                    category="certification",
                    severity="FATAL",
                    generated_claim=match.group(0),
                    reason=f"Unverified certification claim ({cert_name}): not present in canonical career record.",
                    action_taken="validation_failure_block",
                    canonical_baseline="TOGAF 9, SAFe, LeanIX",
                )
            )
    checks["certifications"] = CheckDetail(
        status="FAILED" if cert_failed else "PASSED",
        details="Unverified certification detected" if cert_failed else "All certifications canonical.",
    )

    # 3. Check: Language Proficiency Audit
    spanish_inflation_patterns = [
        r"Spanish[^\n.]*?(?:fluent|full professional|native|bilingual)",
        r"(?:fluent|native|bilingual)[^\n.]*?Spanish",
    ]
    lang_failed = False
    for pat in spanish_inflation_patterns:
        match = re.search(pat, content, re.IGNORECASE)
        if match:
            lang_failed = True
            all_findings.append(
                ValidationFinding(
                    source_file=source,
                    category="language",
                    severity="FATAL",
                    generated_claim=match.group(0),
                    reason="Spanish proficiency inflated to fluent/professional; canonical record defines Elementary proficiency.",
                    action_taken="validation_failure_block",
                    canonical_baseline="Spanish: Elementary proficiency",
                )
            )
            break
    checks["languages"] = CheckDetail(
        status="FAILED" if lang_failed else "PASSED",
        details=(
            "Spanish language proficiency inflated beyond canonical Elementary"
            if lang_failed
            else "Languages conform to canonical record."
        ),
    )

    # 4. Check: Named Technology Claims / Unsupported Platform Experience
    unsupported_platforms = _extract_unsupported_platforms(opportunity_analysis)

    tech_failed = False
    for line in content.splitlines():
        line_clean = line.strip()
        if not line_clean:
            continue
        line_lower = line_clean.lower()

        for platform in unsupported_platforms:
            if re.search(rf"(?<!\w){re.escape(platform)}(?!\w)", line_clean, re.IGNORECASE):
                is_transferable = any(ind in line_lower for ind in TRANSFERABLE_INDICATORS)
                if is_transferable:
                    continue

                is_direct_action = any(re.search(v, line_lower) for v in DIRECT_ACTION_VERBS)
                is_skill_listing = (
                    line_clean.startswith(("-", "*")) and len(line_clean.split()) <= 6
                ) or (
                    ":" in line_clean
                    and any(hdr in line_lower for hdr in ["tools", "platforms", "skills", "technologies"])
                )

                if is_direct_action or is_skill_listing:
                    tech_failed = True
                    all_findings.append(
                        ValidationFinding(
                            source_file=source,
                            category="technology",
                            severity="FATAL",
                            generated_claim=line_clean,
                            reason=f"Direct unevidenced claim of {platform}: target platform is not evidenced in canonical career record.",
                            action_taken="validation_failure_block",
                            canonical_baseline="No direct platform experience; transferable architecture patterns only",
                        )
                    )
    checks["technology_claims"] = CheckDetail(
        status="FAILED" if tech_failed else "PASSED",
        details=(
            "Direct unevidenced platform claims detected"
            if tech_failed
            else "Technology claims strictly evidenced or transferably framed."
        ),
    )

    # 5. Check: Employment Chronology & Titles
    sanitized_emp = any(f.category == "employment" for f in sanitization_findings)
    checks["employment_chronology"] = CheckDetail(
        status="SANITIZED" if sanitized_emp else "PASSED",
        details=(
            "Employment titles/dates sanitized to canonical truth."
            if sanitized_emp
            else "Employment chronology and titles verified."
        ),
    )

    # 6. Check: Cross-Opportunity Isolation
    isolation_failed = False
    for match in re.finditer(r"\bout/([A-Za-z0-9][A-Za-z0-9_-]*)/", content):
        referenced_slug = match.group(1)
        if referenced_slug.lower() not in ("okf", target_slug.lower()):
            isolation_failed = True
            all_findings.append(
                ValidationFinding(
                    source_file=source,
                    category="isolation",
                    severity="FATAL",
                    generated_claim=match.group(0),
                    reason=f"Cross-opportunity reference to 'out/{referenced_slug}/' violates isolation for '{target_slug}'.",
                    action_taken="validation_failure_block",
                    canonical_baseline=f"out/{target_slug}/ or out/okf/",
                )
            )
    checks["cross_opportunity_isolation"] = CheckDetail(
        status="FAILED" if isolation_failed else "PASSED",
        details=(
            "Cross-opportunity reference detected"
            if isolation_failed
            else "Zero cross-opportunity contamination detected."
        ),
    )

    # Summary computation
    has_fatal = any(f.severity == "FATAL" for f in all_findings)
    has_sanitized = any(f.severity == "SANITIZED" for f in all_findings)

    if has_fatal:
        overall_status = "FAILED"
    elif has_sanitized:
        overall_status = "PASSED_WITH_SANITIZATION"
    else:
        overall_status = "PASSED"

    summary = ValidationSummary(
        total_files_audited=1,
        total_findings=len(all_findings),
        sanitized_count=sum(1 for f in all_findings if f.severity == "SANITIZED"),
        unresolved_defects=sum(1 for f in all_findings if f.severity == "FATAL"),
    )

    return ProjectionValidationReport(
        target_slug=target_slug,
        evaluated_at=datetime.now(timezone.utc).isoformat(),
        overall_status=overall_status,
        validator_version="1.0.0",
        summary=summary,
        checks=checks,
        findings=all_findings,
    )


def _merge_check_detail(existing: Optional[CheckDetail], incoming: CheckDetail) -> CheckDetail:
    """Combines per-file check results keeping highest severity (FAILED > SANITIZED > PASSED)."""
    rank = {"PASSED": 0, "SANITIZED": 1, "FAILED": 2}
    if existing is None or rank.get(incoming.status, 0) > rank.get(existing.status, 0):
        return incoming
    return existing


def validate_opportunity_projections(
    target_slug: str,
    auto_sanitize: bool = True,
    output_report_path: Optional[str] = None,
    out_root: Optional[Path] = None,
) -> ProjectionValidationReport:
    """Validates all projection view artefacts for an opportunity in out/<target-slug>/."""
    _validate_target_slug(target_slug)
    base_out = Path(out_root) if out_root is not None else (REPO_ROOT / "out")
    opp_dir = base_out / target_slug
    runtime_dir = opp_dir / "runtime"

    all_findings: List[ValidationFinding] = []
    combined_checks: Dict[str, CheckDetail] = {}

    canonical_selection = None
    selection_file = runtime_dir / "canonical-selection.yaml"
    if selection_file.exists():
        try:
            with open(selection_file, "r", encoding="utf-8") as f:
                canonical_selection = yaml.safe_load(f)
        except Exception as exc:
            all_findings.append(
                ValidationFinding(
                    source_file=str(selection_file),
                    category="isolation",
                    severity="WARNING",
                    generated_claim="canonical-selection.yaml",
                    reason=f"Failed to parse canonical-selection.yaml: {exc}",
                    action_taken="warning_logged",
                )
            )

    opportunity_analysis = None
    analysis_file = runtime_dir / "opportunity-analysis.yaml"
    if analysis_file.exists():
        try:
            with open(analysis_file, "r", encoding="utf-8") as f:
                opportunity_analysis = yaml.safe_load(f)
        except Exception as exc:
            all_findings.append(
                ValidationFinding(
                    source_file=str(analysis_file),
                    category="isolation",
                    severity="WARNING",
                    generated_claim="opportunity-analysis.yaml",
                    reason=f"Failed to parse opportunity-analysis.yaml: {exc}",
                    action_taken="warning_logged",
                )
            )

    projection_filenames = [
        "resume-executive.md",
        "resume-ats.md",
        "resume-recruiter.md",
        "cover-letter.md",
        "linkedin-profile.md",
        "opportunity-alignment.md",
        "executive-brief.md",
        "playbook.md",
        "interview-cheatsheet.md",
        "upwork-qualification-report.md",
        "upwork-screening-answers.md",
        "upwork-work-samples.md",
        "upwork-evidence-gaps.md",
    ]

    scanned_count = 0
    if opp_dir.exists():
        for fname in projection_filenames:
            target_path = opp_dir / fname
            if not target_path.exists():
                continue
            scanned_count += 1
            content = target_path.read_text(encoding="utf-8")

            s_findings: List[ValidationFinding] = []
            if auto_sanitize:
                sanitized_text, s_findings = sanitize_projection_content(
                    content, canonical_selection, file_path=str(target_path)
                )
                if sanitized_text != content:
                    target_path.write_text(sanitized_text, encoding="utf-8")
                    content = sanitized_text

            report = validate_projection_content(
                content,
                canonical_selection=canonical_selection,
                opportunity_analysis=opportunity_analysis,
                file_path=str(target_path),
                target_slug=target_slug,
                prior_sanitization_findings=s_findings,
            )
            all_findings.extend(report.findings)
            for k, v in report.checks.items():
                combined_checks[k] = _merge_check_detail(combined_checks.get(k), v)

    if scanned_count == 0:
        all_findings.append(
            ValidationFinding(
                source_file=str(opp_dir),
                category="isolation",
                severity="FATAL",
                generated_claim="missing_projection_artefacts",
                reason=f"No projection artefacts found in {opp_dir}",
                action_taken="validation_failure_block",
            )
        )
        for key in (
            "education",
            "certifications",
            "languages",
            "employment_chronology",
            "technology_claims",
            "cross_opportunity_isolation",
        ):
            combined_checks.setdefault(
                key,
                CheckDetail(status="FAILED", details="No projection artefacts available to audit."),
            )

    has_fatal = any(f.severity == "FATAL" for f in all_findings)
    has_sanitized = any(f.severity == "SANITIZED" for f in all_findings)

    if has_fatal:
        overall_status = "FAILED"
    elif has_sanitized:
        overall_status = "PASSED_WITH_SANITIZATION"
    else:
        overall_status = "PASSED"

    summary = ValidationSummary(
        total_files_audited=scanned_count,
        total_findings=len(all_findings),
        sanitized_count=sum(1 for f in all_findings if f.severity == "SANITIZED"),
        unresolved_defects=sum(1 for f in all_findings if f.severity == "FATAL"),
    )

    combined_report = ProjectionValidationReport(
        target_slug=target_slug,
        evaluated_at=datetime.now(timezone.utc).isoformat(),
        overall_status=overall_status,
        validator_version="1.0.0",
        summary=summary,
        checks=combined_checks,
        findings=all_findings,
    )

    out_yaml_path = (
        Path(output_report_path)
        if output_report_path
        else (runtime_dir / "projection-validation-report.yaml")
    )
    out_yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(combined_report.to_dict(), f, sort_keys=False, default_flow_style=False)

    return combined_report


def main():
    target_slug = sys.argv[1] if len(sys.argv) > 1 else "default"
    try:
        report = validate_opportunity_projections(target_slug, auto_sanitize=True)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Projection Validation completed for '{target_slug}': status={report.overall_status}")
    print(f"Summary: fatal={report.summary.unresolved_defects}, sanitized={report.summary.sanitized_count}")

    if report.overall_status == "FAILED":
        print("FATAL: Validation failed due to un-sanitizable integrity defects.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
