# Sprint 5 (v0.5) — Executive Narrative & Personal Brand Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a canonical Executive Identity Layer in `okf/` (`executive-identity.md`, `voice-profile.md`, `positioning-statements.md`, `narrative-library.md`, `story-library.md`, `messaging-library.md`) and introduce `brand-validator` to eliminate brand drift across projections.

---

## Global Constraints

- **Executive Identity is canonical** (FR-1). Stored in `okf/`.
- **Single consolidated story library** (FR-4). All executive stories stored in `okf/story-library.md`.
- **Projections adapt, never regenerate** (FR-6). Resumes, Cover Letters, and LinkedIn profiles adapt canonical positioning statements.
- **100% OKF classification** (AGENTS.md). All non-heading body lines in canonical `.md` files carry classification prefixes.

---

## File Structure

### New files
```
skills/executive-identity-generator/SKILL.md
skills/narrative-engine/SKILL.md
skills/story-engine/SKILL.md
skills/brand-validator/SKILL.md
tests/test_executive_identity.py
tests/test_narrative_engine.py
tests/test_story_engine.py
tests/test_brand_validator.py
tests/test_v05_success_criteria.py
tests/golden/executive-identity/executive-identity.md
tests/golden/executive-identity/voice-profile.md
tests/golden/executive-identity/positioning-statements.md
tests/golden/narrative-engine/narrative-library.md
tests/golden/narrative-engine/messaging-library.md
tests/golden/story-engine/story-library.md
tests/golden/brand-validator/brand-validation-report.yaml
```

### Modified files
```
config/config.example.yaml
config/config.yaml
skills/playbook-orchestrator/SKILL.md
skills/resume-projection/SKILL.md
skills/cover-letter-projection/SKILL.md
skills/linkedin-projection/SKILL.md
tests/test_skills.py
AGENTS.md
CLAUDE.md
ARCHITECTURE.md
README.md
```

---

## Tasks

### Task 1: Executive Identity Generator Skill & Canonical Nodes

**Files:**
- Create: `skills/executive-identity-generator/SKILL.md`
- Create: `tests/golden/executive-identity/executive-identity.md`
- Create: `tests/golden/executive-identity/voice-profile.md`
- Create: `tests/golden/executive-identity/positioning-statements.md`
- Create: `tests/test_executive_identity.py`

- [ ] **Step 1: Create `skills/executive-identity-generator/SKILL.md`**.
- [ ] **Step 2: Create golden fixtures for `executive-identity.md`, `voice-profile.md`, and `positioning-statements.md`**.
- [ ] **Step 3: Create `tests/test_executive_identity.py`** asserting frontmatter, section structure, and classification rules.
- [ ] **Step 4: Run tests `pytest tests/test_executive_identity.py -v`**.
- [ ] **Step 5: Commit `git add skills/executive-identity-generator/ tests/golden/executive-identity/ tests/test_executive_identity.py && git commit -m "feat: add executive-identity-generator Skill and canonical nodes"`**.

---

### Task 2: Narrative Engine Skill & Canonical Libraries

**Files:**
- Create: `skills/narrative-engine/SKILL.md`
- Create: `tests/golden/narrative-engine/narrative-library.md`
- Create: `tests/golden/narrative-engine/messaging-library.md`
- Create: `tests/test_narrative_engine.py`

- [ ] **Step 1: Create `skills/narrative-engine/SKILL.md`**.
- [ ] **Step 2: Create golden fixtures for `narrative-library.md` and `messaging-library.md`**.
- [ ] **Step 3: Create `tests/test_narrative_engine.py`** asserting journeys and 30s/2m messaging blocks.
- [ ] **Step 4: Run tests `pytest tests/test_narrative_engine.py -v`**.
- [ ] **Step 5: Commit `git add skills/narrative-engine/ tests/golden/narrative-engine/ tests/test_narrative_engine.py && git commit -m "feat: add narrative-engine Skill and canonical libraries"`**.

---

### Task 3: Story Engine Skill & Consolidated Story Library

**Files:**
- Create: `skills/story-engine/SKILL.md`
- Create: `tests/golden/story-engine/story-library.md`
- Create: `tests/test_story_engine.py`

