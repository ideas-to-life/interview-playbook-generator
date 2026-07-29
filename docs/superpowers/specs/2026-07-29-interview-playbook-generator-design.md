# Interview Playbook Generator — Design Spec

**Status:** Draft, awaiting user review
**Date:** 2026-07-29
**Author:** Brainstorming session (Claude + Alexandre Franco)
**Repo:** `interview-playbook-generator`
**Baseline spec:** `requirements-spec.md` (approved)
**Refinements:** `spec-refinements.md` (applied)

---

## 1. Purpose and scope

### 1.1 Purpose

Generate a high-quality interview preparation package from a candidate's portfolio and career knowledge, with these guarantees:

- Grounded in evidence — never invents projects, metrics, team sizes, budgets, technologies, or responsibilities.
- Adapts to different role types.
- Reuses knowledge consistently across runs.
- Preserves the candidate's authentic voice.
- Optimised for executive conversations.

### 1.2 In scope for v0.1

- A thin-slice pipeline of 6 producer Skills (portfolio-ingestor, portfolio-analyzer, achievement-extractor, evidence-card-generator, interview-strategy-generator, playbook-assembler), plus a `playbook-orchestrator` Skill that drives the pipeline, plus a `knowledge-gaps` Skill that runs as a pre-assembly gate. Total: 8 Skills in v0.1.
- The pipeline turns raw portfolio files plus a target opportunity into a populated OKF knowledge graph and a human-readable Interview Playbook view.
- Local-first execution via Claude Code (or Antigravity).
- Snapshot-tested, lint-enforced, idempotent Skills.

### 1.3 Out of scope for v0.1 (binding guardrails)

The following are explicitly deferred and must not be added in v0.1:

- Competency ontology / catalogue
- View generator (stage-specific packs)
- Career narrative evolution
- Mock interviews
- Conversation simulator
- LLM-as-judge evaluation
- Company research
- Salary research
- Market intelligence
- Advanced OKF linting

The guiding principle: **optimise for a working end-to-end interview pipeline, not a complete career intelligence platform.** Every Skill in v0.1 must directly improve the quality of the generated interview playbook for real interview preparation.

---

## 2. Architecture

### 2.1 One-sentence architecture

A local-first pipeline of Claude Skills in this repo reads a YAML config plus raw portfolio sources, runs Skills that progressively structure the candidate's career into an OKF v0.2 knowledge graph on disk, and a final assembler Skill generates the human-readable Interview Playbook view from the graph.

### 2.2 Load-bearing principles

1. **OKF bundle is the primary artefact.** Every Skill reads/writes an OKF bundle on disk. The Interview Playbook is one view of that bundle. The same bundle can later be sliced into Recruiter / CTO / Executive / Technical packs without re-running analysis.
2. **Skills, not code.** Each Skill is a `SKILL.md` file the user invokes in Claude Code (or Antigravity). No Skill calls an LLM API directly — Claude Code *is* the runtime. State between Skills is the OKF bundle on disk.
3. **Provenance is non-negotiable.** Every statement in the bundle is classified `[evidence | inference | recommendation | assumption]`. Every concept carries a `sources` list with per-source attribution. The Skills never invent values from the NEVER_FABRICATE list — they stop and prompt the user when source is missing.
4. **Thin slice first.** v0.1 ships 8 Skills end-to-end: the 6-Skill producer chain (portfolio-ingestor → portfolio-analyzer → achievement-extractor → evidence-card-generator → interview-strategy-generator → playbook-assembler) plus the `playbook-orchestrator` driver and the pre-assembly `knowledge-gaps` gate. The full 19-Skill pipeline is v0.2+.
5. **Configurable input, predictable output.** Sources are declared in a YAML config (with CLI overrides and interactive prompts as fallbacks). Outputs land at predictable paths in the configured output directory.

### 2.3 Composition with other experiments

The Skills pipeline produces and consumes an OKF v0.2 bundle. This aligns with the candidate's other experiments (CAS, Ideas-to-Life, Publishing Workflow) when they also produce/consume OKF bundles. The pipeline is one more OKF producer/consumer in that ecosystem; no custom interop glue is required.

