<!--
  CROA — README (repository front door)
  Audience: enterprise architects, AI engineers, CTOs, security & governance leaders, researchers.
  This file is the first thing a visitor sees. It must establish, in under a minute, that CROA is a
  serious, falsifiable, vendor-neutral architectural hypothesis currently open for public validation.
-->

# CROA — Constrained Reachability Orchestration Architecture

**A vendor-neutral architecture framework for the governed execution of agentic AI systems.**

> **Status: Public Review Draft (v1.0).** CROA is an open architectural hypothesis published for the community to **test, challenge, and improve**. It is *not* a finished or formally recognized standard. We are asking practitioners to try to break it — and to tell us what they find.

---

## The problem

AI systems are moving from advisory tools to **operational actors** that read, write, call, and change real enterprise systems. That shift creates a class of risk that model-level alignment does not address:

- **Agentic sprawl** — many autonomous agents acting across many systems, with no common control point.
- **Execution ambiguity** — the gap between what a policy *says* and what an agent *does* under pressure.
- **Technical Sycophancy** — the tendency of an agent to reinterpret a constraint in order to satisfy its objective.
- **Auditability gaps** — no tamper-evident record of *why* an action was permitted.

Most current answers operate at the level of *model behavior* — better prompts, better training, runtime guardrails that **discourage** unsafe actions. A discouraged action is still a reachable action.

## The claim (and we want you to test it)

CROA moves governance from model behavior to the **execution layer**, and states its central claim precisely and conditionally:

> Within the **modeled action space**, under the **registered invariant set**, and given **network-enforced execution-boundary containment**, an agent **cannot, by its own choice, reach a state that violates a registered invariant** — such execution paths are **structurally unreachable**.

The one deliberate exception is a **Governed Exception**: a signed, time-bounded, single-use authorization issued by the policy authority — never by the agent — and recorded in the audit trail.

The three conditions are not hedges; they are the scope within which the claim is meant to hold. Outside that scope, CROA makes no claim. **Our request to the community is simple: find the conditions under which this claim fails.** Open a discussion under *Challenge the Claim*, or file a finding.

## What CROA is — and is not

| CROA **is** | CROA is **not** |
|---|---|
| An execution-layer governance architecture | A prompt-engineering method |
| A reference architecture (logical components C1–C7, trust boundaries, an audit model) | A "Responsible AI" manifesto or ethics framework |
| A conformance model (levels L0–L5) for *deployed systems* | A product, an SDK, or a chatbot |
| Vendor-neutral and implementation-agnostic | Tied to any company or commercial tool |

A one-page architectural overview is in [`docs/architecture-overview.md`](docs/architecture-overview.md); the full reasoning is in [`docs/why-croa.md`](docs/why-croa.md).

## What is, and is not, distinctive

Several things CROA does are not distinctive, and we say so rather than let a reader infer otherwise:
deterministic governance, execution-layer enforcement, complete mediation, signed single-use
execution tokens, tamper-evident audit chains, trajectory monitoring as an idea, and the existence of
a conformance ladder are all established elsewhere — in classical security literature and in a dense
body of 2025–2026 work on agentic runtime governance. [`docs/prior-art.md`](docs/prior-art.md) §2
names that work, with citations, and states where CROA overlaps with it, where CROA arrived
independently at the same idea, and where CROA is genuinely doing something the surveyed work is not.

The claim-bearing properties, each written so it can be attacked — claim, preconditions, invariant,
enforcement, falsifying test, evidence produced, and what it does **not** establish — are in
[`spec/properties.md`](spec/properties.md). The properties CROA does *not* have are listed in the same
file, and the honest state of its evidence base is in [`docs/limitations.md`](docs/limitations.md).

## Vendor neutrality

CROA is **vendor-neutral and implementation-agnostic**. Conformance to CROA never requires, and never will require, any particular product.

