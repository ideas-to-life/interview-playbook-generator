#!/usr/bin/env python3
"""Deterministic copy-based deployer for repository agent skills.

Separates CAS-governed source skills (src/skills/) from deployed skill snapshots
(.agents/skills/ locally, or ~/.agents/skills globally) without symlinking into
the active git working tree.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_SOURCE_DIR = REPO_ROOT / "src" / "skills"
DEFAULT_LOCAL_TARGET = REPO_ROOT / ".agents" / "skills"
DEFAULT_GLOBAL_TARGET = Path.home() / ".agents" / "skills"
MANIFEST_FILENAME = ".interview-playbook-skills-manifest.json"
DEFAULT_REPO_MARKER = "interview-playbook-generator"


def validate_skill_md(skill_dir: Path) -> Dict[str, Any]:
    """Validates that skill_dir/SKILL.md has YAML frontmatter with name and description."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise ValueError(f"Missing SKILL.md in {skill_dir}")

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"SKILL.md missing YAML frontmatter delimiter in {skill_dir}")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"SKILL.md has unclosed YAML frontmatter in {skill_dir}")

    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML frontmatter in {skill_md}: {exc}") from exc

    if not isinstance(meta, dict):
        raise ValueError(f"YAML frontmatter in {skill_md} must be a mapping")

    name = meta.get("name")
    description = meta.get("description")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"SKILL.md missing required non-empty 'name' in {skill_md}")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"SKILL.md missing required non-empty 'description' in {skill_md}")

    return meta


def discover_skills(source_dir: Path, only: Optional[List[str]] = None) -> List[Path]:
    """Discovers valid skill subdirectories under source_dir containing SKILL.md."""
    if not source_dir.exists() or not source_dir.is_dir():
        raise FileNotFoundError(f"Skill source directory does not exist: {source_dir}")

    available: Dict[str, Path] = {}
    for entry in sorted(source_dir.iterdir(), key=lambda p: p.name):
        if entry.name.startswith(".") or entry.name == "__pycache__":
            continue
        if entry.is_dir() and (entry / "SKILL.md").is_file():
            available[entry.name] = entry

    if only is not None:
        selected: List[Path] = []
        missing: List[str] = []
        for skill_name in only:
            if skill_name in available:
                selected.append(available[skill_name])
            else:
                missing.append(skill_name)
        if missing:
            raise ValueError(f"Requested skills not found in {source_dir}: {', '.join(missing)}")
        return selected

    return list(available.values())


def _get_git_commit(repo_root: Path) -> Optional[str]:
    """Returns short git HEAD SHA if available, else None."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            return res.stdout.strip() or None
    except Exception:
        pass
    return None


def _remove_path(path: Path) -> None:
    """Removes a file, symlink, or directory tree cleanly."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def deploy_skills(
    source_dir: Path,
    target_dir: Path,
    *,
    only: Optional[List[str]] = None,
    dry_run: bool = False,
    prune: bool = True,
) -> Dict[str, Any]:
    """Validates and copies skills from source_dir into target_dir with manifest-scoped pruning."""
    skills = discover_skills(source_dir, only=only)
    for skill_dir in skills:
        validate_skill_md(skill_dir)

    deployed_names = [p.name for p in skills]
    manifest_path = target_dir / MANIFEST_FILENAME

    previous_managed: List[str] = []
    if manifest_path.is_file():
        try:
            prior_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            if isinstance(prior_data, dict) and isinstance(prior_data.get("skills"), list):
                previous_managed = [str(x) for x in prior_data["skills"]]
        except Exception as exc:
            print(f"WARNING: Failed to read prior manifest {manifest_path}: {exc}", file=sys.stderr)

    pruned_names: List[str] = []
    if prune and only is None:
        deployed_set = set(deployed_names)
        pruned_names = [name for name in previous_managed if name not in deployed_set]

    if dry_run:
        return {
            "source_dir": str(source_dir),
            "target_dir": str(target_dir),
            "deployed": deployed_names,
            "pruned": pruned_names,
            "dry_run": True,
        }

    target_dir.mkdir(parents=True, exist_ok=True)
    ignore_fn = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")

    for skill_dir in skills:
        dest = target_dir / skill_dir.name
        if dest.is_symlink() or dest.exists():
            _remove_path(dest)
        shutil.copytree(skill_dir, dest, ignore=ignore_fn)

    for stale_name in pruned_names:
        stale_path = target_dir / stale_name
        if stale_path.is_symlink() or stale_path.exists():
            _remove_path(stale_path)

    if only is not None:
        merged_skills = sorted(set(previous_managed) | set(deployed_names))
    else:
        merged_skills = sorted(deployed_names)

    manifest_data = {
        "source_dir": str(source_dir),
        "source_commit": _get_git_commit(REPO_ROOT),
        "deployed_at": datetime.now(timezone.utc).isoformat(),
        "skills": merged_skills,
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2) + "\n", encoding="utf-8")

    return {
        "source_dir": str(source_dir),
        "target_dir": str(target_dir),
        "deployed": deployed_names,
        "pruned": pruned_names,
        "dry_run": False,
    }


