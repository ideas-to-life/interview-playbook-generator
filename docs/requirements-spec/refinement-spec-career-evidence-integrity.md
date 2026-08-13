Refinement: Career History Evidence Integrity

Priority: P0 — Evidence Integrity
Scope: Knowledge → Projection → Validation
Primary defect: Projection layer fabricates, alters, infers or reconstructs employment dates and job titles.

⸻

1. Objective

Ensure that all factual employment-history metadata in generated career-projection artefacts is strictly derived from canonical evidence.

The generator may tailor the presentation and relevance of a career history to a target opportunity, but it MUST NOT alter, infer, normalise, approximate, reconstruct, split, merge or fabricate employment-history facts.

The following fields are considered factual evidence:

* Employer
* Employment period
* Start date
* End date
* Job title
* Employment status
* Location, where explicitly evidenced

The core principle is:

Career history is evidence, not projection.

⸻

2. Defect Being Addressed

The latest Head of Enterprise Architecture run demonstrated a material evidence-integrity failure.

Canonical evidence contains:

WPP Media
Senior Director, Agentic AI Systems Architecture
Dec 2025 – Present
BBC Studios
Lead Enterprise Architect
Nov 2021 – Nov 2025
British American Tobacco
Enterprise Architect & Global Solution Architect
2011 – 2021

The generated projection instead produced:

WPP Media
Enterprise Architect & AI Practice Lead
2022 – Present
BBC Studios
Principal Enterprise Cloud Architect
2020 – 2022
British American Tobacco R&D
Head of Enterprise Architecture & Systems
2016 – 2020

The investigation established:

Original Evidence       → Correct
Canonical Knowledge     → Correct
Projection Strategy     → Not responsible
Projection Rendering    → First evidence violation

The projection layer therefore appears to have reconstructed a plausible career chronology rather than rendering the evidenced chronology.

⸻

3. Governing Principle

Add the following permanent governance rule:

Employer names, employment dates, job titles and other explicitly evidenced career-history facts are immutable evidence. Projection may change emphasis and wording around those facts, but must never change the facts themselves.

Add:

When employment metadata is unavailable, ambiguous or conflicting, the generator MUST preserve the ambiguity or defer to the authoritative canonical source. It MUST NOT infer or estimate a value.

⸻

4. Canonical Employment Record

The Knowledge Layer MUST expose an authoritative employment-record representation.

Conceptually:

employment_record:
  employer: "WPP Media"
  title: "Senior Director, Agentic AI Systems Architecture"
  start_date: "2025-12"
  end_date: null
  status: "current"
  location: "London, UK"
  evidence_source: "cv-2026"

The implementation MUST use the existing project schema where one already exists rather than introducing a duplicate model unnecessarily.

The important requirement is that the projection layer has access to structured authoritative employment metadata.

⸻

5. Field Authority

Define an explicit authority hierarchy for employment facts.

Recommended precedence:

1. Canonical employment record
2. Canonical source evidence
3. Original source document
4. Derived knowledge representations
5. Target JD
6. Projection inference

The final two sources MUST NEVER be authoritative for candidate employment facts.

In particular:

A target JD can influence positioning, but can never influence candidate employment metadata.

⸻

6. Immutable Fields

The following fields MUST be treated as immutable during projection.

Employer

Must not be renamed, embellished or substituted.

Example:

WPP Media

must not become:

WPP
WPP Group
WPP Media Enterprise Technology

unless the canonical record explicitly supports that representation.

Job Title

Must not be replaced with a target-aligned title.

Example:

Senior Director, Agentic AI Systems Architecture

must not become:

Enterprise Architect & AI Practice Lead

simply because that title better matches the target position.

Start Date

Must be rendered from canonical evidence.

End Date

Must be rendered from canonical evidence.

Employment Status

Current/former status must be evidence-derived.

Location

Where included, location must be evidence-derived.

⸻

7. Projection Permitted Transformations

The projection layer MAY transform:

* achievement selection;
* bullet ordering;
* achievement wording;
* terminology;
* summary emphasis;
* capability framing;
* relevance;
* ATS vocabulary;
* presentation format.

Example:

Canonical achievement:

Led architecture governance across global business units.

Target-oriented rendering:

Led enterprise architecture governance across a complex global matrixed environment.

This is permissible if evidence remains within established claim-strength boundaries.

However:

Employment metadata

must remain unchanged.

⸻

8. Prohibited Employment Transformations

The projection layer MUST NOT:

Fabricate dates

2022 – Present

when evidence says:

Dec 2025 – Present

