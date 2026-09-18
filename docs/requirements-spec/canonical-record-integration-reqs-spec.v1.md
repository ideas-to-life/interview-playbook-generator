# Interview Playbook Generator
## Canonical Career Record Integration — Requirement Specification

**Status:** Proposed  
**Purpose:** Stabilise factual accuracy and prevent recurrence of known `mind-palace` data-quality problems  
**Scope:** Interview Playbook Generator only  
**Target canonical source:** `mind-palace/canonical/career-record.yaml`

---

# 1. Purpose

The interview-playbook-generator currently consumes professional information from the `mind-palace` knowledge repository to generate outputs such as CVs, interview preparation material, proposals and related professional projections.

The forensic review of `mind-palace` identified a fundamental data-governance problem:

- primary evidence and derived content are mixed;
- conflicting professional facts can coexist;
- AI-generated content can be re-ingested as though it were source knowledge;
- generated outputs can therefore repeat or amplify incorrect titles, qualifications, dates and career history.

A controlled canonical career record has now been established at:

`mind-palace/canonical/career-record.yaml`

The generator must now recognise this record as the **highest-authority professional facts source**.

The objective of this change is not to redesign the generator or implement the complete future provenance architecture.

The immediate objective is:

> Ensure that generated professional outputs use verified canonical career facts consistently and cannot override them with conflicting, derived, quarantined or inferred information.

---

# 2. Scope

## 2.1 In scope

The change shall cover:

1. Discovery and loading of the canonical career record.
2. Authority rules for professional facts.
3. Exclusion of quarantined content from factual sourcing.
4. Conflict resolution between canonical and derived content.
5. Protection against title inflation.
6. Protection against unsupported qualifications, dates and employers.
7. Treatment of unresolved canonical questions.
8. Controlled use of derived knowledge for contextual enrichment.
9. Separation between factual selection and projection/writing.
10. Regression tests covering the known forensic failure cases.
11. Validation that existing generator outputs remain useful while becoming factually safer.

## 2.2 Out of scope

The following shall NOT be implemented as part of this change:

- complete evidence-card architecture;
- full claim-level provenance tracking;
- automatic reconstruction of the canonical record;
- automatic modification of `career-record.yaml`;
- LLM-based reconciliation of contradictory facts;
- repository-wide `mind-palace` restructuring;
- migration of all existing knowledge into the canonical model;
- regeneration of all existing CVs, proposals or website content;
- changes to the OKF format unless required to consume canonical facts;
- replacement of the existing generation workflow;
- introduction of a new application or database layer.

The canonical record remains a **knowledge artefact consumed by the generator**, not an application database.

---

# 3. Target Architecture

The generator shall recognise the following conceptual hierarchy:

    mind-palace/
    ├── canonical/
    │   └── career-record.yaml       ← authoritative professional facts
    │
    ├── knowledge/                   ← contextual knowledge / thinking
    │
    ├── quarantine/                 ← excluded from factual sourcing
    │
    └── derived-content       ← secondary / projection material


The effective information flow shall be:

    CANONICAL FACTS
          │
          ▼
    FACT SELECTION / VALIDATION
          │
          ├───────────────┐
          ▼               ▼
    CONTEXTUAL        GENERATION
    KNOWLEDGE            │
          │               ▼
          └──────────► OUTPUT
                         │
                         ▼
                    CV / Proposal /
                    Interview Playbook /
                    Other Projection

Generated outputs must NOT flow back into the canonical factual layer through this generator.

---

# 4. Source Authority Model

The generator shall implement an explicit source precedence model.

## 4.1 Authority order

For professional facts, authority shall be:

1. `mind-palace/canonical/career-record.yaml`
2. Other explicitly designated authoritative source data, where still required by the existing generator
3. Existing trusted knowledge content
4. Derived / narrative content
5. AI-generated content
6. LLM inference

For facts represented in the canonical career record, level 1 is authoritative.

The generator must NOT use a lower-level source to override a canonical fact.

---

# 5. Canonical Career Record

## 5.1 Discovery

The generator shall locate:

`mind-palace/canonical/career-record.yaml`

using the repository structure/configuration already available to the generator.

The path should not be hard-coded in multiple independent components.

