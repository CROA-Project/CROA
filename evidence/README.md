# Evidence

**Objective:** build a public, citable trail of what happens when people actually implement, benchmark, or assess CROA — successes and failures alike. Evidence is what eventually justifies (or refutes) CROA's claims; it is the currency of this project.

**Audience:** pilot implementers, benchmarkers, assessors, and researchers.

> A framework's credibility is the sum of its honest evidence. We index every report — including the ones that didn't work.

---

## Where CROA's evidence base actually stands

Before asking for evidence, here is what exists. Five of seven buckets are empty, and we would rather
say so than let a reader infer otherwise from the presence of a harness and a benchmark.

| Evidence type | Status |
|---|---|
| Author-controlled testing | **Present** — reference harness, CROA-Bench seed and mock adapters, the founding study. |
| Reproducible testing | **Partial** — both artifacts run deterministically on a clean machine, but what they reproduce is authored fixtures and mock behaviour, not system behaviour. |
| Adversarial testing | **Empty** |
| Independent replication | **Empty** |
| Multi-implementation validation | **Empty** |
| Multi-domain validation | **Empty** |
| Enterprise / production validation | **Empty** |

Detail, including what the founding study does and does not establish, is in
[`docs/limitations.md`](../docs/limitations.md) §4; the five experiments that would most change this
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
