# Roadmap

This roadmap keeps future work bounded.

The project advances only by adding inspection strength, not by inflating claims.

---

## Gate 1 — Structural Proof Pack

Status: PASS

Current state:

- Canonical proof-pack schema exists.
- PASS / HOLD / FAIL examples exist.
- Deterministic inspection surfaces exist.
- Schema validation runs before scoring.

Next milestone:

- Add more negative examples for malformed authority, missing downstream effect, weak limits, and unsupported evidence.

---

## Gate 2 — Receipt Registry

Status: PASS

Current state:

- Canonical manifest exists.
- Golden reports exist.
- Golden report checks run in CI.
- Manifest integrity tests exist.

Next milestone:

- Add report digest/hash fields so pinned reports can be referenced as stable receipt objects.

---

## Gate 3 — Public Control Surface

Status: PASS

Current state:

- CLI supports `inspect`, `validate`, and `manifest`.
- CLI supports `@id` references.
- Public Python API is pinned at v0.2.0.
- API docs exist.

Next milestone:

- Add typed report models or documented JSON schema for inspection output.

---

## Gate 4 — External Audit Readiness

Status: HOLD

Current state:

- The engine can show structural inspectability.
- It cannot certify compliance, safety, legality, or production readiness.

Next milestone:

- Add `docs/EVIDENCE_MODEL.md` describing what each score proves and does not prove.
- Add `docs/EU_AI_ACT_MAPPING.md` as a claim-bounded structural map, not a compliance claim.

---

## Later Candidates

These remain candidates until scoped.

- JSON schema for inspection reports.
- Hash/digest of canonical reports.
- SARIF or machine-readable audit output.
- GitHub Action reusable workflow.
- Pre-commit hook for proof-pack validation.
- More canonical examples.
- Independent reviewer guide.

---

## Stop Line

Do not expand into certification language.

The engine checks whether a submitted proof object can support the bounded claim attached to it.
