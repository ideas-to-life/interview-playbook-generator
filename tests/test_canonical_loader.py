"""Tests for Canonical Career Record Loader."""

import pytest
import tempfile
import time
from pathlib import Path
from scripts.canonical_loader import (
    load_canonical_career_record,
    resolve_canonical_path,
    CanonicalRecordError,
)


def test_load_canonical_career_record_success():
    """Test loading valid canonical career record from repository configuration."""
    start = time.time()
    record = load_canonical_career_record()
    duration = time.time() - start

    assert duration < 1.0, f"Loading took too long: {duration:.3f}s"
    assert len(record.career) >= 11
    assert len(record.education) >= 2
    assert len(record.certifications) >= 5

    # Check BBC Studios entry (CAR-03)
    bbc = record.get_career_entry("CAR-03")
    assert bbc is not None
    assert bbc.formal_title == "Lead Enterprise Architect - Technology Transformation Group"
    assert bbc.employer == "BBC Studios"
    assert bbc.start_date == "Nov 2023"
    assert bbc.end_date == "30 Nov 2025"
    assert len(bbc.acting_responsibilities) > 0
    assert "Head of Architecture" in bbc.acting_responsibilities[0]

    # Check Education entry (EDU-01)
    edu1 = record.get_education_entry("EDU-01")
    assert edu1 is not None
    assert "Mogi das Cruzes" in edu1.institution
    assert "Bachelor" in edu1.degree_level
    assert "Master" not in edu1.degree_level


def test_fast_fail_on_missing_file():
    """Test fast fail (<1s) when canonical record does not exist."""
    start = time.time()
    with pytest.raises(CanonicalRecordError) as exc_info:
        load_canonical_career_record(record_path="/tmp/nonexistent_career_record.yaml")
    duration = time.time() - start

    assert duration < 1.0
    assert "Canonical career record not found" in str(exc_info.value)
    assert "Refusing to fallback" in str(exc_info.value)


def test_fast_fail_on_malformed_yaml():
    """Test fast fail when canonical record contains malformed YAML."""
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write("invalid: yaml: [unclosed bracket\n")
        temp_path = f.name

    try:
        start = time.time()
        with pytest.raises(CanonicalRecordError) as exc_info:
            load_canonical_career_record(record_path=temp_path)
        duration = time.time() - start
        assert duration < 1.0
        assert "Failed to parse YAML" in str(exc_info.value)
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_unresolved_questions_querying():
    """Test separating resolved from unresolved canonical items."""
    record = load_canonical_career_record()
    resolved = record.get_resolved_questions()
    unresolved = record.get_unresolved_questions()

    assert len(resolved) >= 4
    # All verified in mind-palace are resolved
    for q in resolved:
        assert q.current_status == "resolved"
        assert q.resolution is not None
