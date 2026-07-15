# Quick Start

**Objective:** get you from zero to a *verifiable* result — and your first contribution — in about 15 minutes.
**Audience:** implementers and engineers who learn by running things.

> Your first contribution to CROA is a **finding**, not a pull request. The goal of this page is to get you to something you can react to.

---

## 1. Understand the claim (3 min)

Read the [one-page architecture overview](architecture-overview.md). The single thing to hold onto: *unauthorized actions don't reach the system because there's no path for them — not because the agent was told not to.*

## 2. Run the reference harness (8 min)

The vendor-neutral **Minimal Reference Harness** demonstrates the C1–C7 enforcement behavior with no commercial software. It ships four **reference negative tests** — the minimum mechanical evidence that the key properties hold.

```bash

# from the croa-reference-harness repository

git clone https://github.com/croa-project/croa-reference-harness.git
cd croa-reference-harness

# follow the harness README for prerequisites, then:

make demo        # or: python3 -m mrh   (see the harness README)
```

You should see the harness run these and record each in a `C5` event log:

1. **Non-CC execution blocked** — an operation with no Compiled Commitment is refused at the boundary.
2. **Expired CC blocked** — a commitment past its validity is refused.
3. **Replay blocked** — a already-redeemed commitment cannot be reused.
4. **Unregistered context blocked** — an action against a target absent from the Golden Record is stopped before evaluation.

## 3. Read the evidence it produced (2 min)

Open the generated `C5` log. Each line is a typed, signed, hash-chained event. Confirm for yourself that:

- every blocked action has a recorded reason, and
- no execution event exists without a preceding valid commitment.

This is the auditability property in miniature: the decisions are reconstructable from the log alone.

## 4. File your first finding (2 min)

Now you have standing to react. Pick whichever fits:

- *"I think the guarantee fails if…"* → [Challenge the Claim](../.github/ISSUE_TEMPLATE/challenge-the-claim.yml)
- *"This part of the spec is unclear…"* → [Clarification issue](../.github/ISSUE_TEMPLATE/clarification.yml)
- *"I want to govern a real workflow with this"* → the [Pilot Program](../public-review/pilot-program.md)
- *"Here's a question I can't answer"* → comment on the [Research Questions](../public-review/research-questions.md)

---

> **Note:** the harness lives at [`croa-project/croa-reference-harness`](https://github.com/croa-project/croa-reference-harness). The commands above are the real ones; the clone URL resolves once that repository is public. If you're reading this before then, start with the [architecture overview](architecture-overview.md) and the [research questions](../public-review/research-questions.md) — and tell us what you'd want the harness to demonstrate.
