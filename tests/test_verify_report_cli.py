"""CLI tests for report digest verification."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS_REPORT = "examples/reports/pass-minimal-refusal-receipt.report.json"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the package CLI through the Python module entry point."""
    return subprocess.run(
        [sys.executable, "-m", "artifact_readiness_engine.cli", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_verify_report_cli_passes_for_golden_report_text_output():
    completed = run_cli("verify-report", PASS_REPORT)

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert "PASS:" in completed.stdout
    assert "report_digest verified" in completed.stdout


def test_verify_report_cli_passes_for_golden_report_json_output():
    completed = run_cli("verify-report", PASS_REPORT, "--format", "json")

    assert completed.returncode == 0
    assert completed.stderr == ""

    result = json.loads(completed.stdout)
    assert result["file"] == PASS_REPORT
    assert result["valid"] is True
    assert result["algorithm"] == "sha256"
    assert result["expected"] == result["actual"]


def test_verify_report_cli_fails_for_missing_report():
    completed = run_cli("verify-report", "examples/reports/missing.report.json")

    assert completed.returncode == 2
    assert "Error: file not found" in completed.stderr


def test_verify_report_cli_fails_for_tampered_report(tmp_path: Path):
    source = ROOT / PASS_REPORT
    tampered = tmp_path / "tampered.report.json"

    report = json.loads(source.read_text(encoding="utf-8"))
    report["status"] = "HOLD"
    tampered.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    completed = run_cli("verify-report", str(tampered), "--format", "json")

    assert completed.returncode == 1
    assert completed.stderr == ""

    result = json.loads(completed.stdout)
    assert result["valid"] is False
    assert result["algorithm"] == "sha256"
    assert result["expected"] != result["actual"]