def default_global_skill_dirs() -> List[Path]:
    """Returns standard machine-local global skill directories."""
    home = Path.home()
    return [
        home / ".agents" / "skills",
        home / ".gemini" / "skills",
        home / ".gemini" / "antigravity" / "skills",
        home / ".gemini" / "antigravity-cli" / "skills",
    ]


def clean_global_deployments(
    global_dirs: Optional[List[Path]] = None,
    repo_marker: str = DEFAULT_REPO_MARKER,
    dry_run: bool = False,
) -> List[Path]:
    """Removes repo symlinks and manifest-managed copies from global skill directories."""
    dirs = global_dirs if global_dirs is not None else default_global_skill_dirs()
    removed: List[Path] = []

    for gdir in dirs:
        if not gdir.exists() or not gdir.is_dir():
            continue

        manifest_path = gdir / MANIFEST_FILENAME
        manifest_skills: set[str] = set()
        if manifest_path.is_file():
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                if isinstance(data, dict) and isinstance(data.get("skills"), list):
                    manifest_skills = {str(s) for s in data["skills"]}
            except Exception as exc:
                print(f"WARNING: Failed to read manifest {manifest_path}: {exc}", file=sys.stderr)

        for entry in sorted(gdir.iterdir(), key=lambda p: p.name):
            if entry.name == MANIFEST_FILENAME:
                continue
            should_remove = False
            if entry.is_symlink():
                try:
                    target = os.readlink(entry)
                    if repo_marker in target:
                        should_remove = True
                except OSError:
                    pass
            if entry.name in manifest_skills:
                should_remove = True

            if should_remove:
                removed.append(entry)
                if not dry_run:
                    _remove_path(entry)

        if manifest_path.is_file():
            removed.append(manifest_path)
            if not dry_run:
                manifest_path.unlink()

    return removed


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Deploy src/skills to local or global agent directories.")
    parser.add_argument(
        "--scope",
        choices=["local", "global"],
        default="local",
        help="Deployment target scope (default: local -> .agents/skills)",
    )
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR, help="Source skills directory")
    parser.add_argument("--target-dir", type=Path, default=None, help="Explicit target skills directory")
    parser.add_argument("--skills", nargs="+", default=None, help="Specific skill names to deploy")
    parser.add_argument("--no-prune", action="store_true", help="Do not prune removed skills from target")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without modifying disk")
    parser.add_argument(
        "--clean-global",
        action="store_true",
        help="Remove interview-playbook-generator symlinks and deployed manifests from global skill directories",
    )
    args = parser.parse_args(argv)

    if args.clean_global:
        removed = clean_global_deployments(dry_run=args.dry_run)
        prefix = "[DRY-RUN] " if args.dry_run else ""
        print(f"{prefix}Cleaned {len(removed)} global repo skill entries/manifests.")
        for p in removed:
            print(f"  - {p}")
        if args.target_dir is None and args.skills is None and "--scope" not in (argv or sys.argv[1:]):
            return 0

    target_dir = args.target_dir
    if target_dir is None:
        target_dir = DEFAULT_LOCAL_TARGET if args.scope == "local" else DEFAULT_GLOBAL_TARGET

    try:
        result = deploy_skills(
            args.source_dir,
            target_dir,
            only=args.skills,
            dry_run=args.dry_run,
            prune=not args.no_prune,
        )
    except Exception as exc:
        print(f"ERROR: Skill deployment failed: {exc}", file=sys.stderr)
        return 1

    prefix = "[DRY-RUN] " if args.dry_run else ""
    print(
        f"{prefix}Deployed {len(result['deployed'])} skills from {result['source_dir']} "
        f"to {result['target_dir']} (pruned={len(result['pruned'])})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
