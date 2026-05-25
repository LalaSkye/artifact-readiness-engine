# EU AI Act → Engine Inspection Surface Map

> This map is a structural reference only.  
> The engine does **not** certify EU AI Act compliance.  
> It maps where governance pressure exists so you can see which proof surfaces matter.

---

## Pressure Point → Engine Surface

| EU AI Act Reference | Subject | Engine Surface(s) |
|---------------------|---------|--------------------|
| Article 9 | Risk management system | `conditions`, `evidence`, `claim_limits` |
| Article 11 | Technical documentation | `object`, `claim`, `evidence` |
| Article 12 | Record-keeping / automatic logs | `receipt`, `authority` (trace) |
| Article 14 | Human oversight | `authority`, `conditions` (intervention record) |
| Article 17 | Quality management system | `authority`, `evidence` (process evidence) |
| Article 18 | Documentation keeping | `object`, `receipt`, `replay` |
| Article 72 | Post-market monitoring | `replay`, `downstream_effect`, `evidence` (incident trace) |
| Annex IV | Technical documentation contents | All surfaces — full chain required |
| Annex VII | Conformity assessment (QMS + docs) | `report`, `authority`, `receipt`, `replay` |

---

## What this means in practice

### Article 9 (Risk management)
A risk management system requires documented conditions under which the system is safe to operate. Map your risk thresholds to `conditions`. If any condition result is `unknown`, the engine returns HOLD — risk management is incomplete.

### Article 11 (Technical documentation)
Documentation must describe what the system does and how it was built. The `object` block and `evidence` array are the closest proof-pack equivalents. Missing object description → FAIL.

### Article 12 (Record-keeping / logs)
Automatic logs must be kept for high-risk AI systems. The `receipt` block represents this: a timestamped, referenced record of what happened. Missing receipt on a refusal/interruption claim → FAIL.

### Article 14 (Human oversight)
Human oversight requires that a human can intervene. The `authority` block must reference a human or human-approved policy. Authority type `unknown` → HOLD.

### Article 72 (Post-market monitoring)
Post-market monitoring requires ongoing incident tracking. The `replay` surface and `downstream_effect` block are your closest equivalents. Missing replay → HOLD (unless documentation claim type).

### Annex IV (Technical documentation contents)
All eight proof-pack surfaces must be populated for documentation that could support Annex IV requirements.

---

*This map is for structural orientation only. It is not legal advice and does not constitute an EU AI Act compliance assessment.*
