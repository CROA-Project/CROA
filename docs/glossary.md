# Glossary

**Objective:** plain definitions of the terms used across CROA, for newcomers.
**Authoritative source:** Appendix A (Lexicon) of the specification. Where this and the spec differ, the spec governs.

---

**Agentic sprawl** — the uncontrolled proliferation of autonomous agents across enterprise workflows, producing fragmented, weakly governed, hard-to-audit execution.

**Compiled Commitment (CC)** — the immutable, content-addressed, signed artifact produced by C7 that encodes exactly one authorized action and its constraints. The **only** thing allowed to cross the execution boundary. (Named "RFC / Request for Change" in pre-1.0 drafts; unrelated to IETF RFCs.)

**Conformance level (L0–L5)** — how completely a *deployed system* realizes the architecture, within a defined governance boundary. **L4** is the threshold at which a system may be called "CROA-conformant."

**C1–C7** — the seven logical components: Policy Authority (C1), Execution Governor (C2), Path Resolver (C3), Invariant Monitor (C4), Audit & Provenance Store (C5), Execution Firewall (C6), Contract Compiler (C7). Numbers denote identity, not pipeline order.

**Evaluability classes (E1 / E2 / E3)** — how an invariant can be checked: **E1** exact/decidable; **E2** exact over bounded/structured input; **E3** semantic/approximated (sound over-approximation, may over-deny). E3 is where most cost and friction live.

**Execution boundary** — the line (TB-3) past which only Compiled-Commitment-derived operations may pass; enforced by C6, ideally network-enforced (property P4).

**Execution-layer governance** — enforcing policy at the point of action against systems, rather than trying to shape model behavior.

**GAR (Governed Action Request)** — the structured request an agent submits to the Agent Surface to propose an action.

**Governance success** — a *deny* or *block* is the system working correctly, not a fault. CROA requires denies to be recorded as successes, not errors.

**Invariant** — a registered constraint a governed action must not violate (e.g., "data.export must not target an unapproved system"). Each has a declared evaluability class.

**Structural reachability / unreachability** — whether a given (here, invariant-violating) execution path *exists* in the architecture at all. CROA's central claim is that such paths are unreachable *by the agent's own choice* — reachable only through a governed, signed authorization — not merely discouraged. The sense is **state reachability under a constrained transition relation** (the model-checking sense; Part I §2.5), not code or control-flow reachability, and not merely "the tool is not in the allow-list". What is quantified over is the *execution* state space; see **authority state** below for what is and is not covered.

**Accumulation key** — the tuple by which a cumulative (`TP-C`/`TP-X`) invariant's aggregate is kept: for example `(subject, target system)` for a rolling export limit, or a campaign identifier for a spend cap. It is the unit over which the read-evaluate-increment cycle must be serialised.

**Authority state** — the set of governed operations a subject can currently cause to cross the execution boundary. CROA's formal model (Part I §2.5) quantifies over execution states; authority is constrained *pointwise* by monotone admission (RBAC, AQL), the no-widening rule on compilation, and the delegated-scope subset test — and, from v1.1-draft, *compositionally* by property P-B. See [`spec/properties.md`](../spec/properties.md).

**Effective authority** — what a subject can actually cause once roles, qualification, delegated scope, active authorizations, and enforced controls are combined. Deliberately distinguished from **nominal permission**, which is what any one of those grants on paper. The distinction is not CROA's (Miller, *Robust Composition*, 2006); CROA's contribution is the composed, testable non-expansion property over it.

**Execution surface `ES(t)`** — the set of operations for which a valid, unredeemed Compiled Commitment exists at time *t*. `C6` blocks anything outside it, and it never expands without a permit decision (Part II §6.2).

**Technical Golden Record** — the registry of legitimate endpoints, resources, and entities against which C3 grounds a request. Its completeness is an open practical question (RQ-7).

**Technical Sycophancy** — an agent's tendency to reinterpret a constraint, under objective pressure or ambiguity, in order to still satisfy its goal — leading to silent policy bypasses. A core motivating failure mode.

**Trajectory monitoring** — C4's tracking of cumulative/sequential state across actions, to catch slow or distributed patterns single-action evaluation misses.

**Trust boundaries (TB-1…TB-4)** — Agent, Policy, Execution, and Audit boundaries that partition trust in the architecture.
