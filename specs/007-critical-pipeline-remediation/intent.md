# Intent: Critical Pipeline Remediation & Failing Test Resolution

Branch: 007-critical-pipeline-remediation
Status: accepted
Type: fix
Governance Path: Path A (Governed Reuse)

## Problem Statement

A five-axis code review of the deterministic pipeline scripts, CI tests, and generated architecture diagrams identified five critical pipeline integrity/security defects and two failing automated tests, followed by relocating `scripts/` under `src/scripts/` and `skills/` under `src/skills/` to align with CAS repository structure:

1. **Silent loss of Stage 1 sanitization findings & report schema contract mismatch**:
   - [A] src/scripts/projection_validator.py:528 — `validate_opportunity_projections` must preserve Stage 1 sanitization findings and handle missing directories and YAML parse errors.
   - [A] src/scripts/projection_validator.py:322 — `validate_projection_content` must emit the 6 contract check keys including `cross_opportunity_isolation`.
   - [A] specs/006-projection-data-integrity/contracts/projection-validation-report-contract.yaml:49 — authoritative contract check keys.
   - [A] tests/test_projection_validation_report_contract.py:25 — contract tests must exercise `validate_projection_content` and `validate_opportunity_projections` directly.

2. **Technology claim validation bypass & incomplete validation scope**:
   - [A] src/scripts/projection_validator.py:85 — `_extract_unsupported_platforms` and `validate_projection_content` must incorporate `opportunity_analysis` and reject direct claims using generic words like `"ecosystem"` or `"pattern"`.
   - [A] src/scripts/projection_validator.py:111 — `sanitize_projection_content` education date sanitization must avoid double spaces and non-education date rewrites.

3. **Hardcoded factual defaults / fabrication in canonical loader & selector**:
   - [A] src/scripts/canonical_selector.py:203 — `select_canonical_facts` must not fabricate `start_year`, `year`, or language proficiencies, and must reject traversal slugs.
   - [A] src/scripts/canonical_loader.py:87 — `load_canonical_career_record` must extract certification years from `issue_date`, stay null-safe, and avoid candidate-specific overrides.
   - [A] src/scripts/canonical_selector.py:43 — `_text_contains_term` must match symbol terms like `C++` / `.NET` and `_load_okf_corpus` (`52`) preloads OKF corpus once.

4. **Missing CLI entry point & incomplete screening/prose checks in Upwork validator**:
   - [A] src/scripts/upwork_validator.py:87 — `validate_upwork_proposal` and `main` (`325`) must expose a candidate-agnostic CLI, scan `screening_md` and `work_samples_md` for internal tags, and scope Q2/Q4 checks to their sections.

5. **YAML frontmatter injection & pipeline rule gaps in portfolio ingestor**:
   - [A] src/scripts/ingest_portfolio.py:93 — `ingest_portfolio` and `format_okf_frontmatter` (`21`) must serialize YAML frontmatter with `yaml.safe_dump`, support `.txt`, tag summary prose with `[evidence]`, emit dynamic timestamps, prune stale sources, and fail fast on missing `portfolio_dir`.

6. **Two failing tests, malformed Draw.io XML, and `src/` layout alignment**:
   - [A] tests/test_architecture_diagram_generator.py:8 — `test_architecture_diagram_generator_script_runs` and `test_drawio_xml_file_exists_and_valid` (`24`) must invoke `sys.executable` against `src/scripts/generate_architecture_diagrams.py` with `--output-dir` and parse Draw.io XML via `xml.etree.ElementTree.parse`.
   - [A] src/scripts/generate_architecture_diagrams.py:235 — `build_pipeline_drawio_xml` must XML-escape attribute values (such as `<target-slug>`) in `docs/architecture/4-layer-pipeline.drawio.xml`, and `src/scripts/` modules must resolve `REPO_ROOT` to the repository root (`parent.parent.parent`).
   - [A] src/scripts/deploy_skills.py:113 — `deploy_skills` and `clean_global_deployments` must separate `src/skills/` from copy-deployed local `.agents/skills/` and clean global repo symlinks.

## Scope & Constraints

- Strictly reuse ratified CAS patterns (`contract-first-architecture`, `schema-enforced-domain-contracts`, `rule-grounded-compliance-evaluation`, `pure-functional-health-evaluation`, `deterministic-core-selective-augmentation`).
- Follow TDD: write failing tests before production edits and never weaken or delete existing test assertions.
- Maintain candidate agnosticism in `src/scripts/upwork_validator.py` and keep `src/scripts/canonical_loader.py` strictly read-only on `career-record.yaml`.
