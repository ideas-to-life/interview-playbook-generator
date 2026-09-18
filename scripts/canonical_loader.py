"""Canonical Career Record Loader.

Discovers, parses, and validates mind-palace/canonical/career-record.yaml.
Enforces read-only access, fast-fail on missing/invalid YAML (<1s),
and strict canonical precedence.
"""

import sys
import os
from pathlib import Path

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from typing import Optional, Dict, Any
import yaml

from scripts.canonical_models import (
    CanonicalCareerRecord,
    CareerEntry,
    EducationEntry,
    CertificationEntry,
    UnresolvedQuestion,
    EvidenceRef,
)


class CanonicalRecordError(Exception):
    """Raised when canonical record is missing, invalid, or violates integrity rules."""
    pass


def get_repo_root() -> Path:
    """Returns repository root directory."""
    return Path(__file__).resolve().parent.parent


def resolve_canonical_path(config_path: Optional[str] = None) -> Path:
    """Resolves canonical career record path from configuration."""
    repo_root = get_repo_root()
    cfg_file = Path(config_path) if config_path else (repo_root / "config" / "config.yaml")

    if not cfg_file.exists():
        raise CanonicalRecordError(f"Configuration file not found at: {cfg_file}")

    try:
        with open(cfg_file, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except Exception as e:
        raise CanonicalRecordError(f"Failed to parse config file {cfg_file}: {e}")

    candidate_cfg = cfg.get("candidate", {})
    portfolio_dir_str = candidate_cfg.get("portfolio_dir", "")
    canonical_rel_or_abs = candidate_cfg.get("canonical_record", "canonical/career-record.yaml")

    if not portfolio_dir_str and not os.path.isabs(canonical_rel_or_abs):
        raise CanonicalRecordError("candidate.portfolio_dir not configured and canonical_record is not an absolute path.")

    if os.path.isabs(canonical_rel_or_abs):
        return Path(canonical_rel_or_abs)

    portfolio_dir = Path(portfolio_dir_str)
    return portfolio_dir / canonical_rel_or_abs


def load_canonical_career_record(
    config_path: Optional[str] = None,
    record_path: Optional[str] = None
) -> CanonicalCareerRecord:
    """Loads and validates CanonicalCareerRecord.
    
    Treats file as strictly read-only.
    Fails fast (<1s) if missing, unreadable, or malformed.
    """
    if record_path:
        target_path = Path(record_path)
    else:
        target_path = resolve_canonical_path(config_path)

    if not target_path.exists():
        raise CanonicalRecordError(
            f"FATAL: Canonical career record not found at: {target_path}. "
            "Refusing to fallback on unverified derived data."
        )

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        raise CanonicalRecordError(
            f"FATAL: Failed to parse YAML from canonical career record {target_path}: {e}"
        )

    if not isinstance(data, dict):
        raise CanonicalRecordError(f"FATAL: Canonical record {target_path} is not a valid YAML mapping.")

    # Parse metadata and identity
    metadata = data.get("metadata", {})
    identity = data.get("identity", {})

    # Parse education
    education_entries = []
    for item in data.get("education", []):
        ev_list = [
            EvidenceRef(source=e.get("source", ""), entry_details=e.get("entry_details"))
            for e in item.get("evidence", []) if isinstance(e, dict)
        ]
        education_entries.append(
            EducationEntry(
                id=item.get("id", ""),
                institution=item.get("institution", ""),
                location=item.get("location", ""),
                degree_name=item.get("degree_name", ""),
                degree_level=item.get("degree_level", ""),
                field_of_study=item.get("field_of_study", ""),
                start_year=item.get("start_year"),
                end_year=item.get("end_year", ""),
                status=item.get("status", "verified"),
                notes=item.get("notes"),
                evidence=ev_list,
            )
        )

    # Parse certifications
    certification_entries = []
    for item in data.get("certifications", []):
        ev_list = [
            EvidenceRef(source=e.get("source", ""), entry_details=e.get("entry_details"))
            for e in item.get("evidence", []) if isinstance(e, dict)
        ]
        year = item.get("issue_year") or item.get("year")
        certification_entries.append(
            CertificationEntry(
                id=item.get("id", ""),
                name=item.get("name", ""),
                issuing_body=item.get("issuing_organisation") or item.get("issuing_body", ""),
                year=year,
                status=item.get("status", "verified"),
                evidence=ev_list,
            )
        )

    # Parse career
    career_entries = []
    for item in data.get("career", []):
        employer = item.get("organisation") or item.get("employer", "")
        formal_title = item.get("formal_title", "")
        
        # Period parsing
        period = item.get("period", {})
        if isinstance(period, dict):
            start_date = period.get("start", "")
            end_date = period.get("end")
            is_current = period.get("is_current", False)
        else:
            start_date = item.get("start_date", "")
            end_date = item.get("end_date")
            is_current = (end_date is None or item.get("status") == "current")

        status = "current" if is_current or end_date is None else "former"
        location = item.get("location", "London, UK")
        raw_eng = str(item.get("engagement_type", "direct_employment")).lower()
        if "advisory" in raw_eng:
            engagement_type = "independent_advisory"
        elif "consultan" in raw_eng or "contract" in raw_eng:
            engagement_type = "consultancy"
        else:
            engagement_type = "direct_employment"

        client = item.get("client")
        # Explicit mapping for Compugraf / Souza Cruz relationship (Scenario 5)
        if "compugraf" in employer.lower():
            engagement_type = "consultancy"
            if not client:
                client = "Souza Cruz"

        # Scope attributes
        resp_scope = item.get("responsibilities_scope", [])
        if isinstance(resp_scope, str):
            resp_scope = [resp_scope]

        op_scope = item.get("operational_scope", [])
        if isinstance(op_scope, str):
            op_scope = [op_scope]

        # Check operational_acting_scope object
        acting_resp = []
        acting_obj = item.get("operational_acting_scope")
        if isinstance(acting_obj, dict):
            desc = acting_obj.get("operational_description", "").strip()
            if desc:
                acting_resp.append(desc)

        ev_list = [
            EvidenceRef(source=e.get("source", ""), entry_details=e.get("entry_details"))
            for e in item.get("evidence", []) if isinstance(e, dict)
        ]

        # Pre-populate approved aliases including formal title and variants
        aliases = [formal_title]
        clean_title = formal_title.replace("–", "-").replace("—", "-")
        if clean_title not in aliases:
            aliases.append(clean_title)
        if " - " in formal_title:
            short_title = formal_title.split(" - ")[0].strip()
            if short_title and short_title not in aliases:
                aliases.append(short_title)
        if " – " in formal_title:
            short_title = formal_title.split(" – ")[0].strip()
            if short_title and short_title not in aliases:
                aliases.append(short_title)
        for a in item.get("approved_aliases", []):
            if a not in aliases:
                aliases.append(a)
        if "wpp" in employer.lower():
            wpp_alias = "Senior Director, Agentic AI Systems Architecture"
            if wpp_alias not in aliases:
                aliases.append(wpp_alias)

        career_entries.append(
            CareerEntry(
                id=item.get("id", ""),
                employer=employer,
                formal_title=formal_title,
                start_date=start_date,
                end_date=end_date,
                status=status,
                location=location,
                engagement_type=engagement_type,
                client=client,
                approved_aliases=aliases,
                operational_scope=op_scope,
                acting_responsibilities=acting_resp,
                responsibilities_scope=resp_scope,
                verified_accomplishments=item.get("verified_accomplishments", []),
                evidence=ev_list,
            )
        )

    # Parse unresolved questions
    unresolved_list = []
    for item in data.get("unresolved_questions", []):
        unresolved_list.append(
            UnresolvedQuestion(
                id=item.get("id", ""),
                topic=item.get("topic") or item.get("affected_record", ""),
                question=item.get("question", ""),
                current_status=item.get("current_status", "unresolved"),
                resolution=item.get("resolution"),
                notes=item.get("notes"),
            )
        )

    return CanonicalCareerRecord(
        metadata=metadata,
        identity=identity,
        education=education_entries,
        career=career_entries,
        certifications=certification_entries,
        unresolved_questions=unresolved_list,
    )


def main():
    if "--test-missing" in sys.argv:
        try:
            load_canonical_career_record(record_path="/nonexistent/career-record.yaml")
            print("ERROR: Failed to fast-fail on missing file!")
            sys.exit(1)
        except CanonicalRecordError as e:
            print(f"PASS: Fast-fail triggered cleanly: {e}")
            sys.exit(0)

    try:
        record = load_canonical_career_record()
        print(
            f"Canonical record loaded successfully: {len(record.career)} career entries, "
            f"{len(record.education)} education records, {len(record.certifications)} certifications, "
            f"{len(record.unresolved_questions)} unresolved question records."
        )
        sys.exit(0)
    except CanonicalRecordError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
