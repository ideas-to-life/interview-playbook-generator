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

- **Inputs**: Read path declared in `inputs.portfolio` & `target_opportunity.source` in `config/config.yaml`.
- **Outputs**:
  - `okf/sources/index.md` (type: `SourceIndex`, `okf_version: "0.2"`)
  - `okf/sources/<slug>.md` (type: `Source`)
  - `okf/log.md` (append update entry)

## Execution Instructions

1. **Scan Files**: Enumerate all files in `inputs.portfolio` and the active target opportunity specified in `target_opportunity.source` of `config/config.yaml`. Remove any obsolete target opportunity source files in `okf/sources/` that do not match the active `target_opportunity.source`.
2. **Create `Source` Concepts**: For each discovered file:
   - Extract title, author (default `human:alexandre.franco`), last_modified, and resource path.
   - Format concept frontmatter with `type: Source` and frontmatter `sources` list containing itself as `id`.
   - Write body with `[evidence]` line confirming file presence and `[inference]` classifying document type (e.g. CV, architecture doc, job description).
3. **Build `SourceIndex`**: Write `okf/sources/index.md` with:
   - Frontmatter `okf_version: "0.2"`, `type: SourceIndex`.
   - Markdown list of all discovered sources with relative links (`[Title](<slug>.md)`).
   - Coverage summary detailing document types discovered.
4. **Append Log**: Append ISO-8601 timestamped entry to `okf/log.md`.
