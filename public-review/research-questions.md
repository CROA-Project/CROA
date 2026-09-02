# CROA Open Research Questions

What CROA does not yet know. Each question states why it matters and what evidence would settle it,
so that answering one is a bounded piece of work rather than an invitation to speculate. If you have
data, an argument, or an implementation that bears on one, open a Discussion or an issue and cite the
question ID (e.g. `RQ-3`).

These are real unknowns. "CROA does not hold under condition X" is a welcome and citable result.

---

## A. The core guarantee

**RQ-1 — Does structural unreachability hold under realistic adversarial pressure?**
The central claim is that, within the modeled action space and registered invariants, invariant-violating execution paths are unreachable. *Why it matters:* the entire value proposition rests on this. *What would move it:* a concrete scenario or red-team exercise where a governed agent reaches a prohibited end-state without an explicit signed authorization — or a credible argument that the boundary conditions are unachievable in practice.

**RQ-2 — How tight is the boundary between "modeled" and "unmodeled" action space?**
CROA only governs what an enterprise has modeled. *Why it matters:* if real action spaces are too large or too fluid to model usefully, the guarantee covers too little to matter. *What would move it:* evidence on how much of a real agent's action surface can be feasibly modeled, and what fraction of incidents originate in the unmodeled remainder.

## B. Evaluability and cost (the E3 question)

**RQ-3 — What is the real-world false-positive / friction rate of E3 (semantic, approximated) invariants?**
Some invariants can only be checked by approximate (E3) methods, which over-approximate and may deny safe actions. *Why it matters:* high friction drives the governance-erosion loop the framework itself describes (operators pressure to relax policy). *What would move it:* measured AMBIGUOUS→DENY rates from real or simulated deployments, by invariant type.

**RQ-4 — Can the action surface usually be narrowed enough to convert E3 invariants into exact (E1/E2) ones without destroying agent utility?**
The framework's answer to E3 cost is to shrink the action surface. *Why it matters:* if narrowing far enough to be exactly governable makes the agent useless, the approach is self-defeating for expressive agents. *What would move it:* worked cases showing where on the utility–guarantee frontier real deployments actually land.

## C. Performance and operability

**RQ-5 — What is the latency and throughput cost of the control path at scale?**
Every action traverses admission → context → evaluation → compilation → synchronous audit write → execution-boundary check. *Why it matters:* coding/tool-calling agents emit hundreds–thousands of actions/hour; if per-action overhead or the C5 synchronous-write becomes the bottleneck, deployments fail-deny under load. *What would move it:* benchmark reports across realistic action rates and C5 backends. (See the [benchmark report template](../evidence/templates/implementation-report.md).)

**RQ-6 — Is the append-only, tamper-evident C5 audit model operationally sustainable?**
*Why it matters:* the auditability guarantee depends on a complete, verifiable event chain. *What would move it:* operational data on storage growth, chain-verification cost, and the viability of the high-performance WAL pattern under real workloads.

**RQ-15 — Can C5 sustain the availability coupling that fail-closed implies, and is a safe degraded mode achievable?**
Fail-closed plus a synchronous audit write couples C5's availability to the most critical system it governs (see [`operating-c5.md`](../docs/operating-c5.md)). *Why it matters:* if C5 becomes a tier-0 single point of failure, the operational cost and risk may outweigh the governance benefit — and any pressure to relax fail-closed reopens the gap. *What would move it:* deployment data on running C5 at broker-grade availability, and evidence on whether a degraded mode can preserve chain integrity for low-consequence action classes without weakening the guarantee for high-consequence ones.

## D. The dependencies the guarantee rests on

**RQ-7 — Is a sufficiently complete Technical Golden Record (C3) achievable in real enterprises, and at what cost?**
Context grounding depends on a registry of legitimate endpoints/resources the framework itself calls "notoriously incomplete." *Why it matters:* an incomplete Golden Record either blocks legitimate work or leaves gaps. *What would move it:* reports on the effort to build/maintain a Golden Record and its observed completeness over time.

**RQ-8 — Does network-enforced execution-boundary containment (P4) hold in common enterprise topologies?**
The guarantee assumes governed systems accept only operations derived from authorized commitments. *Why it matters:* if the boundary is bypassable (shadow paths, legacy integrations), the structural claim degrades to advisory. *What would move it:* deployment reports on enforcing P4 in real network architectures, and where it proved impractical.

## E. New and second-order risks

**RQ-9 — Can Technical Sycophancy reappear at the policy-authoring layer?**
CROA moves enforcement out of the model — but humans (or agents) still author the invariants and policies. *Why it matters:* if policy authors weaken invariants under the same pressures, the failure mode re-enters one level up. *What would move it:* analysis or evidence of invariant-quality drift over time in governed deployments.

**RQ-10 — Is C4 trajectory monitoring reliable against slow, distributed, multi-session attacks?**
Cumulative patterns (e.g., gradual data exfiltration across sessions/agents) are the class single-action checks miss. *Why it matters:* it's a primary justification for C4. *What would move it:* red-team results on detecting cumulative/sequential abuse without excessive false positives.

**RQ-11 — Is governed multi-agent delegation (Appendix L) sound under delegation chains?**
*Why it matters:* delegation is where authorization scopes can silently widen. *What would move it:* a formal analysis or implementation stress-testing scope-narrowing across delegation hops.

