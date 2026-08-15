# Migration Plan: `mind-palace` → Career-First OKF Foundation (with Wikilinks + Mermaid on Day One)

## Context

`mind-palace` is a curated personal second brain — ten topical folders of markdown notes, HTML narratives, weekly learnings, raw PII in `resume-profile/`, and the canonical `standard-operational-procedure.v1.md`. It has no `out/`, no Skills, no tests, no CI, no OKF frontmatter.

`interview-playbook-generator` is the proven pipeline the owner already built and runs: OKF v0.2 spec, 30+ Skills with hard-rules headers, a five-layer pipeline (Knowledge / Runtime / Coaching / Projection / Evaluation), golden snapshot tests, `tests/test_lint.py` enforcing the five hard rules, and the operating triad (`AGENTS.md` / `CLAUDE.md` / `ARCHITECTURE.md`). It is locked to one candidate and one consumer (career projection).

The intent of this plan: **move the proven pipeline into `mind-palace` and visualise it, without rewriting it.** Two sprints, ~1.5 weeks. The OKF layer (the bundle, the PII sources) stays personal under `evidence/` and `out/`, both gitignored; the solution (spec, Skills, lint, scripts, tests, docs, CI) is shareable. Generic-OKF generalisation (Concept+concept_kind, tenancy, multi-tenant ingest, consumer split) is **deferred** until a real second consumer shows up. Wikilinks and Mermaid are added on day one because they have no dependency on type-vocabulary changes — they pay back immediately.

Locked decisions:

- **Scope:** career-first; OKF v0.2 stays verbatim. Generalisation triggered by second consumer.
- **Audience:** OKF layer personal; solution shareable.
- **Layout:** one repo, shareable surface at root, personal `out/okf/` and `evidence/` gitignored.
- **Disciplines:** canonical SOP for foundation work; feature branches + PRs + golden snapshot tests; existing `tests/test_lint.py` as the lint gate (no new `okf-lint` Skill needed at v0.2); `[[wikilinks]]` + Mermaid visualisation on day one.
- **Implementation toolchain:** Speckit (in Claude Code) for the specify / clarify / plan / tasks phases; Google Antigravity CLI for the implementation phase. See §10 for the workflow shape and constraints.

---

## 1. Target end state

**[S]** shareable (pushed by default) · **[P]** personal (gitignored).