---

## 3. Repository layout

```
interview-playbook-generator/
├── README.md
├── CLAUDE.md                          # Claude Code project memory
├── requirements-spec.md
├── spec-refinements.md
├── config/
│   ├── config.example.yaml
│   └── portfolio.example/             # tiny fixture portfolio for dev/tests
├── skills/                            # one directory per Skill
│   ├── playbook-orchestrator/SKILL.md
│   ├── portfolio-ingestor/SKILL.md
│   ├── portfolio-analyzer/SKILL.md
│   ├── achievement-extractor/SKILL.md
│   ├── evidence-card-generator/SKILL.md
│   ├── interview-strategy-generator/SKILL.md
│   ├── playbook-assembler/SKILL.md
│   └── knowledge-gaps/SKILL.md
├── okf-spec/                          # vendored OKF v0.2 SPEC.md + reference examples
│   ├── SPEC.md
│   └── reference/
│       ├── index.md.example
│       └── concept.md.example
├── tests/
│   ├── fixtures/                      # sample portfolios
│   ├── golden/                        # golden OKF subtrees
│   └── test_*.py                      # pytest + filecmp.dircmp snapshot tests
├── out/                               # default output (gitignored)
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-07-29-interview-playbook-generator-design.md
└── .gitignore
```

Notes:

- `skills/<name>/SKILL.md` matches Claude Code's Skills convention. Each Skill's directory may carry an `examples/` subdirectory and a `schema.md` next to its `SKILL.md`.
- `okf-spec/` is vendored so Skills have a local reference. The upstream is `github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf`.
- `tests/golden/` holds OKF subtree snapshots; tests are plain `pytest` plus `filecmp.dircmp`. No LLM calls in unit tests.
- `out/` is gitignored; the user configures output paths via YAML or CLI.

---

## 4. Configuration

`config/config.example.yaml`:

```yaml
project:
  name: "Master Interview Playbook"
  version: "0.1"

candidate:
  name: ""                 # prompted if absent

inputs:
  portfolio: "config/portfolio.example/"
  cv: ""                   # prompted if absent
  linkedin: ""
  publications: ""
  architecture_docs: ""
  presentations: ""

target_opportunity:
  source: ""               # path to JD | recruiter_msg | role_summary
  type: ""                 # job_description | recruiter_message | role_summary
  company: ""
  industry: ""
  interviewer: ""
  interview_stage: ""      # recruiter_screen | hiring_manager | panel | executive | final
  recruiter_notes: ""

output:
  okf_bundle: "./out/okf/"
  playbook_view: "./out/playbook.md"
  stage_packs: "./out/packs/"

pipeline:
  skills:
    - portfolio-ingestor
    - portfolio-analyzer
    - achievement-extractor
    - evidence-card-generator
    - interview-strategy-generator
    - knowledge-gaps
    - playbook-assembler
  run_knowledge_gaps: true
  fail_on_severe_gaps: false
```

Resolution rules (in priority order):

1. CLI flags override YAML (e.g., `playbook run --cv=… --jd=…`).
2. YAML values override prompts.
3. Missing values prompt the user interactively via the orchestrator Skill.

---

## 5. OKF schema for this project

We honour OKF v0.2 required and recommended fields and add project-specific extensions. The bundle root `index.md` carries `okf_version: "0.2"`.

### 5.1 Common frontmatter (every concept)

```yaml
---
type: <concept-type>          # REQUIRED by OKF; one of the project types below
title: "<human-readable>"
description: "<one-line summary>"
tags: [<tag>, ...]
generated: { by: human:<id> | <skill-name>/<llm-model>, at: <ISO-8601> }
verified: [{ by: human:<id>, at: <ISO-8601> }, ...]   # absent ⇒ unverified
status: draft | stable | deprecated
stale_after: YYYY-MM-DD
sources:
  - id: <stable-key>
    resource: <absolute URL | bundle-relative path | references/ path | scope>
    title: "<source label>"
    author: <optional>
    last_modified: <optional>
---
```

### 5.2 Project concept types

