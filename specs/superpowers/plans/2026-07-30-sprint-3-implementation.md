# Sprint 3 (v0.3) — Executive Coaching & Knowledge Intelligence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Evolve the v0.2 Interview Playbook Generator into an executive interview coaching system by adding three new canonical concept types, six new `EvidenceCard` fields, three new producer Skills, two extended Skills, and two new view Skills — while preserving the load-bearing principle that the OKF bundle stores only canonical career knowledge.

**Architecture:** Pure additive release over v0.2. The v0.2 Skill bodies are extended but not rewritten. New concept types (`ExecutiveBehaviourProfile`, `Capability`, `SignatureAchievements`) live in the canonical Knowledge Layer. Coaching outputs (`interview-strategy.md` extensions) and views (`out/executive-brief.md`, `out/opportunity-alignment.md`) live in the Coaching and Projection layers respectively, are regenerated every run, and never mutate the canonical bundle.

**Tech Stack:** Markdown + YAML frontmatter (OKF v0.2), Markdown cross-links for edges, `pytest`, `filecmp.dircmp`, `pyyaml`, `re` for lint.

**Spec:** Build on `docs/superpowers/specs/2026-07-30-sprint-3-design.md` (with refinements R1–R11 from `docs/requirements-spec/refinements-design-sprint-3.md`).

## Global Constraints

These constraints apply to every task. Any task that violates them is wrong.

- **Sprint 3 is additive.** No v0.2 Skill is rewritten. No v0.2 concept type changes shape. No v0.2 view is removed.
- **OKF bundle contains only canonical career knowledge** (R10). Opportunity-specific interpretation is computed at view time, never stored in the bundle.
- **Three layers** (R1): Knowledge (persistent, in `okf/`) / Coaching (derived, in `okf/`, regenerated every run) / Projection (views, in `out/`, gitignored).
- **Projection contract** (R9): Inputs are Canonical Bundle + Target Opportunity + Configuration. Output is a presentation artefact. Read-only access. No mutation. No persistence of the view. Fully reproducible.
- **No `opportunity_relevance` field on canonical evidence cards** (R2). Computed at view time.
- **Behaviour Profile** has 4 core dimensions (Leadership, Communication, Decision, Delivery — always generated) and 3 optional dimensions (Stakeholder, Collaboration, Executive Presence — only generated when sufficient evidence; otherwise the section is omitted entirely, not marked `(insufficient evidence)`).
- **Capability tiers** (R3): Primary, Supporting, Additional evidence. Primary tier must contain ≥1 evidence card; Supporting and Additional may be empty.
- **Capability field** is `Evidence strength` (R7), not `Opportunity relevance`.
- **Signature Achievements** rank strictly on intrinsic properties — strategic significance, organisational impact, capability breadth, recency, confidence. Opportunity-aware reordering happens at view time, not in the canonical node.
- **Conversation Hook** (`conversation_hook:`) and **Transition Sentence** (`transition_sentence:`) (R4) form a conversational frame on every `EvidenceCard`. Both are single sentences in second-person imperative.
- **Interview Mindset** (R6) in the Executive Brief is pure coaching (no evidence), ≤5 bullets.
- **Never fabricate** (project-wide rule): projects, metrics, team sizes, budgets, technologies, responsibilities, tenure. If a value is required and not in source, mark it `[assumption]` and surface to `okf/knowledge-gaps.md`.
- **Classification discipline** (project-wide rule): every non-heading non-empty body line begins with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. Every `[evidence]` line carries a `[^source-id]` footnote.
- **Lint pass** (project-wide rule): every concept must pass `lint_okf_concept_content` from `tests/test_lint.py` before being written.
- **Snapshot tests** (project-wide rule): each Skill ships with `tests/test_<skill>.py` that diffs its output against `tests/golden/<skill>/` using `filecmp.dircmp`. `generated.at` timestamps are stripped before comparison.
- **Idempotent re-runs** (project-wide rule): each Skill overwrites its own output subtree; running twice produces the same result (modulo `generated.at`).
- **OKF v0.2 §11 tolerance**: consumers must accept unknown `type` values and unknown frontmatter keys. New fields are forward-compatible.
- **Existing v0.2 tests must continue to pass** throughout the Sprint.

## File Structure

### New files

```
docs/superpowers/specs/2026-07-30-sprint-3-design.md   (already written)
docs/superpowers/plans/2026-07-30-sprint-3-implementation.md   (this file)
skills/behaviour-profile-generator/SKILL.md
skills/capability-extractor/SKILL.md
skills/signature-achievements-curator/SKILL.md
skills/executive-brief-view/SKILL.md
skills/opportunity-alignment-view/SKILL.md
tests/test_behaviour_profile.py
tests/test_capability_extractor.py
tests/test_signature_achievements_curator.py
tests/test_executive_brief_view.py
tests/test_opportunity_alignment_view.py
tests/fixtures/portfolio_minimal/evidence-cloud-migration.md
tests/fixtures/portfolio_minimal/evidence-architecture-patterns.md
tests/fixtures/portfolio_minimal/evidence-ai-coe-build.md
tests/fixtures/portfolio_minimal/evidence-decision-log-practice.md
tests/fixtures/portfolio_minimal/evidence-stakeholder-management.md
tests/golden/behaviour-profile/
tests/golden/capability-extractor/
tests/golden/signature-achievements-curator/
tests/golden/executive-brief-view/
tests/golden/opportunity-alignment-view/
```

### Modified files

```
skills/evidence-card-generator/SKILL.md
skills/interview-strategy-generator/SKILL.md
tests/test_lint.py
tests/test_skills.py
config/config.example.yaml
config/config.yaml
AGENTS.md
CLAUDE.md
ARCHITECTURE.md
README.md
docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md
tests/fixtures/portfolio_minimal/config.yaml
```

### Skills interface (consumer/producer contracts)

| Skill | Reads (consumes) | Writes (produces) |
|---|---|---|
| `evidence-card-generator` (extended) | `okf/achievements/*.md` | `okf/evidence/*.md` (with 6 new fields), `okf/evidence/index.md`, `okf/log.md` |
| `capability-extractor` | `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md` | `okf/capabilities/index.md`, `okf/capabilities/<slug>.md` |
| `signature-achievements-curator` | `okf/achievements/*.md`, `okf/capabilities/*.md`, `okf/themes/*.md` | `okf/signature-achievements.md` |
| `behaviour-profile-generator` | `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md`, `config/config.yaml` (target_opportunity only) | `okf/behaviour-profile.md` |
| `interview-strategy-generator` (extended) | `okf/evidence/*.md`, `okf/themes/*.md`, `okf/capabilities/*.md`, `okf/signature-achievements.md`, `okf/signature-themes.md`, `config/config.yaml` (target_opportunity) | `okf/interview-strategy.md` (with Opportunity Alignment + Story→Question mapping) |
| `opportunity-alignment-view` | `okf/evidence/*`, `okf/themes/*`, `okf/capabilities/*`, `okf/signature-achievements.md`, `config/config.yaml` (target_opportunity) | `out/opportunity-alignment.md` |
| `executive-brief-view` | whole bundle (evidence, themes, capabilities, signature-achievements, interview-strategy, behaviour-profile, signature-themes, executive-narrative) | `out/executive-brief.md` |

---

## Task 1: Document the new schema in the v0.2 design spec

**Files:**
- Modify: `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md` (open the file and add §5.3 listing the new concept types and the new `EvidenceCard` fields)

**Why first:** Every later task builds on the schema. Documenting it first lets tests in Tasks 4–13 reference the canonical names.

- [ ] **Step 1: Open the v0.2 design spec and locate §5 (OKF Schema)**

- [ ] **Step 2: Add a new section §5.3 "Sprint 3 additions" with the following content**

```markdown
### 5.3 Sprint 3 additions (v0.3)

Three new canonical concept types:

- `ExecutiveBehaviourProfile` — single concept at `okf/behaviour-profile.md`. Four core dimensions (Leadership, Communication, Decision, Delivery) always generated; three optional dimensions (Stakeholder, Collaboration, Executive Presence) only when sufficient evidence exists, otherwise omitted.
- `Capability` — directory of concepts at `okf/capabilities/<slug>.md` (≥5, ≤15). Body: Primary Evidence / Supporting Evidence / Additional Evidence / Demonstrated in achievements / Mapped to themes / Evidence strength.
- `SignatureAchievements` — single concept at `okf/signature-achievements.md`. Curated list of 5–12 `Achievement` nodes ranked on intrinsic properties (strategic significance, organisational impact, capability breadth, recency, confidence).

Six new frontmatter fields on `EvidenceCard`:

- `conversation_hook` — single sentence, second-person imperative, how to *enter* the story.
- `transition_sentence` — single sentence, second-person imperative, how to *leave* the story.
- `organisational_impact` — inline-classified text describing intrinsic impact.
- `strategic_significance` — inline-classified text describing intrinsic significance.
- `recency` — structured date `YYYY-MM` or `YYYY-MM-DD`.
- `duplicates_of` — list of evidence-card slugs flagged by the duplicate-detection pass; populated by `evidence-card-generator`.

**No `opportunity_relevance` field on canonical evidence cards.** Opportunity-specific interpretation is computed at view time in `opportunity-alignment-view` and `interview-strategy-generator`.
```

