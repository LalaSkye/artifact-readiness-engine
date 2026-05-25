# Proof Structure Inspection Model

Status: v0.1 research note  
Scope: artefact inspection, not certification

## Purpose

This model checks whether a governance, AI-control, or audit-facing artefact can support the claim attached to it.

It does not decide whether a system is safe, lawful, compliant, or production-ready.

It asks a smaller inspection question:

> What exactly does this artefact prove, and what does it not prove?

## Core inspection chain

```text
Claim
→ Object
→ Authority
→ Conditions
→ Evidence
→ Receipt
→ Replay
→ Limit
```

## 1. Claim

The claim must be narrow enough to inspect.

Weak claim:

```text
This system is governed.
```

Inspectable claim:

```text
This requested action was refused before downstream consequence could bind.
```

Inspection question:

```text
What is the smallest claim this artefact is supposed to prove?
```

## 2. Object

The inspected object must be explicit.

Possible objects:

- request
- decision
- transition
- refusal
- receipt
- audit event
- downstream consequence path
- model output
- human approval
- execution attempt

Inspection question:

```text
What exactly is being inspected?
```

## 3. Authority

The artefact should identify who or what had authority to approve, deny, interrupt, or escalate the action.

Inspection question:

```text
Who or what was allowed to bind consequence?
```

## 4. Conditions

The artefact should state the conditions under which the action was admissible.

Common conditions:

- role
- scope
- time
- policy version
- model version
- environment
- risk threshold
- approval state
- evidence freshness

Inspection question:

```text
Which conditions had to hold before movement was permitted?
```

## 5. Evidence

The artefact should provide evidence that maps directly to the claim.

Weak evidence:

```text
Dashboard shows governance status: green.
```

Stronger evidence:

```text
Event record shows request, policy version, authority check, failed condition, refusal event, and downstream route blocked.
```

Inspection question:

```text
Does the evidence prove the claim, or only describe surrounding governance?
```

## 6. Receipt

A receipt is the inspectable record that allows another operator to see what happened.

A useful receipt should include:

- timestamp
- event identifier
- actor or system component
- requested action
- authority basis
- condition result
- allow/refusal outcome
- downstream effect status
- policy or rule reference
- evidence hash or custody pointer where available

Inspection question:

```text
What receipt would allow another operator to inspect the stop or allow event?
```

## 7. Replay

Replay means another operator can reconstruct or challenge the event under known conditions.

Replay may require:

- input state
- policy version
- model version
- environment state
- dependency versions
- receipt chain
- test fixture
- expected outcome

Inspection question:

```text
Can this event be reconstructed, challenged, or replayed?
```

## 8. Limit

The artefact must state what it does not prove.

Example:

```text
This receipt proves that this request was refused under these conditions.
It does not prove that the whole system is safe, compliant, or free from other failure modes.
```

Inspection question:

```text
Where does the proof stop?
```

## Readiness states

### PASS

The artefact contains enough bounded evidence to support the attached claim under inspection.

### HOLD

The artefact is incomplete, ambiguous, or not yet replayable. The claim may be plausible, but the proof surface is not ready.

### FAIL

The artefact cannot support the claim, or the evidence proves a different/weaker claim.

## Minimal scoring dimensions

| Dimension | Question | State |
|---|---|---|
| Claim boundedness | Is the claim narrow enough to inspect? | PASS/HOLD/FAIL |
| Object clarity | Is the inspected object explicit? | PASS/HOLD/FAIL |
| Authority trace | Is authority identified? | PASS/HOLD/FAIL |
| Condition clarity | Are admissibility conditions explicit? | PASS/HOLD/FAIL |
| Evidence fit | Does evidence map to the claim? | PASS/HOLD/FAIL |
| Receipt quality | Is there an inspectable record? | PASS/HOLD/FAIL |
| Replayability | Can the event be reconstructed or challenged? | PASS/HOLD/FAIL |
| Claim limit | Does the artefact say what is not proven? | PASS/HOLD/FAIL |

## Stop line

A proof object should prove the claim attached to it — not less, not everything.
