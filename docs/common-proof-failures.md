# Common Proof Failures

The most frequent mistakes that cause proof packs to fail structural inspection.

None of these failures mean the underlying system is unsafe.
They mean the proof structure cannot support the claim attached to it.

---

## 1. Policy Treated as Proof

**What happens**: A policy document is listed as evidence that a behaviour occurred.

**Why it fails**: Policy says what *should* happen. Evidence must show what *did* happen.
A written rule is not a proof of execution.

**Fix**: Add system logs, execution traces, or evaluation records that show the policy was triggered and its outcome.

---

## 2. Dashboard Treated as Interruption

**What happens**: A monitoring dashboard screenshot is submitted as proof that an AI action was stopped.

**Why it fails**: A dashboard shows current state. It does not prove a specific event occurred at a specific time, or that a downstream path was blocked.

**Fix**: Provide a timestamped log entry, a refusal receipt, and a downstream effect status.

---

## 3. Log Treated as Receipt

**What happens**: A raw system log is submitted as a receipt.

**Why it fails**: A log is a record. A receipt is a confirmed acknowledgement that a specific event occurred and was registered — ideally signed, timestamped, and linked to a specific claim.

**Fix**: Generate a dedicated receipt object with `id`, `timestamp`, `downstream_effect_status`, and optionally `signed_by`.

---

## 4. Human Oversight Without Authority

**What happens**: A proof pack claims human oversight but the authority block is absent or type is unknown.

**Why it fails**: Oversight without traceable authority is not inspectable. The engine cannot confirm that the right human, with the right authority, was involved.

**Fix**: Add an authority block with `type`, `id`, and `granted_by`.

---

## 5. Broad Claim With Narrow Evidence

**What happens**: The claim says the system is "safe", "compliant", or "trusted". The evidence shows one log entry from one test run.

**Why it fails**: The evidence proves a specific, bounded event. The claim implies a universal property. The engine flags this as a claim-evidence mismatch.

**Fix**: Either narrow the claim to match the evidence ("The system refused binding instruction #42") or provide evidence sufficient to support the broad claim.

---

## 6. Refusal Declared but Downstream Path Not Proven Blocked

**What happens**: The claim is "the system refused an instruction" but the receipt has no `downstream_effect_status`, or it is `unknown`.

**Why it fails**: Refusing an instruction is only meaningful if the downstream path was actually blocked. Without evidence the path was closed, the refusal may not have had effect.

**Fix**: Add `downstream_effect_status: "path_blocked"` to the receipt, with supporting evidence.

---

## 7. No Replay Surface

**What happens**: A claim is made but no fixture or trace exists that would allow the event to be replayed or independently verified.

**Why it fails**: Without a replay surface, a reviewer cannot verify the claim occurred as described. It is a closed proof — trust without verifiability.

**Fix**: Add a `replay` block with a `fixture` (input state) and/or `trace` (execution log).

---

## 8. No Claim Limit

**What happens**: The proof pack has no `limits` block, or the `what_is_not_proven` field is absent.

**Why it fails**: Without explicit limits, the claim boundary is undefined. A reviewer cannot know what the pack *is not* claiming. This creates overclaim risk.

**Fix**: Add a `limits` block. State the scope explicitly. List at minimum: EU AI Act compliance, legal sufficiency, full system safety.

---

## 9. No Chain of Custody

**What happens**: Evidence items have no `id`, no `type`, and no link back to the claim or object.

**Why it fails**: Evidence must be traceable — from the claim, to the object, to the evidence item, to the source. Without chain of custody, the evidence cannot be audited.

**Fix**: Give every evidence item a unique `id`, a `type`, and a `proves` field describing what specific sub-claim it supports.

---

## 10. No Version or Policy Reference

**What happens**: Evidence or authority blocks reference unnamed or unversioned policies.

**Why it fails**: If the policy changed between the event and the inspection, the proof becomes ambiguous. The engine cannot confirm which version was active.

**Fix**: Include version identifiers in authority and evidence blocks (e.g., `"id": "ALVIAN-POLICY-v1.1"`).

---

## Stop Line

A proof object should prove the claim attached to it — not less, not everything.
