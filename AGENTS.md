# AGENTS.md

Operating instructions for any AI agent (Claude Code, Antigravity, GitHub Copilot, Cursor, Jules, Codex CLI, Aider, Zed, etc.) working in this repository. This file is vendor-neutral; for Claude-Code-specific notes see [`CLAUDE.md`](CLAUDE.md). For architecture see [`ARCHITECTURE.md`](ARCHITECTURE.md). For approved design specs see [`docs/superpowers/specs/`](docs/superpowers/specs/).

## What this project is

The Career Projection Platform (Interview Playbook Generator v0.5) turns a candidate's portfolio (CV, LinkedIn, slide decks, architecture docs, publications) and a target opportunity (JD / recruiter message / role summary) into a structured OKF v0.2 knowledge graph and multiple tailored executive communication artefacts (Resumes, Cover Letters, LinkedIn Profiles, Playbooks, Briefings). The pipeline runs as a sequence of Skills — each Skill is a `SKILL.md` file the user invokes; state passes between Skills as the OKF bundle and execution context on disk. There is no LLM code to run; the agent (you) *is* the runtime.

## The five hard rules

These are non-negotiable. They are repeated in every Skill's `SKILL.md` and exist because violating any of them produces output that is worse than no output.

### 1. Never fabricate

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

If a value on this list is needed and you cannot find it in any source:

1. Search all sources again (it may be in a different document).
2. If still missing, write it as `[assumption]` with a clear marker the user can grep for.
3. Mark the containing concept `status: draft`.
4. Reference the missing value in `okf/knowledge-gaps.md` with a recommended portfolio improvement.

**Never** invent a plausible-sounding number. The whole system's value comes from its refusal to do this.

### 2. Classify every claim

Every non-empty non-heading line in every concept body MUST start with one of:

- `[evidence]` — directly stated in a source. Requires a `[^source-id]` footnote.
- `[inference]` — derived from one or more `[evidence]` lines. Reasoning stated in the same line or the next.
- `[recommendation]` — advice for the candidate. Grounded in an earlier `[evidence]` or `[inference]`.
- `[assumption]` — placeholder for a value not found in any source.

Untagged lines are rejected by the lint pass. Do not write them.

### 3. Attribute every claim to a source

In addition to classification, every claim should be attributable. Use the OKF v0.2 footnote form:

```markdown
[evidence] Led the migration of the X platform to Y. [^cv-2024]
```

The footnote label resolves to an entry in the concept's frontmatter `sources` list:

```yaml
sources:
  - id: cv-2024
    resource: inputs/cv.pdf
    title: CV (2024 edition)
    author: human:alexandre.franco
```

Without attribution, a claim is just prose.

### 4. Stop and ask rather than guess

Trigger the stop-and-ask protocol when:

- The target opportunity is missing or unparseable.
- The portfolio path is missing or empty.
- A required field has two reasonable readings.
- Classification cannot be determined.
- `knowledge-gaps` reports a `critical` gap AND config says `fail_on_severe_gaps: true`.

Surface the question to the user; do not invent an answer.

### 5. Idempotent re-runs

Every Skill's input set determines its output set. Re-running a Skill overwrites its own output directory cleanly. The `generated.at` timestamp updates on every write; `verified` is preserved if the body is unchanged.

## How the pipeline runs (v0.5)

```
KNOWLEDGE LAYER (canonical; writes to out/okf/)
  portfolio-ingestor
  portfolio-analyzer
  achievement-extractor
  evidence-card-generator        (Extended: 6 fields + dup detection)
  behaviour-profile-generator    (Canonical: okf/behaviour-profile.md)
  capability-extractor            (Canonical: okf/capabilities/)
  signature-achievements-curator  (Canonical: okf/signature-achievements.md)
  signature-theme-miner
  executive-identity-generator    (okf/executive-identity.md, voice-profile.md, positioning-statements.md)
  narrative-engine                (okf/narrative-library.md, messaging-library.md)
  story-engine                    (okf/story-library.md)

RUNTIME LAYER (derived execution context; writes to out/<target-slug>/runtime/)
  opportunity-analyzer            (out/<target-slug>/runtime/opportunity-analysis.yaml)

COACHING LAYER (derived; reads canonical + opportunity-analysis)
  interview-strategy-generator
  knowledge-gaps

PROJECTION LAYER (views; reads canonical + opportunity-analysis; writes to out/<target-slug>/)
  projection-registry             (Orchestrates registered projections into out/<target-slug>/)
  resume-projection               (out/<target-slug>/resume-executive.md, resume-ats.md, resume-recruiter.md)
  cover-letter-projection         (out/<target-slug>/cover-letter.md)
  linkedin-projection             (out/<target-slug>/linkedin-profile.md)
  opportunity-alignment-view      (out/<target-slug>/opportunity-alignment.md)
  executive-brief-view           (out/<target-slug>/executive-brief.md)
  playbook-assembler              (out/<target-slug>/playbook.md & out/<target-slug>/interview-cheatsheet.md)
  projection-validator            (out/<target-slug>/runtime/projection-validation-report.yaml)
  brand-validator                 (out/<target-slug>/runtime/brand-validation-report.yaml)
```

For an end-to-end run on the portfolio, the user runs:

```
/skill playbook-orchestrator
```

## Conventions

### OKF v0.2 compliance

Every concept document follows [`GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). The minimum required frontmatter is `type` (non-empty string). Reserved filenames: `index.md` and `log.md`.

### Project concept types

v0.5 types: `Source`, `SourceIndex`, `PortfolioAnalysis`, `Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `ExecutiveIdentity`, `VoiceProfile`, `PositioningStatements`, `NarrativeLibrary`, `StoryLibrary`, `MessagingLibrary`, `InterviewStrategy`, `KnowledgeGap`.

### File layout

- `skills/<name>/SKILL.md` — the Skill's instructions.
- `config/config.example.yaml` — the YAML config template.
- `out/` — gitignored output directory.
  - `out/okf/` — canonical OKF bundle (shared across target opportunities).
  - `out/<target-slug>/` — opportunity-scoped execution context & views (e.g. `out/senior-architect-vallum/`, `out/head-of-ai/`).

## Testing

1. **Snapshot per Skill.** Diff output against `tests/golden/<skill>/`.
2. **End-to-end criteria.** `tests/test_v05_success_criteria.py`.
3. **Lint pass.** Every concept passes classification & attribution checks.
