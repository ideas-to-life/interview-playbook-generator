FEATURE: Evidence Integrity & Production Qualification Controls

CONTEXT

The first real execution of the Upwork Proposal Generator exposed a
qualification-integrity defect.

A target opportunity explicitly required:

"If you have not already done this for a real company in production,
please do not apply."

The generator incorrectly produced APPLY because production experience
was inferred from a combination of employment evidence, WPP project
evidence, repository naming, production-like terminology, evaluation
metrics, and unrelated CAS/personal-project evidence.

The forensic analysis established that:

- employment evidence proves employment/tenure but does not prove that a
  particular system was deployed to production;
- repository/project names containing terms such as "production",
  "prod", or "prodagents" do not prove production;
- evaluation metrics do not prove production deployment;
- prototype/innovation/personal-project evidence must not satisfy a
  real-company production requirement;
- qualification currently has the ability to infer production status
  rather than consuming an explicit canonical evidence fact;
- projection validation currently trusts the derived qualification result
  rather than independently validating the production claim against
  canonical evidence;
- evidence from different organisations/projects can currently contaminate
  a target-bound qualification decision.

The purpose of this feature is to establish a governed, machine-readable
evidence contract and qualification boundary so that production experience
can only be claimed when explicitly supported by canonical evidence.

IMPORTANT PROCESS CONSTRAINT

This document is requirements input for /speckit.specify.

Do NOT treat this document as an implementation specification.

Do NOT prescribe implementation files, functions, classes, algorithms,
repository changes, or coding tasks here.

The resulting specification must remain consistent with the existing
four-layer architecture:

1. Knowledge
2. Runtime
3. Coaching
4. Projection

Validation remains a cross-cutting quality gate and must not become a
fifth architectural layer.

The implementation approach must subsequently be determined by
/speckit.plan and the repository's CAS/SLDC conventions.


PROBLEM STATEMENT

The system must distinguish between:

1. employment at an organisation;
2. work performed on a particular project/system;
3. operation of that system in production;
4. the candidate's personal implementation responsibility for that
   production system.

These facts must not be inferred interchangeably.

A candidate must not receive credit for a production-experience requirement
merely because:

- they worked for the organisation;
- a project repository contains "production" in its name;
- documentation uses production-like terminology;
- evaluation/test metrics are high;
- a personal project demonstrates similar technical capability;
- a different project at the same organisation was deployed;
- a project at another organisation was deployed;
- the candidate has theoretical or advisory knowledge of the technology.

The system therefore requires an explicit evidence integrity contract,
bounded evidence composition rules, deterministic qualification predicates,
and independent validation of qualification claims.


GOALS

The feature MUST:

1. Establish structured, machine-readable provenance for evidence relevant
   to qualification.

2. Explicitly represent organisation identity and project/system identity.

3. Explicitly represent environment/deployment status.

4. Explicitly represent whether production deployment is verified.

5. Explicitly represent the candidate's implementation responsibility.

6. Distinguish production deployment from production implementation
   experience.

7. Prevent qualification from inferring verified production status from
   indirect signals.

8. Prevent evidence from unrelated organisations or projects from
   satisfying target-bound production requirements.

9. Prevent personal-project evidence from satisfying employer-specific
   production requirements.

10. Allow bounded composition of multiple evidence records only when the
    records refer to the same organisation and project/system.

11. Make UNKNOWN a safe state rather than an implicit positive.

12. Support explicit client dealbreaker requirements where lack of verified
    experience means the opportunity must not be pursued.

13. Ensure projection validation independently verifies production claims
    against canonical evidence.

14. Preserve traceability from qualification decisions back to canonical
    evidence.

15. Make the current failed Upwork scenario a regression case.

16. Preserve deterministic and idempotent qualification behaviour.


NON-GOALS

This feature MUST NOT:

- automate Upwork browsing or scraping;
- automate proposal submission;
- infer marketplace behaviour;
- create new client claims;
- manufacture production evidence;
- upgrade evidence through LLM reasoning;
- establish production status merely from technology usage;
- introduce a separate evidence system that fragments the existing OKF
  unless /speckit.specify establishes a compelling requirement-based need;
- change the four-layer architecture;
- make Validation a fifth architectural layer;
- decide implementation technology or code structure.


FUNCTIONAL REQUIREMENTS


FR-01 — Structured Evidence Identity

Evidence used for qualification MUST expose machine-readable identity for:

- organisation;
- project/system;
- environment;
- production verification;
- implementation responsibility;
- provenance/source authority.

Organisation identity MUST distinguish, at minimum:

- enterprise employer;
- advisory/client organisation;
- personal project;
- academic context.

