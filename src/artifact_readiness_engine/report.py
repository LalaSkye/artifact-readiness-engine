"""Format inspection results for human-readable or JSON output."""
from __future__ import annotations
import json


def format_text(result: dict) -> str:
    lines = []
    lines.append("")
    lines.append("═" * 60)
    lines.append("  ARTIFACT READINESS ENGINE — Proof Structure Inspector v0.1")
    lines.append("═" * 60)
    lines.append(f"  File    : {result['file']}")
    lines.append(f"  Claim ID: {result['claim_id'] or '(none)'}")
    lines.append(f"  Type    : {result['claim_type'] or '(none)'}")
    lines.append("")
    status = result["status"]
    marker = {"PASS": "✓", "HOLD": "⚠", "FAIL": "✗"}.get(status, "?")
    lines.append(f"  Status  : {marker} {status}")
    lines.append("")
    lines.append("  Scores:")
    for surface, detail in result["scores"].items():
        sym = {"PASS": "✓", "HOLD": "⚠", "FAIL": "✗"}.get(detail["result"], "?")
        lines.append(f"    {sym}  {surface:<25}  {detail['result']}")
    lines.append("")
    if result["issues"]:
        lines.append("  Issues:")
        for surface, msg in result["issues"].items():
            lines.append(f"    ·  {surface}: {msg}")
        lines.append("")
    lines.append("  Strongest supported claim:")
    lines.append(f"    {result['strongest_supported_claim']}")
    lines.append("")
    if result["issues"]:
        lines.append("  Next action:")
        for surface, msg in result["issues"].items():
            lines.append(f"    Add or complete: {surface}")
    lines.append("")
    lines.append("─" * 60)
    lines.append("  NOT a compliance cert | NOT legal advice | NOT a safety cert")
    lines.append("─" * 60)
    lines.append("")
    return "\n".join(lines)


def format_json(result: dict) -> str:
    return json.dumps(result, indent=2)
