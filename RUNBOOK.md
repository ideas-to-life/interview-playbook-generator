# RUNBOOK: Career Projection Platform (Interview Playbook Generator)

Welcome to the **Career Projection Platform (Interview Playbook Generator v0.6)**. This runbook is a comprehensive guide for candidates, engineers, and AI agents on how to setup, configure, execute, and validate the pipeline end-to-end.

---

## 1. Overview & System Mission

The Career Projection Platform takes a candidate's raw portfolio (CV, LinkedIn profile, architecture documents, case studies, publications) and a target opportunity specification (Job Description, recruiter message, Upwork posting), and:
1. Builds an immutable, canonical **OKF (Open Knowledge Format) v0.2 Knowledge Graph** in `out/okf/`.
2. Synthesizes a canonical **Executive Identity & Personal Brand Engine** (`okf/executive-identity.md`, `voice-profile.md`, `positioning-statements.md`, `narrative-library.md`, `story-library.md`).
3. Computes opportunity-scoped runtime intelligence, qualification scoring, archetype alignment, and gap analysis in `out/<target-slug>/runtime/`.
4. Orchestrates registered projection views to emit tailored executive communication artifacts (Resumes, Cover Letters, LinkedIn Profiles, Briefings, Upwork Proposals, and Interview Playbooks) in `out/<target-slug>/`.

### Core Architectural Principle
> **"Tailor expression, not identity."**  
> Evidence determines what the candidate can credibly claim; canonical identity determines who the candidate is; the target opportunity determines which truths to emphasize. The system **never fabricates** metrics, titles, or responsibilities.

---

## 2. The Five Non-Negotiable Hard Rules

Every agent, skill, and script operating in this repository MUST strictly enforce these 5 hard rules:

1. **Never Fabricate:** Never invent projects, dollar metrics, percentages, team sizes, budgets, technologies, responsibilities, or employment dates. Missing data must be marked as `[assumption]`.
2. **Classify Every Claim:** Every non-heading prose line in concept files MUST start with one of: `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`.
3. **Attribute Every Claim:** Every `[evidence]` line MUST cite a valid source footnote `[^source-id]` pointing to frontmatter `sources`.
4. **Stop and Ask:** If required inputs (`config/config.yaml` or target opportunity spec) are missing, trigger the stop-and-ask protocol rather than guessing.
5. **Idempotent Re-runs:** Re-running any Skill cleanly overwrites its output subtree while updating `generated_at` timestamps.

---

## 3. Environment & Prerequisites

### System Requirements
* **OS:** macOS or Linux
* **Python:** 3.13+ (with `PyYAML` and `pytest` installed)
* **Agent Runtime:** Antigravity CLI, Claude Code, or compatible AI agent environment.

### Workspace Verification
Run pytest to verify environment setup and baseline test suite status:
```bash
pytest -v
```
*Expected Output:* `154 passed`.

---

## 4. Step-by-Step Execution Guide

### Step 1: Place Candidate Portfolio Sources
Place raw candidate documents inside `inputs/` or `evidence/`:
* `inputs/cv.pdf` (or `cv.md`)
* `inputs/linkedin.pdf` (or `linkedin.md`)
* `inputs/case-studies/` (Architecture docs, project summaries, presentation decks)

### Step 2: Place Target Opportunity Specification
Place the target job description or Upwork project posting inside `evidence/target-position/`:
* Example path: `evidence/target-position/upwork-business-systems-technology-architecture-consultant.md`

### Step 3: Configure `config/config.yaml`
Create or update `config/config.yaml` (copied from `config/config.example.yaml`):

```yaml
candidate:
  name: "Alexandre Franco"
  portfolio_dir: "inputs/"

target_opportunity:
  source: "evidence/target-position/upwork-business-systems-technology-architecture-consultant.md"
  target_type: "upwork"  # Options: "standard", "upwork", "executive"

pipeline:
  fail_on_severe_gaps: false
  validate_brand: true
```

### Step 4: Execute the Pipeline via AI Agent
Inside your agent session (Antigravity or Claude Code), run the top-level 23-step pipeline orchestrator:

```text
/skill playbook-orchestrator
```

The AI agent will sequentially execute the 5-layer pipeline:
1. **Knowledge Layer:** `portfolio-ingestor` ➔ `portfolio-analyzer` ➔ `achievement-extractor` ➔ `evidence-card-generator` ➔ `behaviour-profile-generator` ➔ `capability-extractor` ➔ `signature-achievements-curator` ➔ `signature-theme-miner` ➔ `executive-identity-generator` ➔ `narrative-engine` ➔ `story-engine`.
2. **Runtime Intelligence Layer:** `opportunity-analyzer` ➔ `upwork-qualification` (if upwork) ➔ `archetype-classifier` ➔ `gap-classifier` ➔ `archetype-fit-evaluator` ➔ `projection-strategy-generator`.
3. **Coaching Layer:** `interview-strategy-generator` ➔ `knowledge-gaps`.
4. **Projection & Validation Layer:** `projection-registry` ➔ `resume-projection`, `cover-letter-projection`, `linkedin-projection`, `opportunity-alignment-view`, `executive-brief-view`, `upwork-proposal` (if upwork), `playbook-assembler` ➔ `projection-validator` ➔ `brand-validator`.
5. **Evaluation Layer:** `market-feedback-evaluator`.

### Step 5: (Alternative) Offline Playbook Generation
If you wish to generate or test offline fixture packages without running live LLM inference:

```bash
python3 scripts/generate_upwork_biz_systems_playbook.py
```
This script creates all runtime YAMLs and presentation views under `out/upwork-business-systems-technology-architecture-consultant/`.

---

## 5. Artifact Inventory & Output Directory Structure

Generated outputs are organized into two distinct directories:

