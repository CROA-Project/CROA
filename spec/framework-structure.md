---
tags:
  - croa_foundation
version: 1
language: english
---
# CROA — Constrained Reachability Orchestration Architecture

### A Reference Architecture for Agentic Governance

**Version 1.0.1.1 — Framework Specification**

> *Non-normative overview. This document is a navigational scaffold for the framework. The authoritative content is Parts I–VII; where this overview and a Part differ, the Part governs. Synced to include the subject authorization model (RBAC, §4.9.1), the Agent Qualification Layer (AQL, §4.9.2), threat class TH-11, and the completed Parts VI–VII.*

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The

> **Document status.** This overview accompanies the **first Official Specification** of the CROA framework — see [CROA — Official Specification (Front Matter)](parts/00-front-matter.md) for the governing status statement, publication information, and revision history.

---

## Canonical Positioning Paragraph

> **CROA — Constrained Reachability Orchestration Architecture — is a reference architecture for agentic governance. It treats agentic AI workflows as deterministic state machines whose reachable states are constrained by enforceable invariants. Within the modeled action space, under the registered invariant set, and given network-enforced containment (P4), unsafe execution paths are unreachable by construction, not merely refused at runtime. CROA decouples agent reasoning from system execution, ensuring that every state transition is either validated against governance invariants or compiled under a cryptographically signed authorization. Where probabilistic systems offer alignment and multi-agent frameworks offer orchestration, CROA offers structural enforcement: governance as a property of the architecture, not the agent.**

---

## Framework Document Structure

The CROA framework is organized in seven parts following TOGAF/NIST standards anatomy. This structure supersedes the original eleven-part specification layout; all original content is preserved and relocated as indicated in the mapping below.

| Part    | Title                      | Chapters | Purpose                                          |
| ------- | -------------------------- | -------- | ------------------------------------------------ |
| **I**   | Foundations                | 1–3      | Purpose, scope, definitions, and tenets          |
| **II**  | Reference Architecture     | 4–6      | Logical components, invariants, trust boundaries |
| **III** | Method                     | 7–17     | The CROA Policy-as-Code Lifecycle          |
| **IV**  | Deployment Models          | 18–24    | Concrete realizations and integration patterns   |
| **V**   | Threat Model               | 25–27    | Threats, failure modes, and mitigations          |
| **VI**  | Conformance and Maturity   | 28–30    | Conformance levels and maturity model            |
| **VII** | Governance of the Standard | 31–33    | Lifecycle of the standard itself                 |

### Mapping from Original Eleven-Part Structure

| Original Part | Original Title | Relocated to |
|---|---|---|
| I | Foundations | Part I, Chapters 1–3 |
| II | Principles | Part I, Chapter 3 (Tenets) |
| III | Reference Architecture | Part II, Chapters 4–6 |
| IV | Execution Modes | Part IV, Deployment Models |
| V | Roles and Responsibilities | Part I, Chapter 2 (Definitions) |
| VI | Invariant Taxonomy | Part II, Chapter 5 (Architectural Invariants) |
| VII | Maturity Model | Part VI, Chapter 30 |
| VIII | Conformance Criteria | Part VI, Chapters 28–29 |
| IX | Anti-Patterns | Part V, Chapters 25–26 (Threat Model) |
| X | Adoption Path | Part III, Method (CROA Development Cycle) |
| XI | Reference Implementation | Appendix G (non-normative) |

---

## Part I — Foundations

*Chapters 1–3 | Full specification: [Part I - Foundations](parts/part-1-foundations.md)*

### Chapter 1 — Introduction

#### 1.1 Definition

The **Constrained Reachability Orchestration Architecture (CROA)** is a reference architecture for governing autonomous AI systems that perform consequential actions on enterprise infrastructure.

CROA specifies how agentic workflows are decomposed, validated, compiled, executed, and audited such that:

- No execution path violating a governance invariant is reachable in the system's state space.
- All authorized exceptions to invariants are cryptographically signed and propagated as first-class execution state.
- All transitions, blocked or executed, produce immutable evidence sufficient for independent audit.

CROA is **architecture**, not policy. It does not specify what enterprises should govern; it specifies how governance becomes structurally enforceable in agentic systems.

#### 1.2 Scope

CROA applies to any system in which:

- One or more autonomous components (agents) propose actions affecting enterprise state.
- Those actions, if executed, would create persistent effects on code, data, infrastructure, or external systems.
- The enterprise requires deterministic preservation of safety, security, regulatory, or operational invariants.

CROA does not apply to:

- Conversational systems with no execution authority.
- Purely advisory analytical workloads.

#### 1.3 Relationship to Adjacent Frameworks

| Framework | Domain | Relationship to CROA |
|---|---|---|
| NIST AI RMF | AI risk management lifecycle | Complementary — CROA is the runtime enforcement layer for AI RMF's identified risks |
| ISO/IEC 42001 | AI management system | Complementary — CROA provides the technical control architecture for an AI management system's operational requirements |
| Zero Trust (NIST 800-207) | Network and identity security | Architectural parallel — CROA applies Zero Trust principles to agent state transitions |
| Open Policy Agent / Cedar | Policy-as-code | Adjacent — possible implementation of CROA's enforcement layer |
| ITIL Change Management | IT service management | Conceptual ancestor — CROA's ECC artifact is the agentic analog to the ITIL change request |

---

### Chapter 2 — Definitions and Terminology

- **Agent** — an autonomous component capable of proposing state transitions. Treated as an untrusted operator.
- **Transition** — a proposed change to system state, initiated by an agent or human.
- **Invariant** — a non-negotiable governance constraint that must hold across all reachable states.
- **Authorization** — a cryptographically signed token permitting a specific transition that would otherwise violate an invariant.
- **Execution Change Contract (ECC)** — the compiled artifact representing a validated execution commitment.
- **Reachable State** — a state the system can enter through a sequence of validated transitions.
- **Unreachable State** — a state for which no validated transition sequence exists; structurally impossible to enter.
- **Gatekeeper** — the conceptual function responsible for invariant validation and authorization generation. In the formal reference architecture it is realized by the Execution Governor (`C2`, the permit/deny decision) together with the Invariant Monitor (`C4`, invariant and trajectory state); the resulting commitment is compiled by the Contract Compiler (`C7`). "Gatekeeper" is the layer-model name for this function; the `Cn` names are authoritative (see Part I §2.2).
- **Execution Firewall** — the conceptual name for the runtime control that blocks unvalidated transitions. In the formal reference architecture it is the Execution Firewall component (`C6`).
- **Evidence Ledger** — the conceptual name for the immutable record of all transitions, blocks, and authorizations. In the formal reference architecture it is the **Audit and Provenance Store (`C5`)**. The two terms denote the same registry; they are not two separate stores. **Normative term decision (2026-06-11):** "Audit and Provenance Store (`C5`)" is the single normative term for the component; "Evidence Ledger" is retained **only** as the non-normative name of Layer 6 in this layer model. Normative statements in Parts I–VII use "Audit and Provenance Store (`C5`)" (see Part I §2.2).
- **Technical Sycophancy** — the tendency of agents to reinterpret governance constraints under operational pressure to satisfy task objectives.

**Roles**

| Role | Responsibility |
|---|---|
| **Governance Architect** | Owns the invariant registry. Defines what cannot be violated and what may be authorized. |
| **Authorization Authority** | Owns the cryptographic authorization process. Issues, scopes, and revokes authorizations. Distinct from any agent or operator. |
| **Semantic Custodian** | Owns the Federated Context Registry — the validated context against which agents operate. |
| **Evidence Officer** | Owns the Audit and Provenance Store (`C5`). Ensures audit-readiness, retention, and access controls. |
| **Operations** | Operates the agentic workflows. Cannot issue authorizations, modify invariants, or alter the Ledger. |
| **Independent Auditor** | Verifies CROA conformance using only the Audit and Provenance Store (`C5`). Has no operational role. |

*These organizational roles are a **navigational summary**, not the normative role model. This overview is non-authoritative and carries no normative requirements (see the header note). Each role maps to its authoritative home in the Parts as follows:*

| Overview role | Authoritative home (normative) |
|---|---|
| Governance Architect | Part I §2.2 and Part III §7.4 (Governance Architect) |
| Authorization Authority | Part I §2.2 / Part II §4.3 — the **Policy Authority (`C1`)**, the sole issuer of policy and authorization artifacts (I4); see also the Policy Authority Representative in Part III §7.4 |
| Semantic Custodian | Part I §2.1 (Federated Context Registry) / Part II §4.5.2; owner of the golden record consulted by `C3` |
| Evidence Officer | Part II §4.7 — custodian responsibilities for the Audit and Provenance Store (`C5`) |
| Operations | Part III §7.4 (operational roles) — runs the workflows; cannot issue authorizations or alter `C5` |
| Independent Auditor | Part VI Chapter 29 (independent assessor) and Part VII §32.2 (neutrality) |

