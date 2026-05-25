"""Test: FAIL on an overbroad claim with no evidence and no limits."""
from src.artifact_readiness_engine.inspector import inspect_file

FAIL_FILE = "examples/fail/overbroad-claim.json"


def test_fail_overbroad_status():
    result = inspect_file(FAIL_FILE)
    assert result["status"] == "FAIL", f"Expected FAIL, got {result['status']}"


def test_fail_overbroad_evidence_fit_fails():
    result = inspect_file(FAIL_FILE)
    assert result["scores"]["evidence_fit"]["result"] == "FAIL"


def test_fail_overbroad_claim_limits_fails():
    result = inspect_file(FAIL_FILE)
    assert result["scores"]["claim_limits"]["result"] == "FAIL"
