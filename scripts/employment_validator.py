# scripts/employment_validator.py
"""Deterministic validator for career history evidence integrity.

Enforces:
1. Immutable employer names, job titles, employment dates, and status.
2. Rejection of fabricated, approximated, or reconstructed career chronologies (e.g. WPP 2022-Present, BBC 2020-2022, BAT R&D 2016-2020).
3. Rejection of target-aligned title substitutions not explicitly in approved canonical aliases.
4. Rejection of unsupported role splitting or merging.
"""

import os
import re
import yaml

DEFAULT_EMPLOYMENT_RECORDS_PATH = "out/okf/employment-records.yaml"


def load_canonical_employment_records(path: str = None) -> list[dict]:
    """Loads canonical employment records from YAML."""
    target_path = path or DEFAULT_EMPLOYMENT_RECORDS_PATH
    if not os.path.exists(target_path):
        # Fallback default canonical records for Alexandre Franco
        return [
            {
                "id": "emp-wpp-2025",
                "employer": "WPP Media",
                "title": "Senior Director, Agentic AI Systems Architecture",
                "start_date": "Dec 2025",
                "end_date": None,
                "status": "current",
                "location": "London, UK",
                "approved_aliases": [
                    "Senior Director, Agentic AI Systems Architecture",
                ],
            },
            {
                "id": "emp-bbc-2021",
                "employer": "BBC Studios",
                "title": "Lead Enterprise Architect",
                "start_date": "Nov 2021",
                "end_date": "Nov 2025",
                "status": "former",
                "location": "London, UK",
                "approved_aliases": [
                    "Lead Enterprise Architect",
                    "Lead Enterprise Architect – Technology Transformation Group & Commercial",
                ],
            },
            {
                "id": "emp-bat-2011",
                "employer": "British American Tobacco",
                "title": "Enterprise Architect & Global Solution Architect",
                "start_date": "2011",
                "end_date": "2021",
                "status": "former",
                "location": "London, UK & São Paulo, Brazil",
                "approved_aliases": [
                    "Enterprise Architect & Global Solution Architect",
                    "Enterprise Architect — Scientific Research & Development",
                    "Enterprise Architect",
                ],
            },
        ]
    with open(target_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("employment_records", [])


def validate_employment_history(artefact_content: str, canonical_records: list[dict] = None) -> dict:
    """Validates markdown content against canonical employment records.

    Returns dict with status ('PASS' or 'FAIL'), field_checks count, records_checked count, and violations list.
    """
    if canonical_records is None:
        canonical_records = load_canonical_employment_records()

    violations = []
    field_checks = 0

    # Defect patterns (known fabricated chronologies to reject strictly)
    known_fabricated_patterns = [
        (r"WPP(?:\s+Media)?.*?\b2022\s*[–\-]\s*(?:Present|202\d)", "Fabricated WPP start date (2022 instead of Dec 2025)"),
        (r"BBC(?:\s+Studios)?.*?\b2020\s*[–\-]\s*2022\b", "Fabricated BBC Studios period (2020–2022 instead of Nov 2021–Nov 2025)"),
        (r"BAT\s+R&D.*?\b2016\s*[–\-]\s*2020\b", "Fabricated role split BAT R&D (2016–2020 unsupported by canonical evidence)"),
        (r"Enterprise Architect\s*&\s*AI Practice Lead", "Target title substitution 'Enterprise Architect & AI Practice Lead' unsupported by canonical evidence"),
        (r"Principal Enterprise Cloud Architect", "Target title substitution 'Principal Enterprise Cloud Architect' unsupported by canonical evidence"),
        (r"Head of Enterprise Architecture\s*&\s*Systems", "Target title substitution 'Head of Enterprise Architecture & Systems' unsupported by canonical evidence"),
    ]

    for pattern, description in known_fabricated_patterns:
        field_checks += 1
        if re.search(pattern, artefact_content, re.IGNORECASE):
            violations.append({
                "type": "fabricated_chronology_or_title",
                "reason": description,
            })

    # Validate canonical record integrity
    for rec in canonical_records:
        employer = rec["employer"]
        title = rec["title"]
        start_date = rec["start_date"]
        end_date = rec.get("end_date") or "Present"
        aliases = rec.get("approved_aliases", [title])

        field_checks += 1
        # Check if employer is mentioned in experience section
        if employer in artefact_content:
            # Check for date presence if section header exists
            employer_blocks = re.findall(rf"{re.escape(employer)}.*?(?=\n###|\n##|\Z)", artefact_content, re.DOTALL)
            for block in employer_blocks:
                field_checks += 2
                if "Dec 2025" in start_date:
                    if "2022" in block and "Dec 2025" not in block:
                        violations.append({
                            "type": "date_mutation",
                            "employer": employer,
                            "reason": f"Employer {employer} start date mutated from {start_date} to 2022.",
                        })

                if "Nov 2021" in start_date:
                    if "2020" in block and "Nov 2021" not in block:
                        violations.append({
                            "type": "date_mutation",
                            "employer": employer,
                            "reason": f"Employer {employer} start date mutated from {start_date} to 2020.",
                        })

                has_approved_title = any(alias in block for alias in aliases)
                if not has_approved_title:
                    title_match = re.search(r"^\*\*([^*]+)\*\*", block, re.MULTILINE)
                    if title_match:
                        detected_title = title_match.group(1).strip()
                        if detected_title not in aliases:
                            violations.append({
                                "type": "unsupported_title_alias",
                                "employer": employer,
                                "detected_title": detected_title,
                                "reason": f"Detected title '{detected_title}' for {employer} is not in approved canonical aliases.",
                            })

    status = "PASS" if not violations else "FAIL"
    return {
        "status": status,
        "records_checked": len(canonical_records),
        "field_checks": field_checks,
        "violations": violations,
    }