If the generator has an existing configuration mechanism for knowledge sources, the canonical path should be represented there once.

## 5.2 Loading

The canonical record must be parsed as structured YAML.

Failure to load or parse the canonical record shall be treated as a configuration/data error, not silently ignored.

The generator must not silently fall back to conflicting derived career information if the canonical record is unavailable.

## 5.3 Read-only behaviour

The generator shall treat the canonical record as read-only.

Generation must never:

- modify it;
- append generated claims to it;
- update it from LLM output;
- "correct" it automatically;
- replace it with generated content.

Any future change to the canonical record remains a separate human-controlled knowledge-management activity.

---

# 6. Canonical Fact Selection

The generator must distinguish between:

- **facts**
- **context**
- **interpretation**
- **generated language**

The canonical record provides facts.

Generated outputs may transform the presentation of those facts, but may not change their underlying meaning.

For example:

Canonical:

    title:
      formal: "Lead Enterprise Architect - Technology Transformation Group"

Generated CV wording may reasonably become:

    Lead Enterprise Architect, Technology Transformation Group

But it must NOT become:

    Head of Enterprise Architecture

unless that title is explicitly present as a formal canonical title.

---

# 7. Formal Title vs Scope

This is a mandatory requirement.

The generator must distinguish:

- `formal_title`
- `responsibilities_scope`
- `operational_scope`
- `acting / additional responsibilities`

Where a canonical career entry records an operational or acting scope that differs from the formal employment title, the generator must preserve that distinction.

Example:

Formal title:

    Lead Enterprise Architect - Technology Transformation Group

Operational context:

    Took forward activities previously performed by the Head of Architecture after the position became vacant.

Allowed output:

    Lead Enterprise Architect with responsibility for activities previously performed by the Head of Architecture.

Not allowed:

    Head of Enterprise Architecture

unless explicitly established as the formal title in the canonical record.

This rule exists specifically to prevent title inflation through summarisation.

---

# 8. Education and Qualifications

Education and qualification information shall be treated as high-sensitivity factual claims.

The generator must use canonical education and certification records when available.

It must not:

- upgrade a Bachelor's degree to a Master's degree;
- invent a degree type;
- substitute an institution;
- infer a qualification from a field of study;
- combine separate qualifications into a more senior qualification;
- introduce a qualification found only in derived or AI-generated content.

The canonical record currently establishes the authoritative education history, including the correction of the previously conflicting MSc / Federal University of Rio de Janeiro claim.

Therefore any generated output claiming an MSc from the Federal University of Rio de Janeiro would constitute a generator defect.

---

# 9. Career Chronology

The generator must use the canonical career chronology when producing:

- CVs;
- career summaries;
- interview preparation;
- professional biographies;
- proposals;
- role-specific experience sections;
- other professional projections.

The generator must not silently reconstruct career chronology from secondary documents when a canonical career record exists.

The complete chronology should be available for selection, but the generator should continue to select only relevant experience for the requested output.

The requirement is:

> Canonicalisation controls factual accuracy; it does not require every generated output to reproduce the complete career history.

---

# 10. Dates

Employment dates represented in the canonical record shall be authoritative.

The generator must not:

- shorten an employment period because a secondary source is incomplete;
- extend an employment period without canonical support;
- infer missing months;
- merge separate roles into a different period;
- manufacture dates to make chronology appear cleaner.

Where the canonical record contains a resolved date, that date shall take precedence over conflicting derived content.

---

# 11. Employer Identity

Employer and engagement relationships must be preserved according to the canonical record.

The generator must distinguish, where applicable:

- direct employment;
- consultancy / contracting;
- independent advisory work;
- concurrent engagements.

For example, the Compugraf / Souza Cruz relationship must not be generated as two unrelated concurrent employers where the canonical record establishes Compugraf as the external consultancy through which work was contracted to Souza Cruz.

Similarly, WPP Media direct employment and subsequent Mostelli activity must not be merged into a single engagement.

---

# 12. Location

Locations may be used when relevant to an output, but must be sourced from canonical records where present.

The generator must not infer:

- relocation dates;
- office locations;
- employment locations;
- international assignments

from narrative context where the canonical record provides a different fact.

---

# 13. Unresolved Questions

