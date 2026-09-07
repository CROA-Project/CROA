---
tags:
  - croa_foundation
---

# Appendix M — Mapping to the EU AI Act (Regulation (EU) 2024/1689)

**CROA Framework v1.0.1.1 · Informative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The
>
## M.1 How CROA relates to the EU AI Act

The EU AI Act regulates AI systems by risk tier and assigns obligations to providers and deployers of high-risk systems. It is, like NIST AI RMF and ISO/IEC 42001, predominantly a **management and process** regime: it requires that risks be managed, that systems be logged, that humans can oversee, and that deployers operate systems within instructions. It does not specify a **runtime enforcement mechanism**. CROA occupies exactly that layer: it is the technical control architecture that can *produce the evidence and enforce the constraints* several Act obligations presuppose. CROA does not make a system Act-compliant on its own, but a CROA-governed deployment supplies machine-verifiable substantiation for the obligations below.

The Act's risk-tiering posture is also the natural home for CROA's risk-proportionate profile (Appendix K, CROA Core): consequence classes R0–R4 and method tiering let a deployer concentrate enforcement where the Act concentrates obligation (high-risk systems).

## M.2 Article-level mapping

### Article 9 — Risk management system (high-risk AI)

Article 9 requires a continuous, iterative risk-management process across the lifecycle: identification, estimation, evaluation, and mitigation of foreseeable risks.

| Art. 9 element | CROA contribution |
|---|---|
| Identification/analysis of known and foreseeable risks | Part V threat model (TH-1…TH-11) with falsifiable definitions; Policy Validation (§7.2) (Threat and Failure Architecture) |
| Adoption of risk-management measures | Structural mitigations mapped per threat (Part V §27); invariant registry (GitOps Definition (§7.2)) as enforced controls |
| Testing to identify the most appropriate measures | Negative testing per threat class (Part V §27.3) as a conformance gate (Part VI §29.3) |
| Residual risk judged acceptable and communicated | Residual Risk Register (C-24); declared residuals (TH-3/TH-9/TH-10.A); L4 claim-scope statement (Part VI §28.6) |
| Iterative across lifecycle | CROA-PaC phases, Policy Update (§7.2) change control, Policy Deployment (§7.2) operation reviews |

CROA's contribution to Art. 9 is that the risk measures are **enforced and evidenced**, not merely documented.

### Article 12 — Record-keeping (logging)

Article 12 requires high-risk systems to automatically record events (logs) over their lifetime, to a degree appropriate to the intended purpose. This is the obligation CROA satisfies most directly — almost trait for trait.

| Art. 12 element | CROA contribution |
|---|---|
| Automatic recording of events over lifetime | `C5` Audit and Provenance Store: every governed decision recorded synchronously (I6/I6.1) |
| Traceability appropriate to purpose | Typed events with subject, action, policy version, invariant-set version, decision basis (§4.7) |
| Tamper-evidence / integrity | `event.chain_hash` cryptographic chaining (I3); append-only storage |
| Reconstructability independent of the system's own claims | T3: every action reconstructable from `C5` without the agent's cooperation; assessor reads `C5` only (Part VI §29) |

For a deployer, the `C5` evidence model is a ready-made Article 12 logging substrate.

### Article 14 — Human oversight

Article 14 requires that high-risk systems be designed so that natural persons can effectively oversee them, including the ability to intervene or interrupt.

| Art. 14 element | CROA contribution |
|---|---|
| Oversight built into the system design | Governance is structural (T1/T2), not dependent on the model's cooperation; humans set invariants (GitOps Definition (§7.2)) |
| Ability to not use / override / interrupt | Human override is itself a governed request for authorization (Constrained Execution Mode, §4.3.1); a DENY halts execution by construction |
| Oversight not defeated by automation bias | A human override does not bypass the Gatekeeper; it is signed, scoped, bounded, and recorded — overrides are evidenced, not silent |
| Correct interpretation of output | `C3` blocks execution on hallucinated/assumed context (Corrective Reframing), so oversight is not exercised over false premises |

CROA's distinctive Art. 14 contribution: oversight is **enforced and auditable** (every override is a signed, recorded authorization), not a procedural expectation.

### Article 26 — Obligations of deployers of high-risk AI systems

Article 26 obliges deployers to use high-risk systems per instructions, ensure input data relevance, monitor operation, keep logs, and assign human oversight.

| Art. 26 element | CROA contribution |
|---|---|
| Use in accordance with instructions for use | The governance boundary, operational envelope, and invariant registry encode "permitted use" enforceably (Policy Definition (§7.2)/D) |
| Input data relevance/representativeness (within deployer control) | `C3` golden-record grounding (§4.5, §4.5.2): execution proceeds only on resolved, current context |
| Monitor operation; suspend and inform on risk | `C4` trajectory monitoring; `C5` detection signatures; fail-deny on ambiguity; Policy Deployment (§7.2) reviews |
| Keep automatically generated logs | `C5` retention (Part II §4.7); Audit-and-Provenance-Store custodian responsibilities (Part II §4.7; navigational "Evidence Officer" summary in [Framework structure](../framework-structure.md)) |
| Human oversight by competent persons | Defined roles — Governance Architect (Part I §2.2, Part III §7.4) and the Policy Authority (`C1`, Part II §4.3); AQL for agent subjects (§4.9.2) |

## M.3 Adjacent articles (briefly)

- **Art. 10 (data and data governance):** `C3` golden-record discipline and the determinism of resolution support data-quality-at-use; CROA does not address training-data governance.
- **Art. 13 (transparency / instructions for use):** the published governance boundary, claim-scope statement (Part VI §28.6), and Claims Register (Part VII §33.2) support honest capability communication.
- **Art. 15 (accuracy, robustness, cybersecurity):** structural unreachability, fail-deny, monotone admission, and the threat model (Part V) are robustness/cybersecurity controls; TH-10.A and TH-3/TH-9 residuals are declared, not hidden.
- **Art. 72 (post-market monitoring):** `C5` evidence and Policy Deployment (§7.2) operation reviews are a post-market monitoring data source.
- **GPAI / systemic-risk obligations:** out of scope for CROA, which governs *deployed execution*, not model provision.

## M.4 What this mapping is and is not

This is a control-to-obligation crosswalk to help a deployer of a high-risk AI system show *how* a CROA-governed deployment substantiates specific Act obligations with enforced, evidenced controls. It is **not** a conformity-assessment, a presumption of conformity, or a substitute for the harmonized standards and conformity-assessment procedures the Act requires. A deployer remains responsible for the full set of obligations; CROA reduces the gap between "documented process" and "enforced, auditable control" for Articles 9, 12, 14, and 26 in particular.

Cross-reference: ISO/IEC 42001 mapping (Appendix N); NIST AI RMF crosswalk (Part V §27.4); ISO/IEC 27001 (Appendix F).

---

*End of Appendix M — Mapping to the EU AI Act.*
