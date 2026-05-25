"""Test: HOLD when receipt is missing on a refusal claim."""

import json
from pathlib import Path
from artifact_readiness_engine import inspect_proof_pack


HOLD_FIXTURE = Path("examples/hold/missing-receipt.json")


def test_hold_missing_receipt_overall():
    result = inspect_proof_pack(HOLD_FIXTURE)
    assert result.overall_status == "HOLD", (
        f"Expected HOLD, got {result.overall_status}"
    )


def test_receipt_quality_fail_or_hold():
    result = inspect_proof_pack(HOLD_FIXTURE)
    receipt_dim = next(d for d in result.dimensions if d.name == "receipt_quality")
    assert receipt_dim.status in ("HOLD", "FAIL"), (
        f"Expected receipt_quality to be HOLD or FAIL, got {receipt_dim.status}"
    )


def test_replayability_hold():
    result = inspect_proof_pack(HOLD_FIXTURE)
    replay_dim = next(d for d in result.dimensions if d.name == "replayability")
    assert replay_dim.status in ("HOLD", "FAIL")
