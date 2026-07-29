# Architecture

High-level architecture of the Interview Playbook Generator. For the approved design spec, see [`docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`](docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md). This document is a navigable overview; the design spec is the contract.

## What this system is

A pipeline that turns raw candidate portfolio material (CV, LinkedIn export, slide decks, architecture docs, publications, JD, recruiter message) into a **structured knowledge graph** of the candidate's career, and from that graph produces a **human-readable Interview Playbook** tailored to a target opportunity.

The two outputs are different artefacts:

- **Knowledge graph** — an [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) bundle, a directory of cross-linked `.md` files. Machine-parseable, persists across runs, supports multiple downstream views.
- **Interview playbook** — a single Markdown document assembled by walking the graph. The primary user-facing artefact in v0.1.

The graph is the source of truth. The playbook is one view of it.

## System diagram

```
                 ┌────────────────────────────────────────┐
                 │  config/config.yaml                    │
                 │  • inputs (CV, LinkedIn, docs, …)      │
                 │  • target opportunity                  │
                 │  • output paths                        │
                 └────────────────┬───────────────────────┘
                                  │ reads
                                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │                    playbook-orchestrator                     │
   │       (drives the Skills, surfaces knowledge-gaps)            │
   └──────────────────────────────┬───────────────────────────────┘
                                  │ invokes in order
                                  ▼
   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
   │portfolio-      │─▶│portfolio-      │─▶│achievement-    │
   │ingestor        │  │analyzer        │  │extractor       │
   │                │  │                │  │                │
   │discovers &     │  │produces top-   │  │emits per-      │
   │classifies      │  │level analysis  │  │achievement     │
   │sources         │  │                │  │concepts        │
   └────────┬───────┘  └────────┬───────┘  └────────┬───────┘
            │                   │                   │
            ▼                   ▼                   ▼
   ┌──────────────────────────────────────────────────────────┐
   │                  OKF v0.2 bundle (on disk)               │
   │                                                          │
   │   okf/                                                   │
   │   ├── index.md             # okf_version: "0.2"          │
   │   ├── sources/             # SourceIndex + Source nodes  │
   │   │   ├── index.md                                       │
   │   │   ├── cv.md                                          │
   │   │   └── …                                              │
   │   ├── portfolio.md         # PortfolioAnalysis           │
   │   ├── achievements/        # Achievement nodes           │
   │   │   ├── index.md                                       │
   │   │   └── <slug>.md                                      │
   │   ├── evidence/            # EvidenceCard nodes          │
   │   ├── interview-strategy.md                               │
   │   └── knowledge-gaps.md    # KnowledgeGap report          │
   │                                                          │
   └──────────────────────────────────────────────────────────┘
                                  ▲
   ┌──────────────────────────────────────────────────────────┐
   │                       Skills 4–8                         │
   │  evidence-card-generator                                 │
   │  interview-strategy-generator                            │
   │  knowledge-gaps        ◀── pre-assembly gate             │
   │  playbook-assembler    ──▶ out/playbook.md + packs/     │
   └──────────────────────────────────────────────────────────┘
```

## Component responsibilities

| Component | Reads | Writes | Purpose |
|---|---|---|---|
| `playbook-orchestrator` | YAML config | (drives) | Walks the user through the pipeline; resolves missing config interactively; surfaces `knowledge-gaps` report. |
| `portfolio-ingestor` | raw portfolio files | `okf/sources/*` | Discovers and classifies every portfolio artefact. Does not analyse content. |
| `portfolio-analyzer` | `okf/sources/*` | `okf/portfolio.md` | Top-level coverage map, themes-at-a-glance (inference-flagged), provenance summary. |
| `achievement-extractor` | `okf/sources/*` | `okf/achievements/*` | Extracts one `Achievement` concept per claim, evidence-grounded. |
| `evidence-card-generator` | `okf/achievements/*` | `okf/evidence/*` | Reusable STAR cards (Situation, Actions, Results, Lessons, Competencies, Tags, Possible Questions, Sources, Confidence). |
| `interview-strategy-generator` | `okf/evidence/*`, target opportunity | `okf/interview-strategy.md` | Top differentiators, narrative, strongest cards, objections + mitigations, priorities. |
| `knowledge-gaps` | whole bundle | `okf/knowledge-gaps.md` | Pre-assembly gate. Severity-bucketed (critical / moderate / minor). Marks affected concepts `status: draft`. Does not block unless config says so. |
| `playbook-assembler` | whole bundle | `out/playbook.md` | Walks the graph, composes the human-readable playbook. Section-by-section. |

Each Skill is independent — there is no shared in-memory state, no service mesh, no message queue. State between Skills is *only* the bundle on disk.

## Data flow

The bundle is the spine. Every Skill is a read → transform → write operation against it:

```
raw portfolio  ──┐
                  │
config           ──┼──▶  portfolio-ingestor  ──┐
                  │                            │
                  └──▶  portfolio-analyzer  ──┤
                                               ▼
                                      okf/sources/, okf/portfolio.md
                                               │
                                               ▼
                                achievement-extractor
                                               │
                                               ▼
                                    okf/achievements/
                                               │
                                               ▼
                                evidence-card-generator
                                               │
                                               ▼
                                       okf/evidence/
                                               │
                                               ▼
                            interview-strategy-generator
                                               │
                                               ▼
                                    okf/interview-strategy.md
                                               │
                                               ▼
                                       knowledge-gaps
                                       (pre-assembly gate)
                                               │
                                               ▼
                                      okf/knowledge-gaps.md
                                               │
                                               ▼
                                       playbook-assembler
                                               │
                                               ▼
                                          out/playbook.md
```

Two properties of this flow:

1. **Idempotent.** Each Skill overwrites its own output subtree. Re-running a Skill with the same input set produces the same output set. The Skills never mutate each other's outputs.
2. **Inspectable.** At any point, the user can read the bundle directly — every node, every edge, every classification.

## OKF as the substrate

We chose OKF v0.2 as the knowledge-graph format for three reasons:

- **It is markdown.** Authorable, diffable, version-controllable. No binary blobs, no schema migrations just to inspect a concept.
- **It tolerates change.** OKF consumers must reject nothing for unknown `type` values or unknown frontmatter keys (SPEC §11). We can add Skills and new concept types in v0.2 without breaking v0.1 bundles.
- **It is shared.** The same bundle can be consumed by other tools — including the candidate's other experiments (CAS, Ideas-to-Life, Publishing Workflow) when they also adopt OKF. No custom interop glue required.

The schema we use builds on OKF v0.2's open `type` vocabulary. We add project-specific concept types (`Source`, `Achievement`, `EvidenceCard`, `InterviewStrategy`, `KnowledgeGap`, …) and a per-statement classification discipline inside concept bodies.

See `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md` §5 for the full schema.

## Trust and provenance

Every concept in the bundle is classified along two axes:

**Trust tier** (per OKF v0.2 §5.3):

- *Unverified* — no `verified` key in frontmatter. Default for new concepts.
- *Machine-confirmed* — `verified` contains only non-`human:` actors.
- *Human-reviewed* — `verified` contains at least one `human:<id>` entry.

**Statement classification** (project-specific, in body):

- `[evidence]` — directly stated in a source; accompanied by a footnote attribution.
- `[inference]` — derived from evidence; reasoning stated.
- `[recommendation]` — advice for the candidate; grounded in evidence or inference.
- `[assumption]` — a value the Skill needed but did not find in any source.

These classifications are the single most important behavioural rule. The Skills MUST classify every non-empty non-heading line in every concept body. An lint pass enforces this before any concept is written.

## What we explicitly do NOT do

The v0.1 thin slice is 8 Skills end-to-end. The following are deferred to v0.2 or later and are *not* part of this architecture:

- **Competency ontology / catalogue.** v0.2 adds freeform tags only.
- **View generator** for stage-specific packs (Recruiter / CTO / Executive). v0.1 produces one playbook.
- **Career narrative evolution** (multiple versions of "your story").
- **Mock interviews / conversation simulator.**
- **LLM-as-judge evaluation** for prose quality.
- **External research** (company, market, salary).
- **Advanced OKF linting** (semantic consistency, circular links).

The guiding principle: every Skill added in v0.1 must directly improve the quality of the generated interview playbook for real interview preparation. Optimise for a working end-to-end interview pipeline, not a complete career intelligence platform.

## Extension points

Adding a new Skill in v0.2 follows a simple contract:

1. The Skill declares which OKF node `type`(s) it reads.
2. The Skill declares which OKF node `type`(s) it writes.
3. Every concept it writes passes the lint pass (classification, source attribution, OKF-valid frontmatter).
4. The Skill ships with a snapshot test against a golden fixture.
5. The Skill's `SKILL.md` references the NEVER_FABRICATE list and the stop-and-ask protocol.

Adding a new concept type is a forward-compatible change because OKF v0.2 consumers MUST tolerate unknown `type` values (SPEC §11).

## Directory conventions

Each Skill lives in `skills/<skill-name>/SKILL.md`. The directory may carry:

- `examples/` — worked examples the Skill can reference.
- `schema.md` — local documentation for the Skill's I/O contract (frontmatter keys, body structure).
- `fixtures/` — local test fixtures (the repo-wide fixture lives under `tests/fixtures/`).

`okf-spec/` is vendored (offline reference). Tests live under `tests/` and use plain `pytest` plus `filecmp.dircmp` for golden-subtree snapshot diffing. Outputs land in `out/` (gitignored).

## Further reading

- [`README.md`](README.md) — project overview, status, v0.1 thin slice.
- [`AGENTS.md`](AGENTS.md) — vendor-neutral instructions for any AI agent touching this repo.
- [`CLAUDE.md`](CLAUDE.md) — Claude Code-specific operating instructions.
- [`requirements-spec.md`](requirements-spec.md) — original product requirements (baseline).
- [`spec-refinements.md`](spec-refinements.md) — refinements applied to the baseline.
- [`docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`](docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md) — the approved design spec (the contract).
