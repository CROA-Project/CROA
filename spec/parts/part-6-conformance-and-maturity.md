---
tags:
  - croa_foundation
version: 1
language: english
---

# CROA Framework — Part VI: Conformance and Maturity

**Full title:** CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution
**Series designation:** CROA-6
**Status:** Official Specification (v1.0.1)
**Version:** v1.0.1
**Date:** 2026-09-03
**Part:** VI of VII

---

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The

---

## Chapter 28. Conformance Levels

**Chapter abstract.** This chapter specifies the CROA conformance levels — the ordered classification (L0 through L5) of how completely a system realizes structural governance of agentic execution. Each level is defined by the invariants it enforces, the components and admission controls it requires, the evidence it produces, and the minimum deployment guarantees it provides. The levels are cumulative: a system at level L*n* satisfies every requirement of L0 through L*n*. **L4 (Constructive Enforcement) is the CROA conformance threshold** — the lowest level at which a system may be described as "CROA-conformant" without qualification. This chapter depends on the architectural invariants (Part II, Chapter 5), the components and admission model (Part II, Chapter 4, including §4.9.1 RBAC and §4.9.2 AQL), the deployment invariant properties P1–P7 (Part IV §18.1), and the threat classes and negative-testing requirements (Part V, Chapters 26–27). Chapter 29 specifies how a level is asserted and evidenced.

---

### 28.1 The Conformance Model

A CROA conformance level is a property of a *deployed system within a defined governance boundary*, not of the framework, a vendor, or a product line. Conformance is:

- **Cumulative.** Each level subsumes all requirements of the levels below it. A claim of L*n* is also a claim of L0…L*n*−1.
- **Scoped.** A conformance claim names the governance boundary (Part I §2.3) to which it applies. A system may be L4 within one governance boundary and ungoverned outside it; the claim MUST state the boundary.
- **Evidenced, not attested.** A level is established by reproducible evidence available to an independent assessor without relying on the implementing party's active cooperation or interpretation (T10; see §29.4). Vendor assertion is not evidence (Part I, T10; §29.4).
- **Point-in-time, with continuity for L5.** Levels L0–L4 are assessed for an audit period. L5 additionally requires continuous, self-emitted proof (§28.2).

The level names align with the enforcement-maturity stages defined in the CROA project canon: **L0 Ungoverned, L1 Advisory Governance, L2 Refusal-Based Governance, L3 Reactive Enforcement, L4 Constructive Enforcement, L5 Adaptive Constructive Enforcement.** These describe the *system's* enforcement maturity and are distinct from the *organization's* practice maturity, which is the subject of the maturity model in Chapter 30.

---

### 28.2 The Six Conformance Levels

**L0 — Ungoverned.**
Agents act directly on governed systems; governance, if any, exists as documents and human discipline. No Orchestration Control Plane mediates execution.

- *Invariants enforced:* none structurally.
- *Components required:* none.
- *Admission controls:* none.
- *Evidence produced:* none required.
- *Minimum deployment:* not applicable.
- *Characteristic risk:* every threat class in Part V is unmitigated at the architecture layer.

**L1 — Advisory Governance.**
Governance decisions are produced and recorded, but they are advisory: not all governed actions traverse the OCP, and a deny decision does not structurally prevent execution.

- *Invariants:* I3 (Auditability) and I6 (Observability) for the actions that do traverse the OCP.
- *Components:* `C2` (producing decisions) and `C5` (recording them) present; other components MAY be partial.
- *Admission controls:* subject authentication (§4.9) SHOULD be present.
- *Evidence:* a `C5` record of advisory decisions for traversing actions.
- *Minimum deployment:* any topology that records decisions.
- *Limitation:* unsafe paths remain reachable; deny is not enforced.

**L2 — Refusal-Based Governance.**
Deny decisions are produced and enforced for actions that traverse the OCP, but enforcement is probabilistic or bypassable: not all channels to governed systems are eliminated (P4 is not enforced at the network layer), so refusal can be circumvented.

- *Invariants:* I3, I6, and I5 (Refusal) for traversing actions.
- *Components:* `C2`, `C3`, `C5`, `C6`, `C7` present. `C3` is required wherever an ECC is compiled: an ECC's `ecc.action` is, by schema (Part II §4.4.1, `ecc.schema.json`), a grounded governed action with `gga.semantic_result = GROUNDED`, which only `C3` can produce — so no schema-valid ECC exists without `C3`. `C7` compiles those ECCs and `C6` validates them. What distinguishes L2 from L3 is **not** the absence of `C3` but the absence of network-enforced P4: refusal is still bypassable. (`C1` policy issuance and `C4` trajectory analysis may be partial at L2.)
- *Admission controls:* subject authentication required; role-based admission (§4.9.1) SHOULD be present.
- *Evidence:* `C5` records including `DENY` and refusal events.
- *Minimum deployment:* any; bypass channels not yet eliminated.
- *Limitation:* TH-3 (Orchestration Bypass) is not structurally mitigated.

**L3 — Reactive Enforcement.**
All governed actions within the governance boundary traverse the OCP, and deny decisions are structurally enforced at runtime: P4 (the OCP as sole execution passage) is enforced at the network layer, and `C6` is the sole path to governed systems (TB-3). Some invariants are registered and enforced, but structural unreachability is not yet demonstrated across action sequences.