These extend OKF v0.2's open `type` vocabulary. Consumers MUST tolerate unknown `type` values, so future Skills can add new types without breaking earlier bundles.

| `type` | Where it lives | Purpose | v0.1? |
|---|---|---|---|
| `SourceIndex` | `okf/sources/index.md` | Discovered source list, classification, provenance | yes |
| `Source` | `okf/sources/<name>.md` | One per discovered portfolio artefact | yes |
| `PortfolioAnalysis` | `okf/portfolio.md` | Top-level analysis and coverage map | yes |
| `Achievement` | `okf/achievements/<slug>.md` | One per extracted achievement, evidence-grounded | yes |
| `EvidenceCard` | `okf/evidence/<slug>.md` | Reusable STAR card | yes |
| `InterviewStrategy` | `okf/interview-strategy.md` | Concise strategy briefing | yes |
| `KnowledgeGap` | `okf/knowledge-gaps.md` | Missing-evidence report; recommendations | yes |
| `Playbook` (view, not a bundle node) | `out/playbook.md` | The human-readable view produced by the assembler | yes |
| `TimelineEntry` | `okf/timeline/<slug>.md` | One per role in career timeline | v0.2 |
| `Competency` | `okf/competencies/<slug>.md` | Competency node linked from achievements | v0.2 |
| `Theme` | `okf/themes/<slug>.md` | Recurring signature theme | v0.2 |
| `Narrative` | `okf/narratives/<slug>.md` | 30s / 2min / 5min / executive / coffee / recruiter variants | v0.2 |
| `Role` | `okf/roles/current-role.md` | Parsed target opportunity | v0.2 |
| `Fit` | `okf/fit/current-role.md` | Role-to-evidence mapping | v0.2 |
| `QAPair` | `okf/qa/technical/*.md`, `okf/qa/executive/*.md` | Question + suggested answer | v0.2 |
| `Question` | `okf/questions/<slug>.md` | Question to ask the interviewer | v0.2 |
| `SalaryStrategy` | `okf/salary.md` | Salary negotiation strategy | v0.2 |

### 5.3 Per-statement classification (in body)

Every claim in a concept body starts with a classification marker:

```markdown
[evidence] Led the migration of the X platform to Y. [^cv-2024]
[inference] This required stakeholder management across three regions.
[recommendation] When discussing in interviews, lead with the Y migration outcome.
[assumption] Team size was approximately 20 (not stated explicitly in source).
```

Marker semantics:

- `[evidence]` — directly stated in a source. Must be accompanied by a `[^source-id]` footnote that resolves to an entry in the concept's `sources` list.
- `[inference]` — derived from one or more pieces of evidence. The reasoning must be stated in the same line or the next.
- `[recommendation]` — the candidate should do or say this in the interview. Always grounded in an earlier `[evidence]` or `[inference]` line.
- `[assumption]` — a value the Skill needed but did not find in any source. Flagged so the user can confirm, replace, or remove it.

### 5.4 Per-claim source attribution (in body)

OKF v0.2 footnote-style attribution with `sources[].id` as the join key:

```markdown
[^cv-2024] Senior Staff Engineer, Acme Corp, 2022–2024
```

The footnote label resolves to an entry in the concept's frontmatter `sources` list. This is in addition to (not instead of) the body's classification markers.

### 5.5 Cross-linking

Edges are markdown links:

- `Achievement → EvidenceCard`: the evidence card's body links to its source achievements, and vice versa.
- `Achievement → Competency` (v0.2): competency nodes live under `okf/competencies/`.
- `EvidenceCard → PossibleQuestion` (v0.2): the card lists possible interview questions, each linking to `okf/questions/<slug>.md`.
- `Playbook (view) → bundle node`: the assembler's output uses bundle-relative links starting with `/` (OKF-recommended) so docs can move within their subdirectory without breaking links.

### 5.6 Trust and lifecycle defaults

- New concepts start `status: draft` with no `verified` key (unverified).
- The user promotes a concept to `status: stable` by reading it and either accepting as-is or editing — that is the `verified: [{ by: human:<id>, at: ... }]` event.
- `stale_after` is set by the producing Skill, defaulting to 90 days after `generated.at`. The user may override per concept.
- The playbook assembler shows trust tier in the playbook view: every section header shows a `[draft]`, `[machine-confirmed]`, or `[human-reviewed]` badge. The user can grep for `[draft]` to find every part of the playbook that has not been personally reviewed.

