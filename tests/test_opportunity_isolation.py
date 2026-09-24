"""Test for cross-opportunity runtime isolation (FR-003, FR-017, Scenario 6, Scenario 7).

Verifies that generation runs for target A never read, inspect, or depend on
artefacts belonging to target B (e.g. out/lseg-director-enterprise-architecture/ vs
out/tenth-ai-lead-enterprise-architect/).
"""

from pathlib import Path
import pytest
import shutil
import tempfile
import yaml

from scripts.canonical_selector import select_canonical_facts

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_cross_opportunity_isolation_no_prior_read(tmp_path):
    """Scenario 6 & 7: Verify generation runs read zero files from other target directories."""
    # 1. Create a prior opportunity directory with deliberately contaminated candidate facts
    prior_slug = "lseg-director-enterprise-architecture"
    prior_dir = tmp_path / "out" / prior_slug
    prior_dir.mkdir(parents=True, exist_ok=True)
    corrupted_resume = prior_dir / "resume-executive.md"
    corrupted_resume.write_text(
        "# Alexandre Franco\n"
        "AWS Certified Solutions Architect – Associate (2023)\n"
        "Spanish: Fluent\n"
        "Universidade de Mogi das Cruzes, BSc 1995–1999\n",
        encoding="utf-8"
    )

    # 2. Generate new opportunity factual selection
    active_slug = "tenth-ai-lead-enterprise-architect"
    active_out = tmp_path / "out" / active_slug / "runtime" / "canonical-selection.yaml"
    selection = select_canonical_facts(
        target_slug=active_slug,
        output_path=str(active_out)
    )

    # 3. Assert active selection contains ZERO facts from the prior opportunity
    content = active_out.read_text(encoding="utf-8")
    assert "AWS Certified Solutions Architect" not in content
    assert "1995–1999" not in content
    assert "Fluent" not in content
    assert prior_slug not in content

    # 4. Verify canonical facts in active selection
    edu = selection["selected_education"][0]
    assert edu["start_year"] == 1988
    assert edu["end_year"] == 1991

    spanish = next((l for l in selection["selected_languages"] if l["language"].lower() == "spanish"), None)
    assert spanish is not None
    assert "elementary" in spanish["proficiency"].lower()
    assert "fluent" not in spanish["proficiency"].lower()


def test_opportunity_isolation_order_independence(tmp_path):
    """Scenario 7: Generating Target A then Target B vs Target B then Target A produces identical results."""
    slug_a = "target-alpha"
    slug_b = "target-beta"

    out_a1 = tmp_path / "run1" / "out" / slug_a / "runtime" / "canonical-selection.yaml"
    out_b1 = tmp_path / "run1" / "out" / slug_b / "runtime" / "canonical-selection.yaml"

    out_b2 = tmp_path / "run2" / "out" / slug_b / "runtime" / "canonical-selection.yaml"
    out_a2 = tmp_path / "run2" / "out" / slug_a / "runtime" / "canonical-selection.yaml"

    # Run 1: A then B
    res_a1 = select_canonical_facts(slug_a, output_path=str(out_a1))
    res_b1 = select_canonical_facts(slug_b, output_path=str(out_b1))

    # Run 2: B then A
    res_b2 = select_canonical_facts(slug_b, output_path=str(out_b2))
    res_a2 = select_canonical_facts(slug_a, output_path=str(out_a2))

    # Ensure selected facts are identical regardless of execution order
    assert res_a1["selected_education"] == res_a2["selected_education"]
    assert res_a1["selected_certifications"] == res_a2["selected_certifications"]
    assert res_b1["selected_education"] == res_b2["selected_education"]
    assert res_b1["selected_certifications"] == res_b2["selected_certifications"]
