# AGENTS.md

Operating instructions for any AI agent (Claude Code, Antigravity, GitHub Copilot, Cursor, Jules, Codex CLI, Aider, Zed, etc.) working in this repository. This file is vendor-neutral; for Claude-Code-specific notes see [`CLAUDE.md`](CLAUDE.md). For architecture see [`ARCHITECTURE.md`](ARCHITECTURE.md). For approved design specs see [`docs/superpowers/specs/`](docs/superpowers/specs/).

## What this project is

The Career Projection Platform (Interview Playbook Generator v0.6) turns a candidate's portfolio (CV, LinkedIn, slide decks, architecture docs, publications, Mind Palace repository) and a target opportunity (JD / recruiter message / role summary) into a structured OKF v0.2 knowledge graph and multiple tailored executive communication artefacts (Resumes, Cover Letters, LinkedIn Profiles, Playbooks, Briefings). The pipeline runs as a sequence of Skills — each Skill is a `SKILL.md` file the user invokes; state passes between Skills as the OKF bundle and execution context on disk. There is no LLM code to run; the agent (you) *is* the runtime.

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

Every Skill's input set determines its output set. Re-running a Skill overwrites its own output directory cleanly. The `generated.at` timestamp updates on every write; `verified` is preserved if the body is unchanged. Agents executing a Skill MUST perform explicit disk write/touch operations on every run so that output files bear active modification timestamps. Reading existing files without executing disk writes is prohibited.

## Governing Principles

1. **Tailor expression, not identity**: Tailor the expression of the candidate to the opportunity, never the identity of the candidate to the opportunity.
2. **Evidence determining authority**: Evidence determines what Alexandre can credibly claim; canonical identity determines who Alexandre is; the target opportunity determines which of those truths should be emphasised.
3. **Identity Preservation Invariant**:
   `Projected Identity = Canonical Professional Identity + Target-Relevant Emphasis - Irrelevant Detail`
   Target-role tailoring may change the emphasis of the candidate's canonical identity, but must never redefine the candidate's canonical professional identity.
4. **Evidence relevance does not imply evidence equivalence**: A claim may only be generated at the level of ownership, scope, specificity, duration and seniority explicitly supported by its evidence.
5. **No inferred leadership from contribution**: When evidence supports contribution to a capability, the system must not infer leadership, ownership, establishment, or end-to-end responsibility for that capability.
6. **Project relevance aggressively, project responsibility conservatively**:
   Canonical identity determines who the candidate is $\rightarrow$ Evidence determines what the candidate has done $\rightarrow$ Claim-strength validation determines how strongly that experience may be stated $\rightarrow$ Target relevance determines what should be emphasised.
7. **Target requirements vs Candidate evidence**: Target requirements describe what the client needs; candidate evidence describes what the candidate has done. Target requirements must never become candidate evidence or candidate positioning unless independently supported by canonical evidence.
8. **Transferable framing over domain substitution**: When target requirements are adjacent to, but not directly evidenced by, candidate experience, the projection must use explicit transferable framing rather than domain substitution.
9. **Journey vs Destination Invariant**: The target defines the destination; the evidence defines the journey. Projection may explain why the candidate’s demonstrated experience makes the destination credible, but it must never rewrite the journey as though the candidate has already reached it.
10. **Career History Evidence Integrity Invariant**: Employer names, employment dates, job titles, status, and locations are immutable evidence. Projection may tailor presentation and accomplishment emphasis around those facts, but must never alter, infer, normalize, approximate, reconstruct, split, merge, or fabricate employment-history facts.

## How the pipeline runs (v0.6 Sprint 6)