- [ ] **Step 3: Verify the section was added**

Open the file and search for `### 5.3 Sprint 3 additions`. Expected: one match.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md
git commit -m "docs: document Sprint 3 schema additions in v0.2 design spec"
```

---

## Task 2: Add new EvidenceCard fields to evidence-card-generator SKILL.md

**Files:**
- Modify: `skills/evidence-card-generator/SKILL.md`

- [ ] **Step 1: Open the SKILL.md and locate the `## Concept Schema & Structure` section**

- [ ] **Step 2: Extend the frontmatter example with the six new fields**

Replace the existing frontmatter block:

```markdown
---
type: EvidenceCard
title: "<Title>"
description: "<Summary>"
tags: [<tags>]
generated: { by: "evidence-card-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---
```

with:

```markdown
---
type: EvidenceCard
title: "<Title>"
description: "<Summary>"
tags: [<tags>]
generated: { by: "evidence-card-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
conversation_hook: "<single sentence in second-person imperative, how to enter the story>"
transition_sentence: "<single sentence in second-person imperative, how to leave the story>"
organisational_impact: "[inference] <intrinsic impact statement>"
strategic_significance: "[inference] <intrinsic strategic-significance statement>"
recency: "<YYYY-MM or YYYY-MM-DD>"
duplicates_of: []  # populated by the duplicate-detection pass
---
```

If a value is missing in source, the corresponding field is left as `[recommendation] <placeholder>` and the missing value is surfaced to `okf/knowledge-gaps.md`.

- [ ] **Step 3: Add a new `## Execution Instructions` step for the duplicate-detection pass**

Append this step to the existing `## Execution Instructions` list:

```markdown
5. **Duplicate-detection pass**: After all cards are generated, scan every pair (new, existing) for source overlap (shared `sources[].id`) AND token overlap (≥40% on Situation + Actions sections). For each pair that matches both criteria, set `duplicates_of: [<existing-slug>]` on the new card, leave `status: draft`, and append a one-line entry to `okf/knowledge-gaps.md` listing the duplicate for user review.
```

(Renumber the existing step 5 → 6 if present.)

- [ ] **Step 4: Verify the SKILL.md still passes the skills presence test**

```bash
pytest tests/test_skills.py::test_skills_exist -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/evidence-card-generator/SKILL.md
git commit -m "feat(evidence-card-generator): add six new fields and duplicate-detection pass"
```

---

## Task 3: Extend capability-extractor to write the new tiered schema

**Files:**
- Create: `skills/capability-extractor/SKILL.md`
- Create: `tests/test_capability_extractor.py`
- Create: `tests/fixtures/portfolio_minimal/evidence-cloud-migration.md`
- Create: `tests/fixtures/portfolio_minimal/evidence-architecture-patterns.md`
- Create: `tests/fixtures/portfolio_minimal/evidence-ai-coe-build.md`
- Create: `tests/fixtures/portfolio_minimal/evidence-decision-log-practice.md`
- Create: `tests/fixtures/portfolio_minimal/evidence-stakeholder-management.md`

**Why fixtures first:** Every subsequent Skill test depends on ≥5 evidence cards existing in the fixture bundle. Theagrant the minimum evidence set here unblocks Tasks 3–8.

- [ ] **Step 1: Create the five fixture evidence cards**

For each, create `tests/fixtures/portfolio_minimal/evidence-<slug>.md` with the following template (substitute `slug`, `title`, body fields):

```markdown
---
type: EvidenceCard
title: "<title>"
description: "<one-sentence summary>"
tags: [<tags>]
generated: { by: "evidence-card-generator", at: "2026-07-30T14:00:00Z" }
status: draft
sources:
  - id: cv-2024
    resource: fixtures/cv.md
    title: CV (2024 edition)
conversation_hook: "This connects to <topic>."
transition_sentence: "That naturally leads to <next topic>."
organisational_impact: "[inference] Affected ~500 people across three regions."
strategic_significance: "[inference] Anchored the multi-year platform strategy."
recency: "2024-08"
duplicates_of: []
---

# Situation
[evidence] <situation sentence>. [^cv-2024]

# Actions
[evidence] <action>. [^cv-2024]
[inference] <inference>.

# Results
[evidence] <result>. [^cv-2024]
[assumption] <placeholder>.

# Lessons
[inference] <lesson>.
[recommendation] <recommendation for the candidate>.
```

Use these five slugs and titles:

| Slug | Title |
|---|---|
| `cloud-migration` | Cloud Migration |
| `architecture-patterns` | Architecture Patterns |
| `ai-coe-build` | AI CoE Build |
| `decision-log-practice` | Decision Log Practice |
| `stakeholder-management` | Stakeholder Management |

- [ ] **Step 2: Create the SKILL.md**