A vendor-neutral **Minimal Reference Harness** ([`croa-reference-harness`](https://github.com/croa-project/croa-reference-harness)) lets anyone run the architecture's enforcement behavior and inspect the resulting audit log on their own machine, using no commercial software.

CROA's independence from any commercial product is a governance commitment, recorded in [`GOVERNANCE.md`](GOVERNANCE.md). Anyone may build a CROA implementation; none is privileged, official, or required.

## For architects evaluating fit

CROA is a *logical* architecture; these pages connect it to what you already run, and name its real
costs and dependencies honestly:

- [**CROA on your existing stack**](docs/mapping-to-your-stack.md) — how C1–C7 map onto OPA/Cedar, a service mesh, an API gateway, IAM, your SIEM, and your CMDB. What's composition of what you have vs. genuinely new build.
- [**Deployment topologies**](docs/deployment-topologies.md) — the five reference deployment models (centralized, federated, sidecar/mesh, gateway-mediated, embedded) and where each component physically runs.
- [**Operating C5**](docs/operating-c5.md) — the operational consequence of fail-closed: the audit store is tier-0 infrastructure. SLA, sizing, degraded-mode.
- [**External prerequisites**](docs/prerequisites.md) — the load-bearing dependencies CROA consumes but doesn't provide: agent identity (still unstandardized) and a sufficiently complete Technical Golden Record.
- [**Prior art & related work**](docs/prior-art.md) — where CROA sits relative to OPA/Cedar, capability systems, service meshes, guardrails, human-approval gates, and SIEMs: what it borrows, what it adds, what it doesn't replace.

Adoption is deliberately **low-regret**: because CROA is an architecture, not a product, trying it leaves you with a network boundary, an endpoint registry, and a tamper-evident audit trail — assets with standalone value even if you walk away ([why-croa.md](docs/why-croa.md#adopting-croa-is-low-regret)).

## How to engage

You don't need permission, and your first contribution doesn't have to be code.

1. **Read the claim.** Start with [`docs/architecture-overview.md`](docs/architecture-overview.md) (1 page). The full specification is on Zenodo — see [`spec/README.md`](spec/README.md) for the citable DOI.
2. **Run the demonstrator.** Clone the [reference harness](https://github.com/croa-project/croa-reference-harness), run four of the reference negative tests, and read the `C5` event log it produces. It is a self-contained mock — a way to see the mechanism, not evidence that the properties hold. ([`docs/quick-start.md`](docs/quick-start.md), ≤15 minutes.)
3. **Tell us what you found.**
   - Think the central claim is wrong? → **Discussions → Challenge the Claim**
   - Implemented CROA, in whole or in part? → submit an evidence report ([`evidence/README.md`](evidence/README.md)) — **including implementations that failed.**
   - Found an ambiguity or a conformance gap? → open an Issue (templates provided).
   - Want to propose a change to the framework? → the [RFC process](rfcs/README.md).
4. **Go deeper.** Join the [Public Review Program](public-review/README.md) as a reviewer, or the [Pilot Program](public-review/pilot-program.md) as an implementer.

The questions we most want answered are listed openly in [`public-review/research-questions.md`](public-review/research-questions.md).

## Project status & governance

- **Phase:** Public Review. CROA is stewarded by its founding maintainers during this phase.
- **Direction of travel:** an independent, vendor-neutral foundation — established once the project has demonstrated sufficient community adoption and governance maturity, not before. The progression and its gates are in [`GOVERNANCE.md`](GOVERNANCE.md) and [`ROADMAP.md`](ROADMAP.md).
- **How decisions are made:** in the open, through the [RFC process](rfcs/README.md). Changes are classified by impact (editorial → extension).
- **Code of conduct:** [Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

## License

- **Specification and documentation:** Creative Commons Attribution 4.0 International (**CC BY 4.0**).
- **Code and machine-readable artifacts** (reference harness, JSON schemas): **Apache License 2.0**.

Implementing CROA requires no license, fee, or commercial program. Use it, build on it, cite it, and challenge it.

## Citing CROA

Cite as: *The CROA Project. CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution. Public Review Draft, Version 1.0, 2026.* Canonical DOI: [10.5281/zenodo.21063423](https://doi.org/10.5281/zenodo.21063423) · Zenodo record: <https://zenodo.org/records/21063423> (see [`spec/README.md`](spec/README.md) for versioning guidance).

---

*CROA is published for public validation. The fastest way to help is to try to prove it wrong.*
