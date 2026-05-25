"""Report rendering — human-readable and JSON output."""

import json
from .model import InspectionResult

STATUS_SYMBOLS = {"PASS": "✓", "HOLD": "~", "FAIL": "✗"}


def render_text(result: InspectionResult) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("PROOF STRUCTURE INSPECTION REPORT")
    lines.append("=" * 60)
    lines.append(f"File      : {result.file_path}")
    lines.append(f"Status    : {result.overall_status}")
    lines.append("")
    lines.append("CHAIN SCORES")
    lines.append("-" * 40)
    for dim in result.dimensions:
        sym = STATUS_SYMBOLS.get(dim.status, "?")
        lines.append(f"  [{sym}] {dim.name:<28} {dim.status}")
    lines.append("")
    lines.append("STATED CLAIM")
    lines.append(f"  {result.stated_claim or '(none)'}")
    lines.append("")
    lines.append("STRONGEST SUPPORTED CLAIM")
    lines.append(f"  {result.strongest_supported_claim or '(none)'}")
    if result.key_issue:
        lines.append("")
        lines.append("KEY ISSUE")
        lines.append(f"  {result.key_issue}")
    if result.unsupported_claims:
        lines.append("")
        lines.append("UNSUPPORTED / INCOMPLETE SURFACES")
        for u in result.unsupported_claims:
            lines.append(f"  - {u}")
    lines.append("")
    lines.append("NEXT ACTION")
    lines.append(f"  {result.next_action}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("This report is a pre-audit inspection surface only.")
    lines.append("It does not certify compliance, safety, legality,")
    lines.append("production readiness, or any court or audit outcome.")
    lines.append("=" * 60)
    return "\n".join(lines)


def render_json(result: InspectionResult) -> str:
    payload = {
        "file": result.file_path,
        "status": result.overall_status,
        "scores": {
            d.name: {"status": d.status, "reason": d.reason}
            for d in result.dimensions
        },
        "stated_claim": result.stated_claim,
        "strongest_supported_claim": result.strongest_supported_claim,
        "key_issue": result.key_issue,
        "unsupported_claims": result.unsupported_claims,
        "next_action": result.next_action,
        "disclaimer": (
            "Pre-audit inspection surface only. "
            "Does not certify compliance, safety, legality, "
            "or production readiness."
        ),
    }
    return json.dumps(payload, indent=2)
