"""CLI and validation completeness tests for scripts/upwork_validator.py."""

import subprocess
import sys
from pathlib import Path
import yaml

from src.scripts.upwork_validator import validate_upwork_proposal


REPO_ROOT = Path(__file__).resolve().parent.parent


def _write_upwork_fixture(target_dir: Path, proposal_text: str, screening_text: str = "", work_samples_text: str = "") -> None:
    runtime_dir = target_dir / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    qual = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": "PENDING_HUMAN_SELECTION",
        "requirement_assessments": [
            {
                "requirement_id": "req-1",
                "classification": "PARTIALLY_SUPPORTED",
                "production_status": "unknown",
                "missing_facts": ["production_deployment_verification"],
            }
        ],
    }
    (runtime_dir / "upwork-qualification.yaml").write_text(yaml.safe_dump(qual), encoding="utf-8")
    (target_dir / "upwork-qualification-report.md").write_text(proposal_text, encoding="utf-8")
    if screening_text:
        (target_dir / "upwork-screening-answers.md").write_text(screening_text, encoding="utf-8")
    if work_samples_text:
        (target_dir / "upwork-work-samples.md").write_text(work_samples_text, encoding="utf-8")


def test_upwork_validator_cli_passes_on_valid_directory(tmp_path):
    target_dir = tmp_path / "valid-opp"
    _write_upwork_fixture(
        target_dir,
        proposal_text="Architected agentic orchestration guardrails and evaluation pipelines.",
        screening_text="## Question 1: Describe experience\n**Status**: `ANSWERED`\nBuilt systems.\n",
    )

    res = subprocess.run(
        [sys.executable, str(REPO_ROOT / "src" / "scripts" / "upwork_validator.py"), "--target-dir", str(target_dir)],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Expected exit 0, got {res.returncode}: {res.stdout}\n{res.stderr}"
    assert "PASS" in res.stdout


def test_upwork_validator_cli_fails_on_invalid_directory(tmp_path):
    target_dir = tmp_path / "invalid-opp"
    _write_upwork_fixture(
        target_dir,
        proposal_text="I personally architected and implemented production multi-agent systems [evidence].",
    )

    res = subprocess.run(
        [sys.executable, str(REPO_ROOT / "src" / "scripts" / "upwork_validator.py"), "--target-dir", str(target_dir)],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 1, f"Expected exit 1, got {res.returncode}: {res.stdout}\n{res.stderr}"
    assert "FAIL" in res.stdout


def test_clean_prose_checks_screening_and_work_samples():
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": None,
        "requirement_assessments": [],
    }
    res_screening = validate_upwork_proposal(
        "Clean proposal text.",
        "Answer containing internal [evidence] marker [^src-1].",
        qual_data,
    )
    assert res_screening["status"] == "FAIL"
    assert res_screening["clean_prose_verified"] is False

    res_samples = validate_upwork_proposal(
        "Clean proposal text.",
        "Clean screening answer.",
        qual_data,
        work_samples_md="Sample with leaked [^internal-ref] tag.",
    )
    assert res_samples["status"] == "FAIL"
    assert res_samples["clean_prose_verified"] is False


def test_screening_q2_and_q4_checks_are_section_scoped():
    qual_data = {
        "submission_readiness": "HUMAN_REVIEW_REQUIRED",
        "user_decision_state": None,
        "requirement_assessments": [],
    }
    screening = (
        "## Question 1: Scale?\n"
        "**Status**: `ANSWERED`\n"
        "Coordinated 12 agents and improved speed by 40%.\n\n"
        "## Question 2: How many agents were involved?\n"
        "**Status**: `ANSWERED`\n"
        "Multiple specialized agents collaborated.\n\n"
        "## Question 4: What measurable business result did the system produce?\n"
        "**Status**: `ANSWERED`\n"
        "Improved team visibility without a specific metric.\n"
    )
    res = validate_upwork_proposal("Clean proposal text.", screening, qual_data)
    assert res["status"] == "FAIL"
    assert res["screening_completeness_verified"] is False
    assert len([v for v in res["violations"] if v["type"] == "screening_answer_status_mismatch"]) == 2


def test_upwork_validator_handles_malformed_qualification_yaml(tmp_path):
    from src.scripts.upwork_validator import validate_upwork_directory

    target_dir = tmp_path / "bad-yaml-opp"
    (target_dir / "runtime").mkdir(parents=True)
    (target_dir / "runtime" / "upwork-qualification.yaml").write_text("bad: [unclosed\n", encoding="utf-8")

    res = validate_upwork_directory(target_dir)
    assert res["status"] == "FAIL"
    assert any(v["type"] == "invalid_qualification_yaml" for v in res["violations"])