```
KNOWLEDGE LAYER (canonical; writes to out/okf/)
 1. portfolio-ingestor             (Executes python3 scripts/ingest_portfolio.py over candidate.portfolio_dir)
 2. portfolio-analyzer
 3. achievement-extractor
 4. evidence-card-generator        (Extended: 6 fields + dup detection)
 5. behaviour-profile-generator    (okf/behaviour-profile.md)
 6. capability-extractor            (okf/capabilities/<slug>.md)
 7. signature-achievements-curator  (okf/signature-achievements.md)
 8. signature-theme-miner
 9. executive-identity-generator    (okf/executive-identity.md, voice-profile.md, positioning-statements.md)
10. narrative-engine                (okf/narrative-library.md, messaging-library.md)
11. story-engine                    (okf/story-library.md)

RUNTIME INTELLIGENCE LAYER (derived execution context; writes to out/<target-slug>/runtime/)
12. opportunity-analyzer            (out/<target-slug>/runtime/opportunity-analysis.yaml)
13. archetype-classifier            (out/<target-slug>/runtime/archetype-analysis.yaml)
14. gap-classifier                  (out/<target-slug>/runtime/gap-analysis.yaml)
15. archetype-fit-evaluator         (out/<target-slug>/runtime/opportunity-fit-report.yaml)
16. projection-strategy-generator   (out/<target-slug>/runtime/projection-strategy.yaml)

COACHING LAYER (derived; reads canonical + opportunity-analysis)
17. interview-strategy-generator
18. knowledge-gaps                  (Pre-assembly gate)

PROJECTION & VALIDATION LAYER (views & reports; writes to out/<target-slug>/)
19. projection-registry             (Orchestrates registered projections)
    ├── resume-projection           (out/<target-slug>/resume-executive.md, resume-ats.md, resume-recruiter.md)
    ├── cover-letter-projection     (out/<target-slug>/cover-letter.md)
    ├── linkedin-projection         (out/<target-slug>/linkedin-profile.md)
    ├── opportunity-alignment-view  (out/<target-slug>/opportunity-alignment.md)
    ├── executive-brief-view         (out/<target-slug>/executive-brief.md)
    └── playbook-assembler          (out/<target-slug>/playbook.md & out/<target-slug>/interview-cheatsheet.md)
20. projection-validator            (out/<target-slug>/runtime/projection-validation-report.yaml)
21. archetype-fit-validator        (out/<target-slug>/runtime/projection-validation-report.yaml overpositioning check)
22. brand-validator                 (out/<target-slug>/runtime/brand-validation-report.yaml)

EVALUATION LAYER (learning & feedback; writes to evaluation/opportunities/)
23. market-feedback-evaluator      (evaluation/opportunities/<target-slug>-evaluation.yaml)
```

For an end-to-end run on the portfolio, the user runs:

```
/skill playbook-orchestrator
```

## Conventions

### OKF v0.2 compliance

Every concept document follows [`GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). The minimum required frontmatter is `type` (non-empty string). Reserved filenames: `index.md` and `log.md`.

### Project concept types

v0.6 types: `Source`, `SourceIndex`, `PortfolioAnalysis`, `Achievement`, `EvidenceCard`, `Capability`, `SignatureAchievements`, `ExecutiveBehaviourProfile`, `ExecutiveIdentity`, `VoiceProfile`, `PositioningStatements`, `NarrativeLibrary`, `StoryLibrary`, `MessagingLibrary`, `InterviewStrategy`, `KnowledgeGap`.

### File layout

- `skills/<name>/SKILL.md` — the Skill's instructions.
- `scripts/ingest_portfolio.py` — Python portfolio ingestion script.
- `config/config.yaml` — active YAML config.
- `out/` — gitignored output directory.
  - `out/okf/` — canonical OKF bundle (shared across target opportunities).
  - `out/<target-slug>/` — opportunity-scoped execution context & views (e.g. `out/head-enterprise-architecture/`, `out/head-of-ai/`).
- `evaluation/opportunities/` — market feedback and prediction evaluations.

## Testing

1. **Snapshot per Skill.** Diff output against `tests/golden/<skill>/`.
2. **End-to-end criteria.** `tests/test_v06_success_criteria.py`.
3. **Lint pass.** Every concept passes classification & attribution checks.
