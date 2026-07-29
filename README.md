# Interview Playbook Generator

Generate high-quality interview preparation from a candidate's portfolio and career knowledge — grounded in evidence, adapted to the role, and structured as a reusable knowledge graph.

## Status

**Planning complete; implementation not started.** The product spec, design refinements, and approved design document are in this repo. The next step is implementation planning (turning the design into an executable plan), then the v0.1 thin slice.

## How it works (one paragraph)

A local-first pipeline of **Claude Skills** in this repo reads a YAML config plus raw portfolio sources (CV, LinkedIn, slide decks, architecture docs, etc.), runs Skills that progressively structure the candidate's career into an **OKF (Open Knowledge Format) v0.2** knowledge graph on disk, and a final assembler Skill generates a human-readable Interview Playbook view from the graph. The OKF bundle is the primary artefact — the playbook is one view of it. The same bundle can later be sliced into Recruiter / CTO / Executive / Technical packs without re-running analysis.

## Repository contents

- `requirements-spec.md` — the initial product requirements and scope (approved baseline).
- `spec-refinements.md` — refinement notes applied to the baseline (Skill 0 ingestor, role/fit split, interview strategy generator, knowledge-gap gate, thin-slice scope).
- `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md` — the approved design spec (architecture, repository layout, OKF schema, Skills, error handling, testing, success criteria).
- `config/config.example.yaml` *(pending implementation)* — template for declaring candidate inputs, target opportunity, and output paths.

## Architecture at a glance

- **Primary artefact:** an OKF v0.2 bundle (a directory of `.md` files with YAML frontmatter, cross-linked as a knowledge graph). Spec: [`GoogleCloudPlatform/knowledge-catalog/okf`](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf).
- **Runtime:** Claude Code or Antigravity. Each Skill is a `SKILL.md` file the user invokes; the agent does the work guided by the skill's instructions. No Skill calls an LLM API directly.
- **State between Skills:** the OKF bundle on disk. Idempotent re-runs.
- **Configuration:** a YAML file at `config/config.example.yaml`, with CLI overrides and interactive prompts as fallbacks for missing values.
- **Quality discipline:** every claim in the bundle is tagged `[evidence | inference | recommendation | assumption]`; every concept carries source attribution. The Skills never invent projects, metrics, team sizes, budgets, technologies, or responsibilities — they stop and prompt the user when source is missing.

## v0.1 thin slice (what ships first)

Eight Skills, run end-to-end on the example portfolio:

1. `playbook-orchestrator` — reads config, drives the pipeline.
2. `portfolio-ingestor` — discovers, classifies, and indexes source files.
3. `portfolio-analyzer` — top-level analysis and coverage map.
4. `achievement-extractor` — extracts evidence-grounded achievements.
5. `evidence-card-generator` — produces reusable STAR-shaped cards.
6. `interview-strategy-generator` — concise briefing (differentiators, narrative, objections, priorities).
7. `knowledge-gaps` *(pre-assembly gate)* — missing-evidence report; warns but does not block.
8. `playbook-assembler` — composes the human-readable playbook view.

Snapshot-tested (structural only, no LLM in tests) with golden OKF subtrees as fixtures.

## Explicitly out of scope for v0.1

The following are deferred and **must not** be added in v0.1:

- Competency ontology / catalogue
- View generator (stage-specific packs)
- Career narrative evolution
- Mock interviews / conversation simulator
- LLM-as-judge evaluation
- Company research / salary research / market intelligence
- Advanced OKF linting

The guiding principle: optimise for a working end-to-end interview pipeline, not a complete career intelligence platform.

## Path to v0.2

v0.2 adds the remaining 11 Skills as pure additive readers/producers of the OKF bundle (career timeline, competency mapper, role analyzer, fit mapper, role overlay, technical/executive Q&A, question generator, salary strategy, etc.) plus a view generator that slices the bundle into stage-specific packs. No v0.1 code is rewritten; the bundle schema is the contract.

## Current focus

- ✅ Product requirements approved (`requirements-spec.md`).
- ✅ Design refinements applied (`spec-refinements.md`).
- ✅ Design spec approved (`docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`).
- ⏭ Next: write the implementation plan and ship the v0.1 thin slice.
