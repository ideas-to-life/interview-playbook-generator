# Requirements Specification: Upwork Proposal Generator & Evidence Integrity Controls

**Feature**: Upwork Opportunity Qualification, Evidence Integrity Controls, and Proposal Generation  
**Repository**: `ideas-to-life/interview-playbook-generator`  
**Status**: Refined / Approved Specification (V2)  
**Version**: 2.0  
**Governance**: Existing CAS + SLDC workflow  
**Primary Objective**: Add governed Upwork proposal projection over canonical OKF career evidence, enforcing machine-readable evidence integrity, cross-organisation isolation, deterministic production qualification gates, and independent validation.

---

## Clarifications & Refinement Log

### Session 2026-09-10 (V1 Initial Specification)
- **Architecture Integration**: Registered `upwork-qualification` as a Runtime Layer skill and `upwork-proposal` as a Projection Layer skill orchestrated via `playbook-orchestrator` when `target_type: upwork`.
- **Artifact Formats**: Machine-readable qualification at `out/<target-slug>/runtime/upwork-qualification.yaml` and Markdown presentation views (`upwork-proposal.md`, `upwork-screening-answers.md`, `upwork-work-samples.md`) in `out/<target-slug>/`.
- **Validation**: Extended `projection-validator` to evaluate Upwork artifacts cleanly without leaking provenance tags into client-facing prose.

### Session 2026-09-10 (V2 Refinement: Evidence Integrity & Production Qualification)
- **Forensic Defect Fix**: First real execution revealed an implicit production inference defect where `verified_production` was incorrectly assigned based on WPP employment, repo naming (`pca-productionagents-a2a`), evaluation metrics, and personal CAS project evidence.
- **Evidence Integrity Contract**: Enforced explicit machine-readable frontmatter metadata (`organisation.id`, `project.id`, `environment`, `production_verified`, `implementation_role`, `provenance`) on OKF `EvidenceCard` concepts.
- **Strict Negative Constraints**: Prohibited inference of production status from employment records, enterprise employer names, repo/folder/file names, technology names, latency/success metrics, or personal side projects.
- **Cross-Organisation & Cross-Project Isolation**: Bounded evidence composition so that evidence from Company B or personal projects cannot satisfy Company A production requirements.
- **Dealbreaker Hard Gates**: `UNKNOWN` production status for an explicit dealbreaker requirement ("If you have not already done this in production, do not apply") MUST evaluate to `DO NOT APPLY` (`proposal_generation: blocked`).
- Q: For an opportunity where the client explicitly states “If you have not already done this in production, please do not apply,” should UNKNOWN production evidence always result in DO NOT APPLY, rather than CONDITIONAL? → A: Option A - Always evaluate to DO NOT APPLY (`proposal_generation: blocked`) when a requirement is an explicit client dealbreaker and production evidence status is `UNKNOWN`.
- Q: For a production implementation requirement referring to a specific system/project, should the PERSONAL_PRODUCTION_IMPLEMENTATION_EXPERIENCE predicate require both matching organisation.id and matching project.id, in addition to production verification and compatible implementation role? → A: Option A - Both matching `organisation.id` AND matching `project.id` are strictly mandatory for project-specific production requirements.
- Q: Should AC-15 be changed so that the Senior Agentic AI Architect target evaluates to DO NOT APPLY whenever canonical evidence does not explicitly establish WPP production deployment, with no CONDITIONAL outcome? → A: Option A - Yes, update AC-15 to state strictly: "The Senior Agentic AI Architect target evaluates to DO NOT APPLY whenever canonical evidence does not explicitly establish WPP production deployment."

---

## 1. Purpose

Extend the Interview Playbook Generator so that an Upwork target opportunity is processed through a governed, multi-stage workflow:

```
Upwork Target Specification
        │
        ▼
Opportunity Analysis (Runtime)
        │
        ▼
Qualification Gate (upwork-qualification)
        │
        ├── DO NOT APPLY ──► Gate Report (proposal_generation: blocked)
        │
        ├── CONDITIONAL ───► Draft + [OPEN CONDITION] (proposal_generation: allowed_with_conditions)
        │
        └── APPLY ─────────► Proposal Package (proposal_generation: allowed)
              │
              ▼
    Independent Validation (projection-validator)
              │
              ▼
        Human Review Boundary
```

