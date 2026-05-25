# Common Proof Failures

> These are the most frequent reasons a proof pack returns HOLD or FAIL.  
> Each failure describes what was submitted, why it does not work, and what to do instead.

---

## 1. Policy treated as proof

**What happens**: The authority block references a policy document. The claim says "the system followed policy X".

**Why it fails**: A policy is a statement of intent. It is not evidence that the policy was followed in this specific event. A policy reference belongs in `authority`. The evidence that the policy was applied belongs in `evidence`.

**Fix**: Add an `evaluation_trace` or `decision_log` to `evidence` that shows the policy was evaluated at the time of the event.

---

## 2. Dashboard treated as interruption evidence

**What happens**: Evidence points to a monitoring dashboard screenshot.

**Why it fails**: A dashboard shows a state at a point in time. It does not prove that a specific interruption occurred, when it occurred, or what path was blocked.

**Fix**: Add a timestamped event log or interruption record to `evidence`. The dashboard may be supplementary, not primary.

---

## 3. Log treated as receipt

**What happens**: `receipt` references a system log file.

**Why it fails**: A log is a continuous record. A receipt is a discrete, signed acknowledgement of a specific event. Logs can be amended; receipts are immutable by definition.

**Fix**: Generate a dedicated receipt at the point of the event — a hash-stamped, timestamped record tied to the specific claim event.

---

## 4. Human oversight declared without authority

**What happens**: A condition says "human oversight was present". The authority block is empty.

**Why it fails**: Human oversight requires a named human or human-approved policy as authority. Without a reference, the oversight claim cannot be inspected or replayed.

**Fix**: Populate `authority` with the specific human role or policy that granted oversight. Add an escalation record to `evidence`.

---

## 5. Broad claim with narrow evidence

**What happens**: The claim says "the system is safe for production use". Evidence covers one test case.

**Why it fails**: The evidence proves a narrow claim (this test passed). The stated claim is broad (system-wide safety). The engine will return HOLD on `evidence_fit`.

**Fix**: Reduce the claim to match the evidence, OR add evidence that supports the broader claim.

---

## 6. Refusal declared but downstream path not proven blocked

**What happens**: The claim says a mutation was refused. `downstream_effect` is absent or status is `unknown`.

**Why it fails**: A refusal claim requires proof that the downstream path was actually closed — not just that a HOLD was issued.

**Fix**: Populate `downstream_effect` with status `blocked` and a description of how closure was confirmed.

---

## 7. No replay surface

**What happens**: `replay` is absent or `present: false`.

**Why it fails**: Without a replay fixture, the claim cannot be independently reproduced. It is a one-time assertion, not an inspectable proof.

**Fix**: Create a replay fixture that reproduces the conditions of the claim event. Reference it in the `replay` block.

---

## 8. No claim limit

**What happens**: `claim.limits` is empty.

**Why it fails**: An unlimited claim is an infinite claim. The engine cannot assess fit between evidence and claim if the claim has no boundary.

**Fix**: Add at least one explicit limit: scope, time range, event ID, or system boundary.

---

## 9. No chain of custody

**What happens**: Evidence references exist but do not link back to the claim event via timestamps, IDs, or version references.

**Why it fails**: Without a chain of custody, evidence could belong to a different event. The inspector cannot verify continuity.

**Fix**: Each evidence item must include a reference that ties it to the specific claim event (event ID, timestamp range, policy version).

---

## 10. No version or policy reference

**What happens**: The authority block has a type but no reference, or the reference is generic (e.g., "internal policy").

**Why it fails**: A policy that cannot be versioned cannot be inspected. If the policy changed after the event, the reference is meaningless.

**Fix**: Include the specific policy version and section number in `authority.reference`.

---

*The stop line: a proof object should prove the claim attached to it — not less, not everything.*