- *Invariants:* I3, I4 (Policy Authority), I5, I6, I7 (Lifecycle); a registered subset of enterprise governance invariants enforced per-action.
- *Components:* all seven (C1–C7) present and structurally independent (Part II conformance).
- *Admission controls:* **RBAC subject authorization (§4.9.1) REQUIRED**; the admission predicate is enforced and `ADMISSION_REJECTED` events recorded.
- *Evidence:* Part II conformance criteria satisfied; absence of any `EXECUTION_AUTHORIZED` without a corresponding ECC (TB-3 integrity); Part V threat-assessment documentation complete for all eleven threat classes (Threat Assessment C-22, Mitigation Map C-23, Residual Risk Register C-24, TH-1 Detection Specification C-25). The mitigations introduced at L4 — trajectory analysis (`C4`) and the Agent Qualification Layer — are mapped but need not yet be active at L3.
  - *Execution-evidence rule (Execution boundary integrity, Criterion 2).* An `EXECUTION_AUTHORIZED` event evidences ONLY that an operation was admitted by C6. `EXECUTION_COMPLETED`, `EXECUTION_FAILED`, or `EFFECT_ATTESTED` events evidence execution. A `ECC_COMPILED` event evidences only that a commitment was *compiled*; it does **not** evidence execution (an ECC may be compiled and then expire, be revoked, or be blocked at `C6`). An assessor evaluating execution-boundary integrity MUST treat `EXECUTION_AUTHORIZED` — not `ECC_COMPILED` — as the execution marker, and MUST verify that every `EXECUTION_AUTHORIZED` traces to a valid, redeemed ECC and (for a governed exception) a redeemed `ecc.auth_ref`.
- *Minimum deployment:* a topology that enforces P1–P7 (Part IV §18.1), in particular P4 at the network layer.
- *Limitation:* path-composition (TH-7) and trajectory-based approaches to invariant violation are not yet structurally detected; not all invariants are necessarily registered.

**L4 — Constructive Enforcement (CROA conformance threshold).**
Within the modeled action space, under the registered invariant set, and given network-enforced execution-boundary containment (P4), unsafe execution paths are demonstrably unreachable by construction (I1) — the conditioned T1 guarantee, whose precise claim scope is stated in §28.6. At L4 this requires **all** of the following:

- all enterprise governance invariants are registered and enforced;
- authority non-expansion (I8, Part II §5.9) is evidenced by NT-008 and, where the deployment performs delegation, by the Appendix L §L.4 delegation negative tests;
- trajectory analysis is active (`C4`, T8);
- the negative-testing requirements of Part V are executed and pass under adversarial inputs; and
- all eleven threat classes are assessed.

This is the lowest level at which a system is **CROA-conformant**.

- *Invariants:* **all of I1–I8**, plus the complete registered set of enterprise governance invariants. Completeness of the registered set is established against the governance boundary through GitOps Definition (§7.2) (Part III); it is enterprise-attested and independently assessor-reviewed — not absolute — and any known coverage gap MUST be recorded in the Residual Risk Register (C-24).
- *Components:* all seven (C1–C7) and the Agent Surface. For deployments governing agent subjects with autonomous operational authority, the Agent Qualification Layer (§4.9.2) is **RECOMMENDED (SHOULD)** at L4 and becomes REQUIRED at L5 (see the AQL status note below).
- *Admission controls:* RBAC (§4.9.1) REQUIRED and enforced. For agent subjects, the AQL qualification gate (§4.9.2) **SHOULD** be enforced at L4; where it is deployed it MUST behave as specified in §4.9.2. (AQL is REQUIRED at L5.)
- *Evidence:* full Part II, Part III (method deliverables), Part IV (deployment invariant properties), and Part V (threat assessment, mitigation map, executed negative tests) conformance; the Conformance Evidence Record (C-32, §29.2).
- *Trajectory profiles:* every registered trajectory-relevant invariant is enforced according to its declared trajectory rule profile (Part II §4.6.3). In particular, any invariant exposed to accumulation MUST be registered and enforced as cumulative (`TP-C`) and, where the accumulation can span sessions for a subject, as cross-session cumulative (`TP-X`) with `C4` maintaining the per-subject aggregate across sessions; windowed (`TP-W`) analysis alone does not satisfy L4 for an accumulation-exposed invariant (TH-7.D/E, Part V).
- *Minimum deployment:* any of the five deployment models (Part IV) that preserves P1–P7 for the governance boundary.
- *Property:* a state reachable only through an operation not in the execution surface (Part II §6.2) is structurally unreachable; demonstrated, not asserted.

**L5 — Adaptive Constructive Enforcement (Self-Evidencing).**
A self-verifying architecture: the system continuously emits cryptographic proof of its own conformance as governance artifacts, such that conformance can be re-established at any time without a manual assessment cycle, and the registered invariant set and qualification batteries adapt under governed change (Policy Update (§7.2)) without dropping below L4 at any transition.

- *Invariants:* all of L4, continuously evidenced.
- *Components:* all of L4, plus continuous conformance-evidence emission.
- *Admission controls:* all of L4, plus — for deployments governing agent subjects with autonomous operational authority — the Agent Qualification Layer (§4.9.2) **REQUIRED** and enforced, with continuous (event-driven) qualification re-assessment (AQL recertification triggers, §4.9.2).
- *Evidence:* self-emitted, continuously verifiable conformance proofs; no manual attestation required.
- *Minimum deployment:* any L4-capable topology with continuous evidence emission.
- *Property:* conformance is a continuously held, machine-verifiable property rather than a periodic finding.

> *Note (L5 status, non-normative). The continuous conformance-proof artifact that distinguishes L5 — its content, emission cadence, and independent-verification procedure — is not fully specified in this version. L5 is therefore forward-looking and not independently assessable under v1.0.1; a system MUST NOT claim L5 until the steward publishes the L5 evidence criteria (Part VII §31). Levels L0–L4 are fully assessable in v1.0.1.*

> *Note (AQL status, normative). The Agent Qualification Layer (§4.9.2) is **RECOMMENDED (SHOULD)** at L4 for deployments governing agent subjects with autonomous operational authority, and **REQUIRED** at L5. It is intentionally not REQUIRED at L4: the safety guarantee of L4 rests on the structural enforcement of stages 1–4 (RBAC admission, grounding, evaluation, execution-boundary enforcement), and AQL is monotone — it can only restrict reachability, never widen it (§4.9.2), so it adds no structural safety that L4 does not already provide. AQL's gaming-resistance is also not yet independently validated (§4.9.2, §29.5). It is therefore positioned as a strongly-recommended maturity control at L4 that becomes mandatory at the self-verifying L5, where continuous qualification re-assessment is integral. A deployment that governs agent subjects and does not enforce AQL at L4 MUST record the resulting residual (gaming/unqualified-capability exposure under TH-1) in the Residual Risk Register (C-24).*

