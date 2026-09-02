# Harness defect reproduction — 2 September 2026

A frozen, runnable reproduction of three defects in the
[Minimal Reference Harness](https://github.com/CROA-Project/croa-reference-harness) **as they stood
before the fix**. Their current status is in
[`spec/known-defects-harness.md`](../../spec/known-defects-harness.md).

```bash
python3 reproduce.py
```

No dependencies, Python ≥ 3.8. It exits 1, always — see *A correction* below.

## What it establishes

| | |
|---|---|
| **H-01** | One exception authorization documented as single-use admitted **two** executions. `C5.verify()` returned `True` on the resulting log. |
| **H-02** | A commitment compiled for `subject-A` was admitted when presented as `subject-B`, and `C5` recorded `subject-B`. |
| **H-03** | `cc.id` mixed a random `uuid4()` into the digest, so two compilations of the identical action produced different identifiers. It was not the content address Part II §4.4.1 requires. |

## Provenance

The findings were first reported by an independent enterprise-architecture audit of the CROA
repositories dated **2 September 2026**. This script is the CROA Project's own reproduction of them,
written from the audit's description and run against the harness code as published. All three
reproduced. **All three, and H-04, have since been fixed** — see the register.

## A correction

When this directory was first published, this page called the script *"a regression gate once the
defects are fixed"*. **That was wrong.** The script copies the harness's classes rather than
importing them, so it tests the copy: it will report the defects for ever, whatever the real harness
does. A gate that cannot fail is not a gate, and describing it as one was exactly the kind of
unearned claim this repository is supposed to catch.

What the file is good for is the opposite property — it is *frozen*. Anyone can still see the defects
that were fixed, without archaeology through git history, which is what an evidence record should
offer.

**The regression gate is the harness's own test suite.** `TestAdversarial` in
`croa-reference-harness/tests/test_mrh.py` contains the h01/h02/h03/h04 cases and two 100-thread
races, and it runs against the real code:

```bash
git clone https://github.com/CROA-Project/croa-reference-harness.git
cd croa-reference-harness && make test
```

## What this does *not* establish

It says nothing about the CROA specification. H-01 in particular was a defect the specification
already forbade: Part II §4.8 requires redemption to be a single atomic linearizable compare-and-swap,
and the harness performed a check-then-act. The demonstrator did not implement what the document it
demonstrates requires.

It is also **author-run**. It fills the *adversarial testing* bucket in [`../README.md`](../README.md)
with a first entry, and no more than that: an adversarial test written by the project against its own
artifact is weaker evidence than one written by someone else. What would be worth more is a reader
who finds a fourth defect — the open ones are listed in the register, and H-06 (no network boundary,
so property P4 is untested) is the largest.
