---
rfc: 0001
title: Invariant I8 — Authority Non-Expansion, and reference negative test NT-008
status: accepted
change_level: extension
authors: [Yasmine Durand, Darrin Smith]
created: 2026-08-29
affects: [Part II §5.9 (new), Part VI §29.3, Appendix Q (NT-008), spec/properties.md P-B, spec/errata-v1.0.md E-02 and E-12]
tracking_issue: (none — see "Process note" below)
---

# RFC 0001 — Authority Non-Expansion (I8) and NT-008

> **Process note, stated first because it matters.** This RFC was written **after** the change it
> describes was merged, during the pre-public-communication audit of August 2026 and before the
> repository had any outside participants. It did not go through the fourteen-day Final Comment
> Period the [RFC process](../README.md) requires. It is recorded here so that the repository's
> normative history is complete and so that the first substantive change to CROA is not the one
> change with no RFC behind it. **Anyone who wishes to reopen it should**: the change is additive and
> reversible, and an argument that I8 is wrong, redundant, or wrongly bounded is exactly the kind of
> contribution this repository is asking for. Every subsequent normative change follows the process
> as written.

## Summary

CROA v1.0 already forbade, in four separate places, the various ways one subject's authority might be
made to serve another's action. It never composed those pointwise rules into a single named property,
never stated the bound on a composition's reachable operations, and had no reference test for any of
it. This RFC names the property as **invariant I8 — Authority Non-Expansion**, states it in two
clauses, and adds **NT-008** as its falsifying test. No component, artifact, or mechanism is
introduced, and no existing requirement changes.

## Motivation

The audit asked a question v1.0 could not answer from its own text: *if agent A may read customer
records and agent B may send external email, what bounds the set of operations reachable through a
composition of A and B?*

The rules that answer it were all present — the §4.9.1 admission predicate, tenet T6 (stated intent,
asserted approval and cited authority are not inputs to a decision), `C7`'s prohibition on widening an
exception scope (§4.4.3), the monotone execution surface (§6.2), the delegation rules of Appendix L,
and the prohibition on cross-agent and cross-domain CC redemption (Part IV §21.3, §20.6) — but a
reader had to assemble them, and a reviewer had no single statement to attack. An unstated property
is not a falsifiable one.

There is no external evidence prompting this change; it came from internal review. What would settle
whether it is correctly bounded is an arrangement that admits an operation no participant was
independently authorized to submit. NT-008 exists to look for one.

## Change level and impact

**Extension**, additive.

- **Requirements added:** Part II §5.9 (I8, two clauses); Appendix Q NT-008; three checks in Part VI §29.3.
- **Requirements changed:** none. I8 is entailed by rules already normative in v1.0; a deployment that
  conformed to v1.0 conforms to I8 without modification.
- **Backward compatibility:** preserved. No schema changes. No component gains a responsibility.
- **Migration path:** none required. An assessor targeting the next version runs NT-008 in addition to
  NT-001–NT-007.

## Detailed design

**I8 — Authority Non-Expansion.**

**(a) Delegation attenuates.** Along any delegation chain, authority MUST be non-increasing from the
authorizing subject: `scope(S) ⊆ scope(O) ⊆ … ⊆ scope(P)` for every hop, with independent `C2`
evaluation at each hop (Appendix L D1) and the canonical subset test failing deny wherever the
relation cannot be established (Appendix L D3).

**(b) No authority laundering.** A governed action MUST be admitted only if it is independently
authorized for the subject that submits it. It follows that the operations reachable through a
composition of subjects are the **union** of the participants' individually authorized sets — never a
superset.

**On the union.** An earlier draft of this change bounded a composition by its *least-authorized*
participant. That was wrong: it would have made every delegation a violation of the property it was
meant to express, and it was strictly stronger than the clauses it claimed to follow from. The error
and its correction are recorded in [`spec/errata-v1.0.md`](../../spec/errata-v1.0.md) E-12 rather than
quietly dropped, because how a normative claim was gotten wrong is part of what a reviewer needs.

**NT-008** has two parts. **Part A** begins with a non-vacuous control case that MUST be admitted,
then widens on each dimension of scope — action class, target, parameter constraint, validity window,
delegation depth — each of which MUST fail deny with no commitment compiled. **Part B** runs four
laundering arrangements in which one subject attempts to submit under another's authority (citing the
other's session; citing its permit; citing its commitment; presenting its commitment at the boundary),
each of which MUST fail deny; it closes with a record inspection requiring every executed operation to
be attributable, **from `C5` alone**, to an independent authorization held by its own submitting
subject.

The property in full — claim, preconditions, invariant, enforcement, falsifying test, evidence
produced, and what it does *not* establish — is **P-B** in [`spec/properties.md`](../../spec/properties.md).

## Alternatives considered

**Do nothing.** v1.0's pointwise rules already forbid the arrangements NT-008 tests, so nothing was
*unsafe*. Rejected because an unnamed property cannot be attacked, and because the composition
question is the first one a serious reviewer asks.

**State it as a theorem.** Rejected: CROA has no formal model in which "theorem" would mean anything,
and calling an argued entailment a theorem would be exactly the kind of overclaim the audit was
looking for.

**Bound the composition by the least-authorized participant.** Rejected as wrong — see above.

**Extend the property across arbitrary distinct subject identities.** Rejected: CROA cannot bound the
*joint effect* of two subjects each acting within authority. That is the trajectory problem, and
outside a single delegation chain it remains a declared residual rather than a covered case.

## Risks and drawbacks

- **It may read as stronger than it is.** I8 bounds the *union*; it does not make the union safe. Two
  subjects each acting within authority can still produce a jointly harmful outcome. P-B says so
  explicitly, and that sentence has to survive every future edit.
- **It is only as strong as the identity beneath it.** Agent identity is an external prerequisite CROA
  consumes and does not provide (see [`docs/prerequisites.md`](../../docs/prerequisites.md)). Where
  identity is weak, I8 is weak.
- **The test is not implemented anywhere.** NT-008 needs a delegation model; the Minimal Reference
  Harness has none, so the test is specified and unexercised. That gap is stated in
  [`spec/identifiers.md`](../../spec/identifiers.md) and is a good contribution.
- **Assessment cost rises.** One more mandatory test at L4.

## Open questions

1. Is clause (b)'s entailment from §4.9.1 + T6 + §4.4.3 + §6.2 actually tight, or is there an
   arrangement those four rules permit? **This is the question we most want attacked.**
2. Should the union bound be stated over *effective authority* or over nominal permission where the
   two diverge under enforced controls?
3. Does I8 need a companion clause for authority acquired through a governed system's own downstream
   credentials — i.e., authority CROA does not mediate?

## Prior art

The permission/authority distinction and attenuation under creation are Miller, *Robust Composition*
(2006) and Shapiro & Weber (IEEE S&P 2000); the schematic protection model is Sandhu (JACM 35(2),
1988); one-way attenuating credentials are Macaroons (NDSS 2014), SPKI/SDSI, and RFC 8693. In
contemporary work, AgentBound's "no authority can implicitly expand the perimeter established by
another" (arXiv:2606.30970) is the same intuition, and *The Vulnerability With No CVE*
(arXiv:2608.05884) gives the cleanest available statement of effective authority. **CROA claims no
novelty for the idea**; what this RFC adds is its application to agent delegation as a registered,
testable invariant. See [`docs/prior-art.md`](../../docs/prior-art.md) §2.1.