**RQ-14 — Does the governed-exception rate need to be a monitored governance-health signal, and what threshold indicates erosion?**
The Governed Exception is specified as signed, bounded, single-use and logged (§4.3.1, §4.8; the reference harness demonstrates the replay case, and NT-007 is the conformance test). The *organizational* risk is its twin of RQ-9: under 3-a.m. production pressure, the on-call approver rubber-stamps, and the exception becomes the normal path — governance erosion moving from the agent to the human. *Why it matters:* an exception path that is always available under pressure quietly defeats the guarantee it was meant to preserve. *What would move it:* operational data on exception frequency in real deployments, and whether treating the exception rate (per action class, per approver) as a first-class health metric — with an alert threshold and periodic review — detects erosion early. Candidate practice: exceptions above a threshold trigger a policy review, not just another approval.

**RQ-16 — Is cumulative (`TP-C`/`TP-X`) governance state safe under concurrent evaluation?**
CROA mandates an atomic, linearizable compare-and-swap for *redemption* of a commitment or an authorization (§4.8), which closes the replay and double-redemption race across every enforcement instance. It does **not**, in v1.0, specify concurrency semantics for a cumulative aggregate: two actions evaluated concurrently carry distinct `cc.id`s, so the redemption CAS does not relate them, and each may be evaluated against the same pre-increment total. *Why it matters:* a budget or distinct-set threshold that two concurrent actions jointly cross is exactly the class of violation `TP-C` exists to prevent — and the failure is silent. *What would move it:* an implementation report on serialising the read-evaluate-increment cycle per accumulation key, its throughput cost, and whether a weaker consistency level suffices in practice. Compare Peng & Wu, arXiv:2608.02764, which formalises the general problem as policy-state serializability. Tracked as a declared residual in [`spec/properties.md`](../spec/properties.md) P-D.

**RQ-17 — Should authorization be re-validated at commit time, and against what?**
At redemption, `C6` re-checks signature, expiry, single-use status, revocation, and the invariant **registry** version — but not the runtime trajectory state or the policy-artifact version. A commitment compiled when a session's trajectory was non-convergent therefore remains redeemable until `cc.expires_at` (default ≤24h) even if the session has since become convergent. *Why it matters:* this is stale authorization in the precise sense the literature names; the alternative — full re-evaluation at the boundary — moves work onto the latency-critical path and duplicates `C2`. *What would move it:* evidence on the real-world size of the decision-to-execution window, and whether a bounded freshness check (rather than full re-evaluation) closes the gap at acceptable cost.

**RQ-18 — Should CROA model states from which every continuation violates an invariant?**
A locally safe, individually permitted transition can lead to a state where no permitted continuation exists — a partially completed multi-step operation that can neither proceed nor be reversed. CROA's response is to deny every continuation, which preserves safety but converts the situation into a liveness failure with an operational cost. The state is not modelled as a failure mode anywhere in v1.0. *Why it matters:* the operational pressure to unblock such a state is exactly the pressure that erodes governance (TH-2.C). *What would move it:* real cases from pilots, and an argument about whether trap avoidance belongs in `C4`'s horizon analysis or in invariant authoring.

**RQ-19 — Should resource, cost, and token budgets be governed quantities?**
CROA has no notion of compute, token, or monetary spend as a first-class governed metric; an enterprise may register one as a `TP-C` invariant, but nothing requires it and no reference test covers it. *Why it matters:* cumulative resource abuse across agent trajectories is an empirically demonstrated attack class (Luo et al., USENIX Security 2026), and unbounded spend is one of the more common real-world agent failures. *What would move it:* pilot evidence on whether spend behaves like other cumulative invariants or needs distinct treatment (credits, refunds, multi-currency, provider-side accounting lag).

**RQ-20 — Should irreversibility be a dimension of trajectory analysis?**
The reversibility/consequence classification R0–R4 (Tenet T5) sets the authorization bar for a single transition, but is not used by any trajectory profile: an accumulation of twenty reversible effects and an accumulation of twenty irreversible ones are treated identically by `TP-C`. *Why it matters:* the accumulated consequence of irreversible actions is not recoverable, which is precisely the case where a threshold matters most. *What would move it:* worked cases where an irreversibility-weighted threshold would have changed the outcome, and an assessment of the authoring cost.

## F. Adoptability

**RQ-12 — What is the realistic integration cost and developer experience of adopting CROA?**
*Why it matters:* a correct architecture that is too costly or unpleasant to adopt does not become a standard. *What would move it:* pilot reports on time-to-first-governed-action, integration friction, and what made adoption easier or harder.

**RQ-13 — Does the L0–L5 conformance model map cleanly onto how real systems are actually built and assessed?**
*Why it matters:* if the levels don't correspond to recognizable deployment states, conformance claims become meaningless. *What would move it:* assessor feedback from attempting to place real deployments on the ladder.

---

## How to contribute to a research question

1. Pick a question. Comment in *Discussions → Challenge the Claim* (for A/E) or *Implementation Q&A* (for B–D, F), referencing the `RQ-` ID.
2. If you have results, file an [evidence report](../evidence/README.md) and link the `RQ-` ID.
3. If your finding implies a change to the framework, it becomes an [RFC](../rfcs/README.md).

This list is itself under review. If a question is missing — especially one that threatens the core claim — propose it. We would rather find the hard problems now, in public, than have them found later by an adopter in production.