The canonical record contains an `unresolved_questions` section.

The generator must distinguish:

- `current_status: resolved`
- genuinely unresolved items.

Resolved items may be treated as established canonical facts.

Genuinely unresolved items must NOT be presented as factual claims.

The generator must not resolve an unresolved question by inference.

For example:

    unresolved ≠ probable
    unresolved ≠ likely
    unresolved ≠ inferred from another document

If an output requires the information, the generator should either:

1. omit the claim; or
2. explicitly flag the information as requiring confirmation, where appropriate to the output.

---

# 14. Quarantine Rules

The `mind-palace/quarantine/` directory is explicitly excluded from factual sourcing.

The generator must not use quarantined content as an authoritative source for:

- titles;
- employers;
- dates;
- qualifications;
- achievements;
- responsibilities;
- career chronology;
- professional identity.

Quarantined material may exist for forensic/reference purposes but is not part of the active knowledge authority chain.

If existing discovery/indexing mechanisms currently include quarantine content, the generator must filter it out.

This exclusion must be enforced rather than relying on prompts to tell the LLM not to use it.

---

# 15. Derived and AI-Generated Content

Existing derived content remains potentially useful.

The generator may use derived knowledge for:

- contextual understanding;
- terminology;
- methods;
- domain framing;
- examples;
- narrative context;
- identifying potentially relevant experience.

However, derived content must not become authoritative for canonical career facts.

In particular:

> AI-generated content may provide context, but it cannot establish a professional fact that is absent from or contradictory to the canonical record.

The generator must not assume that a statement is factual merely because it appears in an existing generated document.

---

# 16. No-Inference Rule for Professional Facts

The generator must not infer factual professional claims from indirect evidence.

Examples of prohibited inference:

- inferring a Master's degree from postgraduate study;
- inferring "Head of Architecture" from acting responsibilities;
- inferring employment dates from project dates;
- inferring an employer from a client relationship;
- inferring a formal job title from responsibilities;
- inferring a certification from experience;
- inferring a leadership title from participation in leadership activities.

Generated language may be concise or persuasive, but the underlying factual claim must be supported by the canonical record or another explicitly authoritative source.

---

# 17. Canonical Override Behaviour

When a conflict exists between canonical and derived content, the generator must apply:

    canonical fact
        >
    derived fact

Example:

    Derived:
    "Head of Enterprise Architecture & Digital Evolution"

    Canonical:
    "Lead Enterprise Architect - Technology Transformation Group"

Generated output must use the canonical formal title.

If useful, the generated output may describe the additional operational scope separately.

It must not combine the two into a new title.

---

# 18. Relevance and Tailoring

The canonical record contains the complete career history.

The generator must continue to tailor outputs to the target opportunity.

It must therefore perform two separate activities:

### Activity A — factual selection

Determine which canonical facts are relevant to the target role.

### Activity B — projection

Transform those selected facts into the requested CV, proposal, interview answer, etc.

These activities must not be conflated.

The LLM may choose emphasis and wording.

The LLM may not choose or invent alternative professional facts.

---

# 19. Achievement and Responsibility Claims

Canonical responsibilities and achievements may be used as source material.

However, generated wording must not strengthen a claim beyond the evidence represented in the canonical record.

For example, wording should not transform:

    "supported architecture governance"

into:

    "established the enterprise-wide architecture governance function"

unless the latter is explicitly supported.

Similarly, a responsibility should not automatically become:

- ownership;
- leadership;
- transformation;
- enterprise-wide responsibility;
- strategic authority;
- measurable business impact

without supporting evidence.

This is particularly important because previous generated outputs introduced inflated language such as "visionary", "pioneering", "mission-critical", etc.

The generator must favour factual precision over rhetorical amplification.

---

# 20. Generated Language

The generator may improve:

- grammar;
- clarity;
- conciseness;
- structure;
- relevance;
- readability;
- professional presentation.

It must not improve a factual claim by making it more senior, more extensive or more impressive than its source supports.

Preferred transformation:

    canonical fact
        ↓
    concise, relevant professional wording

Not:

    canonical fact
        ↓
    amplified marketing claim

---

# 21. Provenance — Transitional Requirement

Full claim-level evidence cards are out of scope.

