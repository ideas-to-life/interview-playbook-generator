"""Unit and CLI tests for src/scripts/deploy_skills.py."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent


def _make_skill(root: Path, name: str, *, frontmatter: bool = True, include_cache: bool = False) -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    if frontmatter:
        content = f"---\nname: {name}\ndescription: Test skill {name}\n---\n\n# {name}\n"
    else:
        content = f"# {name}\nMissing frontmatter\n"
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
    if include_cache:
        cache_dir = skill_dir / "__pycache__"
        cache_dir.mkdir(exist_ok=True)
        (cache_dir / "mod.cpython-313.pyc").write_bytes(b"pyc")
        (skill_dir / ".DS_Store").write_bytes(b"ds")
    return skill_dir


def test_discover_skills_finds_valid_skills_and_skips_pycache(tmp_path):
    from src.scripts.deploy_skills import discover_skills

    src = tmp_path / "src_skills"
    _make_skill(src, "alpha-skill")
    _make_skill(src, "beta-skill")
    (src / "__pycache__").mkdir()
    (src / ".hidden").mkdir()
    (src / "not-a-skill").mkdir()

    found = discover_skills(src)
    assert [p.name for p in found] == ["alpha-skill", "beta-skill"]

    subset = discover_skills(src, only=["beta-skill"])
    assert [p.name for p in subset] == ["beta-skill"]

    with pytest.raises(ValueError):
        discover_skills(src, only=["nonexistent-skill"])


def test_validate_skill_frontmatter_rejects_missing_fields(tmp_path):
    from src.scripts.deploy_skills import validate_skill_md

    bad_no_fm = _make_skill(tmp_path, "no-fm", frontmatter=False)
    with pytest.raises(ValueError):
        validate_skill_md(bad_no_fm)

    bad_no_desc = tmp_path / "no-desc"
    bad_no_desc.mkdir()
    (bad_no_desc / "SKILL.md").write_text("---\nname: no-desc\n---\n\n# Body\n", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_skill_md(bad_no_desc)

    good = _make_skill(tmp_path, "valid-skill")
    meta = validate_skill_md(good)
    assert meta["name"] == "valid-skill"
    assert meta["description"] == "Test skill valid-skill"


def test_deploy_skills_copies_replaces_symlinks_and_prunes_only_managed(tmp_path):
    from src.scripts.deploy_skills import MANIFEST_FILENAME, deploy_skills

    src = tmp_path / "src_skills"
    dst = tmp_path / "target_skills"
    _make_skill(src, "alpha-skill", include_cache=True)
    _make_skill(src, "beta-skill")

    # Pre-existing symlink for alpha-skill and unrelated skills that must survive
    dst.mkdir(parents=True)
    (dst / "alpha-skill").symlink_to(src / "alpha-skill")
    (dst / "cas-add-or-modify-feature").mkdir()
    (dst / "cas-add-or-modify-feature" / "SKILL.md").write_text("cas", encoding="utf-8")
    (dst / "speckit-plan").mkdir()
    (dst / "speckit-plan" / "SKILL.md").write_text("speckit", encoding="utf-8")

    summary = deploy_skills(src, dst)
    assert summary["deployed"] == ["alpha-skill", "beta-skill"]
    assert not (dst / "alpha-skill").is_symlink()
    assert (dst / "alpha-skill").is_dir()
    assert not (dst / "alpha-skill" / "__pycache__").exists()
    assert not (dst / "alpha-skill" / ".DS_Store").exists()

    manifest = json.loads((dst / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    assert manifest["skills"] == ["alpha-skill", "beta-skill"]
    assert "deployed_at" in manifest
    assert manifest["source_dir"] == str(src)

    # Remove beta-skill from source and re-deploy; only beta-skill should be pruned
    import shutil
    shutil.rmtree(src / "beta-skill")
    summary2 = deploy_skills(src, dst)
    assert summary2["pruned"] == ["beta-skill"]
    assert not (dst / "beta-skill").exists()
    assert (dst / "alpha-skill").is_dir()
    assert (dst / "cas-add-or-modify-feature" / "SKILL.md").exists()
    assert (dst / "speckit-plan" / "SKILL.md").exists()


def test_deploy_skills_dry_run_makes_no_changes(tmp_path):
    from src.scripts.deploy_skills import MANIFEST_FILENAME, deploy_skills

    src = tmp_path / "src_skills"
    dst = tmp_path / "target_skills"
    _make_skill(src, "alpha-skill")

    summary = deploy_skills(src, dst, dry_run=True)
    assert summary["deployed"] == ["alpha-skill"]
    assert summary["dry_run"] is True
    assert not dst.exists()
    assert not (dst / MANIFEST_FILENAME).exists()


def test_clean_global_deployments_removes_only_repo_symlinks(tmp_path):
    from src.scripts.deploy_skills import MANIFEST_FILENAME, clean_global_deployments

    repo_skill = tmp_path / "interview-playbook-generator" / "skills" / "resume-projection"
    repo_skill.mkdir(parents=True)
    other_skill = tmp_path / "other-repo" / "adk-cheatsheet"
    other_skill.mkdir(parents=True)

    g1 = tmp_path / "global_agents"
    g2 = tmp_path / "global_gemini"
    g1.mkdir()
    g2.mkdir()

    (g1 / "resume-projection").symlink_to(repo_skill)
    (g1 / "adk-cheatsheet").symlink_to(other_skill)
    (g1 / "real-skill").mkdir()

    (g2 / "resume-projection").symlink_to(repo_skill)
    (g2 / MANIFEST_FILENAME).write_text(json.dumps({"skills": ["copied-repo-skill"]}), encoding="utf-8")
    (g2 / "copied-repo-skill").mkdir()

    removed = clean_global_deployments(global_dirs=[g1, g2])
    removed_names = {(p.parent.name, p.name) for p in removed}

    assert ("global_agents", "resume-projection") in removed_names
    assert ("global_gemini", "resume-projection") in removed_names
    assert ("global_gemini", "copied-repo-skill") in removed_names
    assert not (g1 / "resume-projection").exists()
    assert not (g2 / "resume-projection").exists()
    assert not (g2 / "copied-repo-skill").exists()
    assert not (g2 / MANIFEST_FILENAME).exists()

    # Unrelated global skills remain untouched
    assert (g1 / "adk-cheatsheet").is_symlink()
    assert (g1 / "real-skill").is_dir()


def test_deploy_skills_cli_end_to_end(tmp_path):
    res = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "src" / "scripts" / "deploy_skills.py"),
            "--target-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"CLI failed:\n{res.stdout}\n{res.stderr}"
    deployed_dirs = [p for p in tmp_path.iterdir() if p.is_dir()]
    assert len(deployed_dirs) >= 30
    assert all(not p.is_symlink() for p in deployed_dirs)