The feature reuses the repository’s existing career evidence and projection architecture. Upwork proposals are output projections over governed career evidence, not independent truth sources.

---

## 2. Problem Statement

The system must distinguish between:
1. **Employment at an organisation** (tenure & title);
2. **Work performed on a specific project/system**;
3. **Operation of that system in a live production environment**;
4. **The candidate's personal implementation responsibility for that system**.

These facts must NOT be inferred interchangeably. A candidate must NOT receive credit for a production experience requirement merely because:
- They worked for the organisation;
- A project repository contains "production" or "prod" in its name;
- Documentation uses production-like terminology or contains latency/eval metrics;
- A personal project demonstrates similar technical capability;
- A different project at the same organisation was deployed;
- A project at another organisation was deployed;
- The candidate has theoretical or advisory knowledge of the technology.

---

## 3. Goals & Non-Goals

### Goals
1. Establish structured, machine-readable provenance for evidence relevant to qualification (`organisation.id`, `project.id`, `environment`, `production_verified`, `implementation_role`).
2. Explicitly classify environments (`production`, `staging`, `prototype`, `lab`, `personal`, `unknown`).
3. Require explicit `production_verified: true` for production deployment claims.
4. Distinguish hands-on implementation roles (`lead_architect`, `sole_developer`, `contributor`) from advisory/evaluator roles (`advisor`, `evaluator`).
5. Prevent qualification from inferring verified production status from indirect signals (repo names, metrics, company names).
6. Enforce Cross-Organisation Isolation and Cross-Project Isolation.
7. Treat `UNKNOWN` as a safe non-positive state rather than an implicit positive.
8. Support explicit client dealbreaker requirements (`UNKNOWN` $\rightarrow$ `DO NOT APPLY`).
9. Ensure `projection-validator` independently checks qualification claims against canonical OKF evidence.
10. Maintain 100% claim traceability back to canonical evidence.

### Non-Goals
- Automating Upwork browsing, scraping, or proposal submission.
- Manufacturing production evidence or upgrading evidence via LLM reasoning.
- Creating a parallel evidence store outside OKF.
- Changing the four-layer architecture or making Validation a fifth layer.

---

## 4. Functional Requirements

### FR-01 — Structured Evidence Identity
Evidence used for qualification MUST expose machine-readable identity fields:
- `organisation.id`: Reference to `out/okf/employment-records.yaml` ID or registered origin (`personal-cas`, `mostelli-advisory`).
- `organisation.type`: `enterprise_employer` | `advisory_client` | `personal_project` | `academic`.
- `project.id`: Unique system/project identifier (e.g. `wpp-open-pca`).
- `environment`: `production` | `staging` | `prototype` | `lab` | `personal` | `unknown`.
- `production_verified`: Boolean (`true` | `false`).
- `implementation_role`: `lead_architect` | `sole_developer` | `contributor` | `advisor` | `evaluator` | `none`.
- `provenance.source_id` & `provenance.source_type`: `production_telemetry` | `release_notes` | `client_signoff` | `repo_code` | `eval_harness` | `resume_claim`.

### FR-02 — Explicit Environment Classification
If canonical evidence does not explicitly establish the deployment environment in frontmatter, the environment status MUST remain `unknown`. The system MUST NOT infer `production` from free-text prose or filenames.

### FR-03 — Explicit Production Verification
Production deployment MUST be represented as an explicit evidence fact (`production_verified: true`). Production verification MUST NOT be inferred from employment records, company names, repo names, folder paths, filenames, technology names, test metrics, or latency benchmarks.

### FR-04 — Implementation Responsibility
Evidence MUST distinguish the candidate's implementation role. A role equivalent to `advisor` or `evaluator` MUST NOT satisfy a requirement that explicitly requires personal implementation experience.

### FR-05 — Production Implementation Experience Predicate
The system MUST define a deterministic qualification predicate for system/project-specific production requirements:
$$\text{PERSONAL\_PRODUCTION\_IMPLEMENTATION\_EXPERIENCE}(E, R) \iff$$
$$\big(E.\text{organisation.id} = R.\text{target\_organisation\_id} \lor R.\text{organisation\_bound} = \text{ANY}\big)$$
$$\land \big(E.\text{project.id} = R.\text{target\_project\_id} \lor R.\text{project\_bound} = \text{ANY}\big)$$
$$\land \big(E.\text{environment} = \text{production} \land E.\text{production\_verified} = \text{true}\big)$$
$$\land \big(E.\text{implementation\_role} \in \{\text{lead\_architect}, \text{sole\_developer}, \text{contributor}\}\big)$$