Approximate dates

2025 – Present

when only Dec 2025 – Present is evidenced, unless the canonical rendering policy explicitly permits month-to-year formatting.

Reconstruct contiguous chronology

The model must not infer:

2022 – 2025

because another role begins in 2022.

Backfill missing dates

If a start date is unavailable, do not infer it from neighbouring roles.

Change job titles to improve fit

Do not convert:

Senior Director, Agentic AI Systems Architecture

to:

Enterprise Architect & AI Practice Lead

without explicit canonical evidence supporting that title.

Split employment records

Do not turn one evidenced employment period into multiple jobs merely because the candidate performed different functions.

Merge employment records

Do not collapse distinct evidenced roles into one employment period.

Infer employment from projects

A project associated with an employer does not automatically create a separate employment record.

⸻

9. Employment vs Experience Cluster

The implementation MUST explicitly distinguish:

Employment Record

from:

Experience / Achievement / Capability Cluster

For example:

BAT
2011–2021

may contain:

* R&D architecture;
* global SAP architecture;
* integration;
* data governance;
* regional architecture.

Those experiences do not automatically justify:

BAT R&D
2016–2020
BAT Global
2012–2016

unless the canonical evidence explicitly identifies those as separate employment records.

⸻

10. Projection Contract

Update the projection contract with a hard rule:

Professional Experience records MUST be rendered from canonical employment records. The projection model MUST NOT generate employment dates or titles from contextual reasoning.

The rendering pipeline should conceptually become:

Canonical Employment Records
          ↓
Target Relevance Selection
          ↓
Achievement Selection
          ↓
Presentation Rendering
          ↓
Validation

NOT:

Target JD
    ↓
LLM Career Reconstruction
    ↓
Professional Experience

⸻

11. Target JD Isolation

The target opportunity MUST NOT be able to modify:

* employer;
* title;
* start date;
* end date;
* employment status.

The JD MAY influence:

* which roles are emphasised;
* which achievements are selected;
* which capabilities are surfaced;
* which terminology is used in achievement descriptions.

This distinction MUST be explicit in the implementation.

⸻

12. Deterministic Rendering Where Practical

Employment metadata should preferably be rendered deterministically.

For example:

canonical_employment_record
        ↓
template renderer
        ↓
Employer — Title | Location (Dates)

The LLM should ideally generate the achievement content, not the employment metadata.

This reduces unnecessary generative freedom around factual information.

⸻

13. Deterministic Validation

Introduce an employment-history validation control.

For every generated professional-experience record:

Generated Employer
Generated Title
Generated Start
Generated End
Generated Status

must be compared with:

Canonical Employer
Canonical Title
Canonical Start
Canonical End
Canonical Status

The validator should produce explicit results such as:

employment_validation:
  status: "PASS"
  records_checked: 4
  field_checks: 20
  violations: []

⸻

14. Hard Failure Conditions

Validation MUST fail if the generated projection:

* introduces an unsupported employer;
* introduces an unsupported employment period;
* changes an evidenced start date;
* changes an evidenced end date;
* changes employment status;
* changes an evidenced job title without an approved canonical alias;
* creates an employment record absent from canonical evidence;
* splits one employment record into multiple unsupported records;
* merges distinct employment records without an approved canonical rule.

These are evidence-integrity failures, not merely quality warnings.

⸻

15. Title Alias Policy

There may be legitimate cases where a canonical title has an approved short-form representation.

For example:

Senior Director, Agentic AI Systems Architecture

could potentially render as:

Senior Director, Agentic AI Systems Architecture

or another explicitly approved canonical alias.

If title aliases are required, they MUST be:

* deterministic;
* explicitly defined;
* evidence-preserving;
* reusable across projections.

The LLM MUST NOT invent title aliases dynamically.

⸻

16. Date Rendering Policy

Define one deterministic date-rendering policy.

For example:

Canonical: Dec 2025 – Present
Allowed:
Dec 2025 – Present
December 2025 – Present
Not allowed:
2025 – Present
2022 – Present

If the project intentionally uses year-only CV dates, that transformation should be implemented as a deterministic display-format rule, not inferred by the LLM.

For example:

Canonical:
Dec 2025 – Present
Display format:
2025 – Present

would be permissible only if the canonical rendering policy explicitly defines this transformation.

The critical distinction is:

Formatting may change; factual values may not.

⸻

17. Missing or Conflicting Evidence

If canonical evidence contains:

start_date: unknown

the generator MUST NOT infer the date.

It should either:

* omit the date;
* use an approved uncertainty representation;
* or surface the ambiguity for review.