- [ ] **Step 1: Create `skills/story-engine/SKILL.md`**.
- [ ] **Step 2: Create golden fixture `tests/golden/story-engine/story-library.md`**.
- [ ] **Step 3: Create `tests/test_story_engine.py`** validating story structures (Situation, Challenge, Decision, Actions, Outcome, Business Value, Hook, Transition).
- [ ] **Step 4: Run tests `pytest tests/test_story_engine.py -v`**.
- [ ] **Step 5: Commit `git add skills/story-engine/ tests/golden/story-engine/ tests/test_story_engine.py && git commit -m "feat: add story-engine Skill and consolidated story-library"`**.

---

### Task 4: Brand Validator Skill & Report

**Files:**
- Create: `skills/brand-validator/SKILL.md`
- Create: `tests/golden/brand-validator/brand-validation-report.yaml`
- Create: `tests/test_brand_validator.py`

- [ ] **Step 1: Create `skills/brand-validator/SKILL.md`**.
- [ ] **Step 2: Create golden fixture `tests/golden/brand-validator/brand-validation-report.yaml`**.
- [ ] **Step 3: Create `tests/test_brand_validator.py`** checking brand consistency scoring.
- [ ] **Step 4: Run tests `pytest tests/test_brand_validator.py -v`**.
- [ ] **Step 5: Commit `git add skills/brand-validator/ tests/golden/brand-validator/ tests/test_brand_validator.py && git commit -m "feat: add brand-validator Skill"`**.

---

### Task 5: Projection Integration Update

**Files:**
- Modify: `skills/resume-projection/SKILL.md`
- Modify: `skills/cover-letter-projection/SKILL.md`
- Modify: `skills/linkedin-projection/SKILL.md`

- [ ] **Step 1: Update `skills/resume-projection/SKILL.md`** to consume `okf/positioning-statements.md`.
- [ ] **Step 2: Update `skills/cover-letter-projection/SKILL.md`** to consume `okf/messaging-library.md`.
- [ ] **Step 3: Update `skills/linkedin-projection/SKILL.md`** to consume `okf/executive-identity.md`.
- [ ] **Step 4: Run projection tests `pytest tests/test_resume_projection.py tests/test_cover_letter_projection.py tests/test_linkedin_projection.py -v`**.
- [ ] **Step 5: Commit `git add skills/resume-projection/ skills/cover-letter-projection/ skills/linkedin-projection/ && git commit -m "feat: update projection skills to consume canonical Executive Identity"`**.

---

### Task 6: Orchestrator & Configuration Update

**Files:**
- Modify: `config/config.example.yaml`
- Modify: `config/config.yaml`
- Modify: `skills/playbook-orchestrator/SKILL.md`
- Modify: `tests/test_skills.py`

- [ ] **Step 1: Bump version to `"0.5"` in `config/config.example.yaml` & `config/config.yaml`**.
- [ ] **Step 2: Update `skills/playbook-orchestrator/SKILL.md`** for 17-step pipeline.
- [ ] **Step 3: Update `tests/test_skills.py`** asserting all 25 skills exist.
- [ ] **Step 4: Run tests `pytest tests/test_skills.py -v`**.
- [ ] **Step 5: Commit `git add config/ skills/playbook-orchestrator/ tests/test_skills.py && git commit -m "feat: update pipeline orchestrator and config for v0.5"`**.

---

### Task 7: System Documentation Updates

**Files:**
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `ARCHITECTURE.md`
- Modify: `README.md`

- [ ] **Step 1: Update documentation files for v0.5**.
- [ ] **Step 2: Run test suite `pytest tests/ -v`**.
- [ ] **Step 3: Commit `git add AGENTS.md CLAUDE.md ARCHITECTURE.md README.md && git commit -m "docs: update system documentation for v0.5 Executive Narrative & Personal Brand Engine"`**.

---

### Task 8: End-to-End Success Criteria Verification

**Files:**
- Create: `tests/test_v05_success_criteria.py`

- [ ] **Step 1: Create `tests/test_v05_success_criteria.py`** asserting all Sprint 5 success criteria.
- [ ] **Step 2: Run full test suite `pytest tests/ -v`**.
- [ ] **Step 3: Commit `git add tests/test_v05_success_criteria.py && git commit -m "test: add v0.5 success criteria checks"`**.
