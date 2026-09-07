---
tags:
  - croa_foundation
---

# Appendix I — C4 Implementation Approaches (Trajectory Analysis)

**CROA Framework v1.0.1.1 · Informative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The
>
## I.1 Purpose and scope

Part II §4.6.2 requires `C4` to maintain a projection of system state after each permitted action and to raise a trajectory alert when any registered invariant's violation condition is *satisfiable* within a horizon of *h* further governed actions (RECOMMENDED *h* = 3). Stated in full generality this is a reachability/model-checking problem whose cost grows with the branching factor of the action space and the horizon, and whose exactness depends on how state is abstracted. A naïve realization — enumerating all action sequences of length ≤ *h* over a rich state — is exponential and not viable at the action rates of real agents.

This appendix specifies a **state-projection contract** and four implementation patterns of increasing power and cost, so that an enterprise can select a realization matched to its invariants' evaluability classes (Part I §2.6) and consequence classes (R0–R4, Part I T5). None of these patterns is mandatory; an implementation MAY use any method that satisfies Part II §4.6.2 and does not narrow the alert set below the specified minimum.

## I.2 The state-projection contract

The "projected state" of Part II §4.6.2 is **not** a full simulation of the governed external systems. It is an abstraction `σ` over a finite set of *governance-relevant state variables* declared in GitOps Definition (§7.2). Formally, an implementation MUST define:

- a finite set of state variables `V = {v₁ … vₖ}`, each with a finite or finitely-abstracted domain, that are sufficient to express the violation conditions of the registered trajectory-relevant invariants;
- a deterministic **projection function** `project(σ, a) → σ'` that, given the current abstract state and a permitted action `a`, returns the next abstract state. `project` MUST be deterministic (I2) and MUST be sound for the targeted invariants: it MUST NOT under-state any state change that could move the projection toward a violation (it MAY over-state, yielding conservative — earlier — alerts);
- for each trajectory-relevant invariant `I`, a **violation predicate** `viol_I(σ)` over `V`.

The projection function is the missing specification the critique identified. Declaring `V`, `project`, and `viol_I` for each trajectory-relevant invariant is a GitOps Definition (§7.2) deliverable (it is part of the C4 Design Specification, Part III §7.2 Step 4). Soundness of `project` is what makes a *bounded* search safe: if the true reachable set is contained in the abstract reachable set, then "no alert within the abstraction" implies "no violation within the horizon under the modeled action space" — the same conditional guarantee that scopes T1 (Part I §3).

## I.3 Implementation patterns

### Pattern A — Monotone counters and quotas (E1/E2; O(1) per action)

Many trajectory invariants are *accumulation* invariants: "no more than N records exported per session," "cumulative spend ≤ budget," "no more than k distinct PHI subjects touched." These reduce to monotone counters in `σ`. `project` increments the counter; `viol_I` is a threshold test; horizon evaluation is a single arithmetic comparison (`counter + h·max_increment ≥ threshold`). Cost is O(1) per action and O(|V|) memory. This pattern covers the majority of real trajectory invariants and SHOULD be the first choice.

### Pattern B — Typed-sequence (regular / automaton) rules (E2; O(1) amortized)

"Action of type X must not follow an unreverted action of type Y," "a write to zone Z is forbidden after a read from external source S" — order-sensitive invariants over a *typed* action alphabet — are recognizable by a finite automaton. `σ` is the automaton state; `project` is the transition function; `viol_I` is "an accepting (violating) state is reachable within *h* transitions," precomputed as a fixed-radius lookup on the automaton. Cost is O(1) amortized per action; the *h*-bounded reachability table is computed once per invariant-registry version. This is the recommended pattern for ordering and dependency invariants and directly addresses TH-7 (Path Composition Attacks).

### Pattern C — Bounded symbolic reachability over the abstract state (E2; cost bounded by abstraction)