However, the generator should preserve enough internal information to make debugging possible.

Where practical, generated factual selections should retain an internal reference to the canonical career entry used.

For example:

    CAR-03
    CAR-04
    EDU-01
    CERT-01

This information does not necessarily need to appear in the user-facing output.

The purpose is to allow future provenance architecture to be introduced without redesigning the factual-selection boundary.

If the current architecture makes this impractical, do not introduce a large new framework solely for this purpose. Record the limitation and keep the canonical-selection boundary clean.

---

# 22. OKF Integration

The generator currently experimentally generates and consumes OKF.

The canonical career record should become the authoritative source for professional facts consumed by the generator's OKF-based workflows.

The change must not require a redesign of OKF unless the existing schema prevents canonical facts from being represented correctly.

If OKF contains professional facts that conflict with the canonical record:

    canonical career record wins.

If an OKF field cannot represent the distinction between formal title and operational scope, the implementation should preserve the distinction through the smallest appropriate change rather than collapsing the two concepts.

---

# 23. Generator Prompt / Instruction Changes

Existing generator instructions should be updated to explicitly establish:

1. Canonical career record authority.
2. Quarantine exclusion.
3. No inference for professional facts.
4. Formal-title preservation.
5. Canonical chronology precedence.
6. Canonical education/certification precedence.
7. Separation of fact selection from narrative generation.
8. Derived-content limitations.

These rules should be expressed at the appropriate architectural layer.

They should NOT exist solely as prose in one individual generation prompt if the generator has a reusable source-selection or context-building layer.

The implementation should enforce the strongest rules structurally where feasible.

---

# 24. Validation Requirements

The implementation must validate that:

### V01 — Canonical record is discovered

The generator can locate and load:

`mind-palace/canonical/career-record.yaml`

### V02 — YAML is valid

Malformed canonical YAML produces a clear error.

### V03 — Canonical facts are accessible

Career entries, education, certifications and relevant metadata can be selected.

### V04 — Quarantine is excluded

Quarantined content cannot become a factual source.

### V05 — Canonical overrides derived content

Conflicting secondary information does not override canonical facts.

### V06 — Title inflation is prevented

Formal titles remain faithful to the canonical record.

### V07 — Education inflation is prevented

Bachelor's degrees cannot become Master's degrees.

### V08 — Chronology is protected

Canonical dates override conflicting derived dates.

### V09 — Employer relationships are protected

Consultancy, employment and independent work are not incorrectly merged.

### V10 — Unresolved facts are not invented

The generator does not resolve uncertainty through inference.

### V11 — Relevance still works

The generator can select appropriate experience rather than dumping the complete career history into every output.

### V12 — Output quality is preserved

The change must not materially degrade the usefulness, relevance or readability of generated CVs, proposals or interview preparation.

---

# 25. Mandatory Regression Scenarios

The following scenarios must be included in regression testing because they correspond to known forensic findings.

## Scenario 1 — Education

Input conflict:

    Derived content:
    MSc, Federal University of Rio de Janeiro

    Canonical:
    BSc Computer Science,
    Universidade de Mogi das Cruzes

Expected:

    BSc Computer Science,
    Universidade de Mogi das Cruzes

The MSc / Federal University claim must not appear.

---

## Scenario 2 — BBC Formal Title

Input conflict:

    Derived:
    Head of Enterprise Architecture & Digital Evolution

    Canonical:
    Lead Enterprise Architect -
    Technology Transformation Group

Expected:

    Lead Enterprise Architect -
    Technology Transformation Group

Additional acting/operational scope may be described separately if relevant.

---

## Scenario 3 — BBC Acting Scope

Canonical information includes operational responsibility previously performed by the Head of Architecture.

Expected:

The generator may communicate the scope.

It must not convert that scope into a formal Head of Architecture title.

---

## Scenario 4 — BAT Chronology

Derived content contains an incomplete BAT history.

Canonical record contains the complete chronology.

Expected:

The generator uses the canonical chronology when constructing career history.

---

## Scenario 5 — Compugraf / Souza Cruz

Canonical record establishes Compugraf as an external consultancy through which work was contracted to Souza Cruz.

Expected:

The generator does not represent these as contradictory simultaneous direct employers.

---