Project/system identity MUST uniquely identify the project or system to
which the evidence relates.

The exact schema representation is to be determined during specification
and planning, but the information MUST be explicit and machine-readable.


FR-02 — Explicit Environment Classification

Evidence MUST support explicit environment classification including, at
minimum:

- production;
- staging;
- prototype;
- lab;
- personal;
- unknown.

If canonical evidence does not explicitly establish the environment,
the resulting environment status MUST remain UNKNOWN.

The system MUST NOT infer production from free-text terminology.


FR-03 — Explicit Production Verification

Production deployment MUST be represented as an explicit evidence fact.

The system MUST distinguish between:

- explicitly verified production;
- explicitly verified non-production;
- unknown.

Production verification MUST NOT be inferred from:

- employment records;
- organisation name;
- repository names;
- directory names;
- filenames;
- project names;
- technology names;
- deployment-like terminology;
- evaluation/test metrics;
- performance benchmarks;
- source-code structure;
- assumptions about normal enterprise practice.


FR-04 — Implementation Responsibility

Evidence MUST distinguish the candidate's responsibility for the relevant
system.

At minimum, the model MUST distinguish roles equivalent to:

- lead architect;
- sole developer;
- contributor;
- advisor;
- evaluator;
- none/unknown.

A role equivalent to advisor or evaluator MUST NOT satisfy a requirement
that explicitly requires personal implementation experience.

The system MUST NOT infer hands-on implementation responsibility merely
from employment or job title.


FR-05 — Production Implementation Experience Predicate

The system MUST define a deterministic qualification predicate for:

PERSONAL_PRODUCTION_IMPLEMENTATION_EXPERIENCE

A production implementation experience claim is valid only when:

1. the evidence relates to the required organisation, where the
   requirement is organisation-bound; AND

2. the evidence relates to the required project/system; AND

3. the environment is explicitly production; AND

4. production deployment is explicitly verified; AND

5. the candidate's implementation responsibility is explicitly compatible
   with hands-on implementation.

Employment alone MUST NOT satisfy the predicate.

Production evidence alone MUST NOT satisfy the predicate.

An advisory/evaluation role alone MUST NOT satisfy the predicate.


FR-06 — Bounded Evidence Composition

The system MAY combine multiple evidence records to establish a
production implementation experience predicate.

However, composition MUST be bounded.

Evidence records MAY be combined only when they refer to:

- the same organisation; AND
- the same project/system.

Cross-organisation evidence composition MUST NOT satisfy an
organisation-bound production requirement.

Cross-project evidence composition MUST NOT satisfy a
project-bound production requirement.

Employment evidence MAY establish the employment relationship but MUST NOT
upgrade deployment or implementation facts about a project.

A personal-project evidence record MUST NOT upgrade or satisfy an
employer-specific production requirement.


FR-07 — Evidence Provenance

Production-related evidence MUST retain provenance identifying the source
and authority of the assertion.

The evidence model MUST be capable of distinguishing source types such as:

- production telemetry;
- release/deployment records;
- client or organisational sign-off;
- explicit attestation;
- repository/source-code evidence;
- evaluation harness;
- CV/resume claim.

The presence of a source type MUST NOT itself establish production.

For example, repository evidence may establish implementation activity but
does not automatically establish production deployment.


FR-08 — No Implicit Production Inference

The qualification engine MUST NOT infer:

production_verified = true

from any indirect combination of facts.

The following are explicitly prohibited inference paths:

- employment → production;
- employer name → production;
- repository name → production;
- directory name → production;
- "production" in prose → production;
- "deployed" in prose → production;
- "operational" in prose → production;
- technology choice → production;
- evaluation metrics → production;
- high success rate → production;
- latency measurements → production;
- CI/CD evidence → production;
- production-like architecture → production;
- personal project → employer production experience;
- prototype/innovation terminology → production.


FR-09 — Qualification Evidence Boundary

Qualification MUST consume canonical evidence as the authority for factual
claims.

Qualification MUST NOT upgrade:

- environment;
- production verification;
- implementation responsibility;
- organisation identity;
- project identity.

Any derived qualification status MUST remain traceable to the canonical
evidence supporting it.

A qualification artifact MUST NOT become the authoritative source for
facts that originated in canonical evidence.


FR-10 — Production Status Classification

The system MUST distinguish at least:

VERIFIED_PRODUCTION

Meaning:
Canonical evidence explicitly establishes that the relevant system
operated in a production environment.

VERIFIED_NON_PRODUCTION

Meaning:
Canonical evidence explicitly establishes a non-production environment,
such as prototype, lab, staging, or personal.

