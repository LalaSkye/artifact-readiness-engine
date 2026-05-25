"""Canonical digest utilities for inspection reports."""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

DIGEST_FIELD = "report_digest"
DIGEST_ALGORITHM = "sha256"
DIGEST_CANONICALIZATION = "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=False) excluding report_digest"


def canonical_report_payload(report: dict[str, Any]) -> bytes:
    """Return canonical report bytes for digesting.

    The digest excludes the digest field itself so reports can carry their own
    receipt without creating a self-referential hash.
    """
    payload = copy.deepcopy(report)
    payload.pop(DIGEST_FIELD, None)
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def compute_report_sha256(report: dict[str, Any]) -> str:
    """Compute a stable SHA-256 digest for a report dict."""
    return hashlib.sha256(canonical_report_payload(report)).hexdigest()


def attach_report_digest(report: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of report with a self-describing digest field."""
    result = copy.deepcopy(report)
    result[DIGEST_FIELD] = {
        "algorithm": DIGEST_ALGORITHM,
        "canonicalization": DIGEST_CANONICALIZATION,
        "value": compute_report_sha256(result),
    }
    return result


def verify_report_digest(report: dict[str, Any]) -> bool:
    """Return True when a report carries a matching digest field."""
    digest = report.get(DIGEST_FIELD)
    if not isinstance(digest, dict):
        return False
    if digest.get("algorithm") != DIGEST_ALGORITHM:
        return False
    return digest.get("value") == compute_report_sha256(report)
