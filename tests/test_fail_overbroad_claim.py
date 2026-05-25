"""Test: FAIL for an overbroad claim with missing evidence."""
from pathlib import Path

import pytest

from artifact_readiness_engine.inspector import inspect_file

FAIL_FILE = Path("examples/fail/overbroad-claim.json")


@pytest.mark.skipif(not FAIL_FILE.exists(), reason="overbroad-claim.json not present")
def test_fail_overbroad_claim_status():
    result = inspect_file(FAIL_FILE)
    assert result["status"] == "FAIL"


@pytest.mark.skipif(not FAIL_FILE.exists(), reason="overbroad-claim.json not present")
def test_fail_overbroad_claim_flags_evidence_and_authority():
    result = inspect_file(FAIL_FILE)
    assert result["scores"]["evidence_fit"]["result"] == "FAIL"
    assert result["scores"]["authority_trace"]["result"] == "HOLD"
    assert result["scores"]["condition_clarity"]["result"] == "HOLD"
