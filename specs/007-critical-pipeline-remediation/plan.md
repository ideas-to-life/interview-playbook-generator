# Implementation Plan: Critical Pipeline Remediation & Failing Test Resolution

**Branch**: `007-critical-pipeline-remediation` | **Date**: 2026-11-23 | **Spec**: [specs/007-critical-pipeline-remediation/spec.md](spec.md)

## Governance & Pattern Alignment (Path A — Governed Reuse)

This remediation follows **Path A (Governed Reuse)** using ratified patterns from `.cas/patterns/patterns-catalogue.yaml`:
- `contract-first-architecture` & `schema-enforced-domain-contracts`: Align `src/scripts/projection_validator.py` output schema strictly to `specs/006-projection-data-integrity/contracts/projection-validation-report-contract.yaml`.
- `rule-grounded-compliance-evaluation` & `pure-functional-health-evaluation`: Enforce deterministic validation rules across `projection_validator.py`, `upwork_validator.py`, `canonical_loader.py`, and `canonical_selector.py` without fabricated defaults or lost audit alerts.
- `deterministic-core-selective-augmentation`: Guarantee safe serialization (`yaml.safe_dump`, `xml.sax.saxutils.escape`), slug validation, fail-fast boundary checks, and hermetic tests.

## Files that change

- `specs/007-critical-pipeline-remediation/intent.md` — Accepted remediation intent with verified `[A]` citations.
- `specs/007-critical-pipeline-remediation/spec.md` — Functional requirements `FR-001` through `FR-007`.
- `specs/007-critical-pipeline-remediation/plan.md` — This implementation plan.
- `src/scripts/__init__.py` — Relocated package init under `src/scripts/`.
- `src/scripts/canonical_loader.py` — Null-safe YAML parsing, extract certification year from `issue_date` without fabrication, remove default `"London, UK"` location and candidate-specific overrides (`compugraf`/`wpp`), derive consultancy `client` generically, and align `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/canonical_models.py` — Relocated canonical data models under `src/scripts/`.
- `src/scripts/canonical_selector.py` — Remove fabricated defaults (`1988`, `2021`, hardcoded languages/proficiencies), validate `target_slug`, fix `_text_contains_term` boundary matching for `C++`/`.NET`, preload OKF corpus once in `partition_ats_vocabulary`, and align `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/canonical_validator.py` — Relocated under `src/scripts/` with `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/deploy_skills.py` — Copy-based skill deployer (`local` / `global` scope, frontmatter validation, manifest-scoped pruning, and `--clean-global`).
- `src/scripts/employment_validator.py` — Relocated under `src/scripts/` with `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/generate_architecture_diagrams.py` — Escape XML attributes (`<target-slug>`), update `v0.6` skill layer mappings, fix geometry width expression, resolve `REPO_ROOT` (`parent.parent.parent`), support `--output-dir`.
- `src/scripts/generate_upwork_biz_systems_playbook.py` — Relocated under `src/scripts/` with `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/generate_upwork_ea_ai_solution_consultants_playbook.py` — Relocated under `src/scripts/` with `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/generate_upwork_fractional_ai_playbook.py` — Relocated under `src/scripts/` with `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/generate_upwork_playbook.py` — Relocated under `src/scripts/` with `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/generate_upwork_system_architect_adviser_playbook.py` — Relocated under `src/scripts/` with `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/ingest_portfolio.py` — Add `format_okf_frontmatter()` using `yaml.safe_dump`, add `.txt` extraction, tag summary prose with `[evidence]`, emit dynamic UTC timestamps, prune stale source files, fail fast on missing inputs, replace `yaml.dump` with `yaml.safe_dump`, and align `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/projection_validator.py` — Preserve Stage 1 sanitization findings, emit the 6 contract check keys including `cross_opportunity_isolation`, enforce dynamic `opportunity_analysis` unsupported tools, tighten transferable indicators, precision-fix education date sanitization, validate `target_slug`, support `out_root` injection, fail on empty target dir, record YAML warnings, and align `REPO_ROOT` (`parent.parent.parent`).
- `src/scripts/upwork_validator.py` — Add candidate-agnostic CLI (`main()`, `validate_upwork_directory()`), extend clean-prose checks to `screening_md` and `work_samples_md`, scope Q2/Q4 checks to their sections, remove dead regex/imports, and align `REPO_ROOT` (`parent.parent.parent`).
- `src/skills/__init__.py` — Copied skill package init under `src/skills/`.
- `src/skills/projection-validator/__init__.py` — Copied skill package init under `src/skills/projection-validator/`.
- `src/skills/projection-validator/employment_validator.py` — Copied skill validator module under `src/skills/projection-validator/`.
- `.github/workflows/architecture-diagrams.yml` — Update diagram generator script and `src/skills/**` trigger paths.
- `.gitignore` — Ignore locally deployed playbook skill directories and manifest under `.agents/skills/`.
- `docs/architecture/4-layer-pipeline.drawio.xml` — Regenerated valid Draw.io XML output.
- `tests/test_projection_validation_report_contract.py` — Add real validator contract & sanitization preservation tests.
- `tests/test_projection_validator.py` — Add bypass-closure, dynamic vocabulary, isolation, empty-dir, slug traversal, and date precision tests.
- `tests/test_canonical_loader.py` — Add certification year extraction, null-YAML safety, and non-fabrication tests.
- `tests/test_canonical_selection_contract.py` — Add zero-fabrication, slug validation, and symbol-term (`C++`/`.NET`) matching tests.
- `tests/test_upwork_validator_cli.py` — Add CLI exit-code, multi-file clean-prose, and scoped Q2/Q4 screening tests pointing to `src/scripts/upwork_validator.py`.
- `tests/test_upwork_proposal_generator.py` — Update `validator_path` and `skills/...` paths to `src/scripts/` and `src/skills/`.
- `tests/test_portfolio_ingestor.py` — Add YAML-injection safety, `.txt` ingestion, dynamic timestamp, tagged summary, stale-file pruning, and missing-dir fail-fast tests.
- `tests/test_architecture_diagram_generator.py` — Use `sys.executable` + `--output-dir tmp_path`, point to `src/scripts/generate_architecture_diagrams.py`, and enforce `xml.etree.ElementTree.parse` validation on `docs/architecture/4-layer-pipeline.drawio.xml`.
- `tests/test_deploy_skills.py` — Unit and CLI tests for `src/scripts/deploy_skills.py` (`discover_skills`, frontmatter validation, copy/prune behavior, `--dry-run`, `--clean-global`).
- `tests/test_behaviour_profile.py`, `tests/test_brand_validator.py`, `tests/test_capability_extractor.py`, `tests/test_cover_letter_projection.py`, `tests/test_executive_brief_view.py`, `tests/test_executive_identity.py`, `tests/test_forensic_remediation_regression.py`, `tests/test_linkedin_projection.py`, `tests/test_narrative_engine.py`, `tests/test_opportunity_alignment_view.py`, `tests/test_opportunity_analyzer.py`, `tests/test_projection_registry.py`, `tests/test_resume_projection.py`, `tests/test_signature_achievements_curator.py`, `tests/test_skills.py`, `tests/test_story_engine.py`, `tests/test_v04_success_criteria.py`, `tests/test_v05_success_criteria.py`, `tests/test_v06_success_criteria.py` — Update `skills/` path references to `src/skills/`.

