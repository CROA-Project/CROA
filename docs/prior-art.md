# Prior art and related work

**Objective:** place CROA honestly among the mechanisms *and the research* it is often compared to, and
say precisely what it borrows, what it adds, and where it does *not* compete.
**Audience:** architects and reviewers who already know this space.
**Authoritative source:** Appendix O of the specification ("CROA and Adjacent Enforcement Mechanisms").
This page is a repo-accessible summary; where it and the spec differ, the spec governs.

> **Two sections.** Part 1 compares CROA to the **engineering mechanisms** a deployment composes.
> Part 2 compares it to the **research literature** on runtime governance of agentic systems, which
> became dense during 2025–2026. Part 2 exists because a framework published in that field without a
> related-work section is not reviewable. It is maintained on a best-effort basis and is certainly
> incomplete; corrections and additions are among the most useful contributions to this repository.

---

## Part 1 — Engineering mechanisms

CROA is **not** a new point control. It is an architecture that composes existing controls so that,
within the modeled action space and under the registered invariants, an unsafe execution path is
*unreachable* rather than merely denied. Most of the systems below are components a CROA deployment
*uses*.

| Prior art | What it does well | What CROA adds over it | Relationship |
|---|---|---|---|
| **Policy engines** — OPA/Rego, AWS Cedar | Deterministic, declarative allow/deny for a single request | A bare decision is advisory unless something structurally stops the agent from acting on a deny. CROA compiles a permit into a single-use, content-addressed, signed **Compiled Commitment** (C7) that the boundary (C6) alone will admit, and adds context grounding (C3), cumulative trajectory evaluation (C4), and a conformance-bearing audit chain (C5). | **Implements C2.** CROA = a policy engine + C3/C4/C7/C6/C5, composed. |
| **Capability-based security** (object capabilities, capability tokens) | Unforgeable, least-authority handles; possession = authority | Capabilities bound *static* authority; CROA's Compiled Commitment is a *per-action, single-use, context-grounded, audited* capability whose scope is verified against the current invariant set at redemption, and whose use is recorded. It also adds cross-action **trajectory** limits a capability can't express. | **Kindred idea, extended.** The CC is a governed, evidence-bearing capability, not a standing one. |
| **Runtime guardrails** — NeMo Guardrails, LLM-judge / classifier filters | Cheap probabilistic checks on model input/output | Model-layer and bypassable under adversarial pressure or Technical Sycophancy. CROA is structural, not behavioral. | **Advisory only**, outside the control plane (Tenet T2); a guardrail's output must be reduced to a deterministic verdict before it reaches C2. |
| **Service meshes / network policy** — Istio, Linkerd, Cilium; seccomp, microVMs | Bound *where* traffic can flow; strong workload isolation | Bounds blast radius, not per-action permissibility. CROA *realizes* its network-enforced boundary (property P4) on top of the mesh, and adds "is *this* action allowed, in *this* context, given the session?" plus evidence. | **Realizes P4/TB-3.** Complementary layer, not a substitute. |
| **Human-in-the-loop / change-ticket gates** | A person approves consequential actions | CROA subsumes this as **Constrained Execution**: a signed, scoped, single-use, audited authorization compiled into the commitment — it cannot silently widen scope or be applied out of band, and low-consequence actions are not gated on a human. | **Subsumed and disciplined** (§4.3.1). |
| **Agent-platform tool scopes / MCP permissions** | Per-tool allow-lists and scopes | A scope says "this agent may call this tool." CROA additionally decides "may it perform *this* action, on *this* target, in *this* context, under enterprise invariants — and here is the signed, audited record." | **Hosts the Agent Surface / RBAC**; CROA adds the governance pipeline behind it. |
| **SIEM / audit pipelines** | After-the-fact detection over logs | CROA's C5 is *upstream* of the SIEM: an append-only, hash-chained, conformance-bearing record on the fail-closed path, and C4 *enforces* cumulative constraints the SIEM only observes later. | **C5 feeds the SIEM**, and is not replaced by it. |

**The one-sentence version.** "More than OPA in front of my tools" — OPA (or Cedar) is one of seven
components; CROA additionally grounds the action in real context (C3), watches the session for
path-composition (C4), compiles every permitted action into the only signed artifact allowed to execute
(C7+C6), and records every decision in a tamper-evident ledger (C5) — so the unsafe path is not merely
*denied*, it is *unreachable* within the modeled action space.

Think this comparison is unfair to one of these tools, or missing one (e.g., eBPF-based enforcement,
WASM sandboxes, data-flow/IFC systems)? That's exactly the kind of correction the public review wants —
open a Discussion or an issue.

---

## Part 2 — Research prior art

### 2.1 Foundations CROA stands on, and claims no novelty for