Where invariants couple several state variables, encode `V`, `project`, and `viol_I` symbolically (e.g., as SMT constraints or a BDD over finite domains) and ask a bounded solver: "is `viol_I` satisfiable within *h* applications of `project` from `σ`?" This is bounded model checking with a fixed unrolling depth *h*, not unbounded verification, so it terminates with a worst-case cost of O(b^h · solve) where `b` is the abstract branching factor — kept tractable by (i) the small recommended horizon (*h* = 3), (ii) aggressive state abstraction (finite domains, predicate abstraction), and (iii) restricting symbolic search to invariants not already covered by Patterns A/B. Use this pattern only for the residual set of coupled invariants.

### Pattern D — Precomputed convergence signatures (E2/E3; O(1) lookup, conservative)

For high-rate paths where even Pattern C is too costly online, precompute offline (per invariant-registry version) the set of abstract-state "danger signatures" from which a violation is reachable within *h*, and reduce the online check to a membership test against `σ`. The signature set MUST be a sound over-approximation (it may raise early/conservative alerts but must not miss a convergent trajectory), which places this pattern's residual in the E3 sense (false positives, no false negatives). This trades a higher `AMBIGUOUS`/alert rate for O(1) online cost.

## I.4 Choosing a pattern

| Invariant shape | Recommended pattern | Online cost | Residual |
|---|---|---|---|
| Accumulation / quota | A (counters) | O(1) | none (within abstraction) |
| Ordering / dependency over typed actions | B (automaton) | O(1) amortized | none (within abstraction) |
| Coupled multi-variable, low rate | C (bounded symbolic) | O(b^h) | none (within abstraction) |
| Coupled, high rate | D (precomputed signatures) | O(1) lookup | false positives (sound over-approx.) |

A deployment SHOULD cover as much of its trajectory-relevant invariant set as possible with Patterns A and B (exact and O(1)), reserve Pattern C for the residual coupled set, and use Pattern D only where action rate forces it. A registry that requires Pattern C/D for high-consequence (R3–R4) invariants is a signal to narrow the action surface (Part III §7.2 Step 5) so the hazard re-enters the modeled, cheaply-decidable space.

## I.5 Complexity, honesty, and degradation

- **Horizon cost.** All patterns are bounded by the horizon *h*. Increasing *h* increases assurance and cost; Patterns A/B are insensitive to *h* (closed-form/precomputed), Pattern C is exponential in *h*, Pattern D pushes the *h* cost offline. The enterprise's choice of *h* (Part II §4.6.2) is therefore also a performance decision (see Appendix J).
- **Soundness vs. completeness.** Every pattern here is *sound* (no missed convergent trajectory within the abstraction) and may be *incomplete* (conservative alerts). This is the safe direction: a false trajectory alert downgrades the next action to ambiguity resolution (fail-deny-leaning), never to silent permit. The cost of conservatism is governance friction, which is the quantity Part III §7.2 Step 6 requires be measured.
- **Abstraction gap.** The guarantee is relative to the declared abstraction `V`/`project`. A state change that is invisible to `V` is invisible to C4; this is the same modeled-action-space caveat that scopes T1 (Part I, Chapter 3, Tenet T1) and L4 (Part VI §28.6). GitOps Definition (§7.2) review of `V`'s adequacy is therefore a governance control, not an implementation detail.
- **Degradation.** If C4 cannot complete trajectory evaluation within its latency budget (Appendix J) for a given action, it MUST raise an ambiguity (fail-deny), not skip the check — consistent with the fail-deny default (Part II §5).

## I.6 Relationship to the rest of the framework

This appendix realizes Part II §4.6 (C4) and the GitOps Definition (§7.2) C4 Design Specification (Part III §7.2). The state-projection contract (§I.2) is the concrete form of the "projected state" referenced normatively in Part II §4.6.2. Patterns and costs feed the performance profile (Appendix J). The soundness/abstraction discussion is the C4 counterpart of the invariant-evaluability taxonomy (Part I §2.6) and underwrites the conditioned T1 claim (Part I §3) and the L4 claim-scope statement (Part VI §28.6).

---

*End of Appendix I — C4 Implementation Approaches.*
