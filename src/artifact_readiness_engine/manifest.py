"""Manifest utilities for the canonical proof-pack registry."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

VALID_STATUSES = {"PASS", "HOLD", "FAIL"}


@dataclass(frozen=True)
class ManifestEntry:
    """One canonical proof-pack registry entry."""

    id: str
    path: str
    report_path: str
    expected_status: str
    tags: tuple[str, ...]


class ManifestError(ValueError):
    """Raised when the manifest is structurally invalid."""


def load_manifest(path: str | Path = "examples/manifest.json") -> list[ManifestEntry]:
    """Load canonical proof-pack entries from manifest JSON."""
    manifest_path = Path(path)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = data.get("examples", [])
    return [
        ManifestEntry(
            id=entry.get("id", ""),
            path=entry.get("path", ""),
            report_path=entry.get("report_path", ""),
            expected_status=entry.get("expected_status", ""),
            tags=tuple(entry.get("tags", [])),
        )
        for entry in entries
    ]


def check_manifest(entries: Iterable[ManifestEntry], root: str | Path = ".") -> list[str]:
    """Return manifest integrity errors. Empty list means PASS."""
    root_path = Path(root)
    errors: list[str] = []
    seen: set[str] = set()

    for entry in entries:
        if not entry.id:
            errors.append("Manifest entry is missing id.")
        elif entry.id in seen:
            errors.append(f"Duplicate manifest id: {entry.id}")
        else:
            seen.add(entry.id)

        if entry.expected_status not in VALID_STATUSES:
            errors.append(f"{entry.id}: invalid expected_status {entry.expected_status!r}")

        if not entry.tags:
            errors.append(f"{entry.id}: tags must be non-empty")

        if not entry.path:
            errors.append(f"{entry.id}: path is missing")
        elif not (root_path / entry.path).is_file():
            errors.append(f"{entry.id}: proof-pack path does not exist: {entry.path}")

        if not entry.report_path:
            errors.append(f"{entry.id}: report_path is missing")
        elif not (root_path / entry.report_path).is_file():
            errors.append(f"{entry.id}: report path does not exist: {entry.report_path}")

    return errors


def assert_manifest_valid(path: str | Path = "examples/manifest.json", root: str | Path = ".") -> list[ManifestEntry]:
    """Load manifest entries and raise ManifestError if integrity checks fail."""
    entries = load_manifest(path)
    errors = check_manifest(entries, root=root)
    if errors:
        raise ManifestError("Manifest integrity check failed:\n" + "\n".join(f"- {error}" for error in errors))
    return entries
