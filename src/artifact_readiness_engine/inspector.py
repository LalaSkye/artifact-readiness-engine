"""Core inspection logic — load, validate, score, summarise."""

import json
from pathlib import Path
from typing import Union

from .model import ProofPack, InspectionResult
from .scoring import run_all_scores


STATUS_PRIORITY = {"FAIL": 0, "HOLD": 1, "PASS": 2}


def _aggregate_status(dimension_statuses):
    """Return the worst status across all dimensions."""
    return min(dimension_statuses, key=lambda s: STATUS_PRIORITY[s])


def _infer_key_issue(dimensions):
    fails = [d for d in dimensions if d.status == "FAIL"]
    holds = [d for d in dimensions if d.status == "HOLD"]
    worst = fails or holds
    if not worst:
        return ""
    return worst[0].reason


def _infer_next_action(result: InspectionResult) -> str:
    fails = [d for d in result.dimensions if d.status == "FAIL"]
    holds = [d for d in result.dimensions if d.status == "HOLD"]
    if not fails and not holds:
        return "Proof pack passes structural inspection. Submit for human review."
    items = [d.name for d in (fails + holds)]
    return f"Address the following surfaces: {', '.join(items)}."


def _infer_unsupported(dimensions):
    return [
        f"{d.name}: {d.reason}"
        for d in dimensions
        if d.status in ("FAIL", "HOLD")
    ]


def inspect_proof_pack(source: Union[str, Path, dict]) -> InspectionResult:
    """Inspect a proof pack from a file path or dict."""
    if isinstance(source, dict):
        raw = source
        file_path = "<dict>"
    else:
        file_path = str(source)
        with open(source, "r") as f:
            raw = json.load(f)

    pack = ProofPack(raw=raw)
    dimensions = run_all_scores(pack)

    statuses = [d.status for d in dimensions]
    overall = _aggregate_status(statuses)

    result = InspectionResult(
        file_path=file_path,
        overall_status=overall,
        dimensions=dimensions,
        strongest_supported_claim=_derive_strongest_claim(dimensions, pack),
        stated_claim=pack.claim or "",
        key_issue=_infer_key_issue(dimensions),
        next_action="",
        unsupported_claims=_infer_unsupported(dimensions),
    )
    result.next_action = _infer_next_action(result)
    return result


def _derive_strongest_claim(dimensions, pack):
    """Return the strongest claim the evidence can support."""
    failing = {d.name for d in dimensions if d.status in ("FAIL", "HOLD")}
    if not failing:
        return pack.claim or "Claim is fully supported."
    # Reduce claim description based on what's missing
    parts = []
    if "receipt_quality" in failing:
        parts.append("no confirmed receipt")
    if "replayability" in failing:
        parts.append("no replay surface")
    if "evidence_fit" in failing:
        parts.append("partial or absent evidence")
    if "claim_limits" in failing:
        parts.append("unbounded scope")
    if parts:
        return f"Weaker than stated — limitations: {', '.join(parts)}."
    return "Claim is partially supported — see HOLD dimensions."
