---
tags:
  - croa_foundation
---

# Appendix B — Notation, Identifiers, and Symbols

**CROA Framework v1.0.1.1 · Reference (informative).** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index. This appendix consolidates the notation introduced in Part I §1.8 and §2.4; those sections are authoritative.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The

**The notation map (S1).** A reader of the framework must hold the identifier families catalogued below in mind. They group into four clusters; learning the clusters once is easier than meeting the families scattered across seven Parts:

- **What the architecture *is*** — `Tn` tenets, `Cn` components, `In` invariants.
- **What can go *wrong*** — `TH-n` threat classes.
- **How something is *judged*** — `En` evaluability classes, `Rn` reversibility/consequence classes, `TP-*` trajectory profiles.
- **How it is *deployed and assured*** — `DM-n` deployment models, `Pn` deployment properties, `IP-n` integration patterns, `Ln` conformance levels, `C-n` deliverables, `ADR-n` architecture decision records.

> *Watch the `Cn` (component, no hyphen) vs. `C-n` (deliverable, hyphen) collision — it is the one pair the framework most often has to disambiguate.*

The authoritative per-family table follows.

**Stable identifier schemes.**

| Scheme | Form | Denotes |
|---|---|---|
| Tenets | `Tn` | A foundational principle (Part I, Chapter 3) — `T1`…`T10` |
| Logical components | `Cn` | An OCP component (Part II, Chapter 4) — `C1`…`C7` |
| Invariants | `In` | An architectural invariant (Part II, Chapter 5) — `I1`…`I8` |
| Threat classes | `TH-n` | A threat class (Part V, Chapter 26) — `TH-1`…`TH-11` |
| Deployment models | `DM-n` | A deployment model (Part IV) — `DM-1`…`DM-5` |
| Deployment invariant properties | `Pn` | A property preserved across all models (Part IV §18.1) — `P1`…`P7` |
| Integration patterns | `IP-n` | An integration pattern (Part IV, Chapter 24) — `IP-1`…`IP-4` |
| Conformance levels | `Ln` | A conformance level (Part VI, Chapter 28) — `L0`…`L5` |
| Deliverables / artifacts | `C-n` | A CROA-PaC deliverable ([Appendix C - Consolidated Deliverables Catalog](../appendices/appendix-c-consolidated-deliverables-catalog.md)) — `C-01`…`C-36` |
| Architecture decision records | `ADR-n` | A deployment architecture decision (Part II §6.5) |
| Reversibility / consequence classes | `Rn` | A transition's reversibility/consequence class (Part I T5) — `R0` fully reversible, `R1` compensatable, `R2` irreversible/low-impact, `R3` irreversible/high-impact, `R4` irreversible/critical |
| Invariant evaluability classes | `En` | A registered invariant's evaluability class (Part I §2.6) — `E1` syntactic/attribute, `E2` static/decidable, `E3` semantic/approximated |
| Trajectory rule profiles | `TP-*` | A trajectory-relevant invariant's rule profile (Part II §4.6.3) — `TP-0` single-action, `TP-W` windowed, `TP-C` cumulative, `TP-X` cross-session cumulative |
| Delegation requirements | `Dn` | A governed multi-agent delegation requirement ([Appendix L - Governed Multi-Agent Delegation](../appendices/appendix-l-governed-multi-agent-delegation.md), conditional-normative) — `D1`…`D5` |

Identifiers are stable once published (Part VII §31.2). The component scheme `Cn` (no hyphen) and the artifact scheme `C-n` (hyphen) are distinct namespaces and MUST NOT be conflated. Deployment Invariant Registries (Part III, GitOps Definition (§7.2)) assign enterprise-defined instance identifiers to concrete invariants — e.g., `EI-n` in [Appendix H - Worked Example (NovaCare)](../appendices/appendix-h-worked-example-novacare.md) — a deployment-local namespace distinct from the architectural invariants `In`.

**Field namespaces.**

