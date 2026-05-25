"""Golden report digest tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from artifact_readiness_engine.digest import compute_report_sha256, verify_report_digest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "examples" / "manifest.json"


def load_report_paths() -> list[Path]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return [ROOT / entry["report_path"] for entry in manifest["examples"]]


@pytest.mark.parametrize("report_path", load_report_paths())
def test_golden_report_carries_digest(report_path: Path):
    report = json.loads(report_path.read_text(encoding="utf-8"))
    digest = report.get("report_digest")

    assert isinstance(digest, dict)
    assert digest["algorithm"] == "sha256"
    assert digest["value"] == compute_report_sha256(report)


@pytest.mark.parametrize("report_path", load_report_paths())
def test_golden_report_digest_verifies(report_path: Path):
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert verify_report_digest(report) is True
