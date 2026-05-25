"""Data model for a proof-pack submission."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class ProofPack:
    """Parsed representation of a proof-pack JSON file."""
    raw: dict = field(repr=False)

    # Top-level fields
    claim_id: str = ""
    claim_type: str = ""          # e.g. refusal / interruption / documentation / observation
    claim_text: str = ""
    claim_limits: List[str] = field(default_factory=list)

    object_id: str = ""
    object_description: str = ""

    authority: dict = field(default_factory=dict)  # {type, reference}

    conditions: List[dict] = field(default_factory=list)  # [{id, description, result}]

    evidence: List[dict] = field(default_factory=list)    # [{id, type, reference, supports_claim}]

    receipt: Optional[dict] = None  # {present, type, reference, timestamp}

    replay: Optional[dict] = None   # {present, fixture, notes}

    downstream_effect: Optional[dict] = None  # {status, description}

    @classmethod
    def from_dict(cls, data: dict) -> "ProofPack":
        return cls(
            raw=data,
            claim_id=data.get("claim_id", ""),
            claim_type=data.get("claim_type", ""),
            claim_text=data.get("claim", {}).get("text", "") if isinstance(data.get("claim"), dict) else data.get("claim_text", ""),
            claim_limits=data.get("claim", {}).get("limits", []) if isinstance(data.get("claim"), dict) else data.get("claim_limits", []),
            object_id=data.get("object", {}).get("id", "") if isinstance(data.get("object"), dict) else "",
            object_description=data.get("object", {}).get("description", "") if isinstance(data.get("object"), dict) else "",
            authority=data.get("authority", {}),
            conditions=data.get("conditions", []),
            evidence=data.get("evidence", []),
            receipt=data.get("receipt"),
            replay=data.get("replay"),
            downstream_effect=data.get("downstream_effect"),
        )