| Prefix | Structure | Defined in |
|---|---|---|
| `gar.*` | Governed action request (e.g., `gar.type`, `gar.target`, `gar.parameters`, `gar.context_refs`) | §4.5.1 |
| `gga.*` | Grounded governed action (e.g., `gga.semantic_result`, `gga.resolved_entities`; `gga.delegation.*` for a delegated action) | §4.5.1; `gga.delegation.*` Appendix L §L.4 |
| `ecc.*` | Execution Change Contract (e.g., `ecc.id`, `ecc.authorization_scope`, `ecc.expires_at`, `ecc.invariant_set_version`) | §4.4.1 |
| `event.*` | `C5` governance event (e.g., `event.type`, `event.subject_id`, `event.chain_hash`, `event.rejection_reason`; `event.delegation_chain` for a delegated action) | §4.7.1; `event.delegation_chain` Appendix L §L.4 |

The `gga.delegation.*` and `event.delegation_chain` field families are **OPTIONAL** and are populated only for delegated actions under governed multi-agent delegation (Appendix L, normative where delegation is implemented).

**Machine-readable schemas.** JSON Schema (draft 2020-12) files for the `gar.*`, `gga.*`, `ecc.*`, and `event.*` namespaces are published alongside the framework in the `schemas/` directory (`gar.schema.json`, `gga.schema.json`, `ecc.schema.json`, `event.schema.json`; see `schemas/README.md`). The prose schemas in Part II (§4.4.1, §4.5.1, §4.7.1) are authoritative; the JSON Schemas are companion artifacts for implementation and testing.

**Enumerations.**

- `event.type` ∈ { `PERMIT`, `DENY`, `ECC_COMPILED`, `EXECUTION_AUTHORIZED`, `EXECUTION_BLOCKED`, `CONTEXT_FAILURE`, `TRAJECTORY_ALERT`, `ADMISSION_REJECTED`, `QUALIFICATION`, `POLICY_ARTIFACT_ISSUED`, `EXECUTION_COMPLETED`, `EXECUTION_FAILED`, `EFFECT_ATTESTED` } (§4.7.1). `POLICY_ARTIFACT_ISSUED` (the `C1` policy-issuance event) and out-of-session `QUALIFICATION` events are not tied to a governed-action session and are exempt from the otherwise-mandatory `event.session_id` (§4.6.1, §4.7.1).
- `event.rejection_reason` ∈ { `SCHEMA_VIOLATION`, `UNAUTHORIZED_ACTION_CLASS`, `UNQUALIFIED`, `QUALIFICATION_EXPIRED`, `QUALIFICATION_CONFIG_MISMATCH` } (§4.7.1).
- `event.block_reason` ∈ { `ECC_EXPIRED`, `ECC_INTEGRITY_INVALID`, `ECC_NOT_FOUND`, `ECC_INVARIANT_STALE`, `ECC_ALREADY_REDEEMED` } (§4.7.1; `ECC_ALREADY_REDEEMED` = single-use replay, §4.8).
- Qualification verdict status ∈ { `QUALIFIED`, `EXPIRED`, `REVOKED`, `UNQUALIFIED` } (§4.9.2).
- Execution modes: Blocking, Constrained Execution, Corrective Reframing (§2.1).

**Formal symbols.**

- `ES(t)` — the execution surface at time *t*: the set of operations authorized to cross TB-3 (§6.2).
- `exec(r)` — the set of operations authorized by ECC *r* (§6.2).
- CROA-PaC governance changes follow the GitOps workflow steps of Part III §7.2: *Definition*, *Proposal*, *Validation*, *Deployment*, *Rollback*. The TOGAF phase-letter convention (`P, A, B, C, D, E, F, G, H`) is retired in v1.0.1 (see Appendix D, DEPRECATED).

**Citation forms in running text** (Part I §2.4): `(see §4.3)`, `(see C2)`, `(see I3)`, `(see T4)`, `(see TH-1)`, `(see L4)`.

---

*End of Appendix B — Notation, Identifiers, and Symbols.*
