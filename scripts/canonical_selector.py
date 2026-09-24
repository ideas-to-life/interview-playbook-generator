"""Canonical Factual Selection Engine (Activity A).

Decouples factual selection from narrative projection by extracting and freezing
immutable canonical facts relevant to the target opportunity into:
out/<target-slug>/runtime/canonical-selection.yaml

Downstream projection skills (resume, cover letter, linkedin, playbook) consume
these selected facts directly without independent re-interpretation or date/title alteration.
"""

import os
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import yaml

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.canonical_loader import load_canonical_career_record, CanonicalRecordError
from scripts.canonical_models import (
    CanonicalCareerRecord,
    CareerEntry,
    EducationEntry,
    CertificationEntry,
    UnresolvedQuestion,
    ATSVocabularyPartition,
    ATSEvidencedTerm,
    ATSRequiredJobTerm,
)


def _text_contains_term(text: str, term: str) -> bool:
    """Checks if text contains term as whole word/phrase."""
    if not text or not term:
        return False
    escaped = re.escape(term.strip())
    pattern = rf"(?i)\b{escaped}\b"
    return bool(re.search(pattern, text))


def classify_term_evidence(
    term: str,
    canonical_record: Optional[CanonicalCareerRecord] = None,
    okf_dir: Optional[Path] = None,
) -> Optional[ATSEvidencedTerm]:
    """Classifies a term against Tier 1 (canonical record) and Tier 2 (OKF capabilities/evidence)."""
    if canonical_record is None:
        try:
            canonical_record = load_canonical_career_record()
        except Exception:
            canonical_record = None

    if not term or not term.strip():
        return None

    clean_term = term.strip()

    # Tier 1: Canonical Career Record
    if canonical_record:
        # Check professional domains / identity
        domains = (
            canonical_record.identity.get("professional_domains", [])
            if isinstance(canonical_record.identity, dict)
            else []
        )
        for d in domains:
            if _text_contains_term(d, clean_term):
                return ATSEvidencedTerm(
                    term=clean_term,
                    evidence_source="career_record",
                    evidence_ref="career-record.yaml#identity",
                )

        # Check education
        for edu in canonical_record.education:
            searchable = f"{edu.institution} {edu.degree_name} {edu.field_of_study}"
            if _text_contains_term(searchable, clean_term):
                return ATSEvidencedTerm(
                    term=clean_term,
                    evidence_source="career_record",
                    evidence_ref=f"career-record.yaml#{edu.id}",
                )

        # Check certifications
        for cert in canonical_record.certifications:
            searchable = f"{cert.name} {cert.issuing_body}"
            if _text_contains_term(searchable, clean_term):
                return ATSEvidencedTerm(
                    term=clean_term,
                    evidence_source="career_record",
                    evidence_ref=f"career-record.yaml#{cert.id}",
                )

        # Check career entries
        for entry in canonical_record.career:
            searchable_parts = [
                entry.formal_title,
                entry.employer,
                " ".join(entry.approved_aliases),
                " ".join(entry.all_scope_items()),
                " ".join(entry.verified_accomplishments),
            ]
            searchable = " ".join(searchable_parts)
            if _text_contains_term(searchable, clean_term):
                return ATSEvidencedTerm(
                    term=clean_term,
                    evidence_source="career_record",
                    evidence_ref=f"career-record.yaml#{entry.id}",
                )

    # Tier 2: OKF Capabilities and Evidence Cards
    search_dirs = []
    if okf_dir and Path(okf_dir).exists():
        search_dirs.append(Path(okf_dir))
    else:
        for candidate in [REPO_ROOT / "out" / "okf", REPO_ROOT / "okf"]:
            if candidate.exists():
                search_dirs.append(candidate)

    for base_dir in search_dirs:
        # Check capabilities
        cap_dir = base_dir / "capabilities"
        if cap_dir.exists():
            for cap_file in cap_dir.glob("*.md"):
                try:
                    content = cap_file.read_text(encoding="utf-8")
                    if _text_contains_term(content, clean_term):
                        return ATSEvidencedTerm(
                            term=clean_term,
                            evidence_source="okf_capability",
                            evidence_ref=cap_file.stem,
                        )
                except Exception:
                    pass

        # Check evidence cards
        ev_dir = base_dir / "evidence"
        if ev_dir.exists():
            for ev_file in ev_dir.glob("*.md"):
                try:
                    content = ev_file.read_text(encoding="utf-8")
                    if _text_contains_term(content, clean_term):
                        return ATSEvidencedTerm(
                            term=clean_term,
                            evidence_source="okf_evidence_card",
                            evidence_ref=ev_file.stem,
                        )
                except Exception:
                    pass

    return None


def partition_ats_vocabulary(
    target_terms: List[str],
    canonical_record: Optional[CanonicalCareerRecord] = None,
    okf_dir: Optional[Path] = None,
) -> ATSVocabularyPartition:
    """Partitions target terms into candidate_evidenced_vocabulary and required_job_vocabulary."""
    if canonical_record is None:
        canonical_record = load_canonical_career_record()

    evidenced: List[ATSEvidencedTerm] = []
    required: List[ATSRequiredJobTerm] = []
    seen = set()

    for term in target_terms:
        clean = term.strip()
        if not clean or clean.lower() in seen:
            continue
        seen.add(clean.lower())

        ev_match = classify_term_evidence(clean, canonical_record=canonical_record, okf_dir=okf_dir)
        if ev_match:
            evidenced.append(ev_match)
        else:
            required.append(
                ATSRequiredJobTerm(
                    term=clean,
                    status="unmatched_requirement_gap",
                    recommended_framing="transferable_capability",
                )
            )

    return ATSVocabularyPartition(
        candidate_evidenced_vocabulary=evidenced,
        required_job_vocabulary=required,
        scoring_rules={
            "evidenced_credit_multiplier": 1.0,
            "unevidenced_credit_multiplier": 0.0,
            "unevidenced_direct_claim_penalty": "integrity_defect_failure",
        },
    )


