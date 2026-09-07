---
tags:
  - croa_foundation
---

# Appendix K — CROA Core: A Risk-Proportionate Adoption Profile

**CROA Framework v1.0.1.1 · Normative (profile, per Part VII §33.3).** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The 
## K.1 Problem and design rule

The framework's conformance model is deliberately binary: L4 is achieved for the *entire stated governance boundary* or not at all (Part VI §28.3–§28.4). That is correct for the claim "CROA-conformant," but it gives an organization no graded path and no way to spend governance effort in proportion to risk. CROA Core addresses this **without** weakening the conformance model, by using two levers the framework already provides:

1. **Scope narrowing.** A profile MAY restrict the governance boundary (Part VII §33.3). CROA Core conformance is claimed over a *declared, narrow* boundary, not the whole estate.
2. **Method tiering by consequence class.** The reversibility/consequence classes R0–R4 (Part I T5) already fix the *minimum authorization and evidence* per action. CROA Core extends them to also modulate the *evaluation method depth* required (horizon, evaluability class, analyzer rigor) — heavy method where consequences are high, light method where they are low.

**Design rule (normative for this profile).** CROA Core MUST NOT be used to claim CROA conformance for actions outside its declared boundary, and MUST NOT lower any requirement that applies *within* its declared boundary. Anything less than full seven-component coverage of the boundary is an adoption status, not a conformance level.

## K.2 The two tiers

### Tier 0 — CROA Core On-Ramp (adoption status, NOT conformant)

A first deployment of the six components that deliver the most structural risk reduction per unit of effort:

- `C1` Policy Authority, `C2` Execution Governor, `C3` Path Resolver, `C7` Contract Compiler, `C6` Execution Firewall, `C5` Audit and Provenance Store.

`C3` is included because it is **structurally required wherever an ECC is compiled**: an ECC's `ecc.action` is, by schema (Part II §4.4.1, `ecc.schema.json`), a grounded governed action with `gga.semantic_result = GROUNDED`, which only `C3` can produce — so a deployment that compiles ECCs at all cannot omit `C3`. Tier 0 therefore omits exactly one OCP component: `C4` (trajectory analysis). This already yields the two properties that distinguish CROA from refusal-based guardrails: **only `C7`-compiled, `C6`-validated ECC-derived operations reach governed systems** (execution-boundary enforcement, I1/P4), and **every decision is durably recorded** (I3/I6), with context grounding and Corrective Reframing available via `C3`. It is the right first build.

**It is explicitly non-conformant.** Without `C4` (trajectory analysis) there is no protection against path-composition and trajectory attacks (TH-7, T8), and trajectory detection is a requirement of L4 (Part VI §28.2); a Tier 0 deployment has also not yet established the full L3/L4 boundary discipline. A Tier 0 deployment therefore:

- MUST be described only with an adoption status (Part VI §28.5) — typically **"CROA-aligned"** or **"Targeting L4"** — and MUST NOT be described as "CROA-conformant" or as meeting any L*n* level;
- MUST record the absent `C4` guarantee and the resulting residuals (TH-7, trajectory-based invariant violation) in the Residual Risk Register (C-24);
- SHOULD publish a dated plan to reach Tier 1 (add `C4` and the full method) for the boundary.

### Tier 1 — CROA Core Conformant (L3 or L4 over a narrow boundary)

All **seven** components (`C1`–`C7`) are present — as required for any conformance level (Part II §4.2) — but applied to a **declared narrow governance boundary**: a named, minimal set of agents and action types, with the invariant registry restricted to that boundary. Within that boundary the deployment satisfies every requirement of the level it claims:

- **CROA Core L3** — the full OCP enforces the boundary with reactive enforcement and complete evidence, but the enterprise does not yet claim the full constructive-enforcement assurance of L4 (e.g., trajectory horizon is minimal, or the AQL is not yet in place for agent subjects). Claimable on Chapter 29 evidence as **L3 for the declared boundary**.
- **CROA Core L4** — full L4 (Part VI §28.2) for the declared narrow boundary, including the recommended AQL for agent subjects (SHOULD at L4 — a CROA Core deployment is encouraged to enforce it within its narrow boundary even though L4 does not require it). This is a genuine "CROA-conformant" claim, but its scope is the narrow boundary and MUST be stated as such ("L4 conformant for boundary B"), never generalized to the estate.

A Tier-1 claim is faithful to §33.3 because it adds requirements (a defined minimal-but-complete registry for B) and narrows scope; it relaxes nothing that applies within B.

## K.3 Method tiering by consequence class

CROA Core sets, per consequence class, the *minimum method depth* an invariant's evaluation and trajectory analysis MUST use. Higher classes pull in heavier method; lower classes are kept cheap so the profile stays adoptable. (Evaluability classes E1/E2/E3 are defined in Part I §2.6; C4 patterns A–D in Appendix I; horizon *h* in Part II §4.6.2. The reversibility/consequence classes R0–R4 are defined **normatively and solely** in Part I T5 — R0 fully reversible, R1 compensatable, R2 irreversible/low-impact, R3 irreversible/high-impact, R4 irreversible/critical — and are not redefined here; this table only sets the minimum method depth per class.)

| Consequence class | Min. invariant evaluability rigor | C4 trajectory requirement | Authorization (from T5) | Evidence |
|---|---|---|---|---|
| **R0–R1** (fully reversible / compensatable) | E1 attribute checks sufficient | Counters/automaton (Pattern A/B) optional | Standard permit | Standard `C5` record |
| **R2** (irreversible, low-impact) | E1/E2 required | Pattern A/B required where trajectory-relevant | Standard permit | Standard `C5` record |
| **R3** (irreversible, high-impact) | E2 required; E3 only with declared residual + measured AMBIGUOUS rate | Horizon *h* ≥ default; Pattern B/C for coupled invariants | Elevated authorization (T5) | Enhanced evidence; reviewer sign-off |
| **R4** (irreversible, critical) | E1/E2 only; an R4 hazard reachable only via an E3 (approximated) invariant MUST be removed from the action surface or escalated to human authorization | Extended horizon; Pattern C; no reliance on Pattern D over-approximation alone | Highest authorization class (T5, R4); signed exception | Maximal evidence; independent review |

