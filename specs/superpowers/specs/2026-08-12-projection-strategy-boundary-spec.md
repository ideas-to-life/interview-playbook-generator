# Spec: Projection Strategy Evidence Boundary & Transferability

## Objective

Refine the Projection Strategy layer so that target-role requirements cannot be promoted into candidate capabilities unless independently supported by canonical evidence.

The strategy layer enforces a three-layer semantic separation:
1. **Target Requirement**: What the client organisation needs (e.g., "Build out a Cloud Centre of Excellence from the ground up").
2. **Candidate Evidence**: What the candidate has actually demonstrated (e.g., "Led Enterprise Architecture operating-model redesign").
3. **Projection Positioning**: How demonstrated experience is positioned as relevant or transferable (e.g., "Apply EA operating-model and governance experience to the CCoE establishment mandate").

Target requirements MUST NEVER become candidate evidence or candidate positioning unless independently supported by canonical evidence.

## Governing Principles

1. **Target requirements vs Candidate evidence**: Target requirements describe what the client needs; candidate evidence describes what the candidate has done. Target requirements must never become candidate evidence or candidate positioning unless independently supported by canonical evidence.
2. **Transferable framing over domain substitution**: When target requirements are adjacent to, but not directly evidenced by, candidate experience, the projection must use explicit transferable framing rather than domain substitution.
3. **Journey vs Destination**: The target defines the destination; the evidence defines the journey. Projection may explain why the candidate’s demonstrated experience makes the destination credible, but it must never rewrite the journey as though the candidate has already reached it.

## Tech Stack & Commands

- **Language / Framework**: Python 3.13, Pytest, YAML, Markdown Skills specification.
- **Commands**:
  ```bash
  Test: pytest
  Lint: python -m pytest tests/test_lint.py
  Single Test: pytest tests/test_boundary_transferability.py
  ```

## Project Structure & Touched Files

```
skills/
├── projection-strategy-generator/SKILL.md → Restrict lead_with to evidence-supported candidate capabilities; extend bridge section
├── archetype-fit-validator/SKILL.md      → Validate 3-layer semantic separation & domain substitution prevention
├── resume-projection/SKILL.md             → Downstream transferability framing & domain substitution prevention
└── playbook-orchestrator/SKILL.md       → Pipeline integration for end-to-end boundary validation

AGENTS.md                                → Add new permanent governing principles
docs/superpowers/specs/2026-08-12-projection-strategy-boundary-spec.md → Feature specification document
tests/test_boundary_transferability.py   → End-to-end regression test suite
```

## Three-Layer Semantic Separation & Schema Design

### 1. `lead_with` Restrictive Rule
`lead_with` MUST contain ONLY candidate capabilities that are:
- Classified as `DIRECT` or `STRONG_RELEVANT`
- Directly supported by canonical evidence in `okf/`

`lead_with` MUST NOT contain target requirements that are `TRANSFERABLE`, `ADJACENT`, or `GAP` (e.g. `ccoe_establishment` MUST NOT be in `lead_with` if evidence only supports EA operating models).

### 2. Capability Classes & Strategy Mapping
- **DIRECT**: Explicit candidate evidence. Treatment: `lead_with`, `emphasise`.
- **STRONG_RELEVANT**: Substantial related evidence. Treatment: `emphasise`, `support`.
- **RELEVANT**: Relevant experience, secondary focus. Treatment: `support`.
- **TRANSFERABLE**: Strong evidence in adjacent discipline. Treatment: `frame_transferability` in `bridge` section. Must NOT be in `lead_with`.
- **ADJACENT**: Related but limited evidence. Treatment: `acknowledge`, `frame_transferability` in `bridge` section.
- **GAP**: Insufficient evidence. Treatment: `do_not_claim`.

### 3. Extended `bridge` Schema in `projection-strategy.yaml`

```yaml
bridge:
  - target_capability: "ccoe_establishment"
    candidate_evidence:
      - "enterprise_architecture_operating_model"
      - "architecture_governance"
    relationship: "transferable"
    rationale: "Candidate has established and operated EA governance and operating models that provide directly relevant experience for CCoE governance."
    framing: "Applied Enterprise Architecture operating-model and governance experience to cloud and CCoE-aligned initiatives."
```

### 4. Prohibited Domain Substitutions & Target Verb Protection
- Prohibit rewriting:
  - Enterprise Architecture $\rightarrow$ Cloud Centre of Excellence
  - EA governance $\rightarrow$ Cloud governance leadership
  - Architecture operating model $\rightarrow$ CCoE operating model established
- Prohibit transferring target verbs (`build`, `establish`, `create`, `own`, `lead`, `design`, `transform`, `launch`, `found`, `set up`) to candidate history without independent evidence.

## Testing Strategy

- **`tests/test_boundary_transferability.py`**:
  1. `lead_with` verification: Assert `lead_with` in `projection-strategy.yaml` contains zero unsupported target capabilities.
  2. Extended `bridge` schema verification: Assert `bridge` items map `target_capability`, `candidate_evidence`, `relationship`, `rationale`, and `framing`.
  3. Domain substitution & target verb protection verification across generated presentation view files (`resume-executive.md`, `resume-ats.md`, `cover-letter.md`, `executive-brief.md`, `playbook.md`).
  4. Enterprise Cloud Architect regression: CCoE establishment classified as `transferable`/`adjacent` while overall fit remains `Strong Fit`.

## Success Criteria

1. Target requirements and candidate evidence are represented separately.
2. `lead_with` is strictly restricted to evidence-supported candidate capabilities.
3. Target requirements cannot independently become `lead_with` capabilities.
4. `TRANSFERABLE` and `ADJACENT` relationships are explicitly supported in extended `bridge` mappings.
5. Domain substitution is prevented.
6. Target verbs cannot be transferred to candidate history without evidence.
7. End-to-end validation covers all major generated artefacts (`resume-executive.md`, `resume-ats.md`, `cover-letter.md`, `executive-brief.md`, `playbook.md`).
8. The Enterprise Cloud Architect regression case classifies CCoE establishment as transferable/adjacent rather than direct/core.
9. Zero regression on existing 94 tests.

## Boundaries

- **Always do**: Run `pytest` before committing; maintain strict separation between target needs and candidate evidence.
- **Ask first**: Altering core OKF bundle structure.
- **Never do**: Allow target requirements to overwrite candidate historical achievements; perform domain substitution on adjacent capabilities.