---

### 28.3 Conformance Level Requirements Matrix

| Requirement | L0 | L1 | L2 | L3 | L4 | L5 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| `C5` audit record (I3, I6) | — | partial | ✔ | ✔ | ✔ | ✔ |
| Deny produced (`C2`) | — | advisory | ✔ | ✔ | ✔ | ✔ |
| Refusal enforced (I5, `C6`) | — | — | ✔ | ✔ | ✔ | ✔ |
| ECC compilation + signing (`C7`) | — | — | ✔ | ✔ | ✔ | ✔ |
| All actions traverse OCP; P4 at network layer | — | — | — | ✔ | ✔ | ✔ |
| Policy authority exclusivity (I4) | — | — | partial | ✔ | ✔ | ✔ |
| RBAC subject authorization (§4.9.1) | — | — | SHOULD | ✔ | ✔ | ✔ |
| AQL qualification gate (§4.9.2, agent subjects) | — | — | — | — | SHOULD | ✔ |
| All invariants registered + enforced (I1) | — | — | — | subset | ✔ | ✔ |
| Trajectory analysis active (`C4`, T8) | — | — | — | — | ✔ | ✔ |
| Threat assessment complete — all 11 classes (Part V docs) | — | — | — | ✔ | ✔ | ✔ |
| Executed negative tests pass (§27.3, §29.3) | — | — | — | — | ✔ | ✔ |
| Continuous self-emitted conformance proof | — | — | — | — | — | ✔ |

> *Note. "partial" and "subset" indicate that the requirement is present for a defined portion of the governance boundary or invariant set, not in full. A level is achieved only when every cell at that level and below is satisfied for the entire stated governance boundary.*

> *Note (determinism). I2 (Determinism, Part II §5.2) is a property of every `C2.eval` decision and applies from L1 upward wherever `C2` produces decisions; its inclusion within "all I1–I8" at L4 reflects full invariant registration, not the first appearance of determinism.*

---

### 28.4 Level Determination

The conformance level of a system within a governance boundary is the highest level L*n* for which every requirement at L0…L*n* (§28.3) is satisfied by reproducible evidence (Chapter 29). A system that satisfies some but not all requirements of a level holds the highest fully-satisfied level; partial satisfaction of a higher level confers no claim. Where a deployment governs both human and agent subjects, the AQL requirements at L4/L5 apply to the agent-subject portion of the governance boundary; the human-subject portion is assessed against the remaining requirements.

---

### 28.5 Adoption Status Vocabulary

The conformance levels L0–L5 (§28.2) describe a *system's* assessed enforcement maturity and are claimable only on reproducible evidence (Chapter 29). Organizations also need a vocabulary to describe **progress toward** conformance without asserting a level they have not evidenced. The following **adoption statuses** serve that purpose. They are descriptive self-declarations of an adoption journey; they are **NOT conformance levels** and MUST NOT be presented as such.

| Status | Meaning |
|---|---|
| **CROA-aware** | The organization is studying CROA; no architecture or conformance claim. |
| **CROA-aligned** | Some CROA principles or components are implemented, but no conformance is claimed. |
| **Targeting L2** | Refusal-based governance under implementation. |
| **Targeting L3** | Execution-boundary enforcement and full OCP traversal under implementation. |
| **Targeting L4** | Constructive-enforcement pilot with evidence capture underway. |
| **L4 Conformant** | Independent reproducible evidence supports L4 (a conformance claim, per Chapter 29). |
| **L5 Candidate** | Continuous self-evidence (§28.2, L5) being piloted; L5 is not independently assessable in v1.0.1 (§28.2 note). |

Normative constraints on adoption statuses:

- An adoption status MUST NOT be described as, or substituted for, a conformance level. Only **L4 and above**, substantiated per Chapter 29, MAY be described as "CROA-conformant" without qualification.
- A **"Targeting L*n*"** status MUST NOT be abbreviated to "L*n*" in any public statement; it describes work in progress, not an achieved level.
- A **"CROA-aligned"** claim MUST cite the specific Parts and requirements implemented and MUST state known deviations (consistent with the derivative-work rules in Part VII §33.3).
- An adoption status carries no evidentiary weight in a Chapter 29 assessment; an assessor evaluates only against the L0–L5 requirements.

---

### 28.5.1 CROA Pilot Path — 30 / 60 / 90 Days

> *Non-normative. This section describes a structured path from no CROA governance to readiness for L4 conformance assessment. It does not confer conformance at any stage. The adoption statuses it produces are as defined in §28.5 above: descriptive self-declarations, not conformance levels.*

Enterprise adoption of CROA need not start at full L4. The pilot path below gives a structured 90-day progression that allows an organization to build governance capability incrementally, understand the framework concretely through a single agentic use case, and reach a state from which an independent L4 assessment is realistic — without claiming conformance prematurely.

**This path does not produce conformance.** Completing Days 0–90 produces readiness to *pursue* a formal L4 assessment. The assessment itself requires an independent assessor working from the evidence standards in Chapter 29.

---

#### Days 0–30 — CROA-aware Mapping

**Purpose.** Understand whether CROA applies to a target use case and produce an initial architectural picture.

**Activities.**

- Identify one agentic use case where governance failure would be consequential. Do not attempt to govern the entire enterprise in the first pilot.
- Define the governance boundary: which agents, which systems, which action classes are in scope; what is explicitly out of scope and why.
- Define 3–5 candidate invariants. Express each one precisely: which action class does it constrain, what is the condition, what evaluability class (E1/E2/E3) does it fall into?
- Classify action types: for each action class in scope, identify what class of governed action it represents and what reversibility/consequence class (R0–R4) applies.
- Inventory existing systems: which existing systems could play each of the C1–C7 roles? Where are the gaps?
- Produce an initial Operational Envelope document: a plain statement of what the CROA-governed perimeter would look like if implemented.

**Output status:** `CROA-aware` — the organization has studied CROA and mapped a use case against the framework.

**Conformance claim:** None. No CROA conformance is claimed at the end of Days 0–30.

---

#### Days 31–60 — CROA-aligned Pilot

