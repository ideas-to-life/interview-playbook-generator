# CLAUDE.md

Project memory for Claude Code and Antigravity agents. Loaded automatically when a session starts in this directory. For the full project context see [`README.md`](README.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), and [`AGENTS.md`](AGENTS.md). For approved design specs see [`docs/superpowers/specs/`](docs/superpowers/specs/).

The `AGENTS.md` file holds the vendor-neutral operating instructions that also apply to you. This file adds agent-specific context — Skills invocation, lint discipline, snapshot tests, and what to do when working *in* the repo (editing Skills, writing fixtures, adding OKF nodes).

## Current state

- **Status:** v0.6 (Sprint 6) Runtime Intelligence, Market Evaluation & Automated Ingestion active with opportunity-scoped output directories (`out/<target-slug>/`).
- **Approved artefacts:** `requirements-spec.md`, `spec-refinements.md`, `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`, `docs/superpowers/specs/2026-07-30-sprint-3-design.md`, `docs/superpowers/specs/2026-07-31-sprint-4-design.md`, `docs/superpowers/specs/2026-07-31-sprint-5-design.md`, `docs/superpowers/specs/2026-08-03-opportunity-scoped-outputs-design.md`, `docs/superpowers/specs/2026-08-14-mind-palace-portfolio-ingestion-spec.md`, `README.md`, `ARCHITECTURE.md`, `AGENTS.md`.
- **Branch:** `feat/mind-palace-portfolio-ingestion`.

## Agent-specific context

### You are the runtime

This project's Skills do not call an LLM API. The user invokes each Skill as `/skill <name>` inside Claude Code or Antigravity. You do the work guided by the Skill's `SKILL.md`. There is no orchestrator code — the `playbook-orchestrator` Skill guides the pipeline; you follow its 23-step instructions when invoked as that Skill.

### Invocation shape

When the user invokes a Skill, you:

1. Read the Skill's `SKILL.md` carefully.
2. Confirm the input set exists (`config/config.yaml`, upstream bundle nodes, or `out/<target-slug>/runtime/opportunity-analysis.yaml`).
3. Run the lint pass on your output before writing.
4. Write the output subtree per the Skill's contract (`out/okf/` for canonical nodes, `out/<target-slug>/` for opportunity-scoped context & views, `evaluation/opportunities/` for evaluations).
5. Update `out/okf/log.md` with a clean entry.

### Snapshot tests & verification

When extending a Skill or script, regenerate or update its golden fixture under `tests/golden/<skill>/` and run pytest:

```bash
pytest tests/ -v
```

## Useful commands

```bash
# Run the 23-step pipeline orchestrator
/skill playbook-orchestrator

# Run automated portfolio ingestion script
python3 scripts/ingest_portfolio.py

# Run full test suite
pytest tests/ -v
```
