# Sprint 4 (v0.4) — Career Projection Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Evolve the system into a Career Projection Platform by introducing a shared Target Opportunity Analyzer (`out/runtime/opportunity-analysis.yaml`), a pluggable Projection SDK/Registry, and three new projection Skills (`resume-projection`, `cover-letter-projection`, `linkedin-projection`) along with a shared `projection-validator`.

**Architecture:** Pure additive release over v0.3. The canonical OKF bundle in `okf/` remains 100% immutable. Opportunity analysis is executed once and saved to `out/runtime/opportunity-analysis.yaml`. All projections consume this shared analysis file.

---

## Global Constraints

- **The OKF Bundle is immutable** (Principle 1). `okf/` is never modified by projections.
- **Opportunity analysis happens once** (Principle 2). Generated at `out/runtime/opportunity-analysis.yaml`.
- **Projections are views** (Principle 3). Deleting a projection never changes canonical knowledge.
- **100% Traceability** (Principle 4). Every statement traces back to evidence cards or capabilities.
- **Resume Projection Outputs**: Generates `out/resume-executive.md`, `out/resume-ats.md`, and `out/resume-recruiter.md` by default, or single variant if configured in `config/config.yaml`.
- **Cover Letter Projection**: Generates 1-page executive cover letter at `out/cover-letter.md`.
- **LinkedIn Projection**: Generates LinkedIn profile optimization at `out/linkedin-profile.md`.
- **Projection Validator**: Outputs `out/runtime/projection-validation-report.yaml`.

---

## File Structure

### New files
```
skills/opportunity-analyzer/SKILL.md
skills/projection-registry/SKILL.md
skills/resume-projection/SKILL.md
skills/cover-letter-projection/SKILL.md
skills/linkedin-projection/SKILL.md
skills/projection-validator/SKILL.md
tests/test_opportunity_analyzer.py
tests/test_projection_registry.py
tests/test_resume_projection.py
tests/test_cover_letter_projection.py
tests/test_linkedin_projection.py
tests/test_projection_validator.py
tests/test_v04_success_criteria.py
tests/golden/opportunity-analyzer/opportunity-analysis.yaml
tests/golden/projection-registry/projection-registry.yaml
tests/golden/resume-projection/resume-executive.md
tests/golden/resume-projection/resume-ats.md
tests/golden/resume-projection/resume-recruiter.md
tests/golden/cover-letter-projection/cover-letter.md
tests/golden/linkedin-projection/linkedin-profile.md
tests/golden/projection-validator/projection-validation-report.yaml
```

### Modified files
```
config/config.example.yaml
config/config.yaml
skills/playbook-orchestrator/SKILL.md
tests/test_skills.py
AGENTS.md
CLAUDE.md
ARCHITECTURE.md
README.md
```

---

## Tasks

### Task 1: Target Opportunity Analyzer Skill & Schema

**Files:**
- Create: `skills/opportunity-analyzer/SKILL.md`
- Create: `tests/golden/opportunity-analyzer/opportunity-analysis.yaml`
- Create: `tests/test_opportunity_analyzer.py`

- [ ] **Step 1: Create `skills/opportunity-analyzer/SKILL.md`** defining input requirements, parsing steps, and YAML schema for `out/runtime/opportunity-analysis.yaml`.
- [ ] **Step 2: Create golden fixture `tests/golden/opportunity-analyzer/opportunity-analysis.yaml`**.
- [ ] **Step 3: Create `tests/test_opportunity_analyzer.py`** validating file creation, YAML schema parsing, and key sections (Hiring Goals, Executive Positioning, Capability Priorities, ATS Vocabulary, Coverage Matrix).
- [ ] **Step 4: Run tests `pytest tests/test_opportunity_analyzer.py -v`**.
- [ ] **Step 5: Commit `git add skills/opportunity-analyzer/ tests/golden/opportunity-analyzer/ tests/test_opportunity_analyzer.py && git commit -m "feat: add opportunity-analyzer Skill and schema"`**.

---

### Task 2: Projection SDK & Projection Registry

**Files:**
- Create: `skills/projection-registry/SKILL.md`
- Create: `tests/golden/projection-registry/projection-registry.yaml`
- Create: `tests/test_projection_registry.py`

- [ ] **Step 1: Create `skills/projection-registry/SKILL.md`** defining Projection Contract and Registry interface.
- [ ] **Step 2: Create golden fixture `tests/golden/projection-registry/projection-registry.yaml`**.
- [ ] **Step 3: Create `tests/test_projection_registry.py`** validating registration and contract verification.
- [ ] **Step 4: Run tests `pytest tests/test_projection_registry.py -v`**.
- [ ] **Step 5: Commit `git add skills/projection-registry/ tests/golden/projection-registry/ tests/test_projection_registry.py && git commit -m "feat: add projection-registry Skill and contract"`**.

---

### Task 3: Resume Projection Skill

**Files:**
- Create: `skills/resume-projection/SKILL.md`
- Create: `tests/golden/resume-projection/resume-executive.md`
- Create: `tests/golden/resume-projection/resume-ats.md`
- Create: `tests/golden/resume-projection/resume-recruiter.md`
- Create: `tests/test_resume_projection.py`

