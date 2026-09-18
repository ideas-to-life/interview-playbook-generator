# Interview Playbook Generator
## Remediation Requirements Specification — Projection Data Integrity & Provenance

**Status:** Proposed  
**Purpose:** Remediate the forensic defects identified in the September 2026 projection-data diagnostic  
**Scope:** Projection generation, runtime context assembly, ATS vocabulary handling, cross-opportunity isolation, and projection validation

---

# 1. Purpose

The forensic diagnostic of the Tenth AI Lead Enterprise Architect generation established four distinct integrity defects:

1. Target-job-description keywords can be transformed into unsupported candidate claims through ATS-density optimisation.
2. Previous opportunity projections can enter the active generation context and contaminate subsequent projections.
3. `canonical-selection.yaml` can be only partially loaded, leaving authoritative candidate facts outside the model context.
4. Projection validation does not systematically verify generated candidate facts against canonical facts.

This specification defines the requirements to remediate those defects.

The objective is to establish a reliable information-flow boundary:

```text
canonical facts
      ↓
canonical selection
      ↓
complete candidate context
      ↓
evidence-aware opportunity analysis
      ↓
projection
      ↓
validation
```

with the following prohibited flows:

```text
previous projection ──X──► candidate facts

target JD keyword ──X──► candidate capability

partial canonical selection ──X──► projection

generated projection ──X──► canonical / knowledge
```

---

# 2. Architectural Principles

## 2.1 Canonical facts remain authoritative

`mind-palace/canonical/career-record.yaml` remains the authoritative source for controlled professional facts.

The remediation must not weaken or bypass the existing canonical architecture.

---

## 2.2 Canonical selection is the frozen candidate-fact boundary

`canonical-selection.yaml` represents the candidate facts selected for a specific opportunity.

Projection generation must consume the **complete** selection.

The generator must not rely on the LLM to infer omitted portions of the selection.

---

## 2.3 Requirements are not evidence

A requirement appearing in a target job description does not constitute evidence that the candidate possesses the associated capability, technology experience, certification, qualification, or language proficiency.

For example:

```text
JD:
Workday experience required
```

must not become:

```text
Candidate:
Governed Workday integrations
```

unless candidate evidence supports that claim.

---

## 2.4 Projections are terminal outputs

Generated projections are outputs, not candidate-fact sources.

A projection from one opportunity must never become factual input to another opportunity.

This applies across:

- resumes
- cover letters
- LinkedIn profiles
- opportunity alignment
- executive briefs
- interview playbooks
- interview cheat sheets
- other generated collateral

---

## 2.5 Transformation is permitted; factual amplification is not

Projection generation may:

- select relevant facts
- reorder facts
- combine supported facts
- rewrite wording
- tailor emphasis
- map verified experience to job requirements

It must not:

- invent facts
- upgrade proficiency
- create certifications
- change dates
- change formal titles
- turn a job requirement into experience
- turn a course into a certification
- turn inferred familiarity into demonstrated experience

Core principle:

> The generator may select, transform and present candidate evidence. It may not redefine candidate evidence.

---

# 3. Functional Requirements

## FR-01 — Complete canonical-selection loading

Before any projection is generated, the complete:

`out/<target-slug>/runtime/canonical-selection.yaml`

must be loaded into the projection-generation context.

The implementation must not depend on arbitrary line limits, truncation, partial file reads, or opportunistic context selection.

### Acceptance criteria

Given a canonical selection containing:

- employment records
- education
- certifications
- languages
- other selected canonical facts

all selected sections must be available to the projection generator.

A test must specifically verify that facts located beyond the first 50 lines remain available.

The Tenth diagnostic case must therefore expose:

```text
BSc: 1988–1991
```

rather than allowing the generator to infer alternative dates.

---

# 4. FR-02 — Canonical-selection authority

Projection generation must explicitly identify `canonical-selection.yaml` as the authoritative source for controlled candidate facts.

Where another input conflicts with canonical selection, canonical selection takes precedence for facts within its scope.

The projection prompt/context contract must make this distinction explicit.

### Acceptance criteria

If an auxiliary source says:

```text
Spanish: Fluent
```

while canonical selection says:

```text
Spanish: Elementary
```

the generated projection must not state Fluent.

---

# 5. FR-03 — No previous-projection consumption

An active opportunity generation run must not read generated artefacts belonging to another opportunity as candidate factual context.

This includes any path of the form:

```text
out/<other-target-slug>/*
```

unless that file is explicitly classified as an approved non-factual structural resource.

The preferred architecture is that projection formatting and structural examples reside in:

- skills
- templates
- schemas
- controlled static resources

rather than previous candidate-specific outputs.

### Acceptance criteria

Generating:

```text
out/tenth-ai-lead-enterprise-architect/
```

