---
name: cas-audit-agent-rules
description: Audit, deduplicate, and optimize agent instruction and rules files (AGENTS.md, GEMINI.md, .agents/rules/*.md) for token economy, discoverability, progressive disclosure, and governance invariants. Use when asked to review agent rules, optimize AGENTS.md, eliminate duplicate agent instructions, or enforce repository rule hygiene.
---

# Skill: cas-audit-agent-rules

## Intent
Audit, streamline, and optimize repository-level agent instruction files (`AGENTS.md`, `GEMINI.md`, and `.agents/rules/*.md`) in accordance with the **Antigravity Customization System** and open ecosystem standards (`skills.sh`).

The goal is to maintain a crisp, authoritative Single Source of Truth (SSOT) that maximizes model comprehension, respects the context token budget, and enforces architectural guardrails without injecting stale or bloated instructions.

---

## When to Use This Skill
- The user asks to "review AGENTS.md", "audit agent instructions", or "optimize repository rules".
- When token usage from always-on rules is excessively high or approaching the 20,000-token rules budget.
- When multiple agent instruction files (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`) have drifted out of sync or duplicate identical text.
- When an agent instruction file has accumulated stale, ephemeral pointers (such as references to completed feature specifications or historical branches).
- When procedural code blocks and runbooks need to be extracted from always-on rules into on-demand skills.

## When NOT to Use This Skill
- Implementing production software features or refactoring codebase modules (use `cas-add-or-modify-feature` or `cas-refactor-module`).
- Synchronizing external ArchGov reviews (use `cas-sync-archgov-reviews`).
- Writing feature-specific implementation specifications (use `speckit-plan` / `speckit-specify`).

---

## The 5-Point Rule Audit Framework

When executing this skill, evaluate the target instruction files against the following five core dimensions:

### 1. Single Source of Truth & Deduplication
- **Principle**: An agent environment should never load the same instructions twice.
- **Check**: Verify whether both `AGENTS.md` and `GEMINI.md` exist as separate static files at the repository root.
- **Remediation**:
  - Designate `AGENTS.md` as the authoritative canonical SSOT.
  - Symlink tool-specific files to `AGENTS.md` (e.g., `ln -sf AGENTS.md GEMINI.md`).
  - Antigravity deduplicates rule files matching identical resolved inode paths, avoiding double token consumption.

### 2. Token Budget & Size Compliance
- **Principle**: Always-on rules must stay strictly within the Antigravity per-file and aggregate budgets.
- **Limits**:
  - **Per-file limit**: Max `24,000 bytes` (~24 KB) per rule file.
  - **Aggregate budget**: Always-on rules share a `20,000 token` pool (`defaultRulesBudget`).
- **Remediation**: Remove wordy commentary, compress verbose guidelines into bulleted constraints, and keep root files under 10 KB.

### 3. Progressive Disclosure (Rules vs. Skills)
- **Principle**: **Rules** enforce active constraints and negative boundaries (what *not* to do, mandatory gates). **Skills** provide executable, multi-step runbooks on demand.
- **Check**: Look for inline code templates (e.g., Python mock setups, JSON validation snippets) or 10-step CLI workflows embedded directly in root rules.
- **Remediation**:
  - Replace procedural code snippets with references to existing codebase fixtures/examples.
  - Move complex operational workflows (e.g., external ArchGov publishing) into dedicated on-demand skills (`.agents/skills/<skill>/SKILL.md`).

### 4. Discoverability Filtering
- **Principle**: Don't instruct the model on patterns it can trivially discover from project files or default coding standards.
- **Check**: Look for generic guidance (e.g., "use 4 spaces in Python", "name files in snake_case", "write clear docstrings").
- **Remediation**: Prune standard language defaults. Retain only non-obvious repository-specific rules, such as custom virtual environment flags (`uv run --active pytest -k "not trio"`), two-phase commit sequences, or mandatory schema formats.

### 5. Ephemeral Hygiene
- **Principle**: Repository rules are permanent architectural guidelines; they must never contain temporary context.
- **Check**: Look for hardcoded links to specific completed feature specs (`specs/<id>/plan.md`), temporary branches, or developer-specific notes.
- **Remediation**: Remove point-in-time links and replace them with structural patterns (e.g., *"When working on a feature, inspect the active specification under `specs/<feature-id>/`"*).

---

## Step-by-Step Execution Workflow

```
┌────────────────────────────────┐
│ Phase 1: Inventory & Discovery │
└──────────────┬─────────────────┘
               │ Scan AGENTS.md, GEMINI.md, .agents/rules/
               ▼
┌────────────────────────────────┐
│ Phase 2: 5-Point Gap Analysis  │
└──────────────┬─────────────────┘
               │ Evaluate SSOT, Token Budget, Progressive Disclosure, Discoverability, Hygiene
               ▼
┌────────────────────────────────┐
│ Phase 3: Interactive Alignment │
└──────────────┬─────────────────┘
               │ Confirm remediation options with the user (Alex)
               ▼
┌────────────────────────────────┐
│ Phase 4: Refactor & Symlink    │
└──────────────┬─────────────────┘
               │ Write lean AGENTS.md, symlink GEMINI.md -> AGENTS.md
               ▼
┌────────────────────────────────┐
│ Phase 5: Verification          │
└────────────────────────────────┘
               │ Check file sizes, git status, and governance validation
```

### Phase 1: Inventory & Discovery
1. Check existing rule files:
   ```bash
   ls -la AGENTS.md GEMINI.md .agents/rules/
   ```
2. Measure file sizes and check for symlinks.

### Phase 2: 5-Point Gap Analysis
Review file contents against the 5 dimensions. Produce an audit summary highlighting:
- Total size and approximate token count.
- Overlap between `AGENTS.md` and `GEMINI.md`.
- Procedural code blocks candidates for extraction into skills.
- Stale spec links or temporary blocks.

### Phase 3: Interactive Alignment
Present findings to the architect with clear, numbered options:
- Option A: Symlink strategy for `GEMINI.md`.
- Option B: Trimming procedural code blocks vs. keeping inline.
- Option C: Core architecture overview integration.

### Phase 4: Refactor & Symlink
1. Update `AGENTS.md` with streamlined, high-signal invariants and boundaries.
2. Establish the symlink:
   ```bash
   ln -sf AGENTS.md GEMINI.md
   ```
3. Ensure all mandatory governance invariants are preserved (e.g., critical SDD/TDD enforcement banner, 4-tier transitive lineage, ADR schema invariants, two-phase commit sequence).

### Phase 5: Verification
1. Verify the symlink and file sizes:
   ```bash
   ls -l AGENTS.md GEMINI.md
   ```
2. Verify git status:
   ```bash
   git status -s AGENTS.md GEMINI.md
   ```
3. Run governance validation if applicable:
   ```bash
   uv run cas governance validate --project <project>
   ```
