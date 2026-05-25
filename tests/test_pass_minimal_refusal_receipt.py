"""Test: PASS for a minimal complete refusal receipt proof pack."""
from pathlib import Path

import pytest

from artifact_readiness_engine.inspector import inspect_file

PASS_FILE = Path("examples/pass/minimal-refusal-receipt.json")


@pytest.mark.skipif(not PASS_FILE.exists(), reason="minimal-refusal-receipt.json not present")
def test_pass_minimal_refusal_receipt_status():
    result = inspect_file(PASS_FILE)
    assert result["status"] == "PASS"


@pytest.mark.skipif(not PASS_FILE.exists(), reason="minimal-refusal-receipt.json not present")
def test_pass_minimal_refusal_receipt_all_surfaces_pass():
    result = inspect_file(PASS_FILE)
    assert result["issues"] == {}
    assert all(surface["result"] == "PASS" for surface in result["scores"].values())
