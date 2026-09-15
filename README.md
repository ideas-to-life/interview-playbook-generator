# Career Projection Platform (Interview Playbook Generator)

Generate high-quality executive communication artefacts (Resumes, Cover Letters, LinkedIn Profiles, Briefings, and Interview Playbooks) from a candidate's portfolio and career knowledge — grounded in evidence, adapted to the target opportunity, and structured as a reusable knowledge graph.

<!-- BEGIN AUTO-GENERATED ARCHITECTURE DIAGRAM -->
### System Architecture Overview

```mermaid
flowchart TD
    classDef inputStyle fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
    classDef knowledgeStyle fill:#0369A1,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC
    classDef runtimeStyle fill:#B45309,stroke:#FBBF24,stroke-width:2px,color:#F8FAFC
    classDef coachingStyle fill:#6D28D9,stroke:#C084FC,stroke-width:2px,color:#F8FAFC
    classDef projectionStyle fill:#15803D,stroke:#4ADE80,stroke-width:2px,color:#F8FAFC
    classDef validateStyle fill:#334155,stroke:#94A3B8,stroke-width:2px,color:#F8FAFC

    IN["📥 Candidate Portfolio & Target Role Spec"]:::inputStyle
    KL["🧠 1. Knowledge Layer (okf/)<br/><i>Canonical Knowledge Graph & Executive Identity</i>"]:::knowledgeStyle
    RL["⚡ 2. Runtime Layer (out/<target-slug>/runtime/)<br/><i>Opportunity Context & Target Priorities</i>"]:::runtimeStyle
    CL["🎯 3. Coaching Layer (okf/)<br/><i>Opportunity-Aware Strategy & Gap Analysis</i>"]:::coachingStyle
    PL["📄 4. Projection Layer (out/)<br/><i>Resumes, Briefings, Cover Letter & Playbook</i>"]:::projectionStyle
    VG["🛡️ Quality & Brand Validation Gates<br/><i>Projection & Brand Alignment Verification</i>"]:::validateStyle

    IN --> KL
    IN --> RL
    KL --> RL
    KL --> CL
    RL --> CL
    KL --> PL
    RL --> PL
    CL --> PL
    PL --> VG
```
<!-- END AUTO-GENERATED ARCHITECTURE DIAGRAM -->

## Status

**v0.6 (Sprint 6 & V3.2 Contract Alignment) Executive Narrative, Personal Brand Engine & Upwork Proposal Projection active.** All 25+ Skills, canonical Executive Identity Layer (`okf/executive-identity.md`, `okf/voice-profile.md`, `okf/positioning-statements.md`, `okf/narrative-library.md`, `okf/story-library.md`, `okf/messaging-library.md`), Projection SDK & Registry, Upwork Proposal Projection Engine (`upwork-proposal`), Archetype & Gap Classifiers, Brand Validator, and target opportunity slug scoping (`out/<target-slug>/`) are fully tested (154/154 tests passing) and active.

## How it works (one paragraph)

A local-first pipeline of **Agent Skills** in this repo reads a YAML config (`config/config.yaml`) plus raw portfolio sources (CV, LinkedIn, slide decks, architecture docs, etc.), runs Skills that progressively structure the candidate's career into an **OKF (Open Knowledge Format) v0.2** knowledge graph on disk (`out/okf/`), establishes a canonical Executive Identity Layer, runs an opportunity analyzer producing shared execution context (`out/<target-slug>/runtime/opportunity-analysis.yaml`), and orchestrates registered projection Skills (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `executive-brief-view`, `opportunity-alignment-view`, `upwork-proposal`, `playbook-assembler`) to produce read-only presentation views in `out/<target-slug>/`.

## Architecture at a glance

- **Five explicit layers (v0.6):**
  - *Knowledge Layer* (canonical, in `out/okf/`): persistent, immutable career concepts (`Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `ExecutiveIdentity`, `VoiceProfile`, `PositioningStatements`, `NarrativeLibrary`, `StoryLibrary`, `MessagingLibrary`). Shared across all target opportunities.
  - *Runtime Intelligence Layer* (derived execution context, in `out/<target-slug>/runtime/`): shared opportunity analysis (`opportunity-analysis.yaml`), qualification context (`upwork-qualification.yaml`), archetype analysis (`archetype-analysis.yaml`), gap analysis (`gap-analysis.yaml`), opportunity fit report (`opportunity-fit-report.yaml`), projection strategy (`projection-strategy.yaml`), projection validation report (`projection-validation-report.yaml`), and brand validation report (`brand-validation-report.yaml`).
  - *Coaching Layer* (derived strategy, in `okf/`): opportunity-aware interview strategy (`InterviewStrategy`) & pre-assembly knowledge gap analysis (`KnowledgeGap`).
  - *Projection & Validation Layer* (presentation views & reports, in `out/<target-slug>/`): read-only executive communication projections (`resume-executive.md`, `resume-ats.md`, `resume-recruiter.md`, `cover-letter.md`, `linkedin-profile.md`, `playbook.md`, `interview-cheatsheet.md`, `executive-brief.md`, `opportunity-alignment.md`, `upwork-qualification-report.md`, `upwork-screening-answers.md`, `upwork-work-samples.md`, `upwork-evidence-gaps.md`).
  - *Evaluation Layer* (learning & market feedback, in `evaluation/opportunities/`): market feedback evaluation reports (`<target-slug>-evaluation.yaml`).
- **Opportunity-Scoped Output Subtrees (`out/<target-slug>/`):** Opportunity-specific outputs (runtime context, validation reports, presentation projections) are saved under `out/<target-slug>/` (auto-derived from `target_opportunity.source` in `config/config.yaml`), persisting historic runs across different job opportunities without overwriting.
- **Pluggable Projection SDK & Registry:** Projections implement a standardized contract and register with `projection-registry`.
- **Quality & Evidence discipline:** Every claim in the bundle is tagged `[evidence | inference | recommendation | assumption]`; every concept carries source attribution (`[^source-id]`). The system never fabricates metrics, budgets, or responsibilities.

## 📖 Quickstart & Documentation

For complete step-by-step setup, configuration, execution instructions, and user guides, see:
* [`RUNBOOK.md`](RUNBOOK.md) — Operational execution guide for new users and AI agents.
* [`AGENTS.md`](AGENTS.md) — Vendor-neutral operating instructions and hard rules.
* [`ARCHITECTURE.md`](ARCHITECTURE.md) — Detailed 5-layer pipeline architecture and data flow schemas.