The rule of thumb the table encodes: **never let a high-consequence guarantee rest on an approximation.** If an R4 hazard can only be caught by an E3 (best-effort) invariant, the correct move is to constrain the action surface so the hazard leaves the modeled action space (Part III §7.2 Step 5), or to route the action to human authorization — not to accept a bounded residual at R4.

## K.4 What CROA Core does for adoption

- It gives a **defensible first build** (Tier 0) that is honest about not being conformant.
- It gives a **graded conformance claim** (Tier 1, L3 then L4) scoped to a boundary an organization can actually evidence, instead of an all-or-nothing estate-wide L4.
- It makes governance effort **proportional to consequence** (§K.3), aligning CROA with the risk-based posture of the EU AI Act and ISO 31000 (see Appendix M) while keeping the conformance model intact.
- It preserves the integrity of the "CROA-conformant" label by forbidding its use for Tier 0 or for actions outside the declared boundary.

## K.5 Relationship to the rest of the framework

CROA Core is a profile under Part VII §33.3 and is registered there. Its tiers map onto the conformance levels and adoption statuses of Part VI §28.2/§28.5; its method tiering builds on the consequence classes of Part I T5, the evaluability classes of Part I §2.6, and the C4 patterns of Appendix I. It changes no normative requirement of Parts I–VII; it composes them into a proportionate path.

## K.6 Adoption Sizing (Indicative, Non-Normative)

> *Status. This section is **non-normative planning guidance**. The figures below are **indicative order-of-magnitude ranges** derived from the deliverable and phase structure of the method (Part III) — **not** measured results from executed deployments. They are provided because adopters need a starting calibration the conformance model itself does not give; they MUST be replaced by an organization's own measured effort once a pilot (Part VI §29.5) has run. No empirical claim is made or implied.*

**Cost drivers.** Adoption effort is dominated by three quantities, not by the page count of the framework: (1) the number of registered invariants; (2) the share of those invariants that are `E3` — each `E3` invariant requires a pinned analyzer to be built, tuned, and friction-measured (Part I §2.6); and (3) the breadth of the governance boundary (the number of governed action classes and governed systems). The ranges below are for a **single, narrow boundary** of the NovaCare shape (one governed agent, one repository/pipeline class, on the order of 5–10 invariants; Appendix H).

| Tier | What it delivers | Indicative effort (order of magnitude) | Indicative elapsed time |
|---|---|---|---|
| **Tier 0 — On-Ramp** (non-conformant) | `C1`, `C2`, `C3`, `C5`, `C6`, `C7` over one boundary; no `C4`/trajectory | ~1–3 person-months | 4–8 weeks |
| **Tier 1 — L3** (narrow boundary) | adds `C4`, the full method, threat assessment, negative tests; network-enforced P4 | ~3–6 person-months on top of Tier 0 | +6–12 weeks |
| **Tier 1 — L4** (narrow boundary) | adds the executed negative-test battery, `E3` analyzer tuning + friction measurement, the Conformance Evidence Record, and independent assessment | ~3–6 further person-months, dominated by `E3` analyzer work | +8–12 weeks + assessment |

These ranges assume an existing engineering team, a pre-existing IdP/secrets infrastructure, and a policy authority already able to issue signed artifacts. They scale roughly with invariant count and `E3` share. An estate-wide L4 over many boundaries is **not** a linear multiple of the above — it is a programme, not a project, and SHOULD be decomposed into per-boundary Tier-1 efforts (§K.4).

**Pilot duration.** A first independent conformance pilot (Part VI §29.5) SHOULD budget a **bounded operation window** to establish the governance-friction baseline and the mean-time-between-governance-failures figures that cannot be measured before deployment. The NovaCare worked example uses **90 days** of Policy Deployment (§7.2) operation (Appendix H §H.9) as an indicative figure: shorter windows under-sample the AMBIGUOUS→DENY friction (Part V §26); longer windows delay the first conformance evidence.

**Federated Context Registry — the economic blind spot.** Corrective Reframing and much of `C3`'s value rest on a **Federated Context Registry** the framework itself acknowledges is "notoriously incomplete" in enterprises (Part V; Appendix H). Its construction and maintenance are the least-bounded cost of adoption and SHOULD be sized explicitly rather than assumed. Indicative cost drivers:

- **Initial construction** — inventorying the authoritative sources (APIs, services, schemas, crypto/authz standards) the record must resolve against. Order of magnitude: comparable to, or exceeding, the Tier-1 component build for a large estate; for a narrow boundary it is bounded by that boundary's surface.
- **Maintenance** — the golden record is a *living* artifact; it MUST track the systems it describes or it produces false `CONTEXT_FAILURE`s (friction) and, worse, stale "valid alternatives" in reframing. Budget continuous effort proportional to the change rate of the governed systems, not a one-off.
- **Failure mode if under-resourced** — an under-maintained golden record drives the governance-friction erosion loop (Part V §26): rising false positives → relaxation pressure. Golden-record maintenance is therefore a governance cost, not merely an IT cost.

A deployment SHOULD record its actual sizing — effort, pilot window, and golden-record build/maintenance cost — in the Pilot/Validation Plan (Part VI appendix), so that these indicative ranges are progressively replaced by the organization's measured figures.

---

*End of Appendix K — CROA Core Profile.*
