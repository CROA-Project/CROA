---
tags:
  - croa_foundation
---

# Appendix A — Lexicon

**CROA Framework v1.0.1.1 · Normative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index. This appendix is referenced from Part I, Chapter 2.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The

The lexicon below alphabetizes the terms defined in Part I §2.1–§2.3 — together with a small number of cross-Part terms of standard-wide importance (e.g., the Orchestration Control Plane and the Agent Surface), each carrying its defining section — with a summary definition and its source section. The lexicon is **normative**: any discrepancy between a definition in its authoritative source section and its entry here is a document error to be resolved in favor of the source section until a corrigendum is issued. Component (`Cn`) entries point to their full specification in Part II, Chapter 4.

| Term | Summary definition | Source |
|---|---|---|
| **Agent Qualification Layer (AQL)** | Admission-stage control that administers qualification examinations, scores compliance, tracks expiry, validates configuration fingerprint, and produces the qualification verdict; distinct from C1–C7. For agent subjects with autonomous operational authority it is RECOMMENDED (SHOULD) at L4 and REQUIRED at L5; OPTIONAL otherwise (canonical statement: §1.5). | §1.5; §2.2; §4.9.2 |
| **Agent Surface** | The contract exposed to governed agents; it authenticates the subject, hosts the admission-stage controls (RBAC, §4.9.1; AQL, §4.9.2), and is the sole path by which requests reach the OCP. Not one of the seven `Cn` components. | §2.2; §4.9 |
| **Agentic system** | A computational system that selects and executes actions on behalf of a subject, where selection is informed by a generative or inferential model. | §2.1 |
| **AMBIGUOUS verdict** | An invariant-evaluation outcome in which an evaluator (E2/E3) cannot decide satisfaction within its declared method and budget; under the fail-deny rule it resolves to DENY. The AMBIGUOUS→DENY rate is a governed, measured quantity ("governance friction"). | §2.6 |
| **Audit** | The authoritative record of governance decisions, sufficient to reconstruct any decision. | §2.1 |
| **Audit and Provenance Store (`C5`)** | The component that records every decision and its evidence in append-only, tamper-evident, replayable form. This is the **single normative term** for the component; "Evidence Ledger" is the non-normative Layer-6 label used only in the architectural overview (the same registry, not two stores). | §2.2; §4.7 |
| **Authorized action class** | A category of governed action (a `gar.type`) that a role permits its holders to submit. | §2.2; §4.9.1 |
| **Blocking Mode** | Execution mode in which an invariant-violating action with no authorization yields DENY. | §2.1 |
| **Collaborative Compliance Failure** | Failure mode in which an agent acknowledges a constraint yet the decoupled execution pipeline proceeds to violate it. | §2.1 |
| **Execution Change Contract (ECC)** | A compiled, content-addressed, tamper-evident execution commitment produced by the Contract Compiler (`C7`); the unit of authorized execution. Named "RFC (Request for Change)" in drafts before v1.0.1.0; renamed to avoid collision with IETF RFCs. | §2.1; §4.4 |
| **Constrained Execution Mode** | Execution mode in which an invariant violation proceeds within the bounded scope of a valid `C1` authorization artifact (PERMIT_WITH_AUTHORIZATION). | §2.1 |
| **Constraint** | A property the system must preserve, typically derived from invariants. | §2.1 |
| **Contract Compiler (`C7`)** | The component that compiles a permitted governed action into the immutable, content-addressed, signed ECC; distinct from `C2` (which decides permit/deny). | §2.2; §4.4.3 |
| **Corrective Reframing Mode** | Execution mode in which a context-invalid request yields a CONTEXT_FAILURE with, where determinable, a valid alternative — a governance success of the grounding layer. | §2.1 |
| **Cumulative invariant** | An invariant exposed to accumulation, whose violation is a property of a sequence rather than of any single transition; at L4 it MUST be enforced under a cumulative trajectory rule profile (`TP-C`, or `TP-X` where accumulation can span sessions), not windowed-only. | §4.6.3 |
| **Delegation chain** | The signed, append-only record (held in `C5`, `event.delegation_chain`) of which subject delegated which scoped authority to which sub-agent; scope is represented in the canonical Appendix L scope profile and is strictly monotone along the chain (`scope(S) ⊆ scope(O) ⊆ scope(P)`), with depth/duration bounds. | Appendix L |
| **Delegation token** | The signed, scoped, time- and depth-bounded grant by which one subject (an orchestrator) delegates a subset of its authorized scope to a sub-agent; carried as `gga.delegation.*` and recorded in the `C5` delegation chain. A token that widens scope, cannot be canonicalized or compared under Appendix L, or is presented past its expiry or maximum depth, is invalid and fails-deny. | Appendix L |
| **Deny decision** | A `C2` outcome that prohibits a governed action from proceeding. | §2.1 |
| **Deterministic governance** | Governance whose permit/deny decisions are reproducible from policy and request alone, independent of agent state or stated reasoning. | §2.1 |
| **Evaluability class (E1/E2/E3)** | The classification, assigned to every registered invariant in GitOps Definition (§7.2), of how its satisfaction is decided: **E1** syntactic/attribute (exact predicate over typed fields); **E2** static/decidable (a terminating decision procedure over a bounded, well-typed artifact, exact within a declared abstraction); **E3** semantic/approximated — the exact decision is undecidable or intractable in general (Rice's theorem), so it is evaluated by a *deterministic conservative approximation* (a sound over-approximation that may yield false positives but no false negatives, **or** a declared bounded heuristic) returning `SATISFIED`/`VIOLATED`/`AMBIGUOUS`; deterministic given a pinned analyzer version, but not exact. A non-deterministic (unpinned) evaluator is barred from the `C2` decision path; an E3 residual (and, for E3, the measured AMBIGUOUS→DENY rate) is declared per invariant. | §2.6 |
| **Execution** | The act of effecting a state change in a system, resource, or data store. | §2.1 |
| **Execution ambiguity** | A condition in which more than one governed path could satisfy a request and the choice has policy implications the agent may not resolve. | §2.1 |
| **Execution boundary** | The delineation between the control plane and governed systems; only operations produced by the Contract Compiler (`C7`) may cross it, enforced by the Execution Firewall (`C6`). | §2.3 |
| **Execution Firewall (`C6`)** | The component that enforces the execution boundary (only ECC-derived operations cross); contains the Refusal Gateway function that emits typed, audited deny decisions. | §2.2; §4.8 |
| **Execution Governor (`C2`)** | The component that evaluates governed actions against policy and invariants and issues permit/deny; the Policy Decision Point. | §2.2; §4.4 |
| **Execution mode** | The classification of the governance response: Blocking, Constrained Execution, or Corrective Reframing. | §2.1 |
| **Governance** | The structural enforcement of policy at the execution layer (distinguished from guidance and alignment). | §2.1 |
| **Governance Architect** | The human role that leads the CROA-PaC for an enterprise deployment; distinct from `C1`. | §2.2; Part III §7.4 |
| **Governance boundary** | The delineation between systems/actions within a CROA control plane's scope and those outside it; must be explicitly documented. | §2.3 |
| **Governance Success** | A deny decision against an action that would have violated an invariant — a positive outcome that MUST NOT be classified as a system error. | §2.1 |
| **Governed action** | A candidate action emitted by a governed agent and routed through the control plane for evaluation. | §2.1 |
| **Governed agent** | An agentic system whose execution surface is mediated by a CROA control plane; an untrusted principal. | §2.2 |
| **Guardrail** | Colloquial; not used in normative content. The design-level failure it usually denotes is *point-of-delivery blocking* (§1.2). | §2.1 |
| **Guideline** | Non-normative advisory content; not enforced. | §2.1 |
| **Invariant** | A property that must hold across all governed executions; carries an identifier (`In`), scope, statement, and enforcing component(s). | §2.1; Ch 5 |
| **Invariant Monitor (`C4`)** | The component that continuously verifies invariant satisfaction across action sequences (trajectory analysis). | §2.2; §4.6 |
| **Observability** | The broader capacity to inspect system state (distinguished from audit). | §2.1 |
| **Orchestration** | The mediated routing, sequencing, and authorization of an agent's candidate actions through the control plane prior to execution. | §2.1 |
| **Orchestration Control Plane (OCP)** | The logical structure comprising the seven components `C1`–`C7`; the mechanism by which T1 (structural unreachability) and T2 (execution-layer governance) are satisfied for every governed action. The Agent Surface and its admission-stage controls are not part of the OCP. | §2.2; §4.2 |
| **Path Resolver (`C3`)** | The component that validates context grounding and determines admissible execution paths. | §2.2; §4.5 |
| **Permit decision** | A `C2` outcome that authorizes a governed action to proceed to execution. | §2.1 |
| **Policy** | The authoritative artifact issued by the Policy Authority; normative. | §2.1 |
| **Policy artifact** | A versioned, signed declaration of permissible execution paths and conditions, issued by `C1`. | §2.1; §4.3 |
| **Policy Authority (`C1`)** | The sole issuer of authoritative policy artifacts within a governance domain. | §2.2; §4.3 |
| **Policy domain** | The set of agents, subjects, actions, and resources over which one `C1` holds authority. | §2.3 |
| **Qualification** | The determination that an agent subject has demonstrated, through orchestration-administered evidenced examination, ongoing competence to exercise an action class; grants operational authorization. | §2.2; §4.9.2 |
| **Qualification verdict** | The per-(subject, action class) record of status (QUALIFIED/EXPIRED/REVOKED/UNQUALIFIED), validity window, configuration fingerprint, and score. | §2.2; §4.9.2 |
| **Recertification** | Re-administration of a qualification battery on schedule or on configuration/battery/registry change. | §2.2; §4.9.2 |
| **Refusal** | A structured, audited deny decision with a typed reason and a mandatory `C5` entry (distinguished from denial and error). | §2.1 |
| **Refusal Gateway** | The deny-emitting function within the Execution Firewall (`C6`); emits typed, audited deny decisions referenced to the violated policy or invariant and recorded in `C5`. Not a separate component. | §2.2; §4.8 |
| **Role** | A named set of authorized action classes assigned to a subject; confers eligibility, not trust or execution authority. | §2.2; §4.9.1 |
| **Rule** | A single normative statement within a policy artifact. | §2.1 |
| **Structural unreachability** | A property of an execution path such that no sequence of governed actions can lead a conforming system into it (distinguished from behavioral avoidance). | §2.1 |
| **Subject** | A principal on whose behalf a governed action is requested; may be a human, a service, or another agentic system. | §2.2 |
| **Subject authorization** | The admission determination of whether a subject's roles permit submitting a given action class; the second stage of the authorization model. | §2.2; §4.9.1 |
| **Federated Context Registry** | The enterprise's authoritative registry of the entities that actually exist in the governed environment; the reference for `C3` grounding. | §2.1 |
| **Technical Sycophancy** | Failure mode (`TH-1`) in which an agent reinterprets/narrows/evades constraints under execution pressure; a runtime governance failure, not an alignment failure. | §2.1; Ch 26 |
| **Telemetry** | The operational signal stream; not necessarily authoritative. | §2.1 |
| **Tenet** | A foundational principle (`Tn`) from which architectural decisions derive. | §2.1; Ch 3 |
| **Trajectory rule profile** | The declared analysis profile under which a trajectory-relevant invariant is enforced by `C4`: **TP-0** single-action (no trajectory rule), **TP-W** windowed, **TP-C** cumulative, **TP-X** cross-session cumulative. Profiles carry cumulative invariant obligations and close low-and-slow / cross-session accumulation (TH-7.D/E). | §4.6.3 |
| **Trust boundary** | A delineation across which assumptions about authenticity, authority, or correctness change; crossing data must be validated. | §2.1; §2.3; Ch 6 |
| **Write-ahead journal** | A local, append-only, signed, crash-durable journal (chained on the same conditions as `C5`) to which a state transition MUST be durably committed before it proceeds; central replication is deferrable under a bounded RTO, and an RTO breach or local-commit failure resolves to fail-deny (I6.1). | §5.6; I6.1 |

> *Deprecated identifiers, when any exist, are retained here and marked DEPRECATED with a pointer to their successor (Part VII §31.2). No deprecated terms exist in v1.0.1.*

---

*End of Appendix A — Lexicon.*