UNKNOWN

Meaning:
Canonical evidence does not explicitly establish production or
non-production status.

The system MUST NOT treat UNKNOWN as VERIFIED_PRODUCTION.


FR-11 — Dealbreaker Hard Gates

The opportunity model MUST be capable of identifying a hard requirement as
a production-experience dealbreaker when the client explicitly states
that candidates without prior production experience should not apply.

For such a requirement:

- verified production implementation experience MUST satisfy the gate;
- verified non-production experience MUST fail the gate;
- unknown production status MUST NOT result in APPLY.

Where the opportunity explicitly states "do not apply" without verified
experience, the final qualification decision MUST be DO NOT APPLY unless
canonical evidence establishes the required experience.

The system MAY support CONDITIONAL for unknown evidence in opportunities
where the requirement is not an explicit application dealbreaker.

The distinction between ordinary hard requirements and explicit
dealbreaker requirements MUST be represented in the requirements model.


FR-12 — Qualification Decision Integrity

Qualification decisions MUST use the following conceptual states:

APPLY
CONDITIONAL
DO NOT APPLY

For an explicit production dealbreaker:

VERIFIED_PRODUCTION + valid implementation responsibility
    → APPLY

VERIFIED_NON_PRODUCTION
    → DO NOT APPLY

UNKNOWN
    → DO NOT APPLY

For a non-dealbreaker requirement, UNKNOWN MAY result in CONDITIONAL if
the unresolved condition is explicitly surfaced.

The system MUST NOT generate a submission-ready proposal that silently
assumes an unresolved production requirement has been satisfied.


FR-13 — Projection Boundary

Projection artifacts MUST NOT upgrade qualification evidence.

If qualification states that production experience is unknown,
proposal generation MUST NOT transform that into a production claim.

If qualification states DO NOT APPLY, the system MUST NOT generate a
submission-ready proposal.

If qualification is CONDITIONAL, any unresolved material condition MUST
remain explicit in the generated output.

Projection language MUST remain within the evidence boundary established
by qualification.


FR-14 — Independent Validation

Validation MUST independently verify production qualification claims
against canonical evidence.

Validation MUST NOT merely verify that the proposal agrees with the
qualification artifact.

A qualification claim of verified production MUST fail validation unless
canonical evidence independently establishes:

- matching organisation identity;
- matching project/system identity;
- explicit production environment;
- explicit production verification;
- compatible candidate implementation responsibility.

A validation failure MUST prevent the affected projection from reaching
the human submission boundary.


FR-15 — Cross-Organisation Isolation

The system MUST enforce organisation boundaries when evaluating
organisation-specific experience.

Example:

Requirement:
Production multi-agent implementation at Organisation A.

Evidence:
- Organisation A prototype work;
- Organisation B production work;
- personal CAS production-like work.

The result MUST NOT be treated as verified production experience at
Organisation A.

No cross-organisation evidence pooling may upgrade the requirement.


FR-16 — Cross-Project Isolation

The system MUST enforce project/system boundaries when evidence is
organisation-bound and project-specific.

Example:

Organisation A:
- Project X was explicitly production;
- Project Y has implementation evidence but unknown deployment.

Evidence from Project X MUST NOT be used to establish production status
for Project Y.


FR-17 — Personal Project Isolation

Personal project evidence MAY demonstrate technical capability or
transferable experience.

It MUST NOT satisfy a requirement explicitly requiring production
implementation inside a real operating company.

Personal-project evidence MUST NOT upgrade an employer/project evidence
card from unknown or non-production to verified production.


FR-18 — Evidence Traceability

Every material production qualification claim MUST be traceable to one or
more canonical evidence records.

Traceability MUST identify:

- the evidence record(s);
- the relevant organisation;
- the relevant project/system;
- the facts supporting production status;
- the facts supporting implementation responsibility.

Traceability is an internal governance mechanism and MUST NOT leak
internal provenance syntax into client-facing proposal prose unless
explicitly required.


FR-19 — No Unsupported Quantitative Claims

The qualification/projection system MUST NOT invent or infer candidate
business outcomes, staffing reductions, throughput improvements,
agent counts, reliability thresholds, or performance metrics.

Quantitative claims MUST be traceable to canonical evidence or explicitly
identified as proposed future targets/architecture recommendations.

A proposed target MUST NOT be represented as a historical result.


FR-20 — Screening Answer Integrity

Screening answers MUST distinguish:

- verified candidate experience;
- proposed architecture/approach;
- unresolved conditions.

Answers to factual experience questions MUST NOT use future architecture
recommendations as evidence of past implementation.

