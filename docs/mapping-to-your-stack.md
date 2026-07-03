# CROA on your existing stack

**Objective:** map the seven CROA components (C1–C7) onto the enforcement tools an enterprise
**already owns** — OPA/Cedar, a service mesh, an API gateway, IAM, a SIEM, a CMDB — so an architect
can see how much of CROA is *composition of what they have* versus genuinely new build.
**Audience:** enterprise and security architects evaluating fit.
**Authoritative source:** Appendix O ("CROA and Adjacent Enforcement Mechanisms") and Part IV of the
specification. This page is a repo-accessible summary; where it and the spec differ, the spec governs.

---

## The one idea

CROA is **not another point control.** It is the architecture that *composes* the controls you already
run so that, within the modeled action space and under the registered invariants, an unsafe execution
path is **unreachable** rather than merely denied. Most of the mechanisms below are **components a CROA
deployment uses** — not competitors. The value CROA adds is the composition: a signed, single-use
execution commitment, cumulative trajectory evaluation, context grounding, and a tamper-evident
evidence chain, tied together under one policy authority.

## What you probably already have → which component it becomes

| You already run… | CROA role | What it gives you | What CROA adds around it |
|---|---|---|---|
| **OPA / Rego, AWS Cedar** (policy engine) | **C2** Execution Governor | Deterministic "is this request allowed?" against declarative policy | The decision is *advisory* until something makes it the only way to act. CROA compiles a permit into a signed commitment (C7) that the boundary (C6) alone will admit, adds trajectory (C4), context grounding (C3), and an evidence chain (C5). |
| **Service mesh / network policy / micro-segmentation** (Istio, Cilium, seccomp, microVMs) | Realizes **P4 / TB-3** (the execution boundary) | Bounds *blast radius*: what a workload can reach | Sandboxing answers "what can this process touch?" — not "is *this* action permitted, in *this* context, given the session?" CROA needs isolation to enforce P4; isolation needs CROA for per-action governance and evidence. Layers, not substitutes. |
| **API gateway** (Kong, Apigee, AWS API GW) | Hosts the **Agent Surface** + **C6** (DM-4) | A natural place to intercept and mediate agent traffic, especially for unmodifiable/legacy agents | The gateway must run the full `C2.eval` pipeline and admit only commitment-derived operations — not just native rate-limits/ACLs. |
| **IAM / workload identity** (OIDC, SPIFFE/SPIRE) | Feeds **Admission** (identity, RBAC, AQL) | Who is acting, and what they are eligible to submit | CROA consumes identity; it does not mint it. **Agent identity is an external, not-yet-standardized prerequisite** — see [`prerequisites.md`](prerequisites.md). |
| **SIEM / log pipeline** (Splunk, Elastic, Chronicle) | Consumes **C5** output | After-the-fact detection of patterns | CROA's C5 is *upstream* of the SIEM: an append-only, hash-chained, decision-level record that is a first-class, conformance-bearing artifact — not just logs. Your SIEM sees cumulative patterns after the fact; CROA's C4 **enforces** cumulative constraints in the control path. |
| **CMDB / service catalog** (ServiceNow) | Seeds the **Technical Golden Record** (C3) | The registry of legitimate endpoints/resources/entities | This is the framework's biggest practical dependency, and most CMDBs are incomplete. Read [`prerequisites.md`](prerequisites.md) before assuming C3 is "done." |
| **Agent platform tool scopes / MCP** | Hosts the **Agent Surface / RBAC** (DM-5) | Per-tool allow-lists and permission scopes | A scope says "this agent may call this tool." CROA additionally decides "may it perform *this* action, on *this* target, in *this* context, given the session, under enterprise invariants — and here is the signed, audited record." |
| **KMS / HSM** (CloudHSM, KMS, Vault, PKCS#11) | Custody of the **C1 & C7 signing keys** and the C5 WAL sealing key | Non-exportable key storage and signing | The keys are the trust root: CROA requires non-exportable custody, rotation/revocation, **m-of-n dual control** for high-consequence (R3/R4) authorizations, and keys held **off** the agent host (spec Part II §4.3.3, Appendix R Inv. 4). |
| **PAM / privileged-access broker** (CyberArk, BeyondTrust) | Governs the **break-glass / emergency-issuance** path into C1 | Brokered, recorded privileged access | PAM brokers *who may issue*; it does not replace the artifact's structural bounds. A governed exception is still single-use, time-bounded, and dual-controlled (§4.3.1) — incident response must never fall back to standing pre-issued authorizations. |
| **Human approval / change tickets** (ServiceNow, PagerDuty) | **Constrained Execution** (Governed Exception) | A person approves consequential actions | CROA subsumes and disciplines this: an override is a signed, scoped, single-use, audited authorization compiled into the commitment — it cannot silently widen scope or be applied out of band. (Watch the exception *rate* — see [`operating-c5.md`](operating-c5.md) and research question RQ-14.) |
| **Runtime guardrails** (NeMo, LLM-judge, classifiers) | Advisory pre-classifier **outside** the control plane | Probabilistic input/output filtering | Model-layer and bypassable under pressure (Technical Sycophancy). Complementary, never primary: a guardrail's output must be reduced to a deterministic verdict before it reaches C2. |

## So how much is new build?

If you already run a policy engine, a mesh/network-policy layer, an IAM, and a SIEM, then **C2, P4,
Admission, and the C5 sink are largely things you own.** The genuinely CROA-specific build is:

1. **C7 — the Compiled Commitment** and **C6 — the boundary that admits only commitments.** This is the
   structural core: it turns a "deny" from advice into an impossibility. (The [reference harness](https://github.com/croa-project/croa-reference-harness) demonstrates the whole C3→C2→C7→C6→C5 gauntlet in ~300 lines of dependency-free Python — the C6/C7 enforcement logic itself is a few dozen of them.)
2. **C3 — context grounding against the Technical Golden Record.** Cheap to wire, expensive to make
   *complete* — the real cost centre (see prerequisites).
3. **C4 — trajectory / cumulative-constraint enforcement.** The capability nothing in a stateless
   gateway or an after-the-fact SIEM gives you.
4. **C5 as a conformance-bearing ledger** (not just logs) — with the operational commitments that
   implies ([`operating-c5.md`](operating-c5.md)).

## "Isn't this just OPA in front of my tools?"

OPA (or Cedar) is **one of seven components**. CROA additionally grounds the action in real context
(C3), watches the session for path-composition (C4), compiles every permitted action into the only
signed artifact allowed to execute (C7 + C6), and records every decision in a tamper-evident,
conformance-bearing ledger (C5) — so the unsafe path is not merely *denied*, it is *unreachable*
within the modeled action space. The point controls are the parts; CROA is the architecture that makes
the guarantee structural.

→ Next: the [deployment topologies](deployment-topologies.md) (where each component physically runs), the
[operational requirements of C5](operating-c5.md), and the [external prerequisites](prerequisites.md).
For the authoritative treatment, see **Appendix O** and **Part IV** in the [specification](../spec/README.md).
