---
tags:
  - croa_foundation
---

# Appendix L — Governed Multi-Agent Delegation

**CROA Framework v1.0.1.1 · Normative (conditional).** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> *Normative scope. Multi-agent delegation is an **OPTIONAL** capability: a conforming deployment is not required to support it. This appendix is **normative for any deployment that does** — that is, any deployment in which one governed agent (an *orchestrator*) causes another governed agent (a *sub-agent*) to submit governed actions on its behalf. A deployment that performs no such delegation is unaffected by this appendix and remains conformant without it. Because the requirements here constrain only a capability that prior text did not address, and invalidate no system conformant to the prior text, this promotion from informative to conditional-normative is an **Additive (MINOR)** change under Part VII §31.3 — it neither relaxes nor strengthens any existing requirement.*

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The 


## L.1 The gap

CROA governs a single governed agent acting under a subject identity. Real systems increasingly use an **orchestrator** agent that decomposes a task and delegates sub-tasks to **sub-agents** (planner→workers, supervisor→tools-as-agents, agent calling agent over a protocol such as MCP or a message bus). Two questions arise that the single-agent model does not answer:

1. **Identity and attribution.** When sub-agent S executes a governed action on behalf of orchestrator O on behalf of human principal P, *whose* authority is exercised, and how is the chain recorded so that `C5` attribution (I3) and TH-6 (Identity Confusion) protection still hold?
2. **Scope propagation.** O is authorized for some action set; may S do anything O can do, or only a bounded subset? Uncontrolled propagation re-introduces the excessive-agency problem CROA exists to remove.

The safe answer preserves the core invariant: **delegation may only ever narrow reachability, never widen it** — the same monotonicity that governs RBAC and AQL admission (Part II §4.9). A deployment that supports delegation MUST preserve this property; an implementation in which a delegated scope can exceed the delegating subject's authorized scope does not conform to this appendix.

## L.2 Model: delegation as a scoped, governed sub-session

The model reuses existing primitives rather than inventing a parallel control plane. The five requirements **D1–D5** are normative for any deployment that implements delegation.

**D1 — Every agent is a subject; every hop is governed.** Each sub-agent MUST act under its own subject identity (Part I §2.2) and MUST submit its governed actions through the OCP exactly as a top-level agent does. There is no "trusted" intra-system channel: an action by S against a governed external system is a governed action, evaluated by `C2`, compiled by `C7`, enforced by `C6`. Agent-to-agent messages that do **not** touch a governed system are outside execution governance but remain a TH-9.C residual and MUST be network-constrained (P4) unless they too traverse a governed surface.

**D2 — The delegation chain is explicit and recorded.** A delegated governed action MUST carry a **delegation chain**: the ordered list of subject identities (for example `[P, O, S]`) with, for each hop, the authorizing subject, the delegated scope, and a signed delegation token. The chain MUST be recorded in `C5` for every delegated action, in the `event.delegation_chain` field, so that attribution is to the full chain, not to S alone. This is the multi-hop generalization of subject-identity propagation (TH-6.C) and closes the "who really acted" gap.

**D3 — Inherited scope is bounded and monotone.** A delegation token issued by O to S MUST grant a scope that is a **subset** of O's own currently-authorized scope (the intersection of O's RBAC eligibility §4.9.1 with any active ECC/exception scope). Formally, `scope(S) ⊆ scope(O) ⊆ scope(P)`. The OCP MUST admit an action by S only if it is within `scope(S)` **and** independently passes `C2.eval` against policy and invariants. Delegation MUST NOT grant S an action that O could not perform, and MUST NOT bypass invariant evaluation — it may only *restrict*. A token that purports to widen scope is invalid and MUST fail-deny.

For purposes of D3, `scope` is not free text. A delegating deployment MUST represent delegated scope in the canonical Appendix L scope profile, with these minimum fields:

- `scope.subject_id` — the subject to whom the delegated scope applies.
- `scope.action_classes` — the governed action classes the subject may request.
- `scope.targets` — canonical target identifiers resolved against the Federated Context Registry (`C3`); aliases and local names are not sufficient.
- `scope.parameter_constraints` — the parameter predicate, expressed in the deterministic constraint profile declared by `C1`.
- `scope.validity_window` — the token's not-before and not-after bounds.
- `scope.invariant_context` — the policy artifact, invariant-set version, and scope-profile version against which the scope was issued.

Before admitting a delegated action, the OCP MUST canonicalize the presented scope by sorting and deduplicating sets, resolving targets to Federated Context Registry identifiers, binding the parameter predicate to the declared `C1` constraint profile, and binding the policy/invariant versions. `scope(A) ⊆ scope(B)` is true only if: (1) `action_classes(A) ⊆ action_classes(B)`; (2) `targets(A) ⊆ targets(B)` after canonical resolution; (3) `parameter_constraints(A)` logically implies `parameter_constraints(B)` under the declared deterministic constraint profile; (4) `validity_window(A)` is wholly contained within `validity_window(B)`; and (5) `invariant_context(A)` is the same as, or a governed narrowing of, `invariant_context(B)`. If the OCP cannot canonicalize a field, cannot prove predicate implication, sees incomparable policy models, or sees a stale/widened invariant context, the subset relation is not established and the delegation MUST fail-deny. Heterogeneous agent systems MAY use different native policy languages internally, but the token submitted to CROA MUST be mapped into this canonical profile; absent such a mapping, delegated execution is unsupported and MUST NOT be presented as Appendix L conformant.