For example, recommending Temporal, MCP, Redis, Supabase, or LangGraph for
a client's future architecture does not establish that the candidate
previously implemented those technologies in production.


FR-21 — Work Sample Integrity

Recommended work samples MUST respect the same evidence boundary.

A work sample may demonstrate:

- production experience, when explicitly evidenced;
- non-production/prototype experience;
- transferable technical capability.

The description MUST NOT upgrade prototype, personal, innovation, or
research work into production experience.

Work samples must remain consistent with the qualification decision.


FR-22 — Determinism and Idempotence

Given identical canonical evidence, opportunity requirements, and
qualification configuration, qualification MUST produce the same decision
and materially equivalent machine-readable result.

Repeated execution MUST NOT progressively strengthen evidence or introduce
new production claims.


FR-23 — Regression Protection

The system MUST include regression coverage for at least the following
scenarios:

1. WPP employment + WPP prototype evidence
   → production remains unknown/non-production and cannot satisfy an
   explicit production dealbreaker.

2. WPP employment + explicitly verified WPP production evidence +
   compatible implementation responsibility
   → production implementation requirement may be satisfied.

3. WPP prototype evidence + personal-project production evidence
   → personal evidence does not upgrade WPP production status.

4. Repository name containing "production" with no explicit production
   attestation
   → production remains unknown.

5. Company A requirement + Company A evidence + Company B production
   evidence
   → Company B evidence cannot satisfy Company A requirement.

6. Same organisation, different project
   → production evidence from one project cannot satisfy another
   project-specific requirement.

7. Production evidence with advisor/evaluator role only
   → does not satisfy a personal implementation requirement.

8. Qualification artifact claiming verified production without canonical
   production evidence
   → validation MUST fail.

9. Conditional qualification
   → unresolved production condition remains visible and cannot become
   an implicit positive claim during projection.

10. DO NOT APPLY qualification
    → no submission-ready proposal is generated.


ACCEPTANCE CRITERIA

AC-01
Given an explicit production dealbreaker and only prototype/personal/unknown
evidence, the final qualification decision is DO NOT APPLY.

AC-02
Given explicit canonical production evidence for the target organisation
and project plus compatible implementation responsibility, the production
experience requirement can be satisfied.

AC-03
Employment records alone can never establish production implementation
experience.

AC-04
Repository names, filenames, folder names, or production-like wording
cannot establish production verification.

AC-05
Evaluation metrics cannot establish production verification.

AC-06
Personal-project evidence cannot satisfy an employer-specific production
requirement.

AC-07
Evidence from another organisation cannot satisfy a target-organisation
production requirement.

AC-08
Evidence from another project cannot satisfy a project-specific production
requirement.

AC-09
Advisor/evaluator-only responsibility cannot satisfy a personal
implementation requirement.

AC-10
Qualification cannot upgrade canonical evidence.

AC-11
Projection cannot upgrade qualification.

AC-12
Validation independently detects a qualification claim of verified
production that lacks matching canonical evidence.

AC-13
All material production claims are traceable to canonical evidence.

AC-14
Unsupported historical metrics, agent counts, business outcomes, or
staffing claims are rejected or remain explicitly identified as proposed
targets rather than historical facts.

AC-15
The current Senior Agentic AI Architect opportunity becomes DO NOT APPLY
unless canonical evidence explicitly establishes the required real-company
production implementation experience.

AC-16
The resulting implementation preserves the existing Knowledge,
Runtime, Coaching, Projection architecture and treats Validation as a
cross-cutting quality gate.

AC-17
Repeated execution with identical inputs is deterministic and does not
accumulate or strengthen evidence.

AC-18
The regression scenarios above are represented in automated tests and
prevent recurrence of the original false-positive qualification.


ARCHITECTURAL INVARIANTS

The resulting implementation MUST preserve these invariants:

1. Canonical evidence is authoritative for factual experience claims.

2. Qualification evaluates evidence; it does not manufacture evidence.

3. Projection communicates qualification; it does not strengthen it.

4. Validation independently checks critical qualification claims.

5. Employment is not equivalent to production deployment.

6. Production deployment is not equivalent to personal implementation.

7. Personal projects are not equivalent to real-company production
   experience.

8. Evidence composition is bounded by organisation and project/system
   identity.

9. UNKNOWN is never silently promoted to VERIFIED_PRODUCTION.

10. Explicit client dealbreakers override optimistic interpretation.

11. Client-facing prose must remain inside the canonical evidence boundary.

12. Validation is cross-cutting and is not a fifth architectural layer.

13. Human review remains the final boundary before submission.
