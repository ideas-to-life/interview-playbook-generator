# Personal Knowledge Base — Forensic Data Quality Diagnostic

## Purpose

Perform a detailed, forensic data-quality assessment of my personal professional knowledge base.

The objective is **not to clean, modify, rewrite, consolidate or improve the source data**.

The objective is to determine:

1. What information exists.
2. Where it exists.
3. How much duplication exists.
4. Where information conflicts.
5. Which sources appear authoritative.
6. Which information is stale, ambiguous, incomplete or unsupported.
7. Whether generated artefacts have become accidental sources of truth.
8. How these issues could affect downstream AI workflows and generators.
9. What should be fixed, where it should be fixed, and in what order.

Treat this as a **forensic data-quality diagnostic**, not a content review.

The diagnostic must preserve the distinction between:
- a genuine factual conflict;
- a legitimate contextual variation;
- a difference in level of abstraction;
- duplicate information;
- semantic overlap;
- stale information;
- missing information;
- unsupported claims;
- and differences caused simply by different document purposes.

Do not assume that two different statements are contradictory merely because they use different wording.

---

# 1. Scope

Inspect all available relevant sources in the supplied knowledge base, including, where present:

- CVs
- CV variants
- Portfolio
- Portfolio case studies
- LinkedIn-related content
- Upwork profile/content
- Career history
- Employment records
- Project descriptions
- Project documentation
- Architecture work
- Case studies
- Skills/capabilities
- Technology/tool lists
- Certifications
- Education
- Professional positioning
- Personal/professional biography
- Interview material
- Interview playbooks
- Cover letters
- Proposals
- Generated profiles
- Generated summaries
- Other derived or AI-generated artefacts

Do not limit the assessment to filenames that obviously contain "CV", "portfolio" or "profile".

Identify the complete relevant source landscape first.

---

# 2. Operating Principles

Apply the following principles throughout the investigation.

## 2.1 Evidence over inference

Never silently infer that a statement is true simply because it appears plausible.

For every significant finding, identify the source(s) supporting it.

If evidence is insufficient, classify the finding as:

`UNVERIFIED`

rather than attempting to resolve it.

## 2.2 Do not rewrite the source

Quote or paraphrase only enough to identify the issue.

Do not silently correct dates, titles, organisations, achievements, technologies or claims.

## 2.3 Do not select a "winner" without evidence

When two sources conflict:

- identify the conflict;
- identify the competing values;
- identify source provenance;
- assess source authority where possible;
- recommend what should be investigated;
- but do not silently decide which value is true.

If the evidence clearly establishes one value, state that explicitly and explain why.

## 2.4 Preserve contextual differences

Distinguish between:

`FACTUAL CONFLICT`

and:

`LEGITIMATE REPRESENTATION VARIATION`

For example:

> "Enterprise Architect"

and:

> "AI Transformation Advisor"

may describe different aspects of the same professional identity rather than conflicting facts.

Likewise:

> "Led architecture"

and:

> "Designed the architecture"

may differ in scope and responsibility and should not automatically be treated as contradictions.

## 2.5 Treat generated artefacts as potentially untrusted

Determine whether information appears to have originated from:

- primary/source material;
- manually authored derived material;
- AI-generated material;
- AI-generated material subsequently reused as source material.

Pay particular attention to **knowledge contamination loops**, such as:

```text
Source
  ↓
AI-generated CV
  ↓
AI-generated portfolio
  ↓
Knowledge Base
  ↓
AI-generated Interview Playbook
  ↓
Knowledge Base
```

Flag these explicitly.

---

# 3. Phase 1 — Source Inventory

Create a complete inventory of relevant sources.

For each source record:

| Field | Description |
|---|---|
| Source ID | Unique identifier |
| Filename / identifier | Exact source |
| Type | CV, project, portfolio, etc. |
| Authoring status | Human / AI / unknown |
| Approximate date | If available |
| Last modified | If available |
| Likely purpose | What the source is intended to represent |
| Source authority | Primary / secondary / derived / unknown |
| Potentially authoritative domains | What facts this source may be authoritative for |
| Dependencies | Other sources it appears to derive from |

Identify sources that appear to be:

- duplicates;
- versions;
- derivatives;
- superseded;
- generated;
- partially generated;
- or composites of other sources.

Do not assume the newest file is automatically the most authoritative.

---

# 4. Phase 2 — Data Profiling

Profile the knowledge base as a whole.

Report:

### Completeness

Identify missing or weakly represented information relating to:

- career history;
- organisations;
- roles;
- dates;
- responsibilities;
- achievements;
- projects;
- outcomes;
- capabilities;
- technologies;
- qualifications;
- certifications;
- evidence.

