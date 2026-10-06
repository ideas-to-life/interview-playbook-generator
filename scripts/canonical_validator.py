"""Canonical Conflict Audit Detector.

Detects discrepancies between canonical career facts and secondary documents or
generated content. Emits a structured conflict report conforming to
specs/005-canonical-record-integration/contracts/canonical-conflict-report-contract.yaml.
Target location: out/<target-slug>/runtime/canonical-conflict-report.yaml
"""

import os
import re
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
from scripts.canonical_models import CanonicalCareerRecord


# Canonical truth definitions for auditing
CANONICAL_EDUCATION_FACT = "BSc Computer Science, Universidade de Mogi das Cruzes"
CANONICAL_BBC_TITLE_FACT = "Lead Enterprise Architect - Technology Transformation Group"
CANONICAL_WPP_DATES_FACT = "Dec 2025 – Jul 2026"
CANONICAL_BBC_DATES_FACT = "Oct 2021 – Nov 2025"
CANONICAL_BAT_DATES_FACT = "Jul 2011 – Sep 2021"
CANONICAL_COMPUGRAF_FACT = "Compugraf as external consultancy contracted to client Souza Cruz"
CANONICAL_WPP_MOSTELLI_FACT = "WPP Media (direct corporate employment) and Mostelli (independent advisory) are distinct timeline entries"
CANONICAL_GOVERNANCE_FACT = "Supported and contributed to enterprise architecture governance"


def detect_conflicts_in_text(text: str, source_file: str = "unknown") -> List[Dict[str, Any]]:
    """Scans a text content for claims conflicting with canonical career facts."""
    conflicts: List[Dict[str, Any]] = []

    # 1. Degree level / Institution conflicts (Scenario 1)
    msc_matches = re.findall(
        r"(?:MSc|Master of Science)[^.\n]*?(?:Federal University of Rio de Janeiro|UFRJ)",
        text,
        re.IGNORECASE
    )
    if msc_matches:
        for match in msc_matches:
            conflicts.append({
                "source_file": source_file,
                "field_type": "degree_level",
                "conflicting_claim": match.strip(),
                "canonical_fact": CANONICAL_EDUCATION_FACT,
                "action_taken": "canonical_override",
                "severity": "high",
            })
    else:
        # Check standalone Federal University of Rio de Janeiro
        ufrj_matches = re.findall(
            r"Federal University of Rio de Janeiro|UFRJ",
            text,
            re.IGNORECASE
        )
        for match in ufrj_matches:
            conflicts.append({
                "source_file": source_file,
                "field_type": "institution",
                "conflicting_claim": match.strip(),
                "canonical_fact": "Universidade de Mogi das Cruzes",
                "action_taken": "canonical_override",
                "severity": "high",
            })

    # 2. Formal title inflation (Scenario 2 & 3)
    # Target title inflation for BBC: Head of Enterprise Architecture & Digital Evolution or Head of Enterprise Architecture
    bbc_title_patterns = [
        r"Head of Enterprise Architecture(?:\s*&\s*Digital Evolution)?",
        r"Head of Architecture(?:\s*&\s*Digital Evolution)?",
    ]
    # Look for formal title assignments to Alexandre at BBC
    for pat in bbc_title_patterns:
        matches = re.finditer(rf"(?:###|\*\*|Title:)?\s*({pat})(?:\s*\||\s*–|\s*—|\s*at\s+BBC|\s+BBC)", text, re.IGNORECASE)
        for m in matches:
            claim = m.group(1).strip()
            conflicts.append({
                "source_file": source_file,
                "field_type": "formal_title",
                "conflicting_claim": claim,
                "canonical_fact": CANONICAL_BBC_TITLE_FACT,
                "action_taken": "canonical_override",
                "severity": "high",
            })

    # 3. Chronology / Dates conflicts (Scenario 4, WPP 2022, BBC 2020-2022)
    wpp_date_matches = re.finditer(r"WPP(?:\s+Media)?.*?\b(2022\s*[–\-]\s*(?:Present|202\d))", text, re.IGNORECASE | re.DOTALL)
    for m in wpp_date_matches:
        conflicts.append({
            "source_file": source_file,
            "field_type": "dates",
            "conflicting_claim": f"WPP Media period {m.group(1)}",
            "canonical_fact": f"WPP Media {CANONICAL_WPP_DATES_FACT}",
            "action_taken": "canonical_override",
            "severity": "high",
        })

    bbc_date_matches = re.finditer(r"BBC(?:\s+Studios)?.*?\b(2020\s*[–\-]\s*2022\b)", text, re.IGNORECASE | re.DOTALL)
    for m in bbc_date_matches:
        conflicts.append({
            "source_file": source_file,
            "field_type": "dates",
            "conflicting_claim": f"BBC period {m.group(1)}",
            "canonical_fact": f"BBC Studios {CANONICAL_BBC_DATES_FACT}",
            "action_taken": "canonical_override",
            "severity": "high",
        })

    bat_split_matches = re.finditer(r"(?:BAT|British American Tobacco)(?:\s+R&D)?.*?\b(2016\s*[–\-]\s*2020\b)", text, re.IGNORECASE | re.DOTALL)
    for m in bat_split_matches:
        conflicts.append({
            "source_file": source_file,
            "field_type": "dates",
            "conflicting_claim": f"BAT incomplete/split period {m.group(1)}",
            "canonical_fact": f"British American Tobacco {CANONICAL_BAT_DATES_FACT}",
            "action_taken": "canonical_override",
            "severity": "medium",
        })

    # 4. Employer relationship conflicts (Scenario 5 & 6)
    if re.search(r"simultaneous\s+direct\s+employment.*?(?:Compugraf|Souza Cruz)", text, re.IGNORECASE) or \
       re.search(r"employed\s+by\s+Souza Cruz\s+and\s+Compugraf\s+directly", text, re.IGNORECASE):
        conflicts.append({
            "source_file": source_file,
            "field_type": "employer_relationship",
            "conflicting_claim": "Compugraf and Souza Cruz as simultaneous direct employers",
            "canonical_fact": CANONICAL_COMPUGRAF_FACT,
            "action_taken": "canonical_override",
            "severity": "high",
        })

    if re.search(r"WPP(?:\s+Media)?\s*(?:and|&)\s*Mostelli\s*(?:merged|continuous\s+engagement)", text, re.IGNORECASE):
        conflicts.append({
            "source_file": source_file,
            "field_type": "employer_relationship",
            "conflicting_claim": "WPP Media and Mostelli merged into single continuous engagement",
            "canonical_fact": CANONICAL_WPP_MOSTELLI_FACT,
            "action_taken": "canonical_override",
            "severity": "high",
        })

    # 5. Claim strength / Unsupported enhancement (Scenario 8)
    gov_matches = re.finditer(
        r"(?:established\s+and\s+led|created\s+and\s+directed)\s+the\s+enterprise\s+architecture\s+governance\s+function",
        text,
        re.IGNORECASE
    )
    for m in gov_matches:
        conflicts.append({
            "source_file": source_file,
            "field_type": "claim_strength",
            "conflicting_claim": m.group(0).strip(),
            "canonical_fact": CANONICAL_GOVERNANCE_FACT,
            "action_taken": "canonical_override",
            "severity": "medium",
        })

    return conflicts


