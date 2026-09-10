---
name: upwork-opportunity-qualifier
description: Qualifies an Upwork opportunity against explicit hard requirements and canonical career evidence before proposal generation.
---

# Upwork Opportunity Qualifier

## Overview

`upwork-opportunity-qualifier` is a Runtime Layer Skill for Upwork opportunities. It is deliberately a gate, not a proposal writer.

It reads the configured target opportunity, the shared opportunity analysis, and the canonical OKF evidence. It identifies hard client requirements, maps them to evidence, distinguishes direct from adjacent/transferable evidence, and emits an explicit `APPLY`, `CONDITIONAL`, or `DO NOT APPLY` decision.

Output:

`out/<target-slug>/runtime/upwork-qualification.yaml`

The qualification result is consumed by `upwork-proposal-generator`.

## Hard Rules

```
NEVER FABRICATE:
- Production status
- Projects or clients
- Metrics or business outcomes
- Team sizes
- Technologies
- Responsibilities
- Scope or ownership
```

1. Treat explicit client disqualifiers as hard gates.
2. Do not infer production experience from a prototype, personal project, architecture study, or stated capability.
3. Do not treat an adjacent technology as equivalent to a specifically required technology unless the client requirement permits transferable experience.
4. Distinguish `direct`, `adjacent`, `transferable`, and `absent` evidence.
5. If a hard requirement is unsupported, the decision cannot be `APPLY`.
6. If evidence is incomplete but could reasonably be clarified by the candidate, use `CONDITIONAL` and identify the exact evidence needed.
7. Never rewrite a candidate gap as a strength.
8. Re-running the Skill replaces the previous qualification output.

## Decision Rules

### APPLY

Use only when all explicit hard requirements have credible supporting evidence and there is no material evidence-integrity risk.

### CONDITIONAL

Use when the opportunity may fit, but one or more important requirements are unresolved and require candidate confirmation or additional evidence.

### DO NOT APPLY

Use when an explicit hard requirement is contradicted by available evidence, clearly absent, or the client's stated screening condition cannot be met without inventing or materially overstating experience.

## Input

Read:

1. `config/config.yaml`
2. `target_opportunity.source`
3. `out/<target-slug>/runtime/opportunity-analysis.yaml`
4. Relevant canonical OKF evidence, especially:
   - `out/okf/evidence-cards/`
   - `out/okf/capabilities/`
   - `out/okf/signature-achievements.md`
   - `out/okf/story-library.md`
   - `out/okf/executive-identity.md`
5. Any target-specific evidence explicitly referenced by the opportunity configuration.

Do not perform an unrestricted historical scan when the relevant canonical evidence is already available.

## Qualification Procedure

1. Extract the client's explicit hard requirements and disqualifiers.
2. Extract important preferred requirements separately.
3. Identify the client's strongest buying signals.
4. For each hard requirement, locate the strongest canonical evidence.
5. Classify each requirement as `direct`, `adjacent`, `transferable`, or `absent`.
6. Record evidence strength as `strong`, `moderate`, or `weak`.
7. Record production status where relevant as `verified_production`, `verified_non_production`, `unknown`, or `not_applicable`.
8. Identify unsupported client questions that the proposal would otherwise have to answer.
9. Select the 2–3 strongest evidence matches for a potential proposal.
10. Recommend up to three work samples only where supported by available evidence.
11. Determine the final decision using the rules above.

## Output Schema

Write `out/<target-slug>/runtime/upwork-qualification.yaml`:

```yaml
version: "1.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
decision: "APPLY | CONDITIONAL | DO NOT APPLY"
confidence: "HIGH | MEDIUM | LOW"

client_buying_signals:
  - "<signal>"

hard_requirements:
  - requirement: "<requirement>"
    status: "met | unresolved | not_met"
    relationship: "direct | adjacent | transferable | absent"
    evidence_strength: "strong | moderate | weak"
    production_status: "verified_production | verified_non_production | unknown | not_applicable"
    evidence: ["<evidence reference>"]
    rationale: "<brief factual rationale>"

preferred_requirements:
  - requirement: "<requirement>"
    relationship: "direct | adjacent | transferable | absent"
    evidence_strength: "strong | moderate | weak"
    evidence: ["<evidence reference>"]

strongest_evidence_matches:
  - "<evidence reference>"

proposal_risks:
  - "<risk>"

missing_evidence:
  - "<specific evidence needed>"

recommended_work_samples:
  - "<sample>"

rationale: "<decision rationale>"
```

## Special Upwork Integrity Rule

If the client explicitly says the candidate must have personally implemented the capability in production for a real company, architecture leadership, prototypes, personal projects, demos, or prototype-and-innovation work do not satisfy that requirement unless canonical evidence explicitly establishes production implementation in a real operating company.

## Completion

After writing the YAML, append a concise entry to `okf/log.md` if that logging convention is active for the current pipeline.
