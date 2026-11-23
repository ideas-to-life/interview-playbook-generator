# Operational Governance: copilot-instructions.md

> [!CAUTION]
> ### 🚨 CRITICAL ENFORCEMENT: MANDATORY SDD/TDD & CAS SKILLS WORKFLOW 🚨
> You MUST NOT write, modify, or refactor any production code (`src/**`) without FIRST executing:
> 1. **Git Branch Isolation:** Confirm the active branch matches feature branch naming conventions ('<NNN-feature-name>'); NEVER write or modify production code directly on 'main' or 'master'.
> 2. **SDD Artifact Resolution (`.cas/config.yaml`) & Zero-Hallucination Intent Triage**: Confirm or create the active Intent, Specification, and Implementation Plan (`Files that change`, `Order of work`, `Risks`, `Proof`) matching the repository's configured SDLC profile (`auto`, `speckit`, `anthropic-native`, `superpowers`, or `agent-skills`). Run `cas governance verify-intent --target-dir .` to ensure all `[A]` code evidence citations exist and no unresolved `[Q]` questions block `Status: accepted`.
> 3. **CAS Skills Alignment & Plan Routing**: Invoke the mandatory CAS Skill (`cas-add-or-modify-feature` or `cas-refactor-module` in `.cas/` / `.agents/skills/` / `.claude/skills/`), verify all proposed changes against `.cas/patterns/patterns-catalogue.yaml` (`invariants` and `anti_patterns`), and run `cas governance route-plan --target-dir .` to determine the governance path (Path A, B, or C).
> 4. **Proportionate Governance Routing (Path A / B / C)**:
>    - **Path A (Governed Reuse)**: Reuses ratified patterns from `.cas/patterns/patterns-catalogue.yaml` while satisfying all `invariants` and avoiding all `anti_patterns` → unlocked for autonomous TDD build.
>    - **Path B (Architectural Novelty)**: Introduces a net-new architectural pattern or cross-boundary dependency → draft a candidate ADR/proposal and pause for human Architect review.
>    - **Path C (Architectural Exception)**: Intentionally deviates from a rule or invariant → requires an explicit, time-bound exception record (`exc-*.yaml`) approved by an Architect.
> 5. **Test-Driven Development (TDD — Red-Green-Refactor)**: Write or update failing unit tests under `tests/` BEFORE modifying production code under `src/`. Never weaken or delete existing test assertions during bugfixes (`[bugfix]`).
> 6. **Fresh-Context Verification (`.cas/agents/verifier.md`)**: Run deterministic diff verification (`cas governance verify-diff --target-dir .`) and PR review check (`cas governance review-pr --target-dir .`), and invoke the isolated read-only Verifier subagent (`verifier.md`) before completing a task or PR.

## Core Mandates

1. **Specification-Driven Development (SDD & Two-Key Invariance)**: Every feature or structural change requires both a specification (`spec.md`) and plan (`plan.md`) resolved via `.cas/config.yaml`. Modifying code files not declared in the plan violates `PLAN-002`; adding code without updating the specification violates `SPEC-002`.
2. **Pattern Invariants & Anti-Patterns**: Every design and code diff must satisfy the `invariants` and avoid the `anti_patterns` codified in `.cas/patterns/patterns-catalogue.yaml` and `.cas/rules/architecture_rules.md`.
3. **Deterministic PreToolUse Guardrails**: Runtime hooks in `.cas/hooks/path-protection.sh` and `.cas/hooks/production-gate.sh` block unauthorized edits to protected governance/secret files, test-tampering on bugfix branches, and un-specified/unplanned production code edits.
4. **Independent Verification & PR Gate**: Self-auditing in the same context window is insufficient; diffs must pass `.cas/agents/verifier.md` and the 3-pass `REVIEW.md` contract (`Critical: 0 | High: 0`).

## Skill & Subagent Registry

- **`cas-add-or-modify-feature`**: Mandatory before adding features, extending functionality, or introducing integrations.
- **`cas-refactor-module`**: Mandatory before restructuring or decoupling existing modules while preserving behavior.
- **`cas-audit-agent-rules`**: Mandatory for auditing, deduplicating, and optimizing agent rules and instruction files.
- **`verifier` (`.cas/agents/verifier.md`)**: Read-only Fresh-Context Verifier subagent projected to `.agents/subagents/verifier.md` and `.claude/agents/verifier.md`.

## Verification

Run the following deterministic commands to verify compliance before completing any task or PR:

*(Note: 'cas' is the installed CLI in onboarded projects. If developing directly inside the CAS runner repository itself, invoke via 'uv run cas'.)*

```bash
# 1. Run unit and regression test suite
pytest

# 2. Run deterministic architecture & anti-pattern linter (ARCH-LINT-001..004)
cas governance lint --target-dir .

# 3. Run 3-pass diff/PR verification against active SDD profile and REVIEW.md
cas governance verify-diff --target-dir .
cas governance review-pr --target-dir .
cas governance watch

# 4. Run deterministic agent skill evaluations
cas skills eval
```

---
*This file is a governed CAS contract. Do not weaken or remove managed governance rules without an approved architectural decision.*
