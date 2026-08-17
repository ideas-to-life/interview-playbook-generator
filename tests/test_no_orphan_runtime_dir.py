# tests/test_no_orphan_runtime_dir.py
"""
Regression guard for the orphan `out/runtime/` directory bug.

Sprint 6 (commit 6e0f935) migrated the runtime output path from the
top-level `out/runtime/` to the per-target-slug scheme
`out/<target-slug>/runtime/`. The migration updated Skills and the
orchestrator, but the pre-migration files at `out/runtime/` were left
behind in the working tree. They are byte-identical duplicates of the
canonical files at `out/senior-architect-vallum/runtime/`, dated
2026-08-03, and no Skill, config, or test references the orphan path
anymore.

The orphan is harmless — but its presence in the working tree is
misleading: a future reader sees a stale, dated artefact and assumes
the pipeline is broken. This test fails if the orphan reappears (for
example, by reverting the Sprint 6 path migration in a future Skill)
so the regression is caught at CI time.
"""
import os


def test_no_orphan_top_level_out_runtime_dir():
    """
    The runtime output path must be `out/<target-slug>/runtime/`.
    A bare `out/runtime/` directory is residue from before Sprint 6 and
    must not exist.
    """
    orphan = "out/runtime"
    assert not os.path.exists(orphan), (
        f"Orphan runtime directory exists at '{orphan}'. "
        "All runtime outputs must live under 'out/<target-slug>/runtime/'. "
        "If this directory reappeared, a Skill has been migrated back to "
        "the pre-Sprint-6 path. See opportunity-analyzer/SKILL.md for the "
        "current contract."
    )


def test_runtime_dirs_only_under_target_slug():
    """
    Every existing `runtime/` directory under `out/` must be nested inside
    a per-target-slug directory. No top-level or nested-elsewhere runtime
    dirs are permitted.
    """
    out_dir = "out"
    if not os.path.isdir(out_dir):
        return  # No out/ yet; nothing to check.

    # Walk `out/` and collect every `runtime/` directory at any depth.
    runtime_dirs = []
    for root, dirs, _ in os.walk(out_dir):
        if "runtime" in dirs:
            runtime_dirs.append(os.path.join(root, "runtime"))

    # Allowed shape: `out/<target-slug>/runtime/`. Reject everything else.
    for path in runtime_dirs:
        # Normalise trailing separators.
        normalised = path.rstrip(os.sep)
        parts = normalised.split(os.sep)
        # Expect exactly ['out', '<target-slug>', 'runtime'].
        assert parts[0] == "out", f"Unexpected runtime path: {path}"
        assert len(parts) == 3, (
            f"Runtime directory must be at 'out/<target-slug>/runtime/', "
            f"found '{path}'"
        )
        assert parts[2] == "runtime"


def test_out_target_slug_subdirs_have_runtime_subdir():
    """
    For each opportunity-scoped directory under `out/`, verify it has a
    `runtime/` subdirectory. This confirms every pipeline target has its
    derived execution context.
    """
    out_dir = "out"
    if not os.path.isdir(out_dir):
        return

    target_dirs = [
        d for d in os.listdir(out_dir)
        if os.path.isdir(os.path.join(out_dir, d))
        and d not in {"okf"}  # canonical bundle, not a target dir
    ]

    for target in target_dirs:
        runtime_path = os.path.join(out_dir, target, "runtime")
        if not os.path.isdir(runtime_path):
            # Some targets may be intentionally lightweight (e.g. partial
            # runs). Only fail if the directory has view artefacts but no
            # runtime context — that signals a broken pipeline.
            target_root = os.path.join(out_dir, target)
            non_runtime_artifacts = [
                f for f in os.listdir(target_root)
                if not f.startswith(".") and f != "runtime"
            ]
            assert not non_runtime_artifacts, (
                f"Target '{target}' has view artefacts but no runtime/ "
                f"context. Found: {non_runtime_artifacts}"
            )
