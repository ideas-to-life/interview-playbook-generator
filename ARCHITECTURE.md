# Architecture

High-level architecture of the Career Projection Platform (Interview Playbook Generator v0.5). For approved design specs, see [`docs/superpowers/specs/`](docs/superpowers/specs/).

## What this system is

A pipeline that turns raw candidate portfolio material (CV, LinkedIn export, slide decks, architecture docs, publications, JD, recruiter message) into a **structured knowledge graph** of the candidate's career, and from that graph produces multiple tailored **executive communication projections** (Resumes, Cover Letters, LinkedIn Profiles, Briefings, Playbooks).

Sprint 5 introduces the canonical **Executive Identity Layer** in `okf/`:
- **Knowledge Layer** (canonical; stored in `okf/`): Stores persistent canonical career knowledge (`Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `ExecutiveIdentity`, `VoiceProfile`, `PositioningStatements`, `NarrativeLibrary`, `StoryLibrary`, `MessagingLibrary`, `Theme`, `Narrative`). Never modified by projections.
- **Runtime Layer** (execution context; stored in `out/runtime/`): Stores derived opportunity analysis (`opportunity-analysis.yaml`), projection validation reports (`projection-validation-report.yaml`), and brand validation reports (`brand-validation-report.yaml`).
- **Coaching Layer** (derived strategy; stored in `okf/`): Computes opportunity-specific interview strategy (`InterviewStrategy`) and gap analysis (`KnowledgeGap`).
- **Projection Layer** (presentation views; stored in `out/`): Generates read-only executive communication projections (`resume-executive.md`, `resume-ats.md`, `resume-recruiter.md`, `cover-letter.md`, `linkedin-profile.md`, `playbook.md`, `interview-cheatsheet.md`, `executive-brief.md`, `opportunity-alignment.md`).

The load-bearing principle: introductory prose and executive voice are established canonically in `okf/` and adapted by projections rather than independently generated.

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
| **Knowledge** | `executive-identity-generator` | Synthesises canonical Executive Identity, Voice Profile, and Positioning Statements. |
| **Knowledge** | `narrative-engine` | Generates canonical Narrative Library and Messaging Library. |
| **Knowledge** | `story-engine` | Converts Evidence Cards into single consolidated `okf/story-library.md`. |
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
| **Runtime** | `brand-validator` | Evaluates cross-projection brand alignment & voice consistency (`out/runtime/brand-validation-report.yaml`). |


## Architecture Diagram

<!-- BEGIN AUTO-GENERATED ARCHITECTURE DIAGRAM -->
### System Context & 4-Layer Pipeline Flow

```mermaid
flowchart TD
    subgraph Inputs["📥 Portfolio & Role Inputs"]
        CV["CV / LinkedIn / Portfolio Docs"]
        JD["Target Job Description"]
    end

    subgraph KnowledgeLayer["🧠 1. Knowledge Layer (okf/)"]
        PI["portfolio-ingestor"] --> PA["portfolio-analyzer"]
        PA --> AE["achievement-extractor"]
        AE --> ECG["evidence-card-generator"]
        ECG --> BPG["behaviour-profile-generator"]
        ECG --> CE["capability-extractor"]
        ECG --> SAC["signature-achievements-curator"]
        AE --> STM["signature-theme-miner"]
        STM --> EIG["executive-identity-generator"]
        EIG --> NE["narrative-engine"]
        ECG --> SE["story-engine"]
    end

    subgraph RuntimeLayer["⚡ 2. Runtime Layer (out/runtime/)"]
        OA["opportunity-analyzer"]
    end

    subgraph CoachingLayer["🎯 3. Coaching Layer (okf/)"]
        ISG["interview-strategy-generator"]
        KG["knowledge-gaps (Pre-assembly Gate)"]
    end

    subgraph ProjectionLayer["📄 4. Projection Layer (out/)"]
        PR["projection-registry"]
        PR --> RES["resume-projection"]
        PR --> CL["cover-letter-projection"]
        PR --> LI["linkedin-projection"]
        PR --> OAV["opportunity-alignment-view"]
        PR --> EBV["executive-brief-view"]
        PR --> PBA["playbook-assembler"]
        PV["projection-validator"]
        BV["brand-validator"]
    end

    Inputs --> PI
    JD --> OA
    KnowledgeLayer --> OA
    KnowledgeLayer --> ISG
    RuntimeLayer --> ISG
    KnowledgeLayer --> KG
    RuntimeLayer --> KG
    KnowledgeLayer --> ProjectionLayer
    RuntimeLayer --> ProjectionLayer
    ProjectionLayer --> PV
    ProjectionLayer --> BV
```

### OKF Knowledge Graph Schema

```mermaid
erDiagram
    SOURCE ||--o{ ACHIEVEMENT : "grounded in"
    ACHIEVEMENT ||--o{ EVIDENCE-CARD : "structured into STAR"
    EVIDENCE-CARD ||--o{ CAPABILITY : "grouped into"
    EVIDENCE-CARD ||--o{ SIGNATURE-ACHIEVEMENTS : "curated into"
    ACHIEVEMENT ||--o{ SIGNATURE-THEMES : "mined into"
    SIGNATURE-THEMES ||--|| EXECUTIVE-IDENTITY : "synthesises"
    EXECUTIVE-IDENTITY ||--|| VOICE-PROFILE : "defines"
    EXECUTIVE-IDENTITY ||--|| POSITIONING-STATEMENTS : "formulates"
    POSITIONING-STATEMENTS ||--o{ NARRATIVE-LIBRARY : "drives"
    EVIDENCE-CARD ||--|| STORY-LIBRARY : "consolidates"
    OPPORTUNITY-ANALYSIS ||--o{ INTERVIEW-STRATEGY : "shapes"
    STORY-LIBRARY ||--o{ PROJECTIONS : "adapts"
```
<!-- END AUTO-GENERATED ARCHITECTURE DIAGRAM -->
