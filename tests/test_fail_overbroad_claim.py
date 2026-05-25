"""Test: FAIL when claim is overbroad and limits are absent."""

from pathlib import Path
from artifact_readiness_engine import inspect_proof_pack


FAIL_FIXTURE = Path("examples/fail/overbroad-claim.json")


def test_fail_overall():
    result = inspect_proof_pack(FAIL_FIXTURE)
    assert result.overall_status == "FAIL", (
        f"Expected FAIL, got {result.overall_status}"
    )


def test_evidence_or_limits_fail():
    result = inspect_proof_pack(FAIL_FIXTURE)
    fail_dims = {d.name for d in result.dimensions if d.status == "FAIL"}
    assert fail_dims, "Expected at least one FAIL dimension"