Both matching `organisation.id` AND matching `project.id` are MANDATORY for system/project-specific production implementation requirements.

### FR-06 — Bounded Evidence Composition
Multiple evidence records MAY be combined ONLY when they refer to the **same organisation AND the same project/system** (`C_1.organisation.id == C_2.organisation.id` AND `C_1.project.id == C_2.project.id`). Cross-organisation evidence composition and cross-project composition are strictly prohibited for production requirements.

### FR-07 — Evidence Provenance
Production-related evidence MUST retain provenance identifying source type (`production_telemetry`, `release_notes`, `client_signoff`, `repo_code`, `eval_harness`, `resume_claim`). Repository code or evaluation harnesses alone do NOT establish production deployment.

### FR-08 — Prohibited Inference Rules (Negative Constraints)
The qualification engine MUST NOT infer `production_verified = true` from any of the following 15 prohibited paths:
1. Employment relationship
2. Employer name
3. Repository name
4. Directory name
5. "production" in prose
6. "deployed" in prose
7. "operational" in prose
8. Technology choice
9. Evaluation metrics
10. High success rate
11. Latency measurements
12. CI/CD evidence
13. Production-like architecture
14. Personal projects
15. Prototype/innovation terminology

### FR-09 — Qualification Evidence Boundary
Qualification MUST consume canonical evidence as the authority for factual claims. Qualification MUST NOT upgrade environment, production verification, implementation role, or organisation identity.

### FR-10 — Production Status Classification
The system MUST classify requirements as:
- `VERIFIED_PRODUCTION`: Canonical evidence explicitly proves live production operation in a commercial operating enterprise.
- `VERIFIED_NON_PRODUCTION`: Canonical evidence explicitly establishes prototype, lab, staging, or personal environment.
- `UNKNOWN`: Canonical evidence does not explicitly establish deployment environment.

### FR-11 — Dealbreaker Hard Gates
For requirements explicitly stating *"If you have not already done this in production, do not apply"*:
- `VERIFIED_PRODUCTION` + compatible implementation role $\rightarrow$ Satisfies gate (`APPLY`).
- `VERIFIED_NON_PRODUCTION` $\rightarrow$ Fails gate (`DO NOT APPLY` / `proposal_generation: blocked`).
- `UNKNOWN` $\rightarrow$ Always fails gate (`DO NOT APPLY` / `proposal_generation: blocked`). `UNKNOWN` MUST NEVER yield `CONDITIONAL` or `APPLY` for an explicit dealbreaker requirement.

### FR-12 — Qualification Decision Integrity
- `APPLY`: All hard requirements satisfied by verified evidence without fabrication.
- `CONDITIONAL`: Opportunity fits, but material unresolved non-dealbreaker facts require candidate confirmation (`[OPEN CONDITION: <fact>]`).
- `DO NOT APPLY`: Hard requirement absent, contradicted, or unverified dealbreaker (`UNKNOWN` or `VERIFIED_NON_PRODUCTION`). Generates Gate Report only.

### FR-13 — Projection Boundary
Projection artifacts MUST NOT upgrade qualification evidence. If qualification states `UNKNOWN`, proposal generation MUST NOT transform that into a production claim. If qualification states `DO NOT APPLY`, no submission-ready proposal is generated.

### FR-14 — Independent Validation
`projection-validator` MUST independently verify qualification claims against canonical OKF evidence frontmatter. A claim of `verified_production` MUST fail validation unless canonical evidence independently establishes matching organisation, matching project, `environment: production`, `production_verified: true`, and compatible `implementation_role`.

### FR-15 — Cross-Organisation Isolation
Enforce organisation boundaries when evaluating organisation-specific experience. Evidence from Organisation B or Personal/CAS cannot satisfy Organisation A production requirements.

### FR-16 — Cross-Project Isolation
Evidence from Project X cannot satisfy a project-specific requirement for Project Y, even within the same organisation.

### FR-17 — Personal Project Isolation
Personal project evidence (`organisation.id: personal-cas`) MAY satisfy general capability requirements (e.g. "Python API experience"), but MUST NOT satisfy employer-specific production requirements.

