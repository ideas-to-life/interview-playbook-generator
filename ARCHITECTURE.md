# Architecture

High-level architecture of the Career Projection Platform (Interview Playbook Generator v0.4). For approved design specs, see [`docs/superpowers/specs/`](docs/superpowers/specs/).

## What this system is

A pipeline that turns raw candidate portfolio material (CV, LinkedIn export, slide decks, architecture docs, publications, JD, recruiter message) into a **structured knowledge graph** of the candidate's career, and from that graph produces multiple tailored **executive communication projections** (Resumes, Cover Letters, LinkedIn Profiles, Briefings, Playbooks).

Sprint 4 introduces an explicit four-layer architecture:
- **Knowledge Layer** (canonical; stored in `okf/`): Stores persistent canonical career knowledge (`Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `Theme`, `Narrative`). Never modified by projections.
- **Runtime Layer** (execution context; stored in `out/runtime/`): Stores derived opportunity analysis (`opportunity-analysis.yaml`) and projection validation reports (`projection-validation-report.yaml`).
- **Coaching Layer** (derived strategy; stored in `okf/`): Computes opportunity-specific interview strategy (`InterviewStrategy`) and gap analysis (`KnowledgeGap`).
- **Projection Layer** (presentation views; stored in `out/`): Generates read-only executive communication projections (`resume-executive.md`, `resume-ats.md`, `resume-recruiter.md`, `cover-letter.md`, `linkedin-profile.md`, `playbook.md`, `interview-cheatsheet.md`, `executive-brief.md`, `opportunity-alignment.md`).

The load-bearing principle: the OKF bundle stores only canonical career knowledge. Opportunity analysis is executed once (`out/runtime/opportunity-analysis.yaml`) and shared across all projections.

## System diagram

```
                    ┌─────────────────────────────────────────┐
                    │  Canonical OKF Bundle (okf/)            │
                    │  • Achievements, Evidence, Capabilities │
                    │  • Behaviour Profile, Signature Themes  │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │  Target Opportunity (config/ & source) │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │  opportunity-analyzer (Skill)          │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │  out/runtime/opportunity-analysis.yaml  │
                    │  (Shared execution context, derived)    │
                    └────────────────────┬────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         ▼                               ▼                               ▼
 ┌───────────────┐               ┌───────────────┐               ┌───────────────┐
 │ resume-       │               │ cover-letter- │               │ linkedin-     │
 │ projection    │               │ projection    │               │ projection    │
 └───────┬───────┘               └───────┬───────┘               └───────┬───────┘
         │                               │                               │
         ▼                               ▼                               ▼
 ┌───────────────┐               ┌───────────────┐               ┌───────────────┐
 │ out/resume-*.md               │ out/cover-    │               │ out/linkedin- │
 │               │               │ letter.md     │               │ profile.md    │
 └───────────────┘               └───────────────┘               └───────────────┘
```

## Component responsibilities

| Layer | Component | Purpose |
|---|---|---|
| **Knowledge** | `portfolio-ingestor` | Discovers and classifies portfolio source files. |
| **Knowledge** | `portfolio-analyzer` | Builds top-level coverage map and domain breakdown. |
| **Knowledge** | `achievement-extractor` | Extracts evidence-grounded achievement nodes. |
| **Knowledge** | `evidence-card-generator` | Converts achievements into STAR Evidence Cards. |
| **Knowledge** | `behaviour-profile-generator` | Infers executive behaviour profile across core & optional dimensions. |
| **Knowledge** | `capability-extractor` | Groups evidence cards into structured capability nodes. |
| **Knowledge** | `signature-achievements-curator` | Curates signature achievements ranked on intrinsic properties. |
| **Knowledge** | `signature-theme-miner` | Mines recurring executive themes across portfolio. |
| **Knowledge** | `narrative-generator` | Formulates 30s pitch, 2m journey, and 5m executive story. |
| **Runtime** | `opportunity-analyzer` | Generates shared execution context at `out/runtime/opportunity-analysis.yaml`. |
| **Coaching** | `interview-strategy-generator` | Computes opportunity strategy and story-to-question mapping. |
| **Coaching** | `knowledge-gaps` | Pre-assembly evaluation gate assessing bundle against target role. |
| **Projection**| `projection-registry` | Orchestrates pluggable projection contracts. |
| **Projection**| `resume-projection` | Generates Executive, ATS, and Recruiter resume variants in `out/`. |
| **Projection**| `cover-letter-projection` | Generates 1-page executive cover letter at `out/cover-letter.md`. |
| **Projection**| `linkedin-projection` | Generates LinkedIn profile optimization at `out/linkedin-profile.md`. |
| **Projection**| `opportunity-alignment-view` | Generates requirement alignment view at `out/opportunity-alignment.md`. |
| **Projection**| `executive-brief-view` | Generates 10-minute briefing at `out/executive-brief.md`. |
| **Projection**| `playbook-assembler` | Generates `out/playbook.md` and `out/interview-cheatsheet.md`. |
| **Runtime** | `projection-validator` | Evaluates evidence traceability & ATS coverage (`out/runtime/projection-validation-report.yaml`). |

## OKF as the substrate

We chose OKF v0.2 as the knowledge-graph format for three reasons:
- **It is markdown:** Authorable, diffable, version-controllable.
- **It tolerates change:** OKF consumers tolerate unknown `type` values or frontmatter keys.
- **It is shared:** Machine-parseable substrate for multiple downstream projections.

## Trust and provenance

Every concept in the bundle is classified along two axes:
- **Trust tier:** `[draft]` (Unverified), `[machine-confirmed]`, `[human-reviewed]`.
- **Statement classification:** `[evidence]`, `[inference]`, `[recommendation]`, `[assumption]`.
