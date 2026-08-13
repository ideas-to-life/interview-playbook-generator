# Spec: Career History Evidence Integrity (P0 Refinement)

## Objective

Ensure that all factual employment-history metadata (Employer, Job Title, Start Date, End Date, Status, Location) in generated career-projection artefacts is strictly derived from canonical evidence in `okf/`.

The generator may tailor presentation, bullet selection, and emphasis for a target opportunity, but it MUST NOT alter, infer, normalize, approximate, reconstruct, split, merge, or fabricate employment-history facts.

### Defect Addressed

In recent projection runs, the projection layer reconstructed plausible career chronologies (e.g. WPP Media 2022–Present, BBC Studios 2020–2022, BAT R&D 2016–2020) instead of rendering the evidenced canonical chronology (WPP Media Dec 2025–Present, BBC Studios Nov 2021–Nov 2025, BAT 2011–2021). This refinement establishes a hard evidence-integrity boundary: *Career history is evidence, not projection.*

---

## Tech Stack & Commands

- **Language / Runtime**: Python 3.13, Pytest, YAML, Markdown Skills specification.
- **Commands**:
  ```bash
  # Run full test suite
  pytest tests/

  # Run dedicated evidence integrity regression suite
  pytest tests/test_career_evidence_integrity.py

  # Run lint checks
  pytest tests/test_lint.py
  ```

---

## Project Structure & Touched Files

```
skills/
├── portfolio-ingestor/SKILL.md         → Expose authoritative canonical employment records in okf/
├── projection-validator/SKILL.md       → Add employment metadata validation gate (PASS / FAIL)
├── brand-validator/SKILL.md            → Validate cross-artefact employment metadata consistency
├── resume-projection/SKILL.md          → Deterministic header rendering from canonical records
├── cover-letter-projection/SKILL.md    → Deterministic employment reference rendering
├── linkedin-projection/SKILL.md        → Deterministic profile experience section rendering
├── executive-brief-view/SKILL.md       → Deterministic career timeline rendering
├── playbook-assembler/SKILL.md         → Deterministic background summary rendering
└── playbook-orchestrator/SKILL.md      → Pipeline orchestration & pre/post-projection integrity check

okf/                                    → Shared canonical knowledge bundle
└── employment-records.yaml             → Authoritative employment metadata node

AGENTS.md                               → Update governing rules with Career Evidence Integrity rule
docs/superpowers/specs/2026-08-13-career-evidence-integrity-spec.md → This specification document
tests/test_career_evidence_integrity.py → Head of Enterprise Architecture regression test suite
```

---

## Code Style & Implementation Architecture

### 1. Canonical Employment Record Schema (`okf/employment-records.yaml`)

```yaml
employment_records:
  - id: emp-wpp-2025
    employer: "WPP Media"
    title: "Senior Director, Agentic AI Systems Architecture"
    start_date: "Dec 2025"
    end_date: null
    status: "current"
    location: "London, UK"
    sources:
      - cv-2026
    approved_aliases:
      - "Senior Director, Agentic AI Systems Architecture"
  - id: emp-bbc-2021
    employer: "BBC Studios"
    title: "Lead Enterprise Architect"
    start_date: "Nov 2021"
    end_date: "Nov 2025"
    status: "former"
    location: "London, UK"
    sources:
      - cv-2026
    approved_aliases:
      - "Lead Enterprise Architect"
  - id: emp-bat-2011
    employer: "British American Tobacco"
    title: "Enterprise Architect & Global Solution Architect"
    start_date: "2011"
    end_date: "2021"
    status: "former"
    location: "London, UK"
    sources:
      - cv-2026
    approved_aliases:
      - "Enterprise Architect & Global Solution Architect"
```

### 2. Deterministic Rendering Pattern

Header templates consume canonical employment records directly rather than relying on free-form LLM generation:

```python
def render_employment_header(record: dict) -> str:
    """Deterministically formats an employment record header."""
    end_str = record["end_date"] if record["end_date"] else "Present"
    return f"### {record['employer']} | {record['title']}\n*{record['start_date']} – {end_str} | {record['location']}*"
```

### 3. Validation Logic (`validate_employment_history`)

```python
def validate_employment_history(canonical_records: list[dict], artefact_content: str) -> dict:
    """Checks generated artefact against canonical employment records.
    
    Hard failure if:
    - Employer is renamed or missing from canonical evidence
    - Dates are modified or approximated (e.g. 2022 instead of Dec 2025)
    - Job titles are substituted with target JD terms without canonical approval
    - Contiguous periods are reconstructed or split/merged without canonical backing
    """
    violations = []
    # Check each canonical employer presence and attribute exactness
    for rec in canonical_records:
        employer = rec["employer"]
        if employer not in artefact_content and rec["status"] == "current":
            violations.append(f"Current employer '{employer}' missing from artefact.")
        # Detect date mutations (e.g., matching employer with wrong start/end date)
        ...
    return {
        "status": "PASS" if not violations else "FAIL",
        "violations": violations
    }
```

---

## Testing Strategy

- **Test Runner**: Pytest (`pytest tests/`)
- **Dedicated Regression Suite**: `tests/test_career_evidence_integrity.py`
- **Head of Enterprise Architecture Regression Test**:
  - `WPP start == Dec 2025`, `end == Present`, `title == Senior Director, Agentic AI Systems Architecture`
  - `BBC start == Nov 2021`, `end == Nov 2025`, `title == Lead Enterprise Architect`
  - `BAT period == 2011–2021`, `title == Enterprise Architect & Global Solution Architect`
  - Rejection of fabricated chronology: `WPP 2022–Present`, `BBC 2020–2022`, `BAT R&D 2016–2020`
- **Cross-Artefact Validation**:
  - Assert that all 9 generated projection views (`resume-executive.md`, `resume-ats.md`, `resume-recruiter.md`, `cover-letter.md`, `linkedin-profile.md`, `executive-brief.md`, `playbook.md`, `interview-cheatsheet.md`, `opportunity-alignment.md`) render identical, factually valid employment headers.

---

## Boundaries

- **Always do**:
  - Render employment metadata headers deterministically from canonical records in `okf/`.
  - Validate all generated projection artefacts against canonical employment records in `projection-validator` and `brand-validator`.
  - Fail the build/validation gate on any employment metadata mutation or fabrication.
- **Ask first**:
  - Introducing new approved title aliases into `okf/employment-records.yaml`.
  - Changing canonical employment record schema or source mappings.
- **Never do**:
  - Allow the LLM to invent, approximate, reconstruct, split, or merge employment dates or job titles.
  - Allow target JD terms to alter candidate employer names, titles, or dates.
  - Hardcode candidate-specific date exceptions in generic Python logic.

---

## Success Criteria

1. Canonical employment records are explicitly identifiable in `okf/employment-records.yaml`.
2. Employer, title, start date, end date, and status are treated as immutable evidence.
3. Projection cannot infer, reconstruct, or approximate employment dates or job titles.
4. Target JDs cannot modify candidate employment metadata.
5. Deterministic employment metadata renderer and validator are implemented.
6. Validation gate fails strictly (HARD FAIL) on employment evidence violations.
7. All major projection artefacts render consistent, validated canonical employment records.
8. Head of Enterprise Architecture regression test suite passes all assertions.
9. Zero regressions across the entire test suite (`pytest tests/`).

---

## Resolved Open Questions & Key Decisions

1. **Canonical Employment Record Ingestion**: `portfolio-ingestor` will extract structured employment records from portfolio sources (e.g. CVs) and emit `okf/employment-records.yaml` with explicit source footnotes.
2. **Date Rendering Policy**: Exact string matching or explicit deterministic display transformations (e.g. `Dec 2025` to `December 2025` if configured), strictly prohibiting year approximations (e.g., `2022–Present` when source specifies `Dec 2025–Present`).
