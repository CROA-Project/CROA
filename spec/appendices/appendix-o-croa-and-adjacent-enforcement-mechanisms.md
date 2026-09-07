---
tags:
  - croa_foundation
---

# Appendix O — CROA and Adjacent Enforcement Mechanisms

**CROA Framework v1.0.1.1 · Informative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The
>
## O.1 The question

CROA's maturity model (Part I §1.2; Part VI §28.2) classifies refusal-based and reactive-enforcement controls below the L4 conformance threshold. That is a strong claim about a crowded field, and it deserves a direct comparison. The mechanisms below are **not** competitors to be dismissed — most are *components a CROA deployment uses*. The distinction is architectural: CROA is not another point control; it is the architecture that composes controls so that **unsafe execution paths are unreachable within the modeled action space, under the registered invariant set, given network-enforced containment** (the conditioned T1 claim, Part I §3). The comparison clarifies what that composition adds over each mechanism alone.

## O.2 Mechanism-by-mechanism

### Policy engines — OPA/Rego, AWS Cedar

A policy engine answers "is this request allowed?" deterministically against declarative policy. This is exactly what `C2.eval` needs, and **OPA or Cedar is a natural implementation of `C2`** (already noted as an adjacent technology in the CROA overview). What a policy engine alone does **not** provide:

- a **compiled, content-addressed, signed execution commitment** that is the *only* thing allowed across the execution boundary (`C7` ECC + `C6` firewall). A bare policy decision is advisory unless something structurally prevents the agent from acting on a "deny"; CROA makes the ECC the sole unit of execution.
- **trajectory/path-composition** evaluation across a session (`C4`, TH-7): policy engines decide single requests, not sequences converging on a violation.
- **context grounding** (`C3`): a policy engine evaluates the request as presented; it does not verify that referenced entities exist in the system of record.
- a **tamper-evident evidence chain** as a first-class, conformance-bearing artifact (`C5`, I3/I6).

"OPA in front of my tools" is roughly **L2–L3** in CROA terms: real enforcement of single decisions, but the unsafe path remains architecturally available (nothing compiles the decision into the only executable artifact, nothing watches sequences, nothing guarantees the audit chain). CROA = (a policy engine like OPA as `C2`) + `C3` + `C4` + `C7` + `C6` + `C5`, composed under invariants I1–I8.

### Runtime guardrails — NeMo Guardrails, LLM-judge filters, prompt/output classifiers

Guardrails inspect model inputs/outputs and block or rewrite them, often using another model. They are **probabilistic and model-layer** by construction. In CROA terms they are **L2 (refusal-based)**: bypassable under adversarial pressure, jailbreaks, or Technical Sycophancy, because the unsafe action remains reachable if the classifier is fooled. CROA's stance (T2) is that such controls are complementary, never primary: a guardrail may run as an advisory pre-classifier *outside* the control plane, but its output must be reduced to a deterministic verdict before it reaches `C2` (Part I §2.6). The difference is structural vs. behavioral enforcement.

### Sandboxing / isolation — containers, microVMs, seccomp, network policy

Sandboxing bounds the *blast radius* of execution (what a process can touch). It is **essential and complementary**: CROA's network-enforced execution-boundary containment (P4, TB-3) is typically *realized* by isolation and network policy. But sandboxing answers "what can this process reach?" not "is this specific governed action permitted under enterprise invariants, in this context, given the session so far?" Sandboxing without CROA gives coarse, static bounds and no per-action evidence; CROA without isolation has no way to enforce P4. They are layers, not substitutes — CROA assumes sandboxing/network enforcement as part of P4 and adds the per-action governance and evidence on top.

### Transactional human approval — change tickets, "human in the loop" gates

Human-approval gates insert a person before consequential actions. CROA **subsumes and disciplines** this pattern: a human override is a *governed request for authorization* (Constrained Execution Mode, §4.3.1) — signed, scoped, bounded, compiled into the ECC, and recorded in `C5`. The difference from a typical approval workflow: the approval cannot silently widen scope, cannot be applied out of band, and leaves tamper-evident evidence; and it does not become a bottleneck on low-consequence actions, which flow through structural governance without human gating (consequence-class tiering, Appendix K).

