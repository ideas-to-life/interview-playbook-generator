---
name: portfolio-ingestor
description: Scans candidate portfolio inputs and target opportunity, emitting OKF Source nodes and a SourceIndex.
---

# Portfolio Ingestor

## Overview

`portfolio-ingestor` walks the candidate portfolio input directory and target opportunity source, classifying each document (CV, architectural spec, JD, etc.) and registering it into the OKF knowledge graph.

## Hard Rules & Classification

```
NEVER FABRICATE:
- Projects, Metrics, Team sizes, Budgets, Technologies, Responsibilities, Tenure
```

Every statement written into `okf/sources/*.md` must adhere to:
- `[evidence]` — Directly present in source file, with `[^source-id]` footnote.
- `[inference]` — Derived source classification or metadata structure.
- `[recommendation]` — Advice on portfolio completeness.
- `[assumption]` — Explicit placeholder for unconfirmed parameters.

## Input & Output Contracts

- **Inputs**: Read paths declared in `candidate.portfolio_dir`, `candidate.canonical_record`, and `target_opportunity.source` in `config/config.yaml`.
- **Outputs**:
  - `okf/sources/index.md` (type: `SourceIndex`, `okf_version: "0.2"`)
  - `okf/sources/<slug>.md` (type: `Source`)
  - `okf/employment-records.yaml` (Authoritative Canonical Employment Records derived directly from `career-record.yaml`)
  - `okf/log.md` (append update entry)

## Execution Instructions

1. **Automated Ingestion Script**: Execute `python3 scripts/ingest_portfolio.py` to recursively scan `candidate.portfolio_dir` across all active subdirectories (`articles/`, `learnings/`, `architecture-philosophy/`, `experiments/`, `standard-operational-procedure/`, `portfolio/`, `resume-profile/`, `narratives/`, `about/`).
   - **Quarantine Exclusion**: Any `quarantine/` directory is strictly excluded from file discovery and cannot be ingested as evidence or sources.
2. **Canonical Career Record Loading**: Load the authoritative career record from `candidate.canonical_record` (e.g. `canonical/career-record.yaml`) using `scripts/canonical_loader.py`.
3. **Extract Employment Records**: Write `okf/employment-records.yaml` directly from the canonical career record (`career-record.yaml`). Legacy `Positions.csv` parsing is completely deprecated and removed to prevent unverified titles or employers from entering the knowledge graph.
4. **Create `Source` Concepts**: For each discovered non-quarantined file:
   - Extract title, author (default `human:alexandre.franco`), last_modified, and resource path.
   - Format concept frontmatter with `type: Source` and frontmatter `sources` list containing itself as `id`.
   - Write body with `[evidence]` line confirming file presence and `[inference]` classifying document type (e.g. ArticleSource, LearningLogSource, PhilosophySource, PracticeSource).
5. **Build `SourceIndex`**: Write `okf/sources/index.md` with:
   - Frontmatter `okf_version: "0.2"`, `type: SourceIndex`.
   - Markdown list of all discovered sources with relative links (`[Title](<slug>.md)`).
   - Coverage summary detailing document types discovered.
6. **Append Log**: Append ISO-8601 timestamped entry to `okf/log.md`.

