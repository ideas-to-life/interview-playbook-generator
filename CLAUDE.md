# CLAUDE.md

Project memory for Claude Code. Loaded automatically when a session starts in this directory. For the full project context see [`README.md`](README.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), and [`AGENTS.md`](AGENTS.md). For approved design specs see [`docs/superpowers/specs/`](docs/superpowers/specs/).

The `AGENTS.md` file holds the vendor-neutral operating instructions that also apply to you. This file adds Claude-Code-specific context — Skills invocation, lint discipline, snapshot tests, and what to do when working *in* the repo (editing Skills, writing fixtures, adding OKF nodes).

## Current state

- **Status:** v0.5 (Sprint 5) Executive Narrative & Personal Brand Engine implementation complete.
- **Approved artefacts:** `requirements-spec.md`, `spec-refinements.md`, `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`, `docs/superpowers/specs/2026-07-30-sprint-3-design.md`, `docs/superpowers/specs/2026-07-31-sprint-4-design.md`, `docs/superpowers/specs/2026-07-31-sprint-5-design.md`, `docs/superpowers/plans/2026-07-31-sprint-5-implementation.md`, `README.md`, `ARCHITECTURE.md`, `AGENTS.md`.
- **Branch:** `master`.

## Claude Code–specific context

### You are the runtime

This project's Skills do not call an LLM API. The user invokes each Skill as `/skill <name>` inside Claude Code (or in Antigravity). You do the work guided by the Skill's `SKILL.md`. There is no orchestrator code — the `playbook-orchestrator` Skill guides the user; you follow its instructions when invoked as that Skill.

### Invocation shape

When the user invokes a Skill, you:

1. Read the Skill's `SKILL.md` carefully.
2. Confirm the input set exists (config, upstream bundle nodes, or `out/runtime/opportunity-analysis.yaml`).
3. Run the lint pass on your output before writing.
4. Write the output subtree per the Skill's contract.
5. Update `okf/log.md` with a one-line entry.

### Snapshot tests

When extending a Skill, regenerate its golden fixture under `tests/golden/<skill>/`. The test in `tests/test_<skill>.py` will structural-diff your output against the golden.

```
pytest tests/
```

## Useful commands

```
# Run the 17-step pipeline orchestrator
/skill playbook-orchestrator

# Run full test suite
pytest tests/ -v
```