### Agentic-platform capabilities — tool allow-lists, scopes, per-tool permissions (incl. MCP)

Modern agent platforms and protocols (e.g., MCP, framework-level tool scopes) provide per-tool allow-lists and permission scopes. These are an **admission control surface** — close to CROA's RBAC eligibility (§4.9.1) and a natural place to host the Agent Surface in a platform deployment (DM-5; see Part IV §23 and §O.3). What they typically lack: invariant evaluation against enterprise policy, trajectory analysis, context grounding, a compiled execution commitment, and a conformance-bearing evidence chain. A tool scope says "this agent may call this tool"; CROA additionally decides "may it perform *this* action, on *this* target, in *this* context, given the session, under enterprise invariants — and here is the signed, audited record." Platform capabilities are where CROA integrates, not what it replaces.

## O.3 Summary table

| Mechanism | What it does | CROA maturity analog | Relationship to CROA |
|---|---|---|---|
| OPA / Cedar | Deterministic single-request authorization | L2–L3 (as a control) | **Implements `C2`**; CROA adds `C3`,`C4`,`C7`,`C6`,`C5` |
| Runtime guardrails (NeMo, LLM-judge) | Probabilistic input/output filtering | L2 (refusal-based) | Advisory only; outside the control plane (T2) |
| Sandboxing / network policy | Bounds execution blast radius | (enabler of P4) | **Realizes P4/TB-3**; complementary layer |
| Human-approval gates | Person approves consequential actions | (control pattern) | **Subsumed** as signed Constrained Execution (§4.3.1) |
| Platform tool scopes / MCP | Per-tool allow-list / permissions | L1–L3 (admission) | **Hosts the Agent Surface / RBAC**; CROA adds the OCP |

## O.4 Infrastructure column — the assets you already own

The mechanisms above are enforcement *controls*. The table below maps CROA components onto the concrete **infrastructure** an enterprise typically already runs — the column an architect needs for a gap analysis (which asset plays which C-role, and what CROA still requires beyond it).

