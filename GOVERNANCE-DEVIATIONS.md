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

## Structural gaps that made deviation easy

Both entries above were possible because nothing structural prevented them. On **2 September 2026**
three of the six gaps were closed. The remaining three are listed as open, because a register that
claims more than it has done is worth nothing.

| Gap | State |
|---|---|
| No status check is **required** to merge | **Closed.** `dco` and `Review tier` are required status checks on `main`. Deliberately *not* required: `lint` and `links`, which only run when a pull request touches a `.md` file — requiring them would leave any code-only pull request permanently pending. Making them unconditional, and then required, is the next step. |
| Administrators hold a **permanent bypass** of the ruleset | **Closed.** The repository-admin bypass moved from *Always allow* to *Allow for pull requests only*. Direct pushes to `main` are refused for everyone, maintainers included. A bypass still exists inside a pull request, but it is prompted and visible rather than silent. |
| The reference harness repository has **no ruleset, no CI, and no release** | **Partly closed.** CI now runs the full suite on every push, across Python 3.8–3.13, and repeats the two concurrency races 25 times. The harness repository still has **no ruleset and no tagged release**. |
| Approvals are counted, not attributed to owners of the touched surface | **Open.** `Review tier` enforces two approvals on elevated surfaces, but GitHub still cannot require that an approval come from an owner of the paths a pull request touches. |
| GitHub Actions are referenced by **mutable major tags**, not commit SHAs | **Open.** A compromised or retagged action would change what CI does. Marked as a `TODO` in the harness workflow. |
| CI does not validate the JSON schemas, nor any artifact against them | **Open.** Schema drift is invisible — see [`spec/known-defects-harness.md`](spec/known-defects-harness.md) H-03, whose remaining half is exactly this. |

The first two were also acknowledged in [`.github/REVIEW_AND_MERGE.md`](.github/REVIEW_AND_MERGE.md),
which now understates the enforcement and should be updated.

What remains, to make the process structural rather than declarative:

1. Make `lint` and `links` run on every pull request, then require them too.
2. Add a ruleset and a tagged release to the harness repository.
3. Pin every action to a commit SHA.
4. Validate the schemas, and the harness's output against them, in CI.
5. Replace the pull-request bypass with a time-boxed, two-person, logged emergency path — GitHub does
   not offer this natively, so it needs a convention and a record rather than a setting.

**A note on what this cost.** Closing the first two gaps means the maintainers can no longer push
directly to `main`. Every change now needs a branch, a pull request, and green checks — including this
file. That is the point: a constraint that its authors can step around is not a constraint. This
entry is the first change to go through the new path.

---

## How to report a deviation

If you find a case where the project did not follow its own rules, open an issue. A deviation found
by someone outside the project and recorded here is worth more to CROA's credibility than a clean
page would be.
