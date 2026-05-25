# EU AI Act — Proof Structure Inspection Mapping

> **Scope note**: This document maps the inspection engine's surfaces
> against EU AI Act pressure points. It does **not** certify compliance,
> legal sufficiency, or audit readiness. It is a structural reference only.

---

## How to Read This Map

Each row shows:
- The EU AI Act article or annex that creates a governance pressure
- The inspection engine surface(s) that are *relevant* to that pressure
- What kind of gap the engine can detect

The engine can tell you whether a proof structure is *inspectable*.
It cannot tell you whether it *satisfies* a regulator.

---

## Mapping Table

| EU AI Act Reference | What It Requires | Engine Surface | Detectable Gap |
|---|---|---|---|
| **Art. 9** — Risk management system | Ongoing identification, analysis, and mitigation of risks | `conditions` / `evidence` / `limits` | Missing conditions, unknown results, absent limits |
| **Art. 11** — Technical documentation | Documentation of system design, capabilities, and limitations | `object` / `claim` / `evidence` | Unclear object, missing evidence, unbounded claim |
| **Art. 12** — Record-keeping / automatic logs | Logs generated automatically throughout lifecycle | `receipt` / `replay` | Absent receipt, no replay trace, unknown downstream effect |
| **Art. 14** — Human oversight | Humans able to monitor, interpret, override, and stop | `authority` / `receipt` / `replay` | Unknown authority type, no intervention record |
| **Art. 17** — Quality management system | Documented processes for design, development, testing | `authority` / `conditions` / `evidence` | Missing authority trace, undocumented process evidence |
| **Art. 18** — Documentation keeping | Records retained and accessible to regulators | `receipt` / `limits` | No receipt, no explicit scope or exclusion statement |
| **Art. 72** — Post-market monitoring | Ongoing monitoring after deployment | `replay` / `receipt` | No replay surface, no incident trace, no lifecycle evidence |
| **Annex IV** — Technical documentation contents | Specific required documentation fields | `object` / `claim` / `evidence` / `limits` | Missing fields, overbroad claim, absent what-is-not-proven |
| **Annex VII** — Conformity via quality mgmt + tech docs | Internal quality management + documentation match | Full chain: all eight dimensions | Any FAIL or unresolved HOLD |

---

## What This Engine Cannot Do

- It cannot determine whether documentation *meets* regulatory standard
- It cannot substitute for legal counsel or an accredited audit body
- It cannot assess system behaviour — only the proof structure submitted
- It cannot certify, approve, or clear any system for deployment

---

## Stop Line

A proof object should prove the claim attached to it — not less, not everything.

The engine checks whether the structure is there. Whether it is *enough* is a human decision.
