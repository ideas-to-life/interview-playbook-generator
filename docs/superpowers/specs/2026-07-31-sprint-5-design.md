# Design Spec: Sprint 5 (v0.5) — Executive Narrative & Personal Brand Engine

**Status:** Approved Specification  
**Version:** 0.5  
**Date:** 2026-07-31  

---

## 1. Objective & Vision

Transform the Career Projection Platform into a **Career Intelligence Platform** that maintains a single, consistent executive voice and positioning across every projection while remaining 100% evidence-backed and opportunity-aware.

Sprint 5 eliminates brand drift and introductory language duplication by introducing the **Executive Identity Layer** in the canonical `okf/` bundle:
1. **Executive Identity (`okf/executive-identity.md`)**: Canonical positioning, leadership, transformation, AI, consulting philosophies, and professional values.
2. **Voice Profile (`okf/voice-profile.md`)**: Reusable tone guidelines (calm, collaborative, executive) and vocabulary rules (encouraged vs. prohibited marketing hype).
3. **Positioning Statements (`okf/positioning-statements.md`)**: Canonical statement variants (Executive, Advisory, Technical Executive).
4. **Narrative Library (`okf/narrative-library.md`)**: Canonical journeys (Career, Transformation, AI, Leadership, Architecture).
5. **Story Library (`okf/story-library.md`)**: Single consolidated library converting Evidence Cards into reusable executive stories (Situation, Challenge, Decision, Actions, Outcome, Business Value, Hook, Transition).
6. **Messaging Library (`okf/messaging-library.md`)**: Reusable 30s pitch, 2m introduction, career summary, philosophy blocks.
7. **Brand & Narrative Validator (`brand-validator`)**: Evaluates cross-projection voice consistency, positioning alignment, and evidence traceability (`out/runtime/brand-validation-report.yaml`).

---

## 2. Architecture & Knowledge Flow

```
                      ┌────────────────────────────────────────┐
                      │  Evidence Cards & Capabilities         │
                      │  Signature Achievements & Themes       │
                      └───────────────────┬────────────────────┘
                                          │
                                          ▼
                      ┌────────────────────────────────────────┐
                      │  EXECUTIVE IDENTITY LAYER (okf/)       │
                      │  • executive-identity.md               │
                      │  • voice-profile.md                    │
                      │  • positioning-statements.md           │
                      │  • narrative-library.md                │
                      │  • story-library.md                    │
                      │  • messaging-library.md                │
                      └───────────────────┬────────────────────┘
                                          │
                                          ▼
                      ┌────────────────────────────────────────┐
                      │  Runtime Context & Opportunity Analysis│
                      │  (out/runtime/opportunity-analysis.yaml)│
                      └───────────────────┬────────────────────┘
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         │                                │                                │
         ▼                                ▼                                ▼
 ┌───────────────┐                ┌───────────────┐                ┌───────────────┐
 │ resume-       │                │ cover-letter- │                │ linkedin-     │
 │ projection    │                │ projection    │                │ projection    │
 └───────┬───────┘                └───────┬───────┘                └───────┬───────┘
         │                                │                                │
         ▼                                ▼                                ▼
 ┌───────────────┐                ┌───────────────┐                ┌───────────────┐
 │ out/resume-*.md                │ out/cover-    │                │ out/linkedin- │
 │               │                │ letter.md     │                │ profile.md    │
 └───────────────┘                └───────────────┘                └───────────────┘
```

### Knowledge Flow:
`Evidence` ➔ `Achievements` ➔ `Capabilities` ➔ `Themes` ➔ `Executive Identity` ➔ `Narratives & Stories` ➔ `Runtime Opportunity Analysis` ➔ `Projections`

---

## 3. Canonical Concept Schemas

### 3.1 `ExecutiveIdentity` (`okf/executive-identity.md`)
```yaml
type: ExecutiveIdentity
title: "Executive Identity & Positioning"
description: "Canonical executive identity model for Alexandre Franco."
generated: { by: "executive-identity-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: cv-2024
    resource: evidence/resume-profile/Alexandre Franco Resume.pdf
    title: Alexandre Franco Resume
```
- **Sections**: Executive Positioning, Leadership Philosophy, Transformation Philosophy, AI Philosophy, Consulting Philosophy, Professional Values.

### 3.2 `VoiceProfile` (`okf/voice-profile.md`)
```yaml
type: VoiceProfile
title: "Executive Voice Profile"
description: "Tone, vocabulary, and communication guidelines."
generated: { by: "executive-identity-generator", at: "<ISO-8601>" }
status: draft
```
- **Sections**: Core Tone (calm, collaborative, executive), Encouraged Vocabulary (evidence, outcomes, clarity, architecture-as-code), Prohibited Vocabulary (buzzwords, marketing hype, ungrounded claims).

### 3.3 `PositioningStatements` (`okf/positioning-statements.md`)
```yaml
type: PositioningStatements
title: "Canonical Positioning Statements"
description: "Reusable positioning statement variants."
generated: { by: "executive-identity-generator", at: "<ISO-8601>" }
status: draft
```
- **Sections**: Executive Variant, Advisory Variant, Technical Executive Variant.

### 3.4 `NarrativeLibrary` (`okf/narrative-library.md`)
```yaml
type: NarrativeLibrary
title: "Canonical Narrative Library"
description: "Core professional journeys."
generated: { by: "narrative-engine", at: "<ISO-8601>" }
status: draft
```
- **Sections**: Career Journey, Transformation Journey, AI Journey, Leadership Journey, Architecture Journey.

### 3.5 `StoryLibrary` (`okf/story-library.md`)
```yaml
type: StoryLibrary
title: "Canonical Executive Story Library"
description: "Single consolidated library of evidence-backed executive stories."
generated: { by: "story-engine", at: "<ISO-8601>" }
status: draft
```
- **Sections**: Consolidated list of stories formatted with: Situation, Challenge, Decision, Actions, Outcome, Business Value, Conversation Hook, Transition Sentence.