### FR-18 — Evidence Traceability
Every material production claim MUST trace to canonical evidence records (`claim_traceability` array). Internal provenance syntax MUST NOT leak into client-facing proposal prose.

### FR-19 — No Unsupported Quantitative Claims
The system MUST NOT invent business outcomes, staffing reductions, throughput improvements, or agent counts. Historical metrics MUST match canonical evidence; proposed targets MUST be framed as future architecture recommendations.

### FR-20 — Screening Answer Integrity
Screening answers MUST distinguish verified candidate experience from proposed future architecture recommendations.

### FR-21 — Work Sample Integrity
Recommended work samples MUST match qualification status and MUST NOT describe prototype/lab work as production experience.

### FR-22 — Determinism and Idempotence
Identical inputs MUST produce identical qualification decisions and machine-readable YAML artifacts. Repeated runs MUST NOT accumulate or strengthen claims.

### FR-23 — Regression Protection
The suite MUST include automated tests for 10 regression scenarios:
1. WPP employment + WPP prototype evidence $\rightarrow$ `production_status: unknown` / `DO NOT APPLY`.
2. WPP employment + explicit WPP production evidence + implementation role $\rightarrow$ `APPLY`.
3. WPP prototype evidence + Personal project production evidence $\rightarrow$ WPP status remains `unknown`.
4. Repo name containing "production" without explicit frontmatter attestation $\rightarrow$ `unknown`.
5. Company A requirement + Company B production evidence $\rightarrow$ Company A requirement not met.
6. Same organisation, different project $\rightarrow$ Project X evidence cannot satisfy Project Y requirement.
7. Production evidence + `advisor`/`evaluator` role only $\rightarrow$ Fails personal implementation requirement.
8. Qualification claiming `verified_production` without canonical evidence $\rightarrow$ Validation fails.
9. Conditional qualification $\rightarrow$ Unresolved condition remains visible.
10. `DO NOT APPLY` qualification $\rightarrow$ Gate Report generated, no submission proposal.

---

## 5. Acceptance Criteria

- **AC-01**: Given an explicit production dealbreaker and prototype/unknown evidence, decision is `DO NOT APPLY`.
- **AC-02**: Given explicit canonical production evidence + compatible implementation role, requirement is met (`APPLY`).
- **AC-03**: Employment records alone never establish production implementation experience.
- **AC-04**: Repository names, folder paths, filenames, or prose wording cannot establish production verification.
- **AC-05**: Evaluation metrics cannot establish production verification.
- **AC-06**: Personal project evidence cannot satisfy employer-specific production requirements.
- **AC-07**: Evidence from another organisation cannot satisfy target organisation production requirements.
- **AC-08**: Evidence from another project cannot satisfy project-specific production requirements.
- **AC-09**: Advisor/evaluator role cannot satisfy personal implementation requirements.
- **AC-10**: Qualification cannot upgrade canonical evidence.
- **AC-11**: Projection cannot upgrade qualification.
- **AC-12**: Validation independently fails unbacked production claims.
- **AC-13**: All claims trace 100% to canonical evidence.
- **AC-14**: Unsupported quantitative metrics are rejected or framed as targets.
- **AC-15**: The Senior Agentic AI Architect target evaluates to DO NOT APPLY whenever canonical evidence does not explicitly establish WPP production deployment.
- **AC-16**: Architecture remains 4-layer (Knowledge, Runtime, Coaching, Projection) with Validation as a cross-cutting quality gate.
- **AC-17**: Execution is deterministic and idempotent.
- **AC-18**: All 10 regression scenarios pass automated testing.

---

## 6. Architectural Invariants

1. Canonical evidence is authoritative for factual experience claims.
2. Qualification evaluates evidence; it does not manufacture evidence.
3. Projection communicates qualification; it does not strengthen it.
4. Validation independently checks critical qualification claims.
5. Employment is not equivalent to production deployment.
6. Production deployment is not equivalent to personal implementation.
7. Personal projects are not equivalent to real-company production experience.
8. Evidence composition is bounded by organisation and project identity.
9. `UNKNOWN` is never silently promoted to `VERIFIED_PRODUCTION`.
10. Explicit client dealbreakers override optimistic interpretation.
11. Client-facing prose remains inside the canonical evidence boundary.
12. Validation is cross-cutting and is not a fifth architectural layer.
13. Human review remains the final boundary before submission.
