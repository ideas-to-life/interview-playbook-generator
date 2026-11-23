---
name: cas-add-or-modify-feature
description: MANDATORY skill for any feature request or structural modification. Use when adding features, extending functionality, modifying existing behaviour, or introducing integrations. This skill MUST be invoked before making any code changes to ensure architectural alignment, pattern reuse, and governance compliance.
---

# Skill: cas-add-or-modify-feature

## Intent
Introduce a new feature aligned with existing architecture, ensuring consistency with module boundaries, reuse of established patterns, enforcement of pattern `invariants` and `anti_patterns`, and prevention of architectural drift.

**When to use this skill:**
- User asks to "add a feature" or "extend the system"
- User wants to modify existing functionality that affects structure or behaviour
- User proposes a new integration or capability
- Any request that changes architecture, module boundaries, or system behaviour
- BEFORE implementing any feature or structural change, this skill MUST be invoked

**When NOT to use this skill:**
- Small bug fixes with no architectural impact
- Formatting, linting, or minor refactoring with no structural change
- Refactoring existing code without adding new features (use cas-refactor-module instead)

---

## Constraints (Prevent)

These constraints prevent architectural drift and maintain system integrity:

- **Module boundaries** - Align with existing module boundaries; no cross-layer imports
- **Pattern reuse** - Reuse existing patterns before introducing new structures
- **No duplication** - Don't duplicate existing logic or functionality
- **Separation of concerns** - Maintain clear layer separation
- **Traceability** - Document architectural impact and rationale
- **Provider abstraction** - External integrations (LLMs, APIs) require unified provider-agnostic abstractions (e.g., `LiteLLMClient` router + deterministic `MockLLMClient` double); vendor-specific SDK adapters are prohibited
- **MUST execute intent verification** - Run `uv run cas governance verify-intent --target-dir .` to verify all `[A]` citations on disk and confirm no unresolved `[Q]` questions block implementation
- **MUST execute plan governance routing** - Run `uv run cas governance route-plan --target-dir .` before code modification:
  - **Path A (Governed Reuse)**: Auto-mode execution permitted.
  - **Path B (Architectural Novelty)**: Auto-mode halted; candidate ADR scaffolded for Architect / ARB review.
  - **Path C (Architectural Exception)**: Auto-mode permitted only with a valid, approved `exc-*.yaml` exception record.
- **MUST explicitly reference** at least one pattern from `.cas/patterns/patterns-catalogue.yaml`
- **MUST validate** that all proposed `code_changes` satisfy every selected pattern's `invariants` and do NOT match any of its `anti_patterns` in `.cas/patterns/patterns-catalogue.yaml`
- **MUST justify** the chosen architectural structure using patterns and their `invariants`
- **MUST NOT include** meta-commentary outside the defined output schema
- **MUST produce exactly one** output block conforming to OUTPUT.schema.yaml
- **MUST include** a `decision` block in every output
- **MUST set** `decision.status` to one of: `accepted` | `rejected` | `proposed`
- **MUST set** `decision.status: rejected` if the proposed design violates `.cas/rules/architecture_rules.md`, violates any selected pattern's `invariants`, or matches any pattern's `anti_patterns`

**Reference files:**
- `.cas/rules/architecture_rules.md` - Core architecture constraints
- `.cas/patterns/patterns-catalogue.yaml` - Reusable patterns with mandatory `invariants` and `anti_patterns`
- `knowledge/projects/<project>/exceptions/` - Architecture exception records (`exc-*.yaml`)
- `knowledge/projects/<project>/adrs/` - Architecture Decision Records

---

## Instructions

Follow this sequence to add a feature while preserving architectural integrity:

### 1. Understand the Request & Verify Intent
- Read the feature request and identify its purpose
- Ask clarifying questions if the scope is ambiguous
- Identify the target module (user may specify, or infer from system structure)
- Execute `uv run cas governance verify-intent --target-dir .` to ensure all `[A]` anchors resolve, line numbers are in bounds, heuristic presumptions `[P]` are noted, and no open questions `[Q]` block `Status: accepted`