**D4 — Delegation is time- and depth-bounded.** A delegation token MUST be scoped, signed, and bounded: it MUST carry an expiry, a maximum delegation depth (to prevent unbounded chains), and a session linkage so that `C4` trajectory analysis treats the orchestrated work as a coherent unit. A token presented after its expiry, or a delegation that would exceed the maximum depth, MUST fail-deny. Sub-sessions MUST inherit the parent session's trajectory context for path-composition detection (TH-7) across the chain, so that a violation cannot be assembled by spreading steps across sub-agents. **Revocation and termination propagate downward.** Expiry and depth bound a token's lifetime, but they are not the only way authority ends: invalidation, termination, or scope-narrowing of a parent session's authorization (the principal's, or an intermediate orchestrator's) MUST immediately invalidate every delegation token and sub-session derived from it, regardless of any remaining expiry. A sub-agent MUST NOT continue to act under authority that its delegating subject no longer holds; the OCP MUST fail-deny any action presented under a token whose authorizing chain has been revoked or whose parent session has terminated. Without this rule, a revoked orchestrator's sub-agents could keep acting until their tokens lapsed — an authorization-escape window.

**D5 — Qualification propagates by configuration, not by trust.** Where sub-agents are agent subjects exercising autonomous authority, each MUST be independently subject to the AQL (§4.9.2) for the action classes it actually performs; O's qualification does not qualify S. The configuration fingerprint of each sub-agent is part of its own qualification.

## L.3 How it maps to the threat model

| Concern | Existing class | How the model addresses it |
|---|---|---|
| Sub-agent executes beyond delegated authority | TH-3, excessive agency | D1/D3: every hop is governed; inherited scope is a strict subset and is re-evaluated by `C2` |
| "Who acted" is ambiguous across hops | TH-6 (Identity Confusion) | D2: full signed delegation chain recorded in `C5` |
| Violation assembled across sub-agents | TH-7 (Path Composition) | D4: shared trajectory context across the chain |
| Revoked orchestrator's sub-agents keep acting until tokens expire | TH-3, excessive agency | D4: revocation/termination of a parent's authorization immediately invalidates all child tokens and sub-sessions |
| Out-of-band agent-to-agent channel | TH-9.C (Sidechannel) | D1: only governed-surface actions are covered; off-surface channels remain a declared residual and MUST be network-constrained (P4) |
| Silent model swap in a sub-agent | TH-8 / TH-2 | D5: per-sub-agent AQL and configuration fingerprint |

## L.4 Schema, fields, and negative tests

This section specifies the machine-readable surface and the conformance tests for delegation. The fields are **OPTIONAL** at the schema level (a non-delegating deployment emits none); where delegation is implemented, they are **REQUIRED** as stated, so the addition is backward-compatible (Part VII §31.3, MINOR).

**Delegation-token fields (`gga.delegation.*`).** A delegated grounded governed action MUST carry a `gga.delegation` object with at least: the authorizing subject (`gga.delegation.authorizing_subject`), the delegated scope (`gga.delegation.scope`, using the canonical D3 scope profile), the token expiry (`gga.delegation.expires_at`), the maximum delegation depth (`gga.delegation.max_depth`) and the current depth (`gga.delegation.depth`), the parent-session linkage (`gga.delegation.parent_session_id`), and the issuing subject's signature over the token (`gga.delegation.signature`). The field family is reserved in the `gga.*` namespace (Appendix B); its JSON Schema companion is `gga.schema.json`.

**Delegation-chain record (`event.delegation_chain`).** Every `C5` event recording a delegated action MUST populate `event.delegation_chain` as the ordered array of hops, each hop carrying the hop's subject, its authorizing subject, the delegated scope in the canonical D3 scope profile, and the delegation-token signature. The field is absent on non-delegated actions. Its JSON Schema companion is `event.schema.json`.

**Why the request carries one hop while `C5` carries the whole chain (inductive verification).** The two field shapes are deliberate and are *not* an inconsistency: the request-time `gga.delegation` object describes a single immediate hop (O→S, or P→O), whereas `event.delegation_chain` is the ordered array of all hops. Delegation is verified **inductively**, not by replaying the entire chain on every request. D3 already requires each hop's scope to be a subset of the authorizing subject's *currently-authorized* scope, and that subject's own scope was itself narrowed-and-bound when it was admitted. By induction, `scope(S) ⊆ scope(O) ⊆ scope(P)` holds without S re-presenting the upstream P→O or O→S tokens; transitive monotonicity is preserved from per-session scope state held by the OCP/`C4`, not from a stateful `C5` read. The full ordered chain is therefore not needed in the request, but it is preserved in `C5` (D2) for attribution (I3, TH-6) — the correct place for it. Implementations MUST NOT assume that chain-replay in the request is required for sound verification.

