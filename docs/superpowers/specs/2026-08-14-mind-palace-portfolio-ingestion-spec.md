# Spec: Full Recursive Portfolio Ingestion from `candidate.portfolio_dir`

## Objective

Build an automated, spec-compliant ingestion tool (`scripts/ingest_portfolio.py`) for `portfolio-ingestor` that recursively traverses all subdirectories and documents under `candidate.portfolio_dir` (`/Users/avfranco/GitHub/mind-palace/`), parses markdown (`.md`), HTML articles (`.html`), and PDF documents (`.pdf`), and emits OKF v0.2 `Source` concept nodes to `out/okf/sources/` and an updated `SourceIndex` at `out/okf/sources/index.md`.

## Assumptions
1. `candidate.portfolio_dir` in `config/config.yaml` is the single source of truth for the portfolio root (`/Users/avfranco/GitHub/mind-palace/`).
2. All subdirectories (`articles/`, `learnings/`, `architecture-philosophy/`, `experiments/`, `standard-operational-procedure/`, `portfolio/`, `resume-profile/`, `narratives/`, `about/`) should be processed.
3. System files (`.git`, `.DS_Store`, `CLAUDE.md`) are excluded.
4. Python 3 standard library (`re`, `html`, `pathlib`, `os`, `yaml`) will be used to ensure zero external binary dependency issues.

## Tech Stack
- **Language**: Python 3.13
- **Dependencies**: `pyyaml`, standard library (`re`, `html`, `pathlib`, `os`)
- **Testing**: `pytest`

## Commands
- **Ingest Portfolio**: `python3 scripts/ingest_portfolio.py`
- **Run Tests**: `pytest tests/test_portfolio_ingestor.py`
- **Run All Verification Tests**: `pytest`

## Project Structure
- `scripts/ingest_portfolio.py` — Portfolio ingestion script
- `skills/portfolio-ingestor/SKILL.md` — Ingestion skill instructions
- `tests/test_portfolio_ingestor.py` — Unit test suite for portfolio ingestion
- `out/okf/sources/` — Target directory for emitted `Source` nodes and `index.md`

## Code Style & Conventions
- Pure Python 3 functions with type hints.
- Frontmatter follows OKF v0.2 specification (`type: Source`, `id`, `title`, `resource`, `category`, `author`, `sources`).
- Claim classification in emitted source markdown: `[evidence]` for file discovery path, `[inference]` for category classification.

```python
def make_slug(rel_path: str) -> str:
    p = rel_path.replace('\\', '/').lower()
    p = re.sub(r'\.(md|html|pdf|txt)$', '', p)
    return re.sub(r'[^a-z0-9]+', '-', p).strip('-')
```

## Testing Strategy
- Unit test `test_portfolio_ingestor.py` verifying:
  1. Discovery of `.md` and `.html` files in nested subdirectories.
  2. Exclusion of hidden files (`.git`, `.DS_Store`).
  3. Proper OKF v0.2 frontmatter format in output `Source` files.
  4. Generation of `out/okf/sources/index.md` matching `okf_version: "0.2"`.

## Boundaries
- **Always do**: Preserve OKF v0.2 compliance, sanitize file slugs, filter hidden system files.
- **Ask first**: Deleting existing OKF knowledge graph nodes outside `sources/`.
- **Never do**: Fabricate source metadata, alter canonical employment dates, or commit non-reproducible paths.

## Success Criteria
1. Executing `python3 scripts/ingest_portfolio.py` successfully ingests all 20+ documents from `mind-palace` into `out/okf/sources/`.
2. `out/okf/sources/index.md` lists every ingested file with relative links and category classifications.
3. `pytest tests/test_portfolio_ingestor.py` passes cleanly.
4. All existing 107 pytest tests pass without regression.
