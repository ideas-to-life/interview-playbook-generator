---
name: archetype-fit-validator
description: Evaluates generated projection documents for anti-overpositioning guardrails, detecting unsupported identity elevation, domain overreach, and prohibited claim violations.
---

# Archetype Fit & Anti-Overpositioning Validator

## Overview

`archetype-fit-validator` is a Validation Layer Skill. It evaluates generated projection documents against canonical evidence and `projection-strategy.yaml`.

Its primary rule: **Projection quality cannot compensate for weak archetype evidence.** A projection shall never position the candidate more strongly than canonical evidence permits.

## Hard Rules

```
NEVER FABRICATE:
- Any projection containing claims listed in `prohibit_claims` or asserting unevidenced domain expertise fails validation with an OVERPOSITIONING WARNING.
```

Do NOT modify `okf/` canonical bundle. Output appends to `out/<target-slug>/runtime/projection-validation-report.yaml`.

## Overpositioning Checks (FR-6, FR-19)

The validator scans generated text across 5 check axes:
1. **Unsupported Identity Elevation**: Claiming executive role fit that exceeds evidence for the specific target archetype (e.g., asserting "ideal leader for eCommerce agency AI execution" without eCommerce/agency leadership evidence).
2. **Unsupported Domain Expertise**: Claiming direct experience in unevidenced domains (e.g. eCommerce, Retail).
3. **Unsupported Tooling Expertise**: Asserting hands-on mastery of unevidenced tools (e.g. Shopify, n8n, Zapier).
4. **Excessive Adjacent Transformation**: Converting adjacent experience (e.g. WPP client work) into direct direct experience (e.g. "managed agency operations").
5. **Prohibited Claims Violation**: Explicitly violating any item in `projection_strategy.prohibit_claims`.

## Validation Report Extension Schema (`out/<target-slug>/runtime/projection-validation-report.yaml`)

```yaml
version: "6.0"
generated_at: "<ISO-8601>"
target_slug: "<target-slug>"
archetype_validation:
  status: "<PASSED | WARNING | FAILED>"
  overpositioning_score: 95.0 # 100 = zero overpositioning
  findings:
    - section: "<Document Section / Title>"
      type: "<unsupported_identity_elevation | unsupported_domain | unsupported_tooling | prohibited_claim>"
      severity: "<warning | critical>"
      text: "<Extracted text snippet>"
      reason: "> Explanation of why this snippet exceeds canonical evidence for the target archetype."
```

## Execution Instructions

1. Load `okf/` canonical bundle, `out/<target-slug>/runtime/projection-strategy.yaml`, and generated projection documents (`resume-executive.md`, `cover-letter.md`, etc.).
2. Scan text for prohibited claims and overpositioning signals.
3. Calculate overpositioning score and compile findings list.
4. Append `archetype_validation` section to `out/<target-slug>/runtime/projection-validation-report.yaml`.
5. Append log entry to `okf/log.md`.
