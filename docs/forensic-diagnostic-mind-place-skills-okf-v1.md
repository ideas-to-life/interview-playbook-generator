# Forensic Diagnostic: Projection Data Provenance

## Objective

Perform a forensic investigation into the provenance of unsupported candidate facts appearing in the generated artefacts for:

`out/tenth-ai-lead-enterprise-architect/`

Do **not modify, delete, regenerate, refactor, or "fix" any files** during this investigation.

The purpose is to establish exactly where unsupported facts entered the generation pipeline.

The current working assumption is that:

- `mind-palace/canonical/career-record.yaml` is the authoritative candidate fact source.
- `out/tenth-ai-lead-enterprise-architect/runtime/canonical-selection.yaml` appears correct.
- Therefore, the investigation must focus on what happens **after canonical selection** and on any additional sources made available to projection generation.

---

## Known-good checkpoint

Treat:

`out/tenth-ai-lead-enterprise-architect/runtime/canonical-selection.yaml`

as the known-good factual checkpoint unless forensic evidence demonstrates otherwise.

Do not alter it.

The following facts in the generated Tenth artefacts are known forensic canaries because they either contradict or are absent from the canonical selection:

| Canary fact | Canonical / expected | Observed in generated output |
|---|---|---|
| BSc dates | 1988–1991 | 1995–1999 |
| Spanish | Elementary | Fluent |
| AWS Certified Solutions Architect | Not present | Present |
| Sun Certified Enterprise Architect | Not present | Present |
| Sun Certified Java Programmer | Not present | Present |
| Workday | Not established | Present |
| NetSuite | Not established | Present |
| Coupa | Not established | Present |
| Concur | Not established | Present |

Use these facts as provenance markers throughout the investigation.

---

# Phase 1 — Establish the projection generation path

Identify the exact skills, scripts, prompts, and orchestration logic responsible for generating:

- `resume-executive.md`
- `resume-ats.md`
- `resume-recruiter.md`
- `cover-letter.md`
- `linkedin-profile.md`
- `opportunity-alignment.md`
- `executive-brief.md`
- `playbook.md`
- `interview-cheatsheet.md`

Search for their generation entry points.

Use searches such as:

```bash
grep -RniE \
  'resume-executive|resume-ats|resume-recruiter|cover-letter|linkedin-profile|opportunity-alignment|executive-brief|playbook|interview-cheatsheet' \
  skills scripts \
  --exclude-dir=.venv \
  --exclude='*.pyc'
```

Identify:

1. Which skill generates each artefact.
2. Which script/orchestrator invokes it.
3. Which files are explicitly instructed as inputs.
4. Which files are dynamically discovered or searched.
5. Whether generated artefacts from previous opportunities can enter the context.

Do not modify anything.

---

# Phase 2 — Investigate previous generated projections

The execution log contains a particularly important sequence:

```text
Read(.../out/lseg-director-enterprise-architecture/resume-executive.md)
Read(.../out/lseg-director-enterprise-architecture/resume-ats.md)
Read(.../out/lseg-director-enterprise-architecture/cover-letter.md)
Read(.../out/lseg-director-enterprise-architecture/resume-recruiter.md)
Read(.../out/lseg-director-enterprise-architecture/linkedin-profile.md)
Read(.../out/lseg-director-enterprise-architecture/opportunity-alignment.md)
Read(.../out/lseg-director-enterprise-architecture/executive-brief.md)
Read(.../out/lseg-director-enterprise-architecture/playbook.md)
Read(.../out/lseg-director-enterprise-architecture/interview-cheatsheet.md)
```

Determine exactly **why these files were read during Tenth generation**.

Search the repository for references to previous outputs:

```bash
grep -RniE \
  'out/lseg|out/.*/resume|previous.*resume|existing.*resume|example.*resume|reference.*resume|previous.*artefact|previous.*artifact' \
  skills scripts tests \
  --exclude-dir=.venv \
  --exclude='*.pyc'
```

For every relevant match, record:

- file
- relevant instruction/code
- reason the previous projection is being loaded
- whether its factual content can influence the LLM
- whether it is intended only as a formatting/style example

Do not assume that "example" means safe. Establish the actual context flow.

---

# Phase 3 — Trace the canary facts through the repository

Search the repository for all occurrences of the known canaries:

```bash
grep -RniE \
  '1995.*1999|1999.*1995|Spanish.*Fluent|AWS Certified|Sun Certified|Workday|NetSuite|Coupa|Concur' \
  . \
  --exclude-dir=.venv \
  --exclude-dir=.git \
  --exclude='*.pyc'
```

Classify every relevant occurrence into one of:

```text
CANONICAL
PRIMARY SOURCE
KNOWLEDGE
TARGET JOB DESCRIPTION
RUNTIME ANALYSIS
PROJECTION STRATEGY
PROMPT / SKILL
PREVIOUS PROJECTION
CURRENT PROJECTION
TEST FIXTURE
UNKNOWN
```

Do not make any changes based on these findings.

The purpose is to determine whether each unsupported fact already exists somewhere in the repository.

---

# Phase 4 — Specifically inspect the LSEG projection

Search the previous LSEG artefacts:

```bash
grep -nEi \
  '1995|1999|Spanish|Fluent|AWS|Sun Certified|Workday|NetSuite|Coupa|Concur' \
  out/lseg-director-enterprise-architecture/*.md
```

Determine whether the same unsupported facts found in the Tenth resume already existed in the LSEG outputs.

If they do, record this as a potential provenance chain:

```text
unknown / legacy source
        ↓
LSEG projection
        ↓
Tenth projection
```

Do not call this proven unless the generation/context mechanism also confirms that the LSEG output was available as candidate factual context.

---

# Phase 5 — Inspect projection context assembly

Identify how the model context is assembled immediately before resume generation.

Determine whether the effective context contains any combination of:

```text
canonical/career-record.yaml
canonical-selection.yaml
employment-records.yaml
mind-palace knowledge
portfolio content
target job description
opportunity-analysis.yaml
gap-analysis.yaml
opportunity-fit-report.yaml
projection-strategy.yaml
OKF artefacts
previous opportunity outputs
previous resumes
previous cover letters
previous LinkedIn profiles
```

For each input, establish whether it is:

- factual candidate evidence
- contextual professional knowledge
- target-position information
- generated analysis
- previous projection
- formatting/example material

Pay particular attention to whether previous projections are included in the same factual context as canonical candidate information.

---

# Phase 6 — Investigate target-JD keyword leakage

The Tenth job description explicitly contains:

- Salesforce
- Workday
- NetSuite
- Coupa
- Concur
- ERP
- CRM
- HRIS
- Finance

The generated resume contains several of these exact technologies.

Determine whether the pipeline has a mechanism resembling:

```text
target JD
    ↓
mandatory / strong keywords
    ↓
resume generation
```

and whether those keywords are being treated as candidate capabilities rather than as requirements to be evidenced.

Search for:

```bash
grep -RniE \
  'mandatory.*keyword|strong.*keyword|ATS.*keyword|ATS vocabulary|keyword.*resume|resume.*keyword|extract.*keyword' \
  skills scripts \
  --exclude-dir=.venv \
  --exclude='*.pyc'
```

Determine whether the generation instructions distinguish between:

```text
JOB REQUIREMENT
```

and:

```text
CANDIDATE EVIDENCE
```

This distinction is critical.

The desired conceptual flow is:

```text
Job requirement
      ↓
Search candidate evidence
      ↓
Evidence exists?
   ┌──┴──┐
  YES    NO
   ↓      ↓
Use     gap / transferable capability /
fact    explicitly qualified statement
```

It must not be:

```text
Job requirement
      ↓
Insert keyword into candidate profile
```

Do not implement this correction yet. Only diagnose.

---

# Phase 7 — Check whether canonical selection is actually passed to projection

Establish whether the resume generator explicitly receives:

`out/tenth-ai-lead-enterprise-architect/runtime/canonical-selection.yaml`

as its candidate-fact source.

Do not infer this merely because the file exists.

Find the actual invocation/context mechanism.

Answer:

1. Is canonical selection explicitly loaded?
2. Is it loaded before resume generation?
3. Is its content included in the model context?
4. Is there an instruction that it is authoritative?
5. Are other candidate sources loaded alongside it?
6. Can another source override it?
7. Can the LLM freely choose between conflicting candidate sources?

---

# Phase 8 — Inspect validators

Review:

```text
scripts/canonical_validator.py
scripts/employment_validator.py
skills/projection-validator/SKILL.md
tests/test_projection_validator.py
```

Determine exactly what the validators check.

Specifically establish whether they validate:

- dates
- formal employment titles
- education
- certifications
- languages
- named technologies
- unsupported candidate claims
- target-JD keyword leakage
- provenance of generated claims
- contamination from previous projections

The existing:

```text
canonical-conflict-report.yaml
total_conflicts: 0
```

must not be treated as proof that the generated resume is factually clean.

Determine precisely what that report does and does not validate.

---

# Phase 9 — Build a provenance matrix

Produce a forensic matrix for every canary:

| Fact | Canonical | Selection | Repository source | Runtime context | Previous projection | Prompt/skill | Final output | Validator |
|---|---|---|---|---|---|---|---|---|
| BSc 1995–1999 | | | | | | | | |
| Spanish Fluent | | | | | | | | |
| AWS certification | | | | | | | | |
| Sun SCEA | | | | | | | | |
| Sun SCJP | | | | | | | | |
| Workday | | | | | | | | |
| NetSuite | | | | | | | | |
| Coupa | | | | | | | | |
| Concur | | | | | | | | |
| AWS Certified Solutions Architect | | | | | | | | |
| Sun Certified Enterprise Architect (SCEA) | | | | | | | | |
| Sun Certified Java Programmer (SCJP) | | | | | | | | |
| Defined global enterprise architecture strategy and platform foundations for Agentic AI, multi-agent systems, and automated data workflows across media operations. | | | | | | | | |
| Spearheaded the Code Architecture System (CAS) architecture-as-code blueprints, automating governance verification, compliance auditing, and API contract adherence. | | | | | | | | |


For each cell, record the actual file/path and relevant evidence.

Use:

```text
YES
NO
UNKNOWN
```

where appropriate rather than guessing.

---

# Phase 10 — Determine the contamination class

At the end, classify each unsupported fact into one of these categories:

### A. Source-data problem

The fact exists in an authoritative or potentially authoritative source but is missing/incorrect in canonical.

### B. Knowledge-context problem

The fact exists in non-canonical knowledge and is being treated as candidate evidence without sufficient controls.

### C. Previous-projection contamination

The fact originates in an earlier generated artefact and is being recycled into a later projection.

### D. Target-JD leakage

The fact originates from the target job description or derived keyword analysis and is being transformed into a candidate claim.

### E. Prompt-generation inference

The fact is not present in any available source but the LLM generated it through inference or hallucination.

### F. Validation gap

The fact is detected in the output but existing validators fail to flag it.

Multiple categories may apply to the same fact.

---

# Critical constraints

During this entire investigation:

- DO NOT edit source files.
- DO NOT edit skills.
- DO NOT edit prompts.
- DO NOT edit validators.
- DO NOT regenerate artefacts.
- DO NOT delete previous outputs.
- DO NOT "clean up" the repository.
- DO NOT add tests.
- DO NOT fix discovered defects.
- DO NOT infer that a source is authoritative merely because it contains the information.
- DO NOT treat generated output as evidence of truth.
- DO NOT assume the canary facts came from the LSEG output without tracing the context flow.

This is a forensic investigation only.

---

# Required final report

Return a concise but evidence-based forensic report with these sections:

## 1. Executive finding

State where the unsupported facts are entering the pipeline, if established.

## 2. Provenance matrix

Provide the completed canary matrix.

## 3. Projection context

List the actual inputs supplied to projection generation.

## 4. Previous-projection analysis

Explain exactly why `out/lseg-director-enterprise-architecture/*` was read and whether it could influence factual generation.

## 5. JD keyword analysis

Explain whether target-job requirements can become candidate facts.

## 6. Validator coverage

Explain what the existing validators catch and what they do not catch.

## 7. Root-cause classification

Classify each canary as:

- source-data
- knowledge-context
- previous-projection contamination
- target-JD leakage
- prompt-generation inference
- validation gap
- unknown

## 8. Evidence-backed conclusion

Describe the most likely information-flow defect(s), distinguishing proven findings from hypotheses.

## 9. Remediation candidates

List potential fixes only as recommendations.

Do NOT implement any remediation.

The goal is to leave the repository unchanged and provide enough evidence to decide exactly what should be fixed next.