### 5.7 Reserved filenames

Per OKF v0.2, `index.md` and `log.md` are reserved. The bundle root `index.md` carries `okf_version: "0.2"`. Other directories' `index.md` files contain only a body listing concepts as `* [Title](relative-url) - short description`. `log.md` records change history (newest first, ISO-8601 date headings) and is updated by every Skill after it writes.

---

## 6. Skills

### 6.1 Full list with v0.1 scope

| # | Skill | Reads from bundle | Writes to bundle | v0.1? |
|---|---|---|---|---|
| 0 | `playbook-orchestrator` | (config) | (drives the pipeline) | yes |
| 1 | `portfolio-ingestor` | raw portfolio files | `okf/sources/index.md`, `okf/sources/*.md` | yes |
| 2 | `portfolio-analyzer` | `okf/sources/*` | `okf/portfolio.md` | yes |
| 3 | `achievement-extractor` | `okf/sources/*` | `okf/achievements/*.md` | yes |
| 4 | `evidence-card-generator` | `okf/achievements/*` | `okf/evidence/*.md` | yes |
| 5 | `interview-strategy-generator` | `okf/evidence/*`, target opportunity | `okf/interview-strategy.md` | yes |
| 6 | `knowledge-gaps` | whole bundle | `okf/knowledge-gaps.md` | yes (gate) |
| 7 | `playbook-assembler` | whole bundle | `out/playbook.md` | yes |
| 8 | `career-timeline-builder` | `okf/sources/*` | `okf/timeline/*.md` | v0.2 |
| 9 | `competency-mapper` | `okf/achievements/*` | `okf/competencies/*.md` | v0.2 |
| 10 | `star-generator` (length variants) | `okf/evidence/*` | extends `okf/evidence/*.md` | v0.2 |
| 11 | `signature-theme-miner` | `okf/competencies/*`, `okf/evidence/*` | `okf/themes/*.md` | v0.2 |
| 12 | `narrative-generator` | `okf/timeline/*`, `okf/themes/*`, `okf/evidence/*` | `okf/narratives/*.md` | v0.2 |
| 13 | `role-analyzer` | target opportunity | `okf/roles/current-role.md` | v0.2 |
| 14 | `fit-mapper` | `okf/roles/*`, `okf/evidence/*` | `okf/fit/current-role.md` | v0.2 |
| 15 | `role-overlay-builder` (presentation) | `okf/roles/*`, `okf/fit/*` | `okf/overlay.md` | v0.2 |
| 16 | `technical-qa-generator` | competencies + overlay | `okf/qa/technical/*.md` | v0.2 |
| 17 | `executive-qa-generator` | themes + overlay | `okf/qa/executive/*.md` | v0.2 |
| 18 | `question-generator` | overlay + competencies | `okf/questions/*.md` | v0.2 |
| 19 | `salary-strategy-generator` | overlay + bundle | `okf/salary.md` | v0.2 |

### 6.2 Each v0.1 Skill's contract

**`playbook-orchestrator`** — Reads the YAML config, validates inputs (paths exist, types set), and walks the user through the pipeline. Lists Skills in order, says what each does, and tells the user to invoke the next Skill. Surfaces the `knowledge-gaps` report between `interview-strategy-generator` and `playbook-assembler` and asks the user whether to continue. Exits when `playbook-assembler` is done.

**`portfolio-ingestor`** — Walks the configured input paths. For each file, classifies it (CV, LinkedIn export, slide deck, arch doc, publication, recruiter message, JD, etc.) and emits one `Source` concept under `okf/sources/`. Builds `okf/sources/index.md` with one entry per source plus a coverage map (which `type` of source is present, how many of each, which target-opportunity input types are covered). Each `Source` carries `sources[].resource` pointing at the file path and any frontmatter extracted (author, last_modified, language). Does not analyse content — that is the next Skill's job.

