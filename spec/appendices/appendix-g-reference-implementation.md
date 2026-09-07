---
tags:
  - croa_foundation
version: 1
language: english
---

# Appendix G — Reference Implementation

**Full title:** CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution
**Series designation:** CROA-G
**Status:** Official Specification (v1.0.1) — Non-normative
**Version:** v1.0.1
**Date:** 2026-09-03
**Appendix:** G (Non-normative)

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The

---

## G.1 Riven — The Founding Implementation

**Riven** is the CROA Project's founding implementation of CROA — a governed AI software factory that served as the primary design driver for the architecture during the framework's development phase.

Riven's role in the CROA corpus is precisely scoped:

**What Riven is:**

- The founding implementation that demonstrated the CROA architecture is operationally realizable.
- Prototype evidence that the C1–C7 component model functions as an integrated governance pipeline.
- The system used in the founding comparative study (Part VI §29.5), which provided directional validation evidence for the architectural thesis across adversarial scenarios.
- A historical design driver: architectural decisions recorded in the Parts I–VI are traceable to design choices refined through Riven's development.

**What Riven is not:**

- Independent conformance proof. Riven's validation evidence is self-authored and small-N (see Part VI §29.5); it is directional validation, not an independent assessment.
- The only implementation path. An enterprise implementing CROA may use any architecture that satisfies the conformance criteria in Part VI. No derivation from Riven is required.
- A current implementation artifact. Riven development is **currently paused**. The code base as it existed at the point of pause is the relevant artifact; it has not been assessed for conformance against this version of the specification.

**Conformance authority:** CROA conformance is determined solely by the criteria in Part VI (Chapters 28–29). The architecture's requirements are in Parts I–VI. No implementation, including Riven, defines conformance by its behavior; only the specification does.

Riven is a derivative work in the sense of Part VII §33.3 and is governed separately from the specification. A future resumption of Riven development — or the development of any other CROA implementation — would be assessed for conformance against the Part VI criteria, not against Riven's prior behavior.

---

## G.2 The CROA Minimal Reference Harness

> *This section describes a recommended minimal artifact that demonstrates the CROA evidence model and enforcement logic in a self-contained, inspectable form. The harness is not a conformance artifact; it is an educational and exploratory tool. It does not confer conformance on any deployment.*

### G.2.1 Purpose

The CROA Minimal Reference Harness (MRH) is a vendor-neutral, minimal implementation artifact intended to demonstrate:

- how CROA evidence is structured in C5;
- how an Execution Change Contract (ECC) links a permit decision to an execution commitment;
- how a negative test proves that enforcement is present, not merely asserted;
- how an auditor can replay a governance decision from C5 alone.

The MRH is not a production-grade system. Its role is to make the architecture concrete for practitioners who are evaluating CROA before committing to a full pilot implementation.

### G.2.2 Harness Components

A conforming MRH implementation SHOULD contain the following mock components:

| Component | Mock role | Minimum behavior |
|---|---|---|
| C1 mock | Policy Authority | Produces a versioned, signed policy artifact (YAML or JSON) covering a defined set of action classes and invariants |
| C2 mock | Execution Governor | Evaluates a governed action request against the policy artifact; returns PERMIT, DENY, or PERMIT_WITH_AUTHORIZATION deterministically |
| C3 mock | Path Resolver | Validates action request context against a static Federated Context Registry; returns CONTEXT_FAILURE for absent entities |
| C4 mock | Invariant Monitor | Maintains trajectory state for one TP-C invariant; produces TRAJECTORY_ALERT when the threshold is reached |
| C7 mock | Contract Compiler | Produces a JSON ECC from a PERMIT decision; signs it with a local key; sets a short expiry |
| C6 mock | Execution Firewall | Validates an ECC (signature, expiry, prior redemption); admits or blocks; produces EXECUTION_AUTHORIZED or EXECUTION_BLOCKED |
| C5 mock | Audit and Provenance Store | Appends all events to a local file with hash chaining; provides a chain-verification function |

### G.2.3 Required Test Scenarios

A conforming MRH MUST demonstrate at least four test scenarios, each producing verifiable C5 evidence:

**Test 1 — Permit path.** A well-formed governed action request with a valid subject, eligible role, grounded context, and no invariant violation proceeds through the full pipeline: C3 validates, C2 permits, C7 compiles an ECC, C6 admits, C5 records PERMIT + ECC_COMPILED + EXECUTION_AUTHORIZED.

**Test 2 — Deny path.** A governed action request that violates a registered invariant without authorization is denied: C2 produces DENY, no ECC is compiled, C6 is not reached, C5 records DENY (governance success).

**Test 3 — Context failure.** A governed action request referencing an entity absent from the Federated Context Registry is blocked at C3: C3 produces CONTEXT_FAILURE, C2 is not invoked, no ECC is compiled, C5 records CONTEXT_FAILURE.

**Test 4 — Replay blocked.** An ECC that has been redeemed (EXECUTION_AUTHORIZED already in C5) is presented again: C6 checks its redemption record, finds prior redemption, blocks, C5 records ECC_ALREADY_REDEEMED.

**Test 5 — Governed exception is single-use (NT-007).** An invariant-violating action is denied on its own; a `C1`-signed authorization then permits it once as PERMIT_WITH_AUTHORIZATION (the ECC carrying `ecc.auth_ref` + `ecc.exception_scope`, C5 recording `event.auth_id`); a **second** use of the same authorization within its validity window is blocked (AUTHORIZATION_ALREADY_REDEEMED). This demonstrates the single-use, per-action exception semantics of §4.3.1/§4.8 and corresponds to Reference Negative Test NT-007 (Appendix Q).

### G.2.4 Evidence Verification

The MRH MUST include a chain-verification function that:

1. reads the C5 event log from the first event;
2. for each event, computes `hash(event_record)` and compares it to the `chain_hash` of the next event;
3. reports any chain break;
4. confirms that each PERMIT event has a corresponding ECC_COMPILED event with matching `ecc_id`;
5. confirms that each ECC_COMPILED event has exactly one corresponding EXECUTION_AUTHORIZED event (single-use enforcement).

This verification function is the minimal auditor replay tool. An assessor who can run it and observe a clean result has established that the evidence chain is intact for the duration of the harness run.

### G.2.5 Publication Status

The CROA Minimal Reference Harness is **published** as a vendor-neutral, dependency-free (Python standard library only) reference implementation under the Apache-2.0 license at `github.com/croa-project/croa-reference-harness`. It implements the mock components (§G.2.2) and the reference scenarios above — the permit path, deny path, context failure, replay-blocked, and the governed-exception single-use test (NT-007) — and includes the chain-verification function (§G.2.4). It runs the reference negative tests NT-001 through NT-004 plus the governed-exception (NT-007) property, and emits a verifiable `C5` event log. It is a demonstrator, not a production implementation (it uses demonstration keys and mock components). Implementers are encouraged to extend it — notably with NT-005 (ambiguous E3) and NT-006 (trajectory), which require an E3 analyzer and C4 trajectory state respectively — and to submit findings through the public review process.

---

*End of Appendix G — Reference Implementation.*