*The **separation of the authorization authority (`C1`) from operations** is the load-bearing separation-of-duties property; its normative force comes from the component-independence requirements of Part II (§4.3 `C1` exclusivity, §4.7 `C5` append-only) and the neutrality requirements of Part VII §32.2 — not from this overview. Appendices M and N reference these roles via their authoritative homes in Part I §2.2 / Part III §7.4, not via this overview.*

---

### Chapter 3 — Tenets

CROA conformance requires adherence to ten tenets. These are normative, not aspirational — they are the architectural contract from which the conformance criteria derive. A system that violates any tenet is not CROA-conformant. The authoritative statements and justifications are in Part I, Chapter 3; the summaries below are navigational.

**T1 — Unsafe execution paths are structurally unreachable, not merely discouraged**
No sequence of governed actions may lead from any reachable state to an invariant-violating state, except through a valid authorization. Realized by the Path Resolver (`C3`), Invariant Monitor (`C4`), Contract Compiler (`C7`), and Execution Firewall (`C6`).

**T2 — Governance is enforced at the execution layer, not the model layer**
Governance controls are interposed between the agent's candidate action and the systems it would act on. Training, system prompts, and alignment are complementary measures only — never primary governance.

**T3 — Every governed action is an explicit, auditable orchestration decision**
Each executed action is traceable to a specific permit decision in the Audit and Provenance Store (`C5`), reconstructable independently of the agent's reasoning.

**T4 — Policies are deterministic artifacts; their interpretation is not delegated to the agent**
Policy is evaluated by the Execution Governor (`C2`), structurally independent of the governed agent. The agent receives a permit/deny decision, never policy text to interpret.

**T5 — State transitions are observable, reversible where feasible, and bounded**
Every governed transition is assigned a reversibility/consequence class (R0–R4) that fixes the minimum authorization and evidence required; the class is recorded in the ECC (`C7`) and in `C5`.

**T6 — Trust is never inferred from stated intent; it is established by the orchestration layer**
No elevated permission, relaxed constraint, or authorization exemption may be granted on the basis of the agent's stated purpose, expressed reasoning, or asserted urgency.

**T7 — Ambiguity is resolved by refusal-to-execute, not best-effort interpretation**
When policy evaluation cannot produce a deterministic permit, the Refusal Gateway function of the Execution Firewall (`C6`) issues a deny and the gap is surfaced to the Policy Authority (`C1`). Unknown permissibility is treated as impermissibility until resolved.

**T8 — Sycophantic reinterpretation of constraints is a structural failure mode and is detectable**
The Invariant Monitor (`C4`) detects trajectories that are individually permitted but cumulatively violating, covering at least five patterns: Sequence Accumulation, Scope Drift, Context Degradation, Path Composition, and Policy Reinterpretation. Detection is never delegated to the governed agent.

**T9 — Governance artifacts are versioned, signed, and survive the agent's lifecycle**
All policy artifacts, authorization records, and audit entries are cryptographically signed, versioned, and retained in `C5` independently of any governed agent instance's lifecycle.

**T10 — Conformance is demonstrated by reproducible properties, not by attestation**
Governance properties are demonstrable by an independent auditor through reproducible tests against `C5` and the architecture itself; assertions from the vendor, implementer, or agent are not evidence of conformance.

---

## Part II — Reference Architecture

*Chapters 4–6*

### Chapter 4 — Logical Reference Architecture

CROA specifies six architectural layers. Implementations may combine or distribute these layers across components, but all six functions must be present and enforceable.

**Layer 1 — Intake**
Receives requests from agents or humans and normalizes them into a canonical form for evaluation. Every request is identified, time-stamped, and attributed to a principal. Within a session, the Invariant Monitor (`C4`) maintains trajectory state across requests (Part II §4.6), and identical requests yield identical decisions under the determinism invariant I2. *(The Parts specify identical-input determinism (I2, Part II §5.2) and session-scoped trajectory state (§4.6.1) — not a cross-session "semantic-equivalence" linker; this overview previously overstated intake as linking "semantically equivalent" requests, which no Part specifies.)*

