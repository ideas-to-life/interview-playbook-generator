Documentation Currency Audit — Pre-Implementation Gate

Objective

Before implementing new changes, perform a complete documentation currency audit of:

* AGENTS.md
* CLAUDE.md
* ARCHITECTURE.md

The objective is to ensure these documents accurately describe the current state of the repository and architecture before any new implementation begins.

This is a documentation audit and update task.

Do not implement the remediation requirements in this task.

Do not modify application logic, tests, skills, prompts, schemas, or runtime behaviour.

⸻

1. Core Principle

The documentation must describe the repository as it exists now, not:

* the intended future architecture;
* assumptions from previous conversations;
* outdated implementation plans;
* historical architecture;
* the remediation requirements that have not yet been implemented.

Use the actual repository, current code, current skills, current configuration, current tests, and current runtime artefacts as the source of truth.

Where documentation and implementation disagree:

Treat the implementation as the current-state authority and update the documentation accordingly, unless the discrepancy clearly represents an intentional architectural contract already established elsewhere in the repository.

Do not silently invent missing information.

⸻

2. Scope

Audit the entire repository sufficiently to understand the current architecture and operating model.

At minimum inspect:

AGENTS.md
CLAUDE.md
ARCHITECTURE.md
skills/
scripts/
tests/
config/
out/                     # inspect structure and representative runtime artefacts

Also inspect relevant repository-level documentation and configuration files where necessary.

Pay particular attention to the recently implemented canonicalisation architecture:

mind-palace/
    canonical/
    knowledge/
    projections/
    quarantine/

and the current generator architecture involving:

canonical/career-record.yaml
canonical-selection.yaml
canonical-conflict-report.yaml
employment-records.yaml
opportunity-analysis.yaml
gap-analysis.yaml
opportunity-fit-report.yaml
projection-strategy.yaml

Do not assume every listed artefact currently exists or is used. Verify.

⸻

3. Current-State Architecture

Determine and document the actual current information flow.

At minimum establish whether the current system implements:

Canonical career facts
        ↓
Canonical selection
        ↓
Opportunity analysis
        ↓
Projection strategy
        ↓
Projection generation
        ↓
Validation
        ↓
Generated artefacts

Document the actual flow, including any deviations discovered.

Do not document the proposed remediation as if it were already implemented.

⸻

4. Canonical Architecture Audit

Verify how the current implementation handles:

4.1 Canonical source

Determine:

* location of the canonical career record;
* schema/model used;
* loading mechanism;
* validation mechanism;
* authority rules;
* relationship to legacy employment data.

4.2 Canonical selection

Determine:

* how it is generated;
* where it is stored;
* what information it contains;
* which components consume it;
* whether it is currently considered authoritative during projection;
* how selection is frozen or persisted.

4.3 Conflict detection

Determine:

* what canonical-conflict-report.yaml represents;
* what conflicts it detects;
* what it does not detect;
* which code produces it.

Do not describe it as a comprehensive projection factual validator unless the implementation actually supports that claim.

⸻

5. Knowledge / Projection Separation Audit

Verify the current implementation of the separation between:

canonical
knowledge
projections
quarantine

Document:

* what belongs in each tier;
* which direction information is allowed to flow;
* whether projections can currently be consumed by later runs;
* whether generated outputs are structurally excluded from canonical ingestion;
* how quarantine is treated.

Pay particular attention to the invariant:

projection → canonical

must not occur.

If the repository currently enforces only part of this invariant, document the current state accurately.

⸻

6. Opportunity Runtime Architecture

Audit the current runtime artefact model.

Document the actual role of:

canonical-selection.yaml
opportunity-analysis.yaml
gap-analysis.yaml
opportunity-fit-report.yaml
projection-strategy.yaml
interview-strategy.yaml

For each, establish:

1. Who creates it?
2. What inputs does it consume?
3. Who consumes it afterwards?
4. Is it authoritative, analytical, strategic, or presentational?
5. Can it contain candidate facts?
6. Can it override canonical facts?

Do not infer these properties from filenames. Verify them from implementation.

⸻

7. Projection Architecture Audit

Determine how the current projection skills work.

Inspect the relevant skills and document:

* resume generation;
* ATS resume generation;
* recruiter resume generation;
* cover letter generation;
* LinkedIn generation;
* executive brief;
* opportunity alignment;
* interview playbook;
* interview cheat sheet.

Determine what inputs each projection currently consumes.

Specifically establish whether projections currently consume:

canonical-selection
target JD
opportunity analysis
gap analysis
projection strategy
previous projections
other generated artefacts
mind-palace knowledge

Document actual behaviour.

⸻

8. Validation Architecture Audit

Review the current validators and document their actual responsibilities.

At minimum inspect:

scripts/canonical_validator.py
scripts/employment_validator.py

and relevant validation skills/tests.

Document:

* what is validated;
* what is deterministic;
* what is regex-based;
* what is schema-based;
* what is LLM-based;
* what is not currently validated;
* what the current test suite covers.

Do not claim capabilities that are only planned.

⸻

9. Testing Architecture Audit

Inspect the current test suite.

Determine:

* number and type of tests;
* major test modules;
* canonicalisation tests;
* selection tests;
* employment validation tests;
* projection tests;
* forensic regression tests;
* integration tests.

Document important invariants already protected by tests.

Do not modify tests in this task.

⸻

10. Recent Forensic Findings

The repository has recently undergone a forensic diagnostic of the Tenth AI Lead Enterprise Architect generation.

The documentation should accurately reflect the current discovered state, where appropriate, without prematurely documenting the remediation as implemented.

The diagnostic established:

Finding A — Partial canonical-selection context

