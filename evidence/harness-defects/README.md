# Harness defect reproduction — 2 September 2026

A runnable reproduction of three defects in the
[Minimal Reference Harness](https://github.com/CROA-Project/croa-reference-harness), described in
[`spec/known-defects-harness.md`](../../spec/known-defects-harness.md).

```bash
python3 reproduce.py
```

No dependencies, Python ≥ 3.8. It exits **1** while any defect reproduces, so it can be wired into CI
as a regression gate once the harness is fixed.

## What it establishes

| | |
|---|---|
| **H-01** | One exception authorization documented as single-use admitted **two** executions. `C5.verify()` returned `True` on the resulting log. |
| **H-02** | A commitment compiled for `subject-A` was admitted when presented as `subject-B`, and `C5` recorded `subject-B`. |
| **H-03** | `cc.id` mixes a random `uuid4()` into the digest, so two compilations of the identical action produce different identifiers. It is not the content address Part II §4.4.1 requires. |

## Provenance

The findings were first reported by an independent enterprise-architecture audit of the CROA
repositories dated **2 September 2026**. This script is the CROA Project's own reproduction of them,
written from the audit's description and run against the published harness code. **All three
reproduce.** Where the audit's account and this script differ, this script is the one you can run.

## Why the code is copied rather than imported

`reproduce.py` copies `AuditStore`, the C1–C7 mocks and `Harness.present` verbatim from
`croa-reference-harness@main`. That makes the file runnable with no clone and puts the code under
test next to the assertions about it — but it will drift as the harness changes. When the harness is
fixed, these become tests inside the harness repository, and this directory keeps only the dated
record of what was reproduced before the fix.

## What it does *not* establish

It says nothing about the CROA specification. H-01 in particular is a defect the specification
already forbids: Part II §4.8 requires redemption to be a single atomic linearizable compare-and-swap,
and the harness performs a check-then-act instead. The demonstrator does not implement what the
document it demonstrates requires.

It is also **author-run**. It fills the *adversarial testing* bucket in
[`../README.md`](../README.md) with a first entry, and no more than that: an adversarial test written
by the project against its own artifact is weaker evidence than one written by someone else. What
would be worth more is a reader who makes this script fail to reproduce, or who finds a fourth defect
it misses.
