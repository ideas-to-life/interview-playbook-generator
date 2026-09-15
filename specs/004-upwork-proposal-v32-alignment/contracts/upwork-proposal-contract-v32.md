# Interface Contract: Upwork Proposal Projection (V3.2 Alignment)

## Overview

Defines the V3.2 interface contract governing artifact generation for Upwork target opportunities across the runtime qualification state (`out/<target-slug>/runtime/upwork-qualification.yaml`) and projection view outputs (`out/<target-slug>/`).

---

## Inputs

1. `out/<target-slug>/runtime/upwork-qualification.yaml`
2. `out/<target-slug>/runtime/opportunity-analysis.yaml`
3. Canonical OKF evidence graph (`out/okf/`)

---

## Output Artifact Contracts

| Artifact Path | Contract Name | Contents & Invariants |
| :--- | :--- | :--- |
| `out/<target-slug>/upwork-qualification-report.md` | Executive Proposal Draft | **Clean Executive Proposal Cover Letter (350–500 words)**.<br>- Header metadata dynamically bound to `upwork-qualification.yaml`.<br>- Zero static verdict stubs.<br>- Zero internal tags (`[evidence]`, `[^source-id]`, `[OPEN CONDITION]`). |
| `out/<target-slug>/upwork-screening-answers.md` | Screening Answers | **Screening question responses only**.<br>- Zero `## Proposal Cover Letter` section.<br>- Bounded attribution per question. |
| `out/<target-slug>/upwork-work-samples.md` | Work Sample Recommendations | **Recommended work samples (max 3)**.<br>- Explicit `project_type` labels retained. |
| `out/<target-slug>/upwork-evidence-gaps.md` | Evidence Gap Analysis | **Companion Evidence Gap Report**.<br>- Requirement missing facts & confirmation questions. |

---

## Output Validation Invariants

1. **Clean Prose Rule**: `upwork-qualification-report.md` MUST pass `scripts/upwork_validator.py` clean-prose check (0 internal tags, 0 footnotes, 0 diagnostic markers).
2. **Word Count Bound Rule**: Proposal prose MUST fall within target range (350–500 words).
3. **No Duplicate Proposal Copy Rule**: `upwork-screening-answers.md` MUST NOT contain proposal cover letter copy.
4. **Attribution Integrity Rule**: Proposal copy MUST NOT inflate candidate contribution level or infer unevidenced production deployment.
5. **Candidate Agnosticism Rule**: Generator logic MUST NOT hardcode candidate employer or project names.