**Layer 2 — Semantic Authority**
Validates that the request is grounded in real, current, accessible technical and organizational context. Requests referencing non-existent APIs, dependencies, files, or entities are blocked before invariant evaluation. Hallucinated context is treated as a category of invariant violation, not as a recoverable error.

**Layer 3 — Invariant Validation (Gatekeeper)**
Evaluates the grounded request against the invariant set. Produces one of three outcomes:

- **Permitted** — transition does not violate any invariant; proceeds to compilation.
- **Authorized Exception** — transition violates an invariant but carries valid authorization; proceeds under bounded scope.
- **Blocked** — transition violates an invariant with no valid authorization; halts pipeline.

The Gatekeeper issues the permit/deny decision; on a permit, the validated transition proceeds to compilation. It never relaxes an invariant. The signed **authorization artifacts** that enable a Constrained-Execution exception are issued **solely by the Policy Authority (`C1`)** (I4, Part II §4.3.1) — not by the Gatekeeper. Human override attempts are evaluated as requests for a `C1` authorization; they do not bypass the Gatekeeper and are never processed as an unblock at the Execution Firewall (§4.8).

**Layer 4 — Contract Compilation (`C7` — Contract Compiler)**
Compiles validated transitions into immutable execution contracts (ECCs). ECCs are content-addressed and tamper-evident. An ECC cannot be modified after compilation; modifications produce a new ECC linked to the original. Downstream agents operate against ECCs, never against the original request.

**Layer 5 — Execution Firewall (`C6`)**
Enforces, at runtime, that only ECC-derived operations execute against governed systems. Performs binary validity checks — no reasoning, negotiation, or interpretation. Block decisions are not appealable at the Firewall layer; appeals re-enter at Layer 1.

**Layer 6 — Evidence Ledger**
Records all transitions, blocks, authorizations, ECCs, and execution events in immutable, cryptographically chained form. Every entry is sufficient to reconstruct the governance decision without access to agent reasoning logs.

**Admission stage (Agent Surface).** Before a request enters the six-layer pipeline, the Agent Surface applies a four-stage subject authorization model at the Agent Boundary: (1) Identity, (2) Role eligibility (RBAC, §4.9.1), (3) Qualification — for agent subjects, via the Agent Qualification Layer (AQL, §4.9.2), and (4) Runtime policy (the pipeline above). The admission stage can only *restrict* what enters the pipeline; it is not one of the six layers and never relaxes the governance decision.

---

### Chapter 5 — Architectural Invariants

CROA does not prescribe specific invariants — these are enterprise-defined. Conformant implementations classify invariants along the following taxonomy to ensure governance coverage.

| Category | Examples |
|---|---|
| **Data Sovereignty** | Cross-border data movement, residency, anonymization requirements |
| **Access Control** | Authorization checks, object-level permissions, identity propagation |
| **Cryptographic Integrity** | Encryption standards, signature validation, key management |
| **Dependency Governance** | Approved libraries, supply-chain controls, version pinning |
| **Execution Environment** | Sandboxing, isolation boundaries, runtime restrictions |
| **Observability Boundaries** | What may be logged, where, and with what protections |
| **Regulatory Compliance** | GDPR, HIPAA, sectoral requirements |
| **Architectural Integrity** | Service boundaries, contract conformance, schema validation |
| **Functional Validity** | Existence of referenced APIs, dependencies, and abstractions |
| **Resource and Cost Governance** | Compute/token budgets, spend caps, rate and concurrency limits (counterpart to the availability threat class TH-11) |

Each enterprise's invariant registry should map to this taxonomy. Gaps indicate governance coverage risk.

---

### Chapter 6 — Trust Boundaries

Four trust boundaries — TB-1 (Agent), TB-2 (Policy), TB-3 (Execution), TB-4 (Audit) — plus the execution-surface formalism and a §6.5 architecture-description (ISO/IEC/IEEE 42010) viewpoint set. Fully specified in Part II, Chapter 6.

---

**Step 4 — Authorization Framework** *(CROA-PaC: Phases B and D)*
Establish the Policy Authority (`C1`) as a structurally separate role. Define authorization scopes, signing infrastructure, and propagation mechanisms.