## Scenario 6 — WPP / Mostelli

Canonical record establishes:

- WPP Media as direct corporate employment;
- Mostelli as subsequent independent advisory activity.

Expected:

The generator preserves the distinction.

---

## Scenario 7 — Quarantine

Place a conflicting professional claim in `mind-palace/quarantine/`.

Expected:

The generator ignores it as a factual source.

---

## Scenario 8 — Unsupported Enhancement

Canonical:

    "Contributed to architecture governance"

Generated attempt:

    "Established and led the enterprise architecture governance function"

Expected:

The stronger claim is rejected or rewritten to remain within the canonical evidence boundary.

---

# 26. Error Handling

The generator must fail safely.

It must not silently substitute lower-authority data when:

- canonical YAML is malformed;
- canonical record cannot be parsed;
- required canonical data is unavailable;
- a requested factual claim cannot be established.

Errors should be explicit enough to identify the source/configuration problem.

The generator should prefer omission over fabrication.

---

# 27. Backward Compatibility

Existing generation workflows should continue to operate unless they explicitly depend on incorrect or conflicting professional facts.

The implementation should minimise changes to:

- existing generator interfaces;
- OKF contracts;
- output formats;
- prompt invocation mechanisms;
- unrelated skills;
- unrelated generators.

The goal is to introduce a stronger factual authority boundary, not to redesign the entire system.

---

# 28. Non-Functional Requirements

## NFR01 — Determinism

Canonical factual selection should be deterministic where practical.

Given the same canonical record and target requirements, factual source selection should not vary merely because the LLM generated a different interpretation.

## NFR02 — Traceability

The implementation should make it possible to determine which canonical career entries informed factual output.

## NFR03 — Maintainability

The authority model should be implemented once and reused rather than duplicated across individual prompts.

## NFR04 — Safety against regression

Future derived content must not silently regain authority over canonical facts.

## NFR05 — Minimal architectural change

Do not introduce infrastructure that is not required to satisfy this requirement.

---

# 29. Acceptance Criteria

The change is complete when all of the following are true:

- [ ] `career-record.yaml` is recognised as the authoritative professional-facts source.
- [ ] The canonical record is loaded successfully by the generator.
- [ ] Quarantine content is excluded from factual sourcing.
- [ ] Canonical facts override conflicting derived content.
- [ ] Formal job titles cannot be inflated from operational scope.
- [ ] Education and certification claims cannot be upgraded or invented.
- [ ] Canonical career dates are authoritative.
- [ ] Employer relationships are preserved.
- [ ] Unresolved questions cannot become factual claims.
- [ ] Generated wording does not materially amplify canonical claims.
- [ ] Relevant career history can still be selected for the target opportunity.
- [ ] Existing output structure remains functional.
- [ ] Regression tests cover all known forensic failure cases.
- [ ] No generator-generated content is written back into the canonical record.
- [ ] No changes are made to unrelated components without a demonstrated dependency.
- [ ] Test results demonstrate that the known factual regressions no longer occur.

---

# 30. Implementation Principle

The central architectural rule for this change is:

> **The generator is allowed to select, transform and present canonical facts. It is not allowed to redefine them.**

This creates the required boundary between:

    TRUTH
      │
      ▼
    SELECTION
      │
      ▼
    PROJECTION

rather than allowing:

    TRUTH
      ↕
    DERIVED KNOWLEDGE
      ↕
    GENERATED OUTPUT

The latter is the feedback loop that contributed to the original data-quality problem and must not be recreated.

---

# 31. Definition of Done

The implementation should be considered complete only after:

1. The source hierarchy has been implemented.
2. Canonical loading has been implemented.
3. Quarantine exclusion has been implemented.
4. Fact-selection behaviour has been separated from narrative generation sufficiently to enforce the authority rules.
5. The known forensic conflicts have regression tests.
6. The generator has been exercised against at least one realistic CV-generation scenario and one realistic Upwork/proposal/interview scenario.
7. Generated outputs have been manually inspected for:
   - factual accuracy;
   - title accuracy;
   - chronology;
   - qualification accuracy;
   - absence of unsupported claims;
   - relevance to the target opportunity.
8. No unrelated architecture or repository changes have been introduced.

The implementation should stop at this point.