**`portfolio-analyzer`** — Reads `okf/sources/*` and produces `okf/portfolio.md`: a top-level analysis with (a) what is in the portfolio, (b) what is missing or thin (links forward to `knowledge-gaps`), (c) inferred themes at a glance (inference-flagged), and (d) provenance summary. Does not extract achievements — that is a separate concern with its own Skill.

**`achievement-extractor`** — Reads `okf/sources/*`, extracts achievements as `Achievement` nodes under `okf/achievements/`. Each achievement: (a) names what happened, (b) cites its source(s) via `sources` plus footnote attribution, (c) classifies every statement, (d) is marked `status: draft` until reviewed. Hard rule: no metrics, team sizes, budgets, technologies, or scope are invented — if a value is not in the source, the achievement either omits it or marks `[assumption]`.

**`evidence-card-generator`** — Reads `okf/achievements/*`, produces reusable STAR `EvidenceCard` nodes under `okf/evidence/`. Each card carries: Situation, Actions, Results, Lessons, Competencies demonstrated (links to v0.2 competency nodes when they exist), Tags, Possible interview questions, Supporting artefacts (links to `Source` nodes), Confidence level, and full source attribution. Short/medium/detailed STAR variants are a v0.2 Skill — v0.1 cards are detailed only.

**`interview-strategy-generator`** — Reads `okf/evidence/*` and the target opportunity (JD / recruiter message / role summary). Produces `okf/interview-strategy.md`: top differentiators, recommended narrative, strongest evidence cards (links), likely objections, mitigation for each, interview priorities. All strategy claims are `[inference]` or `[recommendation]`; the underlying evidence cards remain the source of truth.

**`knowledge-gaps`** — Walks the bundle, the target opportunity, and the interview strategy. Identifies missing evidence (e.g., target opportunity asks for a skill the candidate has no Achievement or EvidenceCard for), marks affected downstream nodes as `status: draft`, and recommends portfolio improvements (e.g., "add a slide deck on your X experience to address the Y requirement"). Emits `okf/knowledge-gaps.md`. Severity buckets: `critical` (blocks confident interview prep), `moderate` (weakens the narrative), `minor` (nice-to-have). The orchestrator surfaces this to the user; the run continues unless `fail_on_severe_gaps: true`.

**`playbook-assembler`** — Walks the bundle, composes the human-readable Interview Playbook at `out/playbook.md`. Sections present in v0.1: Executive Summary (Section 1), Fit Assessment (Section 3, simplified — without dimension stars until competencies are mapped in v0.2), Personal Narrative (Section 4, partial — until narratives are generated in v0.2), Evidence Library (Section 6), Interview Strategy (Section 9 stand-in), plus a clear "what is not yet generated" section pointing at v0.2 Skills. Optional stage packs (`out/packs/recruiter.md`, `out/packs/cto.md`, etc.) come later.

---

## 7. Error handling and quality gates

### 7.1 Classification discipline (load-bearing)

Every claim in every concept body MUST start with one of the four markers in §5.3. Enforcement:

- Every Skill's `SKILL.md` includes a final pass: scan the body, reject any non-empty non-heading line that does not start with a marker.
- A shared `okf-lint` helper (called by every Skill, not a separate v0.1 Skill) runs the same scan and lists violations before write.
- The orchestrator pauses on lint failures and surfaces them to the user.

### 7.2 Never-fabricate contract

A `NEVER_FABRICATE` list is included verbatim in every Skill's `SKILL.md` and in `CLAUDE.md`:

```
NEVER FABRICATE:
- Projects (named programmes, products, systems)
- Metrics (percentages, dollar figures, counts)
- Team sizes
- Budgets
- Technologies (named tools, languages, platforms)
- Responsibilities
- Tenure (start/end dates when not in source)
```

When a Skill needs a value on this list and cannot find it in any source:

1. Search all sources again (sometimes the value is in a different document).
2. If still missing, write the value as `[assumption]` with a clear marker the user can grep for.
3. Mark the containing concept `status: draft`.
4. Reference the missing value in `okf/knowledge-gaps.md` with a recommended portfolio improvement.