must not require reading:

```text
out/lseg-director-enterprise-architecture/
```

or any other previous opportunity output.

A regression test must prove that a deliberately contaminated previous projection cannot influence the new projection.

---

# 6. FR-04 — Structural examples must be fact-free

If examples are required to demonstrate:

- section layout
- formatting
- length
- style
- Markdown structure
- ATS structure

they must not be candidate-specific previous projections.

Approved examples must contain clearly synthetic or neutral placeholder content.

### Acceptance criteria

The projection generator must be able to generate a resume without reading a previous candidate-specific resume.

---

# 7. FR-05 — Separate job requirements from candidate evidence

The opportunity-analysis model must distinguish between:

```text
job requirement
```

and:

```text
candidate-supported capability
```

ATS vocabulary extracted from the job description must remain classified as **job vocabulary** unless candidate evidence has been established.

The presence of a technology or platform in:

```text
ats_vocabulary
```

must not itself establish candidate experience.

---

# 8. FR-06 — Evidence-aware ATS vocabulary

ATS vocabulary must be divided conceptually into at least:

```text
required / desired job vocabulary
```

and:

```text
candidate-evidenced vocabulary
```

Only candidate-evidenced vocabulary may be used to make factual claims about the candidate.

Unmatched requirements must remain requirements/gaps.

### Example

If the JD contains:

```text
Salesforce
Workday
NetSuite
Coupa
Concur
```

and candidate evidence supports only:

```text
SAP
enterprise integration
HR systems
finance systems
```

the resume may legitimately describe the supported experience and transferable architecture capability.

It must not claim experience with:

```text
Workday
NetSuite
Coupa
Concur
```

without evidence.

---

# 9. FR-07 — ATS scoring must not reward unsupported claims

ATS-density scoring must not create an incentive to insert unsupported candidate claims.

A resume achieving:

```text
100% ATS vocabulary density
```

must not automatically be considered successful if the additional terms are unsupported.

The scoring model must distinguish between:

1. inclusion of relevant job vocabulary;
2. supported candidate evidence;
3. unsupported claims.

Unsupported keyword insertion must be treated as a defect, not as an optimisation.

---

# 10. FR-08 — Gap-aware projection behaviour

When a target requirement has no candidate evidence, projection generation should use an appropriate representation rather than fabricate direct experience.

Possible representations include:

- explicit gap
- transferable capability
- adjacent experience
- architecture-level applicability
- interview preparation topic

The exact presentation depends on the projection type.

The generator must not represent a gap as established experience.

---

# 11. FR-09 — Education validation

Generated projections containing education must be validated against canonical education records.

Validation must cover at least:

- institution
- qualification
- field of study where controlled
- start year
- end year

### Example regression

Canonical:

```text
Universidade de Mogi das Cruzes
BSc Computer Science
1988–1991
```

Generated:

```text
Universidade de Mogi das Cruzes
BSc Computer Science
1995–1999
```

must fail validation.

---

# 12. FR-10 — Certification validation

Generated certifications must be validated against canonical certifications.

A certification appearing in a projection but absent from the canonical certification set must fail validation unless explicitly marked as a non-certification learning activity.

### Regression cases

The following must fail if generated as certifications:

```text
AWS Certified Solutions Architect – Associate
Sun Certified Enterprise Architect
Sun Certified Java Programmer
```

because they are not present in the canonical certification record established by the diagnostic.

Course preparation or learning activity must not be promoted to formal certification.

---

# 13. FR-11 — Language proficiency validation

Generated language proficiency must be validated against canonical language records.

The generator must not upgrade proficiency.

### Regression case

Canonical:

```text
Spanish: Elementary
```

Generated:

```text
Spanish: Fluent
```

must fail validation.

This applies to all controlled language proficiency levels.

---

# 14. FR-12 — Employment fact validation

Existing employment validation must remain in place and be extended only where required.

Generated employment sections must continue to respect:

- canonical employer
- canonical formal title
- approved title aliases
- employment dates
- engagement type
- known operational/acting scope distinctions

Operational responsibility must not be transformed into a formal contracted title.

---

# 15. FR-13 — Named technology/evidence validation

The system must distinguish between:

```text
technology mentioned in the target JD
```

and:

```text
technology supported by candidate evidence
```

Where a generated projection makes a specific candidate-experience claim involving a named platform, the validator should determine whether supporting evidence exists.

This requirement should initially cover the forensic canaries:

```text
Workday
NetSuite
Coupa
Concur
```

and should be designed so that it can later support broader evidence-card/provenance validation.

The implementation must not hard-code these four platforms as permanently forbidden technologies.

The rule is:

> unsupported candidate claims fail regardless of the technology name.

---

# 16. FR-14 — Previous-projection contamination regression

