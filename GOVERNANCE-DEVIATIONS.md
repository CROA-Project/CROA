# Governance deviations

CROA's argument is that an important requirement should be structurally hard to bypass. This page
records the occasions on which the project did not apply that argument to itself.

It exists because the alternative — quietly following the process from now on and saying nothing —
would be the governance equivalent of the failure mode CROA is named after: satisfying the objective
while stepping around the constraint.

**Nothing here is backdated.** No comment period is simulated after the fact, and no deviation is
retroactively declared compliant. Each entry states what the rule required, what happened, and what
was done about it.

---

## D-01 — PR #2 merged as a normative change with no RFC and no Final Comment Period

**Rule.** [`GOVERNANCE.md`](GOVERNANCE.md) and the [RFC process](rfcs/README.md) require an RFC and a
Final Comment Period of at least **14 days** for any normative, schema, conformance or claim change.

**What happened.** [PR #2](https://github.com/CROA-Project/CROA/pull/2), explicitly classified
*normative-correction · extension*, was opened and merged on **29 August 2026 within roughly fourteen
minutes**, with no review and no comment period. It added invariant **I8**, reference negative test
**NT-008**, a per-accumulation-key serialisation requirement (Part II §4.6.3), and the first thirteen
errata.

**Mitigating context, not a justification.** The repository was private at the time and had no
outside participants, so no comment period could have received a comment. That explains the decision;
it does not make it compliant, and the rule as written admits no such exception.

**What was done.** [RFC 0001](rfcs/text/0001-authority-non-expansion.md) was written **after** the
merge and says so in its first paragraph. It documents I8 and NT-008 so the normative history is
complete, and invites anyone to reopen the question — the change is additive and reversible.

**What remains open.** The serialisation requirement and the errata are not covered by an RFC. If
review produces an objection to any of them, it is handled as a normal change, not defended on the
grounds that it already shipped.

## D-02 — PR #1 changed governance itself with no RFC and no 21-day period

**Rule.** Changing `GOVERNANCE.md` requires an RFC and a Final Comment Period of at least **21 days**.

**What happened.** [PR #1](https://github.com/CROA-Project/CROA/pull/1) modified `GOVERNANCE.md` and
the project's authority structure, and was merged after roughly three days without an RFC.

**What was done.** Recorded here. No retroactive ratification is claimed.

**What remains open.** The next change to `GOVERNANCE.md` follows the 21-day rule, and this entry is
the baseline against which that is checked.

---

## Structural gaps that make deviation easy

These are open, and they are the reason the entries above were possible.

| Gap | State |
|---|---|
| No status check is **required** to merge | Workflows can be red and the merge still proceeds |
| Administrators hold a **permanent bypass** of the ruleset | The review tier is advisory, not a barrier |
| Approvals are counted, not attributed to owners of the touched surface | Two approvals from anyone satisfy the rule |
| The reference harness repository has **no ruleset, no CI, and no release** | Nothing gates it at all |
| GitHub Actions are referenced by **mutable major tags**, not commit SHAs | A compromised or retagged action changes what CI does |
| CI does not validate the JSON schemas, nor any artifact against them | Schema drift is invisible (see [`spec/known-defects-harness.md`](spec/known-defects-harness.md) H-03) |

The first two are also acknowledged in [`.github/REVIEW_AND_MERGE.md`](.github/REVIEW_AND_MERGE.md).

Closing them is what would make the process structural rather than declarative:

1. Require DCO, tests, lint, link-check, schema validation and `review-tier` as merge checks.
2. Replace the permanent administrator bypass with a time-boxed, two-person, logged emergency path.
3. Pin every action to a commit SHA.
4. Apply a ruleset and CI to the harness repository.

---

## How to report a deviation

If you find a case where the project did not follow its own rules, open an issue. A deviation found
by someone outside the project and recorded here is worth more to CROA's credibility than a clean
page would be.