def generate_conflict_audit_report(
    target_slug: str,
    source_paths: Optional[List[str]] = None,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """Generates canonical conflict report at out/<target-slug>/runtime/canonical-conflict-report.yaml."""
    all_conflicts: List[Dict[str, Any]] = []

    # If source paths provided, scan them
    if source_paths:
        for sp in source_paths:
            p = Path(sp)
            if p.exists() and p.is_file():
                content = p.read_text(encoding="utf-8", errors="ignore")
                file_conflicts = detect_conflicts_in_text(content, source_file=str(p))
                all_conflicts.extend(file_conflicts)

    # Also scan any projection files in out/<target-slug>/ if they exist
    target_dir = REPO_ROOT / "out" / target_slug
    if target_dir.exists():
        for proj_file in target_dir.glob("*.md"):
            content = proj_file.read_text(encoding="utf-8", errors="ignore")
            file_conflicts = detect_conflicts_in_text(content, source_file=str(proj_file))
            all_conflicts.extend(file_conflicts)

    report = {
        "target_slug": target_slug,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "total_conflicts": len(all_conflicts),
        "conflicts": all_conflicts,
    }

    out_file = Path(output_path) if output_path else (REPO_ROOT / "out" / target_slug / "runtime" / "canonical-conflict-report.yaml")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(report, f, sort_keys=False, default_flow_style=False)

    return report


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "default"
    rep = generate_conflict_audit_report(slug)
    print(f"Audit completed: {rep['total_conflicts']} conflicts found.")
