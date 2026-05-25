# Independent Reviewer Guide

Status: v0.2.0  
Scope: how to review Artifact Readiness Engine outputs without inflating them into certification claims.

This guide is for reviewers inspecting proof-pack reports produced by Artifact Readiness Engine.

It is not a legal review guide, regulatory submission guide, or conformity assessment procedure.

---

## Hard Non-Claims

A report from this engine does not prove:

- EU AI Act compliance
- legal sufficiency
- production safety
- independent audit approval
- notified-body acceptance
- conformity assessment readiness
- system-wide governance effectiveness
- future behaviour of the system

A report only addresses this question:

```text
Can this submitted proof object support the bounded claim attached to it?
```

---

## Reviewer Posture

Review the report as a proof-structure triage object.

Do not treat it as:

- a certification
- a compliance opinion
- an audit sign-off
- a legal conclusion
- a safety guarantee

Use it to identify:

- what is claimed
- what is evidenced
- what is missing
- what is overbroad
- what needs human or independent review

---

## Review Sequence

### 1. Read the claim first

Check:

- Is the claim narrow?
- Is the claim event-bound, object-bound, or scope-bound?
- Does the claim include broad words such as safe, secure, compliant, trusted, certified, or governed?

Reviewer question:

```text
What is the smallest claim this report is allowed to support?
```

---

### 2. Check the claim limits

Check:

- Does the report state what is not proven?
- Are time, environment, object, or system boundaries declared?
- Does the claim try to stretch beyond the evidence?

Reviewer question:

```text
Where does the proof stop?
```

---

### 3. Inspect the object

Check:

- Is the inspected object identifiable?
- Is there an event id, request id, receipt id, or transition id?
- Is the object description specific enough for another reviewer to locate it?

Reviewer question:

```text
What exactly is being inspected?
```

---

### 4. Inspect authority

Check:

- Is authority type declared?
- Is the authority reference present?
- Is authority human, role, policy, system, or hybrid?
- Is authority merely named, or supported by evidence?

Reviewer question:

```text
Who or what was allowed to bind, refuse, interrupt, or approve movement?
```

---

### 5. Inspect conditions

Check:

- Are conditions explicit?
- Are condition results known?
- Are unknown conditions holding the report at HOLD?
- Are condition results backed by evidence references?

Reviewer question:

```text
Which conditions had to hold before movement was admissible?
```

---

### 6. Inspect evidence fit

Check:

- Does evidence exist?
- Does each evidence item directly support the claim?
- Is evidence merely surrounding context?
- Does evidence prove a weaker claim than stated?

Reviewer question:

```text
Does this evidence prove the claim, or only describe the area around it?
```

---

### 7. Inspect receipt quality

Check:

- Is a receipt present?
- Does it have a reference?
- Does it include time, event, authority, and outcome information?
- For refusal/interruption claims, can the stop be inspected?

Reviewer question:

```text
What receipt lets another operator inspect the stop or allow event?
```

---

### 8. Inspect replayability

Check:

- Is replay declared?
- Is a fixture, trace, or reconstruction surface present?
- Are missing inputs named?
- Is replay unnecessary only because the claim type is documentation?

Reviewer question:

```text
Can the event be reconstructed or challenged under known conditions?
```

---

### 9. Inspect downstream effect

For refusal or interruption claims, check:

- Is downstream effect marked blocked?
- Is downstream effect unknown?
- Are queues, retries, handles, or partial states accounted for?
- Does the report show consequence path closure, or only declared refusal?

Reviewer question:

```text
Did consequence remain possible after the claimed stop?
```

---

## Interpreting Status

### PASS

A PASS means:

```text
The proof pack is structurally inspectable for the attached bounded claim.
```

Reviewer action:

- Accept as structurally ready for the stated claim only.
- Do not generalise beyond the stated limits.
- Check whether independent verification is still required.

### HOLD

A HOLD means:

```text
The proof pack is incomplete, ambiguous, or missing a surface needed to support the claim confidently.
```

Reviewer action:

- Identify the missing surface.
- Request the next evidence item.
- Do not treat the claim as proven.

### FAIL

A FAIL means:

```text
The submitted artefact cannot support the stated claim in its current form.
```

Reviewer action:

- Reduce the claim, add evidence, or reject the proof pack.
- Do not infer legal non-compliance from the FAIL.
- Do infer that this proof object is not fit for the stated claim.

---

## Reviewer Output Template

```text
Reviewer verdict: PASS / HOLD / FAIL

Claim reviewed:
<claim>

Strongest supported claim:
<smallest defensible claim>

Unsupported claim pressure:
<where the artefact overreaches>

Missing evidence:
<receipt / replay / authority / downstream / limits / other>

Recommended next action:
<add evidence / reduce claim / human review / independent review>

Non-claim:
This review does not certify compliance, safety, legality, or production readiness.
```

---

## Common Review Errors

Avoid these errors:

- Treating PASS as certification.
- Treating HOLD as failure.
- Treating FAIL as legal non-compliance.
- Treating logs as receipts without checking what they prove.
- Treating dashboard visibility as interruption capability.
- Treating authority labels as authority evidence.
- Treating a refusal event as downstream closure.
- Letting a narrow proof object support a broad claim.

---

## Stop Line

A reviewer should not ask a proof object to prove the universe.

A proof object should prove the claim attached to it — not less, not everything.
