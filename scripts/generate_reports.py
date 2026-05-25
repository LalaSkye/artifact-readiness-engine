"""Generate or verify golden JSON inspection reports.

Usage:
  python scripts/generate_reports.py --write
  python scripts/generate_reports.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from artifact_readiness_engine.inspector import inspect_file  # noqa: E402

REPORTS = {
    ROOT / "examples/pass/minimal-refusal-receipt.json": ROOT / "examples/reports/pass-minimal-refusal-receipt.report.json",
    ROOT / "examples/hold/missing-receipt.json": ROOT / "examples/reports/hold-missing-receipt.report.json",
    ROOT / "examples/fail/overbroad-claim.json": ROOT / "examples/reports/fail-overbroad-claim.report.json",
}


def render_report(example_path: Path) -> str:
    """Return deterministic JSON for a live inspection report."""
    result = inspect_file(example_path.relative_to(ROOT))
    return json.dumps(result, indent=2) + "\n"


def write_reports() -> int:
    """Write all golden reports."""
    for example_path, report_path in REPORTS.items():
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_report(example_path), encoding="utf-8")
        print(f"wrote {report_path.relative_to(ROOT)}")
    return 0


def check_reports() -> int:
    """Check all golden reports match current live inspection output."""
    failures: list[str] = []
    for example_path, report_path in REPORTS.items():
        expected = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
        actual = render_report(example_path)
        if actual != expected:
            failures.append(str(report_path.relative_to(ROOT)))

    if failures:
        print("Report snapshot mismatch:")
        for failure in failures:
            print(f"- {failure}")
        print("Run: python scripts/generate_reports.py --write")
        return 1

    print("PASS: golden inspection reports match live engine output.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or verify golden inspection reports.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Write golden report snapshots.")
    mode.add_argument("--check", action="store_true", help="Check snapshots against live output.")
    args = parser.parse_args()

    if args.write:
        return write_reports()
    return check_reports()


if __name__ == "__main__":
    raise SystemExit(main())