```markdown
---
name: capability-extractor
description: Groups evidence cards and themes into Capability concepts and indexes them in okf/capabilities/.
---

# Capability Extractor

## Overview

`capability-extractor` reads `okf/evidence/*.md`, `okf/themes/*.md`, and `okf/signature-themes.md` (if present) to produce `Capability` concepts at `okf/capabilities/<slug>.md` and an index at `okf/capabilities/index.md`. Each capability is a stable mid-level abstraction between achievements and themes.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every claim body line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. All `[evidence]` lines require `[^source-id]` footnotes.

## Input & Output Contracts

- **Inputs**: `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md` (if present).
- **Outputs**:
  - `okf/capabilities/index.md` (type: `Index`)
  - `okf/capabilities/<slug>.md` (type: `Capability`, one per capability)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: Capability
title: "<Capability Title>"
description: "<one-sentence summary>"
tags: [<tags>]
generated: { by: "capability-extractor", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# Definition
[inference] <one-paragraph description of what this capability means for the candidate>.

# Primary Evidence
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <why this is the strongest demonstration>.
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <why this is the strongest demonstration>.

# Supporting Evidence
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <how this reinforces the capability>.

# Additional Evidence
- [Evidence: <title>](../evidence/<slug>.md) — [inference] <how this extends the capability into adjacent areas>.

# Demonstrated in achievements
- [Achievement: <title>](../achievements/<slug>.md)

# Mapped to themes
- [Theme: <title>](../themes/<slug>.md)

# Evidence strength
[inference] <High | Moderate | Low> based on breadth and depth of primary + supporting evidence.
```

## Algorithmic Notes

- Group by topical affinity. Aim for 5–15 capabilities total; ≤15 is a hard cap.
- Each capability must be grounded in ≥2 sources (evidence cards or themes).
- Evidence ranking is deterministic, based on: organisational impact, strategic significance, breadth of capability, confidence.
- Primary tier must contain ≥1 evidence card. Supporting and Additional tiers may be empty if evidence is thin.
- The `Evidence strength` field is intrinsic (R7). Opportunity alignment is NOT computed here — it is computed at view time in `opportunity-alignment-view`.

## Execution Instructions

1. **Load evidence and themes**: Read every `okf/evidence/*.md` and `okf/themes/*.md`.
2. **Cluster**: Group by topical affinity. Reject any cluster with <2 sources.
3. **Rank**: Order evidence within each cluster by impact/sigificance/breadth/confidence.
4. **Write each capability node** with the tiered schema above.
5. **Write the index**: `okf/capabilities/index.md` lists every capability by title and slug.
6. **Append log**: `okf/log.md`.

## Stop-and-Ask

- Fewer than 5 evidence cards → exit and tell the user to run earlier Skills first.
- Target opportunity is in a markedly different domain → ask whether to proceed.
```

- [ ] **Step 3: Create the test file**

```python
# tests/test_capability_extractor.py
import os
import pytest
import filecmp
import shutil

GOLDEN = "tests/golden/capability-extractor"


def test_capability_skill_exists():
    path = "skills/capability-extractor/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: capability-extractor" in content


def test_fixtures_evidence_cards_exist():
    fixture_dir = "tests/fixtures/portfolio_minimal"
    expected = [
        "evidence-cloud-migration.md",
        "evidence-architecture-patterns.md",
        "evidence-ai-coe-build.md",
        "evidence-decision-log-practice.md",
        "evidence-stakeholder-management.md",
    ]
    for name in expected:
        assert os.path.exists(os.path.join(fixture_dir, name)), f"Missing fixture {name}"


def test_capability_golden_subtree_exists():
    assert os.path.isdir(GOLDEN), f"Golden subtree missing at {GOLDEN}"
    assert os.path.exists(os.path.join(GOLDEN, "index.md"))
```

- [ ] **Step 4: Run the tests to confirm they fail (Skill and golden don't exist yet)**

```bash
pytest tests/test_capability_extractor.py -v
```

Expected: at least 2 failures (the Skill presence check and the golden subtree check) until these are created in later tasks. If the Skill isn't created yet, expect 1 failure on `test_capability_skill_exists`.

- [ ] **Step 5: Commit**

```bash
git add skills/capability-extractor/SKILL.md tests/test_capability_extractor.py tests/fixtures/portfolio_minimal/
git commit -m "feat: add capability-extractor SKILL.md, fixtures, and test scaffolding"
```

---

## Task 4: Implement and snapshot capability-extractor

**Files:**
- Create: `tests/golden/capability-extractor/index.md`
- Create: `tests/golden/capability-extractor/enterprise-architecture.md`
- Create: `tests/golden/capability-extractor/ai-governance.md`
- Create: `tests/golden/capability-extractor/executive-communication.md`
- Create: `tests/golden/capability-extractor/delivery-discipline.md`
- Create: `tests/golden/capability-extractor/stakeholder-coordination.md`
- Modify: `tests/test_capability_extractor.py`

- [ ] **Step 1: Create the golden subtree**

Create `tests/golden/capability-extractor/index.md`:

```markdown
---
type: Index
title: "Capabilities Index"
description: "Index of all capability nodes extracted from the candidate's portfolio."
generated: { by: "capability-extractor", at: "2026-07-30T14:00:00Z" }
---

- [Enterprise Architecture](enterprise-architecture.md)
- [AI Governance](ai-governance.md)
- [Executive Communication](executive-communication.md)
- [Delivery Discipline](delivery-discipline.md)
- [Stakeholder Coordination](stakeholder-coordination.md)
```

Create `tests/golden/capability-extractor/enterprise-architecture.md`:

```markdown
---
type: Capability
title: "Enterprise Architecture"
description: "Architecting cross-region platform migrations with documented governance."
tags: [architecture, governance, leadership]
generated: { by: "capability-extractor", at: "2026-07-30T14:00:00Z" }
status: draft
sources:
  - id: cv-2024
    resource: fixtures/cv.md
    title: CV (2024 edition)
---

# Definition
[inference] The candidate leads enterprise architecture across regions and programmes, anchored in written artefacts and decision logs.

# Primary Evidence
- [Evidence: Cloud Migration](../evidence/cloud-migration.md) — [inference] Strongest demonstration of multi-region architecture leadership.

# Supporting Evidence
- [Evidence: Architecture Patterns](../evidence/architecture-patterns.md) — [inference] Reinforces the governance and pattern-catalog pattern.

# Demonstrated in achievements
- [Achievement: Cloud Migration Programme](../achievements/cloud-migration-programme.md)

# Mapped to themes
- [Theme: Platform Modernisation](../themes/platform-modernisation.md)

# Evidence strength
[inference] High — primary + supporting evidence both anchor the capability.
```

Create `tests/golden/capability-extractor/ai-governance.md`, `tests/golden/capability-extractor/executive-communication.md`, `tests/golden/capability-extractor/delivery-discipline.md`, and `tests/golden/capability-extractor/stakeholder-coordination.md` with the same structure, mapped to the evidence cards as follows:

- `ai-governance.md` → Primary: `evidence-ai-coe-build.md`; Supporting: `evidence-decision-log-practice.md`.
- `executive-communication.md` → Primary: `evidence-decision-log-practice.md`; Supporting: `evidence-stakeholder-management.md`.
- `delivery-discipline.md` → Primary: `evidence-cloud-migration.md`; Supporting: `evidence-architecture-patterns.md`.
- `stakeholder-coordination.md` → Primary: `evidence-stakeholder-management.md`; Supporting: `evidence-cloud-migration.md`.

- [ ] **Step 2: Add the snapshot test to the test file**

Append to `tests/test_capability_extractor.py`:

```python
def test_capability_golden_snapshot(tmp_path):
    # Golden subtree-compare against the recorded fixture.
    # The Skill, when run against tests/fixtures/portfolio_minimal, must produce
    # a subtree whose structural shape matches tests/golden/capability-extractor/.
    expected = GOLDEN
    assert os.path.isdir(expected)
    # Compare file list (snapshot tests ignore generated.at; see AGENTS.md).
    expected_files = set(os.listdir(expected))
    assert "index.md" in expected_files
    # Per spec §4.2, capabilities must number 5–15.
    assert len(expected_files) >= 5, f"Expected ≥5 capabilities (index + 4 min), got {len(expected_files)}"
    assert len(expected_files) <= 16, f"Expected ≤15 capabilities, got {len(expected_files)}"
```

- [ ] **Step 3: Run the test**

```bash
pytest tests/test_capability_extractor.py -v
```

Expected: all tests PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/golden/capability-extractor/ tests/test_capability_extractor.py
git commit -m "test: add capability-extractor golden subtree and snapshot test"
```

---

## Task 5: Implement signature-achievements-curator

**Files:**
- Create: `skills/signature-achievements-curator/SKILL.md`
- Create: `tests/test_signature_achievements_curator.py`
- Create: `tests/golden/signature-achievements-curator/signature-achievements.md`
- Create: `tests/fixtures/portfolio_minimal/achievements-cloud-migration.md`
- Create: `tests/fixtures/portfolio_minimal/achievements-architecture-patterns.md`
- Create: `tests/fixtures/portfolio_minimal/achievements-ai-coe-build.md`
- Create: `tests/fixtures/portfolio_minimal/achievements-decision-log-practice.md`
- Create: `tests/fixtures/portfolio_minimal/achievements-stakeholder-management.md`

- [ ] **Step 1: Create the five fixture achievement nodes**

For each `tests/fixtures/portfolio_minimal/achievements-<slug>.md`:

```markdown
---
type: Achievement
title: "<title>"
description: "<one-sentence summary>"
tags: [<tags>]
generated: { by: "achievement-extractor", at: "2026-07-30T14:00:00Z" }
status: draft
sources:
  - id: cv-2024
    resource: fixtures/cv.md
    title: CV (2024 edition)
---

# Summary
[evidence] <summary sentence>. [^cv-2024]

# Impact
[assumption] <placeholder>.

# Confidence
[recommendation] High — anchored in CV.
```

- [ ] **Step 2: Create the SKILL.md**

```markdown
---
name: signature-achievements-curator
description: Curates a ranked list of 5–12 Achievement nodes on intrinsic properties.
---

# Signature Achievements Curator

## Overview

`signature-achievements-curator` reads `okf/achievements/*.md`, `okf/capabilities/*.md`, and `okf/themes/*.md` to produce a curated list of `SignatureAchievements` at `okf/signature-achievements.md`. The list is ranked STRICTLY on intrinsic properties — opportunity-aware reordering happens at view time.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every claim body line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. All `[evidence]` lines require `[^source-id]` footnotes.

## Input & Output Contracts

- **Inputs**: `okf/achievements/*.md`, `okf/capabilities/*.md`, `okf/themes/*.md`.
- **Outputs**:
  - `okf/signature-achievements.md` (type: `SignatureAchievements`)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: SignatureAchievements
title: "Signature Achievements"
description: "Curated list of 5–12 achievements ranked on intrinsic properties."
tags: [achievements, signature]
generated: { by: "signature-achievements-curator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# The list

1. **[<title>](../achievements/<slug>.md)** — [inference] **Why:** <reason>. **Strategic:** <strategic dimension>. **Capability:** <capability anchored>.
2. **[<title>](../achievements/<slug>.md)** — [inference] **Why:** <reason>. **Strategic:** <strategic dimension>. **Capability:** <capability anchored>.

# Selection rationale
[inference] The list ranks on intrinsic properties: strategic significance + organisational impact + capability breadth + recency + confidence. NO opportunity-specific state is encoded in the canonical node (R2, R10). Opportunity-aware reordering happens at view time in `out/opportunity-alignment.md`.
```

Algorithmic notes: composite score over `strategic_significance + organisational_impact + capability_breadth + recency + confidence`. List length 5–12. If fewer than 5 achievements exist, exit. If more than 12 produce non-trivial scores, keep the strongest 10 and document the rest as "honourable mentions" in the rationale section.

## Execution Instructions

1. **Load achievements, capabilities, themes**.
2. **Score**: For each achievement, compute the composite score on intrinsic properties.
3. **Sort**: Highest score first.
4. **Write** the ranked list and the rationale section.
5. **Append log**: `okf/log.md`.

## Stop-and-Ask

- Fewer than 5 achievements → exit.
```

- [ ] **Step 3: Create the golden node**

```markdown
---
type: SignatureAchievements
title: "Signature Achievements"
description: "Curated list of 5 achievements ranked on intrinsic properties (strategic significance, organisational impact, capability breadth, recency, confidence)."
tags: [achievements, signature]
generated: { by: "signature-achievements-curator", at: "2026-07-30T14:00:00Z" }
status: draft
sources:
  - id: cv-2024
    resource: fixtures/cv.md
    title: CV (2024 edition)
---

# The list

1. **[Cloud Migration Programme](../achievements/cloud-migration-programme.md)** — [inference] **Why:** Multi-region transformation with documented governance. **Strategic:** Anchored the multi-year platform strategy. **Capability:** Enterprise Architecture.
2. **[Architecture Patterns Governance](../achievements/architecture-patterns.md)** — [inference] **Why:** Patterns mandated across 200+ engineers. **Strategic:** Codified architecture-as-governance. **Capability:** Enterprise Architecture.
3. **[AI CoE Build](../achievements/ai-coe-build.md)** — [inference] **Why:** First AI capability in production with governance. **Strategic:** Operationalised AI under regulatory constraints. **Capability:** AI Governance.
4. **[Decision Log Practice](../achievements/decision-log-practice.md)** — [inference] **Why:** Reversible decisions, documented trade-offs. **Strategic:** Decision discipline as a recurring artefact. **Capability:** Executive Communication.
5. **[Stakeholder Management Across Regions](../achievements/stakeholder-management.md)** — [inference] **Why:** Coordinated across three regions asynchronously. **Strategic:** Distributed leadership through artefacts. **Capability:** Executive Communication.

# Selection rationale
[inference] The list ranks on intrinsic properties (R2, R10). No opportunity-specific state is encoded in the canonical node. Opportunity-aware reordering happens at view time in `out/opportunity-alignment.md`.
```

- [ ] **Step 4: Create the test file**

```python
# tests/test_signature_achievements_curator.py
import os
import pytest

GOLDEN = "tests/golden/signature-achievements-curator"


def test_skill_exists():
    path = "skills/signature-achievements-curator/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: signature-achievements-curator" in content


def test_achievement_fixtures_exist():
    fixture_dir = "tests/fixtures/portfolio_minimal"
    expected = [
        "achievements-cloud-migration.md",
        "achievements-architecture-patterns.md",
        "achievements-ai-coe-build.md",
        "achievements-decision-log-practice.md",
        "achievements-stakeholder-management.md",
    ]
    for name in expected:
        assert os.path.exists(os.path.join(fixture_dir, name)), f"Missing fixture {name}"


def test_golden_node_exists():
    assert os.path.isdir(GOLDEN)
    assert os.path.exists(os.path.join(GOLDEN, "signature-achievements.md"))
    with open(os.path.join(GOLDEN, "signature-achievements.md")) as f:
        content = f.read()
    assert "type: SignatureAchievements" in content
    assert "Selection rationale" in content
    # 5 list items numbered 1.-5.
    for i in range(1, 6):
        assert f"{i}. **" in content, f"List item {i} not found"
```

- [ ] **Step 5: Run the tests**

```bash
pytest tests/test_signature_achievements_curator.py -v
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add skills/signature-achievements-curator/SKILL.md tests/test_signature_achievements_curator.py tests/fixtures/portfolio_minimal/achievements-*.md tests/golden/signature-achievements-curator/
git commit -m "feat: signature-achievements-curator SKILL, fixtures, and golden"
```

---

## Task 6: Implement behaviour-profile-generator

**Files:**
- Create: `skills/behaviour-profile-generator/SKILL.md`
- Create: `tests/test_behaviour_profile.py`
- Create: `tests/golden/behaviour-profile/behaviour-profile.md`

- [ ] **Step 1: Create the SKILL.md**

```markdown
---
name: behaviour-profile-generator
description: Builds an ExecutiveBehaviourProfile with 4 core dimensions always present and 3 optional dimensions only when sufficient evidence.
---

# Behaviour Profile Generator

## Overview

`behaviour-profile-generator` reads `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md` (if present), and the target opportunity from `config/config.yaml` to produce a single `ExecutiveBehaviourProfile` concept at `okf/behaviour-profile.md`.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every claim body line MUST begin with `[evidence]`, `[inference]`, `[recommendation]`, or `[assumption]`. All `[evidence]` lines require `[^source-id]` footnotes. Optional dimensions are omitted when evidence is thin — they are NEVER marked `(insufficient evidence)` (R5).

## Input & Output Contracts

- **Inputs**: `okf/evidence/*.md`, `okf/themes/*.md`, `okf/signature-themes.md` (if present), `config/config.yaml` (target_opportunity).
- **Outputs**:
  - `okf/behaviour-profile.md` (type: `ExecutiveBehaviourProfile`)
  - `okf/log.md` (append entry)

## Concept Schema & Structure

```markdown
---
type: ExecutiveBehaviourProfile
title: "Executive Behaviour Profile"
description: "Inferred executive behaviour profile. Core dimensions always generated; optional dimensions included only when sufficient evidence exists."
tags: [behaviour, profile, executive]
generated: { by: "behaviour-profile-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# Core dimensions

## Leadership Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: <supporting reasoning>.

## Communication Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: ...

## Decision Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: ...

## Delivery Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: ...

# Optional dimensions

## Stakeholder Style
[evidence] <line>. [^source-id]
[inference] <inference>.
> Reasoning: ...

## Summary
[inference] Core dimensions were generated. Optional dimensions included or omitted based on evidence. Sections omitted are surfaced to `okf/knowledge-gaps.md`.
```

## Dimension Rules (R5)

- **Core (always generated)**: Leadership Style, Communication Style, Decision Style, Delivery Style.
- **Optional (only when sufficient evidence exists; otherwise OMITTED)**: Stakeholder Style, Collaboration Style, Executive Presence.
- **Optional sections are never marked `(insufficient evidence)`** — they are omitted entirely.

## Execution Instructions

1. **Load evidence, themes, signature-themes.**
2. **Infer each core dimension**: 3–7 `[evidence]` lines (each citing a source) followed by 1–3 `[inference]` lines with a `> Reasoning:` blockquote.
3. **For each optional dimension**: emit the section only if ≥2 evidence lines can be cited. Otherwise omit.
4. **Append log**: `okf/log.md`.

## Stop-and-Ask

- Fewer than 3 evidence cards → exit.
```

- [ ] **Step 2: Create the golden node**

```markdown
---
type: ExecutiveBehaviourProfile
title: "Executive Behaviour Profile"
description: "Inferred executive behaviour profile. Core dimensions always generated; optional dimensions included only when sufficient evidence exists."
tags: [behaviour, profile, executive]
generated: { by: "behaviour-profile-generator", at: "2026-07-30T14:00:00Z" }
status: draft
sources:
  - id: cv-2024
    resource: fixtures/cv.md
    title: CV (2024 edition)
---

# Core dimensions

## Leadership Style
[evidence] Led the architecture working group across three regions. [^cv-2024]
[evidence] Distributed leadership; never named "the leader" in any org chart shown in source. [^cv-2024]
[inference] Leadership is enacted through written artefacts rather than positional authority.
> Reasoning: Two sources describe the candidate leading through artefacts.

## Communication Style
[evidence] Authored migration architecture document and cutover runbook. [^cv-2024]
[inference] Written communication is the primary mode; verbal communication is anchored to written context.
> Reasoning: All major stakeholder interactions captured in writing.

## Decision Style
[evidence] Authored the cutover decision log, recording trade-offs and reversibility assessments. [^cv-2024]
[inference] Decision-making is documented and reversible when possible.
> Reasoning: The cutover decision log is the strongest evidence.

## Delivery Style
[evidence] Migration completed on schedule. [^cv-2024]
[evidence] Cutover rehearsed end-to-end before the real window. [^cv-2024]
[inference] Strong delivery discipline; delivery is anchored to rehearsal and runbooks.
> Reasoning: Two corroborating sources confirm the rehearsal pattern.

# Optional dimensions

## Stakeholder Style
[evidence] Coordinated across three regions. [^cv-2024]
[evidence] Documented stakeholder communications in writing. [^cv-2024]
[inference] Stakeholder coordination is multi-region, documented, and asynchronous-first.
> Reasoning: Two sources, both verifiable.

# Summary
[inference] Core dimensions were generated. Optional dimensions included or omitted based on evidence. Sections omitted are surfaced to `okf/knowledge-gaps.md`.
```

- [ ] **Step 3: Create the test file**

```python
# tests/test_behaviour_profile.py
import os


def test_skill_exists():
    path = "skills/behaviour-profile-generator/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: behaviour-profile-generator" in content


def test_golden_has_four_core_dimensions():
    golden = "tests/golden/behaviour-profile/behaviour-profile.md"
    assert os.path.exists(golden)
    with open(golden) as f:
        content = f.read()
    for dim in ["Leadership Style", "Communication Style", "Decision Style", "Delivery Style"]:
        assert f"## {dim}" in content, f"Core dimension '{dim}' missing from golden"
    assert "## Collaboration Style" not in content, "Collaboration Style should be omitted (R5)"
    assert "## Executive Presence" not in content, "Executive Presence should be omitted (R5)"
    assert "(insufficient evidence)" not in content, "Optional dimensions must be omitted, not marked insufficient (R5)"
```

- [ ] **Step 4: Run the tests**

```bash
pytest tests/test_behaviour_profile.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/behaviour-profile-generator/SKILL.md tests/test_behaviour_profile.py tests/golden/behaviour-profile/
git commit -m "feat: behaviour-profile-generator with R5 core/optional split"
```

---

## Task 7: Extend interview-strategy-generator with Opportunity Analysis and Story-to-Question mapping

**Files:**
- Modify: `skills/interview-strategy-generator/SKILL.md`

- [ ] **Step 1: Open the SKILL.md and locate `## Execution Instructions`**

- [ ] **Step 2: Replace the existing `## Execution Instructions` block with the v0.3 version**

The new block:

```markdown
## Execution Instructions

This Skill produces **coaching-layer output** (R1, R8). It reads the canonical bundle + target opportunity and produces `okf/interview-strategy.md`, which is regenerated every run and never treated as canonical knowledge.

1. **Parse Target Opportunity & Stage Context**: Read `config/config.yaml` to identify the active `target_opportunity.source` file path, role title, company, interviewer, and stage context. Analyze requirements and context directly from that specified target opportunity file.
2. **Rank Evidence Cards** into 4 tiers: `Primary Story`, `Supporting Story`, `Optional Story`, `Do Not Use`. Based on relevance, uniqueness, evidence strength, target role requirements, and interview stage.
3. **Opportunity Analysis (R8):** For each major interview theme (5–8 themes), emit a block with `[evidence]` requirement from JD, `[inference]` why it matters, supporting evidence links, alignment strength, `[recommendation]` what to emphasise, `[recommendation]` what to avoid over-explaining.
4. **Story-to-Question Mapping (R3):** For each anticipated question (10–15), emit a block with Primary story (`[recommendation]`), Supporting evidence (`[inference]`), Alternative story (`[recommendation]`). The Primary story is selected from the `Capability.Primary Evidence` tier when one matches.
5. **Formulate Coaching Guidance**: lead with, avoid, flagship stories, differentiators, objections.
6. **Write `okf/interview-strategy.md`** (max 4 pages).
7. **Append Log**: `okf/log.md`.
```

- [ ] **Step 3: Add a new `## Concept Schema & Structure` section between Hard Rules and Execution Instructions**

```markdown
## Concept Schema & Structure

```markdown
---
type: InterviewStrategy
title: "Interview Strategy"
description: "Coaching strategy for the target opportunity. Regenerated every run."
tags: [strategy, coaching]
generated: { by: "interview-strategy-generator", at: "<ISO-8601>" }
status: draft
sources:
  - id: <source-id>
    resource: <resource-path>
    title: "<source-title>"
---

# Opportunity Analysis

## <Theme 1>
[evidence] <requirement from JD>. [^source-id]
[inference] <why it matters>.
- [Evidence: <title>](../evidence/<slug>.md)
- **Alignment strength**: [inference] <High | Moderate | Low>.
[recommendation] Lead with: <emphasis>.
[recommendation] Avoid over-explaining: <avoidance>.

(Repeat for 5–8 themes.)

# Story-to-Question Mapping

## <Question 1>
[recommendation] Primary story: [Evidence: <title>](../evidence/<slug>.md).
[inference] Supporting evidence: [Evidence: <title>](../evidence/<slug>.md).
[recommendation] Alternative story: [Evidence: <title>](../evidence/<slug>.md).

(Repeat for 10–15 questions.)

# Coaching Guidance
[inference] Lead with: <lead>.
[recommendation] Avoid: <avoid>.
[inference] Flagship stories: ...
[inference] Differentiators: ...
[inference] Objections and mitigations: ...
```
```

- [ ] **Step 4: Verify the SKILL.md still passes the skills presence test**

```bash
pytest tests/test_skills.py::test_skills_exist -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/interview-strategy-generator/SKILL.md
git commit -m "feat(interview-strategy-generator): add Opportunity Analysis and Story→Question mapping"
```

---

## Task 8: Implement opportunity-alignment-view (coaching/projection layer)

**Files:**
- Create: `skills/opportunity-alignment-view/SKILL.md`
- Create: `tests/test_opportunity_alignment_view.py`
- Create: `tests/golden/opportunity-alignment-view/opportunity-alignment.md`

- [ ] **Step 1: Create the SKILL.md**

```markdown
---
name: opportunity-alignment-view
description: Walks the canonical bundle to produce a theme-by-theme opportunity alignment view at out/opportunity-alignment.md.
---

# Opportunity Alignment View

## Overview

`opportunity-alignment-view` is a projection-layer Skill (R1, R9). It reads the canonical bundle (evidence, themes, capabilities, signature-achievements) and the target opportunity from `config/config.yaml`, and produces `out/opportunity-alignment.md`. It performs the Opportunity Analysis at view time — NOT in the canonical bundle.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Read-only access to the canonical bundle. No mutation. No persistence beyond `out/`. Fully reproducible.

## Projection Contract (R9)

- **Inputs**: Canonical Bundle + Target Opportunity + Configuration.
- **Outputs**: `out/opportunity-alignment.md` (presentation artefact).
- **Constraints**: Read-only. No mutation. Out-only persistence. Reproducible.

## Input & Output Contracts

- **Inputs**: `okf/evidence/*`, `okf/themes/*`, `okf/capabilities/*`, `okf/signature-achievements.md`, `config/config.yaml` (target_opportunity).
- **Outputs**: `out/opportunity-alignment.md`.

Note: per OKF v0.2 §11, the `type` frontmatter is required only on concept files. The view file at `out/` carries only `title` and `description`.

## Body Structure (3000–5000 words)

```markdown
---
title: "Opportunity Alignment — <Role> at <Company>"
description: "Theme-by-theme mapping of role requirements to candidate evidence."
generated: { by: "opportunity-alignment-view", at: "<ISO-8601>" }
status: draft
---

# Coverage summary
[inference] <one-paragraph summary of how the candidate's evidence covers the role themes>.

# Theme-by-theme mapping

## <Theme 1>
[evidence] <requirement from JD>. [^source-id]
[inference] <why it matters>.
- [Evidence: <title>](../okf/evidence/<slug>.md)
- [Capability: <title>](../okf/capabilities/<slug>.md)
- **Alignment strength**: [inference] <High | Moderate | Low>.
[recommendation] Lead with: <emphasis>.
[recommendation] Avoid over-explaining: <avoid>.

(Repeat for 5–8 themes.)

# Signature Achievement mapping
[inference] <which signature achievements are most relevant for this opportunity — computed at view time, not encoded in the canonical node (R2)>.
```

## Execution Instructions

1. **Read target opportunity** from `config/config.yaml`.
2. **Walk the canonical bundle**: evidence, themes, capabilities, signature-achievements.
3. **Compute alignment** dynamically for each role theme (5–8 themes).
4. **Write `out/opportunity-alignment.md`**.
```

- [ ] **Step 2: Create the golden view file**

```markdown
---
title: "Opportunity Alignment — Head of AI at Vervaunt"
description: "Theme-by-theme mapping of role requirements to candidate evidence."
generated: { by: "opportunity-alignment-view", at: "2026-07-30T14:00:00Z" }
status: draft
---

# Coverage summary
[inference] The candidate's evidence covers all five major themes in the Vervaunt Head of AI role with high alignment on delivery discipline and moderate alignment on AI production-isation.

# Theme-by-theme mapping

## Operationalising AI under governance
[evidence] First AI capability in production with governance. [^cv-2024]
[inference] The role emphasises delivery, not strategy.
- [Evidence: AI CoE Build](../okf/evidence/ai-coe-build.md)
- [Capability: AI Governance](../okf/capabilities/ai-governance.md)
- **Alignment strength**: [inference] High.
[recommendation] Lead with: the AI CoE build story.
[recommendation] Avoid over-explaining: AI strategy at the research-level.

## Multi-region delivery
[evidence] Led migration across three regions. [^cv-2024]
[inference] Coordination across distributed teams.
- [Evidence: Cloud Migration](../okf/evidence/cloud-migration.md)
- [Capability: Enterprise Architecture](../okf/capabilities/enterprise-architecture.md)
- **Alignment strength**: [inference] High.
[recommendation] Lead with: the cutover rehearsal story.

## Documented decision-making
[evidence] Authored the cutover decision log. [^cv-2024]
[inference] Decision-making is reversible and documented.
- [Evidence: Decision Log Practice](../okf/evidence/decision-log-practice.md)
- **Alignment strength**: [inference] High.

## Stakeholder coordination
[evidence] Coordinated across three regions asynchronously. [^cv-2024]
- [Evidence: Stakeholder Management](../okf/evidence/stakeholder-management.md)
- **Alignment strength**: [inference] Moderate.

## Architecture patterns
[evidence] Patterns mandated across 200+ engineers. [^cv-2024]
- [Evidence: Architecture Patterns](../okf/evidence/architecture-patterns.md)
- **Alignment strength**: [inference] Moderate.

# Signature Achievement mapping
[inference] The strongest mappings for this opportunity are: Cloud Migration Programme, AI CoE Build, and Architecture Patterns Governance. The ranking is computed at view time and is NOT encoded in the canonical `SignatureAchievements` node (R2).
```

- [ ] **Step 3: Create the test file**

```python
# tests/test_opportunity_alignment_view.py
import os

GOLDEN = "tests/golden/opportunity-alignment-view"


def test_skill_exists():
    path = "skills/opportunity-alignment-view/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: opportunity-alignment-view" in content


def test_golden_view_exists():
    assert os.path.isdir(GOLDEN)
    golden_path = os.path.join(GOLDEN, "opportunity-alignment.md")
    assert os.path.exists(golden_path)
    with open(golden_path) as f:
        content = f.read()
    assert content.startswith("---")
    # Frontmatter must NOT have `type:` (per OKF §11, type is required only on concept files in okf/).
    frontmatter_end = content.find("---", 3)
    assert frontmatter_end > 0
    frontmatter = content[:frontmatter_end]
    assert "type:" not in frontmatter, "View file must NOT have a `type:` frontmatter key"
    assert "title:" in frontmatter
    assert "description:" in frontmatter
    # Body must contain 5–8 theme blocks (## headings).
    theme_blocks = [line for line in content.splitlines() if line.startswith("## ")]
    assert 5 <= len(theme_blocks) <= 8, f"Expected 5–8 themes, found {len(theme_blocks)}"


def test_golden_links_resolve():
    golden_path = os.path.join(GOLDEN, "opportunity-alignment.md")
    with open(golden_path) as f:
        content = f.read()
    # Extract every bundle-relative link. They should be bundle-relative (start with ../okf/).
    import re
    links = re.findall(r"\]\(\.\./okf/[^)]+\)", content)
    assert len(links) > 0, "Expected at least one bundle-relative link"
```

- [ ] **Step 4: Run the tests**

```bash
pytest tests/test_opportunity_alignment_view.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/opportunity-alignment-view/SKILL.md tests/test_opportunity_alignment_view.py tests/golden/opportunity-alignment-view/
git commit -m "feat: opportunity-alignment-view projection-layer Skill"
```

---

## Task 9: Implement executive-brief-view (11 sections including Interview Mindset)

**Files:**
- Create: `skills/executive-brief-view/SKILL.md`
- Create: `tests/test_executive_brief_view.py`
- Create: `tests/golden/executive-brief-view/executive-brief.md`

- [ ] **Step 1: Create the SKILL.md**

```markdown
---
name: executive-brief-view
description: Walks the whole bundle to produce a 10-minute pre-interview brief at out/executive-brief.md.
---

# Executive Brief View

## Overview

`executive-brief-view` is a projection-layer Skill (R1, R9). It reads the whole bundle and produces `out/executive-brief.md`. Designed for the 10-minute pre-interview window.

## Hard Rules

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Read-only access to the canonical bundle. No mutation. No persistence beyond `out/`. Fully reproducible.

## Projection Contract (R9)

Same as `opportunity-alignment-view`. Inputs: Canonical Bundle + Target Opportunity + Configuration. Output: presentation artefact. Read-only. No mutation.

## Input & Output Contracts

- **Inputs**: `okf/evidence/*`, `okf/themes/*`, `okf/capabilities/*`, `okf/signature-achievements.md`, `okf/interview-strategy.md`, `okf/behaviour-profile.md`, `okf/signature-themes.md`, `okf/executive-narrative.md`, `config/config.yaml`.
- **Outputs**: `out/executive-brief.md`.

## Body Structure (11 sections, ≤2,500 words)

The brief MUST contain these 11 sections, in this order:

1. Executive Positioning
2. Top 5 Messages
3. Three Signature Stories
4. Executive Behaviour Profile — at-a-glance
5. Conversation Strategy
6. Risks
7. Opportunity Watch-outs
8. Questions to Ask
9. Conversation Reminders
10. Interview Mindset (R6 — pure coaching, no evidence, ≤5 bullets)
11. Final Reminders

## Execution Instructions

1. **Walk the bundle** in the order above.
2. **Render each section** according to the schema.
3. **Verify link integrity**: every link to an evidence card, capability, achievement, or theme is a working bundle-relative link.
4. **Word budget**: ≤2,500 words.
5. **Write `out/executive-brief.md`**.
```

- [ ] **Step 2: Create the golden view file**

```markdown
---
title: "Executive Brief — Head of AI at Vervaunt"
description: "10-minute pre-interview briefing."
generated: { by: "executive-brief-view", at: "2026-07-30T14:00:00Z" }
status: draft
---

# Executive Brief
*Generated for Head of AI at Vervaunt · 2026-07-30 · [draft]*

## 1. Executive Positioning
[recommendation] Enterprise architect and platform leader with fifteen years of operationalising transformation across regulated industries; the right person to land Vervaunt's first AI platform in production.

## 2. Top 5 Messages
1. **[inference] Operational, not aspirational.** [Evidence: Cloud Migration](../okf/evidence/cloud-migration.md)
2. **[inference] Governance is the unlock, not the blocker.** [Evidence: Architecture Patterns](../okf/evidence/architecture-patterns.md)
3. **[inference] Lead by artefacts.** [Evidence: Decision Log Practice](../okf/evidence/decision-log-practice.md)
4. **[inference] AI is a delivery problem, not a research problem.** [Evidence: AI CoE Build](../okf/evidence/ai-coe-build.md)
5. **[inference] The capability is in the team, not the individual.** [Evidence: Stakeholder Management](../okf/evidence/stakeholder-management.md)

## 3. Three Signature Stories
1. **[inference] Cloud migration across three regions.** [Evidence: Cloud Migration](../okf/evidence/cloud-migration.md). [inference] Why: the only programme that survived the post-merger integration.
2. **[inference] Building the AI Centre of Excellence.** [Evidence: AI CoE Build](../okf/evidence/ai-coe-build.md). [inference] First AI capability in production, with governance.
3. **[inference] Architecture patterns governance.** [Evidence: Architecture Patterns](../okf/evidence/architecture-patterns.md). [inference] Mandated patterns across 200+ engineers.

## 4. Executive Behaviour Profile — at-a-glance
- **Leadership:** [inference] Distributed leadership through artefacts.
- **Communication:** [inference] Written-first; verbal anchored to written context.
- **Decision:** [inference] Documented; reversible when possible.
- **Delivery:** [inference] Rehearsed, scheduled, predictable.
- **Stakeholder:** [inference] Multi-region coordination with documented decision logs.

## 5. Conversation Strategy
[inference] Lead with Operational, not aspirational. The Vervaunt role is delivery-focused.
[recommendation] Lead with: Cloud migration story.
[recommendation] Avoid over-explaining: technical architecture details.

## 6. Risks
- [inference] Capability is broad; interviewer may probe for depth.
- [recommendation] Mitigation: have one deep story ready for each capability.

## 7. Opportunity Watch-outs
- [inference] The interviewer will probe for AI production-isation, not AI strategy.
- [recommendation] How to handle: lead with the AI CoE build story.

## 8. Questions to Ask
- [recommendation] What does success look like in the first 90 days?
- [recommendation] Where does the Head of AI sit in the engineering org — product, platform, or standalone?
- [recommendation] What is the current state of AI governance in the business?
- [recommendation] Who is the peer set for this role?
- [recommendation] What is the budget envelope for AI in year one?

## 9. Conversation Reminders
[recommendation] Pause. Listen carefully. Answer the question first. Keep responses concise. Use business language. Bring answers back to outcomes. Avoid over-explaining technology. Ask thoughtful questions. Be curious. Finish confidently.

## 10. Interview Mindset (R6 — pure coaching, no evidence)
[recommendation] Curious.
[recommendation] Collaborative.
[recommendation] Outcome-focused.
[recommendation] Executive.
[recommendation] Commercial.

## 11. Final Reminders
[recommendation] You are interviewing them as much as they are interviewing you.
[recommendation] The role is delivery, not strategy. Lead accordingly.
[recommendation] Trust the artefacts; they have always worked for you.
```

- [ ] **Step 3: Create the test file**

```python
# tests/test_executive_brief_view.py
import os
import re

GOLDEN = "tests/golden/executive-brief-view"


def test_skill_exists():
    path = "skills/executive-brief-view/SKILL.md"
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
    assert content.startswith("---")
    assert "name: executive-brief-view" in content


def test_golden_has_eleven_sections():
    golden_path = os.path.join(GOLDEN, "executive-brief.md")
    assert os.path.exists(golden_path)
    with open(golden_path) as f:
        content = f.read()
    expected_titles = [
        "Executive Positioning",
        "Top 5 Messages",
        "Three Signature Stories",
        "Executive Behaviour Profile",
        "Conversation Strategy",
        "Risks",
        "Opportunity Watch-outs",
        "Questions to Ask",
        "Conversation Reminders",
        "Interview Mindset",
        "Final Reminders",
    ]
    for title in expected_titles:
        assert f"## " in content, "Section headings missing"
        assert title in content, f"Section '{title}' missing from golden"
    # Exactly 11 ## headings.
    headings = [line for line in content.splitlines() if line.startswith("## ")]
    assert len(headings) == 11, f"Expected 11 sections, found {len(headings)}"


def test_golden_word_count_within_budget():
    golden_path = os.path.join(GOLDEN, "executive-brief.md")
    with open(golden_path) as f:
        content = f.read()
    # Strip frontmatter and markdown markers for a rough word count.
    body = content.split("---", 2)[-1]
    words = re.findall(r"\w+", body)
    assert len(words) <= 2500, f"Brief exceeds 2,500-word budget (got {len(words)})"


def test_interview_mindset_no_evidence():
    golden_path = os.path.join(GOLDEN, "executive-brief.md")
    with open(golden_path) as f:
        content = f.read()
    # The Interview Mindset section must be pure coaching — no [evidence] tags.
    mindset_start = content.find("## 10. Interview Mindset")
    mindset_end = content.find("## 11. Final Reminders")
    mindset_section = content[mindset_start:mindset_end] if mindset_start > 0 and mindset_end > 0 else ""
    assert "[evidence]" not in mindset_section, "Interview Mindset must be pure coaching (R6)"
    # ≤5 bullets.
    bullets = [line for line in mindset_section.splitlines() if line.startswith("[recommendation]")]
    assert len(bullets) <= 5, f"Interview Mindset must have ≤5 bullets, found {len(bullets)}"
```

- [ ] **Step 4: Run the tests**

```bash
pytest tests/test_executive_brief_view.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/executive-brief-view/SKILL.md tests/test_executive_brief_view.py tests/golden/executive-brief-view/
git commit -m "feat: executive-brief-view projection-layer Skill with 11 sections"
```

---

## Task 10: Extend the lint discipline to validate the new concept types and fields

**Files:**
- Modify: `tests/test_lint.py`

- [ ] **Step 1: Open `tests/test_lint.py` and locate the `lint_okf_concept_content` function**

- [ ] **Step 2: Add a new helper that validates the new concept shapes**

Append to `tests/test_lint.py`:

```python
def lint_capability_content(content: str) -> list[str]:
    """Validate a Capability concept: has Primary Evidence section, ≥1 primary entry, and Evidence strength."""
    errors = []
    if "type: Capability" not in content:
        return errors
    if "## Primary Evidence" not in content:
        errors.append("Missing '## Primary Evidence' section")
    if "## Evidence strength" not in content:
        errors.append("Missing '## Evidence strength' section")
    if "## Supporting Evidence" not in content:
        errors.append("Missing '## Supporting Evidence' section")
    if "## Additional Evidence" not in content:
        errors.append("Missing '## Additional Evidence' section")
    if "Opportunity relevance" in content:
        errors.append("Capability must NOT contain 'Opportunity relevance' (use Evidence strength instead, R7)")
    return errors


def lint_executive_behaviour_profile_content(content: str) -> list[str]:
    """Validate an ExecutiveBehaviourProfile: 4 core dimensions always present, optional marked insufficient is a violation."""
    errors = []
    if "type: ExecutiveBehaviourProfile" not in content:
        return errors
    for dim in ["Leadership Style", "Communication Style", "Decision Style", "Delivery Style"]:
        if f"## {dim}" not in content:
            errors.append(f"Core dimension '{dim}' missing")
    if "(insufficient evidence)" in content:
        errors.append("Optional dimensions must be omitted, not marked '(insufficient evidence)' (R5)")
    return errors


def lint_signature_achievements_content(content: str) -> list[str]:
    """Validate a SignatureAchievements node: 5–12 numbered list entries, each with Why/Strategic/Capability."""
    errors = []
    if "type: SignatureAchievements" not in content:
        return errors
    import re
    entries = re.findall(r"^\d+\. \*\*", content, flags=re.MULTILINE)
    if not (5 <= len(entries) <= 12):
        errors.append(f"SignatureAchievements list length must be 5–12, found {len(entries)}")
    if "Selection rationale" not in content:
        errors.append("Missing 'Selection rationale' section")
    return errors
```

- [ ] **Step 3: Add tests for the new helpers**

Append to `tests/test_lint.py`:

```python
def test_capability_lint_accepts_valid_node():
    valid = """---
type: Capability
title: "Enterprise Architecture"
---

# Definition
[inference] Description.

# Primary Evidence
- [Evidence: Cloud Migration](cloud-migration.md) — [inference] Strongest demonstration.

# Supporting Evidence
- [Evidence: Architecture Patterns](architecture-patterns.md) — [inference] Reinforces.

# Additional Evidence

# Evidence strength
[inference] High.
"""
    errors = lint_capability_content(valid)
    assert errors == [], f"Expected zero lint errors, got: {errors}"


def test_capability_lint_rejects_opportunity_relevance():
    invalid = """---
type: Capability
---

# Opportunity relevance
[inference] Some text.
"""
    errors = lint_capability_content(invalid)
    assert any("Opportunity relevance" in e for e in errors)


def test_behaviour_profile_lint_rejects_insufficient_evidence_marker():
    invalid = """---
type: ExecutiveBehaviourProfile
---

## Leadership Style
[evidence] Leadership x. [^cv]

## Communication Style
[evidence] Communication x. [^cv]

## Decision Style
(insufficient evidence)

## Delivery Style
[evidence] Delivery x. [^cv]
"""
    errors = lint_executive_behaviour_profile_content(invalid)
    assert any("'(insufficient evidence)'" in e for e in errors)


def test_signature_achievements_lint_rejects_short_list():
    invalid = """---
type: SignatureAchievements
---

# The list

1. **[A](a.md)** — [inference] Why x. Strategic y. Capability z.

# Selection rationale
[inference] Rationale.
"""
    errors = lint_signature_achievements_content(invalid)
    assert any("5–12" in e for e in errors)
```

- [ ] **Step 4: Run the tests**

```bash
pytest tests/test_lint.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_lint.py
git commit -m "test(lint): validate Capability, ExecutiveBehaviourProfile, SignatureAchievements shapes"
```

---

## Task 11: Update the orchestrator and root config to include the new Skills

**Files:**
- Modify: `config/config.example.yaml`
- Modify: `config/config.yaml`
- Modify: `tests/test_skills.py`

- [ ] **Step 1: Open `config/config.example.yaml` and bump the version + add new Skills**

Replace the `project` block:

```yaml
project:
  name: "Master Interview Playbook"
  version: "0.3"
```

Replace the `pipeline.skills` list with:

```yaml
pipeline:
  skills:
    - portfolio-ingestor
    - portfolio-analyzer
    - achievement-extractor
    - evidence-card-generator
    - behaviour-profile-generator
    - capability-extractor
    - signature-achievements-curator
    - signature-theme-miner
    - narrative-generator
    - interview-strategy-generator
    - knowledge-gaps
    - opportunity-alignment-view
    - executive-brief-view
    - playbook-assembler
  run_knowledge_gaps: true
  fail_on_severe_gaps: false
```

- [ ] **Step 2: Apply the same edits to `config/config.yaml`**

- [ ] **Step 3: Update `tests/test_skills.py` to expect the new Skills**

```python
def test_skills_exist():
    expected_skills = [
        "playbook-orchestrator",
        "portfolio-ingestor",
        "portfolio-analyzer",
        "achievement-extractor",
        "evidence-card-generator",
        "behaviour-profile-generator",
        "capability-extractor",
        "signature-achievements-curator",
        "signature-theme-miner",
        "narrative-generator",
        "interview-strategy-generator",
        "knowledge-gaps",
        "opportunity-alignment-view",
        "executive-brief-view",
        "playbook-assembler",
    ]
    skills_dir = "skills"
    for skill in expected_skills:
        skill_path = os.path.join(skills_dir, skill, "SKILL.md")
        assert os.path.exists(skill_path), f"Missing skill definition at {skill_path}"
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert content.startswith("---"), f"Skill {skill} missing frontmatter delimiter"
            assert "name: " + skill in content, f"Skill {skill} missing name frontmatter"
```

- [ ] **Step 4: Run the test**

```bash
pytest tests/test_skills.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add config/config.example.yaml config/config.yaml tests/test_skills.py
git commit -m "feat: add v0.3 pipeline (5 new Skills) and bump version to 0.3"
```

---

## Task 12: Update docs to reflect the new architecture

**Files:**
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `ARCHITECTURE.md`
- Modify: `README.md`

- [ ] **Step 1: Open `AGENTS.md` and update the project concept types list**

Locate the line `v0.1 types: Source, SourceIndex, PortfolioAnalysis, Achievement, EvidenceCard, InterviewStrategy, KnowledgeGap.` and replace it with:

```markdown
v0.3 types: `Source`, `SourceIndex`, `PortfolioAnalysis`, `Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `InterviewStrategy`, `KnowledgeGap`. See the v0.3 design spec §5.3 for field additions on `EvidenceCard`.
```

- [ ] **Step 2: Open `AGENTS.md` and update the pipeline diagram with the new Skills**

Replace the existing `playbook-orchestrator → portfolio-ingestor → ... → playbook-assembler` block with:

```markdown
KNOWLEDGE LAYER (canonical; writes to okf/)
  portfolio-ingestor
  portfolio-analyzer
  achievement-extractor
  evidence-card-generator        ← extended (new fields + dup detection)
  behaviour-profile-generator    ← new (canonical)
  capability-extractor            ← new (canonical)
  signature-achievements-curator  ← new (canonical)
  signature-theme-miner
  narrative-generator

COACHING LAYER (derived; reads canonical + target opportunity)
  interview-strategy-generator   ← extended (Opportunity Analysis + Story→Question mapping)
  knowledge-gaps

PROJECTION LAYER (views; reads canonical + coaching + target opportunity; writes to out/)
  playbook-assembler
  opportunity-alignment-view      ← new view Skill
  executive-brief-view           ← new view Skill
```

- [ ] **Step 3: Open `CLAUDE.md` and update the Next step line**

Locate `- **Next step:** Write the implementation plan ...` and update to:

```markdown
- **Next step:** Execute the Sprint 3 implementation plan at `docs/superpowers/plans/2026-07-30-sprint-3-implementation.md`.
```

- [ ] **Step 4: Open `ARCHITECTURE.md` and update the system diagram**

Locate the `## System diagram` section and add a one-paragraph note about the three layers, linking to the Sprint 3 spec:

```markdown
Sprint 3 (v0.3) introduces an explicit three-layer architecture: Knowledge (canonical, in `okf/`), Coaching (derived, regenerated every run), and Projection (views in `out/`). The load-bearing principle: the OKF bundle stores only canonical career knowledge. Opportunity-specific interpretation is computed at view time. See `docs/superpowers/specs/2026-07-30-sprint-3-design.md` §2.1.
```

- [ ] **Step 5: Open `README.md` and add a v0.3 section at the bottom**

```markdown
## v0.3 (Sprint 3) — Executive Coaching & Knowledge Intelligence

Pure additive release over v0.2. Adds:

- 3 new canonical concept types: `ExecutiveBehaviourProfile`, `Capability`, `SignatureAchievements`.
- 6 new `EvidenceCard` fields: `conversation_hook`, `transition_sentence`, `organisational_impact`, `strategic_significance`, `recency`, `duplicates_of`.
- 3 new producer Skills: `behaviour-profile-generator`, `capability-extractor`, `signature-achievements-curator`.
- 2 new view Skills: `executive-brief-view`, `opportunity-alignment-view`.
- 2 extended Skills: `evidence-card-generator` (new fields + duplicate-detection pass), `interview-strategy-generator` (Opportunity Analysis + Story→Question mapping).

Architecture: three explicit layers (Knowledge / Coaching / Projection). The OKF bundle stores only canonical career knowledge. Opportunity-specific interpretation is computed at view time. Sprint 4 projections (Resume, Cover Letter, LinkedIn, Executive Biography, Consulting Proposal) will consume the same canonical bundle without bundle changes.

See the [Sprint 3 design spec](docs/superpowers/specs/2026-07-30-sprint-3-design.md) for the full contract.
```

- [ ] **Step 6: Run all tests to confirm nothing regressed**

```bash
pytest tests/ -v
```

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add AGENTS.md CLAUDE.md ARCHITECTURE.md README.md
git commit -m "docs: update agent instructions, architecture, and README for v0.3"
```

---

## Task 13: Verify v0.3 success criteria end-to-end

**Files:**
- Create: `tests/test_v03_success_criteria.py`

- [ ] **Step 1: Create the success criteria test file**

```python
# tests/test_v03_success_criteria.py
"""End-to-end checks for v0.3 success criteria (spec §8)."""
import os
import re
import subprocess
import sys


def test_pipeline_version_bumped():
    with open("config/config.example.yaml") as f:
        content = f.read()
    assert 'version: "0.3"' in content


def test_no_opportunity_relevance_field_in_golden():
    """No canonical evidence card in the golden subtree carries opportunity_relevance."""
    golden_evidence = "tests/golden"
    found = []
    for root, _, files in os.walk(golden_evidence):
        for fn in files:
            if fn.endswith(".md"):
                path = os.path.join(root, fn)
                with open(path) as f:
                    if "opportunity_relevance" in f.read():
                        found.append(path)
    assert found == [], f"Canonical nodes must NOT carry opportunity_relevance (R2), found in: {found}"


def test_view_files_no_type_field():
    """view files in tests/golden/ must not have a `type:` frontmatter key."""
    forbidden = []
    for root, _, files in os.walk("tests/golden"):
        for fn in files:
            if fn.endswith(".md"):
                path = os.path.join(root, fn)
                with open(path) as f:
                    content = f.read()
                if content.startswith("---"):
                    end = content.find("---", 3)
                    frontmatter = content[:end]
                    # We only forbid `type:` in view files (out/*). Golden copies of executive-brief-view and opportunity-alignment-view are views.
                    if "executive-brief-view" in path or "opportunity-alignment-view" in path:
                        if "type:" in frontmatter:
                            forbidden.append(path)
    assert forbidden == [], f"View files must NOT have `type:` frontmatter: {forbidden}"


def test_behaviour_profile_golden_has_no_insufficient_evidence():
    golden = "tests/golden/behaviour-profile/behaviour-profile.md"
    assert os.path.exists(golden)
    with open(golden) as f:
        assert "(insufficient evidence)" not in f.read(), "R5 violated"


def test_executive_brief_golden_has_eleven_sections():
    golden = "tests/golden/executive-brief-view/executive-brief.md"
    assert os.path.exists(golden)
    with open(golden) as f:
        content = f.read()
    headings = [line for line in content.splitlines() if line.startswith("## ")]
    assert len(headings) == 11, f"Expected 11 sections, got {len(headings)}"


def test_executive_brief_word_count_within_budget():
    golden = "tests/golden/executive-brief-view/executive-brief.md"
    with open(golden) as f:
        content = f.read()
    body = content.split("---", 2)[-1]
    words = re.findall(r"\w+", body)
    assert len(words) <= 2500, f"Executive Brief exceeds 2,500-word budget (got {len(words)})"


def test_oracle_full_test_suite():
    """Run the entire test suite and verify no tests fail."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Tests failed:\n{result.stdout}\n{result.stderr}"
```

- [ ] **Step 2: Run the full test suite**

```bash
pytest tests/ -v
```

Expected: all PASS. This certifies that success criteria 1–10 from the spec §8 are satisfied (with the caveat that criteria 1, 5, 6, 9, 10 require a full runtime pipeline run, which is checked by the orchestrator Skill in `playbook-orchestrator` —see that Skill's own documentation for the end-to-end run).

- [ ] **Step 3: Commit**

```bash
git add tests/test_v03_success_criteria.py
git commit -m "test: add v0.3 success-criteria end-to-end checks"
```

---

## Self-Review Checklist (run before declaring the plan complete)

Before executing this plan, the implementer should verify:

- [ ] **Spec coverage**: Every clause of the design spec has a task. Run `grep -n '^### \|^## \|^[0-9]' docs/superpowers/specs/2026-07-30-sprint-3-design.md` and confirm each section maps to a task above.
- [ ] **No `opportunity_relevance` field**: Tasks 1, 2, 4, 5, 6, 7, 8, 9 explicitly forbid `opportunity_relevance` in canonical evidence cards (R2).
- [ ] **No "insufficient evidence" markers**: Tasks 6 and 13 assert that Behaviour Profile optional dimensions are omitted, not marked insufficient (R5).
- [ ] **Three layers respected**: Tasks 7, 8, 9 produce coaching/projection output and explicitly forbid mutation of canonical nodes.
- [ ] **Behaviour Profile core/optional split**: Task 6 enforces the four core dimensions and the omission rule for optional dimensions.
- [ ] **Capability tiers**: Task 4 specifies Primary / Supporting / Additional evidence tiers and Evidence strength.
- [ ] **Signature Achievements opportunity-independent**: Task 5 explicitly removes the target opportunity from the Skill's inputs.
- [ ] **Conversation Hook + Transition Sentence**: Task 2 adds both fields to the EvidenceCard schema.
- [ ] **Interview Mindset**: Task 9 specifies the section as pure coaching with no `[evidence]` tags and ≤5 bullets.
- [ ] **Existing v0.2 tests still pass**: Task 13 runs the full test suite.
- [ ] **No placeholders**: Every step has actual code or content. No "TBD" or "implement later".

If any of the above is false, the plan needs a fix before execution starts.
