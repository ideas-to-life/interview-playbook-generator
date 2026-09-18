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

