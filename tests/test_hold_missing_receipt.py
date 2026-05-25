"""Test: HOLD when receipt is absent on a refusal claim."""
from pathlib import Path

import pytest

from artifact_readiness_engine.inspector import inspect_file

HOLD_FILE = Path("examples/hold/missing-receipt.json")


@pytest.mark.skipif(not HOLD_FILE.exists(), reason="missing-receipt.json not present")
def test_hold_missing_receipt_status():
    result = inspect_file(HOLD_FILE)
    assert result["status"] == "HOLD"


@pytest.mark.skipif(not HOLD_FILE.exists(), reason="missing-receipt.json not present")
def test_hold_missing_receipt_flags_expected_surfaces():
    result = inspect_file(HOLD_FILE)
    assert result["scores"]["receipt_quality"]["result"] == "HOLD"
    assert result["scores"]["replayability"]["result"] == "HOLD"
    assert result["scores"]["downstream_effect"]["result"] == "HOLD"
