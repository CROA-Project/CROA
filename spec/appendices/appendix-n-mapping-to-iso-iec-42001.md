---
tags:
  - croa_foundation
---

# Appendix N — Mapping to ISO/IEC 42001 (AI Management System, 2023)

**CROA Framework v1.0.1.1 · Informative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The
>
## N.1 Relationship

ISO/IEC 42001:2023 specifies an **AI management system (AIMS)** — the organizational processes by which an enterprise governs its AI activities (policy, objectives, roles, risk and impact assessment, operational controls, monitoring, improvement). It is a management-system standard in the ISO high-level-structure (clauses 4–10) with normative Annex A controls and informative implementation guidance (Annex B), plus AI impact-assessment guidance.

CROA is **complementary and at a different layer**: it is the technical control architecture an AIMS can adopt to *operationalize and evidence* several of its controls for agentic execution. Where 42001 asks the organization to define and apply operational controls and to monitor AI systems, CROA provides the enforcement mechanism (structural unreachability) and the evidence substrate (`C5`). An organization can run a 42001 AIMS without CROA, and can deploy CROA without a formal AIMS; together, 42001 supplies the management wrapper and CROA supplies the runtime control and audit evidence.

## N.2 Management-system clauses (4–10)

| ISO/IEC 42001 clause | CROA contribution |
|---|---|
| 4 Context / scope of the AIMS | The **governance boundary** definition (Part I §2.3; Policy Definition (§7.2)) gives a precise, technical scope statement for agentic execution within the AIMS scope |
| 5 Leadership & AI policy | `C1` Policy Authority as the single signed source of execution policy (Part II §4.3, I4); Governance Architect and Policy Authority Representative roles (Part I §2.2; Part III §7.4) |
| 6 Planning — AI risks & opportunities; AI impact assessment | Part V threat model + Policy Validation (§7.2); Residual Risk Register (C-24); consequence classes R0–R4 inform impact assessment |
| 7 Support (resources, competence, awareness, documentation) | Defined roles and competence (AQL for agent subjects §4.9.2); versioned, signed artifacts as controlled documents (I4, Policy Update (§7.2)) |
| 8 Operation (operational planning & control; AI system lifecycle) | The CROA-PaC method (Part III, Phases P–H) is a lifecycle operational-control process; the OCP (C1–C7) is the operational control at runtime |
| 9 Performance evaluation (monitoring, internal audit) | `C4` monitoring; `C5` evidence enabling independent audit (Part VI §29); performance profile (Appendix J) |
| 10 Improvement (nonconformity, corrective action) | Governance Success model (a DENY is data, not an incident); Policy Deployment (§7.2) operation reviews; Policy Update (§7.2) change control feeding policy/invariant updates |

## N.3 Annex A controls (representative)

The mapping below targets the Annex A control areas most directly served by CROA. It is representative, not exhaustive, and uses the 2023 Annex A structure.

| ISO/IEC 42001 Annex A area | CROA contribution |
|---|---|
| Policies related to AI | `C1` signed, versioned policy artifacts; profiles (§33.3, Appendix K) |
| Internal organization / roles & responsibilities | Separation of the Policy Authority (`C1`) from operations — normative in Part II §4.3 (`C1` exclusivity, I4) and Part VII §32.2 (neutrality); summarized navigationally in [Framework structure](../framework-structure.md) |
| Resources for AI systems (data, tooling, compute) | Federated Context Registry as the authoritative resolution surface (§4.5.2); tool/action-class scoping |
| Assessing impacts of AI systems | Consequence classes R0–R4 (Part I T5); impact-proportionate method tiering (Appendix K) |
| AI system lifecycle (responsible development, deployment) | CROA-PaC Phases P–H; conformance levels L0–L5 (Part VI) |
| Data for AI systems (quality, provenance at use) | `C3` grounding against the golden record; `gga.resolved_entities` provenance at resolution time |
| Operational controls / use of AI systems | The OCP enforces permitted use; only `C7`-compiled, `C6`-validated operations execute (I1/P4) |
| Information & logging for AI systems | `C5` synchronous, tamper-evident, typed event log (I3/I6) |
| Monitoring of AI systems | `C4` trajectory analysis; `C5` detection signatures (Part V); fail-deny on ambiguity |
| Incident / problem management | Governance Success classification (a DENY is a success, not an incident); declared residuals tracked in C-24 |
| Third-party / supplier relationships | Deployment models (Part IV) including platform DM-5 and per-tenant isolation; reference implementation as a derivative work (§32.2, §33.3) |

## N.4 What this mapping is and is not

This crosswalk shows where a CROA-governed deployment supplies enforced controls and audit evidence for an ISO/IEC 42001 AIMS. It is **not** a claim of 42001 certification, nor a substitute for the AIMS clauses an organization must itself implement (leadership, planning, competence, internal audit, management review). CROA's value to a 42001 program is concentrated in clauses 8–9 and the operational/logging/monitoring Annex A controls, where it converts management intent into enforced, machine-verifiable behavior.

Cross-reference: EU AI Act mapping (Appendix M); ISO/IEC 27001 (Appendix F); NIST AI RMF crosswalk (Part V §27.4).

---

*End of Appendix N — Mapping to ISO/IEC 42001.*
