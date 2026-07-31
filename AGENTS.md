# AGENTS.md

Operating instructions for any AI agent (Claude Code, Antigravity, GitHub Copilot, Cursor, Jules, Codex CLI, Aider, Zed, etc.) working in this repository. This file is vendor-neutral; for Claude-Code-specific notes see [`CLAUDE.md`](CLAUDE.md). For architecture see [`ARCHITECTURE.md`](ARCHITECTURE.md). For the approved design spec see [`docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`](docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md).

## What this project is

The Interview Playbook Generator turns a candidate's portfolio (CV, LinkedIn, slide decks, architecture docs, publications) and a target opportunity (JD / recruiter message / role summary) into a structured OKF v0.2 knowledge graph and a tailored Interview Playbook. The pipeline runs as a sequence of Skills — each Skill is a `SKILL.md` file the user invokes; state passes between Skills as the OKF bundle on disk. There is no LLM code to run; the agent (you) *is* the runtime.

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

Every Skill's input set determines its output set. Re-running a Skill overwrites its own output; it does not append and does not touch other Skills' outputs. The `generated.at` timestamp updates on every write; `verified` is preserved if the body is unchanged.

## How the pipeline runs

```
KNOWLEDGE LAYER (canonical; writes to okf/)
  portfolio-ingestor
  portfolio-analyzer
  achievement-extractor
  evidence-card-generator        ← extended (new fields + dup detection)
  behaviour-profile-generator    ← new (canonical)
  capability-extractor            ← new (canonical)
  signature-achievements-curator  ← new (canonical)
  signature-theme-miner
  narrative-generator

COACHING LAYER (derived; reads canonical + target opportunity)
  interview-strategy-generator   ← extended (Opportunity Analysis + Story→Question mapping)
  knowledge-gaps

PROJECTION LAYER (views; reads canonical + coaching + target opportunity; writes to out/)
  playbook-assembler
  opportunity-alignment-view      ← new view Skill
  executive-brief-view           ← new view Skill
```

The user invokes each Skill manually inside Claude Code (or Antigravity). The orchestrator tells them which to invoke next. There is no code-driven orchestration in v0.1.

For an end-to-end run on the example portfolio, the user runs:

```
/skill playbook-orchestrator
```

then follows the prompts. Each subsequent Skill is invoked the same way.

## Conventions

### OKF v0.2 compliance

Every concept document follows [`GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). The minimum required frontmatter is `type` (non-empty string). Producers MAY include any additional keys; consumers MUST tolerate unknown keys. We use this latitude heavily.

Reserved filenames: `index.md` (directory listing, no frontmatter except `okf_version` at bundle root) and `log.md` (update history, ISO-8601 date headings, newest first).

### Project concept types

The project extends OKF's open `type` vocabulary. v0.3 types: `Source`, `SourceIndex`, `PortfolioAnalysis`, `Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `InterviewStrategy`, `KnowledgeGap`. See the v0.3 design spec §5.3 for field additions on `EvidenceCard`.

### File layout

- `skills/<name>/SKILL.md` — the Skill's instructions. May carry `examples/` and `schema.md`.
- `config/config.example.yaml` — the YAML config template.
- `okf-spec/` — vendored copy of OKF SPEC.md (offline reference).
- `tests/fixtures/`, `tests/golden/` — fixtures and golden OKF subtrees.
- `out/` — gitignored output directory.

### Git

- Branch: `master`.
- Conventional commits encouraged (`docs:`, `feat:`, `fix:`, `test:`, `chore:`). Not enforced.
- Do not commit `out/` or any OKF bundle. Output is regenerable.

## Testing

Three layers, all CI-friendly:

1. **Snapshot per Skill.** Run the Skill against a fixture, diff the output subtree against `tests/golden/<skill>/` using `filecmp.dircmp`. Structural only — `generated.at` timestamps are stripped before comparison.
2. **End-to-end thin slice.** Run the full 8-Skill pipeline on the example portfolio and diff the resulting bundle + playbook.
3. **Lint pass.** Every concept must pass classification + source attribution checks.

LLM-as-judge eval is **not** part of v0.1; quality is enforced by lint + human review of golden fixtures.

## Out of scope for v0.1 (do NOT add)

The following are explicitly deferred. Adding them in v0.1 violates the spec's guiding principle.

- Competency ontology / catalogue
- View generator (stage-specific packs)
- Career narrative evolution
- Mock interviews / conversation simulator
- LLM-as-judge evaluation
- Company research / salary research / market intelligence
- Advanced OKF linting

If a task seems to require one of these, surface it as a "deferred — should this be v0.2?" question to the user; do not implement it silently.

## What to do if you're stuck

1. Re-read the Skill's `SKILL.md`. The contract is documented there.
2. Re-read the design spec — especially §6 (Skills) and §7 (error handling).
3. Read a real OKF v0.2 example in `okf-spec/reference/`.
4. Look at a golden fixture under `tests/golden/`.
5. If still stuck, ask the user.

## Doing the right thing

This system exists because generating interview prep without grounding produces confidently wrong output. Refusing to invent, classifying every claim, attributing every source, stopping when uncertain — these are not bureaucracy, they are the product. The system is only useful if a candidate trusts it enough to use it in a real interview.
