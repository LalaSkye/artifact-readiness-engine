"""Golden report stability tests.

These tests make the receipt registry self-verifying:
- every canonical example must have a pinned JSON report
- live inspection output must exactly match the pinned report
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    (
        ROOT / "examples/pass/minimal-refusal-receipt.json",
        ROOT / "examples/reports/pass-minimal-refusal-receipt.report.json",
        "PASS",
    ),
    (
        ROOT / "examples/hold/missing-receipt.json",
        ROOT / "examples/reports/hold-missing-receipt.report.json",
        "HOLD",
    ),
    (
        ROOT / "examples/fail/overbroad-claim.json",
        ROOT / "examples/reports/fail-overbroad-claim.report.json",
        "FAIL",
    ),
]


@pytest.mark.parametrize("example_path,report_path,expected_status", CASES)
def test_golden_report_file_exists(example_path: Path, report_path: Path, expected_status: str):
    assert example_path.exists(), f"Missing canonical example: {example_path}"
    assert report_path.exists(), f"Missing golden report for {expected_status}: {report_path}"


@pytest.mark.parametrize("example_path,report_path,expected_status", CASES)
def test_live_cli_report_matches_golden_snapshot(example_path: Path, report_path: Path, expected_status: str):
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "artifact_readiness_engine.cli",
            "inspect",
            str(example_path.relative_to(ROOT)),
            "--format",
            "json",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    if expected_status == "PASS":
        assert completed.returncode == 0, completed.stderr
    else:
        assert completed.returncode == 1, completed.stderr

    live = json.loads(completed.stdout)
    golden = json.loads(report_path.read_text(encoding="utf-8"))

    assert live == golden


@pytest.mark.parametrize("example_path,report_path,expected_status", CASES)
def test_golden_report_core_surfaces(example_path: Path, report_path: Path, expected_status: str):
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["status"] == expected_status
    assert "scores" in report
    assert "authority_trace" in report["scores"]
    assert "evidence_fit" in report["scores"]
    assert "receipt_quality" in report["scores"]
    assert "downstream_effect" in report["scores"]
    assert "passing_surfaces" in report
    assert "issues" in report
    assert "evidence" in report
    assert "authority" in report

    if expected_status == "PASS":
        assert report["issues"] == {}
        assert all(surface["result"] == "PASS" for surface in report["scores"].values())

    if expected_status == "HOLD":
        assert report["scores"]["receipt_quality"]["result"] == "HOLD"
        assert report["scores"]["replayability"]["result"] == "HOLD"
        assert report["scores"]["downstream_effect"]["result"] == "HOLD"

    if expected_status == "FAIL":
        assert report["scores"]["evidence_fit"]["result"] == "FAIL"
        assert report["scores"]["authority_trace"]["result"] == "HOLD"