### 2. Load Context
- Read `.cas/rules/architecture_rules.md` to understand constraints
- Read `.cas/patterns/patterns-catalogue.yaml` to inspect reusable patterns, including each pattern's `invariants` and `anti_patterns`
- Review existing code structure in `src/` to avoid duplication

### 3. Validate Against Rules & Pattern Guardrails
- Check that the feature doesn't violate module boundaries or introduce cross-layer dependencies
- Ensure external integrations (such as LLMs) use a unified provider-agnostic gateway rather than vendor-specific SDK adapters
- Verify the proposed `code_changes` against every selected pattern's `invariants` and `anti_patterns` in `.cas/patterns/patterns-catalogue.yaml`
- If the request or proposed design violates any architecture rule, fails a pattern invariant, or matches any listed `anti_patterns`, set `decision.status: rejected` and provide a compliant `decision.alternative`

### 4. Design & Route Implementation Plan
- Identify which files need to be created or modified
- Identify applicable patterns from `patterns-catalogue.yaml`
- Select the most appropriate pattern(s) and verify full compliance with their `invariants`
- Justify why these patterns are used and how their `invariants` are satisfied
- Run `uv run cas governance route-plan --target-dir .` to evaluate the implementation plan:
  - **Path A (Governed Reuse)**: Proceed with autonomous TDD build
  - **Path B (Architectural Novelty)**: Set `decision.status: proposed`, halt autonomous coding, and ensure candidate ADR is generated for ARB review
  - **Path C (Architectural Exception)**: Verify explicit approved exception record exists in `knowledge/projects/<project>/exceptions/`
- Ensure all architecture rules are preserved

### 5. Produce Output
- MUST produce a single valid output block
- MUST always include the `decision` block, even for accepted features

---

## Output Contract

Your output must conform to this structure:

```yaml
output:
  feature:
    name: string        # Feature identifier
    module: string      # Target module
    description: string # What it does

  decision:
    status: string        # accepted | rejected | proposed
    reason: string        # Explanation for decision (especially for rejections)
    alternative: string   # Suggested alternative approach if rejected

  code_changes:
    - file: string      # Path to file
      change_type: string  # create | modify | delete
      summary: string      # What changed and why

  architecture_decision:
    description: string     # Architectural decision rationale
    rationale: string       # Why this approach was taken over alternatives
  
  architectural_impact:
    - affected_components: [string]
      pattern_usage: [string]  # Pattern IDs from catalogue
      pattern_justification: string  # Why this pattern applies and how its invariants are met

  risks:
    - description: string  # Potential issues

  validation_notes:
    - description: string  # How you validated against rules, invariants, and anti_patterns
```

**Why this matters:** The structured output ensures the feature can be machine-validated against architecture rules, pattern `invariants`, and `anti_patterns`, and tracked for governance.

**Important:**
- OUTPUT.schema.yaml is the authoritative definition of this structure
- Do not duplicate or restate the schema elsewhere
- Output must be a single, clean YAML block with no surrounding commentary

---

## Anti-Patterns (must avoid)
- Introducing tight coupling between modules
- Creating vendor-specific LLM adapters (e.g., `providers/gemini.py`, `providers/ollama.py`) or adding direct vendor SDK dependencies (`google-genai`, `openai`, `anthropic`) instead of a unified multi-provider gateway (`provider-agnostic-llm-client`)
- Citing a pattern ID in `pattern_usage` while violating its `invariants` or matching its `anti_patterns`
- Creating new modules without justification
- Duplicating existing logic
- Bypassing established patterns
- Implicit dependencies or hidden integrations

---

## Pattern Usage
- Identify and reuse existing patterns before introducing new structures
- Enforce every selected pattern's `invariants` and reject any design matching its `anti_patterns`
- If no pattern applies, set `decision.status: proposed` and explicitly justify the new structure
- Use `provider-agnostic-llm-client` and `provider-agnostic-llm-gateway` for all LLM integrations
- Maintain layered-architecture boundaries

---

## Examples

See `EXAMPLES.md` for worked examples showing accepted and rejected input/output pairs.
