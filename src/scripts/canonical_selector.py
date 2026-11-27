"""Canonical Factual Selection Engine (Activity A).

Decouples factual selection from narrative projection by extracting and freezing
immutable canonical facts relevant to the target opportunity into:
out/<target-slug>/runtime/canonical-selection.yaml

Downstream projection skills (resume, cover letter, linkedin, playbook) consume
these selected facts directly without independent re-interpretation or date/title alteration.
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import yaml

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.scripts.canonical_loader import load_canonical_career_record
from src.scripts.canonical_models import (
    CanonicalCareerRecord,
    ATSVocabularyPartition,
    ATSEvidencedTerm,
    ATSRequiredJobTerm,
)

SLUG_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def _validate_target_slug(target_slug: str) -> str:
    """Validates target_slug to prevent path traversal."""
    if not target_slug or not SLUG_PATTERN.fullmatch(target_slug):
        raise ValueError(
            f"Invalid target_slug '{target_slug}': must match {SLUG_PATTERN.pattern}"
        )
    return target_slug


def _text_contains_term(text: str, term: str) -> bool:
    """Checks if text contains term as whole word/phrase, supporting symbol-bearing terms like C++ and .NET."""
    if not text or not term:
        return False
    escaped = re.escape(term.strip())
    pattern = rf"(?i)(?<!\w){escaped}(?!\w)"
    return bool(re.search(pattern, text))


def _load_okf_corpus(okf_dir: Optional[Path] = None) -> List[Tuple[str, str, str]]:
    """Loads OKF capability and evidence markdown texts once for reuse across term checks."""
    search_dirs: List[Path] = []
    if okf_dir and Path(okf_dir).exists():
        search_dirs.append(Path(okf_dir))
    else:
        for candidate in [REPO_ROOT / "out" / "okf", REPO_ROOT / "okf"]:
            if candidate.exists():
                search_dirs.append(candidate)

    corpus: List[Tuple[str, str, str]] = []
    for base_dir in search_dirs:
        for sub_name, ev_source in [("capabilities", "okf_capability"), ("evidence", "okf_evidence_card")]:
            sub_dir = base_dir / sub_name
            if sub_dir.exists():
                for md_file in sorted(sub_dir.glob("*.md")):
                    try:
                        corpus.append((ev_source, md_file.stem, md_file.read_text(encoding="utf-8")))
                    except Exception as exc:
                        print(f"WARNING: Failed to read OKF file {md_file}: {exc}", file=sys.stderr)
    return corpus


def classify_term_evidence(
    term: str,
    canonical_record: Optional[CanonicalCareerRecord] = None,
    okf_dir: Optional[Path] = None,
    _preloaded_okf: Optional[List[Tuple[str, str, str]]] = None,
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

        for edu in canonical_record.education:
            searchable = f"{edu.institution} {edu.degree_name} {edu.field_of_study}"
            if _text_contains_term(searchable, clean_term):
                return ATSEvidencedTerm(
                    term=clean_term,
                    evidence_source="career_record",
                    evidence_ref=f"career-record.yaml#{edu.id}",
                )

        for cert in canonical_record.certifications:
            searchable = f"{cert.name} {cert.issuing_body}"
            if _text_contains_term(searchable, clean_term):
                return ATSEvidencedTerm(
                    term=clean_term,
                    evidence_source="career_record",
                    evidence_ref=f"career-record.yaml#{cert.id}",
                )

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
    okf_corpus = _preloaded_okf if _preloaded_okf is not None else _load_okf_corpus(okf_dir)
    for ev_source, stem, content in okf_corpus:
        if _text_contains_term(content, clean_term):
            return ATSEvidencedTerm(
                term=clean_term,
                evidence_source=ev_source,
                evidence_ref=stem,
            )

    return None


def partition_ats_vocabulary(
    target_terms: List[str],
    canonical_record: Optional[CanonicalCareerRecord] = None,
    okf_dir: Optional[Path] = None,
) -> ATSVocabularyPartition:
    """Partitions target terms into candidate_evidenced_vocabulary and required_job_vocabulary."""
    if canonical_record is None:
        canonical_record = load_canonical_career_record()

    preloaded_okf = _load_okf_corpus(okf_dir)
    evidenced: List[ATSEvidencedTerm] = []
    required: List[ATSRequiredJobTerm] = []
    seen = set()

    for term in target_terms:
        clean = term.strip()
        if not clean or clean.lower() in seen:
            continue
        seen.add(clean.lower())

        ev_match = classify_term_evidence(
            clean,
            canonical_record=canonical_record,
            okf_dir=okf_dir,
            _preloaded_okf=preloaded_okf,
        )
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
    _validate_target_slug(target_slug)
    if canonical_record is None:
        canonical_record = load_canonical_career_record()

    # 1. Select Roles (Preserve immutable metadata, IDs, and titles)
    selected_roles: List[Dict[str, Any]] = []
    for entry in canonical_record.career:
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

    # 2. Select Education (Immutable canonical credentials; never fabricate missing start_year)
    selected_education: List[Dict[str, Any]] = []
    for edu in canonical_record.education:
        selected_education.append({
            "canonical_id": edu.id,
            "institution": edu.institution,
            "degree_name": edu.degree_name,
            "degree_level": edu.degree_level,
            "field_of_study": edu.field_of_study,
            "start_year": edu.start_year,
            "end_year": edu.end_year,
        })

    # 3. Select Certifications (Verified professional qualifications; never fabricate missing year)
    selected_certifications: List[Dict[str, Any]] = []
    for cert in canonical_record.certifications:
        selected_certifications.append({
            "canonical_id": cert.id,
            "name": cert.name,
            "issuing_body": cert.issuing_body,
            "year": cert.year,
        })

    # 4. Select Languages (Verified language proficiencies; never fabricate missing languages)
    selected_languages: List[Dict[str, Any]] = []
    raw_langs = (
        canonical_record.identity.get("languages", [])
        if hasattr(canonical_record, "identity") and isinstance(canonical_record.identity, dict)
        else []
    )
    if isinstance(raw_langs, list):
        for lang in raw_langs:
            if isinstance(lang, dict):
                selected_languages.append({
                    "language": lang.get("language") or lang.get("name", ""),
                    "proficiency": lang.get("proficiency"),
                })
            elif isinstance(lang, str):
                selected_languages.append({
                    "language": lang,
                    "proficiency": None,
                })

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
    try:
        record = select_canonical_facts(slug)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"Canonical factual selection completed for '{slug}': {len(record['selected_roles'])} roles selected.")


if __name__ == "__main__":
    main()
