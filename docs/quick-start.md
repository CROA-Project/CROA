# Quick Start

Fifteen minutes from nothing to a running demonstrator, an audit log you can read, and something
concrete to disagree with. Your first contribution to CROA is a finding, not a pull request.

---

## 1. Understand the claim (3 min)

Read the [one-page architecture overview](architecture-overview.md). The single thing to hold onto: *unauthorized actions don't reach the system because there's no path for them — not because the agent was told not to.*

## 2. Run the reference harness (8 min)

The vendor-neutral **Minimal Reference Harness** demonstrates a *reduced* control plane — mock `C1`, `C2`, `C3`, `C5`, `C6`, `C7`, with **no `C4`** (trajectory state) and **no admission layer** (no authentication, RBAC, or AQL) — using no commercial software. It ships four of the specification's **reference negative tests** (NT-001 to NT-004), plus the replay step of NT-007. It does not demonstrate C1–C7; see [`spec/known-defects-harness.md`](../spec/known-defects-harness.md) for what it does and does not establish.

> **What the harness is, precisely.** It is a *demonstrator*: a self-contained mock of the control plane, so its assertions check that the mock behaves as the specification describes. That makes it a useful way to see the mechanism and the event log — it is **not** evidence that a real implementation has the properties, and it is not an experiment. NT-005 (ambiguous `E3` verdict), NT-006 (trajectory), and NT-008 (authority non-expansion) are not implemented there; they require a semantic analyzer, `C4` state, and a delegation model respectively. NT-007 covers replay and, since September 2026, double pre-compilation and concurrent redemption — but not scope widening. The evidence buckets CROA has and has not filled are listed in [`evidence/README.md`](../evidence/README.md).

```bash

# from the croa-reference-harness repository

git clone https://github.com/CROA-Project/croa-reference-harness.git
cd croa-reference-harness

# follow the harness README for prerequisites, then:

make demo        # or: python3 -m mrh   (see the harness README)
```

You should see the harness run these and record each in a `C5` event log:

1. **Non-CC execution blocked** — an operation with no Compiled Commitment is refused at the boundary.
2. **Expired CC blocked** — a commitment past its validity is refused.
3. **Replay blocked** — an already-redeemed commitment cannot be reused.
4. **Unregistered context blocked** — an action against a target absent from the Golden Record is stopped before evaluation.

## 3. Read the evidence it produced (2 min)

Open the generated `C5` log. Each line is a typed, signed, hash-chained event. Confirm for yourself that:

- every blocked action has a recorded reason, and
- no execution event exists without a preceding valid commitment.

The harness exposes two checks, and the difference between them is the whole point:

- **`verify_chain()`** recomputes the hash chain and each signature. It establishes that the events
  present were not altered or reordered — **and nothing else**. Until September 2026 this was all
  `verify()` did, which is why an independent audit could produce a log containing *two* authorized
  executions from one single-use authorization that verified as valid.
- **`verify_decisions()`** performs the Appendix G.2.4 correlation: every commitment cites an earlier
  permit, at most one execution per commitment, **at most one execution per authorization**, and the
  executing subject is the one the commitment was compiled for.
- **`verify()`** does both.

Read a passing `verify()` as the *shape* of a reconstructable record, not as the auditability
property holding for a real system. A chain establishes the ordering and non-alteration of the events
it contains — not that every governed action produced one. That distinction is why the
specification's property is named **Decision Reconstructability** and not "evidence completeness":
see **P-E** in [`spec/properties.md`](../spec/properties.md), and
[`spec/known-defects-harness.md`](../spec/known-defects-harness.md) for what the harness does and does
not establish.

## 4. File your first finding (2 min)

Now you have standing to react. Pick whichever fits:

- *"I think the guarantee fails if…"* → [Challenge the Claim](https://github.com/CROA-Project/CROA/issues/new?template=challenge-the-claim.yml)
- *"This part of the spec is unclear…"* → [Clarification issue](https://github.com/CROA-Project/CROA/issues/new?template=clarification.yml)
- *"I want to govern a real workflow with this"* → the [Pilot Program](../public-review/pilot-program.md)
- *"Here's a question I can't answer"* → comment on the [Research Questions](../public-review/research-questions.md)

---

> **Note:** the harness lives at [`CROA-Project/croa-reference-harness`](https://github.com/CROA-Project/croa-reference-harness) and is public. Tell us what else you'd want it to demonstrate — the gaps it does *not* cover are listed in its README, and closing one is the most useful first contribution to that repository.
