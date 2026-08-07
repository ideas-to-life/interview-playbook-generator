# Architecture

High-level architecture of the Career Projection Platform (Interview Playbook Generator v0.5). For approved design specs, see [`docs/superpowers/specs/`](docs/superpowers/specs/).

## What this system is

A pipeline that turns raw candidate portfolio material (CV, LinkedIn export, slide decks, architecture docs, publications, JD, recruiter message) into a **structured knowledge graph** of the candidate's career, and from that graph produces multiple tailored **executive communication projections** (Resumes, Cover Letters, LinkedIn Profiles, Briefings, Playbooks).

Four-Layer Pipeline Architecture:

- **Knowledge Layer** (canonical; stored in `out/okf/`): Stores persistent canonical career knowledge (`Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `ExecutiveIdentity`, `VoiceProfile`, `PositioningStatements`, `NarrativeLibrary`, `StoryLibrary`, `MessagingLibrary`, `Theme`, `Narrative`). Never modified by projections and shared across all target opportunities.
- **Runtime Layer** (execution context; stored in `out/<target-slug>/runtime/`): Stores derived opportunity analysis (`opportunity-analysis.yaml`), projection validation reports (`projection-validation-report.yaml`), and brand validation reports (`brand-validation-report.yaml`).
- **Coaching Layer** (derived strategy; stored in `okf/`): Computes opportunity-specific interview strategy (`InterviewStrategy`) and gap analysis (`KnowledgeGap`).
- **Projection Layer** (presentation views; stored in `out/<target-slug>/`): Generates read-only executive communication projections (`resume-executive.md`, `resume-ats.md`, `resume-recruiter.md`, `cover-letter.md`, `linkedin-profile.md`, `playbook.md`, `interview-cheatsheet.md`, `executive-brief.md`, `opportunity-alignment.md`).

The load-bearing principles:
1. Introductory prose and executive voice are established canonically in `okf/` and adapted by projections rather than independently generated.
2. Opportunity-specific execution context and views are scoped per target opportunity under `out/<target-slug>/` (derived from `target_opportunity.source`), preventing runs for different job opportunities from overwriting each other.

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
| **Runtime** | `opportunity-analyzer` | Generates shared execution context at `out/<target-slug>/runtime/opportunity-analysis.yaml`. |
| **Coaching** | `interview-strategy-generator` | Computes opportunity strategy and story-to-question mapping. |
| **Coaching** | `knowledge-gaps` | Pre-assembly evaluation gate assessing bundle against target role. |
| **Projection**| `projection-registry` | Orchestrates pluggable projection contracts into `out/<target-slug>/`. |
| **Projection**| `resume-projection` | Generates Executive, ATS, and Recruiter resume variants in `out/<target-slug>/`. |
| **Projection**| `cover-letter-projection` | Generates 1-page executive cover letter at `out/<target-slug>/cover-letter.md`. |
| **Projection**| `linkedin-projection` | Generates LinkedIn profile optimization at `out/<target-slug>/linkedin-profile.md`. |
| **Projection**| `opportunity-alignment-view` | Generates requirement alignment view at `out/<target-slug>/opportunity-alignment.md`. |
| **Projection**| `executive-brief-view` | Generates 10-minute briefing at `out/<target-slug>/executive-brief.md`. |
| **Projection**| `playbook-assembler` | Generates `out/<target-slug>/playbook.md` and `out/<target-slug>/interview-cheatsheet.md`. |
| **Runtime** | `projection-validator` | Evaluates evidence traceability & ATS coverage (`out/<target-slug>/runtime/projection-validation-report.yaml`). |
| **Runtime** | `brand-validator` | Evaluates cross-projection brand alignment & voice consistency (`out/<target-slug>/runtime/brand-validation-report.yaml`). |


## Architecture Diagram

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
    RL["⚡ 2. Runtime Layer (out/runtime/)<br/><i>Opportunity Context & Target Priorities</i>"]:::runtimeStyle
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

### Detailed 4-Layer Skill Data Flow

```mermaid
flowchart TD
    subgraph S0["📥 Input Ingestion"]
        direction LR
        IN_CV["Portfolio Sources<br/>(CV, LinkedIn, Architecture Docs)"]
        IN_JD["Target Opportunity Spec<br/>(Job Description / Recruiter Spec)"]
    end

    subgraph S1["🧠 1. Knowledge Layer (Canonical Graph in okf/)"]
        direction TB
        S1_ING["portfolio-ingestor"] --> S1_ANA["portfolio-analyzer"]
        S1_ANA --> S1_ACH["achievement-extractor"]
        S1_ACH --> S1_EVD["evidence-card-generator"]
        S1_EVD --> S1_CAP["capability-extractor & signature-curator"]
        S1_ACH --> S1_THM["signature-theme-miner"]
        S1_THM --> S1_IDN["executive-identity-generator"]
        S1_IDN --> S1_NAR["narrative-engine & story-engine"]
    end

    subgraph S2["⚡ 2. Runtime Layer (Derived Context in out/runtime/)"]
        S2_OPP["opportunity-analyzer<br/><i>Emits opportunity-analysis.yaml</i>"]
    end

    subgraph S3["🎯 3. Coaching Layer (Derived Strategy in okf/)"]
        S3_STR["interview-strategy-generator"]
        S3_GAP["knowledge-gaps (Pre-assembly Gate)"]
    end

    subgraph S4["📄 4. Projection Layer (Presentation Views in out/)"]
        direction TB
        S4_REG["projection-registry"]
        subgraph S4_VIEWS["Projections & Presentation Suite"]
            direction LR
            V_RES["resume-projection<br/><i>(Executive, ATS, Recruiter)</i>"]
            V_COV["cover-letter-projection"]
            V_LKD["linkedin-projection"]
            V_ALI["opportunity-alignment-view"]
            V_BRF["executive-brief-view"]
            V_PBK["playbook-assembler<br/><i>(Playbook & Cheat Sheet)</i>"]
        end
        S4_REG --> V_RES
        S4_REG --> V_COV
        S4_REG --> V_LKD
        S4_REG --> V_ALI
        S4_REG --> V_BRF
        S4_REG --> V_PBK
    end

    subgraph S5["🛡️ Quality Validation Gates"]
        S5_PV["projection-validator"]
        S5_BV["brand-validator"]
    end

    IN_CV --> S1_ING
    IN_JD --> S2_OPP
    S1_NAR --> S2_OPP
    S1_NAR --> S3_STR
    S2_OPP --> S3_STR
    S1_NAR --> S3_GAP
    S2_OPP --> S3_GAP
    S1_NAR --> S4_REG
    S2_OPP --> S4_REG
    S3_STR --> S4_REG
    S4_VIEWS --> S5_PV
    S4_VIEWS --> S5_BV
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
