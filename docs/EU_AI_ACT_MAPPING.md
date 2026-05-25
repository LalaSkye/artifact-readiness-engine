# EU AI Act Structural Mapping

Status: v0.2.0  
Scope: structural mapping only.

This document maps Artifact Readiness Engine surfaces to selected EU AI Act structural pressure points.

It is not a compliance assessment.

---

## Hard Non-Claims

This mapping does not prove, certify, assess, or imply:

- EU AI Act compliance
- conformity assessment readiness
- legal sufficiency
- production safety
- independent audit approval
- notified-body acceptance
- CE marking readiness
- risk-management completeness
- technical-documentation completeness
- human-oversight sufficiency
- Article-by-Article satisfaction

This tool does not replace:

- legal review
- regulatory submission
- provider obligations
- deployer obligations
- notified-body assessment
- conformity assessment
- risk management system design
- technical documentation required under Annex IV

The engine only checks whether a submitted proof object can support the bounded claim attached to it.

---

## Structural Reference Points

| EU AI Act reference | Structural obligation area | Engine relation |
|---|---|---|
| Article 9 | Risk management system | Conditions, evidence, claim limits |
| Article 11 | Technical documentation | Object, claim, evidence, limits |
| Article 12 | Record-keeping / automatic logs | Receipt, evidence, replay |
| Article 13 | Transparency and provision of information to deployers | Claim, object, limits, report output |
| Article 14 | Human oversight | Authority trace, conditions, downstream effect |
| Article 17 | Quality management system | Authority, conditions, evidence, manifest discipline |
| Article 18 | Documentation keeping | Receipt, report, manifest, golden snapshots |
| Article 43 | Conformity assessment | Report structure only; no conformity claim |
| Annex IV | Technical documentation contents | Object, purpose, evidence, limits, report output |
| Annex VII | Quality management system and technical documentation assessment | Registry, reports, documentation discipline only |

---

## Engine Surface Mapping

| Engine surface | Relevant EU AI Act structural pressure | What the engine can show | What the engine cannot show |
|---|---|---|---|
| `claim_boundedness` | Article 11, Article 13, Annex IV | Whether the submitted claim has a visible boundary | Whether the claim satisfies legal disclosure or documentation requirements |
| `object_clarity` | Article 11, Annex IV | Whether the inspected object is identifiable | Whether the AI system description is complete under Annex IV |
| `authority_trace` | Article 14, Article 17 | Whether an authority type and reference are present | Whether human oversight is legally sufficient or operationally adequate |
| `condition_clarity` | Article 9, Article 14 | Whether listed conditions have known results | Whether the risk management system is complete |
| `evidence_fit` | Article 9, Article 11, Article 12, Annex IV | Whether supplied evidence maps to the stated claim | Whether the evidence is legally sufficient or independently verified |
| `receipt_quality` | Article 12, Article 18 | Whether an inspectable receipt exists | Whether record-keeping obligations are satisfied |
| `replayability` | Article 9, Article 12, Article 43 | Whether reconstruction or replay is declared | Whether conformity assessment requirements are met |
| `downstream_effect` | Article 14 | Whether downstream state is marked blocked/allowed/unknown | Whether all operational consequences were prevented |
| `claim_limits` | Article 11, Article 13, Annex IV | Whether proof boundaries are declared | Whether limitations are complete or legally adequate |
| `status` | Whole proof pack only | Lowest-confidence structural verdict | Any regulatory conclusion |

---

## PASS / HOLD / FAIL Mapping

### PASS

A `PASS` means:

```text
The proof pack is structurally inspectable for the attached bounded claim.
```

It may support preparation for:

- internal review
- evidence organisation
- documentation discipline
- audit-facing discussion
- proof-pack triage

It does not mean:

- the system complies with the EU AI Act
- a notified body would accept the artefact
- the relevant Article obligation is satisfied
- legal risk is removed

### HOLD

A `HOLD` means:

```text
The proof pack is incomplete, ambiguous, or missing a surface required to support the claim confidently.
```

Typical HOLD conditions:

- authority unknown
- condition result unknown
- receipt missing or incomplete
- replay absent
- downstream effect unknown
- evidence only partially supports the claim

