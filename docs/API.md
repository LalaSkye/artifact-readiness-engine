# Public API Contract

Status: v0.2.0  
Scope: public CLI and Python API for Artifact Readiness Engine.

Related documents:

- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

This document is the human-readable contract for the public surface.

The engine does not certify compliance, safety, legality, production readiness, or EU AI Act conformity.

It checks whether a submitted proof object can support the bounded claim attached to it.

---

## CLI Surface

Install locally:

```bash
pip install -e .
```

### Inspect

Inspect a proof-pack file and return a report.

```bash
artifact-readiness inspect examples/pass/minimal-refusal-receipt.json
artifact-readiness inspect @pass-minimal-refusal-receipt
artifact-readiness inspect @hold-missing-receipt --format json
```

Accepted input:

- direct proof-pack JSON path
- `@id` from `examples/manifest.json`

Output formats:

```bash
--format text
--format json
```

Exit behaviour:

- `0` when status is `PASS`
- `1` when status is `HOLD` or `FAIL`
- `2` for file, manifest, parsing, or validation errors

### Validate

Validate proof-pack structure against the canonical schema.

```bash
artifact-readiness validate examples/pass/minimal-refusal-receipt.json
artifact-readiness validate @fail-overbroad-claim
```

Validation confirms schema shape only. It does not mean the proof-pack passes inspection.

Example:

```text
validate = file is structurally valid
inspect = proof strength is evaluated
```

### Verify Report

Verify that a report JSON file carries a valid `report_digest`.

```bash
artifact-readiness verify-report examples/reports/pass-minimal-refusal-receipt.report.json
artifact-readiness verify-report examples/reports/hold-missing-receipt.report.json --format json
```

The digest is computed over canonical JSON excluding the `report_digest` field itself.

Exit behaviour:

- `0` when the stored digest verifies
- `1` when the stored digest mismatches
- `2` for file, parsing, or runtime errors

JSON output shape:

```json
{
  "file": "examples/reports/pass-minimal-refusal-receipt.report.json",
  "valid": true,
  "algorithm": "sha256",
  "expected": "<stored-sha256>",
  "actual": "<computed-sha256>"
}
```

### Manifest

List or check canonical example registry.

```bash
artifact-readiness manifest
artifact-readiness manifest --check
artifact-readiness manifest --format json
```

Manifest entries define:

- `id`
- `path`
- `report_path`
- `expected_status`
- `tags`

---

## Python API

Stable public imports:

```python
from artifact_readiness_engine import (
    ManifestEntry,
    inspect_by_id,
    inspect_file,
    load_manifest,
    validate_file,
)
```

### `inspect_file(path) -> dict`

Inspect a direct proof-pack JSON file path.

```python
from artifact_readiness_engine import inspect_file

report = inspect_file("examples/pass/minimal-refusal-receipt.json")
assert report["status"] == "PASS"
```

Returns a deterministic report dictionary with fields including:

- `file`
- `status`
- `claim_id`
- `claim_type`
- `stated_claim`
- `claim_limits`
- `object`
- `authority`
- `conditions`
- `evidence`
- `receipt`
- `replay`
- `downstream_effect`
- `scores`
- `passing_surfaces`
- `issues`
- `strongest_supported_claim`
- `report_digest` for generated golden reports

### `inspect_by_id(entry_id) -> dict`

Inspect a manifest-registered proof pack by id.

```python
from artifact_readiness_engine import inspect_by_id

report = inspect_by_id("pass-minimal-refusal-receipt")
report = inspect_by_id("@hold-missing-receipt")
```

Both plain ids and `@id` references are accepted.

### `validate_file(path_or_id) -> bool`

Validate a direct path or `@id` reference against the canonical schema.

```python
from artifact_readiness_engine import validate_file

assert validate_file("examples/pass/minimal-refusal-receipt.json") is True
assert validate_file("@pass-minimal-refusal-receipt") is True
```

Returns `True` when schema validation passes.

Raises an exception for invalid schema, unknown manifest id, or missing file.

### `load_manifest() -> list[ManifestEntry]`

Load canonical example registry entries.

```python
from artifact_readiness_engine import load_manifest

entries = load_manifest()
for entry in entries:
    print(entry.id, entry.expected_status, entry.path)
```

### `ManifestEntry`

Dataclass fields:

```python
id: str
path: str
report_path: str
expected_status: str
tags: tuple[str, ...]
```

---

## Version Stability

Current public API version:

```python
__version__ = "0.2.0"
```

Pinned public exports:

```python
__all__ = [
    "ManifestEntry",
    "inspect_by_id",
    "inspect_file",
    "load_manifest",
    "validate_file",
]
```

Any change to this public surface should update:

- `src/artifact_readiness_engine/__init__.py`
- `pyproject.toml`
- `tests/test_public_api.py`
- this document
- `docs/CHANGELOG.md`

---

## Golden Examples

Canonical examples live in:

```text
examples/manifest.json
```

Current registry:

```text
@pass-minimal-refusal-receipt
@hold-missing-receipt
@fail-overbroad-claim
```

Each example has a pinned report under:

```text
examples/reports/*.report.json
```

Golden reports carry a self-verifying `report_digest` and are checked in CI.

To regenerate:

```bash
python scripts/generate_reports.py --write
```

To verify:

```bash
python scripts/generate_reports.py --check
artifact-readiness verify-report examples/reports/pass-minimal-refusal-receipt.report.json
```

---

## Error Behaviour

Unknown manifest id:

```text
Error: Unknown manifest id: @missing-id. Known ids: ...
```

Missing file:

```text
Error: file not found — <path>
```

Schema failure:

```text
Proof pack failed schema validation:
- <field>: <reason>
```

Digest mismatch:

```text
FAIL: <path> report_digest mismatch.
expected: <stored-sha256>
actual  : <computed-sha256>
```

Inspection statuses:

- `PASS`: structurally inspectable for the attached bounded claim
- `HOLD`: incomplete or ambiguous proof surface
- `FAIL`: submitted artefact cannot support the claim

---

## Stop Line

A proof object should prove the claim attached to it — not less, not everything.
