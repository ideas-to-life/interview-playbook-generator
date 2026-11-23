# Specification: Critical Pipeline Remediation & Failing Test Resolution

**Feature Branch**: `007-critical-pipeline-remediation`
**Created**: 2026-11-23
**Status**: Accepted

## Functional Requirements

### FR-001: Projection Validator Contract Conformance & Sanitization Finding Preservation
- `validate_projection_content` MUST emit the exact six check keys defined in `specs/006-projection-data-integrity/contracts/projection-validation-report-contract.yaml`: `education`, `certifications`, `languages`, `employment_chronology`, `technology_claims`, and `cross_opportunity_isolation`.
- `validate_opportunity_projections` MUST preserve Stage 1 (`sanitize_projection_content`) findings when `auto_sanitize=True` so `ProjectionValidationReport.findings`, `summary.sanitized_count`, `checks[*].status`, and `overall_status` (`PASSED_WITH_SANITIZATION`) accurately reflect in-place remediations.
- `cross_opportunity_isolation` MUST detect references to `out/<other-slug>/` (excluding `out/okf/` and `out/<target_slug>/`) as `FATAL` `isolation` findings.
- `validate_opportunity_projections` MUST validate `target_slug` against `^[A-Za-z0-9][A-Za-z0-9_-]*$`, include `upwork-work-samples.md` and `upwork-evidence-gaps.md`, record `WARNING` findings instead of swallowing YAML parse errors, and return `FAILED` (exit code `1`) if no projection files exist in the target directory.

### FR-002: Technology Claim Bypass Closure & Education Date Sanitization Precision
- `validate_projection_content` MUST derive `unsupported_platforms` from the baseline set (`Workday`, `NetSuite`, `Coupa`, `Concur`) unioned with `opportunity_analysis["ats_vocabulary"]["required_job_vocabulary"]` (excluding `candidate_evidenced_vocabulary`).
- `transferable_indicators` MUST NOT exempt direct implementation claims containing generic words such as `"ecosystem"` or `"pattern"`.
- `sanitize_projection_content` MUST NOT insert double spaces when rewriting education dates and MUST restrict bare `1995–1999` sanitization to education-context lines.

### FR-003: Zero-Fabrication Canonical Loading & Selection
- `canonical_loader.py` MUST validate non-dict/empty YAML cleanly, parse certification years from `issue_date` when `issue_year`/`year` are absent (returning `None` if no year exists), avoid defaulting missing role locations to `"London, UK"`, derive consultancy `client` generically from `engagement_type` (`contracted to <client>`), and avoid hardcoding candidate-specific employer overrides.
- `canonical_selector.py` MUST NOT fabricate `start_year: 1988`, `year: 2021`, or fallback language/proficiency values when absent from `CanonicalCareerRecord`.
- `canonical_selector.py` MUST validate `target_slug` against path traversal, match non-word-boundary terms (e.g., `C++`, `.NET`), and preload OKF capability/evidence files once per `partition_ats_vocabulary` invocation.

### FR-004: Upwork Validator CLI & Scoped Screening/Prose Checks
- `scripts/upwork_validator.py` MUST expose a candidate-agnostic `main()` CLI (`--target-dir`, positional slug, or auto-discovery under `out/`) returning exit code `0` on `PASS` and `1` on `FAIL` or invalid explicit target directory.
- Clean-prose checks MUST scan `proposal_md`, `screening_md`, and `work_samples_md` for leaked internal tags (`[evidence]`, `[inference]`, `[^source-id]`, `[OPEN CONDITION: ...]`).
- Question 2 and Question 4 screening checks MUST inspect only their respective question sections rather than the full `screening_md` text.

### FR-005: Safe YAML Serialization & Rule Compliance in Portfolio Ingestor
- `scripts/ingest_portfolio.py` MUST serialize all Markdown YAML frontmatter with `yaml.safe_dump()` via a dedicated helper and use `yaml.safe_dump()` for `employment-records.yaml`.
- `ingest_portfolio.py` MUST generate current UTC ISO timestamps in `index.md`, classify summary body lines under `[evidence] ... [^{slug}]`, handle `.txt` files, prune stale `.md` files in `out/okf/sources/`, and fail fast when `portfolio_dir` or `target_opportunity.source` is missing.

### FR-006: Valid Draw.io XML Generation & Hermetic Diagram Tests
- `src/scripts/generate_architecture_diagrams.py` MUST XML-escape attribute values (fixing unescaped `<target-slug>`), update skill/layer metadata to `v0.6`, resolve paths relative to `REPO_ROOT`, and support `--output-dir` for hermetic testing.
- `tests/test_architecture_diagram_generator.py` MUST execute the diagram generator via `sys.executable` against `tmp_path` and verify `docs/architecture/4-layer-pipeline.drawio.xml` parses cleanly with `xml.etree.ElementTree.parse`.

### FR-007: CAS `src/` Layout Alignment
- All modules under `src/scripts/` MUST resolve `REPO_ROOT` via `Path(__file__).resolve().parent.parent.parent` so config, `out/`, `docs/`, and `skills/` resolve to the repository root rather than `src/`.
- Tests and CI workflows referencing script file paths (`tests/test_architecture_diagram_generator.py`, `tests/test_upwork_validator_cli.py`, `tests/test_upwork_proposal_generator.py`, `.github/workflows/architecture-diagrams.yml`) MUST point to `src/scripts/`.

### FR-008: Copy-Based Skill Deployment & Global Cleanup
- `src/scripts/deploy_skills.py` MUST validate YAML frontmatter (`name`, `description`) in every `SKILL.md` under `src/skills/` before deploying.
- Deployment MUST copy skill trees (excluding `__pycache__`, `*.pyc`, `.DS_Store`) rather than creating symlinks, and MUST replace any pre-existing symlink of the same skill name.
- `deploy_skills` MUST record deployed skill names in `.interview-playbook-skills-manifest.json` and prune only previously managed skills without touching unrelated skills (`cas-*`, `speckit-*`, `aspire*`, or third-party global skills).
- `--clean-global` MUST remove `interview-playbook-generator` symlinks and manifest-tracked skills from global agent skill directories (`~/.agents/skills`, `~/.gemini/skills`, `~/.gemini/antigravity/skills`, `~/.gemini/antigravity-cli/skills`).
