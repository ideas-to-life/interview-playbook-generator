# Implementation Plan: Mind Palace Portfolio Ingestion

## Overview

Implement recursive ingestion of all candidate portfolio sources from `candidate.portfolio_dir` into the OKF knowledge graph (`out/okf/sources/`), complete with automated category mapping, HTML stripping, metadata extraction, and unit test coverage.

## Phase 1: Test-Driven Unit Tests
- Create `tests/test_portfolio_ingestor.py` containing unit test cases to verify:
  - Recursive traversal across mock/temp directory structures containing `.md`, `.html`, and hidden `.git` files.
  - Slug generation and HTML tag stripping.
  - Output OKF v0.2 frontmatter format and `index.md` validity.

## Phase 2: Ingestion Driver Script (`scripts/ingest_portfolio.py`)
- Implement `scripts/ingest_portfolio.py` reading `config/config.yaml`.
- Walk `candidate.portfolio_dir` (`/Users/avfranco/GitHub/mind-palace/`).
- Classify files into `ArticleSource`, `LearningLogSource`, `PhilosophySource`, `PracticeSource`, `PortfolioNarrativeSource`, `PortfolioSource`.
- Write individual concept markdown nodes under `out/okf/sources/<slug>.md`.
- Generate master index at `out/okf/sources/index.md`.

## Phase 3: Verification & Test Execution
- Run `pytest tests/test_portfolio_ingestor.py` to confirm all ingestion tests pass.
- Execute `python3 scripts/ingest_portfolio.py` to populate `out/okf/sources/`.
- Run full pytest test suite (`pytest`) to guarantee zero regressions across the codebase.

## Task Breakdown

- [x] Task 1: Create Spec `docs/superpowers/specs/2026-08-14-mind-palace-portfolio-ingestion-spec.md`
- [x] Task 2: Create Implementation Plan `docs/superpowers/plans/2026-08-14-mind-palace-portfolio-ingestion-plan.md`
- [ ] Task 3: Create Unit Test Suite `tests/test_portfolio_ingestor.py`
- [ ] Task 4: Finalize Ingestion Script `scripts/ingest_portfolio.py`
- [ ] Task 5: Run Pytest Suite & Verify Ingested OKF Sources