If two authoritative sources conflict, the generator MUST NOT silently select one.

It should surface:

Employment metadata conflict detected.
Human resolution required.

⸻

18. Downstream Artefact Propagation

Validated employment records MUST be reused consistently across all relevant projection artefacts.

At minimum:

* Executive CV
* ATS CV
* Recruiter CV
* Cover Letter
* LinkedIn Profile
* Executive Brief
* Interview Playbook
* Interview Cheatsheet
* Opportunity Alignment, where employment history is displayed

The system must avoid allowing each artefact renderer to independently reconstruct career history.

Recommended pattern:

Canonical Employment Records
          ↓
Validated Employment View
          ↓
All Projection Artefacts

⸻

19. Regression Test — Head of Enterprise Architecture

Use the current failed run as the mandatory regression case.

Canonical evidence

WPP Media
Senior Director, Agentic AI Systems Architecture
Dec 2025 – Present
BBC Studios
Lead Enterprise Architect
Nov 2021 – Nov 2025
British American Tobacco
Enterprise Architect & Global Solution Architect
2011 – 2021

Required output

The generated projection MUST preserve these factual employment records.

It MUST NOT generate:

WPP Media — 2022–Present
BBC Studios — 2020–2022
BAT R&D — 2016–2020
BAT Global — 2012–2016

unless those exact records are independently supported by canonical employment evidence.

⸻

20. Regression Assertions

Add deterministic assertions for:

WPP start == Dec 2025
WPP end == Present
BBC start == Nov 2021
BBC end == Nov 2025
BAT employment period == canonical period

Also assert that generated titles correspond to canonical records or approved aliases.

The regression should inspect all generated artefacts, not only resume-executive.md.

⸻

21. Existing Golden Tests

Update or add golden test coverage to ensure that:

* employment dates remain stable;
* titles remain stable;
* employer names remain stable;
* target-role terminology cannot replace employment metadata;
* multiple artefacts receive identical employment metadata.

The current golden resume should be reviewed because a golden fixture containing fabricated dates would otherwise institutionalise the defect.

⸻

22. Interaction With Existing Evidence Controls

This refinement MUST integrate with the existing controls:

Identity Protection

Prevents target roles from redefining the candidate’s professional identity.

Claim Strength & Evidence Scope

Prevents achievement claims from exceeding evidence.

Projection Strategy Evidence Boundary

Prevents target capabilities from becoming unsupported candidate capabilities.

New Career History Evidence Integrity

Prevents employment facts from being altered.

The resulting control architecture becomes:

Canonical Evidence
        ↓
Identity Protection
        ↓
Employment Evidence Integrity
        ↓
Capability Evidence Mapping
        ↓
Projection Strategy Boundary
        ↓
Claim Strength / Evidence Scope
        ↓
Projection
        ↓
Deterministic Validation
        ↓
Final Artefacts

⸻

23. Acceptance Criteria

Implementation is complete when:

* Canonical employment records are explicitly identifiable.
* Employer, title and employment dates are treated as immutable evidence.
* Projection cannot infer employment dates.
* Projection cannot reconstruct contiguous career periods.
* Projection cannot alter job titles to improve target alignment.
* Projection cannot create unsupported employment records.
* Projection cannot split or merge employment records without explicit evidence.
* Employment records are distinguished from experience/capability clusters.
* Target JDs cannot influence employment metadata.
* Date rendering is deterministic.
* Any approved title aliases are explicit and evidence-bound.
* Missing dates are never inferred.
* Conflicting employment evidence is surfaced rather than silently resolved.
* A deterministic employment metadata validator is implemented.
* Employment validation is a hard evidence-integrity gate.
* All major projection artefacts use validated employment records.
* The Head of Enterprise Architecture regression test passes.
* The fabricated 2022/2020/2016 chronology cannot reappear.
* Existing Claim Strength and Projection Strategy validation remains intact.
* All existing tests continue to pass.
* No candidate-specific hard-coded date exceptions are introduced.

⸻

24. Required Regression Outcome

For the Head of Enterprise Architecture test, the system should be able to produce a CV whose positioning is tailored to the target role while the career history remains factually unchanged.

In particular:

The generator may decide that Alexandre’s WPP experience is highly relevant to the Head of Enterprise Architecture role. It may select the most relevant WPP achievements and change their presentation. It may not decide that Alexandre worked at WPP from 2022 simply because that makes the generated career chronology look more plausible.

That is the fundamental invariant this refinement must establish.

Governing principle

The generator may project relevance; it may not project history.
