# Data Model: Canonical Career Record Integration

**Feature**: `005-canonical-record-integration`  
**Status**: Completed  
**Date**: 2026-09-18  

This document formalizes the entity structures, attributes, validation rules, and lifecycle transitions for integrating the canonical career record into the Interview Playbook Generator.

---

## 1. Entity Definitions & Attributes

### 1.1 CanonicalCareerRecord (Root Model)
Authoritative entity loaded from `mind-palace/canonical/career-record.yaml`. Read-only at runtime.

| Field | Type | Description | Required |
|---|---|---|---|
| `metadata` | `RecordMetadata` | Schema version, verification timestamp, change policy | Yes |
| `identity` | `IdentityProfile` | Candidate name, contact location, primary domains, languages | Yes |
| `education` | List[`EducationEntry`] | Verified academic history | Yes |
| `career` | List[`CareerEntry`] | Verified professional chronology, roles, and scopes | Yes |
| `certifications` | List[`CertificationEntry`] | Verified professional qualifications | Yes |
| `unresolved_questions` | List[`UnresolvedQuestion`] | Tracked ambiguities and verification status | No |

---

### 1.2 CareerEntry
Represents an immutable professional engagement.

| Field | Type | Description | Required |
|---|---|---|---|
| `id` | String | Unique identifier (e.g., `CAR-01`, `CAR-02`) | Yes |
| `employer` | String | Legal corporate employer or firm | Yes |
| `client` | String | Contracting client organization (if consultancy) | Optional |
| `engagement_type` | Enum | `direct_employment`, `consultancy`, `independent_advisory` | Yes |
| `formal_title` | String | Formal contracted job title | Yes |
| `approved_aliases` | List[String] | Permitted formatting aliases (e.g. punctuation variants) | Yes |
| `start_date` | String | Verified start date (e.g., `"Nov 2023"`, `"1998-05"`) | Yes |
| `end_date` | String / Null | Verified end date or `null` if current | Yes |
| `status` | Enum | `current`, `former` | Yes |
| `location` | String | Work location (e.g., `"London Area, United Kingdom"`) | Yes |
| `operational_scope` | List[String] | Operational context, acting responsibilities, governance scopes | Optional |
| `verified_accomplishments` | List[String] | Accomplishments explicitly supported by primary evidence | Optional |
| `evidence` | List[EvidenceRef] | Primary source citations backing this entry | Yes |

---

### 1.3 EducationEntry
Represents a verified academic qualification. Treated as high-sensitivity.

| Field | Type | Description | Required |
|---|---|---|---|
| `id` | String | Unique identifier (e.g., `EDU-01`) | Yes |
| `institution` | String | Academic institution name (e.g., `"Universidade de Mogi das Cruzes"`) | Yes |
| `location` | String | Institution location | Yes |
| `degree_name` | String | Original degree title in language of origin | Yes |
| `degree_level` | String | Standardized level (e.g., `"Bachelor of Science (BSc)"`) | Yes |
| `field_of_study` | String | Academic discipline | Yes |
| `start_year` | Integer / String | Start year | Optional |
| `end_year` | Integer / String | Graduation year | Yes |
| `status` | Enum | `verified`, `draft` | Yes |
| `notes` | String | Explicit guardrails (e.g. refuting MSc claims) | Optional |

---

### 1.4 CertificationEntry
Represents a verified professional accreditation.

| Field | Type | Description | Required |
|---|---|---|---|
| `id` | String | Unique identifier (e.g., `CERT-01`) | Yes |
| `name` | String | Official certification name | Yes |
| `issuing_body` | String | Granting organization | Yes |
| `year` | Integer / String | Year issued | Optional |
| `status` | Enum | `verified`, `draft` | Yes |

---

### 1.5 UnresolvedQuestion
Tracks ambiguities or unverified claims awaiting human review.

| Field | Type | Description | Required |
|---|---|---|---|
| `id` | String | Unique identifier (e.g., `UNRES-01`) | Yes |
| `topic` | String | Professional domain or specific role | Yes |
| `question` | String | Description of the ambiguity | Yes |
| `current_status` | Enum | `resolved`, `unresolved` | Yes |
| `resolution` | String | Factual conclusion if resolved | Optional |

---

### 1.6 CanonicalSelectionRecord (Runtime Entity)
Persisted at `out/<target-slug>/runtime/canonical-selection.yaml` to decouple Activity A (selection) from Activity B (projection).

| Field | Type | Description | Required |
|---|---|---|---|
| `target_slug` | String | Target opportunity slug | Yes |
| `generated_at` | DateTime | Timestamp of selection | Yes |
| `source_canonical_record` | String | Path to loaded `career-record.yaml` | Yes |
| `selected_roles` | List[SelectedRole] | Canonical career entries relevant to opportunity | Yes |
| `selected_education` | List[String] | Selected `EDU-xx` IDs | Yes |
| `selected_certifications` | List[String] | Selected `CERT-xx` IDs | Yes |
| `flagged_unresolved_items` | List[FlaggedUnresolved] | Items surfaced for internal coaching with `[NEEDS CONFIRMATION]` | Optional |

---

### 1.7 CanonicalConflictReport (Runtime Audit Entity)
Persisted at `out/<target-slug>/runtime/canonical-conflict-report.yaml`.

| Field | Type | Description | Required |
|---|---|---|---|
| `target_slug` | String | Target opportunity slug | Yes |
| `evaluated_at` | DateTime | Audit timestamp | Yes |
| `total_conflicts` | Integer | Total number of discrepancies detected | Yes |
| `conflicts` | List[ConflictItem] | Array of specific conflicting claims | Yes |

#### ConflictItem Structure:
- `source_file`: Path of the secondary/derived document.
- `field_type`: `formal_title`, `degree_level`, `employer_relationship`, `dates`.
- `conflicting_claim`: Prose or value found in secondary source.
- `canonical_fact`: Authoritative fact from `career-record.yaml`.
- `action_taken`: `"canonical_override"`.

---

## 2. Validation & Integrity Rules

1. **Title Inflation Invariant**:
   `operational_scope` and `acting_responsibilities` MUST NEVER overwrite or append to `formal_title`. A candidate may only be credited with a leadership title if `formal_title` in the canonical record matches that title.
2. **Education Degree Inflation Invariant**:
   `degree_level` is strictly immutable. If `degree_level` is Bachelor of Science, generated output MUST NOT emit Master of Science (MSc) or PhD under any circumstances.
3. **Employer Relationship Invariant**:
   If `engagement_type` is `consultancy`, the firm is the employer and the client is the contracting recipient. They MUST NOT be represented as simultaneous, competing direct employers.
4. **Quarantine Exclusion Invariant**:
   Any file path containing `/quarantine/` or `quarantine/` is rejected by the loader and factual ingestion pipeline.
5. **Unresolved Question Policy**:
   - `current_status: resolved` → Usable as verified factual evidence.
   - `current_status: unresolved` → Omitted from external projections; flagged with `[NEEDS CONFIRMATION]` in internal coaching artifacts.