These are older than the agentic-AI framing and settle several questions CROA is sometimes assumed to
have opened. CROA borrows from all of them.

| Idea | Source | What it settles |
|---|---|---|
| **Complete mediation; the reference monitor** | Anderson, *Computer Security Technology Planning Study*, ESD-TR-73-51, 1972 — "must always be invoked… tamper proof… small enough to be subject to analysis". Saltzer & Schroeder, *The Protection of Information in Computer Systems*, 1975. | CROA's execution boundary (I1, P4, TB-3) is a reference monitor. The **principle** is not CROA's. |
| **What a runtime monitor can and cannot enforce** | Schneider, *Enforceable Security Policies*, ACM TISSEC 3(1), 2000 — the EM class and its limits. Hamlen, Morrisett & Schneider, ACM TOPLAS 28(1), 2006. Ligatti, Bauer & Walker, *Edit automata*, IJIS 4(1–2), 2005. | Sets the theoretical ceiling on any execution gate, CROA's included. A reviewer should read CROA's L4 claim against Schneider's EM characterisation. |
| **Mediation proved, not asserted** | seL4 (SOSP 2009; *seL4 Enforces Integrity*, ITP 2011). | The bar for a *proved* mediation claim. CROA does not meet it and does not claim to: CROA's guarantee is a conformance finding about a deployment, not a machine-checked proof. |
| **Nominal permission vs. effective authority; attenuation** | Miller, *Robust Composition*, PhD thesis, Johns Hopkins, 2006 — "only connectivity begets connectivity". Shapiro & Weber, *Verifying the EROS Confinement Mechanism*, IEEE S&P 2000. Sandhu, *The Schematic Protection Model*, JACM 35(2), 1988. | The permission/authority distinction and attenuation under creation. CROA's property **P-B** ([`spec/properties.md`](../spec/properties.md)) applies this to agent delegation; it is not a new idea. |
| **One-way attenuating credentials** | Macaroons (NDSS 2014); Biscuit; SPKI/SDSI chain discovery (JCS 9(4), 2001); Delegation Logic (ACM TISSEC 6(1), 2003); RFC 8693 OAuth 2.0 Token Exchange. | A Compiled Commitment is, structurally, a per-action attenuated capability carrying an audit obligation. CROA already cites RFC 8693 (Appendix O §O.5). |
| **Safety/reachability analysis over authority states** | Harrison, Ruzzo & Ullman, *Protection in Operating Systems*, CACM 19(8), 1976 (safety undecidable in general); Lipton & Snyder, JACM 24(3), 1977; ARBAC policy analysis (Sasturkar et al., TCS 412(44), 2011). | The formal ancestry of CROA's reachability framing — and the reason CROA scopes its claim to a *registered invariant set over a modeled action space* rather than to an unbounded state space. |
| **Tamper-evident logging and its limits** | Haber & Stornetta, J. Cryptology 3(2), 1991; Crosby & Wallach, USENIX Security 2009 (both already cited in Part I §1.6.3); RFC 9162 (consistency proofs prove append-only-ness, **not** receipt of everything issued); Amir-Mohammadian, Chong & Skalka, *Correct Audit Logging*, POST 2016; Haeberlen et al., *PeerReview*, SOSP 2007. | Why CROA's evidence property is named **Decision Reconstructability** and not "Evidence Completeness". |

### 2.2 Contemporary work on runtime governance of agentic AI

Verified as of **August 2026**. Grouped by the property each addresses. CROA overlaps with several
of these, in most cases by independent arrival at the same idea rather than by borrowing.