Create a regression scenario in which a previous projection contains deliberately false candidate information.

Example:

```text
Previous projection:
AWS Certified Solutions Architect
Spanish Fluent
BSc 1995–1999
```

The next opportunity's generated artefacts must not reproduce those facts unless they independently exist in approved candidate evidence.

This test proves the information-flow boundary rather than merely checking known strings.

---

# 17. FR-15 — Target-JD leakage regression

Create a regression scenario where the target JD contains technologies deliberately absent from candidate evidence.

Example:

```text
Workday
NetSuite
Coupa
Concur
```

The generated resume must not claim that the candidate has direct experience with those platforms.

The job requirements may still appear in:

- gap analysis
- opportunity analysis
- interview preparation
- transferable capability analysis

provided they are clearly represented as requirements rather than candidate facts.

---

# 18. FR-16 — Projection cannot modify canonical truth

Projection generation must not write generated candidate claims back into:

```text
mind-palace/canonical/
```

or any other authoritative candidate-fact source.

The existing one-way architecture remains:

```text
canonical
   ↓
knowledge
   ↓
projections
```

No reverse flow is permitted.

---

# 19. FR-17 — Opportunity isolation

Each opportunity runtime must be isolated from other opportunity runtimes.

Generation of:

```text
target-A
```

must not depend on:

```text
target-B
```

candidate-specific outputs.

This should apply regardless of generation order.

For example:

```text
Generate LSEG
Generate Tenth
```

and:

```text
Generate Tenth
Generate LSEG
```

should not change the candidate facts appearing in either output.

---

# 20. FR-18 — Deterministic validation before completion

Projection generation must include deterministic validation after generation.

A projection containing a known canonical contradiction must fail rather than merely produce a warning.

At minimum, validation must cover:

```text
education
certifications
languages
employment facts
unsupported named candidate technologies
```

The validation result must be machine-readable.

---

# 21. FR-19 — No false confidence from conflict reports

`canonical-conflict-report.yaml` must not be treated as a complete projection-factual-integrity report unless its scope is expanded accordingly.

The system should distinguish between:

```text
canonical conflict detection
```

and:

```text
projection factual validation
```

A zero-conflict canonical report must not imply that every generated claim is supported.

---

# 22. FR-20 — Preserve useful professional knowledge

The remediation must not over-correct by requiring every useful professional statement to appear verbatim in `career-record.yaml`.

The canonical record remains the authoritative controlled fact layer.

Approved knowledge may still provide:

- contextual detail
- methodology
- project knowledge
- architectural patterns
- demonstrated approaches
- thought leadership
- technical context

provided it does not contradict canonical facts or create unsupported candidate claims.

This requirement deliberately avoids turning `career-record.yaml` into a complete replacement for the knowledge repository.

---

# 23. Information Classification

The implementation should explicitly distinguish at least these classes of information:

```text
TIER 1 — CONTROLLED CANDIDATE FACT
  canonical career record
  canonical selection
  verified primary evidence

TIER 2 — SUPPORTING PROFESSIONAL KNOWLEDGE
  trusted knowledge
  project context
  methods
  learnings

TIER 3 — OPPORTUNITY REQUIREMENTS
  target JD
  required capabilities
  ATS vocabulary
  employer expectations

TIER 4 — GENERATED ANALYSIS
  gap analysis
  fit analysis
  projection strategy

TIER 5 — GENERATED PROJECTION
  resume
  cover letter
  LinkedIn
  executive brief
  playbook
  other collateral
```

The following information-flow rules apply:

```text
TIER 1 → TIER 2       permitted where explicitly designed
TIER 1 → TIER 3       permitted for evidence matching
TIER 1 → TIER 4       permitted
TIER 1 → TIER 5       permitted

TIER 2 → TIER 5       permitted with factual controls
TIER 3 → TIER 4       permitted
TIER 3 → TIER 5       permitted only as requirements/context

TIER 4 → TIER 5       permitted as analysis/strategy
TIER 5 → TIER 1       prohibited
TIER 5 → TIER 2       prohibited
TIER 5 → candidate facts in another opportunity — prohibited
```

---

# 24. Required Regression Scenarios

The existing regression suite must be extended to cover the newly discovered failure modes.

At minimum:

### Scenario 1 — Complete canonical selection

Verify that facts beyond line 50 of canonical selection are available during projection generation.

### Scenario 2 — Education contradiction

Generate a projection with an incorrect BSc date and verify validation failure.

### Scenario 3 — Certification invention

Generate a projection containing AWS/SCEA/SCJP and verify validation failure.

### Scenario 4 — Language inflation

Generate a projection stating Spanish Fluent when canonical says Elementary and verify failure.

### Scenario 5 — JD platform leakage

