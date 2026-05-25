"""Deterministic scoring rules v0.1.

Rules are evaluated in order. First FAIL encountered stops the
evaluation of that dimension — STRUCTURE_FIRST then FIRST_FAIL.
"""

from typing import List
from .model import ProofPack, ScoredDimension

BROAD_CLAIM_WORDS = {
    "safe", "safety", "compliant", "compliance",
    "governed", "governance", "secure", "security",
    "trusted", "trust", "certified", "audited",
}

REFUSAL_CLAIM_TYPES = {"refusal", "interruption", "stop", "hold"}


def score_claim_boundedness(pack: ProofPack) -> ScoredDimension:
    if not pack.claim:
        return ScoredDimension("claim_boundedness", "FAIL", "No claim present.")
    claim_lower = pack.claim.lower()
    broad_hits = [w for w in BROAD_CLAIM_WORDS if w in claim_lower]
    if broad_hits:
        limits = pack.limits or {}
        if not limits.get("scope"):
            return ScoredDimension(
                "claim_boundedness", "HOLD",
                f"Claim contains broad word(s) {broad_hits} without explicit scope in limits."
            )
    return ScoredDimension("claim_boundedness", "PASS", "Claim is bounded.")


def score_object_clarity(pack: ProofPack) -> ScoredDimension:
    obj = pack.object_
    if not obj:
        return ScoredDimension("object_clarity", "FAIL", "No object defined.")
    if not obj.get("id") or not obj.get("type"):
        return ScoredDimension("object_clarity", "HOLD", "Object missing id or type.")
    return ScoredDimension("object_clarity", "PASS", "Object is clearly identified.")


def score_authority_trace(pack: ProofPack) -> ScoredDimension:
    auth = pack.authority
    if not auth:
        return ScoredDimension("authority_trace", "HOLD", "No authority block present.")
    if auth.get("type", "").lower() == "unknown":
        return ScoredDimension("authority_trace", "HOLD", "Authority type is unknown.")
    if not auth.get("type"):
        return ScoredDimension("authority_trace", "HOLD", "Authority type not specified.")
    return ScoredDimension("authority_trace", "PASS", "Authority is traceable.")


def score_condition_clarity(pack: ProofPack) -> ScoredDimension:
    conditions = pack.conditions
    if conditions is None:
        return ScoredDimension("condition_clarity", "HOLD", "No conditions block present.")
    for c in conditions:
        if c.get("result", "").lower() == "unknown":
            return ScoredDimension(
                "condition_clarity", "HOLD",
                f"Condition '{c.get('id', '?')}' result is unknown."
            )
    return ScoredDimension("condition_clarity", "PASS", "All conditions have known results.")


def score_evidence_fit(pack: ProofPack) -> ScoredDimension:
    evidence = pack.evidence
    if evidence is None:
        return ScoredDimension("evidence_fit", "FAIL", "Evidence array is missing entirely.")
    if len(evidence) == 0:
        return ScoredDimension("evidence_fit", "FAIL", "Evidence array is empty.")
    for e in evidence:
        if e.get("proves", "").lower() == "weaker_than_claim":
            return ScoredDimension(
                "evidence_fit", "HOLD",
                f"Evidence item '{e.get('id', '?')}' proves a weaker claim than stated."
            )
    return ScoredDimension("evidence_fit", "PASS", "Evidence fits the claim.")


def score_receipt_quality(pack: ProofPack) -> ScoredDimension:
    receipt = pack.receipt
    claim_type = (pack.claim_type or "").lower()
    if receipt is None:
        if claim_type in REFUSAL_CLAIM_TYPES:
            return ScoredDimension(
                "receipt_quality", "FAIL",
                "Receipt is absent. Refusal/interruption claims require a receipt."
            )
        return ScoredDimension(
            "receipt_quality", "HOLD",
            "No receipt present. Cannot confirm claim was executed and recorded."
        )
    if receipt.get("present") is False:
        return ScoredDimension(
            "receipt_quality", "HOLD",
            "Receipt marked present=false."
        )
    if claim_type in REFUSAL_CLAIM_TYPES:
        if not receipt.get("downstream_effect_status"):
            return ScoredDimension(
                "receipt_quality", "HOLD",
                "Receipt present but downstream_effect_status is missing for refusal claim."
            )
        if receipt.get("downstream_effect_status", "").lower() == "unknown":
            return ScoredDimension(
                "receipt_quality", "HOLD",
                "Downstream effect status is unknown — path-blocked cannot be confirmed."
            )
    return ScoredDimension("receipt_quality", "PASS", "Receipt quality is sufficient.")


def score_replayability(pack: ProofPack) -> ScoredDimension:
    claim_type = (pack.claim_type or "").lower()
    replay = pack.replay
    if claim_type == "documentation":
        return ScoredDimension("replayability", "PASS", "Replay not required for documentation claims.")
    if not replay:
        return ScoredDimension(
            "replayability", "HOLD",
            "No replay surface present. Cannot verify the claim is reproducible."
        )
    if not replay.get("fixture") and not replay.get("trace"):
        return ScoredDimension(
            "replayability", "HOLD",
            "Replay block exists but contains no fixture or trace."
        )
    return ScoredDimension("replayability", "PASS", "Replay surface is present.")


def score_claim_limits(pack: ProofPack) -> ScoredDimension:
    limits = pack.limits
    if not limits:
        return ScoredDimension("claim_limits", "FAIL", "No limits block present — claim boundary is undefined.")
    if not limits.get("what_is_not_proven"):
        return ScoredDimension(
            "claim_limits", "HOLD",
            "Limits block present but 'what_is_not_proven' is missing."
        )
    return ScoredDimension("claim_limits", "PASS", "Claim limits are explicitly stated.")


def run_all_scores(pack: ProofPack) -> List[ScoredDimension]:
    return [
        score_claim_boundedness(pack),
        score_object_clarity(pack),
        score_authority_trace(pack),
        score_condition_clarity(pack),
        score_evidence_fit(pack),
        score_receipt_quality(pack),
        score_replayability(pack),
        score_claim_limits(pack),
    ]