| Work | What it does | Relationship to CROA |
|---|---|---|
| **LATTICE** — Calboreanu, *LATTICE: a governance-first architecture for authorized autonomous AI operations*, Frontiers in Artificial Intelligence 9:1800407 (2026), DOI 10.3389/frai.2026.1800407 | Governance/operational plane separation; hashed action bundles; a non-bypassable execution gate; four prose properties including *governance invariance* and *governance determinism*; author-run empirical evaluation. | **The closest published architecture to CROA, and the most important comparison for a reviewer.** Convergent on: execution gating, determinism, plane separation, hash-chained signed evidence, TOCTOU awareness at the gate. Divergent: LATTICE explicitly does **not** cover trajectory-dependent policy (it cites Kaptein et al. for that), cumulative constraints (it names fan-out amplification as an open hole), a delegation calculus, or a conformance ladder; CROA has none of LATTICE's confidence-score routing and no equivalent of its author-run bypass evaluation. Neither work derives from the other. |
| **Policies on Paths** — Kaptein, Khan & Podstavnychy, arXiv:2603.16586 | Formalises governance as deterministic policy functions over an execution *path*, with a shared organisational governance state; argues path-dependent policy is enforceable only at runtime. | Strong convergence with CROA's `C4` and its trajectory profiles. CROA's `TP-0/TP-W/TP-C/TP-X` taxonomy is a finer-grained, registrable form of the same idea; Kaptein et al. give the cleaner general formalism. Conceptual paper — no implementation, no results. |
| **Trajectory Assurance** — Lotfi, Karmaker Shanto, Karim & Bertino, arXiv:2608.01558 (ACM AI Leadership Summit 2026, visionary track) | Position paper: "a sequence of individually permitted actions can collectively violate a state-conditioned invariant"; identity does not propagate across delegation hops. | States CROA's TH-7 problem precisely and proposes no mechanism. Independent corroboration that the problem class is real; **not** support for any CROA result. |
| **Stateful governance / policy-state serializability** — Peng & Wu, *Stateful Governance for Concurrent Agentic Systems*, arXiv:2608.02764 | Names *stale authorization* as the core failure and defines a serializability condition requiring committed effects to be authorized against the policy state immediately before they occur; soundness theorem; author-run prototype. | **The sharpest challenge to CROA's stateful story.** CROA solves the single-use redemption race (§4.8 — an atomic linearizable compare-and-swap shared across all `C6` instances, stronger than most work in this space) but does *not* solve the general case for cumulative governance state. CROA now states that as an explicit residual (`spec/properties.md` P-D) instead of implying coverage. CROA does **not** adopt this work's terminology. |
| **AgentBound** (behavioural governance) — Kaul, Lan & Gupta, arXiv:2606.30970 | Parallel judgments from delegated authorization, an owner-signed constitution, and a site contract, composed over a Deny<Review<Permit lattice; co-signed, replay-verifiable governance receipts. | Convergent on: signed per-decision evidence, an interposed gate between authorization and execution, and monotone composition — "no authority can implicitly expand the perimeter established by another" is the same intuition as CROA's P-B. Divergent: no trajectory or cumulative dimension, no conformance model. ⚠️ **Distinct from the FSE paper of the same name below — do not conflate them.** |
| **AgentBound** (execution boundaries) — Bühler, Biagiola, Di Grazia & Salvaneschi, *Securing Execution Boundaries of AI Agents*, Proc. ACM Softw. Eng. 3, FSE, Article FSE096 (2026), DOI 10.1145/3808103 | Permission manifests for MCP servers plus container/iptables default-deny enforcement; evaluated on 296 servers. | The strongest *empirical* work on execution-boundary containment, and a concrete realisation of the kind of network-enforced containment CROA's P4 assumes. Operates at resource/capability granularity, not action semantics; no evidence chain; permissions bound once at launch. Complementary, not competing. |
| **Runtime contracts** — Ng, Han, Zhang & Wang, *Agent Safety Should Be a Runtime Contract*, arXiv:2608.11274 | Preventive and evidential faces of a runtime contract; gates task completion on checkable evidence; trajectory-with-evidence as the unit of safety. | Convergent with CROA's T3/T10 (evidence as the object of conformance). CROA adds a normative conformance model; this work adds *evidential* gating of claimed completion, which CROA does not do. |
| **Per-decision runtime evidence** — AIREP, arXiv:2608.21363 | A vendor-neutral, signed, hash-chained, offline-checkable record per decision, which declares both what its evidence covers and what it does not. | **CROA should interoperate with this rather than compete.** CROA's four JSON schemas are its own event model; the design intent is that a CROA `C5` event be mappable onto a vendor-neutral per-decision evidence record. See [`spec/schemas/README.md`](../spec/schemas/README.md). |
| **Auditability as a measurable property** — Nian et al., *Auditable Agents*, arXiv:2604.05485 | Defines auditability over coverage, recoverability and policy-checkability thresholds: "policy checkability… cannot operate on actions or phases absent from the record". | Directly relevant to CROA's I3/I6, and the reason P-E is scoped as it is. |
| **Effective authority as a first-class object** — Salomon, Shaked & Noga, *The Vulnerability With No CVE*, arXiv:2608.05884 | Defines *effective authority* as what an agent can cause once tools, credentials, connectors, environment reach and enforced controls are combined — broader than an IAM permission, narrower than what a tool advertises. | The cleanest available statement of the distinction CROA's **P-B** operationalises. A vendor position paper with no empirical support; cited for the concept only. |
| **Adaptive runtime restriction** — Marín & Chaudhary, arXiv:2604.24686 (RiskGate) | Viability-theoretic governance with a monotonic-restriction property and a predicted time-to-boundary. | Convergent with CROA's monotonicity clauses (§4.9.1, §4.9.2). Divergent: probabilistic and advisory where CROA is deterministic and structural. The paper states it has **no** empirical evaluation; it should not be cited as evidence for anything. |
| **Cumulative resource abuse** — Luo et al., *Autonomy Comes with Costs*, USENIX Security 2026 (AgentDoS) | Grey-box fuzzing for denial of service through resource abuse across agent sessions; 36 zero-day findings, 15 CVEs assigned. | Offensive work, not a governance mechanism. It is the best available **evidence that a gap CROA does not close is real**: CROA has no notion of a compute, token, or monetary budget as a governed quantity (see `spec/properties.md`, *Resource-Budget Preservation*, and RQ-19). |
| **Governance by construction** — IBM Research, *Governance by Construction for Generalist Agents*, arXiv:2605.20874 (ACM CAIS 2026) | Policy-as-code intercepting a generalist agent at five checkpoints, including a pre-planning intent guard and a human-approval gate outside the reasoning loop. | Convergent on multi-checkpoint enforcement. Divergent: several of its checkpoints are prompt-level and therefore, in CROA's terms, advisory (Tenet T2) rather than structural. |
| **Conformance and maturity ladders** | Microsoft Agent Governance Toolkit governance maturity model (L0–L4, 2026); CAGE-1, arXiv:2607.03510; OWASP Agentic AI Governance Maturity Model (two-dimensional); CSA *Agentic AI Autonomy Levels and Control Framework* v2 (2026); AARM, arXiv:2602.09433. | **CROA's L0–L5 ladder is not novel as a ladder.** What distinguishes it is that it is a *conformance* regime: each rung carries executed-evidence requirements, L4 is a threshold with a normative claim-scope statement (§28.6), and a deployment without a populated evidence record must describe itself as "targeting L*n*", never "L*n*-conformant". Most adjacent ladders are maturity narratives; AARM is a conformance regime with two tiers. |
| **Deterministic governance as a framing** | Bhattarai & Vu, arXiv:2602.09947; Smith & McCarthy, *Deterministic governance for generative systems*, AI and Ethics 6, 394 (2026), DOI 10.1007/s43681-026-01172-6; and, in products, AWS Cedar / Verified Permissions and the Microsoft toolkit. | **Deterministic governance is not a CROA differentiator, and CROA does not claim it as one** (see `spec/properties.md` P-F). It is the field's consensus framing as of mid-2026. |