```
mind-palace/
├── [S] AGENTS.md, ARCHITECTURE.md, CLAUDE.md, README.md, LICENSE  # rewritten to describe the new home
├── [S] .gitignore                                                  # covers out/, evidence/, *.pdf, secrets
├── [S] standard-operational-procedure/                             # governance SOP, kept as-is at root
│
├── [S] okf-spec/
│   └── [S] SPEC.md                                                 # OKF v0.2 (verbatim lift, no rewrite)
│
├── [S] skills/                                                     # all 30+ Skills lifted from interview-playbook-generator
│   ├── [S] portfolio-ingestor/SKILL.md
│   ├── [S] portfolio-analyzer/SKILL.md
│   ├── [S] achievement-extractor/SKILL.md
│   ├── [S] evidence-card-generator/SKILL.md
│   ├── [S] capability-extractor/SKILL.md
│   ├── [S] signature-achievements-curator/SKILL.md
│   ├── [S] signature-theme-miner/SKILL.md
│   ├── [S] executive-identity-generator/SKILL.md
│   ├── [S] narrative-engine/SKILL.md
│   ├── [S] story-engine/SKILL.md
│   ├── [S] opportunity-analyzer/SKILL.md
│   ├── [S] archetype-classifier/SKILL.md                          # v0.6
│   ├── [S] gap-classifier/SKILL.md                                # v0.6
│   ├── [S] archetype-fit-evaluator/SKILL.md                       # v0.6
│   ├── [S] projection-strategy-generator/SKILL.md                 # v0.6
│   ├── [S] interview-strategy-generator/SKILL.md
│   ├── [S] knowledge-gaps/SKILL.md
│   ├── [S] projection-registry/SKILL.md
│   ├── [S] resume-projection/SKILL.md
│   ├── [S] cover-letter-projection/SKILL.md
│   ├── [S] linkedin-projection/SKILL.md
│   ├── [S] opportunity-alignment-view/SKILL.md
│   ├── [S] executive-brief-view/SKILL.md
│   ├── [S] playbook-assembler/SKILL.md
│   ├── [S] projection-validator/SKILL.md
│   ├── [S] archetype-fit-validator/SKILL.md                       # v0.6
│   ├── [S] brand-validator/SKILL.md
│   ├── [S] narrative-generator/SKILL.md
│   ├── [S] market-feedback-evaluator/SKILL.md                     # v0.6
│   ├── [S] architecture-diagram-generator/SKILL.md
│   ├── [S] behaviour-profile-generator/SKILL.md
│   ├── [S] playbook-orchestrator/SKILL.md                         # entry point
│   ├── [S] okf-linkify/SKILL.md                                   # NEW — wikilink post-processor
│   └── [S] okf-graph/SKILL.md                                      # NEW — Mermaid emitter
│
├── [S] scripts/
│   ├── [S] ingest_portfolio.py
│   ├── [S] generate_architecture_diagrams.py
│   ├── [S] employment_validator.py
│   ├── [S] okf_linkify.py                                          # NEW
│   ├── [S] generate_okf_graph.py                                   # NEW
│   └── [S] ci_local.sh                                             # NEW — local-CI runner (see §10.3)
│
├── [S] tests/
│   ├── [S] conftest.py
│   ├── [S] fixtures/                                               # 10 fixtures from interview-playbook-generator
│   ├── [S] golden/<skill>/                                         # 6 dirs from interview-playbook-generator
│   ├── [S] test_lint.py                                            # verbatim (already enforces v0.2 hard rules)
│   ├── [S] test_*.py                                               # all existing Skill tests lifted
│   ├── [S] test_okf_linkify.py                                     # NEW
│   ├── [S] test_okf_graph.py                                       # NEW
│   ├── [S] test_v03_success_criteria.py
│   ├── [S] test_v04_success_criteria.py
│   ├── [S] test_v05_success_criteria.py
│   ├── [S] test_v06_success_criteria.py
│   ├── [S] test_career_evidence_integrity.py
│   ├── [S] test_claim_evidence_validation.py
│   └── [S] test_boundary_transferability.py
│
├── [S] docs/
│   ├── [S] requirements-spec.md
│   ├── [S] spec-refinements.md
│   ├── [S] architecture/
│   ├── [S] prompt-resume-ai-coe-ea.md
│   ├── [S] prompt-resume-writter.md
│   ├── [S] pull_request_description_*.md
│   └── [S] superpowers/specs/                                      # all 14 spec docs from interview-playbook-generator
│
├── [S] config/
│   ├── [S] config.example.yaml
│   └── [S] config.yaml                                             # gitignored (personal)
│
├── [S] .github/workflows/
│   ├── [S] okf-lint.yml                                            # renamed/adopted from existing test workflow
│   ├── [S] golden-snapshot.yml                                     # renamed/adopted from existing pytest workflow
│   ├── [S] validate.yml                                            # adapted
│   └── [S] markdown-lint.yml                                       # verbatim
│
├── [S] evaluation/opportunities/                                   # gitignored outputs from market-feedback-evaluator
│
├── [P] evidence/alexandre-franco/                                  # gitignored raw inputs
│   ├── [P] resume-profile/                                         # PDFs, CSVs, PerformanceManagement/ from mind-palace root
│   └── [P] target-position/                                        # 10 role briefs from mind-palace root
│
└── [P] out/                                                        # gitignored canonical bundle + per-target projections
    ├── [P] okf/                                                    # the knowledge base
    │   ├── [P] index.md, log.md, graph.md                          # graph.md is NEW (Mermaid)
    │   ├── [P] sources/, achievements/, evidence/, capabilities/
    │   ├── [P] signature-achievements.md, signature-themes.md
    │   ├── [P] executive-identity.md, voice-profile.md, positioning-statements.md
    │   ├── [P] narrative-library.md, messaging-library.md, story-library.md
    │   ├── [P] knowledge-gaps.md
    │   ├── [P] employment-records.yaml
    │   └── [P] **/*.md with [[wikilinks]]                         # NEW — every node wikilinked
    └── [P] <target-slug>/                                          # per-opportunity projections (resume, playbook, etc.)
```