**Step 5 — Conformance Validation** *(CROA-PaC: Phases F–G; Part VI)*
Engage an independent assessor to perform the conformance tests. Remediate findings before claiming CROA conformance externally.

**Step 6 — Continuous Operation** *(CROA-PaC: Policy Update (§7.2))*
Treat invariant maintenance, authorization scope review, and Ledger integrity as ongoing operational disciplines, not project deliverables.

---

## Part IV — Deployment Models

*Chapters 18–24*

CROA defines five deployment models — topological arrangements of the OCP and the Agent Surface relative to the governed agent and the governed systems. All five preserve the same seven invariant properties (P1–P7, §18.1); they differ in component placement, trust-boundary realization, and operational trade-offs. A conformant deployment selects one primary model (or a documented hybrid) under Part III §11.2 and records the rationale in the RTM.

**DM-1 — Centralized**
A single OCP mediates all governed agents. Lowest topological complexity; the baseline against which the other models vary.

**DM-2 — Federated**
Per-domain OCPs under a coordinating meta-policy authority; for multi-domain or multi-business-unit governance.

**DM-3 — Sidecar**
An OCP instance co-located with each governed agent or workload; enforcement sits close to the agent, common in service-mesh environments.

**DM-4 — Gateway-Mediated**
The OCP enforces at an API gateway or egress boundary through which all governed actions must pass.

**DM-5 — Embedded**
The OCP is embedded within a host platform (e.g., a multi-tenant SaaS), with per-tenant audit isolation (§23.5.1).

Model selection is driven by six criteria (§18.2) — including trust topology, latency, and throughput — and the invariant properties P1–P7 hold in every model. The three CROA *execution modes* (Blocking, Constrained Execution, Corrective Reframing) are an orthogonal concept defined in Part I §2.1, not a property of the deployment model.

---

## Part V — Threat Model

*Chapters 25–27*

The following patterns violate CROA conformance even when they appear to provide governance. Each is a documented failure mode in probabilistic and multi-agent systems.

- **Advisory enforcement** — security reviews that identify violations but do not block them
- **Distributed authorization** — multiple components capable of granting overrides
- **Reconstructed evidence** — audit trails assembled from operational logs rather than produced as first-class artifacts
- **Agent self-governance** — relying on the agent's own reasoning to detect and refuse its own violations
- **Override as bypass** — treating authorization as a way to skip governance rather than as a bounded exception
- **Refusal without unreachability** — blocking individual requests while leaving the unsafe path architecturally available
- **Context fabrication** — agents synthesizing missing context to maintain workflow velocity
- **Compliance simulation** — generating compliance artifacts without enforcing the constraints they document

*Normative Part V specifies eleven formal threat classes (TH-1 Technical Sycophancy through TH-11 Governance Availability Exhaustion), each with manifestation patterns, detection signatures, structural mitigations, and minimum negative tests (§27.3); the patterns above are informal precursors. The Agent Qualification Layer attack surface is covered as a note in §26.*

---

## Part VI — Conformance and Maturity

*Chapters 28–30*

### Chapter 28–29 — Conformance Criteria

A system claims CROA conformance only if it satisfies the normative conformance criteria. The seven tests below are a **non-normative navigational summary** of the conformance intent; the **authoritative criteria are the twelve Part II Conformance Requirements** (Part II, "Part II Conformance Requirements": component completeness, execution-boundary integrity incl. ECC single-use, policy-authority exclusivity, subject-authorization conformance, agent-qualification conformance, ECC schema conformance, C2.eval determinism, C5 integrity chain, Governance Success classification, session-lifecycle conformance, trajectory-analysis presence, ECC-to-invariant consistency) together with the Part VI Chapters 28–29 level model. Where this summary and those criteria differ, the Parts govern. All criteria are verifiable by an Independent Auditor using the Audit and Provenance Store (`C5`) and the cross-check artifacts named in the Part II/VI conformance preambles:

1. **Decoupling test** — No agent output causes state change without traversing the enforcement layer. *(→ Part II "execution-boundary integrity")*
2. **Reachability test** — No transition sequence exists from any reachable state to a state violating any registered invariant, except via valid authorization.
3. **Authorization integrity test** — All authorizations in the Ledger are cryptographically valid, scoped, and issued by the designated Authority.
4. **Evidence completeness test** — Every transition in the period under audit is represented in the Ledger.
5. **Override resistance test** — Documented adversarial attempts produce no unauthorized executions.
6. **Context grounding test** — Requests referencing non-existent technical entities produce blocking decisions, not synthesized implementations.
7. **Determinism test (I2)** — Identical requests (same grounded action, policy artifact version, and invariant state) produce identical governance decisions, and within a session trajectory state is maintained by `C4`. *(CROA specifies identical-input determinism and session-scoped trajectory analysis, not cross-session semantic-equivalence matching; see Part II §5.2 and §4.6.1. The authoritative Part II conformance criterion is "C2.eval determinism (I2)".)*

A system that fails any single criterion is not CROA-conformant. Partial conformance is not recognized.

### Conformance Levels (Chapters 28–29)

The table below is the **system enforcement-maturity** scale — the L0–L5 **conformance levels** specified in Part VI, **Chapter 28**. These are distinct from the *organizational* maturity model (M0–M4) in Chapter 30; Part VI §30.1 draws the distinction precisely. (Earlier versions of this overview mislabeled this table as "Chapter 30 — Maturity Model"; the L0–L5 scale is the Chapter 28 conformance model, and the M0–M4 organizational model is summarized below it.)

| Level | Name | Description |
|---|---|---|
| L0 | Ungoverned | Agents act directly on systems. Governance exists in documents only. No structural enforcement. |
| L1 | Advisory Governance | Governance is detected and reported but does not block execution. |
| L2 | Refusal-Based Governance | Deny decisions are produced and enforced for actions that traverse the OCP, but enforcement is bypassable (P4 not network-enforced). |
| L3 | Reactive Enforcement | All governed actions traverse the OCP and deny is structurally enforced (P4 at the network layer), but structural unreachability is not yet demonstrated across action sequences. |
| **L4** | **Constructive Enforcement** | **Registered-invariant-violating transitions are architecturally unreachable within the modeled action space, under the registered invariant set, and given network-enforced P4. CROA conformance threshold.** |
| L5 | Adaptive Constructive Enforcement | A self-verifying architecture: L4 plus continuous self-emission of cryptographic proof of its own conformance, such that conformance is re-establishable at any time without a manual assessment cycle, while the registered invariant set and qualification batteries adapt under governed change (Policy Update (§7.2)) without dropping below L4 at any transition. (L5 evidence criteria are not fully specified in v1.0.1 and are not independently assessable yet — Part VI §28.2.) |

### Chapter 30 — Organizational Maturity Model (M0–M4)

Chapter 30 specifies a separate **organizational practice** maturity model, **M0–M4**, describing how mature an *organization's* governance practice is (people, process, and continuous-improvement discipline) — as opposed to how enforcing a *system* is (the L0–L5 conformance levels above). An organization may run an L4-conformant system while still maturing its organizational practice, and vice versa. The authoritative M0–M4 definitions are in Part VI, Chapter 30 (§30.1 distinguishes the two scales).

---

## Part VII — Governance of the Standard

*Chapters 31–33.* Lifecycle and versioning of the standard (§31), governance with neutrality and a public change/ratification process (§32), and conformance stewardship, profiles, and derivative-works rules (§33). Fully specified.

---

## Appendices

All appendices to the CROA Framework are published as standalone files in the `Appendices/` folder. Appendix A is normative; C and D are deprecated in v1.0.1, superseded by the Policy-as-Code lifecycle in Part III; K is a normative profile (Part VII §33.3); L is normative for deployments that implement multi-agent delegation (conditional); D, E, F, I, J, M, N, and O are informative; B is reference; G and H are non-normative. Machine-readable JSON Schemas for the `gar.*`, `gga.*`, `ecc.*`, and `event.*` namespaces are published in the `schemas/` folder (see [Appendix B - Notation, Identifiers and Symbols](appendices/appendix-b-notation-identifiers-and-symbols.md) and `schemas/README.md`).

