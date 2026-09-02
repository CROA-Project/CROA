# CROA stable identifiers

The specification itself lives on Zenodo (see [`README.md`](README.md)). This page mirrors only
its **stable identifier scheme** in Markdown, so reviewers, issues, and RFCs can cite precise
targets — *Part VI §29.5*, *C6*, *L4*, *Appendix Q* — without paging through the PDF, and so those
citations stay valid across editions even as pagination changes.

> This is a navigation aid, not normative text. Where it and the Zenodo specification differ, the
> **specification governs**.

## Parts (the CROA-1 … CROA-7 document series)

| ID | Part | Scope |
|---|---|---|
| **Part I** | Foundations | Problem, scope, definitions, the ten Tenets (T1–T10), the central claim |
| **Part II** | Reference Architecture | The seven components (C1–C7), trust boundaries (TB-1…TB-4), the audit model |
| **Part III** | Method (CROA Development Cycle) | How an organization models actions, authors invariants, and reaches conformance |
| **Part IV** | Deployment Models | Reference deployments, the P4 network-enforced boundary property |
| **Part V** | Threat Model | Threats (TH-*), failure modes, adversary assumptions |
| **Part VI** | Conformance and Maturity | Conformance criteria, levels L0–L5, evidence requirements |
| **Part VII** | Governance of the Standard | Change classes (§31.3), neutrality, claims-usage policy (§33) |

## Components (identity, not pipeline order)

| ID | Component | One-line role |
|---|---|---|
| **C1** | Policy Authority | Single source of signed policy and authorization artifacts |
| **C2** | Execution Governor | Deterministic decision point → permit / deny |
| **C3** | Path Resolver | Grounds the request against the Technical Golden Record |
| **C4** | Invariant Monitor | Invariant and trajectory (cumulative) state |
| **C5** | Audit & Provenance Store | Append-only, hash-chained event log |
| **C6** | Execution Firewall | The execution boundary; admits only CC-derived operations |
| **C7** | Contract Compiler | Compiles a permitted action into a signed Compiled Commitment (CC) |

## Trust boundaries

| ID | Boundary |
|---|---|
| **TB-1** | Agent boundary (the agent is an untrusted principal) |
| **TB-2** | Policy boundary (policy authored only by C1) |
| **TB-3** | Execution boundary (only CC-derived operations pass; network-enforced = property **P4**) |
| **TB-4** | Audit boundary (C5 append-only; auditors read-only) |

## Conformance levels

| ID | Level |
|---|---|
| **L0–L3** | Increasing partial enforcement and evidence |
| **L4** | Constructive Enforcement — the conformance **threshold**; only L4+ may be called "CROA-conformant" |
| **L5** | L4 plus continuous self-verification (evidence criteria not fully specified in v1.0) |

## Evaluability classes

| ID | Class |
|---|---|
| **E1** | Exact / decidable |
| **E2** | Exact over bounded / structured input |
| **E3** | Semantic / approximated (sound over-approximation; may over-deny) |

## Reference negative tests (Appendix Q)

| ID | Test | In the reference harness? |
|---|---|---|
| **NT-001** | Non-CC execution blocked | ✅ |
| **NT-002** | Expired CC blocked | ✅ |
| **NT-003** | Replay blocked | ✅ |
| **NT-004** | Unregistered context blocked | ✅ |
| **NT-005** | Ambiguous E3 invariant → fail-closed deny | ⛔ needs an E3 analyzer (contributed extension) |
| **NT-006** | Trajectory / cumulative constraint | ⛔ needs C4 trajectory state (contributed extension) |
| **NT-007** | Governed exception single-use — authorization replay, scope-widening, and concurrent double-redemption blocked | ⚠️ partial — the harness governed-exception scenario covers **replay only**; the scope-widening and concurrent-presentation steps are not implemented |
| **NT-008** *(new; not in v1.0 as published — see [`errata-v1.0.md`](errata-v1.0.md) E-02)* | Authority non-expansion — delegation attenuation and no authority laundering by composition | ⛔ needs a delegation model (contributed extension) |

## Appendices (A–S)

| ID | Appendix |
|---|---|
| **A** | Lexicon |
| **B** | Notation, Identifiers and Symbols |
| **C** | Consolidated Deliverables Catalog |
| **D** | Mapping to TOGAF ADM |
| **E** | Mapping to NIST SP 800-207 |
| **F** | Mapping to ISO/IEC 27001 |
| **G** | Reference Implementation |
| **H** | Worked Example (NovaCare) |
| **I** | C4 Implementation Approaches |
| **J** | Performance and Latency Profile |
| **K** | CROA Core Profile |
| **L** | Governed Multi-Agent Delegation |
| **M** | Mapping to the EU AI Act |
| **N** | Mapping to ISO/IEC 42001 |
| **O** | CROA and Adjacent Enforcement Mechanisms |
| **P** | Sector Worked Examples |
| **Q** | Evidence Pack and Reference Negative Tests |
| **R** | C5 High-Performance Evidence Pattern |
| **S** | Implementing C4 in Common Enterprise Cases |

## How to cite in an issue or RFC

- A requirement: **Part VI §29.5**, **Part II §12.3** (Part + section number).
- A component or level: **C6**, **L4**.
- An appendix: **Appendix Q**, **Appendix K**.
- A negative test / tenet / threat: **NT-003**, **T1**, **TH-1**.

Cite the identifier, not a page number — pages move between editions; identifiers do not.
