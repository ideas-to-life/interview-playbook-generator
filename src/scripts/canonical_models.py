"""Data models and validation structures for Canonical Career Record.

Represents immutable canonical professional facts loaded from career-record.yaml.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any


@dataclass
class EvidenceRef:
    source: str
    entry_details: Optional[str] = None


@dataclass
class CareerEntry:
    id: str
    employer: str
    formal_title: str
    start_date: str
    end_date: Optional[str] = None
    status: str = "former"  # 'current' | 'former'
    location: str = "London, UK"
    engagement_type: str = "direct_employment"  # 'direct_employment' | 'consultancy' | 'independent_advisory'
    client: Optional[str] = None
    approved_aliases: List[str] = field(default_factory=list)
    operational_scope: List[str] = field(default_factory=list)
    acting_responsibilities: List[str] = field(default_factory=list)
    responsibilities_scope: List[str] = field(default_factory=list)
    verified_accomplishments: List[str] = field(default_factory=list)
    evidence: List[EvidenceRef] = field(default_factory=list)

    def all_scope_items(self) -> List[str]:
        """Returns all combined operational, acting, and responsibilities scopes."""
        combined = []
        combined.extend(self.operational_scope)
        combined.extend(self.acting_responsibilities)
        combined.extend(self.responsibilities_scope)
        return combined

    def is_consultancy(self) -> bool:
        """Returns True if this engagement was a consultancy or contracted to a client."""
        return self.engagement_type == "consultancy" or bool(self.client)

    def display_relationship(self) -> str:
        """Returns formatted string distinguishing direct, consultancy, or advisory."""
        if self.client and self.engagement_type == "consultancy":
            return f"{self.employer} (Consultancy contracted to {self.client})"
        elif self.engagement_type == "independent_advisory":
            return f"{self.employer} (Independent Advisory)"
        elif self.engagement_type == "direct_employment":
            return f"{self.employer} (Direct Corporate Employment)"
        return self.employer


@dataclass
class EducationEntry:
    id: str
    institution: str
    degree_name: str
    degree_level: str
    field_of_study: str
    end_year: Union[int, str]
    location: str = ""
    start_year: Optional[Union[int, str]] = None
    status: str = "verified"
    notes: Optional[str] = None
    evidence: List[EvidenceRef] = field(default_factory=list)


@dataclass
class CertificationEntry:
    id: str
    name: str
    issuing_body: str
    year: Optional[Union[int, str]] = None
    status: str = "verified"
    evidence: List[EvidenceRef] = field(default_factory=list)


@dataclass
class UnresolvedQuestion:
    id: str
    topic: str
    question: str
    current_status: str  # 'resolved' | 'unresolved'
    resolution: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class CanonicalCareerRecord:
    metadata: Dict[str, Any]
    identity: Dict[str, Any]
    education: List[EducationEntry] = field(default_factory=list)
    career: List[CareerEntry] = field(default_factory=list)
    certifications: List[CertificationEntry] = field(default_factory=list)
    unresolved_questions: List[UnresolvedQuestion] = field(default_factory=list)

    def get_career_entry(self, entry_id: str) -> Optional[CareerEntry]:
        for entry in self.career:
            if entry.id.lower() == entry_id.lower():
                return entry
        return None

    def get_education_entry(self, entry_id: str) -> Optional[EducationEntry]:
        for entry in self.education:
            if entry.id.lower() == entry_id.lower():
                return entry
        return None

    def get_certification_entry(self, entry_id: str) -> Optional[CertificationEntry]:
        for entry in self.certifications:
            if entry.id.lower() == entry_id.lower():
                return entry
        return None

    def get_resolved_questions(self) -> List[UnresolvedQuestion]:
        return [q for q in self.unresolved_questions if q.current_status == "resolved"]

    def get_unresolved_questions(self) -> List[UnresolvedQuestion]:
        return [q for q in self.unresolved_questions if q.current_status != "resolved"]

    def filter_unresolved_for_external(self) -> List[UnresolvedQuestion]:
        """Returns only resolved questions safe for external collateral; genuinely unresolved items are excluded."""
        return [q for q in self.unresolved_questions if q.current_status.lower() == "resolved"]

    def filter_unresolved_for_coaching(self) -> List[Dict[str, Any]]:
        """Surfaces genuinely unresolved questions flagged [NEEDS CONFIRMATION] for coaching artifacts."""
        return [
            {
                "id": q.id,
                "topic": q.topic,
                "question": q.question,
                "flag": "[NEEDS CONFIRMATION]",
                "status": "unresolved",
                "notes": q.notes,
                "coaching_guidance": f"[NEEDS CONFIRMATION] Candidate verification required: {q.question}"
            }
            for q in self.unresolved_questions
            if q.current_status.lower() != "resolved"
        ]


@dataclass
class LanguageEntry:
    language: str
    proficiency: str
    status: str = "verified"
    notes: Optional[str] = None


@dataclass
class ValidationFinding:
    source_file: str
    category: str  # 'education' | 'certification' | 'language' | 'employment' | 'technology' | 'isolation'
    severity: str  # 'FATAL' | 'SANITIZED' | 'WARNING'
    generated_claim: str
    reason: str
    action_taken: str  # 'sanitized_in_place' | 'validation_failure_block' | 'warning_logged'
    canonical_baseline: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "source_file": self.source_file,
            "category": self.category,
            "severity": self.severity,
            "generated_claim": self.generated_claim,
            "reason": self.reason,
            "action_taken": self.action_taken,
        }
        if self.canonical_baseline:
            d["canonical_baseline"] = self.canonical_baseline
        return d


@dataclass
class CheckDetail:
    status: str  # 'PASSED' | 'FAILED' | 'SANITIZED'
    details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {"status": self.status}
        if self.details:
            d["details"] = self.details
        return d


@dataclass
class ValidationSummary:
    total_files_audited: int
    total_findings: int
    sanitized_count: int
    unresolved_defects: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_files_audited": self.total_files_audited,
            "total_findings": self.total_findings,
            "sanitized_count": self.sanitized_count,
            "unresolved_defects": self.unresolved_defects,
        }


@dataclass
class ProjectionValidationReport:
    target_slug: str
    evaluated_at: str
    overall_status: str  # 'PASSED' | 'FAILED' | 'PASSED_WITH_SANITIZATION'
    validator_version: str = "1.0.0"
    summary: Optional[ValidationSummary] = None
    checks: Dict[str, CheckDetail] = field(default_factory=dict)
    findings: List[ValidationFinding] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_metadata": {
                "target_slug": self.target_slug,
                "evaluated_at": self.evaluated_at,
                "overall_status": self.overall_status,
                "validator_version": self.validator_version,
            },
            "summary": self.summary.to_dict() if self.summary else {
                "total_files_audited": 0,
                "total_findings": len(self.findings),
                "sanitized_count": sum(1 for f in self.findings if f.severity == "SANITIZED"),
                "unresolved_defects": sum(1 for f in self.findings if f.severity == "FATAL"),
            },
            "checks": {k: v.to_dict() for k, v in self.checks.items()},
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass
class ATSEvidencedTerm:
    term: str
    evidence_source: str  # 'career_record' | 'okf_capability' | 'okf_evidence_card'
    evidence_ref: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "term": self.term,
            "evidence_source": self.evidence_source,
            "evidence_ref": self.evidence_ref,
        }


@dataclass
class ATSRequiredJobTerm:
    term: str
    status: str = "unmatched_requirement_gap"
    recommended_framing: str = "transferable_capability"  # 'explicit_gap' | 'transferable_capability' | 'adjacent_experience'

    def to_dict(self) -> Dict[str, Any]:
        return {
            "term": self.term,
            "status": self.status,
            "recommended_framing": self.recommended_framing,
        }


@dataclass
class ATSVocabularyPartition:
    candidate_evidenced_vocabulary: List[ATSEvidencedTerm] = field(default_factory=list)
    required_job_vocabulary: List[ATSRequiredJobTerm] = field(default_factory=list)
    scoring_rules: Dict[str, Any] = field(default_factory=lambda: {
        "evidenced_credit_multiplier": 1.0,
        "unevidenced_credit_multiplier": 0.0,
        "unevidenced_direct_claim_penalty": "integrity_defect_failure",
    })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_evidenced_vocabulary": [t.to_dict() for t in self.candidate_evidenced_vocabulary],
            "required_job_vocabulary": [t.to_dict() for t in self.required_job_vocabulary],
            "scoring_rules": self.scoring_rules,
        }


