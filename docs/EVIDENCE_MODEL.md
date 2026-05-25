# Evidence Model

Status: v0.2.0  
Scope: score-surface meaning, evidence requirements, and claim boundaries.

This document explains what each inspection surface proves, what it does not prove, and what evidence upgrades it.

The engine does not certify compliance, safety, legality, production readiness, or EU AI Act conformity.

It checks whether a submitted proof object can support the bounded claim attached to it.

---

## Summary Table

| Surface | What it asks | PASS means | HOLD means | FAIL means |
|---|---|---|---|---|
| `status` | What is the overall verdict? | All required surfaces passed | At least one surface is incomplete or ambiguous | At least one required surface cannot support the claim |
| `claim_boundedness` | Is the claim narrow enough to inspect? | Claim and limits are present | Broad claim pressure exists | Claim text absent |
| `object_clarity` | Is the inspected object clear? | Object id or description exists | Not currently used | Object missing |
| `authority_trace` | Is authority identifiable? | Authority type and reference exist | Authority unknown or incomplete | Not currently used |
| `condition_clarity` | Are conditions known? | All conditions have known results | One or more conditions are unknown | Not currently used |
| `evidence_fit` | Does evidence support the claim? | Evidence exists and supports claim | Evidence exists but does not fully support claim | Evidence missing |
| `receipt_quality` | Is there an inspectable receipt? | Receipt exists with reference | Receipt absent/incomplete where still recoverable | Receipt absent for claim type that requires it |
| `replayability` | Can the event be reconstructed? | Replay declared or not required | Replay absent where useful | Not currently used |
| `downstream_effect` | Was downstream movement blocked/allowed as claimed? | Effect matches claim requirements | Effect unknown or not blocked for refusal | Not currently used |
| `claim_limits` | Does the proof say where it stops? | Limits declared | Not currently used | Limits missing |

---

## `status`

### What it proves

`status` is the overall inspection verdict.

It proves only that the submitted proof pack received the weakest result across all inspected score surfaces.

### What it does not prove

It does not prove:

- legal compliance
- operational safety
- production readiness
- independent audit approval
- EU AI Act conformity
- future system behaviour

### Upgrade evidence

To improve `status`, improve the weakest score surface first.

The engine follows the lowest-confidence surface. One bad surface can keep the whole pack at HOLD or FAIL.

---

## `claim_boundedness`

### What it proves

A PASS proves that a claim exists and declared limits are present.

### What it does not prove

It does not prove the claim is true.

It does not prove that the evidence supports the claim.

It only proves that the claim has a visible boundary.

### Minimal upgrade evidence

- Narrow claim text
- Explicit scope
- Explicit non-claims
- Time, event, object, or system boundary

---

## `object_clarity`

### What it proves

A PASS proves that the inspected object is identifiable.

Examples:

- request
- decision
- transition
- refusal
- receipt
- audit event
- execution attempt

### What it does not prove

It does not prove the object behaved correctly.

It does not prove the object is complete, trustworthy, or independently verified.

### Minimal upgrade evidence

- Stable object id
- Description
- Event reference
- Version or timestamp where relevant

---

## `authority_trace`

### What it proves

A PASS proves that the proof pack identifies an authority type and authority reference.

Examples:

- human
- role
- policy
- system
- hybrid authority

### What it does not prove

It does not prove that the authority was correct, lawful, independent, or sufficient.

It does not prove that authority was actually applied unless supporting evidence exists.

### Minimal upgrade evidence

- Authority type
- Authority reference
- Policy version
- Role or human approval basis
- Evaluation trace showing authority was checked

---

## `condition_clarity`

### What it proves

A PASS proves that all listed conditions have known results.

### What it does not prove

It does not prove that the conditions were the right conditions.

It does not prove that the conditions were independently tested.

### Minimal upgrade evidence

- Known result for each condition
- Condition id
- Description
- Evidence pointer for each result

---

## `evidence_fit`

### What it proves

A PASS proves that evidence exists and each submitted evidence item is marked as supporting the stated claim.

### What it does not prove

It does not prove the evidence is authentic, sufficient for legal review, independently audited, or cryptographically protected.

It does not prove the evidence supports broader claims outside the submitted proof pack.

### Minimal upgrade evidence

- Evidence id
- Evidence type
- Reference
- `supports_claim: true`
- Direct link to the inspected event or object

---

## `receipt_quality`

### What it proves

A PASS proves that a receipt exists and has a reference.

For refusal and interruption claims, receipt quality matters because the stop must be inspectable.

### What it does not prove

It does not prove the receipt is immutable, externally audited, cryptographically signed, or legally sufficient.

It does not prove downstream effect unless paired with `downstream_effect`.

### Minimal upgrade evidence

- Receipt present
- Receipt type
- Receipt reference
- Timestamp
- Event id
- Optional signature or hash chain

---

## `replayability`

### What it proves

A PASS proves that a replay surface is declared, or that replay is not required for the claim type.

### What it does not prove

It does not prove replay has been independently performed.

It does not prove replay will reproduce the same result under all conditions.

### Minimal upgrade evidence

- Replay fixture
- Trace
- Inputs
- Policy/model version
- Expected result
- Known missing inputs if incomplete

---

## `downstream_effect`

### What it proves

For refusal/interruption claims, a PASS proves the downstream effect is marked as blocked.

This matters because a refusal only has control value if the consequence path did not remain open.

### What it does not prove

It does not prove every downstream path was blocked.

It does not prove no side effect occurred elsewhere.

It does not prove the system is globally safe.

### Minimal upgrade evidence

- Downstream effect status
- Route closure evidence
- No-mutation record
- Queue/retry/handle status where relevant
- Receipt tying refusal to downstream state

---

## `claim_limits`

### What it proves

A PASS proves that the proof pack includes at least one explicit limit.

### What it does not prove

It does not prove the limits are complete.

It does not prove the claim is safe to publish.

It only proves that the proof surface has a declared edge.

### Minimal upgrade evidence

- What is not proven
- Scope limit
- Time limit
- Environment limit
- Claim boundary

---

## Stop Line

A proof object should prove the claim attached to it — not less, not everything.
