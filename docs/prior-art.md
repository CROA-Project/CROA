# Prior art and related work

**Objective:** place CROA honestly among the mechanisms it is often compared to, and say precisely what
it borrows, what it adds, and where it does *not* compete.
**Audience:** architects and reviewers who already know this space.
**Authoritative source:** Appendix O of the specification ("CROA and Adjacent Enforcement Mechanisms").
This page is a repo-accessible summary; where it and the spec differ, the spec governs.

---

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
