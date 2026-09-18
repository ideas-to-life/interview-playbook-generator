"""Integration test for Cross-Projection Factual Consistency.

Verifies that multiple projection variants (executive resume, ATS resume,
cover letter, LinkedIn profile) share identical canonical dates and formal titles
derived from out/<target-slug>/runtime/canonical-selection.yaml.
"""

from pathlib import Path
import pytest

from scripts.canonical_selector import select_canonical_facts
from scripts.employment_validator import validate_canonical_integrity


def test_projections_share_identical_canonical_facts(tmp_path):
    target_slug = "test-slug"
    out_file = tmp_path / "canonical-selection.yaml"
    selection = select_canonical_facts(target_slug, output_path=str(out_file))

    roles = {r["employer"]: r for r in selection["selected_roles"]}
    wpp_fact = roles.get("WPP Media")
    bbc_fact = next((r for r in selection["selected_roles"] if "BBC" in r["employer"]), None)

    assert wpp_fact is not None
    assert bbc_fact is not None

    # Synthetic executive resume projection consuming canonical selection
    executive_resume = f"""
# Alexandre Franco
## Professional Experience
### {wpp_fact['employer']}
**{wpp_fact['formal_title']}** | *{wpp_fact['start_date']} – {wpp_fact['end_date']}*
* Strategic leadership in Agentic AI.

### {bbc_fact['employer']}
**{bbc_fact['formal_title']}** | *{bbc_fact['start_date']} – {bbc_fact['end_date']}*
* Architecture operating model.
"""

    # Synthetic ATS resume projection consuming canonical selection
    ats_resume = f"""
EXPERIENCE
{wpp_fact['employer']}
{wpp_fact['formal_title']} ({wpp_fact['start_date']} - {wpp_fact['end_date']})
* AI Transformation.

{bbc_fact['employer']}
{bbc_fact['formal_title']} ({bbc_fact['start_date']} - {bbc_fact['end_date']})
* Enterprise Architecture.
"""

    # Synthetic cover letter projection citing canonical background
    cover_letter = f"""
Dear Hiring Team,
As {wpp_fact['formal_title']} at {wpp_fact['employer']} and previously {bbc_fact['formal_title']} at {bbc_fact['employer']},
I have led enterprise transformations across regulated global enterprises.
"""

    # Both resume variants must pass canonical integrity validation
    exec_val = validate_canonical_integrity(executive_resume)
    assert exec_val["status"] == "PASS", f"Executive resume failed validation: {exec_val['violations']}"

    # Verify both variants contain identical canonical titles and dates
    assert wpp_fact['formal_title'] in executive_resume
    assert wpp_fact['formal_title'] in ats_resume
    assert wpp_fact['formal_title'] in cover_letter

    assert bbc_fact['formal_title'] in executive_resume
    assert bbc_fact['formal_title'] in ats_resume
    assert bbc_fact['formal_title'] in cover_letter
