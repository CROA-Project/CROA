# CROA Pilot Program

CROA needs one thing more than any other: someone outside the project building it against a real
system and reporting what happened. That is what a pilot is. One honest report — including "we tried
and it was too expensive" — moves CROA further than any endorsement.

---

## What a pilot is

A pilot is a time-boxed effort (typically a few weeks) to implement some meaningful slice of CROA and govern a real or realistic agentic workflow with it. You do **not** need to implement the whole framework. The most useful pilots are often narrow and deep.

Good pilot shapes:

- **Single action class, end to end.** Govern one class of action (e.g., `data.export`, `refund.issue`, `code.deploy`) through the full path: context grounding → evaluation → compiled commitment → execution-boundary enforcement → audit.
- **Reference harness + one real adapter.** Start from the [Minimal Reference Harness](https://github.com/CROA-Project/croa-reference-harness) and connect it to one real system.
- **Conformance probe.** Attempt to reach a specific conformance level (e.g., L4 for one boundary) and document where you got stuck.
- **Adversarial pilot.** Try to *break* a governed workflow — reach a prohibited end-state — and report whether you could.

## What we ask back

A published **evidence report** (see [`evidence/README.md`](../evidence/README.md)). It should cover:

- what you implemented and what you deliberately left out;
- what worked, what didn't, and what surprised you;
- **cost and friction:** integration effort, latency observed, false-positive/deny rates;
- which [research questions](research-questions.md) your pilot bears on (`RQ-` IDs);
- if it failed or you abandoned it: **why** — this is the most valuable report of all.

Reports may be anonymized or use a pseudonymous organization name if commercial sensitivity requires it. We care about the findings, not the logo.

## What we provide

- **Direct maintainer support** during the pilot (a dedicated Discussion thread, and a call where scheduling allows). CROA is maintained by two people on a best-effort basis; we will tell you what we can commit to before you start, rather than after.
- **Fast-track triage** for issues you hit, labeled `pilot-feedback`.
- **Co-development of the report** if you want help structuring it (we will never edit your findings).
- **Recognition:** pilots are credited in release notes and in a public "Implementations & Evidence" index; pilot leads are strong candidates for the review board.

## What we will not do

- We will not pressure you to report a success. A failed pilot that teaches us where CROA is too costly or unclear is a first-class outcome.
- We will not require any specific product. CROA is implementation-agnostic; build it however you like.
- We will not publish your internal details without consent.

## How to start a pilot

1. Open a **"Pilot proposal"** Discussion: the workflow you want to govern, the slice of CROA you'll implement, your rough timeline, and any constraints.
2. A maintainer responds within a few days to help scope it and flag known pitfalls.
3. You build. Ask questions in your pilot thread; we prioritize them.
4. You publish an evidence report (PR into `evidence/reports/`). We index it and fold any findings into the review process / RFCs.

## Why this matters for you, not just for CROA

Beyond contributing to the field: a pilot gives your team a concrete, defensible position on agentic-AI governance — a working reference, measured costs, and a documented point of view — well ahead of the market. Early pilots also shape the framework while it is still malleable.

→ Ready? Open a Pilot proposal Discussion, or read the [evidence report templates](../evidence/README.md) first.
