"""Deterministic scoring rules v0.1."""
from __future__ import annotations
from enum import Enum
from typing import Tuple

from .model import ProofPack


class Score(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


# Words that flag an overbroad claim unless a tight scope is also present.
_BROAD_WORDS = {"safe", "compliant", "governed", "secure", "trusted", "certified", "proven"}
_REFUSAL_TYPES = {"refusal", "interruption"}


def _score_claim_boundedness(pack: ProofPack) -> Tuple[Score, str]:
    if not pack.claim_text:
        return Score.FAIL, "No claim text found."
    lower = pack.claim_text.lower()
    hit = [w for w in _BROAD_WORDS if w in lower]
    if hit and not pack.claim_limits:
        return Score.HOLD, f"Broad word(s) detected ({', '.join(hit)}) with no explicit limits."
    return Score.PASS, "Claim text is present and limits are declared."


def _score_object_clarity(pack: ProofPack) -> Tuple[Score, str]:
    if not pack.object_id and not pack.object_description:
        return Score.FAIL, "No object id or description found."
    return Score.PASS, "Object is identified."


def _score_authority_trace(pack: ProofPack) -> Tuple[Score, str]:
    if not pack.authority:
        return Score.HOLD, "No authority block found."
    if pack.authority.get("type", "").lower() in ("", "unknown"):
        return Score.HOLD, "Authority type is unknown."
    if not pack.authority.get("reference", ""):
        return Score.HOLD, "Authority reference is missing."
    return Score.PASS, "Authority type and reference are present."


def _score_condition_clarity(pack: ProofPack) -> Tuple[Score, str]:
    if not pack.conditions:
        return Score.HOLD, "No conditions listed."
    unknown = [c.get("id", "?") for c in pack.conditions if c.get("result", "unknown") == "unknown"]
    if unknown:
        return Score.HOLD, f"Condition(s) with unknown result: {', '.join(unknown)}."
    return Score.PASS, "All conditions have known results."


def _score_evidence_fit(pack: ProofPack) -> Tuple[Score, str]:
    if not pack.evidence:
        return Score.FAIL, "Evidence array is missing or empty."
    unsupported = [e.get("id", "?") for e in pack.evidence if e.get("supports_claim") is False]
    if unsupported:
        return Score.HOLD, f"Evidence item(s) do not support the stated claim: {', '.join(unsupported)}."
    return Score.PASS, "Evidence array is present and all items support the claim."


def _score_receipt_quality(pack: ProofPack) -> Tuple[Score, str]:
    if pack.receipt is None:
        if pack.claim_type.lower() in _REFUSAL_TYPES:
            return Score.FAIL, "Receipt is absent. Required for refusal/interruption claim types."
        return Score.HOLD, "No receipt block found."
    if not pack.receipt.get("present", False):
        if pack.claim_type.lower() in _REFUSAL_TYPES:
            return Score.HOLD, "Receipt present=false on a refusal/interruption claim."
        return Score.HOLD, "Receipt present=false."
    if not pack.receipt.get("reference", ""):
        return Score.HOLD, "Receipt has no reference."
    return Score.PASS, "Receipt is present with a valid reference."


def _score_replayability(pack: ProofPack) -> Tuple[Score, str]:
    if pack.claim_type.lower() == "documentation":
        return Score.PASS, "Replay not required for documentation claims."
    if pack.replay is None or not pack.replay.get("present", False):
        return Score.HOLD, "Replay surface is absent or marked not present."
    return Score.PASS, "Replay surface is declared."


def _score_claim_limits(pack: ProofPack) -> Tuple[Score, str]:
    if not pack.claim_limits:
        return Score.FAIL, "Claim limits are not declared."
    return Score.PASS, "Claim limits are declared."


_SCORERS = [
    ("claim_boundedness", _score_claim_boundedness),
    ("object_clarity", _score_object_clarity),
    ("authority_trace", _score_authority_trace),
    ("condition_clarity", _score_condition_clarity),
    ("evidence_fit", _score_evidence_fit),
    ("receipt_quality", _score_receipt_quality),
    ("replayability", _score_replayability),
    ("claim_limits", _score_claim_limits),
]


def run_all(pack: ProofPack) -> dict[str, Tuple[Score, str]]:
    return {name: fn(pack) for name, fn in _SCORERS}


_PRIORITY = {Score.FAIL: 0, Score.HOLD: 1, Score.PASS: 2}


def overall(scores: dict[str, Tuple[Score, str]]) -> Score:
    worst = min(scores.values(), key=lambda t: _PRIORITY[t[0]])
    return worst[0]