**Negative tests (REQUIRED where delegation is implemented).** A deployment that implements delegation MUST include, and pass, the following delegation-specific negative tests, recorded in the Conformance Evidence Record alongside the §27.3 threat-class minimums (Part VI §29.3):

- **Scope widening** — a delegation token whose `gga.delegation.scope` exceeds the delegating subject's authorized scope MUST be rejected fail-deny (no ECC compiled) and recorded in `C5`.
- **Incomparable or non-canonical scope** — a delegation token whose scope cannot be canonicalized or compared under the declared Appendix L scope profile (including target aliases not resolved by the Federated Context Registry, parameter predicates in an undeclared profile, parameter constraints that widen the delegating subject's predicate, or policy/invariant-version mismatch) MUST fail-deny.
- **Chain forgery** — a delegated action whose `gga.delegation.signature` does not verify against the authorizing subject, or whose `event.delegation_chain` is inconsistent with the presented token, MUST fail-deny.
- **Depth / expiry breach** — a delegation exceeding `gga.delegation.max_depth`, or a token presented after `gga.delegation.expires_at`, MUST fail-deny.
- **Revocation propagation** — after a parent session's authorization is revoked, terminated, or narrowed, any subsequent action presented under a child token derived from it (including a token not yet expired) MUST fail-deny and be recorded in `C5`.
- **Cross-agent trajectory** — a violating sequence assembled across sub-agents within one orchestrated session MUST raise `TRAJECTORY_ALERT` (TH-7) and DENY the next step, exactly as for a single agent.

---

**Summary of Normative Content (recap — skippable on a first linear read) — Appendix L (conditional: applies where multi-agent delegation is implemented)**

- §L.1 / D3: Delegation MUST preserve monotone reachability — `scope(S) ⊆ scope(O) ⊆ scope(P)` — using the canonical Appendix L scope profile; a token that widens scope, cannot be canonicalized, or cannot be compared MUST fail-deny.
- D1: Every agent in a delegation chain MUST act under its own subject identity and submit governed actions through the OCP; no intra-system channel is trusted; off-surface agent-to-agent channels MUST be network-constrained (P4).
- D2: Every delegated action MUST carry a delegation chain recorded in `C5` (`event.delegation_chain`), attributing the action to the full chain.
- D3: A delegated action MUST be within the delegated scope **and** independently pass `C2.eval`; delegation MUST NOT bypass invariant evaluation.
- D4: A delegation token MUST be signed and carry an expiry and a maximum depth; expiry or depth breach MUST fail-deny; sub-sessions MUST inherit the parent trajectory context (TH-7); and revocation, termination, or scope-narrowing of a parent session's authorization MUST immediately invalidate all child tokens and sub-sessions derived from it, regardless of remaining expiry.
- D5: Each autonomous sub-agent MUST be independently AQL-qualified (§4.9.2) for the action classes it performs.
- §L.4: A delegated grounded governed action MUST carry the `gga.delegation.*` fields; a delegating deployment MUST include and pass the scope-widening, incomparable/non-canonical-scope, chain-forgery, depth/expiry, revocation-propagation, and cross-agent-trajectory negative tests. Verification is inductive: the request carries the immediate hop while `C5` retains the full chain for attribution; chain-replay in the request is not required.

---

## Appendix L Conformance Requirements

These requirements are **conditional**: they apply to, and only to, a deployment that implements multi-agent delegation. Such a deployment satisfies Appendix L if and only if an independent assessor can verify, from the Conformance Evidence Record and `C5` (Part VI §29):

**Delegation monotonicity.** No delegated action was admitted with a scope exceeding its delegating subject's authorized scope; scope-widening and incomparable/non-canonical-scope attempts fail-deny. Verifiable by: the scope-widening and incomparable/non-canonical-scope negative tests and `C5` extracts.

**Delegation attribution.** Every delegated action in `C5` carries a complete, signature-verifiable `event.delegation_chain`. Verifiable by: `C5` inspection and the chain-forgery negative test.

**Delegation bounding.** Depth and expiry breaches fail-deny; revocation, termination, or scope-narrowing of a parent session immediately invalidates derived child tokens and sub-sessions; cross-agent violating sequences raise `TRAJECTORY_ALERT` and DENY. Verifiable by: the depth/expiry, revocation-propagation, and cross-agent-trajectory negative tests.

A deployment that performs no delegation is conformant with Part VI without these criteria; they neither add to nor relax the Part VI conformance levels for non-delegating deployments (Part VII §31.3, MINOR).

---

*End of Appendix L — Governed Multi-Agent Delegation.*