**Purpose.** Implement one governed action class, produce the first C5 evidence, and run the first negative tests.

**Activities.**

- Implement one governed action class end-to-end: at minimum, C2 (policy evaluation), C5 (evidence recording), and C6 (execution boundary enforcement) for that action class.
- Implement a minimal C5 event log: produce PERMIT and DENY events for governed actions. Verify that the hash chain is intact.
- Define one deny path: configure the policy so that at least one action class in scope produces a DENY under defined conditions.
- Define one permit path: verify that a well-formed, compliant action produces a PERMIT and an ECC.
- Define one context failure: submit a request referencing an entity absent from the Federated Context Registry. Verify that C3 produces CONTEXT_FAILURE and C2 is not invoked.
- Run one negative test: NT-001 (non-ECC execution blocked). Verify that the expected C5 evidence appears.

**Output status:** `CROA-aligned pilot` — the organization is running a CROA-aligned pilot using core CROA concepts, with initial evidence production.

**Conformance claim:** None. The pilot uses CROA concepts; it is not L4-conformant. The phrase "CROA-aligned pilot" MUST NOT be used as a substitute for a conformance claim.

---

#### Days 61–90 — Targeting L4

**Purpose.** Close the gap to full structural enforcement and assess readiness for independent L4 evaluation.

**Activities.**

- Enforce the execution boundary at the network layer (P4): ensure that C6 operates at the network layer, not only at the application layer. An agent must not be able to submit operations directly to governed systems without traversing C6.
- Introduce ECC compilation (C7): ensure that all permitted actions produce an ECC before any operation is admitted. Validate ECC signature, expiry, and single-use enforcement.
- Ensure C6 blocks non-ECC operations: run NT-001, NT-002, NT-003 (non-ECC, expired ECC, replay). All three must produce the expected C5 evidence.
- Implement C4 for at least one trajectory profile: if any registered invariant uses TP-W, TP-C, or TP-X, implement the corresponding trajectory analysis and run NT-006 (progressive trajectory alert and deny).
- Produce a conformance evidence pack: a structured C5 evidence set covering the reference negative tests of Appendix Q, at least one PERMIT path, at least one DENY path, and at least one TRAJECTORY_ALERT (if applicable). See [Appendix Q](../appendices/appendix-q-evidence-pack-and-reference-negative-tests.md).
- Assess gaps against L4 criteria: review each of the 12 Part II conformance requirements and identify which are satisfied, which are partially satisfied, and which are not yet addressed.

**Output status:** `Targeting L4` — the design is being prepared for L4 evidence. The organization can describe specific criteria it has satisfied and specific gaps it is closing.

**Conformance claim:** None yet. At the end of Days 61–90, the organization may be ready for a formal L4 assessment by an independent assessor. The independent assessment, not the completion of this pilot path, produces the L4 conformance finding.

---

#### Pilot path adoption status summary

| Status | Meaning | Allowed public claim |
|---|---|---|
| `CROA-aware` | Organization has mapped CROA against a use case | "We are evaluating CROA" |
| `CROA-aligned pilot` | Pilot is using CROA concepts with initial evidence | "We are running a CROA-aligned pilot" |
| `Targeting L4` | Design is being prepared for L4 evidence; gaps identified | "We are targeting CROA L4" |
| `L4 Conformant` | Independent assessor has verified L4 criteria from C5 evidence | "This scoped implementation is CROA L4-conformant" (cite version, boundary, assessor) |

No claim in the first three rows MAY be phrased so as to imply CROA conformance. The fourth row requires independent assessment (Chapter 29).

---

### 28.6 What L4 Conformance Does and Does Not Claim

The CROA conformance threshold L4 ("Constructive Enforcement") is a strong but *bounded* claim. Because the central CROA proposition — unsafe execution paths are structurally unreachable — can be over-read, this section states the boundaries of an L4 conformance claim normatively, so that the label "CROA-conformant" is not extended beyond what an assessment establishes. This section restates and conditions the T1 claim scope (Part I, Chapter 3, Tenet T1, "Precise scope of the claim").

**What L4 conformance DOES claim.** For the stated governance boundary, on reproducible evidence (Chapter 29):

- Every governed action reaches a governed external system only as a `C7`-compiled, `C6`-validated ECC-derived operation (I1, P4); no governed action bypasses the OCP.
- Within the modeled action space and under the registered invariant set, no sequence of governed actions reaches a registered-invariant-violating state except through a valid, signed authorization (T1, I1).
- Every governance decision — permit, deny, authorization, context failure — is durably and tamper-evidently recorded (I3, I6), and a DENY is a governance success, not an incident.
- Admission controls (subject authorization §4.9.1, and for agent subjects the AQL §4.9.2) gate which requests enter the pipeline; they can only restrict, never widen, reachability.

**What L4 conformance DOES NOT claim.**

- **It does not claim semantic safety of the content of a permitted action.** Authorization is over a *typed action* (e.g., `code.write` with parameters), not over the full semantic effect of what is written. A permitted action may carry effects (e.g., a latent backdoor in generated code) that neither `C2` nor `C3` evaluates. This is the declared residual TH-10.A (Part V §26). L4 bounds the *action space*, not the *effect space*.
- **It does not certify the completeness of the enterprise's invariant registry.** Registry completeness against the governance boundary is enterprise-attested and assessor-reviewed (§28.2), not established by CROA. An unregistered hazard is outside the guarantee, and any known coverage gap is recorded in the Residual Risk Register (C-24).
- **It does not guarantee against effects produced through channels outside the modeled execution boundary** — undeclared side effects (TH-9), or execution-layer prompt injection of permitted actions (TH-10.A), or out-of-band channels where P4 is not network-enforced (TH-3 residual). These are declared residuals, not covered states.
- **It does not assert that approximated invariant evaluations are exact.** Where an invariant's evaluability class is "semantic-approximated" (§2.6, Part I), residual false negatives are part of the claim's honest scope and MUST be declared per the invariant's evaluation-method record.
- **It is not transitive to other deployments, model versions, or configurations.** An L4 assertion is scoped to the assessed governance boundary and configuration fingerprint.

