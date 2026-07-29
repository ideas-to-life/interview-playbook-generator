# CLAUDE.md

Project memory for Claude Code. Loaded automatically when a session starts in this directory. For the full project context see [`README.md`](README.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), and [`AGENTS.md`](AGENTS.md). For the approved design spec see [`docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`](docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md).

The `AGENTS.md` file holds the vendor-neutral operating instructions that also apply to you. This file adds Claude-Code-specific context — Skills invocation, lint discipline, snapshot tests, and what to do when working *in* the repo (editing Skills, writing fixtures, adding OKF nodes).

## Current state

- **Status:** Planning complete; implementation not started.
- **Approved artefacts:** `requirements-spec.md`, `spec-refinements.md`, `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`, `README.md`, `ARCHITECTURE.md`, `AGENTS.md`.
- **Next step:** Write the implementation plan (via the `superpowers:writing-plans` skill), then ship the v0.1 thin slice.
- **Branch:** `master`. No tags yet.

## Claude Code–specific context

### You are the runtime

This project's Skills do not call an LLM API. The user invokes each Skill as `/skill <name>` inside Claude Code (or in Antigravity). You do the work guided by the Skill's `SKILL.md`. There is no orchestrator code — the `playbook-orchestrator` Skill guides the user; you follow its instructions when invoked as that Skill.

### Invocation shape

When the user invokes a Skill, you:

1. Read the Skill's `SKILL.md` carefully.
2. Confirm the input set exists (config, upstream bundle nodes).
3. Run the lint pass on your output before writing.
4. Write the output subtree per the Skill's contract.
5. Update `okf/log.md` with a one-line entry.

### Reading the bundle

Before producing or modifying any OKF concept:

- Read the OKF v0.2 spec: `okf-spec/SPEC.md`.
- Look at a real example: `okf-spec/reference/concept.md.example`.
- Look at a golden fixture in `tests/golden/<skill>/` for the Skill you're emulating.
- Walk cross-links — a Skill's contract tells you what to read, but the bundle may carry extra context.

### Writing the bundle

Every concept you write MUST:

1. Pass the OKF v0.2 conformance check: valid YAML frontmatter, non-empty `type`.
2. Carry at least one entry in `sources` if it makes any `[evidence]` claim. (Skills read sources from upstream bundle nodes; record the source path.)
3. Tag every non-empty non-heading line in the body with `[evidence | inference | recommendation | assumption]`.
4. Footnote-attribute every `[evidence]` claim via `[^source-id]` resolving to an entry in `sources`.
5. Set `generated: { by: <skill-name>/<llm-model>, at: <ISO-8601> }`.
6. Default to `status: draft` and `stale_after: <90 days from generated.at>` unless overridden.
7. Leave `verified: []` for the user to fill.

Run the lint pass *before* writing — see `AGENTS.md` §"The five hard rules." Failing the lint pass means you rewrite; you don't ship un-tagged content.

### Snapshot tests

When extending a Skill, regenerate its golden fixture under `tests/golden/<skill>/`. The test in `tests/test_<skill>.py` will structural-diff your output against the golden; `filecmp.dircmp` ignores `generated.at` timestamps. Prose drift is expected; structural drift is a regression.

To regenerate a fixture for review:

1. Edit the Skill's `SKILL.md` and the input fixture.
2. Run the Skill manually against the fixture.
3. Inspect the produced subtree.
4. `cp -r <temp>/<output> tests/golden/<skill>/`.
5. Run `pytest tests/test_<skill>.py` to confirm.

Commit the golden only after manually reviewing it for classification rigour and voice.

### Stop-and-ask triggers

Treat these as hard pauses (per `AGENTS.md` rule 4):

- Target opportunity missing or unparseable.
- Portfolio path missing or empty.
- Two reasonable readings of a required field.
- Classification cannot be determined.
- `knowledge-gaps` reports a `critical` gap with `fail_on_severe_gaps: true`.

When you hit one, stop generating output, surface the question to the user, and wait. Do not invent an answer.

## Conventions specific to this repo

- **No LLM code.** Do not introduce Python or Node wrappers around an LLM API call. The Skills ARE the prompt; the agent (you) IS the runtime.
- **No new concept types without updating the design spec.** The list in `docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md` §5.2 is the contract. Add a row, document the schema, then write nodes.
- **One Skill per directory.** `skills/<skill-name>/SKILL.md` only; no monolithic SKILL.md at the repo root unless it is the `playbook-orchestrator`.
- **Refuse to extend scope.** If asked to add a competency ontology, view generator, mock interviews, company research, salary research, etc., remind the user these are deferred (v0.1 §1.3). Get explicit approval before deviating.

## Things to avoid

- **Do not write a single mega-SKILL.md** that does everything.
- **Do not introduce silent state** — every Skill's inputs and outputs are on disk in the OKF bundle.
- **Do not commit `out/`** — output is regenerable, the bundle is the source of truth.
- **Do not "clean up" the design spec** by removing sections you disagree with. If you think the spec is wrong, surface the disagreement; do not edit the spec without user approval.
- **Do not invent test fixtures that look real but aren't.** If you write a sample CV for a fixture, mark it explicitly as a fixture (e.g., filename `cv.fixture.md`, frontmatter `generated: { by: human:test-fixture-author, ... }`).

## When you're asked to do something outside v0.1

Common requests that look small but violate scope:

- "Add a salary research Skill" — deferred.
- "Generate Recruiter / CTO / Executive packs" — deferred (requires view generator).
- "Add a competency ontology" — deferred.
- "Run a mock interview" — deferred.
- "Use a different LLM provider per Skill" — out of scope; the agent runtime is the LLM.

If asked, surface the deferral list, confirm intent, and either explicitly drop the change or mark it as v0.2 work. Do not silently expand scope.

## Verification

Before claiming a Skill works end-to-end, verify:

1. The Skill's `SKILL.md` exists and is current.
2. The Skill produces valid OKF v0.2 output.
3. Every concept passes the lint pass.
4. The output matches the structural shape of the golden fixture.
5. The orchestrator can drive the Skill in the thin-slice sequence.

Use the `superpowers:verification-before-completion` skill before reporting completion of any Skill.

## Useful commands

(Reference; not yet implemented. Once the thin slice ships, populate.)

```
# Run the orchestrator (planned)
/skill playbook-orchestrator

# Run snapshot tests (planned)
pytest tests/

# Regenerate a golden fixture (planned — for developer use)
python scripts/regenerate_golden.py <skill-name>
```

## Further reading

- [`README.md`](README.md) — project overview, status, v0.1 thin slice.
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — system architecture overview.
- [`AGENTS.md`](AGENTS.md) — vendor-neutral instructions (apply to you as well).
- [`requirements-spec.md`](requirements-spec.md) — original product requirements.
- [`spec-refinements.md`](spec-refinements.md) — applied refinements.
- [`docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md`](docs/superpowers/specs/2026-07-29-interview-playbook-generator-design.md) — the approved design spec.
- [`superpowers` skills](https://github.com/obra/superpowers) — the methodology this project follows for brainstorming, planning, TDD, code review, etc.