The projection generation run loaded only part of canonical-selection.yaml, leaving education and certification information outside the active model context.

Finding B — Previous projection contamination

Previous opportunity outputs under:

out/lseg-director-enterprise-architecture/

were read as structural references during another opportunity generation and influenced generated content.

Finding C — JD keyword leakage

Target-JD terms such as:

Workday
NetSuite
Coupa
Concur

entered ATS vocabulary and were subsequently treated as candidate-relevant keywords without sufficient evidence separation.

Finding D — Validation gaps

Current validation does not comprehensively verify:

* education dates;
* certifications;
* language proficiency;
* named technology claims;
* cross-opportunity projection contamination.

Document these as known current-state limitations, not as already-remediated defects.

⸻

11. AGENTS.md Requirements

Review AGENTS.md as the operational contract for coding agents.

Ensure it accurately describes:

* repository purpose;
* important directory structure;
* current architecture;
* canonical data rules;
* information-flow rules currently enforced;
* testing expectations;
* validation expectations;
* safe handling of generated artefacts;
* relevant commands;
* important invariants;
* known limitations that agents must understand.

The document should help an agent safely modify the repository without accidentally violating the canonical architecture.

Do not turn AGENTS.md into a duplicate of ARCHITECTURE.md.

Prefer:

AGENTS.md = operational rules for agents
ARCHITECTURE.md = system architecture and design
CLAUDE.md = Claude-specific operating guidance

where that distinction matches the existing repository conventions.

⸻

12. CLAUDE.md Requirements

Review CLAUDE.md for:

* stale paths;
* obsolete workflows;
* outdated commands;
* obsolete architecture;
* references to legacy data sources;
* incorrect assumptions about canonical facts;
* outdated generation workflow;
* outdated validation workflow;
* duplicated or contradictory instructions.

Ensure it is consistent with:

AGENTS.md
ARCHITECTURE.md

Do not allow the three documents to establish conflicting rules.

If CLAUDE.md contains Claude-specific operational instructions, preserve them where still valid.

⸻

13. ARCHITECTURE.md Requirements

Review ARCHITECTURE.md as the authoritative architectural description.

It should describe:

1. System purpose
2. Major components
3. Repository structure
4. Canonical data architecture
5. Knowledge architecture
6. Opportunity runtime
7. Projection architecture
8. Validation architecture
9. Information-flow boundaries
10. Testing architecture
11. Current limitations
12. Important architectural invariants

The architecture document must distinguish clearly between:

CURRENT

and:

PROPOSED / FUTURE

Do not present the remediation requirements as implemented.

⸻

14. Cross-Document Consistency

After auditing the three documents, compare them against one another.

Identify contradictions such as:

* different canonical paths;
* different descriptions of the source of truth;
* different definitions of projection;
* different validation claims;
* different commands;
* different directory structures;
* obsolete workflow descriptions;
* conflicting information-flow rules.

Resolve these inconsistencies based on the actual repository implementation.

The three documents must not contradict each other.

⸻

15. Documentation Quality Requirements

The updated documentation should be:

* factual;
* concise;
* technically precise;
* current;
* actionable;
* internally consistent;
* explicit about boundaries;
* explicit about known limitations.

Avoid:

* marketing language;
* speculative architecture;
* undocumented capabilities;
* aspirational claims presented as current;
* excessive duplication;
* implementation details that are irrelevant to agents or architecture readers.

⸻

16. Required Audit Report Before Editing

Before making any edits, produce a short report containing:

A. Current-state summary

What the repository currently does.

B. AGENTS.md findings

* correct/current sections;
* stale sections;
* missing sections;
* contradictory sections.

C. CLAUDE.md findings

Same structure.

D. ARCHITECTURE.md findings

Same structure.

E. Cross-document inconsistencies

List contradictions between the three files.

F. Recommended documentation changes

List exact changes required.

Do not implement application changes.

⸻

17. Editing Rules

After completing the audit:

1. Update only:
    * AGENTS.md
    * CLAUDE.md
    * ARCHITECTURE.md
2. Do not modify:
    * application code;
    * skills;
    * prompts;
    * validators;
    * tests;
    * canonical data;
    * runtime artefacts.
3. Preserve useful existing documentation where it remains accurate.
4. Remove or rewrite documentation that describes obsolete architecture.
5. Do not document the remediation specification as implemented.
6. If a capability is uncertain, inspect the implementation before documenting it.

⸻

18. Final Verification

After updating the three documents:

Verify repository consistency

Confirm that all documented paths exist or are explicitly identified as generated/runtime paths.

Verify architecture consistency

Confirm that the information-flow description matches the actual implementation.

Verify command accuracy

Confirm documented commands actually exist and are still valid.

Verify canonical terminology

Use the repository’s current terminology consistently.

Verify future-state separation

Ensure proposed remediation is not accidentally described as current implementation.

Verify tests

Run the existing test suite if appropriate, but do not modify tests.

The documentation update must not alter application behaviour.

⸻

19. Final Deliverable

Return:

Documentation Audit
-------------------
AGENTS.md       PASS / UPDATED / ISSUES
CLAUDE.md      PASS / UPDATED / ISSUES
ARCHITECTURE.md PASS / UPDATED / ISSUES
Cross-document consistency: PASS / ISSUES
Current architecture accurately documented: YES / NO
Known limitations accurately documented: YES / NO
Application code modified: NO
Tests modified: NO

Then provide a concise summary of:

* what documentation was changed;
* what stale information was removed;
* what current architecture was clarified;
* what known limitations were documented;
* what remains intentionally future-state.

This task is a documentation currency gate before implementation begins.