A public or contractual statement of CROA conformance MUST NOT be phrased so as to imply any of the "does not claim" items above. The conditioned T1 formulation (Part I, Chapter 3, Tenet T1) is the canonical wording.

---

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 28**

- §28.1: A conformance claim MUST name the governance boundary, MUST be cumulative, and MUST be established by reproducible evidence available to an independent assessor without relying on the implementing party's active cooperation or interpretation (see §29.4).
- §28.2: L4 (Constructive Enforcement) is the CROA conformance threshold. A system described as "CROA-conformant" without qualification MUST satisfy L4. For deployments governing agent subjects, the Agent Qualification Layer (§4.9.2) is RECOMMENDED (SHOULD) at L4 and REQUIRED at L5 (AQL is monotone and adds no structural safety beyond L4; see the AQL status note).
- §28.3–§28.4: A level is achieved only when every requirement at that level and below is satisfied for the entire stated governance boundary. Partial satisfaction of a higher level confers no claim.
- §28.5: Adoption statuses (CROA-aware, CROA-aligned, Targeting L*n*, L5 Candidate) are NOT conformance levels and MUST NOT be presented as such; only an evidenced L4+ assertion MAY be described as "CROA-conformant" without qualification.
- §28.6: An L4 conformance claim is bounded — it claims structural unreachability *within the modeled action space, under the registered invariant set, given network-enforced P4*, and does NOT claim semantic safety of permitted-action content, completeness of the invariant registry, coverage of declared residuals, exactness of approximated evaluations, or transitivity to other deployments/configurations. Conformance statements MUST NOT imply any of these.

**Cross-references.** Chapter 28 depends on I1–I8 (Part II Ch 5), the components and admission model (Part II Ch 4, §4.9.1–§4.9.2), P1–P7 (Part IV §18.1), and the threat/negative-testing requirements (Part V Ch 26–27). Chapter 29 specifies assertion and evidence. Chapter 30 distinguishes system conformance from organizational maturity.

---

## Chapter 29. Conformance Assertions and Evidence

**Chapter abstract.** This chapter specifies how a CROA conformance level is *asserted*, what *evidence* substantiates the assertion, how *negative testing* is aggregated as a conformance gate, and what *independence* an assessment requires. It also establishes the validation discipline for an in-deployment framework: a conformance level is a finding about executed behavior, not about design intent. Chapter 29 depends on the method deliverables (Part III), the threat negative-testing requirements (Part V §27.3), and the conformance levels (Chapter 28).

---

### 29.1 Making a Conformance Assertion

A CROA conformance assertion is a signed statement that MUST contain:

1. **Subject** — the system and the named governance boundary (Part I §2.3) to which the assertion applies.
2. **Claimed level** — one of L0–L5 (§28.2).
3. **Assessment basis** — the audit period, the deployment model(s) in scope (Part IV), and the registered invariant set version.
4. **Assessor** — the party that verified the assertion and the basis of their independence (§29.4).
5. **Evidence reference** — the Conformance Evidence Record (C-32) that substantiates the claim (§29.2).

An assertion that omits any element is incomplete and MUST NOT be recognized. A conformance assertion is itself a governance artifact and SHOULD be signed by the assessor and retained.

---

### 29.2 Evidence Requirements

A conformance assertion at L*n* MUST be substantiated by the following evidence, available to the assessor from sources that do not depend on the implementing party's active cooperation or interpretation (T10; see §29.4):

| Evidence | Source artifact | Substantiates |
|---|---|---|
| Requirements Traceability Matrix | RTM (Part III) | That enterprise governance requirements map to registered invariants and controls |
| Threat Assessment | C-22 (Part III §10.1; Part V) | That all eleven threat classes were assessed (L4+) |
| Mitigation Map | C-23 | That each relevant threat maps to an implemented structural mitigation (§27.1) |
| Residual Risk Register | C-24 | That residual conditions are documented with management approach |
| TH-1 Detection Specification | C-25 | That Technical Sycophancy detection addresses all six patterns |
| Test Plan + executed results | C-29 → C-32 | That positive, negative (§27.3), TH-1, and — for agent subjects that enforce AQL — AQL-gate tests were executed and passed (L4+) |
| `C5` extracts | `C5` (Part II §4.7) | Decision reconstructability (I3), chain integrity (I3/I6), session lifecycle, Governance Success classification |
| ECC integrity sample | `C7` ECCs + `C5` permit events | That sampled ECCs carry a valid `C7` signature, reference a `C5` permit event, bind the `C2.eval` decision and the policy/invariant-set versions, and are consistent with the `C7` active ECC registry (L2+) |
| Deployment conformance | Part IV evidence | That P1–P7 hold for the governance boundary, in particular P4 at the network layer (L3+), and — in production — the availability engineering P7 requires of the `C5` durable-commit path and the shared redemption authority |
| Conformance Evidence Record | C-32 | The accumulated, signed body of the above |

The **Conformance Evidence Record (C-32)** is the single artifact an assessor consults to verify a level. Its template is given in the Part VI appendix. At L4 and above, the evidence MUST include *executed* test results — not test plans alone — and `C5` extracts demonstrating that the negative tests produced the required `DENY` / `EXECUTION_BLOCKED` / `ADMISSION_REJECTED` / `TRAJECTORY_ALERT` outcomes.

---

### 29.3 Negative Testing Requirements

Structural enforcement is demonstrated by showing that unsafe inputs are *prevented*, not only that safe inputs are permitted. For L4 and above:

