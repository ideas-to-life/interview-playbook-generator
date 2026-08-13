---
name: resume-projection
description: Generates full-length executive, ATS, and recruiter resume variants from canonical OKF knowledge, Executive Identity, and shared opportunity analysis.
---

# Resume Projection

## Overview

`resume-projection` is a Projection Layer Skill. It reads the canonical OKF bundle (`okf/`, including `okf/positioning-statements.md`, `okf/messaging-library.md`, and `okf/story-library.md`), candidate config (`config/config.yaml`), and the shared execution context at `out/<target-slug>/runtime/opportunity-analysis.yaml` to generate complete, full-length, submission-ready resume projection variants in `out/<target-slug>/`:

1. **Executive Resume** (`out/<target-slug>/resume-executive.md`): Complete 2-page strategic resume covering all 10 required sections, emphasizing leadership outcomes, capability progression, and signature initiatives.
2. **ATS Resume** (`out/<target-slug>/resume-ats.md`): Complete reverse-chronological resume incorporating explicit ATS keyword density (`mandatory` and `strong` terms from `out/<target-slug>/runtime/opportunity-analysis.yaml`).
3. **Recruiter Resume** (`out/<target-slug>/resume-recruiter.md`): Complete 1-to-2 page recruiter-focused resume optimized for rapid 30-60 second scan, tailored to the target opportunity.

By default, all three variants are generated. If `config/config.yaml` specifies `projections.resume.variant`, only the selected variant is generated.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

6. **Headline Generation Priority**: The professional headline MUST prioritize:
   1. Canonical professional identity (e.g. `Enterprise Architect`)
   2. Strong target-relevant differentiators (e.g. `Transformation`, `Governance`, `AI`)
   3. Relevant target terminology (e.g. `Cloud Modernisation`)
   4. Role-specific keywords for discoverability
   Target job titles may be incorporated ONLY where they remain truthful representations of candidate archetype (e.g., `Enterprise Architect | Cloud Transformation, Governance & AI` rather than `Enterprise & Cloud Architect | CCoE Leader`).
7. **Executive Summary Hierarchy**: Executive summaries MUST preserve the candidate's career trajectory hierarchy:
   `Enterprise Architecture` -> `Transformation & Governance` -> `Cloud Modernisation` -> `AI`
   Target terminology MUST NOT displace the candidate's primary Enterprise Architecture foundation.
8. **Automatic Claim Verb Downgrading**: If a claim's verb strength exceeds evidence support (e.g. `Established` or `Led` when evidence supports `Contributed`), the generator MUST automatically down-level the verb to the evidence-supported level (e.g., "Contributed to CCoE governance" instead of "Established CCoE").
9. **Transferable Domain Framing**: Evidence from an adjacent domain MUST be expressed as *transferable experience* (e.g., "Applied Enterprise Architecture governance experience to cloud and CCoE-related initiatives") rather than converting the adjacent domain into the target domain ("Established a Cloud Centre of Excellence").
10. **Immutable Career History Metadata**: Professional Experience section headers (Employer, Job Title, Start Date, End Date, Location) MUST be rendered directly from canonical records in `okf/employment-records.yaml`. The generator MUST NOT alter dates, substitute job titles for target alignment, or reconstruct career chronologies.

## Required 10 Standard Sections

Every generated resume variant MUST include the following 10 sections:

1. **Contact Header**: Candidate name, title sub-headline, location, phone, email, LinkedIn URL, portfolio website URL.
2. **Professional Headline**: Opportunity-tailored primary positioning headline.
3. **Executive Summary**: 150-180 words adapted from canonical identity & messaging.
4. **Enterprise AI Transformation Leadership**: Key bulleted transformation capabilities.
5. **Enterprise Architecture Expertise**: Key bulleted architectural capabilities.
6. **AI Platform, Data & Governance Expertise**: Key bulleted platform & governance capabilities.
7. **Professional Experience**: Reverse-chronological career history (WPP Media, BBC Studios, British American Tobacco - R&D, BAT - Global, BAT - Americas) with signature achievements and opportunity-weighted bullets.
8. **Selected Enterprise AI Initiatives**: Detailed descriptions of CAS (Architecture-as-Code), EA4ALL (AI Accessibility), and RAI (Observability).
9. **Education & Professional Development**: MSc in Computer Science, TOGAF 9, SAFe, LeanIX.
10. **Technical Skills**: Categorized by domain (Enterprise Architecture, AI Platforms & Governance, Architecture-as-Code, Data Architecture & Integration, Observability & Evaluation, Cloud & Enterprise Software, Programming Languages).

## Execution Instructions

1. **Read Candidate Config & Opportunity Analysis**: Read `config/config.yaml` and `out/<target-slug>/runtime/opportunity-analysis.yaml`.
2. **Read Canonical OKF Knowledge**: Read `okf/positioning-statements.md`, `okf/messaging-library.md`, `okf/story-library.md`, `okf/evidence/*.md`, `okf/achievements/*.md`, `okf/capabilities/*.md`, and `okf/behaviour-profile.md`.
3. **Render Executive Resume (`out/<target-slug>/resume-executive.md`)**: Full submission-ready executive resume.
4. **Render ATS Resume (`out/<target-slug>/resume-ats.md`)**: Full ATS-optimized resume.
5. **Render Recruiter Resume (`out/<target-slug>/resume-recruiter.md`)**: Full recruiter summary resume.
6. **Append Log**: `okf/log.md`.
