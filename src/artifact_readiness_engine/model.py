"""Data models for proof packs and inspection results."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class ProofPack:
    """Parsed representation of a submitted proof-pack JSON."""
    raw: Dict[str, Any]

    @property
    def claim(self) -> Optional[str]:
        return self.raw.get("claim")

    @property
    def claim_type(self) -> Optional[str]:
        return self.raw.get("claim_type")

    @property
    def object_(self) -> Optional[Dict]:
        return self.raw.get("object")

    @property
    def authority(self) -> Optional[Dict]:
        return self.raw.get("authority")

    @property
    def conditions(self) -> Optional[List]:
        return self.raw.get("conditions")

    @property
    def evidence(self) -> Optional[List]:
        return self.raw.get("evidence")

    @property
    def receipt(self) -> Optional[Dict]:
        return self.raw.get("receipt")

    @property
    def replay(self) -> Optional[Dict]:
        return self.raw.get("replay")

    @property
    def limits(self) -> Optional[Dict]:
        return self.raw.get("limits")


@dataclass
class ScoredDimension:
    name: str
    status: str  # PASS | HOLD | FAIL
    reason: str


@dataclass
class InspectionResult:
    file_path: str
    overall_status: str  # PASS | HOLD | FAIL
    dimensions: List[ScoredDimension] = field(default_factory=list)
    strongest_supported_claim: str = ""
    stated_claim: str = ""
    key_issue: str = ""
    next_action: str = ""
    unsupported_claims: List[str] = field(default_factory=list)
