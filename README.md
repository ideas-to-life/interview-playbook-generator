# Interview Playbook Generator

Generate high-quality interview preparation from a candidate's portfolio and career knowledge — grounded in evidence, adapted to the role, and structured as a reusable knowledge graph.

## Status

**v0.3 (Sprint 3) Implementation Complete.** All 15 Skills, three-layer architecture (Knowledge, Coaching, Projection), 27 OKF bundle nodes, and view outputs (`out/playbook.md`, `out/interview-cheatsheet.md`, `out/executive-brief.md`, `out/opportunity-alignment.md`) are tested and active.

## How it works (one paragraph)

A local-first pipeline of **Claude Skills** in this repo reads a YAML config plus raw portfolio sources (CV, LinkedIn, slide decks, architecture docs, etc.), runs Skills that progressively structure the candidate's career into an **OKF (Open Knowledge Format) v0.2** knowledge graph on disk, and view Skills generate human-readable Interview Playbooks, Executive Briefs, and Opportunity Alignment views from the graph. The OKF bundle is the primary artefact — the views are projections of it.

## Repository contents

- `requirements-spec.md` — the initial product requirements and scope (approved baseline).
- `spec-refinements.md` — refinement notes applied to the baseline.
- `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md` — the approved v0.2 design spec.
- `docs/superpowers/specs/2026-07-30-sprint-3-design.md` — the approved v0.3 design spec (Executive Coaching & Knowledge Intelligence).
- `docs/superpowers/plans/2026-07-30-sprint-3-implementation.md` — the Sprint 3 implementation plan.
- `config/config.example.yaml` — template for declaring candidate inputs, target opportunity, and output paths.

## Architecture at a glance

- **Primary artefact:** an OKF v0.2 bundle (a directory of `.md` files with YAML frontmatter, cross-linked as a knowledge graph). Spec: [`GoogleCloudPlatform/knowledge-catalog/okf`](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf).
- **Three explicit layers (v0.3):**
  - *Knowledge Layer* (canonical, in `okf/`): persistent career concepts.
  - *Coaching Layer* (derived, in `okf/`): opportunity-aware strategy & knowledge gaps, regenerated every run.
  - *Projection Layer* (views, in `out/`): presentation artefacts (`playbook.md`, `executive-brief.md`, `opportunity-alignment.md`).
- **Runtime:** Claude Code or Antigravity. Each Skill is a `SKILL.md` file the user invokes; the agent does the work guided by the skill's instructions. No Skill calls an LLM API directly.
- **State between Skills:** the OKF bundle on disk. Idempotent re-runs.
- **Configuration:** a YAML file at `config/config.yaml`, with CLI overrides and interactive prompts as fallbacks for missing values.
- **Quality discipline:** every claim in the bundle is tagged `[evidence | inference | recommendation | assumption]`; every concept carries source attribution. The Skills never invent projects, metrics, team sizes, budgets, technologies, or responsibilities — they stop and prompt the user when source is missing.

## v0.3 (Sprint 3) — Executive Coaching & Knowledge Intelligence

Pure additive release over v0.2. Adds:

- 3 new canonical concept types: `ExecutiveBehaviourProfile`, `Capability`, `SignatureAchievements`.
- 6 new `EvidenceCard` fields: `conversation_hook`, `transition_sentence`, `organisational_impact`, `strategic_significance`, `recency`, `duplicates_of`.
- 3 new producer Skills: `behaviour-profile-generator`, `capability-extractor`, `signature-achievements-curator`.
- 2 new view Skills: `executive-brief-view`, `opportunity-alignment-view`.
- 2 extended Skills: `evidence-card-generator` (new fields + duplicate-detection pass), `interview-strategy-generator` (Opportunity Analysis + Story→Question mapping).

Architecture: three explicit layers (Knowledge / Coaching / Projection). The OKF bundle stores only canonical career knowledge. Opportunity-specific interpretation is computed at view time. Sprint 4 projections (Resume, Cover Letter, LinkedIn, Executive Biography, Consulting Proposal) will consume the same canonical bundle without bundle changes.

See the [Sprint 3 design spec](docs/superpowers/specs/2026-07-30-sprint-3-design.md) for the full contract.