| Appendix | Title | Status | File |
|---|---|---|---|
| A | Lexicon | Normative | [Appendix A - Lexicon](appendices/appendix-a-lexicon.md) |
| B | Notation, Identifiers, and Symbols | Reference | [Appendix B - Notation, Identifiers and Symbols](appendices/appendix-b-notation-identifiers-and-symbols.md) |
| C | Consolidated Deliverables Catalog | Deprecated in v1.0.1 | [Appendix C - Consolidated Deliverables Catalog](appendices/appendix-c-consolidated-deliverables-catalog.md) |
| D | Mapping to TOGAF ADM | Deprecated in v1.0.1 | [Appendix D - Mapping to TOGAF ADM](appendices/appendix-d-mapping-to-togaf-adm.md) |
| E | Mapping to NIST SP 800-207 (Zero Trust) | Informative | [Appendix E - Mapping to NIST SP 800-207](appendices/appendix-e-mapping-to-nist-sp-800-207.md) |
| F | Mapping to ISO/IEC 27001 (Annex A) | Informative | [Appendix F - Mapping to ISO IEC 27001](appendices/appendix-f-mapping-to-iso-iec-27001.md) |
| G | Reference Implementation (Riven) and Minimal Reference Harness | Non-normative | [Appendix G - Reference Implementation](appendices/appendix-g-reference-implementation.md) |
| H | Worked Example (NovaCare) | Non-normative | [Appendix H - Worked Example (NovaCare)](appendices/appendix-h-worked-example-novacare.md) |
| I | C4 Implementation Approaches (Trajectory Analysis) | Informative | [Appendix I - C4 Implementation Approaches](appendices/appendix-i-c4-implementation-approaches.md) |
| J | Performance and Latency Profile | Informative | [Appendix J - Performance and Latency Profile](appendices/appendix-j-performance-and-latency-profile.md) |
| K | CROA Core: A Risk-Proportionate Adoption Profile | Normative (profile) | [Appendix K - CROA Core Profile](appendices/appendix-k-croa-core-profile.md) |
| L | Governed Multi-Agent Delegation | Normative (conditional) | [Appendix L - Governed Multi-Agent Delegation](appendices/appendix-l-governed-multi-agent-delegation.md) |
| M | Mapping to the EU AI Act | Informative | [Appendix M - Mapping to the EU AI Act](appendices/appendix-m-mapping-to-the-eu-ai-act.md) |
| N | Mapping to ISO/IEC 42001 | Informative | [Appendix N - Mapping to ISO IEC 42001](appendices/appendix-n-mapping-to-iso-iec-42001.md) |
| O | CROA and Adjacent Enforcement Mechanisms | Informative | [Appendix O - CROA and Adjacent Enforcement Mechanisms](appendices/appendix-o-croa-and-adjacent-enforcement-mechanisms.md) |
| P | Sector Worked Examples (Luxury, Logistics, E-commerce) | Informative | [Appendix P - Sector Worked Examples](appendices/appendix-p-sector-worked-examples.md) |
| Q | Evidence Pack and Reference Negative Tests | Informative | [Appendix Q - Evidence Pack and Reference Negative Tests](appendices/appendix-q-evidence-pack-and-reference-negative-tests.md) |
| R | C5 High-Performance Evidence Pattern | Informative | [Appendix R - C5 High-Performance Evidence Pattern](appendices/appendix-r-c5-high-performance-evidence-pattern.md) |
| S | Implementing C4 in Common Enterprise Cases | Informative | [Appendix S - Implementing C4 in Common Enterprise Cases](appendices/appendix-s-implementing-c4-in-common-enterprise-cases.md) |

**Reference implementation (Appendix G).** **Riven** is the CROA Foundation's founding implementation — the prototype evidence that the architecture is operationally realizable. Riven is currently paused. It is repositioned in Appendix G as founding implementation and historical design driver, not as independent conformance proof. Appendix G also introduces the **CROA Minimal Reference Harness** specification: a vendor-neutral, minimal demonstration artifact that any implementer can build to illustrate the evidence model, the ECC flow, and the four reference negative tests. Implementations claiming CROA conformance need not be derived from Riven but must pass the conformance criteria in Part VI (Chapters 28–29). The conformance criteria, not any reference implementation, define the architecture.

**Companion Documents.** Three non-normative companion documents are published alongside the specification in the `Companion Documents/` folder:

| Document | Audience | Location |
|---|---|---|
| CROA Executive Brief | CEO, CTO, CDO, AI governance leaders | `Companion Documents/CROA Executive Brief.md` |
| CROA Implementation Primer | Enterprise architects, security architects, tech leads | `Companion Documents/CROA Implementation Primer.md` |
| CROA Conformance Evidence Guide | Auditors, risk teams, security leads, independent assessors | `Companion Documents/CROA Conformance Evidence Guide.md` |