### 1. Canonical Knowledge Graph (`out/okf/`)
Shared across all target opportunities; immutable by projections:
* `okf/index.md` & `okf/log.md`: Knowledge graph index and execution audit log.
* `okf/behaviour-profile.md`: Canonical executive behaviour profile.
* `okf/capabilities/*.md`: Domain capability concept nodes.
* `okf/signature-achievements.md`: Ranked intrinsic achievements.
* `okf/signature-themes.md`: Recurring executive themes.
* `okf/executive-identity.md`: Canonical identity core.
* `okf/voice-profile.md`: Executive voice principles & tone guidelines.
* `okf/positioning-statements.md`: Core positioning formulations.
* `okf/narrative-library.md` & `messaging-library.md`: Strategic messaging options.
* `okf/story-library.md`: Consolidated STAR story library.

### 2. Opportunity-Scoped Subtree (`out/<target-slug>/`)
Scoped specifically to the target opportunity (e.g. `out/upwork-business-systems-technology-architecture-consultant/`):

#### Presentation Projections (Root of Target Slug)
* `resume-executive.md`: 2-page strategic executive resume.
* `resume-ats.md`: Single-column ATS-optimized resume.
* `resume-recruiter.md`: 1-page recruiter overview.
* `cover-letter.md`: 1-page tailored executive cover letter.
* `linkedin-profile.md`: Optimized LinkedIn headline, about section, and featured achievements.
* `opportunity-alignment.md`: Requirement-by-requirement alignment matrix.
* `executive-brief.md`: 10-minute pre-interview briefing memo.
* `playbook.md`: Detailed coaching interview playbook with story-to-question mappings.
* `interview-cheatsheet.md`: 2-page quick reference interview sheet.
* `upwork-qualification-report.md`: Clean 350-500 word submission-ready Upwork Executive Proposal Cover Letter with runtime qualification header metadata.
* `upwork-screening-answers.md`: Isolated screening question responses (Q1–Q5).
* `upwork-work-samples.md`: STAR case study work sample recommendations with explicit project tags.
* `upwork-evidence-gaps.md`: Companion evidence gap report and candidate confirmation questions.

#### Derived Execution Context (`out/<target-slug>/runtime/`)
* `opportunity-analysis.yaml`: Structured target position priorities & requirements.
* `upwork-qualification.yaml`: Qualification readiness, fit rating, and requirement assessments.
* `archetype-analysis.yaml`: Archetype classification breakdown.
* `gap-analysis.yaml`: Missing capability & evidence gaps.
* `opportunity-fit-report.yaml`: Positioning fit evaluation.
* `projection-strategy.yaml`: Strategy and story selection logic.
* `projection-validation-report.yaml`: Evidence coverage & ATS keyword density report.
* `brand-validation-report.yaml`: Voice consistency and brand alignment report.

#### Evaluation Layer (`evaluation/opportunities/`)
* `<target-slug>-evaluation.yaml`: Market feedback evaluation.

---

## 6. Testing, Validation & Governance Checks

### Run Full Test Suite
To verify systemic integrity, attribution logic, and contract compliance:
```bash
pytest tests/ -v
```

### Validate Upwork Proposals
To independently inspect generated client-facing proposal copy for zero internal tags (`[evidence]`, `[^source-id]`), non-fabrication, screening answer isolation, and metric integrity:
```bash
python3 scripts/upwork_validator.py
```

---

## 7. Troubleshooting & Common Scenarios

| Issue / Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| **Pipeline stops with missing config error** | `config/config.yaml` missing or `target_opportunity.source` empty. | Copy `config/config.example.yaml` to `config/config.yaml` and set valid paths. |
| **Pytest failure on golden diffs** | Skill output format modified without updating tests. | Run `pytest -v` to identify diff, then regenerate golden fixture under `tests/golden/<skill>/` if intentional. |
| **Internal tags visible in proposal output** | Skill generated raw OKF tags in client-facing view. | Run `python3 scripts/upwork_validator.py`. Ensure client-facing projections filter out `[evidence]` tags. |
| **Unforced human decision state** | Machine qualification does not finalize submission. | Intended behavior. Human user selects `user_decision_state: APPLY` in `upwork-qualification.yaml`. |

---

## 8. Spec Kit (`speckit`) SDLC Workflow

This repository uses **Spec Kit (`speckit`)** as its primary Spec-Driven Development framework for specifying, planning, tasking, implementing, and validating new features and architectural refinements. All design specifications are stored under `specs/<feature-slug>/`.

### Spec Kit Lifecycle Commands

When contributing new capabilities or refining existing skills:

1. **Intake & Specify (`/speckit-specify`):**  
   Generate or update feature requirements in `specs/<feature-slug>/spec.md`.  
   *Output:* `spec.md`, `checklists/requirements.md`.

2. **Clarify Requirements (`/speckit-clarify`):**  
   Identify underspecified requirements and record clarification decisions directly into `spec.md`.

3. **Architecture & Plan (`/speckit-plan`):**  
   Generate the technical design and architectural contracts in `specs/<feature-slug>/plan.md`.  
   *Output:* `plan.md`, `research.md`, `data-model.md`, `contracts/`.

4. **Task Decomposition (`/speckit-tasks`):**  
   Decompose the plan into dependency-ordered, user-story-aligned implementation tasks.  
   *Output:* `tasks.md`.

5. **Cross-Artifact Analysis (`/speckit-analyze`):**  
   Run non-destructive consistency audits across `spec.md`, `plan.md`, and `tasks.md`.

6. **Implementation Execution (`/speckit-implement`):**  
   Execute tasks in `tasks.md` incrementally, running test verification after each task.

7. **Commit Changes (`/speckit-git-commit`):**  
   Auto-commit validated changes following conventional commit syntax.