### 3.6 `MessagingLibrary` (`okf/messaging-library.md`)
```yaml
type: MessagingLibrary
title: "Canonical Messaging Library"
description: "Reusable messaging blocks across projections."
generated: { by: "narrative-engine", at: "<ISO-8601>" }
status: draft
```
- **Sections**: 30-Second Introduction, 2-Minute Executive Introduction, Career Summary Block, Core Philosophy Blocks.

---

## 4. Producer Skills

1. `executive-identity-generator` (`skills/executive-identity-generator/SKILL.md`): Synthesises `okf/executive-identity.md`, `okf/voice-profile.md`, and `okf/positioning-statements.md`.
2. `narrative-engine` (`skills/narrative-engine/SKILL.md`): Generates `okf/narrative-library.md` and `okf/messaging-library.md`.
3. `story-engine` (`skills/story-engine/SKILL.md`): Converts Evidence Cards into consolidated `okf/story-library.md`.

---

## 5. Projection Integration

All projections adapt introductory text directly from the canonical Executive Identity layer:
- `resume-projection`: Consumes `Executive Variant` from `positioning-statements.md` & `Career Summary Block` from `messaging-library.md`.
- `cover-letter-projection`: Consumes `30-Second Introduction` from `messaging-library.md` & stories from `story-library.md`.
- `linkedin-projection`: Consumes `About Section` & `Headlines` from `executive-identity.md` and `positioning-statements.md`.
- `executive-brief-view`: Consumes `2-Minute Introduction` & `Top 3 Stories` from `messaging-library.md` and `story-library.md`.
- `playbook-assembler`: Consumes stories from `story-library.md` and narrative journeys from `narrative-library.md`.

---

## 6. Brand & Narrative Validator (`brand-validator`)

Generates `out/runtime/brand-validation-report.yaml`:
- **Voice & Tone Consistency Score**: % alignment with `okf/voice-profile.md`.
- **Positioning Alignment Score**: Checks if introductory text across projections derives from `okf/positioning-statements.md`.
- **Evidence Traceability**: % of narrative claims backed by `okf/evidence/`.
- **Story Reuse Score**: Evaluates story asset reuse across written projections and interview materials.

---

## 7. Project Structure

```
config/
  config.yaml                            # Updated for v0.5
  config.example.yaml

skills/
  executive-identity-generator/SKILL.md  # FR-1, FR-2, FR-5
  narrative-engine/SKILL.md              # FR-3, FR-8
  story-engine/SKILL.md                  # FR-4
  brand-validator/SKILL.md               # FR-7, FR-9
  ... (pre-existing 21 skills)

okf/
  executive-identity.md                 # FR-1
  voice-profile.md                      # FR-5
  positioning-statements.md             # FR-2
  narrative-library.md                  # FR-3
  story-library.md                      # FR-4 (Single consolidated)
  messaging-library.md                  # FR-8

out/
  runtime/
    opportunity-analysis.yaml
    projection-validation-report.yaml
    brand-validation-report.yaml        # FR-7
  resume-executive.md
  resume-ats.md
  resume-recruiter.md
  cover-letter.md
  linkedin-profile.md
  playbook.md
  interview-cheatsheet.md
  executive-brief.md
  opportunity-alignment.md
```

---

## 8. Pipeline Execution Order (v0.5 Sprint 5)

```
KNOWLEDGE LAYER (canonical; writes to okf/)
  1.  portfolio-ingestor
  2.  portfolio-analyzer
  3.  achievement-extractor
  4.  evidence-card-generator
  5.  behaviour-profile-generator
  6.  capability-extractor
  7.  signature-achievements-curator
  8.  signature-theme-miner
  9.  executive-identity-generator      # New: okf/executive-identity.md, voice-profile.md, positioning-statements.md
 10.  narrative-engine                  # New: okf/narrative-library.md, messaging-library.md
 11.  story-engine                      # New: okf/story-library.md

RUNTIME LAYER (derived execution context; writes to out/runtime/)
 12.  opportunity-analyzer              # out/runtime/opportunity-analysis.yaml

COACHING LAYER (derived; reads canonical + opportunity-analysis)
 13.  interview-strategy-generator
 14.  knowledge-gaps

PROJECTION LAYER (views; reads canonical + opportunity-analysis; writes to out/)
 15.  projection-registry
      ├── resume-projection
      ├── cover-letter-projection
      ├── linkedin-projection
      ├── opportunity-alignment-view
      ├── executive-brief-view
      └── playbook-assembler
 16.  projection-validator
 17.  brand-validator                   # New: out/runtime/brand-validation-report.yaml
```

---

## 9. Boundaries

### Always Do:
- Store Executive Identity, Voice Profile, Positioning Statements, Narrative Library, Story Library, and Messaging Library in `okf/`.
- Ensure all projections consume identical canonical positioning statements.
- Tag every claim line in canonical narrative nodes with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.

### Ask First:
- Modifying the consolidated structure of `okf/story-library.md`.

### Never Do:
- Allow individual projections to independently generate introductory positioning prose.
- Fabricate metrics, team sizes, or career roles in narratives.

---

## 10. Success Criteria

Sprint 5 is complete when:
1. All 6 canonical Executive Identity concept files exist in `okf/`.
2. Projections (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `executive-brief-view`, `playbook-assembler`) adapt introductory text from canonical positioning statements rather than generating it independently.
3. `brand-validator` outputs `out/runtime/brand-validation-report.yaml` showing 100% brand alignment and voice consistency.
4. Full test suite (`pytest`) passes cleanly.