The Skills never invent plausible-sounding numbers.

### 7.3 Stop-and-ask protocol

When a Skill is uncertain about something load-bearing, it stops and asks the user rather than guessing. Triggers (each Skill lists its own):

- Target opportunity is missing or unparseable.
- Portfolio path is missing or empty.
- A required field is ambiguous (two reasonable readings).
- Classification cannot be determined.
- `knowledge-gaps` reports a `critical` gap AND `fail_on_severe_gaps: true` in config.

### 7.4 Idempotency and re-runs

Every Skill is idempotent given the same inputs:

- Input set = set of files the Skill reads (bundle subtree plus config). Two runs with the same input set produce the same output set.
- Re-running a Skill overwrites its output directory; it does not append.
- Cross-Skill outputs are not touched by a Skill that did not write them.
- The `generated.at` timestamp updates on every write; `verified` is preserved if the body is unchanged.
- A "what changed since last run" note is appended to `okf/log.md` by each Skill.

### 7.5 Failure handling

Three failure classes, each handled differently:

1. **Lint / classification failure** — Skill re-runs the lint pass and rewrites the body, then writes. If the body still fails, the Skill reports the violations and exits without writing. The orchestrator surfaces this to the user.
2. **Missing source for a required field** — Skill writes the concept with `[assumption]` markers and `status: draft`. Downstream Skills see `status: draft` and either skip the concept or include it with a visible "draft" badge in the playbook view.
3. **Pipeline failure** — The OKF bundle on disk is the source of truth. Partial output is preserved. Re-running the failed Skill resumes from where it stopped. Nothing is rolled back.

### 7.6 Provenance and trust at the bundle level

Trust tiers from OKF v0.2 §5.3 apply per concept:

- Unverified — no `verified` key. Default for new concepts.
- Machine-confirmed — `verified` list contains only non-`human:` actors.
- Human-reviewed — `verified` list contains at least one `human:<id>` entry.

The playbook assembler shows trust tier in the playbook view. The user can grep for `[draft]` to find every part of the playbook that has not been personally reviewed.

---

## 8. Testing strategy

### 8.1 Snapshot testing (catches Skill regressions)

Each Skill ships with a snapshot test in `tests/test_<skill>.py`:

```python
def test_skill_name():
    fixture = "tests/fixtures/portfolio_minimal/"
    golden  = "tests/golden/skill_name/"
    actual  = run_skill_in_tempdir(skill="skill-name", config=fixture + "config.yaml")
    diff = filecmp.dircmp(actual, golden)
    assert not diff.diff_files, f"Drift: {diff.diff_files}"
    assert not diff.left_only, f"Unexpected new files: {diff.left_only}"
    assert not diff.right_only, f"Missing files: {diff.right_only}"
```

- The first run creates the golden tree (manually reviewed and committed).
- Subsequent runs fail on any structural drift.
- Snapshot diffs are structural only — they do not fail on `generated.at` timestamp drift (timestamps are stripped before comparison).
- Snapshot diffs do not validate prose quality. LLM-as-judge eval is deferred (out of v0.1 scope).

### 8.2 Test pyramid for v0.1

| Test | What it catches | Speed |
|---|---|---|
| Snapshot per Skill | Structural drift, missing concepts, broken schema | Fast (no LLM) |
| End-to-end thin slice | Integration drift between Skills, broken cross-links | Fast (no LLM, just file diffs) |
| Lint check | Un-classified statements, missing source attribution | Fast (no LLM) |
| Manual review of golden | Prose quality, voice, classification correctness | Slow, human |

### 8.3 What is NOT tested in v0.1

Market positioning accuracy, salary ranges, company research — these are inference-class outputs and the deferred LLM-as-judge suite grades them later.

---

## 9. Success criteria for v0.1

The thin slice is "done" when **all** of the following are true:

1. The pipeline runs end-to-end on the example portfolio. A fresh clone plus `playbook run --config=config/config.example.yaml` produces a populated OKF bundle and an `out/playbook.md` without manual intervention.
2. Every concept in the bundle carries source attribution. A grep for `[^` finds at least one match in every concept. A grep for un-classified statements finds zero.
3. The playbook view never claims something not in the bundle. The assembler walks the bundle — no LLM generation of playbook text from outside the graph.
4. Snapshot tests pass. All eight v0.1 Skills (the 6 producer Skills plus orchestrator and knowledge-gaps) have a green test against their golden fixture. CI-ready.
5. `knowledge-gaps.md` is generated and surfaced. Even when no gaps exist, the file is emitted with "no critical gaps" so the user knows the gate ran.
6. The user can iterate. Edit a config field, re-run, see the diff. The bundle is the source of truth; nothing is regenerated from a hidden internal state.
7. The never-fabricate list is enforced. A test case where a fixture deliberately omits a team size produces a card with `[assumption]` markers, not a fabricated number.
8. The Skills work in both Claude Code and Antigravity. Each `SKILL.md` uses only the conventional frontmatter and instructions (no Claude-Code-only syntax). Validation: the Skills install cleanly in both runtimes.

---

## 10. Iteration path to v0.2

The pipeline is shaped so v0.2 lands naturally without rewriting v0.1:

- Add `career-timeline-builder`, `competency-mapper`, `star-generator`, `signature-theme-miner`, `narrative-generator` — pure additive Skills that read existing bundle nodes and emit new ones.
- Add `role-analyzer` plus `fit-mapper` plus `role-overlay-builder` — the role/fit layer sits alongside the achievement/evidence layer.
- Add `technical-qa-generator`, `executive-qa-generator`, `question-generator`, `salary-strategy-generator` — these add the remaining spec sections.
- Add a `view-generator` Skill that slices the bundle into `out/packs/recruiter.md`, `out/packs/cto.md`, `out/packs/executive.md` — each view is a different walk of the same bundle.
- Add the LLM-as-judge eval suite as a separate workflow (`tests/eval/`), not part of CI.

The bundle schema is the contract; adding a Skill is a forward-compatible change because OKF consumers tolerate unknown `type` values and unknown frontmatter keys.

---

## 11. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Skills drift from OKF v0.2 conventions over time | Medium | Vendored `okf-spec/SPEC.md` is the source of truth; the lint pass checks required frontmatter keys. |
| LLM non-determinism makes golden snapshots brittle | Medium | Snapshots are structural only; prose drift is expected and accepted. We snapshot concept existence and frontmatter shape, not exact text. |
| Classification discipline becomes performative (markers without rigour) | Medium | Each Skill's `SKILL.md` includes worked examples of correct vs incorrect classification. Golden fixtures include a mix of all four marker types so reviewers see the difference. |
| `interview-strategy-generator` invents objections the user cannot back up | Medium | The strategy file links every claim to an evidence card; the assembler renders the link so the user can verify before the interview. `knowledge-gaps` flags strategy claims whose evidence is thin. |
| User overloads the orchestrator with too many Skills at once | Low | v0.1 is 7 Skills; the orchestrator list is short and linear. |
| OKF v0.3 breaks our producer assumptions | Low (now) → Medium (over time) | Vendor the spec; subscribe to the OKF repo for releases. The adapter boundary is the `okf-spec/` directory. |
| The user runs without a target opportunity | Low | The orchestrator blocks on missing target opportunity; this is a stop-and-ask trigger, not a silent skip. |
| Provenance becomes "claimed" rather than real | Medium | `sources[].resource` must be a real path or URL, not a placeholder. Lint pass checks for placeholder resources like `TBD`, `TODO`, or empty strings. |

---

## 12. Open questions (not blocking the spec)

These are real but not load-bearing for v0.1. Carried forward to v0.2 design time:

1. **Voice preservation at scale.** How do we keep the candidate's authentic voice across many Skills without per-Skill style drift? Possible answer: a `voice-fingerprint.md` reference at the bundle root, written by the user once.
2. **Multi-target support.** Today the config has one target opportunity. Should v0.2 support N target opportunities producing N interview strategies in the same bundle?
3. **Bundle version control.** Should the OKF bundle be committed to git (full provenance) or kept in `out/` (regenerable, ephemeral)? Current assumption: ephemeral, regenerable from inputs.
4. **Inter-Skill data passing via metadata.** Some Skills may benefit from a small metadata sidecar (e.g., "this achievement is central to the target opportunity"). v0.1 passes data via the bundle only; v0.2 may add a `.playbook-state.json` sidecar.
5. **Anti-pattern: a Skill that needs the full bundle.** v0.1's assembler walks everything; that is fine. But if a future Skill needs the full bundle and is expensive, it should cache a derived view, not re-walk. Pattern to design when needed.