- [ ] **Step 1: Create `skills/resume-projection/SKILL.md`** detailing rendering rules for 3 resume variants.
- [ ] **Step 2: Create golden fixtures for Executive, ATS, and Recruiter resumes in `tests/golden/resume-projection/`**.
- [ ] **Step 3: Create `tests/test_resume_projection.py`** asserting variant creation, structure, and traceability.
- [ ] **Step 4: Run tests `pytest tests/test_resume_projection.py -v`**.
- [ ] **Step 5: Commit `git add skills/resume-projection/ tests/golden/resume-projection/ tests/test_resume_projection.py && git commit -m "feat: add resume-projection Skill and golden variants"`**.

---

### Task 4: Cover Letter Projection Skill

**Files:**
- Create: `skills/cover-letter-projection/SKILL.md`
- Create: `tests/golden/cover-letter-projection/cover-letter.md`
- Create: `tests/test_cover_letter_projection.py`

- [ ] **Step 1: Create `skills/cover-letter-projection/SKILL.md`** for 1-page executive cover letter.
- [ ] **Step 2: Create golden fixture `tests/golden/cover-letter-projection/cover-letter.md`**.
- [ ] **Step 3: Create `tests/test_cover_letter_projection.py`** verifying sections (Motivation, Alignment, Evidence, Closing) and length constraint (≤1 page).
- [ ] **Step 4: Run tests `pytest tests/test_cover_letter_projection.py -v`**.
- [ ] **Step 5: Commit `git add skills/cover-letter-projection/ tests/golden/cover-letter-projection/ tests/test_cover_letter_projection.py && git commit -m "feat: add cover-letter-projection Skill"`**.

---

### Task 5: LinkedIn Projection Skill

**Files:**
- Create: `skills/linkedin-projection/SKILL.md`
- Create: `tests/golden/linkedin-projection/linkedin-profile.md`
- Create: `tests/test_linkedin_projection.py`

- [ ] **Step 1: Create `skills/linkedin-projection/SKILL.md`** for LinkedIn profile optimization.
- [ ] **Step 2: Create golden fixture `tests/golden/linkedin-projection/linkedin-profile.md`**.
- [ ] **Step 3: Create `tests/test_linkedin_projection.py`** verifying Headline, About, Featured Summary, and Experience sections.
- [ ] **Step 4: Run tests `pytest tests/test_linkedin_projection.py -v`**.
- [ ] **Step 5: Commit `git add skills/linkedin-projection/ tests/golden/linkedin-projection/ tests/test_linkedin_projection.py && git commit -m "feat: add linkedin-projection Skill"`**.

---

### Task 6: Shared Projection Validator

**Files:**
- Create: `skills/projection-validator/SKILL.md`
- Create: `tests/golden/projection-validator/projection-validation-report.yaml`
- Create: `tests/test_projection_validator.py`

- [ ] **Step 1: Create `skills/projection-validator/SKILL.md`** for automated validation of all generated projections.
- [ ] **Step 2: Create golden fixture `tests/golden/projection-validator/projection-validation-report.yaml`**.
- [ ] **Step 3: Create `tests/test_projection_validator.py`** checking validation scoring logic.
- [ ] **Step 4: Run tests `pytest tests/test_projection_validator.py -v`**.
- [ ] **Step 5: Commit `git add skills/projection-validator/ tests/golden/projection-validator/ tests/test_projection_validator.py && git commit -m "feat: add projection-validator Skill"`**.

---

### Task 7: Orchestrator & Configuration Update

**Files:**
- Modify: `config/config.example.yaml`
- Modify: `config/config.yaml`
- Modify: `skills/playbook-orchestrator/SKILL.md`
- Modify: `tests/test_skills.py`

- [ ] **Step 1: Bump version to `"0.4"` in `config/config.example.yaml` & `config/config.yaml`** and add projection configuration blocks.
- [ ] **Step 2: Update `skills/playbook-orchestrator/SKILL.md`** to orchestrate the v0.4 pipeline including `opportunity-analyzer`, `projection-registry`, projections, and `projection-validator`.
- [ ] **Step 3: Update `tests/test_skills.py`** to assert all 21 skills exist and have valid frontmatter.
- [ ] **Step 4: Run tests `pytest tests/test_skills.py -v`**.
- [ ] **Step 5: Commit `git add config/ skills/playbook-orchestrator/ tests/test_skills.py && git commit -m "feat: update pipeline orchestrator and config for v0.4"`**.

---

### Task 8: Documentation Updates

**Files:**
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `ARCHITECTURE.md`
- Modify: `README.md`

- [ ] **Step 1: Update `AGENTS.md`** with Runtime Layer and Projection Platform diagram.
- [ ] **Step 2: Update `CLAUDE.md`** with Sprint 4 status.
- [ ] **Step 3: Update `ARCHITECTURE.md`** with Four-Layer system diagram.
- [ ] **Step 4: Update `README.md`** with v0.4 features overview.
- [ ] **Step 5: Run tests `pytest tests/ -v`**.
- [ ] **Step 6: Commit `git add AGENTS.md CLAUDE.md ARCHITECTURE.md README.md && git commit -m "docs: update documentation for v0.4 Career Projection Platform"`**.

---

### Task 9: End-to-End Success Criteria Verification

**Files:**
- Create: `tests/test_v04_success_criteria.py`

- [ ] **Step 1: Create `tests/test_v04_success_criteria.py`** asserting all 8 spec success criteria.
- [ ] **Step 2: Run full test suite `pytest tests/ -v`**.
- [ ] **Step 3: Commit `git add tests/test_v04_success_criteria.py && git commit -m "test: add v0.4 success criteria checks"`**.