Distinguish:

`UNKNOWN`

from:

`NOT APPLICABLE`

from:

`NOT PROVIDED`

from:

`NOT YET VERIFIED`

### Uniqueness

Identify:

- exact duplicates;
- near-duplicates;
- semantic duplicates;
- repeated claims;
- duplicated projects;
- duplicated career entries;
- multiple representations of the same achievement.

Do not count legitimate repeated references across different documents as defects unless the repetition creates ambiguity or unnecessary divergence.

### Consistency

Assess consistency:

- within individual sources;
- across sources;
- across time;
- across documents representing the same professional history.

### Timeliness

Identify:

- obsolete roles;
- obsolete technology references;
- outdated positioning;
- outdated employment status;
- superseded projects;
- stale achievements;
- old professional objectives;
- stale generated content.

Do not classify historical information as stale merely because it is old. Historical information can remain valid.

### Validity

Identify values that violate obvious structural or semantic expectations, for example:

- impossible date sequences;
- employment periods that overlap unexpectedly;
- projects occurring before the associated role;
- inconsistent organisation names;
- malformed URLs;
- invalid qualification dates;
- implausible chronology.

### Accuracy

Where evidence exists, compare claims against stronger source material.

Do not attempt to externally verify every professional claim unless external verification is explicitly within scope.

Use:

`VERIFIED`

`SUPPORTED`

`UNSUPPORTED`

`CONTRADICTED`

`UNKNOWN`

rather than inventing an accuracy judgement.

---

# 5. Phase 3 — Semantic Duplicate Detection

Go beyond exact textual duplication.

Identify statements that express substantially the same underlying claim despite different wording.

For example:

```text
"Designed an enterprise architecture framework"

"Created an EA framework"

"Architected the enterprise framework"
```

Potentially represent one underlying claim.

For each semantic duplicate group provide:

```text
Duplicate Group ID
Underlying concept
Source A
Statement A
Source B
Statement B
Similarity rationale
Likely same fact? YES / NO / UNCERTAIN
Recommended investigation
```

Do not merge them.

The purpose is to identify candidates for later consolidation.

---

# 6. Phase 4 — Contradiction Detection

Identify factual contradictions across sources.

Prioritise:

### Career

- organisation names;
- employment dates;
- role titles;
- seniority;
- responsibilities;
- reporting relationships where stated.

### Projects

- project dates;
- project ownership;
- role;
- responsibilities;
- technologies;
- architecture scope;
- outcomes;
- clients/organisations.

### Capabilities

- claimed expertise;
- depth of experience;
- technology proficiency;
- domain expertise;
- leadership claims.

### Achievements

- claimed outcomes;
- quantified results;
- scale;
- ownership;
- business impact.

### Professional positioning

- role identity;
- target roles;
- service offering;
- areas of expertise;
- professional narrative.

For every contradiction produce:

```text
Conflict ID
Subject
Claim
Source A
Value A
Source B
Value B
Conflict type
Materiality
Potential impact
Evidence available
Likely reason for divergence
Recommended resolution method
```

Classify conflict types such as:

- DATE_CONFLICT
- TITLE_CONFLICT
- ROLE_SCOPE_CONFLICT
- RESPONSIBILITY_CONFLICT
- TECHNOLOGY_CONFLICT
- ACHIEVEMENT_CONFLICT
- METRIC_CONFLICT
- OWNERSHIP_CONFLICT
- POSITIONING_CONFLICT
- OTHER

---

# 7. Phase 5 — Temporal Consistency

Construct a reconstructed professional timeline from the available sources.

Do not resolve conflicting dates silently.

Identify:

- conflicting employment dates;
- overlapping roles;
- unexplained gaps;
- projects outside their apparent employment period;
- technologies appearing before/after plausible usage;
- achievements attributed to the wrong period;
- portfolio case studies with unclear chronology.

Produce a timeline showing:

```text
Period
Organisation
Role
Source evidence
Confidence
Conflicts
```

Flag chronology that requires human confirmation.

---

# 8. Phase 6 — Claim-Level Analysis

Identify important professional claims and assess each claim independently.

Focus particularly on claims that are likely to influence:

- recruiter perception;
- interview answers;
- CV generation;
- Upwork proposals;
- portfolio content;
- professional positioning.

Examples:

```text
"Led..."
"Designed..."
"Architected..."
"Delivered..."
"Built..."
"Implemented..."
"Transformed..."
"Reduced..."
"Increased..."
"Saved..."
"Managed..."
"Owned..."
"Created..."
```

For each material claim identify:

```text
Claim ID
Claim
Claim type
Source(s)
Evidence
Provenance
Status
Confidence
Conflicts
Potential downstream impact
```

Classify claim status as:

- VERIFIED
- WELL_SUPPORTED
- PARTIALLY_SUPPORTED
- UNVERIFIED
- CONFLICTED
- POTENTIALLY_DERIVED
- POTENTIALLY_GENERATED
- STALE

Pay particular attention to quantified claims.

A numerical achievement should receive additional scrutiny because incorrect numbers can propagate disproportionately through generated content.

---

# 9. Phase 7 — Provenance Analysis

For every material claim, determine whether it is possible to answer:

> "Where did this information originally come from?"

Classify provenance as:

```text
PRIMARY
SECONDARY
DERIVED
GENERATED
UNKNOWN
```

Examples:

### PRIMARY

Original project documentation, employment record, personal record, direct evidence.

### SECONDARY

CV, portfolio, LinkedIn profile, manually written summary.

### DERIVED

A document created from another source.

### GENERATED

AI-generated content.

### UNKNOWN

Origin cannot be established.

Identify claims where:

```text
GENERATED → became apparent SOURCE
```

or:

```text
DERIVED → became apparent AUTHORITATIVE SOURCE
```

These should be high-priority findings.

---

# 10. Phase 8 — Source Authority Analysis

For each important category of information, identify which source appears to have the strongest authority.

Create a table:

| Information domain | Candidate source | Authority | Evidence | Confidence |
|---|---|---|---|---|
| Employment dates | | | | |
| Role titles | | | | |
| Project history | | | | |
| Project responsibilities | | | | |
| Achievements | | | | |
| Technology experience | | | | |
| Capabilities | | | | |
| Professional positioning | | | | |
| Education | | | | |
| Certifications | | | | |

Do not assume that one document must be authoritative for everything.

A source may be authoritative for one category but not another.

---

# 11. Phase 9 — Cross-Document Consistency

Explicitly compare the major professional representations:

```text
CV
vs
Portfolio

CV
vs
LinkedIn

CV
vs
Upwork

Portfolio
vs
Project records

Interview material
vs
source knowledge
```

For each pair identify:

- consistent facts;
- missing facts;
- additional facts;
- contradictory facts;
- different levels of abstraction;
- different narrative emphasis;
- potentially problematic divergence.

Distinguish:

`EXPECTED_PROJECTION_DIFFERENCE`

from:

`DATA_QUALITY_PROBLEM`.

This distinction is critical.

A CV and portfolio should not necessarily contain identical information.

---

# 12. Phase 10 — AI/Generator Contamination Analysis

Identify evidence that generated content may have entered the knowledge base and subsequently influenced later generated content.

Look for:

```text
source → generated artefact → source
```

patterns.

Flag:

- unsupported claims introduced by generated content;
- inflated terminology;
- invented metrics;
- stronger claims than the source evidence supports;
- role descriptions that become progressively embellished;
- technologies appearing only after generation;
- "buzzword drift";
- claims appearing first in an AI-generated artefact.

Explicitly identify possible **semantic amplification**:

```text
Original:
"Contributed to architecture"

Generated:
"Led architecture"

Later generated:
"Led enterprise-wide architecture transformation"
```

Do not assume this happened unless evidence supports the sequence.

---

# 13. Phase 11 — Impact Analysis

Assess how each significant data-quality issue could affect downstream outputs.

Use:

### Critical

Could materially misrepresent professional history, experience, ownership, dates, achievements or qualifications.

### High

Could materially distort positioning, interview responses, CV content or proposals.

### Medium

Could cause inconsistency or confusion but is unlikely to materially misrepresent experience.

### Low

Minor wording, formatting or metadata issue.

For each issue identify affected downstream artefacts:

```text
CV
Portfolio
Upwork
Interview Playbook
Cover Letter
LinkedIn
Other
```

---

# 14. Phase 12 — Root-Cause Analysis

Do not stop at identifying symptoms.

For significant issues determine the likely root cause.

Possible categories:

```text
SOURCE_DATA_ERROR
DUPLICATION
VERSION_DRIFT
MANUAL_EDIT
CONTEXTUAL_VARIATION
AMBIGUOUS_SOURCE
MISSING_PROVENANCE
AI_GENERATION
AI_REGENERATION
STALE_DATA
INCONSISTENT_SCHEMA
KNOWLEDGE_BASE_DESIGN
UNKNOWN
```

Where appropriate, show:

```text
Observed issue
      ↓
Immediate cause
      ↓
Underlying cause
      ↓
Systemic cause
```

For example:

```text
Conflicting role description
        ↓
Two CV variants contain different wording
        ↓
No canonical career record
        ↓
Documents are acting as competing sources
```

---

# 15. Phase 13 — Quality Scoring

Do NOT produce an arbitrary overall score unless there is sufficient evidence and a clearly defined scoring model.

Instead report measurable indicators such as:

```text
Sources assessed
Claims identified
Material claims
Exact duplicates
Semantic duplicate groups
Material conflicts
Unverified claims
Claims without provenance
Potential generated-source claims
Stale items
Chronology conflicts
Cross-document inconsistencies
```

If a quality score is useful, construct it transparently from the underlying measures and explain the methodology.

Do not hide uncertainty behind a single number.

---

# 16. Phase 14 — Findings Register

Produce a complete findings register.

Use:

| ID | Severity | Dimension | Finding | Evidence | Affected sources | Impact | Root cause | Recommended action |
|---|---|---|---|---|---|---|---|---|

Do not recommend modifying source content yet unless necessary to explain the remediation.

---

# 17. Phase 15 — Remediation Recommendations

For each significant finding recommend one of:

```text
LEAVE
MONITOR
VERIFY
MERGE
DEPRECATE
REPLACE
ESTABLISH_CANONICAL_SOURCE
ADD_PROVENANCE
REWRITE_SOURCE
REMOVE_DERIVED_SOURCE
RESTRUCTURE_KNOWLEDGE
```

Prioritise recommendations using:

```text
Priority
Impact
Confidence
Effort
Dependency
```

Do not execute the remediation.

---

# 18. Final Report Structure

Produce the final report using exactly this structure:

# Personal Knowledge Base — Forensic Data Quality Diagnostic

## 1. Executive Summary

Summarise:

- overall condition;
- most important findings;
- major risks;
- whether the interview-playbook-generator is likely to be affected;
- whether the problem appears primarily to be source-data quality, knowledge architecture, generator behaviour, or a combination.

Do not make claims that the evidence does not support.

## 2. Scope & Methodology

Document:

- sources examined;
- sources excluded;
- analysis performed;
- limitations;
- assumptions.

## 3. Source Inventory

Provide the complete source inventory and authority assessment.

## 4. Data Quality Profile

Report:

- completeness;
- uniqueness;
- consistency;
- timeliness;
- validity;
- accuracy;
- provenance.

## 5. Duplicate Analysis

Report:

- exact duplicates;
- near duplicates;
- semantic duplicates;
- duplicate claims.

## 6. Conflict Analysis

Report all material contradictions.

## 7. Temporal Consistency

Provide the reconstructed timeline and chronology issues.

## 8. Claim-Level Analysis

Report significant professional claims and their evidence/provenance.

## 9. Cross-Document Consistency

Compare:

- CV;
- Portfolio;
- LinkedIn;
- Upwork;
- Project records;
- interview material.

## 10. AI/Generated-Content Contamination

Identify potential generation → ingestion → regeneration loops.

## 11. Root-Cause Analysis

Identify systemic causes rather than only symptoms.

## 12. Downstream Impact

Explain likely consequences for:

- interview-playbook-generator;
- CV generator;
- proposal generator;
- portfolio;
- other relevant workflows.

## 13. Findings Register

Provide the complete prioritised findings table.

## 14. Recommended Remediation

Provide a sequenced remediation plan.

## 15. Recommended Target-State Architecture

Describe what the knowledge base should ideally look like after remediation.

Do not implement it.

## 16. Immediate Next Steps

Provide the smallest practical sequence of actions required to move from the current state to a trustworthy knowledge base.

## 17. Appendix A — Detailed Evidence

Include detailed source-level evidence for significant findings.

## 18. Appendix B — Unresolved Questions

List every question that requires human confirmation.

---

# 19. Important Constraints

You MUST:

- inspect the actual available source material;
- use evidence from the sources;
- preserve provenance;
- distinguish facts from interpretations;
- distinguish conflicts from contextual variation;
- identify uncertainty;
- identify generated-content contamination;
- report both symptoms and root causes;
- avoid silently correcting information;
- avoid silently selecting conflicting values;
- avoid inventing missing information.

You MUST NOT:

- modify source files;
- delete anything;
- rewrite the CV;
- rewrite the portfolio;
- create a canonical knowledge base;
- resolve conflicts silently;
- invent facts;
- infer achievements;
- improve marketing language;
- "polish" claims;
- treat AI-generated content as authoritative merely because it sounds plausible.

The result must be a **diagnostic report and remediation plan only**.

The final objective is to establish a reliable baseline from which a subsequent **Personal Knowledge Base Remediation** exercise can be performed safely.