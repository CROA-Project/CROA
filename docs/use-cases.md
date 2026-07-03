# Use Cases

**Objective:** show, with concrete sector examples, the kinds of failure CROA is meant to prevent — and invite you to bring your own.
**Audience:** architects and decision-makers assessing fit.
**Authoritative source:** Appendices H and P of the specification (worked examples). These are illustrative summaries.

> These are *scenarios the architecture is designed to handle*, not adoption claims. Whether it handles them well in practice is what the [Pilot Program](../public-review/pilot-program.md) is for.

---

## Customer support — refund limits under pressure

An agent can issue refunds, with a rule: no refund over €500 without manager approval. Under pressure it reasons toward a €900 refund (or splits it). **Without enforcement,** the rule is a suggestion. **With CROA,** the over-limit refund has no path to execution; the only way through is an explicit signed authorization, and both the block and any exception are recorded.

## Data handling — gradual exfiltration (luxury / VIP data)

A clienteling agent legitimately reads VIP profiles one at a time. No single read is suspicious; the *cumulative* pattern reconstructs a customer database. Per-action checks miss it. **C4 trajectory monitoring** tracks the cumulative count and raises an alert before a hard limit, and denies the action that would cross it.

## Logistics — safety thresholds under operational pressure

A routing agent, told to free up capacity, reclassifies cold-chain shipments as standard or changes a safety threshold. **CROA** registers safety-critical parameters as invariants requiring C1 authorization; the agent cannot reclassify them on its own, and any authorized exception is signed and audited.

## E-commerce — refund farming across a window

Many individually-small refunds to one customer, each permitted alone, together exceed a fraud threshold over a rolling window. **C4** maintains the cumulative total and denies the action that would breach it — catching the pattern, not just the instance.

## Healthcare (NovaCare) — generated actions touching PHI

An agent generates code/queries that could create a PHI-exfiltration path. This is an **E3** (semantic) invariant — checked by an approximate analyzer that fails safe (ambiguous → deny). The worked example shows how the architecture handles approximate evaluation and where its costs and limits are.

---

## Bring your own

The most useful thing you can add here is **your** scenario:

- a workflow where you're unsure CROA's guarantee would hold (→ [Challenge the Claim](../.github/ISSUE_TEMPLATE/challenge-the-claim.yml)), or
- one you'd like to govern and are willing to pilot (→ [Pilot Program](../public-review/pilot-program.md)).

Real scenarios — especially the awkward ones — are how we learn where the architecture's edges are.
