"""JSON schema validation for proof-pack submissions."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "proof-pack.schema.json"


class ProofPackValidationError(ValueError):
    """Raised when a proof-pack does not match the canonical schema."""


def load_schema() -> dict[str, Any]:
    """Load the canonical proof-pack JSON schema."""
    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_proof_pack(data: dict[str, Any]) -> None:
    """Validate proof-pack data against the canonical schema.

    Raises:
        ProofPackValidationError: if any schema validation errors are found.
    """
    validator = Draft202012Validator(load_schema())
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if not errors:
        return

    lines = ["Proof pack failed schema validation:"]
    for error in errors:
        path = ".".join(str(part) for part in error.path) or "<root>"
        lines.append(f"- {path}: {error.message}")
    raise ProofPackValidationError("\n".join(lines))
