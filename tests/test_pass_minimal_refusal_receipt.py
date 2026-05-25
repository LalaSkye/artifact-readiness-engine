"""Test: PASS on a minimal but complete refusal receipt proof pack."""

from pathlib import Path
from artifact_readiness_engine import inspect_proof_pack


PASS_FIXTURE = Path("examples/pass/minimal-refusal-receipt.json")


def test_pass_overall():
    result = inspect_proof_pack(PASS_FIXTURE)
    assert result.overall_status == "PASS", (
        f"Expected PASS, got {result.overall_status}\n"
        + "\n".join(f"  {d.name}: {d.status} — {d.reason}" for d in result.dimensions)
    )


def test_no_fail_dimensions():
    result = inspect_proof_pack(PASS_FIXTURE)
    fail_dims = [d for d in result.dimensions if d.status == "FAIL"]
    assert not fail_dims, f"Unexpected FAIL dimensions: {[d.name for d in fail_dims]}"
