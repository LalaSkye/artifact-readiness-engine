"""Test: HOLD when receipt is absent on a refusal claim."""
import json
import pytest
from pathlib import Path

from src.artifact_readiness_engine.inspector import inspect_file

HOLD_FILE = Path("examples/hold/missing-receipt.json")


@pytest.mark.skipif(not HOLD_FILE.exists(), reason="missing-receipt.json not present")
def test_hold_missing_receipt_status():
    result = inspect_file(HOLD_FILE)
    assert result["status"] in ("HOLD", "FAIL"), f"Expected HOLD or FAIL, got {result['status']}"


@pytest.mark.skipif(not HOLD_FILE.exists(), reason="missing-receipt.json not present")
def test_hold_missing_receipt_has_issues():
    result = inspect_file(HOLD_FILE)
    assert result["issues"], "Expected at least one issue to be flagged"
