# CROA Normative Properties — statement, enforcement, and falsification

**Objective:** state CROA's claim-bearing properties in a form an external reviewer can attack.
Each property below is given as **Claim → Preconditions → Invariant → Enforcement mechanism →
Counterexample / test → Evidence produced → What it does *not* establish.**

**Audience:** researchers, assessors, and implementers who want to know exactly what would falsify CROA.

**Authoritative source:** the specification (Parts I–VII, Appendices) at the DOI in
[`spec/README.md`](README.md). This page *restates* properties already normative there and adds no
requirement of its own except where a row is marked **(new in v1.1-draft)**. Where this page and the
specification differ, the specification governs.

---

## Why this page exists

A framework that says "unsafe paths are unreachable" and stops there is not falsifiable. The list
below is the set of things CROA asserts that could be shown to be false — by a counterexample, by a
failed test against a conformant deployment, or by an argument that the enforcement mechanism does
not entail the invariant.

Two rules govern this page:

1. **A property is listed only if CROA's normative text already entails it.** We do not name
   aspirations.
2. **A property is named for what it establishes, not for what it evokes.** Where CROA establishes
   a narrower property than a familiar name would suggest, the narrower name is used and the gap is
   stated. See P-D and P-E in particular.

Properties CROA does **not** claim — and which are therefore *not* on this list — are enumerated in
[§ Properties CROA does not have](#properties-croa-does-not-have) at the end. That section is part of
the specification's honesty obligation, not an afterthought.

---

## P-A — Complete Execution Mediation

| | |
|---|---|
| **Claim** | Every operation that takes effect on a governed system is the authorized execution content of a valid, unexpired, unredeemed Compiled Commitment produced by `C7`. |
| **Preconditions** | The operation targets a system inside the declared governance boundary; the execution boundary (TB-3) is enforced at the network layer (property P4); `C6` is reachable and the redemption authority is available (otherwise fail-deny applies). |
| **Invariant** | I1 (Reachability), realized at the boundary by the execution surface `ES(t)` of Part II §6.2: `ES(t) = { op \| ∃ CC r in C7's active registry at t such that op ∈ exec(r) }`, and `C6` MUST block any operation not in `ES(t)`. |
| **Enforcement** | `C7` compiles; `C6` validates signature, expiry, redemption status, and invariant-set version, then admits. `ES(t)` is monotonically shrinking between permit decisions: nothing enters it except through a `C2` permit. |
| **Counterexample / test** | NT-001 (no CC → blocked), NT-002 (expired CC → blocked), NT-003 (replay → blocked), and the Part IV network-layer P4 verification. **A falsification is any demonstrated path by which an operation reaches a governed system in the boundary without a redeemed CC.** |
| **Evidence produced** | `EXECUTION_BLOCKED` events with a typed `block_reason`; the absence of any `EXECUTION_AUTHORIZED` without a corresponding redeemed CC; governed systems' own access logs, cross-checked per §29.4. |
| **Does NOT establish** | That the *content* of a permitted action is safe (Part VI §28.6, residual TH-10.A); that channels outside the modeled boundary are covered (TH-3/TH-9 residuals); that P4 is achievable in a given network (open question RQ-8). |

**Prior art.** Complete mediation is Saltzer & Schroeder (1975) and Anderson (1972); its formal
treatment as an enforceable class is Schneider, *Enforceable Security Policies*, TISSEC 3(1), 2000,
and Ligatti, Bauer & Walker on edit automata (IJIS 4(1–2), 2005). CROA claims no novelty for the
principle. What CROA adds is the *artifact* that carries the decision across the boundary (the CC)
and the requirement that it be the sole admitted form. See [`docs/prior-art.md`](../docs/prior-art.md).

---

## P-B — Authority Non-Expansion **(new in v1.1-draft)**

| | |
|---|---|
| **Claim** | No admission control, delegation, orchestration, or composition of governed actions can cause a subject to cause an execution that the composition's least-authorized participant could not have caused alone. |
| **Preconditions** | All participants act as authenticated subjects through the Agent Surface; delegation, where used, conforms to Appendix L; no participant holds an out-of-band channel to a governed system (P4). |
| **Invariant** | **I8 — Authority Non-Expansion.** *Effective authority is non-increasing under admission, delegation, and composition.* Formally, for any delegation or composition producing an executing subject `S` from authorizing subjects `A₁…Aₙ`: `effective_authority(S) ⊆ ⋂ᵢ effective_authority(Aᵢ)`, where *effective authority* is the set of governed operations the subject can cause to cross TB-3 after roles, qualification, delegated scope, active authorizations, and enforced controls are combined — as distinct from the nominal permissions any one of those grants. |
| **Enforcement** | Already required pointwise and now stated as one property: RBAC monotonicity (§4.9.1) and AQL monotonicity (§4.9.2) may only restrict; `C7` MUST NOT widen an authorization's exception scope (§4.4.3); `ES(t)` does not expand without a `C2` permit (§6.2); delegated scope MUST satisfy `scope(S) ⊆ scope(O)` under the canonical subset test (Appendix L D3) and MUST additionally pass `C2.eval` independently (D1); cross-domain and cross-agent CC redemption are prohibited (Part IV §20.6, §21.3). |
| **Counterexample / test** | **NT-008 (new)** — authority non-expansion: (a) a delegation token purporting to widen an action class, a target, a parameter constraint, or a validity window MUST fail-deny with no CC compiled; (b) an authorization artifact presented against an action outside its compiled `cc.exception_scope` MUST be blocked at `C6`; (c) a sub-agent MUST NOT obtain a CC whose `cc.authorization_scope` exceeds the delegating subject's authorized scope at the time of compilation; (d) two subjects each individually permitted MUST NOT, by composition, cause an operation neither could cause alone. **A falsification is any construction that yields effective authority strictly greater than the intersection.** |
| **Evidence produced** | `ADMISSION_REJECTED` / `DENY` / `EXECUTION_BLOCKED` events carrying the failed subset relation; `event.delegation_chain` for every delegated action (schema: `event.schema.json`), recording per hop the authorizing subject and the canonical scope whose subset relation was established. |
| **Does NOT establish** | That the *nominal* permissions an enterprise grants are appropriate — CROA governs composition, not policy content (§1.3). That authority is non-increasing across systems CROA does not mediate. That an identity, once spoofed, is bounded — the property is conditioned on the identity prerequisite (RQ-16 in [`prerequisites.md`](../docs/prerequisites.md)). |

**Why this is stated as one property.** Each clause under *Enforcement* was already normative in
v1.0; none is new. What was missing was the composed statement and a test for it. Naming the
property makes the architecture falsifiable at its weakest structural joint — composition — rather
than only at each mechanism in isolation. The distinction between *nominal permission* and
*effective authority* is not CROA's; it is Miller, *Robust Composition* (2006), and, for agentic
systems, Salomon, Shaked & Noga, arXiv:2608.05884. CROA cites both and claims only the composed,
testable statement over its own architecture.

---

## P-C — Trajectory Constraint Preservation

| | |
|---|---|
| **Claim** | A violation assembled from individually permitted actions is denied before the action that would complete it, for any invariant registered with a trajectory profile that matches its accumulation behaviour. |
| **Preconditions** | The invariant is registered with the correct trajectory rule profile — `TP-W` for bounded-horizon convergence, `TP-C` for aggregate accumulation, `TP-X` where accumulation spans sessions for a subject (Part II §4.6.3); the accumulation-contributing action classes are declared completely and validated against the `C4` configuration at deployment (Appendix S §S.6). |
| **Invariant** | T8; realized by `C4` maintaining trajectory state and by `C2.eval` step 4 (hard breach → DENY) and step 6 (unrebutted alert → AMBIGUOUS → DENY under I5). |
| **Enforcement** | `C4` MUST provide invariant state to `C2` *before* the permit decision; it MUST raise a trajectory alert before the next action in the session is evaluated; at L4, any invariant exposed to accumulation MUST be registered as `TP-C` and, where accumulation spans sessions, `TP-X` — windowed analysis alone does not satisfy L4 (Part VI §28.2). |
| **Counterexample / test** | NT-006 (progressive export → alert at threshold, deny at limit). **A falsification is a sequence of individually permitted actions that reaches a registered-invariant-violating state without a deny** — including the low-and-slow and cross-session patterns of TH-7.D/TH-7.E. |
| **Evidence produced** | `TRAJECTORY_ALERT` with the contributing action sequence, the projected state, and a `trajectory_state_id`; the subsequent `DENY` linked by that id; the cumulative value reconstructable from the `C5` record alone. |
| **Does NOT establish** | That accumulation over an *unregistered* invariant is detected — it is not; profile assignment is an enterprise obligation, not an architectural discovery mechanism. That accumulation **across distinct subjects** is detected: `C4` trajectory scope is per-session and, for `TP-X`, per-subject; cross-agent trajectory state exists only within one orchestrated delegation session (Appendix L D4) and is otherwise an OPTIONAL extension (§4.6.1). **Two cooperating agents under distinct subject identities and outside a single delegation chain are, by construction, outside `C4`'s default scope.** That cumulative state is safe under concurrent evaluation — see P-D and the open residual below. |

**Prior art.** That individually valid actions can collectively violate a system invariant is the
thesis of Lotfi, Karmaker Shanto, Karim & Bertino, arXiv:2608.01558, and of Kaptein, Khan &
Podstavnychy, arXiv:2603.16586; the non-compositionality of permissibility is stated in Liu, Wang &
Capponi, arXiv:2605.24462. CROA claims no novelty for the observation. What CROA contributes is
making the trajectory profile a **declared, registered property of every invariant**, with a
conformance level that refuses `TP-W` alone where accumulation is possible.

---

## P-D — Single-Use Authorization Consistency

> **Named narrowly on purpose.** CROA establishes atomicity for the *redemption of a commitment or
> an authorization artifact*. It does **not** establish general stateful-authorization consistency
> across cumulative governance state. Naming this property "Stateful Authorization Consistency"
> would claim the latter. It does not.

| | |
|---|---|
| **Claim** | At most one execution is authorized per Compiled Commitment, and at most one (or `N` under a declared `bounded-count` policy) per authorization artifact — under concurrency, across every enforcement instance, in every deployment topology. |
| **Preconditions** | A single linearizable redemption authority shared by all `C6` instances (§4.8). A per-instance or per-gateway redemption registry is non-conformant. |
| **Invariant** | §4.8: redemption MUST be a single linearizable compare-and-swap claiming `cc.id` (and, for a governed exception, `cc.auth_ref`) in one indivisible operation. Query-then-act is explicitly prohibited as a time-of-check-to-time-of-use race. |
| **Enforcement** | `C6`, against the shared redemption authority, committing ahead of asynchronous evidence materialisation (Appendix R Inv. 5 replication lag MUST NOT open a redemption window). |
| **Counterexample / test** | NT-007 step 4: present the same `cc.id` (and the same `auth_id`) simultaneously to two `C6` instances; **at most one** `EXECUTION_AUTHORIZED`. **A falsification is any topology or timing under which two executions are authorized from one commitment or one authorization.** |
| **Evidence produced** | Exactly one `EXECUTION_AUTHORIZED` per `cc.id`; `EXECUTION_BLOCKED` with `CC_ALREADY_REDEEMED` / `AUTHORIZATION_ALREADY_REDEEMED` for every loser. |
| **Does NOT establish** | **Consistency of cumulative (`TP-C`/`TP-X`) trajectory state under concurrency.** Two governed actions evaluated concurrently carry *distinct* `cc.id`s, so the redemption CAS does not relate them; each may be evaluated against the same pre-increment aggregate and both admitted, jointly crossing a threshold neither crossed alone. See the residual below and RQ-16. Nor does it establish that a CC remains *appropriate* at redemption: `C6` re-validates signature, expiry, redemption status, revocation, and `cc.invariant_set_version` against the invariant **registry**, but not the runtime trajectory state or the policy-artifact version (open residual; RQ-17). |

**Prior art and the open residual.** The general problem — an authorization that was valid when
decided but stale when the effect commits — is formalised as *policy-state serializability* by Peng
& Wu, arXiv:2608.02764. CROA solves the single-use case and does not solve the general case. That
is stated here rather than implied. The v1.1-draft adds a minimum requirement for the cumulative
case (per-accumulation-key serialisation of the read-evaluate-increment cycle for `TP-C`/`TP-X`
invariants; Part II §4.6.3) but does **not** claim general serializability, and the residual remains
declared until independent evidence exists.

---

## P-E — Decision Reconstructability

> **Named narrowly on purpose.** This is *not* "Evidence Completeness". A hash chain proves the
> ordering and non-alteration of the events that were written. It cannot, by itself, prove that
> every governed action produced an event. Completeness rests on I6/I6.1 fail-deny plus external
> anchoring — an architectural assumption, verifiable by cross-check, not a cryptographic result.

| | |
|---|---|
| **Claim** | Any individual governance decision is reconstructable from the `C5` record alone — without the agent's reasoning logs, the agent's operating environment, or the implementing party's narration. |
| **Preconditions** | Read access to `C5` (which §29.4 distinguishes sharply from the implementing party's *cooperation*); the `C5` signing key held outside the governed agent's trust domain (Appendix R Inv. 4); external anchoring of the sealed-segment head (TH-4). |
| **Invariant** | I3 (Auditability), I6 (Observability), I6.1 (durable write-ahead recording before the transition proceeds), I7 (Lifecycle). |
| **Enforcement** | Append-only, hash-chained, per-component-signed events; storage-layer append-only enforcement (P2); fail-deny if local durable commitment is unavailable. |
| **Counterexample / test** | Chain verification over the audit period; reconstruction of a sampled decision from `C5` alone; the §29.4(c) cross-checks against governed systems' own logs and incident records. **A falsification is a decision that cannot be reconstructed from `C5`, or a divergence between the local WAL and the central store.** |
| **Evidence produced** | The `C5` extract, its chain verification result, and the CC-integrity sample. |
| **Does NOT establish** | **Capture completeness from the record itself.** A conformant record proves what it contains; that it contains *everything* follows from the fail-deny gate and is corroborated by external anchoring and the §29.4(c) cross-checks — it is not proved by the chain. It does not establish non-forgery against an adversary holding the signing key (Appendix R Inv. 4 states the condition that excludes this). It does not establish that the *policy* the record shows was correct — a complete, verifiable log of a wrong decision is a complete, verifiable log of a wrong decision. |

**Prior art.** Tamper-evident logging is Haber & Stornetta (1991) and Crosby & Wallach (2009), both
already cited in Part I §1.6.3; the omission/split-view gap is explicit in RFC 9162 (Merkle
consistency proofs prove append-only-ness, not receipt of everything issued); provably correct audit
instrumentation is Amir-Mohammadian, Chong & Skalka, POST 2016; detection scoped to *observable*
behaviour is Haeberlen et al., PeerReview, SOSP 2007. For agentic systems specifically, the
coverage/recoverability distinction is Nian et al., *Auditable Agents*, arXiv:2604.05485. CROA's
evidence position is deliberately conservative and its schemas are intended to interoperate with
vendor-neutral per-decision evidence formats rather than to replace them — see
[`spec/schemas/README.md`](schemas/README.md).

---

## P-F — Evaluation Determinism

| | |
|---|---|
| **Claim** | Two evaluations of the same governed action yield the same outcome. |
| **Preconditions** | Same grounded action specification, same policy-artifact version, same invariant state, and — where an `E3` method applies — the same pinned analyzer version. |
| **Invariant** | I2 (Determinism). The analyzer version is part of the determinism key, so a verdict change across an analyzer upgrade is not an I2 violation. |
| **Enforcement** | `C2`; a non-deterministic evaluator, including an LLM without a pinned reproducible decoding configuration, MUST NOT be placed in the `C2` decision path. A generative model MAY act only as an advisory pre-classifier outside the control plane, reduced to a deterministic verdict before reaching `C2`. |
| **Counterexample / test** | Replay of sampled decisions at equal determinism key. **A falsification is two differing outcomes at equal key.** |
| **Evidence produced** | `event.action_spec`, `event.policy_artifact_id`, `event.invariant_state`, `event.analyzer_version` on every decision event. |
| **Does NOT establish** | That the decision is *correct*. Determinism is reproducibility, not soundness. It also does not establish that a *replayed workflow* reproduces the same downstream outcomes — CROA's determinism is a property of the governance verdict and its evidence record, not of the governed agent, whose behaviour is expressly non-deterministic. |

**Prior art.** Deterministic governance is not a CROA differentiator and is not claimed as one.
See Kaptein et al. (arXiv:2603.16586) on deterministic policy functions, Bhattarai & Vu
(arXiv:2602.09947) on architectural determinism as a necessary condition, and Smith & McCarthy,
*Deterministic governance for generative systems*, AI and Ethics 6, 394 (2026),
DOI 10.1007/s43681-026-01172-6.

---

## Properties CROA does not have

Listed so that no reader infers them, and so that each is a candidate for future work rather than a
silent gap.

| Property CROA does **not** establish | Status | Where it is tracked |
|---|---|---|
| **Cumulative-State Serializability** — that concurrent evaluations against a shared `TP-C`/`TP-X` aggregate cannot jointly cross a threshold | v1.1-draft adds a minimum per-accumulation-key serialisation requirement; the general property is **not** claimed | RQ-16; Part II §4.6.3; Appendix S §S.6 |
| **Commit-time authorization freshness** — that a CC still reflects current trajectory state and policy-artifact version at redemption | Not established. `C6` re-checks the invariant **registry** version, not runtime state | RQ-17; Part II §4.8 |
| **Trap-State Freedom** — that a permitted action never leads to a state from which every continuation violates an invariant | Not modelled. CROA's answer to such a state is to deny every continuation, which is safety-preserving but is a liveness cost, not a safety property | RQ-18 |
| **Resource-Budget Preservation** — that cumulative compute, token, or monetary spend cannot be exhausted across a trajectory | Not a governed quantity in v1.0. `TP-C` can carry a spend metric if an enterprise registers one, but no requirement makes it so | RQ-19; Part II §5.8 |
| **Irreversible-Effect Accumulation Bounds** — that the accumulation of individually authorized *irreversible* effects is bounded | The R0–R4 reversibility classification (T5) is not currently a dimension of any trajectory profile | RQ-20 |
| **Cross-agent trajectory detection** outside a single delegation session | OPTIONAL extension only (§4.6.1); see P-C *Does NOT establish* | RQ-10 |
| **Semantic safety of permitted content** | Explicitly disclaimed (Part VI §28.6; residual TH-10.A) | RQ-2 |
| **Completeness of the registered invariant set** | Enterprise-attested and assessor-reviewed; not established by CROA | Part VI §28.2 |

---

## How to falsify CROA

The shortest path for a reviewer:

1. Pick a property above. Read its **Preconditions** — a break that violates a stated precondition
   is a finding about the *precondition's achievability* (still valuable; see `SECURITY.md`), not a
   break of the property.
2. Construct a counterexample against the **Invariant**, or an argument that the **Enforcement**
   does not entail it.
3. File it under *Discussions → Challenge the Claim*, or as a
   [conformance-gap issue](../.github/ISSUE_TEMPLATE/conformance-gap.yml).

The properties most likely to break, in our own estimation, are **P-B** (composition is where
authority silently widens), **P-C** across distinct subject identities, and **P-D**'s cumulative
residual. We would rather those be found here than in a production deployment.