- For each threat class assessed as relevant (Part III §10.2), the Test Plan MUST include at least the minimum negative test case specified in Part V **§27.3**, and the executed result MUST be present in the Conformance Evidence Record.
- The **TH-1 negative tests** (urgency/authority bypass framing → `DENY`; convergent trajectory → `TRAJECTORY_ALERT` then `DENY`) MUST be present regardless of TH-1 severity rating (Part V; Part III §10.2).
- For deployments governing agent subjects that enforce AQL (REQUIRED at L5; SHOULD at L4), the **AQL qualification-gate negative tests** (expired verdict → `QUALIFICATION_EXPIRED`; configuration mismatch → `QUALIFICATION_CONFIG_MISMATCH`; forged/unsigned verdict not accepted) MUST be present (Part V §27.3, AQL note in §26).
- For deployments that **implement multi-agent delegation** (Appendix L, normative where implemented), the **delegation negative tests** — scope-widening, incomparable/non-canonical scope, chain-forgery, and depth/expiry breach (each → fail-deny), and a cross-agent violating sequence (→ `TRAJECTORY_ALERT` then `DENY`) — MUST be present and passed (Appendix L §L.4). Delegation is OPTIONAL; a deployment that performs no delegation is unaffected by this bullet.
- The **ECC-integrity negative tests** MUST be present at L4: (a) a forged `C7` signature → `EXECUTION_BLOCKED` (`ECC_INTEGRITY_INVALID`); (b) an expired ECC → `EXECUTION_BLOCKED`; (c) an ECC presenting operations outside `ecc.authorization_scope` (scope expansion) → blocked; (d) an ECC carrying a stale `ecc.invariant_set_version` that conflicts with a since-registered invariant → blocked with a recompilation directive (Part II §4.8); (e) an unauthorized ECC-compilation attempt with no valid `C2.eval` permit → not admitted to the `C7` active ECC registry and blocked at `C6`; and (f) a re-presented, still-valid but already-redeemed ECC (replay) → `EXECUTION_BLOCKED` (`ECC_ALREADY_REDEEMED`), confirming single-use enforcement (Part II §4.8).
- The **concurrent double-redemption test** MUST be present at L4: two presentations of the same `ecc.id` — and, for a governed exception, of the same `ecc.auth_ref` — issued **simultaneously** to two `C6` instances MUST admit **at most one** `EXECUTION_AUTHORIZED`, the loser receiving `EXECUTION_BLOCKED` with `ECC_ALREADY_REDEEMED` or `AUTHORIZATION_ALREADY_REDEEMED`. This is the conformance expression of the atomic linearizable redemption requirement of Part II §4.8, and it is tested by NT-007 step 4 (Appendix Q). A deployment operating a per-instance or per-gateway redemption registry cannot pass it and is non-conformant.
  - *Note on interpreting a negative result.* A single passing run of a concurrency test does not establish the property — an interleaving that would fail may simply not have occurred. The test MUST be run repeatedly under contention, and the assessor SHOULD record the number of trials in the Conformance Evidence Record. Where an implementation can instead evidence that redemption is a single compare-and-swap against one linearizable authority (by design review of the redemption path), that evidence is stronger than any finite number of passing runs and SHOULD be recorded alongside it.
- The **authority non-expansion tests** MUST be present at L4: NT-008 (Appendix Q), covering widening of an action class, a target, a parameter constraint, and a validity window, and the composition case. Steps applicable only to delegation are recorded as *not applicable* where the deployment performs no delegation.
- The **cumulative-aggregate concurrency test** MUST be present at L4 for any deployment enforcing a `TP-C` or `TP-X` invariant: two governed actions contributing to the same accumulation key, presented concurrently against an aggregate one increment below its threshold, MUST NOT both be admitted (Part II §4.6.3). The note on interpreting a negative result above applies equally here.
- A negative test that does not produce the required structural outcome is a conformance failure at L4, not a deferrable finding.

Negative testing is the operational expression of T1: a conformance claim that unsafe paths are unreachable is only credible if it has been demonstrated that representative attempts to reach them are structurally blocked.

---

### 29.4 Independent Assessment

Conformance is meaningful only if it can be verified by a party that did not build the system (T10). This requires separating two senses of "independent of the implementing party" that the framework otherwise risks conflating — *cooperation* and *read access* — because the model relies on the first being unnecessary and the second being granted. ("From `C5` alone," used elsewhere in this Part, is the decision-reconstructability property of the first bullet below; it is not a claim that a *level* can be established without reading any other artifact.)

- **Decision reconstructability is from `C5` alone.** Any individual governance decision — permit, deny, authorization, context failure — MUST be reconstructable from the `C5` audit record alone, without the governed agent's internals, the implementing organization's narration, or the agent's operating environment (I3). This is the property that makes the evidence self-supporting.
- **Verifying a *level* uses the evidence set, with read access, without cooperation.** Establishing a conformance level (as opposed to reconstructing one decision) draws on the full Conformance Evidence Record (C-32) and its constituent artifacts (§29.2) — the RTM, the Threat Assessment and its companions (C-22…C-25), and the executed test results — together with the cross-check sources named below. The assessor MUST be granted **read access** to these sources. Read access is distinct from **cooperation**: the assessor MUST be able to reach the conclusion *without relying on the implementing party's interpretation, attestation, narration, or active assistance*. The artifacts speak for themselves; the audited party is not asked to vouch for them.
- **Read-access cross-checks beyond `C5`.** A few criteria cannot be settled from `C5` in isolation and require read access to the implementer's operational records — specifically: (a) the **governed systems' own access/effect logs**, to corroborate execution-boundary integrity (P4) independently of `C5`'s self-report; (b) the **incident-management records**, to confirm that DENY decisions were classified as Governance Successes and not quietly re-filed as incidents (Part I §2.1); and (c) the **`C4` operational logs**, to confirm trajectory-analysis availability across the audit period. To preserve independence, these sources MUST be tamper-evident or independently corroborable (for example, cross-hashed against `C5`, or collected under the assessor's control), so that granting read access does not reduce to trusting the audited party. A criterion that can be met only by the audited party's *assertion*, with no readable corroborating artifact, is not assessable and MUST be reported as not assessable rather than accepted.
- **Self-assessment is labelled.** Vendor, implementer, or agent assertions of conformance are not evidence of conformance (T10). The assessor's independence basis MUST be stated in the assertion (§29.1). An assessment performed by the implementing party is a *self-assessment* and MUST be labelled as such; it does not satisfy the independence expectation for an external conformance claim.

---

### 29.5 Validation and the Evidence Base

