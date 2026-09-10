# Validation Contract: Independent Production Verification & Upwork Validation (V2.0)

## Overview

`projection-validator` evaluates generated projection artifacts in `out/<target-slug>/` against canonical OKF evidence frontmatter and runtime qualification context, emitting `out/<target-slug>/runtime/projection-validation-report.yaml`.

---

## Independent Production Verification Check (FR-14)

$$\text{ValidateQualification}(Q, \text{OKF}) = \text{PASS} \iff$$

$$\forall r \in Q.\text{hard\_requirements}: \Big(r.\text{production\_status} = \text{verified\_production} \implies$$

$$\exists e \in \text{OKF}.\text{evidence\_cards}: e.\text{id} \in r.\text{evidence\_sources}$$
$$\land e.\text{production\_verified} = \text{true}$$
$$\land e.\text{environment} = \text{production}$$
$$\land e.\text{implementation\_role} \in \{\text{lead\_architect}, \text{sole\_developer}, \text{contributor}\}$$
$$\land (r.\text{target\_organisation\_id} \implies e.\text{organisation.id} = r.\text{target\_organisation\_id})\Big)$$

If any requirement in `upwork-qualification.yaml` claims `verified_production` without matching canonical evidence meeting this predicate, `projection-validator` MUST emit `status: FAIL`.

---

## Validated Metrics

1. **Production Status Integrity**: Verifies that every `verified_production` claim is backed by canonical EvidenceCard frontmatter with `production_verified: true`, `environment: production`, and matching `organisation.id` / `project.id`.
2. **Employment History Evidence Integrity**: Deterministically executes `scripts/employment_validator.py` against `out/okf/employment-records.yaml`.
3. **Internal Provenance & Attribution**: Confirms 100% of claims in `upwork-proposal.md` map to valid evidence cards in `upwork-qualification.yaml` `claim_traceability`.
4. **Gate Compliance**: Verifies `DO NOT APPLY` state (`proposal_generation: blocked`) prevents submission proposal generation and renders a valid Gate Report.
5. **Open Condition Verification**: Verifies `CONDITIONAL` state artifacts contain explicit `[OPEN CONDITION: <fact>]` tags.
6. **Readability & Word Count**: Validates word count (350-500 words target).
