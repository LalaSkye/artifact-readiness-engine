"""Public API surface tests.

These tests ensure the importable Python API remains stable and documented.
"""
from __future__ import annotations

import artifact_readiness_engine as are
from artifact_readiness_engine import (
    ManifestEntry,
    inspect_by_id,
    inspect_file,
    load_manifest,
    validate_file,
)

EXPECTED_ALL = [
    "ManifestEntry",
    "inspect_by_id",
    "inspect_file",
    "load_manifest",
    "validate_file",
]


def test_public_all_is_exact():
    assert are.__all__ == EXPECTED_ALL


def test_public_version_is_pinned():
    assert are.__version__ == "0.2.0"


def test_public_symbols_import_cleanly():
    assert ManifestEntry is not None
    assert callable(inspect_by_id)
    assert callable(inspect_file)
    assert callable(load_manifest)
    assert callable(validate_file)


def test_load_manifest_returns_manifest_entries():
    entries = load_manifest()
    assert entries
    assert all(isinstance(entry, ManifestEntry) for entry in entries)
    assert {entry.expected_status for entry in entries} >= {"PASS", "HOLD", "FAIL"}


def test_inspect_by_id_round_trip_pass_case():
    result = inspect_by_id("pass-minimal-refusal-receipt")
    assert result["status"] == "PASS"
    assert result["claim_id"] == "refusal-001"
    assert result["issues"] == {}


def test_inspect_by_id_accepts_at_prefix():
    result = inspect_by_id("@hold-missing-receipt")
    assert result["status"] == "HOLD"
    assert result["scores"]["receipt_quality"]["result"] == "HOLD"


def test_validate_file_accepts_path_and_manifest_id():
    assert validate_file("examples/pass/minimal-refusal-receipt.json") is True
    assert validate_file("@pass-minimal-refusal-receipt") is True
