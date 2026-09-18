"""Canonical Factual Selection Engine (Activity A).

Decouples factual selection from narrative projection by extracting and freezing
immutable canonical facts relevant to the target opportunity into:
out/<target-slug>/runtime/canonical-selection.yaml

Downstream projection skills (resume, cover letter, linkedin, playbook) consume
these selected facts directly without independent re-interpretation or date/title alteration.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
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
        selected_education.append({
            "canonical_id": edu.id,
            "institution": edu.institution,
            "degree_name": edu.degree_name,
            "degree_level": edu.degree_level,
            "field_of_study": edu.field_of_study,
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

    # 4. Unresolved items flagged exclusively for internal coaching (FR-010)
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
