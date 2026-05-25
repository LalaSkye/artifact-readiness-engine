# Artifact Readiness Engine

[![CI](https://github.com/LalaSkye/artifact-readiness-engine/actions/workflows/tests.yml/badge.svg)](https://github.com/LalaSkye/artifact-readiness-engine/actions/workflows/tests.yml)

Artifact Readiness Engine checks whether an artefact is ready to support the claim attached to it.

It currently has two inspection surfaces:

1. **Repo Readiness** — can a repository actually install, run, and be used?
2. **Proof Structure Inspection Mode** — can a governance or AI-control artefact support a bounded proof claim?

---

## Public Surface

- [Public API Contract](docs/API.md)
- [Evidence Model](docs/EVIDENCE_MODEL.md)
- [EU AI Act Structural Mapping](docs/EU_AI_ACT_MAPPING.md)
- [Independent Reviewer Guide](docs/REVIEWER_GUIDE.md)
- [Changelog](docs/CHANGELOG.md)
- [Roadmap](docs/ROADMAP.md)
- CLI supports direct paths and `@id` references from `examples/manifest.json`
- Python API is pinned at `0.2.0`

Quickstart:

```bash
pip install -e .
artifact-readiness inspect @pass-minimal-refusal-receipt
artifact-readiness validate @fail-overbroad-claim
artifact-readiness manifest --check
```

Python:

```python
from artifact_readiness_engine import inspect_by_id, validate_file, load_manifest

report = inspect_by_id("@pass-minimal-refusal-receipt")
assert report["status"] == "PASS"
assert validate_file("@pass-minimal-refusal-receipt") is True
entries = load_manifest()
```

---

## Proof Structure Inspection Mode

This mode is a pre-audit inspection surface.

It does **not** certify compliance, safety, legality, production readiness, or EU AI Act conformity.

It asks a smaller question:

> What exactly does this artefact prove, and what does it not prove?

Core chain:

```text
Claim
→ Object
→ Authority
→ Conditions
→ Evidence
→ Receipt
→ Replay
→ Downstream Effect
→ Limit
```

### Output

```text
Status: PASS | HOLD | FAIL

Scores:
- claim_boundedness
- object_clarity
- authority_trace
- condition_clarity
- evidence_fit
- receipt_quality
- replayability
- downstream_effect
- claim_limits
```

### States

- `PASS` — structurally inspectable for the attached bounded claim
- `HOLD` — incomplete or ambiguous proof surface
- `FAIL` — claim cannot be supported by the submitted artefact

### Non-claims

This project does not claim that an artefact is:

- EU AI Act compliant
- legally sufficient
- independently audited
- production safe
- fully secure
- court-ready
- certified

It only checks whether the submitted proof object can support the claim attached to it.

---

## Repo Readiness Mode

The original repo-readiness surface checks whether a repository can actually be used.

It asks:

- Can the repo install?
- Can it run?
- Are instructions correct?
- Are dependencies pinned?
- Are tests present?
- Are there obvious security risks?

A short, structured **Repo Readiness Report** may look like:

```text
Status: HOLD

Runability: FAIL
Build: FAIL
Docs: PARTIAL
Tests: MISSING
Security: REVIEW

Key issue:
Install path is broken (dependency mismatch)

Next action:
Fix environment + dependency versions
```

---

## Position

This is not a linter.

This is not static analysis.

This is a readiness check at the execution boundary.

---

## Status

v0.2.0 — proof-structure inspection engine, CLI, manifest registry, golden reports, and public Python API.

---

## Stop line

A proof object should prove the claim attached to it — not less, not everything.
