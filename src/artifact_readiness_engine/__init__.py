"""Artifact Readiness Engine — Proof Structure Inspection Mode v0.1"""

from .inspector import inspect_proof_pack
from .model import ProofPack, InspectionResult

__version__ = "0.1.0"
__all__ = ["inspect_proof_pack", "ProofPack", "InspectionResult"]