---

## Appendix A — Worked example: an EvidenceCard node

This is what an `EvidenceCard` looks like in v0.1, modelled on the OKF v0.2 reference example at `bundles/acme_retail/metrics/revenue.md`.

```markdown
---
type: EvidenceCard
title: Migration of the X platform to Y
description: Two-year migration of the X platform to Y, completed on schedule with measured impact.
tags: [enterprise-architecture, migration, platform]
generated: { by: evidence-card-generator/claude-sonnet, at: 2026-07-29T14:00:00Z }
verified: []
status: draft
stale_after: 2026-09-30
sources:
  - id: cv-2024
    resource: inputs/cv.pdf
    title: CV (2024 edition)
    author: human:alexandre.franco
    last_modified: 2024-11-01
  - id: arch-doc-x-to-y
    resource: inputs/architecture/x-to-y.md
    title: Architecture document: X to Y migration
    author: human:alexandre.franco
    last_modified: 2024-08-12
---

# Situation

[evidence] The X platform was reaching end of life and the team needed a multi-year migration to Y to maintain service availability and reduce operational cost. [^arch-doc-x-to-y]

# Actions

[evidence] I led the architecture working group across three regions. [^cv-2024]
[inference] Coordinating across three regions required deliberate stakeholder management and a written decision log.
[evidence] I authored the migration architecture document and the cutover runbook. [^arch-doc-x-to-y]

# Results

[evidence] The migration completed on schedule. [^arch-doc-x-to-y]
[evidence] Post-migration operational cost was reduced by an unspecified amount. [^arch-doc-x-to-y]
[assumption] Operational cost reduction was approximately 30% (not stated explicitly in source).

# Lessons

[inference] Multi-region migrations succeed when the cutover plan is rehearsed end-to-end before the real window.
[recommendation] In the interview, lead with the cutover rehearsal, not the architecture diagram.

# Competencies demonstrated

- Enterprise architecture (v0.2 will link to a Competency node)
- Cross-region stakeholder management
- Technical writing and runbook discipline

# Possible interview questions

- Why Y, and not Z? (v0.2 will link to a Question node)
- What was the hardest part of the cutover?
- How did you handle regional variance in the migration plan?

# Supporting artefacts

- [CV (2024 edition)](../sources/cv.md) — source of the role and team context
- [Architecture document: X to Y migration](../sources/arch-doc-x-to-y.md) — primary source

# Confidence level

Medium — the outcome figures are `[assumption]`-flagged and require user verification.

# Trust and freshness

- Verified: not yet (unverified).
- Stale after 2026-09-30: re-verify the operational cost figure and any successor-platform plans before serving in an interview after that date.
```

## Appendix B — Glossary

- **OKF** — Open Knowledge Format, v0.2. The bundle format this project produces and consumes. Spec: `github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf`.
- **Bundle** — A directory of OKF `.md` files. The persistent artefact of this project.
- **Concept** — A single OKF document (one `.md` file) representing one node in the knowledge graph.
- **Skill** — A `SKILL.md` file the user invokes in Claude Code or Antigravity. The unit of work in this project.
- **Evidence** — A claim directly stated in a source, tagged `[evidence]`.
- **Inference** — A claim derived from evidence, tagged `[inference]`.
- **Recommendation** — A claim advising what the candidate should do, tagged `[recommendation]`.
- **Assumption** — A placeholder value not found in any source, tagged `[assumption]`.
- **Trust tier** — Per-concept classification: unverified, machine-confirmed, or human-reviewed (driven by OKF v0.2 `verified` list).
- **Golden snapshot** — A committed reference OKF subtree a Skill's output is diffed against in tests.
