# Implementation Plan: Opportunity-Scoped Pipeline Outputs (`out/<target-slug>/`)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scope all opportunity-specific outputs (runtime analysis, validation reports, and presentation views) under `out/<target-slug>/` derived from `target_opportunity.source`, leaving `out/okf/` as the shared canonical career knowledge graph.

---

## File Structure

### Modified Skills & Docs
```
skills/opportunity-analyzer/SKILL.md
skills/projection-registry/SKILL.md
skills/resume-projection/SKILL.md
skills/cover-letter-projection/SKILL.md
skills/linkedin-projection/SKILL.md
skills/opportunity-alignment-view/SKILL.md
skills/executive-brief-view/SKILL.md
skills/playbook-assembler/SKILL.md
skills/projection-validator/SKILL.md
skills/brand-validator/SKILL.md
skills/playbook-orchestrator/SKILL.md
tests/test_opportunity_analyzer.py
tests/test_projection_registry.py
tests/test_v04_success_criteria.py
tests/test_v05_success_criteria.py
AGENTS.md
CLAUDE.md
ARCHITECTURE.md
README.md
```

---

## Tasks

### Task 1: Update Target Opportunity Analyzer & Projection Registry Skills

**Files:**
- Modify: `skills/opportunity-analyzer/SKILL.md`
- Modify: `skills/projection-registry/SKILL.md`
- Modify: `tests/test_opportunity_analyzer.py`
- Modify: `tests/test_projection_registry.py`

- [ ] **Step 1: Update `skills/opportunity-analyzer/SKILL.md`** to derive `<target-slug>` from `target_opportunity.source` and emit `out/<target-slug>/runtime/opportunity-analysis.yaml`.
- [ ] **Step 2: Update `skills/projection-registry/SKILL.md`** to direct outputs into `out/<target-slug>/`.
- [ ] **Step 3: Update `tests/test_opportunity_analyzer.py` and `tests/test_projection_registry.py`**.
- [ ] **Step 4: Run tests `pytest tests/test_opportunity_analyzer.py tests/test_projection_registry.py -v`**.
- [ ] **Step 5: Commit `git add skills/opportunity-analyzer/ skills/projection-registry/ tests/ && git commit -m "feat: update opportunity-analyzer and projection-registry for target-slug scoping"`**.

---

### Task 2: Update Projection & View Skills for Opportunity Subdirectory Output

**Files:**
- Modify: `skills/resume-projection/SKILL.md`
- Modify: `skills/cover-letter-projection/SKILL.md`
- Modify: `skills/linkedin-projection/SKILL.md`
- Modify: `skills/opportunity-alignment-view/SKILL.md`
- Modify: `skills/executive-brief-view/SKILL.md`
- Modify: `skills/playbook-assembler/SKILL.md`
- Modify: `skills/projection-validator/SKILL.md`
- Modify: `skills/brand-validator/SKILL.md`

- [ ] **Step 1: Update `skills/resume-projection/SKILL.md`, `cover-letter-projection/SKILL.md`, and `linkedin-projection/SKILL.md`**.
- [ ] **Step 2: Update `skills/opportunity-alignment-view/SKILL.md`, `executive-brief-view/SKILL.md`, and `playbook-assembler/SKILL.md`**.
- [ ] **Step 3: Update `skills/projection-validator/SKILL.md` and `brand-validator/SKILL.md`**.
- [ ] **Step 4: Run tests `pytest tests/test_*_projection.py tests/test_*_view.py -v`**.
- [ ] **Step 5: Commit `git add skills/ tests/ && git commit -m "feat: update projection and view skills for opportunity-scoped out/<target-slug>/ outputs"`**.

---

### Task 3: Update Orchestrator, Documentation & Test Suite

**Files:**
- Modify: `skills/playbook-orchestrator/SKILL.md`
- Modify: `tests/test_v04_success_criteria.py`
- Modify: `tests/test_v05_success_criteria.py`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `ARCHITECTURE.md`
- Modify: `README.md`

- [ ] **Step 1: Update `skills/playbook-orchestrator/SKILL.md`** to document `out/<target-slug>/`.
- [ ] **Step 2: Update `tests/test_v04_success_criteria.py` and `tests/test_v05_success_criteria.py`**.
- [ ] **Step 3: Update `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `README.md`**.
- [ ] **Step 4: Run full test suite `pytest -v`**.
- [ ] **Step 5: Commit `git add skills/playbook-orchestrator/ tests/ AGENTS.md CLAUDE.md ARCHITECTURE.md README.md && git commit -m "feat: complete opportunity-scoped output architecture"`**.
