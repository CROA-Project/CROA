# Evidence

This is where reports go when someone actually implements, benchmarks, or assesses CROA. Every report
is indexed, including — especially — the ones where it didn't work. Evidence is what will eventually
justify CROA's claims or refute them, and right now there is very little of it.

---

## Where CROA's evidence base actually stands

Before asking for evidence, here is what exists. Five of seven buckets are empty, and we would rather
say so than let a reader infer otherwise from the presence of a harness and a benchmark.

| Evidence type | Status |
|---|---|
| Author-controlled testing | **Present** — the reference harness and the founding study. (CROA-Bench, an internal metric seed, is not yet published and is not counted here.) |
| Reproducible testing | **Partial** — the harness runs deterministically on a clean machine, but what it reproduces is authored fixtures and mock behaviour, not system behaviour. |
| Adversarial testing | **Empty** |
| Independent replication | **Empty** |
| Multi-implementation validation | **Empty** |
| Multi-domain validation | **Empty** |
| Enterprise / production validation | **Empty** |

Two things to hold together when reading that table. First, an empty independent-replication bucket
is **field-normal** in agentic runtime governance as of August 2026 — several of the closest published
frameworks have no empirical evaluation at all, and the most directly comparable architecture reports
an author-run one. Second, field-normal is not the same as sufficient, and it is not the reason we
publish the table: we publish it so a reader knows what our claims rest on without reconstructing it
from seven Parts.

Detail, including what the founding study does and does not establish — and why its *currency*
(it evaluated an earlier architecture) matters more than its *independence* — is in
[`docs/limitations.md`](../docs/limitations.md) §4; the experiments that would most change this
picture are in §5 of the same page. A report against any of them — favourable or not — is the single
most useful thing anyone can contribute right now.

## What counts as evidence

| Kind | Use the template | Captures |
|---|---|---|
| **Implementation report** | [`templates/implementation-report.md`](templates/implementation-report.md) | You built CROA (in whole or part) and ran it. What worked, what it cost. |
| **Benchmark report** | [`templates/implementation-report.md`](templates/implementation-report.md) (Performance section) | Latency/throughput/overhead measurements (RQ-5, RQ-6). |
| **Failure / lessons-learned report** | [`templates/failure-report.md`](templates/failure-report.md) | You tried and it didn't work, or you abandoned it. **The highest-value report.** |
| **Architecture review** | implementation-report (Review section) | A structured critique from applying CROA to a design without full implementation. |
| **Adoption story** | implementation-report | A deployment in use, with outcomes over time. |

## How to submit

1. Copy the relevant template into `evidence/reports/` as `YYYY-MM-<org-or-pseudonym>-<short-name>.md`.
2. Fill it in. Link any related [research questions](../public-review/research-questions.md) (`RQ-` IDs) and issues.
3. Open a pull request. Maintainers will review for completeness (not for "favorable" findings), index it, and route any findings into the review process.

## Anonymity & sensitivity

Reports may use a pseudonymous organization name and omit proprietary detail. State clearly what has been generalized or withheld. We care about the findings, not attribution — though named reports carry more weight in the citation graph and are warmly credited.

## How evidence is used

- Indexed in a public **Implementations & Evidence** table (linked from the README).
- Findings that imply a change become [RFCs](../rfcs/README.md); the evidence is cited as the justification.
- Aggregate results update the status of the [open research questions](../public-review/research-questions.md).
- Evidence — not opinion — is the tie-breaker in normative decisions (`GOVERNANCE.md`).

## A note on negative results

We will never bury a failed pilot or an unfavorable benchmark. A framework that only publishes its wins is marketing, not engineering. If CROA is too costly, too hard to integrate, or wrong in some condition, the evidence record is exactly where that should become visible — early, in public, and on our own initiative.
