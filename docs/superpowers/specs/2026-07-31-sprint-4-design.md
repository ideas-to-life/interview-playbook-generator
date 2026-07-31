# Design Spec: Sprint 4 (v0.4) — Career Projection Platform

**Status:** Approved Specification  
**Version:** 0.4  
**Date:** 2026-07-31  

---

## 1. Objective & Vision

Transform the Interview Playbook Generator into a **Career Projection Platform** capable of generating multiple executive communication artefacts (Resumes, Cover Letters, LinkedIn Profiles, Briefings, and Playbooks) from a single canonical OKF knowledge graph.

Sprint 4 introduces:
1. **Target Opportunity Analyzer (`opportunity-analyzer`)**: Executes opportunity interpretation exactly once, outputting `out/runtime/opportunity-analysis.yaml`.
2. **Projection SDK & Projection Registry (`projection-registry`)**: Standardised contract enabling pluggable, read-only projection generators without changing pipeline architecture.
3. **Executive Projections**:
   - `resume-projection`: Generates `out/resume-executive.md`, `out/resume-ats.md`, and `out/resume-recruiter.md` (all three by default, configurable via `config/config.yaml`).
   - `cover-letter-projection`: Generates 1-page executive cover letter at `out/cover-letter.md`.
   - `linkedin-projection`: Generates LinkedIn profile optimization at `out/linkedin-profile.md` (Headline, About, Featured Summary, Experience Refinements).
4. **Shared Validation (`projection-validator`)**: Automated validation report assessing evidence coverage, capability alignment, ATS vocabulary density, and readability across all projection artefacts.

---

## 2. Architecture & Four-Layer System Model

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
                    │  • JD, Recruiter Notes, Company Info   │
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