A HOLD may indicate that an organisation should improve documentation, evidence, logs, receipts, replay fixtures, or authority records before relying on the proof pack.

### FAIL

A `FAIL` means:

```text
The submitted artefact cannot support the stated claim in its current form.
```

Typical FAIL conditions:

- evidence missing
- claim text missing
- claim limits missing
- required receipt absent for refusal/interruption claim
- object missing

A FAIL does not prove non-compliance.

It only means the submitted proof object cannot support the attached claim.

---

## Article Mapping Detail

### Article 9 — Risk Management System

Engine-relevant surfaces:

- `condition_clarity`
- `evidence_fit`
- `claim_limits`
- `replayability`

Structural relation:

The engine can show whether a proof pack contains explicit conditions, known condition results, evidence references, and declared limits.

Claim boundary:

The engine does not assess whether a risk management system has been established, implemented, documented, maintained, regularly reviewed, or updated.

---

### Article 11 — Technical Documentation

Engine-relevant surfaces:

- `claim_boundedness`
- `object_clarity`
- `evidence_fit`
- `claim_limits`

Structural relation:

The engine can show whether a proof pack identifies the object, states the claim, attaches evidence, and declares limits.

Claim boundary:

The engine does not assess whether Annex IV technical documentation is complete.

---

### Article 12 — Record-Keeping

Engine-relevant surfaces:

- `receipt_quality`
- `evidence_fit`
- `replayability`

Structural relation:

The engine can show whether an inspectable receipt, evidence reference, or replay surface is present.

Claim boundary:

The engine does not assess whether logging mechanisms meet Article 12 requirements.

---

### Article 13 — Transparency and Provision of Information to Deployers

Engine-relevant surfaces:

- `claim_boundedness`
- `object_clarity`
- `claim_limits`
- report output

Structural relation:

The engine can show whether the submitted proof object states what is being claimed, what is being inspected, and what is not proven.

Claim boundary:

The engine does not assess whether information supplied to deployers is complete, accessible, appropriate, or legally sufficient.

---

### Article 14 — Human Oversight

Engine-relevant surfaces:

- `authority_trace`
- `condition_clarity`
- `downstream_effect`

Structural relation:

The engine can show whether authority is identified, whether intervention/condition states are known, and whether downstream movement is marked blocked, allowed, unknown, or not applicable.

Claim boundary:

The engine does not assess whether human oversight measures meet Article 14.

---

### Article 17 — Quality Management System

Engine-relevant surfaces:

- `authority_trace`
- `condition_clarity`
- `evidence_fit`
- manifest discipline

Structural relation:

The engine can show whether proof-pack evidence is organised and registry-controlled.

Claim boundary:

The engine does not assess quality management system adequacy.

---

### Article 18 — Documentation Keeping

Engine-relevant surfaces:

- `receipt_quality`
- report output
- golden reports
- manifest registry

Structural relation:

The engine can preserve pinned reports and example receipts for regression inspection.

Claim boundary:

The engine does not assess whether provider documentation-retention obligations are satisfied.

---

### Article 43 — Conformity Assessment

Engine-relevant surfaces:

- report output
- manifest registry
- golden reports
- evidence model

Structural relation:

The engine can organise proof packs into reviewable artefacts.

Claim boundary:

The engine does not conduct conformity assessment.

---

### Annex IV — Technical Documentation Contents

Engine-relevant surfaces:

- `object_clarity`
- `claim_boundedness`
- `evidence_fit`
- `claim_limits`
- report output

Structural relation:

The engine can assist internal organisation of proof artefacts.

Claim boundary:

The engine does not generate, validate, or complete Annex IV technical documentation.

---

### Annex VII — Conformity Based on Quality Management System and Technical Documentation

Engine-relevant surfaces:

- manifest registry
- report outputs
- golden reports
- public API contract
- changelog
- roadmap

Structural relation:

The engine can show controlled evidence handling and regression stability for its own proof-pack examples.

Claim boundary:

The engine does not establish an approved quality management system or assess technical documentation.

---

## Stop Line

This document maps inspection surfaces to regulatory pressure points.

It does not convert inspection output into a regulatory conclusion.

A proof object should prove the claim attached to it — not less, not everything.