## Order of work

1. Verify SDD intent and governance routing (`cas governance verify-intent`, `cas governance route-plan`).
2. **TDD Red**: Add/update all tests listed above while preserving every existing assertion; run `pytest` to confirm expected failures.
3. **TDD Green**: Implement fixes across `src/scripts/` and align `REPO_ROOT`, tests, and CI paths with the `src/` layout; regenerate `docs/architecture/4-layer-pipeline.drawio.xml`.
4. **Verify**: Run full `pytest`, XML validation, `cas governance verify-intent`, `cas governance route-plan`, `cas governance lint`, `cas governance verify-diff`, `cas governance review-pr`, and `cas governance watch --once`.

## Risks

- **Downstream test compatibility**: Removing candidate-specific aliases or extending `upwork_validator.py` clean-prose checks to `screening_md`/`work_samples_md` could reveal hidden assumptions in existing tests; verified against existing test files before editing.
- **Path depth shift (`src/scripts/`)**: Moving scripts one directory deeper changes `Path(__file__).resolve().parent.parent` from repo root to `src/`. All `REPO_ROOT` definitions in `src/scripts/*.py` must use `.parent.parent.parent`.

## Proof

```bash
.venv/bin/pytest tests/ -q
.venv/bin/python3 -c "import xml.etree.ElementTree as ET; ET.parse('docs/architecture/4-layer-pipeline.drawio.xml'); print('DRAWIO XML VALID')"
cas governance verify-intent --target-dir .
cas governance route-plan --target-dir .
cas governance lint --target-dir .
cas governance verify-diff --target-dir .
cas governance review-pr --target-dir .
cas governance watch --once
```