### The Four Layers:
1. **Knowledge Layer (`okf/`)**: Canonical, persistent, immutable career knowledge (`Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `Theme`, `Narrative`). Never modified by projections.
2. **Coaching Layer (`okf/`)**: Derived strategy & gap analysis (`interview-strategy.md`, `knowledge-gaps.md`).
3. **Runtime Layer (`out/runtime/`)**: Derived opportunity-specific execution context (`opportunity-analysis.yaml`). Completely separate from `okf/` to preserve canonical separation.
4. **Projection Layer (`out/`)**: Read-only presentation views (Resumes, Cover Letter, LinkedIn Profile, Playbook, Executive Brief, Opportunity Alignment, Cheat Sheet).

---

## 3. Opportunity Analysis Schema (`out/runtime/opportunity-analysis.yaml`)

The `opportunity-analyzer` Skill parses the target opportunity and generates `out/runtime/opportunity-analysis.yaml` with the following schema:

```yaml
version: "0.4"
generated_at: "2026-07-31T08:00:00Z"
target_opportunity:
  company: "Vervaunt"
  role_title: "Head of AI"
  industry: "E-Commerce & Digital Agency"
  interviewer: "Senior Talent Acquisition Specialist"

hiring_goals:
  - "Build internal GenAI and agentic workflow tools across delivery, ops, and finance."
  - "Expand client-facing AI service offerings for enterprise e-commerce clients."

executive_positioning: "Enterprise AI Architect & Builder specialising in production GenAI platforms, agentic guardrails, and rapid ROI."

capability_priorities:
  - capability: "Enterprise AI Governance"
    priority: "High"
  - capability: "Agentic AI Architecture"
    priority: "High"
  - capability: "Architecture-as-Code & Spec-Driven Development"
    priority: "High"
  - capability: "Executive Stakeholder Leadership"
    priority: "Medium"
  - capability: "Observability & Agent Evals"
    priority: "Medium"

behaviour_expectations:
  - "Hands-on builder"
  - "Founder mindset"
  - "High velocity execution"
  - "Governance as enablement"

ats_vocabulary:
  mandatory:
    - "Generative AI"
    - "Multi-Agent Systems"
    - "LLM Tools"
    - "AI Governance"
  strong:
    - "Architecture-as-Code"
    - "Agentic Workflows"
    - "Observability & Evals"
  optional:
    - "SAP Integration"
    - "Enterprise Architecture"

organisational_signals:
  company_maturity: "Fast-growing high-velocity agency"
  delivery_style: "Pragmatic, spec-driven, hands-on"
  governance_expectations: "Lightweight automated rails"

risks:
  - "Corporate over-governance perception"
  - "Deep research vs production engineering confusion"

coverage_matrix:
  - requirement: "Operationalising GenAI in Enterprise Production"
    coverage: "High"
    confidence: "Strong"
    primary_evidence: ["bbc-studios-genai-framework", "wpp-agentic-ai-platform"]
    capabilities: ["enterprise-ai-governance"]
  - requirement: "Multi-Agent Systems & Platform Architecture"
    coverage: "High"
    confidence: "Strong"
    primary_evidence: ["wpp-agentic-ai-platform", "cas-architecture-as-code"]
    capabilities: ["agentic-ai-architecture"]
```

---

## 4. Projection SDK & Projection Registry Interface

Every projection Skill implements a common projection contract:

### 4.1 Projection Contract (`ProjectionContract`)

- **Metadata**: `name`, `version`, `target_audience`, `output_format`
- **Inputs**:
  - Canonical OKF Bundle (`okf/`)
  - Shared Opportunity Analysis (`out/runtime/opportunity-analysis.yaml`)
  - Projection Configuration (`config/config.yaml` under `projections.<name>`)
- **Processing Constraints**:
  - Read-only access to canonical bundle
  - Zero mutation of `okf/`
  - All statements traceable to evidence cards/capabilities
- **Outputs**:
  - Presentation Artefact(s) in `out/`
  - Projection Validation Report

### 4.2 Projection Registry (`skills/projection-registry/SKILL.md`)

Discovers, registers, and executes active projections. Known registered projections for v0.4:
- `playbook-assembler` ➔ `out/playbook.md`, `out/interview-cheatsheet.md`
- `opportunity-alignment-view` ➔ `out/opportunity-alignment.md`
- `executive-brief-view` ➔ `out/executive-brief.md`
- `resume-projection` ➔ `out/resume-executive.md`, `out/resume-ats.md`, `out/resume-recruiter.md`
- `cover-letter-projection` ➔ `out/cover-letter.md`
- `linkedin-projection` ➔ `out/linkedin-profile.md`

---

## 5. Projection Skill Specifications

### 5.1 Resume Projection (`skills/resume-projection/SKILL.md`)
Generates 3 default variants (or a single variant if `projections.resume.variant` is specified in `config/config.yaml`):
1. **Executive Resume** (`out/resume-executive.md`): Strategic positioning, 2 pages, capability progression, high-impact outcomes.
2. **ATS Resume** (`out/resume-ats.md`): Structured section headers, explicit ATS vocabulary keyword placement, clear chronological format.
3. **Recruiter Resume** (`out/resume-recruiter.md`): 1-page high-density summary briefing for talent acquisition.

### 5.2 Cover Letter Projection (`skills/cover-letter-projection/SKILL.md`)
Generates 1-page executive cover letter at `out/cover-letter.md`:
- Motivation & Strategic Alignment
- Core Signature Achievements & Capability Fit
- 90-Day Execution Value Proposition
- Call to Action & Sign-off

### 5.3 LinkedIn Projection (`skills/linkedin-projection/SKILL.md`)
Generates LinkedIn profile optimization at `out/linkedin-profile.md`:
- Headline (high-impact professional positioning)
- About Section (executive narrative, core capability pillars, contact CTA)
- Featured Summary & Key Projects
- Experience Section Refinements

### 5.4 Projection Validator (`skills/projection-validator/SKILL.md`)
Evaluates generated artefacts and outputs `out/runtime/projection-validation-report.yaml`:
- **Evidence Traceability**: % of claims backed by OKF evidence cards.
- **Capability Alignment**: % alignment with capability priorities.
- **ATS Keyword Density**: % of mandatory and strong ATS terms included.
- **Readability & Word Budget**: Sentence length, section word count compliance.

---

## 6. Project Structure

```
config/
  config.yaml                            # Updated for v0.4 projections
  config.example.yaml

skills/
  opportunity-analyzer/SKILL.md          # FR-1, FR-2
  projection-registry/SKILL.md           # FR-3, FR-11
  resume-projection/SKILL.md              # FR-4
  cover-letter-projection/SKILL.md        # FR-5
  linkedin-projection/SKILL.md            # FR-6
  projection-validator/SKILL.md           # FR-10
  ... (pre-existing 10 skills)

out/
  runtime/
    opportunity-analysis.yaml           # FR-2 (Derived execution context)
    projection-validation-report.yaml   # FR-10
  resume-executive.md                    # FR-4
  resume-ats.md                          # FR-4
  resume-recruiter.md                    # FR-4
  cover-letter.md                        # FR-5
  linkedin-profile.md                    # FR-6
  playbook.md                            # Pre-existing
  interview-cheatsheet.md                # Pre-existing
  executive-brief.md                     # Pre-existing
  opportunity-alignment.md               # Pre-existing
```

---

## 7. Pipeline Execution Order (v0.4 Sprint 4)

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
  9.  narrative-generator

RUNTIME LAYER (derived execution context; writes to out/runtime/)
  10. opportunity-analyzer              # New: produces out/runtime/opportunity-analysis.yaml

COACHING LAYER (derived; reads canonical + opportunity-analysis)
  11. interview-strategy-generator
  12. knowledge-gaps

PROJECTION LAYER (views; reads canonical + opportunity-analysis; writes to out/)
  13. projection-registry               # New: orchestrates all registered projections
      ├── resume-projection             # New: out/resume-*.md
      ├── cover-letter-projection       # New: out/cover-letter.md
      ├── linkedin-projection           # New: out/linkedin-profile.md
      ├── opportunity-alignment-view
      ├── executive-brief-view
      └── playbook-assembler
  14. projection-validator              # New: produces out/runtime/projection-validation-report.yaml
```

---

## 8. Testing & Quality Discipline

- **Unit & Linter Tests**:
  - `tests/test_opportunity_analyzer.py`: Validates schema and parsing of `opportunity-analysis.yaml`.
  - `tests/test_projection_registry.py`: Validates registration and invocation of projection contracts.
  - `tests/test_resume_projection.py`: Validates generation of 3 resume variants.
  - `tests/test_cover_letter_projection.py`: Validates 1-page length and section structure.
  - `tests/test_linkedin_projection.py`: Validates headline, about, and experience sections.
  - `tests/test_projection_validator.py`: Validates validation report scoring logic.
  - `tests/test_v04_success_criteria.py`: End-to-end success criteria checks.

- **Golden Fixtures**:
  - `tests/golden/opportunity-analyzer/opportunity-analysis.yaml`
  - `tests/golden/resume-projection/`
  - `tests/golden/cover-letter-projection/`
  - `tests/golden/linkedin-projection/`

---

## 9. Boundaries

### Always Do:
- Keep the `okf/` bundle strictly canonical and immutable.
- Place derived opportunity analysis in `out/runtime/opportunity-analysis.yaml`.
- Ensure all projections consume identical capability priorities and opportunity analysis.
- Trace every projection statement back to canonical evidence.

### Ask First:
- Modifying the Projection SDK interface contract.
- Adding non-standard file extensions or export formats (e.g. PDF generation).

### Never Do:
- Mutate `okf/` nodes during projection execution.
- Fabricate metrics, team sizes, budgets, or technologies in resumes or cover letters.
- Duplicate opportunity interpretation across individual projections.

---

## 10. Success Criteria

Sprint 4 is complete when:
1. `opportunity-analyzer` generates `out/runtime/opportunity-analysis.yaml` once per pipeline run.
2. All projections (`resume-projection`, `cover-letter-projection`, `linkedin-projection`, `executive-brief-view`, `opportunity-alignment-view`, `playbook-assembler`) consume the shared `opportunity-analysis.yaml`.
3. `resume-projection` generates `out/resume-executive.md`, `out/resume-ats.md`, and `out/resume-recruiter.md` by default.
4. `cover-letter-projection` generates a 1-page executive cover letter at `out/cover-letter.md`.
5. `linkedin-projection` generates LinkedIn optimization at `out/linkedin-profile.md`.
6. `projection-validator` outputs `out/runtime/projection-validation-report.yaml`.
7. The `okf/` canonical bundle remains 100% untouched during projection runs.
8. Full test suite (`pytest`) passes cleanly.