Target JD contains Workday, NetSuite, Coupa and Concur but candidate evidence does not.

Verify that generated candidate experience does not claim those platforms.

### Scenario 6 — Previous projection contamination

Place false candidate facts in a previous opportunity projection.

Generate a new opportunity.

Verify that the false facts cannot enter the new candidate projection.

### Scenario 7 — Opportunity isolation

Generate two opportunities containing deliberately different target-specific requirements.

Verify that requirements from one opportunity cannot become candidate facts in the other.

### Scenario 8 — Unsupported technology claim

Introduce a named technology that is absent from candidate evidence and verify that a direct candidate-experience claim fails validation.

### Scenario 9 — Target keyword remains a requirement

Verify that an unsupported JD keyword can still appear in gap analysis or interview preparation without being incorrectly classified as candidate experience.

### Scenario 10 — Canonical contradiction takes precedence

Provide conflicting non-canonical information and verify that canonical information wins.

---

# 25. Non-Functional Requirements

## NFR-01 — Determinism

Factual validation must be deterministic wherever practical.

Do not rely on an LLM to decide whether:

```text
1995–1999
```

matches:

```text
1988–1991
```

or whether:

```text
AWS Certified Solutions Architect
```

exists in the canonical certification set.

---

## NFR-02 — Explainability

Validation failures must identify:

- generated claim
- expected/authoritative value where applicable
- source of authority
- reason for failure

Example:

```text
FAIL
Claim: Spanish — Fluent
Canonical: Spanish — Elementary
Source: canonical/career-record.yaml
Reason: generated proficiency exceeds canonical proficiency
```

---

## NFR-03 — No hard-coded forensic-only fixes

Do not implement special-case rules solely for:

```text
Workday
NetSuite
Coupa
Concur
AWS
Sun SCEA
Sun SCJP
Spanish
1995–1999
```

These are forensic test cases, not the architecture.

The implementation must generalise the underlying integrity rules.

---

## NFR-04 — Backwards compatibility

Existing valid canonical facts, employment aliases, and approved projection functionality must continue to work.

The remediation must not unnecessarily reduce useful professional context.

---

# 26. Out of Scope

The following are explicitly out of scope for this remediation:

1. Rebuilding the entire `mind-palace`.
2. Implementing a complete evidence-card architecture.
3. Reclassifying every historical knowledge item.
4. Regenerating all existing opportunity outputs.
5. Rewriting the canonical career record unless forensic evidence subsequently demonstrates a source-data defect.
6. Introducing an LLM-based factual adjudicator as the primary validator.
7. Optimising resume wording or branding.
8. Expanding the canonical record into a complete project knowledge repository.
9. Adding new career facts based solely on generated projections.

---

# 27. Implementation Sequence

The remediation should be implemented in this order:

```text
1. Complete canonical-selection loading
            ↓
2. Enforce opportunity/projection isolation
            ↓
3. Separate JD requirements from candidate evidence
            ↓
4. Remove ATS-density incentive for unsupported claims
            ↓
5. Add deterministic projection factual validation
            ↓
6. Add regression scenarios
            ↓
7. Re-run forensic target generation
            ↓
8. Compare output against forensic baseline
```

Do not begin by adding individual forbidden terms.

The implementation should correct the information-flow architecture first.

---

# 28. Acceptance Gate

The remediation is considered successful only when the Tenth AI Lead Enterprise Architect scenario can be regenerated and all of the following are true:

### Candidate facts

- BSc is represented as 1988–1991.
- Spanish is not represented as Fluent.
- AWS certification is not invented.
- Sun SCEA is not invented.
- Sun SCJP is not invented.

### Target requirements

- Workday is not presented as demonstrated candidate experience without evidence.
- NetSuite is not presented as demonstrated candidate experience without evidence.
- Coupa is not presented as demonstrated candidate experience without evidence.
- Concur is not presented as demonstrated candidate experience without evidence.

### Context isolation

- No LSEG candidate-specific projection is required as input.
- Previous opportunity outputs cannot contribute candidate facts.
- Complete canonical selection is available to projection generation.

### Validation

- Contradictory education dates fail.
- Unsupported certifications fail.
- Inflated language proficiency fails.
- Unsupported candidate technology claims fail.
- JD keyword density cannot be achieved by unsupported factual claims without validation failure.

### Regression

All existing tests remain passing and all new forensic regression scenarios pass.

---

# 29. Core Design Rule

The remediation must preserve the following invariant:

> **The target position describes what the employer wants. The canonical record describes what the candidate has established. The projection describes how the candidate's established evidence is relevant to the position.**

No stage may collapse those three concepts into one.

And the generator must remain governed by the fundamental rule:

> **It may select, transform and present canonical facts. It may not redefine them.**
