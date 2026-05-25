"""Core inspection pipeline."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Union

from .model import ProofPack
from .scoring import run_all, overall


def inspect_file(path: Union[str, Path]) -> dict:
    """Load a proof-pack JSON and return an inspection result dict."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    pack = ProofPack.from_dict(data)
    scores = run_all(pack)
    status = overall(scores)

    # Derive strongest_supported_claim
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
        "scores": {k: {"result": s.value, "note": msg} for k, (s, msg) in scores.items()},
        "passing_surfaces": passing,
        "issues": failing,
        "strongest_supported_claim": _derive_strongest(pack, scores),
    }


def _derive_strongest(pack: ProofPack, scores: dict) -> str:
    """Return a plain-language description of what the evidence does support."""
    passing = [k for k, (s, _) in scores.items() if s.value == "PASS"]
    if not passing:
        return "No claim surfaces passed inspection. Proof pack cannot support any bounded claim."
    return (
        f"Evidence supports a claim covering: {', '.join(passing)}. "
        "Surfaces that did not pass are not supported by this proof pack in its current state."
    )
