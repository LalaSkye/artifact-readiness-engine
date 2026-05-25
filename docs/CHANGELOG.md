# Changelog

All notable changes to Artifact Readiness Engine are recorded here.

This project follows a semantic-versioning style:

- `MAJOR` — incompatible public API or report-shape change
- `MINOR` — new public capability, command, manifest field, or stable exported symbol
- `PATCH` — fixes, documentation, tests, internal refactors that preserve public behaviour

---

## v0.2.0

Status: current public API surface.

### Added

- Public Python API surface:
  - `inspect_file`
  - `inspect_by_id`
  - `validate_file`
  - `load_manifest`
  - `ManifestEntry`
- `@id` manifest resolution for CLI and Python helper usage.
- Canonical manifest registry at `examples/manifest.json`.
- Golden JSON inspection reports under `examples/reports/`.
- Golden report snapshot checking.
- Manifest integrity tests.
- Public API tests.
- API contract documentation at `docs/API.md`.
- CI badge and CI workflow.

### Changed

- CLI examples now prefer manifest `@id` references over hard-coded paths.
- Golden report generation and tests are driven from the canonical manifest.
- README now exposes the public surface and API contract.

### Guardrails

- The engine does not certify compliance, safety, legality, production readiness, or EU AI Act conformity.
- `validate` means schema-valid only.
- `inspect` evaluates proof-surface strength.

---

## v0.1.0

Status: initial proof-structure inspection prototype.

### Added

- Proof-pack schema.
- PASS / HOLD / FAIL scoring model.
- CLI `inspect` command.
- CLI `validate` command.
- Initial examples:
  - PASS minimal refusal receipt
  - HOLD missing receipt
  - FAIL overbroad claim
- Deterministic scoring surfaces:
  - `claim_boundedness`
  - `object_clarity`
  - `authority_trace`
  - `condition_clarity`
  - `evidence_fit`
  - `receipt_quality`
  - `replayability`
  - `downstream_effect`
  - `claim_limits`

### Guardrails

- One proof object should prove the claim attached to it — not less, not everything.