Personal narrative HTMLs (`about/`, `architecture-philosophy/`, `articles/`, `narratives/*/index.html`, `portfolio/index.html`, `method-bridge.html`) **stay in place** — authored prose, no PII. The `.drawio` library and the BBC Python subproject stay.

`interview-playbook-generator/` becomes a frozen archive with a single `ARCHIVED.md` pointing at `mind-palace/`.

---

## 2. OKF v0.2 — kept verbatim, no generalisation in this plan

The spec, the type vocabulary, and the hard rules lift from `interview-playbook-generator/okf-spec/SPEC.md` and `interview-playbook-generator/AGENTS.md` without modification. Concretely:

- **Spec:** v0.2. Minimum frontmatter `type`; recommended `title`, `description`, `tags`, `generated`, `verified`, `status`, `stale_after`, `sources`. Statement classification `[evidence] / [inference] / [recommendation] / [assumption]`. Reserved filenames `index.md` and `log.md`.
- **Types stay career-centric for now:** `Source`, `SourceIndex`, `PortfolioAnalysis`, `Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `ExecutiveIdentity`, `VoiceProfile`, `PositioningStatements`, `NarrativeLibrary`, `StoryLibrary`, `MessagingLibrary`, `InterviewStrategy`, `KnowledgeGap` (+ v0.6 `archetype-*`, `gap-classifier`, `projection-strategy-generator`). Renaming these to a generic `Concept + concept_kind` vocabulary is **deferred** to a future refactor triggered by a real second consumer.
- **Hard rules** (from `AGENTS.md` §"The five hard rules"): never fabricate, classify every claim, attribute every claim, stop and ask, idempotent re-runs. Lifted verbatim into the new `mind-palace/AGENTS.md`.
- **Identity Preservation Invariant** and the other career-specific invariants stay in `mind-palace/AGENTS.md` (not yet moved to a consumer scope).

The only **additions** are:

- `out/okf/graph.md` — auto-generated Mermaid `flowchart TD` of the bundle (NEW).
- `[[wikilinks]]` injected into every node body by `okf-linkify` (NEW).
- `scripts/ci_local.sh` — local-CI runner that mirrors the GitHub Actions workflows (NEW; see §10.3).

---

## 3. Repo restructure — ordered, repo stays working at every step

All on a fresh `feature/restructure-into-okf-foundation` branch from `master`. Each numbered step is one PR. Steps 1–6 are Sprint 0; steps 7–10 are Sprint 1.

| # | Step | PR title |
|---|---|---|
| 1 | Replace `.gitignore` with the OKF-foundation template: ignore `out/`, `evidence/`, `*.pdf`, `__pycache__/`, secrets, `config/config.yaml`. Allow shareable fixture inputs. | `chore: tighten .gitignore for OKF foundation` |
| 2 | `cp -R /Users/avfranco/GitHub/interview-playbook-generator/{okf-spec,skills,tests,scripts,docs,config,.github,AGENTS.md,ARCHITECTURE.md,CLAUDE.md} → mind-palace/`. `git mv mind-palace/resume-profile → mind-palace/evidence/alexandre-franco/resume-profile`. Same for `target-position/`. | `feat: relocate pipeline into mind-palace + move raw PII under evidence/` |
| 3 | Update `mind-palace/README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md` to describe the new home. Keep `interview-playbook-generator` references as historical. Add `LICENSE` (MIT recommended). | `docs: rewrite operating triad for the mind-palace home + add LICENSE` |
| 4 | CI: rename the two existing test workflows to `okf-lint.yml` and `golden-snapshot.yml`. Keep `validate.yml` and `markdown-lint.yml`. Update `.markdownlint.json` to ignore `out/`, `evidence/`, `evaluation/`. | `ci: adopt GitHub Actions workflows for OKF foundation` |
| 5 | Add `scripts/ci_local.sh` — a bash runner that mirrors the four GitHub Actions jobs locally (pytest, okf-lint, golden snapshot, markdown-lint). | `ci: add local-ci runner script for Antigravity/CLI use` |
| 6 | First end-to-end run on the personal bundle. `python scripts/ingest_portfolio.py` produces `out/okf/`; orchestrator runs all 23 Skills; CI green on a PR titled "first OKF run". | `feat: first end-to-end OKF bundle run (no wikilinks, no graph yet)` |
| 7 | Add `skills/okf-linkify/SKILL.md` + `scripts/okf_linkify.py` (~150 lines). Walks `out/okf/**/*.md`, parses YAML frontmatter, rewrites each body line so references to other nodes' titles / slugs / footnote-resolved `sources[].id` become Obsidian-style `[[wikilinks]]`. Idempotent. Wired into `playbook-orchestrator/SKILL.md` as post-processing step after `story-engine`. | `feat(okf-linkify): Skill + script + idempotent wikilink post-processor` |
| 8 | Add `tests/test_okf_linkify.py` (~80 lines): for every `[^source-id]` in any node, the corresponding `Source` node's slug is linkified in at least one body line. If not, test fails. | `test(okf-linkify): structural test for wikilink integrity` |
| 9 | Add `skills/okf-graph/SKILL.md` + `scripts/generate_okf_graph.py` (~200 lines). Walks `out/okf/`, parses frontmatter and footnote references, emits `out/okf/graph.md` containing a Mermaid `flowchart TD` block + a Markdown node list with `[[wikilinks]]`. Wired into `playbook-orchestrator/SKILL.md` after `okf-linkify`. | `feat(okf-graph): Skill + script + Mermaid emitter` |
| 10 | Add `tests/test_okf_graph.py`: verifies the generated `graph.md` parses as Mermaid via `mermaid-cli` (`npx -p @mermaid-js/mermaid-cli mmdc -i out/okf/graph.md -o /tmp/graph.svg`). If `mmdc` not on PATH, test skips with a clear message. | `test(okf-graph): structural test for Mermaid render` |
| 11 | Open PR in `interview-playbook-generator`: add `ARCHIVED.md` pointing at `mind-palace/`. Update that repo's `README.md` to one line. | `chore(interview-playbook-generator): archive, point at mind-palace` |

`standard-operational-procedure/standard-operating-procedure.v1.md` stays unchanged at root. Sprints 0 and 1 follow it (Trigger → Frame → Specify → Plan → Implement → Verify → Refine → Capture).

---

## 4. Skills — `okf-linkify` and `okf-graph` (the only new ones)

### 4.1 `okf-linkify` (NEW)

**Purpose:** post-processor that injects `[[wikilinks]]` into every node body so the bundle is navigable in Obsidian / VS Code / GitHub.

**Frontmatter:**
```
name: okf-linkify
description: Idempotent post-processor. Walks out/okf/**/*.md, rewrites each node body so references to other nodes (by title, slug, or footnote-resolved sources[].id) become [[wikilinks]].
```

**Hard rules (lifted from `AGENTS.md`):** the five. Plus: never modify YAML frontmatter (linkify only touches body); never mutate other Skills' output files outside `out/okf/`; idempotent (re-run over same input produces same output).

**Execution:**
1. Walk `out/okf/**/*.md`, skip `index.md`, `log.md`, `graph.md`.
2. Parse YAML frontmatter of each node; build three maps: `slug → title`, `slug → sources[].id[]`, `sources[].id → slug`.
3. For each body line:
   - If the line contains `[^source-id]` and that source-id maps to a slug, append a `[[[slug]]]` marker after the line.
   - If the line contains a substring matching another node's title, replace with `[[[slug]]]`.
   - Preserve classification prefixes (`[evidence]`, etc.) and footnote markers.
4. Write back; update `generated.at`.
5. Append one entry to `out/okf/log.md`.

**Test (`tests/test_okf_linkify.py`):**
- For every `[^source-id]` in every node, the corresponding `Source` slug is linkified in at least one body line across the bundle.
- Running the script twice produces byte-identical output (idempotency check).
- Frontmatter is untouched (YAML parse before/after yields the same dict).

### 4.2 `okf-graph` (NEW)

**Purpose:** emit `out/okf/graph.md` containing a Mermaid `flowchart TD` of the bundle plus a Markdown node list with `[[wikilinks]]`.

**Frontmatter:**
```
name: okf-graph
description: Reads out/okf/**/*.md, emits out/okf/graph.md with a Mermaid flowchart TD of Source → Claim → EvidenceCard → Concept → Narrative edges and a Markdown node list with [[wikilinks]].
```

**Hard rules:** the five. Plus: never edit other Skills' output files; idempotent.

**Execution:**
1. Walk `out/okf/**/*.md`, parse frontmatter.
2. Build edge list:
   - For every `Claim` (Achievement) with `[^source-id]`, edge `Claim --> Source(slug)`.
   - For every `EvidenceCard`, edge `EvidenceCard --> Claim(slug)` (via body footnote refs).
   - For every `Concept` (Capability/Theme/Identity/...), edge `Concept --> Concept` for cross-references in body.
   - For every `Narrative`, edge `Narrative --> EvidenceCard(slug)` for body refs.
3. Emit `out/okf/graph.md`:
   ```markdown
   ---
   type: GraphIndex
   okf_version: "0.2"
   generated: { by: okf-graph, at: <iso> }
   ---

   # OKF Knowledge Graph

   ```mermaid
   flowchart TD
       Source(cv.md) --> Achievement(achievements/foo.md)
       Achievement --> EvidenceCard(evidence/foo.md)
       EvidenceCard --> Capability(capabilities/bar.md)
       ...
   ```

   ## Nodes
   - [[[cv]]] — Source: CV (2024 edition)
   - [[[achievements/foo]]] — Achievement: Foo
   - ...
   ```
4. Append one entry to `out/okf/log.md`.

**Test (`tests/test_okf_graph.py`):**
- Run `okf-graph` against the default bundle; verify `out/okf/graph.md` exists.
- If `mmdc` is on PATH (`which mmdc`), run `mmdc -i out/okf/graph.md -o /tmp/graph.svg` and assert exit 0. Otherwise skip with message "mmdc not installed; install with `npm i -g @mermaid-js/mermaid-cli` to enable".
- Running the script twice produces byte-identical output (idempotency).

---

## 5. CI

| Workflow | Trigger | Job |
|---|---|---|
| `okf-lint.yml` | PR/push on `skills/**`, `okf-spec/**`, `scripts/**`, `tests/test_lint.py` | `python -m pytest tests/test_lint.py tests/test_career_evidence_integrity.py tests/test_claim_evidence_validation.py tests/test_boundary_transferability.py -v` |
| `golden-snapshot.yml` | PR on `skills/**`, `tests/fixtures/**`, `tests/golden/**` | `python scripts/run_skill.py` for each Skill; `pytest tests/ -v -k golden` |
| `validate.yml` | PR/push | Required files exist (`AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `README.md`, `okf-spec/SPEC.md`, `tests/test_lint.py`, `scripts/ci_local.sh`) |
| `markdown-lint.yml` | PR/push | `markdownlint-cli`; `.markdownlint.json` ignores `out/`, `evidence/`, `evaluation/` |

**Local CI (`scripts/ci_local.sh`)** mirrors all four jobs so the same checks run without GitHub Actions — needed for Antigravity CLI implementation (§10).

---

## 6. Roadmap — two sprints

### Sprint 0 — relocate (~3 days)

**Outcome hypothesis:** A clean, working OKF pipeline in `mind-palace`. The proven career-projection flow runs end-to-end. CI green. Personal PII under `evidence/`. `out/` gitignored.

**Exit criteria:**
- `.gitignore` covers `out/`, `evidence/`, `*.pdf`, `__pycache__/`, secrets.
- `okf-spec/SPEC.md` (v0.2) committed.
- `evidence/alexandre-franco/{resume-profile,target-position}/` populated from `mind-palace/resume-profile/` and `mind-palace/target-position/`.
- All 30+ Skills, all tests, all fixtures, all golden snapshots, all scripts, all docs, all `.github/workflows/` files moved from `interview-playbook-generator/` to `mind-palace/`.
- `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `README.md` rewritten for the new home. `LICENSE` added.
- All four CI workflows green on the first PR.
- `scripts/ci_local.sh` runs the same checks locally.

**Issues to open:**
1. `chore: tighten .gitignore for OKF foundation (out/, evidence/, *.pdf)`
2. `feat: relocate pipeline into mind-palace + move raw PII under evidence/`
3. `docs: rewrite operating triad for the mind-palace home + add LICENSE`
4. `ci: adopt GitHub Actions workflows for OKF foundation`
5. `ci: add local-ci runner script for Antigravity/CLI use`
6. `feat: first end-to-end OKF bundle run (no wikilinks, no graph yet)`

### Sprint 1 — visualise (~1 week)

**Outcome hypothesis:** The OKF bundle is *navigable*. Every node wikilinks to every other node it references. A Mermaid diagram shows the whole graph. Tests enforce both. CI runs `mmdc` if available.

**Exit criteria:**
- `skills/okf-linkify/SKILL.md` + `scripts/okf_linkify.py` + `tests/test_okf_linkify.py` exist; idempotency + wikilink-integrity tests pass.
- `skills/okf-graph/SKILL.md` + `scripts/generate_okf_graph.py` + `tests/test_okf_graph.py` exist; Mermaid render test passes (or skips clearly if `mmdc` missing).
- `playbook-orchestrator/SKILL.md` runs both Skills as post-processing steps.
- `out/okf/graph.md` is regenerated on every orchestrator run; Mermaid parses.
- `interview-playbook-generator` archived.

**Issues to open:**
7. `feat(okf-linkify): Skill + script + idempotent wikilink post-processor`
8. `test(okf-linkify): structural test for wikilink integrity`
9. `feat(okf-graph): Skill + script + Mermaid emitter`
10. `test(okf-graph): structural test for Mermaid render`
11. `chore(interview-playbook-generator): archive, point at mind-palace`

---

## 7. Reused references (lift from `interview-playbook-generator`)

All files in this list move verbatim. The few files that get *modified* are listed in §3 by PR title.

### Operating triad (modified in PR-3)
- `AGENTS.md` → rewrite opening sections to describe the new home; five hard rules stay verbatim.
- `CLAUDE.md` → rewrite opening sections; Skill invocation discipline + lint discipline + snapshot-test guidance stay.
- `ARCHITECTURE.md` → rewrite opening sections; 4-layer pipeline + ER diagram stay.

### Spec, fixtures, golden, tests (verbatim)
- `okf-spec/SPEC.md` (v0.2)
- `tests/conftest.py`, `tests/fixtures/*`, `tests/golden/*`
- `tests/test_lint.py` and all `tests/test_*.py`
- `config/config.example.yaml`

### Skills (verbatim)
All 30+ files in `skills/<name>/SKILL.md`.

### Scripts (verbatim, plus two NEW)
- `scripts/ingest_portfolio.py`
- `scripts/generate_architecture_diagrams.py`
- `scripts/employment_validator.py`

### Docs (verbatim)
- `docs/requirements-spec.md`, `docs/spec-refinements.md`, `docs/architecture/*`
- `docs/prompt-resume-*.md`, `docs/pull_request_description_*.md`
- `docs/superpowers/specs/*` (all 14 specs)

### CI (verbatim, plus renamed)
- `.github/workflows/okf-lint.yml` (adopted from existing test workflow)
- `.github/workflows/golden-snapshot.yml` (adopted from existing pytest workflow)
- `.github/workflows/validate.yml` (adapted)
- `.github/workflows/markdown-lint.yml` (verbatim)

---

## 8. Critical files

- `/Users/avfranco/GitHub/mind-palace/.gitignore` — first edit; gates the personal surface.
- `/Users/avfranco/GitHub/mind-palace/okf-spec/SPEC.md` — v0.2 verbatim; defines the universal contract.
- `/Users/avfranco/GitHub/mind-palace/skills/okf-linkify/SKILL.md` + `/Users/avfranco/GitHub/mind-palace/scripts/okf_linkify.py` — the linkifier.
- `/Users/avfranco/GitHub/mind-palace/skills/okf-graph/SKILL.md` + `/Users/avfranco/GitHub/mind-palace/scripts/generate_okf_graph.py` — the graph emitter.
- `/Users/avfranco/GitHub/mind-palace/skills/playbook-orchestrator/SKILL.md` — updated to invoke the two new Skills as post-processing.
- `/Users/avfranco/GitHub/mind-palace/scripts/ci_local.sh` — local CI; the contract Antigravity CLI enforces (§10.3).
- `/Users/avfranco/GitHub/mind-palace/AGENTS.md` — operating manual; the five hard rules.
- `/Users/avfranco/GitHub/mind-palace/standard-operational-procedure/standard-operating-procedure.v1.md` — governs foundation work itself.
- `/Users/avfranco/GitHub/interview-playbook-generator/ARCHIVED.md` — pointer to the new home.

---

## 9. Verification — end-to-end after Sprint 1

1. **Lint on default fixtures:**
   ```
   pytest tests/test_lint.py tests/test_career_evidence_integrity.py -v
   ```
   Expect: zero errors against the existing fixture set in `tests/fixtures/`.

2. **Golden-snapshot regeneration:**
   ```
   pytest tests/ -v -k golden
   ```
   Expect: every Skill with a `tests/golden/<skill>/` fixture passes a structural diff.

3. **Full orchestrator run:**
   ```
   python scripts/ingest_portfolio.py
   python scripts/run_skill.py --skill playbook-orchestrator
   ```
   Expect: `out/okf/` populated; `out/<target-slug>/` populated; `out/okf/graph.md` regenerated; `[[wikilinks]]` present in every node body.

4. **Link integrity check:**
   ```
   pytest tests/test_okf_linkify.py -v
   ```
   Expect: zero errors. Every `[^source-id]` resolves to a `[[[slug]]]` somewhere in the bundle.

5. **Mermaid render check:**
   ```
   npx -p @mermaid-js/mermaid-cli mmdc -i out/okf/graph.md -o /tmp/graph.svg
   ```
   Expect: exit 0; SVG produced.

6. **Local CI:**
   ```
   bash scripts/ci_local.sh
   ```
   Expect: all four checks (lint, golden, validate, markdown) pass.

7. **GitHub CI green** on a PR that changes a Skill: `okf-lint.yml`, `golden-snapshot.yml`, `validate.yml`, `markdown-lint.yml` all pass.

8. **Governance self-check:** open an Issue to add a new Skill and follow the eight-stage SOP — Trigger → Frame → Specify → Plan → Implement → Verify → Refine → Capture — as proof that the foundation obeys its own contract.

---

## 10. Implementation toolchain — Speckit + Antigravity CLI

### 10.1 Phasing

The work is split across two LLM surfaces to stay within the user's token budget:

- **Speckit (in Claude Code):** the four planning phases — `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`. Produces `docs/superpowers/specs/<NNNN>-<slug>/{spec.md,plan.md,tasks.md}`. Heavy on planning tokens, light on implementation tokens.
- **Antigravity CLI:** the implementation phase. Reads `tasks.md` line by line, executes each task, runs `bash scripts/ci_local.sh` after each task, opens a PR per task group.

This is the most token-efficient shape because Speckit does the expensive thinking once, and Antigravity's job becomes mechanical execution of a pre-decided list — no architectural interpretation required at execution time.

### 10.2 Speckit output shape

Per the existing convention in `docs/superpowers/specs/`, one folder per work item:

```
docs/superpowers/specs/2026-08-15-relocate-pipeline-into-mind-palace/
    spec.md      # from /speckit.specify
    plan.md      # from /speckit.plan
    tasks.md     # from /speckit.tasks — line-by-line executable list
```

The 11 issues from §6 produce 11 such folders (or grouped: 6 in Sprint 0, 5 in Sprint 1). Each `tasks.md` ends with a "Verification" block mirroring §9.

### 10.3 Antigravity CLI expectations

Antigravity receives the tasks list and runs each one in a fresh context. Per-task contract:

1. Read the relevant files (no whole-repo dump).
2. Make the smallest change that satisfies the task.
3. Run `bash scripts/ci_local.sh` (the local CI mirror of GitHub Actions — this is the single most important contract). If CI fails, fix and retry; do not move on.
4. Commit on the current branch; reference the issue number in the commit message.
5. Update `docs/superpowers/specs/<...>/tasks.md` with a `[x]` next to the completed task and a one-line note.

`scripts/ci_local.sh` runs locally without GitHub Actions:

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "== okf-lint =="
python -m pytest tests/test_lint.py tests/test_career_evidence_integrity.py tests/test_claim_evidence_validation.py tests/test_boundary_transferability.py -v
echo "== golden-snapshot =="
python scripts/run_skill.py --skill playbook-orchestrator --tenant default || true
python -m pytest tests/ -v -k golden
echo "== validate =="
test -f AGENTS.md && test -f ARCHITECTURE.md && test -f CLAUDE.md && test -f README.md && test -f okf-spec/SPEC.md && test -f scripts/ci_local.sh
echo "== markdown-lint =="
npx -y markdownlint-cli '**/*.md' --config .markdownlint.json
echo "== all checks passed =="
```

Antigravity must invoke this script after every meaningful change and only commit when it exits 0.

### 10.4 Constraints to call out before starting

Three things to confirm with the Antigravity CLI environment before Sprint 0 begins. None are blockers; each is a 30-minute setup step:

1. **Skill portability.** Antigravity's Skill system uses a similar Markdown+YAML shape, but the invocation model and what the agent does with each Skill differ from Claude Code. Verify that `skills/<name>/SKILL.md` (with `name` + `description` frontmatter) is consumable by Antigravity's task system. If not, the Skills live as documentation only and Antigravity executes its own task list directly from `tasks.md`.

2. **Token budget per task.** Antigravity CLI runs each task in a fresh context. The `tasks.md` for each issue must be small enough to fit in one context window with the relevant files. Aim for ≤10 sub-tasks per `tasks.md`. If a task grows larger, split it.

3. **mmdc availability.** Sprint 1's Mermaid test requires `@mermaid-js/mermaid-cli` on PATH. Confirm whether Antigravity CLI's environment has Node.js + npm. If not, the test gracefully skips with a clear message; the bundle still generates Mermaid text, just no SVG render.

### 10.5 What Antigravity CLI is NOT expected to do

- Make architectural decisions. Every decision is already in §3 of this plan.
- Rewrite Skills unless a task explicitly says so. Most Skills lift verbatim.
- Touch `out/` or `evidence/` except via the Skills that are designed to.
- Push to remote. PRs are opened locally; the user reviews and merges.

### 10.6 What the user does between Antigravity sessions

- Review the PR per issue (1 of 11).
- Merge when green.
- Open the next Speckit issue if a new question emerges.
- Re-prioritise `tasks.md` lines if implementation reveals a sequencing issue.

This keeps the user as architect/decision-maker per the canonical SOP — Speckit thinks, Antigravity executes, the user approves, the repo gains evidence.