| Existing infrastructure | CROA role it can play | What CROA still requires on top |
|---|---|---|
| **API gateway** (Kong, Apigee, AWS API GW, NGINX) | Hosts the **Agent Surface** and, in DM-4, the `C2` pipeline + **`C6`** boundary | Must run the full `C2.eval` (not native ACLs only) and admit **only** ECC-derived operations; horizontally scaled gateways MUST share one linearizable ECC/auth **redemption authority** (§4.8) — a per-gateway registry is non-conformant |
| **Service mesh** (Istio, Linkerd, Cilium) | Realizes **P4/TB-3**; carries the DM-3 sidecar `C6`/`C2` | mTLS/identity ≠ governance; the mesh enforces *where* traffic flows, CROA enforces *whether this action* may proceed and records evidence |
| **SIEM / log lake** (Splunk, Elastic, Chronicle) | *Downstream consumer* of **`C5`**, and the home of exception-rate / TRAJECTORY_ALERT dashboards | Not a substitute for `C5`: `C5` is the upstream append-only, hash-chained, **conformance-bearing** ledger; the SIEM indexes it, it does not replace its integrity or its position on the fail-closed path |
| **KMS / HSM** (CloudHSM, KMS, Vault, PKCS#11) | **Custody of the `C1` and `C7` signing keys** and the `C5` WAL sealing key | Non-exportable keys, m-of-n dual control for R3/R4 authorizations, rotation/revocation, and keys held **off** the agent host (Part II §4.3.3; Appendix R Inv. 4) |
| **PAM / secrets & session broker** (CyberArk, BeyondTrust, Vault) | Governs the **human-approval / emergency-issuance** path into `C1` (Constrained Execution) | The break-glass path MUST still produce a single-use, bounded, dual-controlled authorization artifact (§4.3.1) — PAM brokers *access to issue*, it does not replace the artifact's structural bounds |
| **IAM / workload identity** (OIDC, SPIFFE/SPIRE) | Feeds **Admission** (subject identity, RBAC eligibility) | Agent identity is an external prerequisite CROA consumes, not mints (see §O.5) |

## O.5 IAM and agent identity — an external prerequisite to profile against

CROA postulates an *authenticated subject identity* at admission but does not, in v1.0.1, architect how that identity is established. This is a real external dependency, and an enterprise IAM team will reject any framework that treats it as solved. The spec's position is explicit:

- **Agent identity is consumed, not minted.** CROA requires that the acting agent be identifiable at TB-1; it does not define the identity system. Deployments SHOULD bind agent identity to an established **workload-identity** standard — **SPIFFE/SPIRE** (SVIDs) is the RECOMMENDED profile for service-to-service agent identity — and MUST document the delegation and impersonation-resistance properties of whatever primitive they use.
- **Delegation tokens SHOULD profile against a standard, not reinvent one.** The delegation mechanism of Appendix L (scope-narrowing across agent-to-agent hops) is, in protocol terms, a token-exchange problem. Implementations SHOULD profile it against **OAuth 2.0 Token Exchange (RFC 8693)** — modeling a delegated authorization as an exchanged token whose scope is monotonically narrowing — rather than defining a bespoke token. CROA adds the requirement that every exchange is bounded, single-use where it authorizes an exception, and recorded in `C5`.
- **Key custody is part of identity.** The custody of `C1`/`C7` signing keys (Part II §4.3.3) is the trust root that makes an authenticated identity *actionable*; identity and key-management are specified together, not separately.

This is flagged as an open external dependency (see the public-review research questions on identity and delegation). Convergence of agent-identity standards strengthens CROA's admission stage for free; the guarantee is only ever as strong as the identity feeding it.

## O.6 The one-sentence answer

*"More than OPA in front of my tools"* = OPA (or Cedar) is one of seven components; CROA additionally grounds the action in real context (`C3`), watches the session for path-composition (`C4`), compiles every permitted action into the only signed artifact allowed to execute (`C7`+`C6`), and records every decision in a tamper-evident, conformance-bearing ledger (`C5`) — so that the unsafe path is not merely *denied*, it is *unreachable* within the modeled action space. The point controls above are the parts; CROA is the architecture that makes the guarantee structural.

Cross-reference: maturity model (Part VI §28.2); conditioned T1 claim and L4 claim-scope (Part I, Chapter 3, Tenet T1; Part VI §28.6); deployment models incl. platform DM-5 (Part IV).

---

## O.7 Research prior art — foundations, contemporary work, and what is no longer differentiating

*Informative.* Sections O.1–O.6 compare CROA to the engineering mechanisms a deployment composes.
This section compares it to the **literature**. It exists because a framework published into an
active research field without a related-work section is not reviewable, and because several
properties CROA states are, by mid-2026, the field's shared ground rather than CROA's distinguishing
features. Naming them as such is a claims-hygiene obligation (Part VII §33.7), not modesty.

This section is maintained on a best-effort basis and is certainly incomplete. The
repository copy — `docs/prior-art.md` §2 — carries the current version with full citations, is
correctable by pull request, and governs where the two differ in detail.

### O.7.0 CROA's own dated record

Dates matter in a related-work section, and a section that omits them concedes priority by default.

- **CROA Framework: Deterministic AI Governance and Mitigation of Technical Sycophancy** — Durand & Smith, working paper, DOI `10.5281/zenodo.19846872`, **submitted 27 April 2026, published 28 April 2026**, CC BY 4.0, OpenAIRE-indexed. Introduces **Technical Sycophancy** and **Agentic Sprawl** as named failure modes, models agentic execution as a **constrained state-transition system** with actions conditioned on pre-validated invariants and validated transitions formalised into contracts before execution, and states the central thesis verbatim: *"unsafe transitions are not merely rejected at runtime; they are excluded from the executable state space by construction."* It describes the earlier four-layer architecture under the name *Cognitive RFC Orchestration Architecture*.
- **CROA v1.0.1 Official Specification** — DOI `10.5281/zenodo.21063423`, **July 2026**. The seven-component control plane, the invariants, the evaluability classes, the trajectory profiles, the conformance levels, and the conditioned T1 claim.

**Which record a given claim dates from matters, and this framework should be precise about it.** The April 2026 paper establishes priority for the *thesis* and for two named failure modes. It does **not** date the v1.0.1 machinery: `C1`–`C7`, `I1`–`I8`, `E1`/`E2`/`E3`, the `TP-*` profiles and `L0`–`L5` are July 2026 and are to be dated as such.

Relative to 28 April 2026, the contemporary literature divides three ways. **Preceding it** — and therefore beyond any priority claim: the FSE AgentBound (arXiv October 2025), LATTICE (received at *Frontiers* 30 January 2026, published August 2026 — submission is what counts), Trinity and AARM (February 2026), *Policies on Paths* (17 March 2026), the Aegis architecture (March 2026), and every classical foundation in §O.7.1. **Concurrent to the day and independent:** RiskGate (arXiv 27 April 2026). **Following it:** certificate-gated execution (May 2026), IBM CUGA (May 2026), proof-carrying agent actions (September 3, 2026), the eBay AgentBound (September 3, 2026), CAGE-1 and CAVA (July 2026), trajectory assurance and policy-state serializability (3 August 2026), APV (6 August 2026), composed stateful gates and per-decision evidence protocols (August 2026).

Where CROA and a later work share a framing, CROA's record is the earlier one. That is a statement about dates and nothing more: it carries no implication that the later work derived from CROA, and independent convergence should be assumed in this field absent evidence to the contrary. Nor does priority make a claim novel — several works that *precede* CROA occupy ground CROA also occupies, and no filing date changes that.

### O.7.1 Foundations CROA stands on

CROA claims no novelty for any of the following, and a reviewer should read CROA's claims against
them:

- **Complete mediation and the reference monitor** — Anderson (ESD-TR-73-51, 1972); Saltzer &
  Schroeder (1975). CROA's execution boundary (I1, P4, TB-3) is a reference monitor.
- **The theoretical ceiling on runtime enforcement** — Schneider, *Enforceable Security Policies*
  (ACM TISSEC 3(1), 2000); Hamlen, Morrisett & Schneider (ACM TOPLAS 28(1), 2006); Ligatti, Bauer &
  Walker on edit automata (IJIS 4(1–2), 2005). The conditioned T1 claim should be assessed against
  this characterization.
- **Mediation proved rather than asserted** — seL4 (SOSP 2009; ITP 2011). CROA does not meet this
  bar and does not claim to: its guarantee is a conformance finding about a deployment, not a
  machine-checked proof (see the note in Part I §2.5).
- **Nominal permission versus effective authority, and attenuation** — Miller, *Robust Composition*
  (2006); Shapiro & Weber (IEEE S&P 2000); Sandhu, *The Schematic Protection Model* (JACM 35(2),
  1988). This is the ancestry of Invariant I8 (Part II §5.9).
- **One-way attenuating credentials** — macaroons (NDSS 2014); SPKI/SDSI chain discovery (JCS 9(4),
  2001); Delegation Logic (ACM TISSEC 6(1), 2003); RFC 8693, already cited in §O.5. A Compiled
  Commitment is structurally a per-action attenuated capability carrying an audit obligation.
- **Safety and reachability analysis over authority states** — Harrison, Ruzzo & Ullman (CACM 19(8),
  1976), whose undecidability result is the reason CROA scopes reachability to a *registered
  invariant set over a modeled action space* rather than to an unbounded state space.
- **Tamper-evident logging and its limits** — Haber & Stornetta (1991) and Crosby & Wallach (2009),
  both already in Part I §1.6.3; RFC 9162, whose consistency proofs establish append-only-ness but
  **not** receipt of everything issued; Amir-Mohammadian, Chong & Skalka (POST 2016) on provably
  correct audit instrumentation; Haeberlen et al., *PeerReview* (SOSP 2007) on detection scoped to
  observable behaviour. These are why the framework's evidence property is decision
  *reconstructability* (I3) and not evidence *completeness*.

### O.7.2 Contemporary work on runtime governance of agentic systems

A body of work published during 2025–2026 addresses the same surface. The relationship is in most
cases **independent convergence**, not derivation in either direction. The most consequential for a
reviewer are: governance-plane/operational-plane separation with a non-bypassable execution gate and
an asserted governance-invariance property; the formalization of governance as deterministic policy
functions over an execution *path* rather than over isolated actions; the position that individually
permitted actions can collectively violate a state-conditioned invariant; the formalization of
*stale authorization* and a serializability condition requiring committed effects to be authorized
against the policy state immediately before they occur; certificate-gated execution architectures in
which an action may not execute without a certificate produced by a prior certification step —
structurally the closest published analogue of the `C7`/`C6` pair and the Execution Change Contract, and
the comparison a reviewer will reach for first; the composition of stateful pre-action controls;
proof-carrying agent actions; permission manifests with container- and network-level default-deny
enforcement for tool servers; vendor-neutral per-decision runtime evidence
records that declare what they do and do not cover; the treatment of *effective authority* as a
persistent, task-conditioned object distinct from nominal permission; and empirical work
demonstrating cumulative resource abuse across agent trajectories. Full citations are in
`docs/prior-art.md` §2.2.

Two consequences for this framework are recorded normatively elsewhere:

1. The concurrency requirement added to §4.6.3 for cumulative (`TP-C`/`TP-X`) aggregates responds to
   the stale-authorization line of work. CROA closes the cumulative case and explicitly does **not**
   claim the general serializability property; it does not adopt that work's terminology.
2. CROA's four machine-readable schemas are its own event model and are **not** proposed as a
   general evidence standard. Where a vendor-neutral per-decision evidence format exists, mapping a
   `C5` event onto it is preferable to inventing a competing one.

### O.7.3 What is, and is not, differentiating

**No longer differentiating.** CROA asserts each of the following and MUST NOT present any of them
as a distinguishing feature: deterministic governance; execution-layer enforcement; complete
mediation; model/authority separation; signed single-use execution tokens; tamper-evident audit
chains; trajectory monitoring as an idea; the existence of a conformance or maturity ladder; and the
observation that an audit log evidences only what it recorded.

**Differentiating, so far as this survey reaches.** Five things, none of which is a new point
mechanism. Each is a negative statement over a survey this section already declares incomplete, so
each is phrased as *we are not aware of*, never as *no work does*. A counterexample to any of them is
a correction the project wants:

1. **Evaluability as a registered property of every invariant** (Part I §2.6) — E1/E2/E3, with Rice's
   theorem as the reason E3 exists, a directional false-positive-versus-false-negative discipline,
   `AMBIGUOUS` → fail-deny, and the measured ambiguity rate treated as a governed quantity. No
   are not aware of other work that makes decidability a declared attribute of each individual
   invariant.
2. **The utility–guarantee frontier as an auditable design obligation** (Part I §2.7) — the
   requirement to locate and record the point at which narrowing the action surface stops being
   worth the capability it costs. We are not aware of other work that treats that trade as a
   first-class recorded decision.
3. **Claim-scope discipline as a governance obligation** — the conditioned T1 statement, the §28.6
   "what L4 does and does not claim" list, and the Brand and Claims Usage Policy (§33.7) that makes
   stating the unconditioned claim a governance violation. We are not aware of another framework
   that normatively binds its own claim wording.
4. **A trajectory profile registered per invariant** (§4.6.3), with an L4 rule that refuses windowed
   analysis alone wherever accumulation is possible.
5. **Atomic linearizable redemption mandated across every enforcement instance and topology**
   (§4.8), with a concurrent double-redemption conformance test (NT-007) — narrower than general
   policy-state serializability, and stronger than most surveyed work.

**A caution about the composition argument.** "CROA composes known primitives into one architecture
with a reproducible evidence model" (Part I §1.5) remains true, but it is a weak claim to
distinction: it is hard to falsify, and several of the works above could make it equally. CROA's
case rests on the five items listed, on the conformance model, and on what public review produces —
not on composition alone.

---

*End of Appendix O — CROA and Adjacent Enforcement Mechanisms.*