### 2.3 What is, and is not, differentiating

An honest reading of the above.

**No longer differentiating.** CROA asserts these but must not present them as distinguishing:
deterministic governance; execution-layer enforcement; complete mediation; model/authority
separation; signed single-use execution tokens; tamper-evident audit chains; trajectory monitoring
as an idea; the existence of a conformance or maturity ladder; the observation that a log proves
only what it recorded.

**Genuinely differentiating, on the evidence available:**

1. **Evaluability classes as a registered property of every invariant.** `E1` syntactic / `E2`
   static-decidable / `E3` semantic-approximated, with Rice's theorem stated as the reason `E3`
   exists, a directional false-positive-versus-false-negative discipline, `AMBIGUOUS` → fail-deny,
   and the measured ambiguity rate treated as a governed quantity. No surveyed work makes
   decidability a declared attribute of each individual invariant.
2. **The utility–guarantee frontier as an auditable design obligation** (Part I §2.7). CROA requires
   a deployment to *locate and record* the point at which narrowing the action surface stops being
   worth the capability it costs. No surveyed work treats that trade as a first-class recorded
   decision.
3. **Claim-scope discipline as a governance obligation.** The conditioned T1 statement, the §28.6
   "what L4 does and does not claim" list, and a Brand and Claims Usage Policy that makes stating
   the unconditioned claim a *governance* violation. No surveyed framework normatively binds its own
   claim wording.
4. **A trajectory profile registered per invariant**, with a conformance level (L4) that refuses
   windowed analysis alone wherever accumulation is possible.
5. **Atomic linearizable redemption mandated across every enforcement instance and every topology**,
   with a concurrent double-redemption conformance test — stronger than most surveyed work, though
   narrower than policy-state serializability (see `spec/properties.md` P-D).

**Composition is the weakest of CROA's claims to distinction.** "We compose known primitives into one
architecture" is hard to falsify and is a claim several of the works above could equally make. CROA
rests instead on the five items listed, on the conformance model, and on whatever the public review
produces — not on composition alone.

### 2.4 How to read this section

Names in this field collide and move. Two unrelated systems are called *AgentBound*; at least four
distinct artifacts are called *Aegis*; at least one system was renamed between preprint versions.
Citations above are therefore by author plus identifier. If a citation here is wrong, out of date, or
uncharitable to the work cited, please open an issue: misattribution in a related-work section is a
defect, and we will correct it.