CROA conformance is a finding about *executed behavior*. The architectural thesis underlying this framework — that execution-layer enforcement preserves invariants under adversarial pressure where probabilistic and multi-agent approaches do not, and that Technical Sycophancy (TH-1) is a real failure mode — has **directional support** from the founding comparative study (see the *Founding validation study* note below). That support is bounded in three specific ways, each stated in the note and none of which this sentence may be read as overriding: the study was conducted by the framework's originators rather than an independent assessor; it evaluated the earlier four-layer model rather than the seven-component OCP, the L0–L5 levels, and the RBAC/AQL admission model of this version; and its authors characterize the results as directional and not statistically generalizable. The thesis is therefore **supported and not established**, and no statement of CROA's evidence base may describe it as empirically validated without those three qualifications attached. That support is *validation* evidence in any case; it is distinct from *conformance* evidence, which is a per-deployment finding assessed independently against the levels of Chapter 28. This framework specifies the conformance model in full but is published ahead of a public **conformance** evidence base. The following discipline applies and is the basis for the evidence-capture structure in the Part VI appendix:

- A conformance assertion at L4 or above MUST reference executed evidence (§29.2); design intent, specifications, and code review alone do not substantiate L4.
- An enterprise establishing CROA for the first time SHOULD validate its deployment through a **pilot** before asserting conformance: a bounded governance boundary, a registered invariant subset, an executed negative-test battery, and a populated Conformance Evidence Record. The pilot/validation plan template is given in the Part VI appendix.
- Until an enterprise has populated a Conformance Evidence Record from a real deployment, it MUST describe its status as *"targeting L<n>"* rather than *"L<n>-conformant."*

> *Note (founding validation study). The founding study — Y. Durand & D. Smith, "From Orchestrated Agents to Enforced Systems: An RFC-Driven Architecture for Deterministic Governance in Agentic AI Workflows" [publication venue, year, and DOI to be completed in the published reference list] — reports a controlled comparison of a probabilistic assistant, a multi-agent system, and the CROA reference implementation (Riven) across three adversarial scenario classes (51 runs total), in which the CROA-enforced system preserved all tested invariants while the comparison systems did not. The study provides directional support for the architectural thesis and the threat phenomenology of this framework (notably TH-1, Technical Sycophancy) and is the empirical origin of Governance Success, the three execution modes, and the Federated Context Registry. It introduced the architecture under its earlier name, "Cognitive RFC Orchestration Architecture"; the canonical name is now **Constrained Reachability Orchestration Architecture**. The study does **not** constitute a Part VI conformance assertion: (a) it was conducted by the framework's originators, not an independent assessor (T10); (b) it evaluated the earlier four-layer model rather than the seven-component OCP, the L0–L5 levels, and the RBAC/AQL admission model of this version; and (c) its authors characterize the results as directional, not statistically generalizable. An independent L4 conformance assessment against this version remains to be produced via a conformance pilot. The conceptual delimitation of Technical Sycophancy from adjacent prior concepts — behavioral sycophancy, specification gaming / reward hacking, excessive agency, and prompt injection — is now stated in Part V §26 (TH-1, "Delimitation"). Publishing this founding study with a citable DOI and carrying that delimitation in its related-work section is an external, pre-ratification action (specialist-report item 8) that the editorial process cannot itself discharge; the venue/year/DOI placeholder above is retained until publication.*

> *Note (AQL validation status). The Agent Qualification Layer (§4.9.2) is **RECOMMENDED (SHOULD) at L4 and REQUIRED at L5** for deployments governing agent subjects with autonomous operational authority (the conformance position is fixed in §28.2, and this note states only its validation rationale). Its qualification batteries are evaluations of non-deterministic agents and are therefore subject to gaming (Goodhart) effects whose practical resistance has not yet been empirically validated against a public benchmark (see the AQL attack-surface note, Part V §26). Enterprises MUST treat AQL gaming-resistance as an open validation item and document it in the Residual Risk Register. The structural safety guarantee (T1) does not depend on AQL: AQL gates admission only, and every admitted request is still fully governed by C2.eval and the execution boundary. This note will be revised when empirical validation evidence exists.*

---

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 29**

- §29.1: A conformance assertion MUST contain subject, claimed level, assessment basis, assessor, and an evidence reference; an incomplete assertion MUST NOT be recognized.
- §29.2: An assertion MUST be substantiated by the listed evidence in a Conformance Evidence Record (C-32). At L4+, evidence MUST include executed test results and corroborating `C5` extracts.
- §29.3: At L4+, the minimum negative test cases (§27.3), the TH-1 tests, any conditional Appendix L delegation tests, and — for agent subjects that enforce AQL — the AQL-gate tests MUST be executed and pass; a failed negative test is an L4 conformance failure.
- §29.4: Any individual governance decision MUST be reconstructable from `C5` alone (I3); verifying a *level* additionally requires **read access** — without the implementing party's *cooperation* (interpretation, attestation, assistance) — to the Conformance Evidence Record and the named cross-check sources (governed-system access logs for P4, incident records for Governance Success classification, `C4` logs), which MUST be tamper-evident or independently corroborable; a criterion meetable only by the audited party's unsupported assertion is not assessable. Vendor assertion is not evidence; self-assessments MUST be labelled.
- §29.5: An L4+ assertion MUST reference executed evidence; absent a populated Conformance Evidence Record, status MUST be described as "targeting L<n>". AQL gaming-resistance MUST be tracked as an open validation item.

**Cross-references.** Chapter 29 depends on the method deliverables and artifact catalog (Part III), the negative-testing minimums (Part V §27.3), and the conformance levels (Chapter 28). The Conformance Evidence Record (C-32) and the templates in the Part VI appendix are the operational basis for §29.2.

---

## Chapter 30. Organizational Maturity Model

**Chapter abstract.** Conformance levels (Chapter 28) describe a *system*. Organizational maturity describes the *enterprise's practice* of governing agentic AI with CROA — its ability to produce, operate, and sustain conformant systems repeatably across teams and over time. A high-conformance system built once by heroics is not the same as an organization that reliably produces L4 systems. This chapter specifies a five-dimension maturity model and its stages. It is distinct from, though correlated with, system conformance.

---

### 30.1 System Conformance versus Organizational Maturity

