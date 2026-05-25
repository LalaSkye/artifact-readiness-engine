"""Public validation API for proof-pack files."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .manifest import resolve_proof_pack_reference
from .validation import validate_proof_pack


def validate_file(path: Union[str, Path]) -> bool:
    """Validate a proof-pack file against the canonical schema.

    Args:
        path: Direct proof-pack path or @manifest-id reference.

    Returns:
        True when validation passes.

    Raises:
        ProofPackValidationError: if the proof-pack fails schema validation.
        ManifestError: if an @manifest-id cannot be resolved.
        FileNotFoundError: if the resolved file does not exist.
    """
    resolved = resolve_proof_pack_reference(str(path))
    data = json.loads(Path(resolved).read_text(encoding="utf-8"))
    validate_proof_pack(data)
    return True
