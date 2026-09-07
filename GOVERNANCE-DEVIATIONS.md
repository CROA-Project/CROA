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

## D-03 — The elevated review tier is unsatisfiable for a project this size

**Not a deviation. A rule the project cannot obey**, found within an hour of making the rule
enforceable — which is the entire argument for making rules enforceable.

**Rule.** `.github/workflows/review-tier.yml` requires **two approvals** on elevated surfaces
(`spec/`, `rfcs/`, `.github/`, `GOVERNANCE.md`, and the licence and citation files), and excludes the
author from the count:

```js
.filter(([login, state]) => state === 'APPROVED' && login !== pr.user.login)
```

**What happened.** [PR #4](https://github.com/CROA-Project/CROA/pull/4) — the first change made after
direct pushes to `main` were disabled — touched `rfcs/`. The project has two maintainers. With the
author excluded, one possible approver remains. **Two approvals cannot be obtained. The pull request
was structurally unmergeable**, not merely waiting.

This was written on the assumption of a larger team, and nothing revealed it for as long as nothing
enforced it. Between 29 August and 2 September the rule existed and was ignored; the moment it was
enforced, it turned out to be impossible. Both facts are about the same underlying problem: an
unenforced requirement is not a requirement, and it is not tested either.

**What was done.** PR #4 was reduced to this file alone, which is not an elevated surface, so the
standard tier applies and one approval unblocks it. The rule itself is corrected separately — and
that correction touches `.github/`, so it is subject to the very rule it fixes. Any bypass used to
land it will be recorded here as its own entry, with the reason.

**What remains open.** The corrected rule will require *two approvals, or every eligible reviewer
when the project has fewer than three maintainers*. That is weaker than two eyes beyond the author,
and it should be stated on every pull request rather than buried: a two-person project cannot have
four-eyes review, and pretending otherwise is worse than admitting it. If the project grows, the rule
tightens on its own.

## D-04 — Four pull requests merged past the elevated review tier, and one merged into the wrong branch

**Rule.** `.github/workflows/review-tier.yml` requires **two approvals** on `spec/`, `rfcs/`,
`.github/`, `GOVERNANCE.md` and the licence and citation files, and it is a **required** status check
on `main`.

**What happened.** Between 6 and 7 September 2026, four pull requests carrying the v1.0.1 work —
[#6](https://github.com/CROA-Project/CROA/pull/6) (corpus and repairs),
[#7](https://github.com/CROA-Project/CROA/pull/7) (RFC 0003),
[#8](https://github.com/CROA-Project/CROA/pull/8) and
[#9](https://github.com/CROA-Project/CROA/pull/9) (the normative surface) — each touched `spec/` or
`rfcs/`. Each was merged through **Merge without waiting for requirements to be met**, with
`Review tier` red and **zero approvals** on all four.

**This is D-03, recurring — which is the part worth reading.** The project has two maintainers, and
the workflow excludes the author from the approval count. One possible approver remains against two
required. All four pull requests were **structurally unmergeable**, exactly as D-03 described on
2 September. The bypass was not a shortcut past a satisfiable rule; it was the only path.

D-03 ended with a commitment: the rule would be corrected to require *two approvals, or every
eligible reviewer when the project has fewer than three maintainers*. That correction was opened as
[PR #5](https://github.com/CROA-Project/CROA/pull/5) and **closed without merging**.
`REQUIRED_APPROVALS = 2` is still what `main` carries. Five days passed between recording the problem
and needing the fix, and the fix did not land.

So the honest reading is not that four merges were careless. It is that **an impossible rule stayed
on `main` for five days after the project documented that it was impossible**, and the next four
changes had to step around it. A required check that must be bypassed to ship anything is not
enforcement; it is a ritual with an override, and the override is where the real policy lives.

**A second, different deviation, in the same batch.** PR #8's base branch was
`spec/v1.0.1-editorial`, not `main`. It was merged — into that branch. GitHub reported it merged and
closed, and `main` did not contain it. For a period on 7 September, `main` therefore carried **RFC
0003 accepted with no implementation**: a repository that had authorised a normative change it did
not contain, while every status on every pull request was green.

No rule was broken there. That is the point: **nothing checks that a merged change reached `main`.**
It was caught by reading `main`'s tree file by file, not by any control, and repaired by PR #9. A
project whose central argument is that governance must be mechanical rather than declarative had a
merge report success while the artifact was absent, and had no mechanism that would ever have said
so.

**What was done.** Both are recorded here, unbackdated, and neither is claimed compliant. PR #9 put
the normative surface on `main`.

**What remains open.**

1. **Land the review-tier correction.** Until `REQUIRED_APPROVALS` accounts for a two-person project,
   every elevated pull request needs a bypass, and this register becomes a log rather than an
   exception list. That correction touches `.github/`, so it is subject to the rule it fixes; the
   bypass used to land it gets its own entry, with the reason — as D-03 already said it would.
2. **Add a check that a normative pull request lands where it claims to.** A merge whose base is not
   `main` should say so on the pull request in a way that is hard to miss, or the merge should be
   gated on the base being the default branch unless the stack is declared. This is a small piece of
   automation and it is the second time the project has learned the same lesson: the gap was not the
   judgement, it was that nothing mechanical was watching.
3. **Do not let a bypass become routine.** Four in two days is how a control stops being a control.
   If the fix in (1) is not landed before the next elevated change, the correct response is to stop
   merging, not to add a fifth entry here.

---

## Structural gaps that made deviation easy

The entries above were possible because nothing structural prevented them. On **2 September 2026**
three of the six gaps were closed. The remaining three are listed as open, because a register that
claims more than it has done is worth nothing.

| Gap | State |
|---|---|
| No status check is **required** to merge | **Closed.** `dco` and `Review tier` are required status checks on `main`. Deliberately *not* required: `lint` and `links`, which only run when a pull request touches a `.md` file — requiring them would leave any code-only pull request permanently pending. Making them unconditional, and then required, is the next step. |
| Administrators hold a **permanent bypass** of the ruleset | **Closed.** The repository-admin bypass moved from *Always allow* to *Allow for pull requests only*. Direct pushes to `main` are refused for everyone, maintainers included. A bypass still exists inside a pull request, but it is prompted and visible rather than silent. |
| The reference harness repository has **no ruleset, no CI, and no release** | **Partly closed.** CI runs the full suite on every push and pull request, across Python 3.8–3.13, repeats the two concurrency races 25 times, and since 7 September also runs an 8-process compare-and-swap race and the event-schema conformance job. The harness repository still has **no ruleset and no tagged release** — so its `main` is protected by nothing, which is the same shape of gap as D-04. |
| Approvals are counted, not attributed to owners of the touched surface | **Open**, and now known to be worse than described: the two-approval rule is unsatisfiable at this team size (**D-03**). GitHub also still cannot require that an approval come from an owner of the paths a pull request touches. |
| GitHub Actions are referenced by **mutable major tags**, not commit SHAs | **Open.** A compromised or retagged action would change what CI does. Marked as a `TODO` in the harness workflow. |
| CI does not validate the JSON schemas, nor any artifact against them | **Partly closed, 7 September 2026.** `schema validation / validate` checks the four schemas against draft 2020-12 and against the namespace contract on every pull request here; `schema-conformance` in the harness repository validates **every emitted event** against `event.schema.json`, checked out from this repository, and fails the build on drift. **Still open:** nothing validates an **ECC**, and the ECC does not in fact conform — see [`spec/known-defects-harness.md`](spec/known-defects-harness.md) H-03 for the exact list. |

The first two were also acknowledged in [`.github/REVIEW_AND_MERGE.md`](.github/REVIEW_AND_MERGE.md),
which now understates the enforcement and should be updated.

What remains, to make the process structural rather than declarative:

1. Make `lint` and `links` run on every pull request, then require them too.
2. Add a ruleset and a tagged release to the harness repository.
3. Pin every action to a commit SHA.
4. Validate the schemas, and the harness's output against them, in CI. *(Done for events on
   7 September 2026; the ECC is still unvalidated and non-conformant.)*
5. Replace the pull-request bypass with a time-boxed, two-person, logged emergency path — GitHub does
   not offer this natively, so it needs a convention and a record rather than a setting.
6. Correct `REQUIRED_APPROVALS` so the elevated tier is satisfiable at this team size — **D-03**
   promised this on 2 September, [PR #5](https://github.com/CROA-Project/CROA/pull/5) was closed
   without merging, and **D-04** is what that cost. This is now the first of these to do: until it
   lands, every elevated pull request needs a bypass.
7. Gate or flag a pull request whose base is not the default branch, so a merge cannot report success
   while `main` does not contain the change (**D-04**).

**A note on what this cost.** Closing the first two gaps means the maintainers can no longer push
directly to `main`. Every change now needs a branch, a pull request, and green checks — including this
file. That is the point: a constraint that its authors can step around is not a constraint.

**And what it bought, immediately.** The first pull request to travel the new path failed, for a
reason nobody had noticed in the four days the rule had existed: it demanded more approvals than the
project has people. That is recorded as **D-03**. A rule that is never enforced is never tested
either, and this one was wrong the whole time.

---

## How to report a deviation

If you find a case where the project did not follow its own rules, open an issue. A deviation found
by someone outside the project and recorded here is worth more to CROA's credibility than a clean
page would be.
