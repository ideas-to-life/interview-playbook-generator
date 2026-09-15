# CLAUDE.md

Project memory for Claude Code. Loaded automatically when a session starts in this directory. For the full project context see [`README.md`](README.md), [`RUNBOOK.md`](RUNBOOK.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), and [`AGENTS.md`](AGENTS.md). For approved design specs see [`specs/`](specs/).

The `AGENTS.md` file holds the vendor-neutral operating instructions that also apply to you. This file adds Claude-Code-specific context — Skills invocation, lint discipline, snapshot tests, and what to do when working *in* the repo (editing Skills, writing fixtures, adding OKF nodes).


## Current state

- **Status:** v0.6 (Sprint 6 & V3.2 Contract Alignment) Executive Narrative, Personal Brand Engine, Upwork Proposal Projection, Archetype Classifier, Gap Classifier, Market Evaluation, and opportunity-scoped output directories (`out/<target-slug>/`).
- **Approved artefacts:** `README.md`, `RUNBOOK.md`, `ARCHITECTURE.md`, `AGENTS.md`, `specs/003-upwork-proposal-refinement/`, `specs/004-upwork-proposal-v32-alignment/`.
- **Branch:** `003-upwork-proposal-refinement` / `main`.

## Claude Code–specific context

### You are the runtime

This project's Skills do not call an LLM API. The user invokes each Skill as `/skill <name>` inside Claude Code (or in Antigravity). You do the work guided by the Skill's `SKILL.md`. There is no orchestrator code — the `playbook-orchestrator` Skill guides the user; you follow its instructions when invoked as that Skill.

### Invocation shape

When the user invokes a Skill, you:

1. Read the Skill's `SKILL.md` carefully.
2. Confirm the input set exists (config, upstream bundle nodes, or `out/<target-slug>/runtime/opportunity-analysis.yaml`).
3. Run the lint pass on your output before writing.
4. Write the output subtree per the Skill's contract (`out/okf/` for canonical nodes, `out/<target-slug>/` for opportunity-scoped context & views).
5. Update `okf/log.md` with a one-line entry.

### Snapshot & Contract tests

When extending a Skill, regenerate its golden fixture under `tests/golden/<skill>/` or test suite in `tests/test_upwork_proposal_generator.py`. The test will structural-diff or validate your output against the canonical contract.

```bash
pytest tests/ -v
```

## Useful commands

```bash
# Run the 23-step pipeline orchestrator
/skill playbook-orchestrator

# Run full test suite (154 tests)
pytest tests/ -v

# Run independent Upwork proposal validator
python3 scripts/upwork_validator.py

# Run offline playbook fixture generator
python3 scripts/generate_upwork_biz_systems_playbook.py
```