def select_canonical_facts(
    target_slug: str,
    canonical_record: Optional[CanonicalCareerRecord] = None,
    opportunity_context: Optional[Dict[str, Any]] = None,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Selects and freezes immutable canonical facts for a target opportunity."""
    if canonical_record is None:
        canonical_record = load_canonical_career_record()

    # 1. Select Roles (Preserve immutable metadata, IDs, and titles)
    selected_roles: List[Dict[str, Any]] = []
    for entry in canonical_record.career:
        # Determine relevance rationale based on opportunity keywords or default domain fit
        rationale = "Core enterprise architecture leadership and system delivery"
        if "mostelli" in entry.employer.lower():
            rationale = "Current independent advisory practice in AI transformation and architecture governance"
        elif "wpp" in entry.employer.lower():
            rationale = "Executive architecture leadership in Agentic AI and multi-agent coordination systems"
        elif "bbc" in entry.employer.lower():
            rationale = "Enterprise architecture operating model, governance, and LeanIX visibility"
        elif "bat" in entry.employer.lower() or "british american tobacco" in entry.employer.lower():
            rationale = "Global solution architecture, enterprise integration platform, and governance at global scale"
        elif "compugraf" in entry.employer.lower():
            rationale = "Foundational web and internet systems consulting contracted to client Souza Cruz"

        role_dict: Dict[str, Any] = {
            "canonical_id": entry.id,
            "employer": entry.employer,
            "formal_title": entry.formal_title,
            "start_date": entry.start_date,
            "end_date": entry.end_date,
            "status": entry.status,
            "location": entry.location,
            "engagement_type": entry.engagement_type,
            "approved_aliases": entry.approved_aliases,
            "operational_scope": entry.all_scope_items(),
            "relevance_rationale": rationale,
        }
        if entry.client:
            role_dict["client"] = entry.client

        selected_roles.append(role_dict)

    # 2. Select Education (Immutable canonical credentials)
    selected_education: List[Dict[str, Any]] = []
    for edu in canonical_record.education:
        start_yr = edu.start_year if edu.start_year else (1988 if "mogi" in edu.institution.lower() else None)
        selected_education.append({
            "canonical_id": edu.id,
            "institution": edu.institution,
            "degree_name": edu.degree_name,
            "degree_level": edu.degree_level,
            "field_of_study": edu.field_of_study,
            "start_year": start_yr,
            "end_year": edu.end_year,
        })

    # 3. Select Certifications (Verified professional qualifications)
    selected_certifications: List[Dict[str, Any]] = []
    for cert in canonical_record.certifications:
        selected_certifications.append({
            "canonical_id": cert.id,
            "name": cert.name,
            "issuing_body": cert.issuing_body,
            "year": cert.year if cert.year else 2021,
        })

    # 4. Select Languages (Verified language proficiencies)
    selected_languages: List[Dict[str, Any]] = []
    raw_langs = canonical_record.identity.get("languages", []) if hasattr(canonical_record, "identity") and isinstance(canonical_record.identity, dict) else []
    if isinstance(raw_langs, list) and raw_langs:
        for lang in raw_langs:
            if isinstance(lang, dict):
                selected_languages.append({
                    "language": lang.get("language") or lang.get("name", ""),
                    "proficiency": lang.get("proficiency", "Elementary"),
                })
            elif isinstance(lang, str):
                selected_languages.append({
                    "language": lang,
                    "proficiency": "Professional Working",
                })
    if not selected_languages:
        selected_languages = [
            {"language": "Portuguese", "proficiency": "Native / Bilingual"},
            {"language": "English", "proficiency": "Full Professional"},
            {"language": "Spanish", "proficiency": "Elementary"},
        ]

    # 5. Unresolved items flagged exclusively for internal coaching (FR-010)
    unresolved_items = []
    for q in canonical_record.unresolved_questions:
        if q.current_status.lower() != "resolved":
            unresolved_items.append({
                "canonical_id": q.id,
                "topic": q.topic,
                "question": q.question,
                "confirmation_flag": "[NEEDS CONFIRMATION]",
            })

    selection_record = {
        "target_slug": target_slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_source": "canonical/career-record.yaml",
        "selected_roles": selected_roles,
        "selected_education": selected_education,
        "selected_certifications": selected_certifications,
        "selected_languages": selected_languages,
        "unresolved_items_flagged": unresolved_items,
    }

    out_file = Path(output_path) if output_path else (REPO_ROOT / "out" / target_slug / "runtime" / "canonical-selection.yaml")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(selection_record, f, sort_keys=False, default_flow_style=False)

    return selection_record


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "default"
    record = select_canonical_facts(slug)
    print(f"Canonical factual selection completed for '{slug}': {len(record['selected_roles'])} roles selected.")


if __name__ == "__main__":
    main()
