"""Core inspection pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .manifest import resolve_proof_pack_reference
from .model import ProofPack
from .scoring import overall, run_all
from .validation import validate_proof_pack


def inspect_file(path: Union[str, Path]) -> dict:
    """Load, validate, score, and report on a proof-pack JSON file.

    Args:
        path: Direct path to a proof-pack JSON file.

    Returns:
        A deterministic inspection report dictionary.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_proof_pack(data)

    pack = ProofPack.from_dict(data)
    scores = run_all(pack)
    status = overall(scores)

    passing = [k for k, (s, _) in scores.items() if s.value == "PASS"]
    failing = {k: msg for k, (s, msg) in scores.items() if s.value != "PASS"}

    return {
        "file": str(path),
        "status": status.value,
        "claim_id": pack.claim_id,
        "claim_type": pack.claim_type,
        "stated_claim": pack.claim_text,
        "claim_limits": pack.claim_limits,
        "object": pack.object_description or pack.object_id,
        "authority": pack.authority,
        "conditions": pack.conditions,
        "evidence": pack.evidence,
        "receipt": pack.receipt,
        "replay": pack.replay,
        "downstream_effect": pack.downstream_effect,
        "scores": {k: {"result": s.value, "note": msg} for k, (s, msg) in scores.items()},
        "passing_surfaces": passing,
        "issues": failing,
        "strongest_supported_claim": _derive_strongest(pack, scores),
    }


def inspect_by_id(entry_id: str) -> dict:
    """Inspect a proof-pack registered in examples/manifest.json by id.

    Args:
        entry_id: Manifest id with or without leading '@'.

    Returns:
        A deterministic inspection report dictionary.
    """
    reference = entry_id if entry_id.startswith("@") else f"@{entry_id}"
    return inspect_file(resolve_proof_pack_reference(reference))


def _derive_strongest(pack: ProofPack, scores: dict) -> str:
    """Return a plain-language description of what the evidence does support."""
    passing = [k for k, (s, _) in scores.items() if s.value == "PASS"]
    if not passing:
        return "No claim surfaces passed inspection. Proof pack cannot support any bounded claim."

    if all(scores[k][0].value == "PASS" for k in scores):
        return (
            f"The proof pack structurally supports the stated {pack.claim_type or 'bounded'} claim: "
            f"{pack.claim_text}"
        )

    return (
        f"Evidence currently supports only these surfaces: {', '.join(passing)}. "
        "Surfaces that did not pass are not supported by this proof pack in its current state."
    )