A system's conformance level answers "how completely does *this deployment* enforce structural governance?" Organizational maturity answers "how reliably can *this enterprise* produce and sustain such deployments?" The two are correlated but independent: an organization may operate one L4 system while lacking the practice to produce a second, and a mature organization may temporarily operate a system at L3 by deliberate, documented choice. Conformance is assessed per system; maturity is assessed per organization.

---

### 30.2 Maturity Dimensions

Organizational maturity is assessed across five dimensions, each scored on the stage scale in §30.3:

| Dimension | What it measures |
|---|---|
| **Governance architecture practice** | Repeatable execution of the CROA-PaC (Part III): phase discipline, role clarity, deliverable completeness across deployments |
| **Policy lifecycle practice** | Discipline of `C1` policy and role/qualification-artifact issuance, versioning, signing, and Policy Update (§7.2) change governance (I4) |
| **Threat practice** | Routine threat assessment (all eleven classes), maintained TH-1 detection, negative-test coverage, residual-risk management |
| **Evidence discipline** | Completeness and routine use of `C5` evidence and Conformance Evidence Records; treating deny decisions as Governance Successes, not incidents |
| **Qualification practice** | For agent subjects: maintained qualification batteries, recertification on configuration change, and gaming-resistance review (§4.9.2) |

---

### 30.3 Maturity Stages

| Stage | Name | Characteristic |
|---|---|---|
| **M0** | Ad hoc | Governance is project-specific and personality-dependent; no repeatable practice |
| **M1** | Defined | The CROA-PaC and artifacts are documented and followed for new deployments |
| **M2** | Managed | Deployments are measured against conformance levels; evidence is routinely produced and reviewed |
| **M3** | Integrated | Governance is integrated with enterprise risk, security, and change management; Policy Update (§7.2) operates continuously |
| **M4** | Optimizing | The organization improves its invariant coverage, batteries, and detection from operational evidence; it sustains L4 systems and is progressing deployments toward L5 |

Maturity stages are assessed per dimension; an organization's overall maturity is the lowest dimension stage that is fully satisfied, with per-dimension stages reported alongside. Maturity assessment is advisory: it informs investment and roadmap decisions and is not a conformance claim.

---

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 30**

Chapter 30 is primarily descriptive. The following applies:

- Organizational maturity (this chapter) MUST NOT be represented as, or substituted for, a system conformance level (Chapter 28). A maturity stage is not a conformance claim.

**Cross-references.** Chapter 30 depends on the method (Part III), the conformance levels (Chapter 28), and the evidence discipline (Chapter 29). The qualification-practice dimension depends on §4.9.2 (Part II).

---

## Part VI Conformance Requirements

Part VI is the conformance model itself; "conformance with Part VI" means that a conformance *assertion* about a system is well-formed and substantiated. An assertion conforms with Part VI if and only if an independent assessor can verify all of the following:

**Level claim well-formedness.** The assertion contains all elements required by §29.1 and names a governance boundary. Verifiable by: inspection of the assertion.

**Cumulative satisfaction.** Every requirement at the claimed level and below (§28.3) is satisfied for the entire stated governance boundary. Verifiable by: the Conformance Evidence Record cross-referenced with `C5`.

**Executed evidence at L4+.** For a claim of L4 or above, the Conformance Evidence Record contains executed negative-test results (§29.3) and corroborating `C5` extracts, not test plans alone. Verifiable by: Conformance Evidence Record and `C5` inspection.

**Independence.** The assessor's independence basis is stated, and the claimed conclusion is reachable from the Conformance Evidence Record, `C5`, and the named cross-check sources (§29.4). Verifiable by: re-derivation of the conclusion from the evidence.

**Honest status.** Where a populated Conformance Evidence Record does not yet exist, the status is described as "targeting L<n>", not as conformance (§29.5). Verifiable by: comparison of the asserted status against the evidence present.

A system that fails any single criterion does not have a recognized Part VI conformance assertion. Partial conformance is not recognized.

---

## Appendix VI-A — Artifact Templates (Informative)

> *This appendix is non-normative. It provides skeletal templates for the conformance-relevant artifacts. Templates are starting points; the normative content of each artifact is defined in the referenced sections. Fields in angle brackets are placeholders to be populated from a real deployment — they are intentionally empty in this framework, which carries no deployment evidence of its own.*

**Requirements Traceability Matrix (RTM).**
`| Enterprise requirement | Source (policy/regulation) | Registered invariant(s) | Enforcing component(s) | Test case(s) |`

**Threat Assessment (C-22).**
`| Threat class (TH-1…TH-11) | Relevant? (Y/N + rationale) | Inherent severity (§27.1.1) | Mitigating controls (§27.1) | Residual condition |`

**Mitigation Map (C-23).**
`| Relevant threat | Structural mitigation (invariant/component) | Implemented in (design ref) | Verified by (test case) |`

**Test Plan / Conformance Evidence Record (C-29 → C-32).**
`| Test ID | Type (positive/negative/TH-1/AQL/boundary) | Input | Expected structural outcome | Executed result | C5 event ref | Pass/Fail |`

**Pilot / Validation Plan (for §29.5).**

```
Governance boundary:        <systems, agents, action classes in scope>
Registered invariant subset: <invariant IDs>
Deployment model:           <DM-1 … DM-5>
Target conformance level:   <L3 / L4>
Negative-test battery:      <TH classes + AQL gate, per §27.3 / §29.3>
Evidence to capture:        <C5 extracts, executed test results, C-32>
Exit criterion:             <Conformance Evidence Record populated; level asserted>
Status:                     targeting L<n>   (until evidence is populated)
```

**Conformance Assertion (§29.1).**

```
Subject:          <system + governance boundary>
Claimed level:    <L0 … L5>
Assessment basis: <audit period, deployment model(s), invariant set version>
Assessor:         <party + independence basis>
Evidence:         <Conformance Evidence Record reference>
Signature:        <assessor signature>
```

---

*End of Part VI — Conformance and Maturity.*
*Continues in Part VII — Governance of the Standard (Chapter 31: Lifecycle of the Standard).*
