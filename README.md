# Career Projection Platform (Interview Playbook Generator)

Generate high-quality executive communication artefacts (Resumes, Cover Letters, LinkedIn Profiles, Briefings, and Interview Playbooks) from a candidate's portfolio and career knowledge — grounded in evidence, adapted to the target opportunity, and structured as a reusable knowledge graph.

## Status

**v0.4 (Sprint 4) Career Projection Platform Active.** All 21 Skills, four-layer architecture (Knowledge, Runtime, Coaching, Projection), Projection SDK & Registry, and full projection suite (`out/resume-*.md`, `out/cover-letter.md`, `out/linkedin-profile.md`, `out/playbook.md`, `out/executive-brief.md`, `out/opportunity-alignment.md`, `out/runtime/projection-validation-report.yaml`) are tested and active.

## How it works (one paragraph)

A local-first pipeline of **Claude Skills** in this repo reads a YAML config plus raw portfolio sources (CV, LinkedIn, slide decks, architecture docs, etc.), runs Skills that progressively structure the candidate's career into an **OKF (Open Knowledge Format) v0.2** knowledge graph on disk (`okf/`), runs an opportunity analyzer producing shared execution context (`out/runtime/opportunity-analysis.yaml`), and orchestrates registered projection Skills (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `executive-brief-view`, `opportunity-alignment-view`, `playbook-assembler`) to produce read-only presentation views in `out/`.

## Architecture at a glance

- **Four explicit layers (v0.4):**
  - *Knowledge Layer* (canonical, in `okf/`): persistent, immutable career concepts (`Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `Theme`, `Narrative`).
  - *Runtime Layer* (derived execution context, in `out/runtime/`): shared opportunity analysis (`opportunity-analysis.yaml`) and projection validation report (`projection-validation-report.yaml`).
  - *Coaching Layer* (derived strategy, in `okf/`): opportunity-aware strategy & knowledge gaps.
  - *Projection Layer* (presentation views, in `out/`): read-only executive communication projections (`resume-executive.md`, `resume-ats.md`, `resume-recruiter.md`, `cover-letter.md`, `linkedin-profile.md`, `playbook.md`, `interview-cheatsheet.md`, `executive-brief.md`, `opportunity-alignment.md`).
- **Pluggable Projection SDK & Registry:** Projections implement a standardized contract and register with `projection-registry`.
- **Quality discipline:** Every claim in the bundle is tagged `[evidence | inference | recommendation | assumption]`; every concept carries source attribution. The system never fabricates metrics, budgets, or responsibilities.

## v0.4 (Sprint 4) — Career Projection Platform

Pure additive release over v0.3. Adds:

- **Target Opportunity Analyzer (`opportunity-analyzer`)**: Generates shared execution context at `out/runtime/opportunity-analysis.yaml` once per pipeline run.
- **Projection SDK & Projection Registry (`projection-registry`)**: Standardised contract for pluggable, read-only projection generators.
- **Resume Projection (`resume-projection`)**: Generates Executive, ATS, and Recruiter resume variants (`out/resume-executive.md`, `out/resume-ats.md`, `out/resume-recruiter.md`).
- **Cover Letter Projection (`cover-letter-projection`)**: Generates 1-page executive cover letter (`out/cover-letter.md`).
- **LinkedIn Projection (`linkedin-projection`)**: Generates LinkedIn profile optimization (`out/linkedin-profile.md`).
- **Projection Validator (`projection-validator`)**: Automated validation report assessing evidence coverage, capability alignment, ATS vocabulary density, and readability (`out/runtime/projection-validation-report.yaml`).

See the [Sprint 4 design spec](docs/superpowers/specs/2026-07-31-sprint-4-design.md) for the full contract.
