---
tags:
  - croa_foundation
version: 1
language: english
---





---

# CROA

## Constrained Reachability Orchestration Architecture

### A Framework for Deterministic Governance of Agentic AI Execution

---

**Official Specification — Version 1.0.1**

**September 3, 2026**

CROA Core team (Yasmine Durand, Darrin Smith, Sylvain Durand)

Published by the CROA Project

---

<div style="page-break-after: always;"></div>

## Publication Information

| | |
|---|---|
| **Framework Name** | CROA — Constrained Reachability Orchestration Architecture |
| **Framework Status** | Official Specification |
| **Version** | v1.0.1 (Official Specification) |
| **Editorial version** | v1.0.1 — the internal specification identifier carried on each Part; "v1.0.1 Official Specification" is the public release label for this editorial baseline |
| **Publication Date** | September 3, 2026 |
| **Authors** | CROA Core team (Yasmine Durand, Darrin Smith, Sylvain Durand) |
| **Published by** | The CROA Project |
| **Publication Type** | Architecture and Governance Framework |
| **Document Series** | CROA-1 through CROA-7 (Parts I–VII) and Appendices A–S |

CROA is a vendor-neutral architecture and governance framework for agentic AI systems. This publication is released for public review and experimentation. It is published under the license stated in the released version (see [Part VII - Governance of the Standard](../parts/part-7-governance-of-the-standard.md) §32.6) and may be implemented, evaluated, and cited by any party without fee.

**How to cite this document.** The CROA Project. *CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution.* Official Specification, Version 1.0.1, September 3, 2026.

---

<div style="page-break-after: always;"></div>

## Document Status

This document represents the **first Official Specification** of the CROA framework.

The purpose of this publication is to support community discussion, experimentation, and validation.

The framework should be considered **stable enough for evaluation and pilot implementations**, but remains subject to refinement based on practitioner feedback and implementation experience.

Future revisions may incorporate findings from external pilots, working groups, and governance reviews.

> *This document is an Official Specification, not a finalized or formally recognized standard. Where the text uses the language and structure of a formal specification — including RFC 2119 normative keywords (MUST, SHALL, SHOULD, MAY) and a conformance model — that language defines the framework's intended technical contract and supports rigorous evaluation. It does not assert that CROA is, at the date of this publication, an adopted, ratified, or industry-recognized standard. The path toward formal standardization is described in [Part VII - Governance of the Standard](../parts/part-7-governance-of-the-standard.md).*

---

## Terminology Convention: Framework, Specification, Standard

This Official Specification uses three terms with distinct meanings:

| Term | Use in this publication |
|---|---|
| **CROA Framework** | The public-facing name of the current publication in its entirety — the architecture, its method, and its governance model. |
| **CROA Specification** | The normative technical content within the framework — the Parts I–VII document series that defines what a conformant implementation MUST satisfy. |

Where this document uses the phrase "this specification," it refers to the normative technical requirements of the CROA Specification. Where it uses "CROA Framework" or "the framework," it refers to the full publication.

---

## How to Read and Adopt CROA

> *Non-normative. This section routes each audience to the most relevant reading path. The full specification remains the authoritative technical reference.*

### Reading Paths by Audience

The CROA specification is the complete technical reference. Different audiences will benefit from different entry points.

| Audience | Recommended entry point | Then proceed to |
|---|---|---|
| **Executive reader** (CEO, CTO, CDO, AI governance leader) | CROA Executive Brief companion document | §0 ("CROA in One Page") in Part I; Part VII §33.7 (Brand and Claims Usage Policy) and §33.8 (Claims Usage Guide — approved and prohibited claim formulations) |
| **Enterprise architect** | CROA Implementation Primer companion document | Part II (Reference Architecture); Part III (Method); Part IV (Deployment Models) |
| **Security or risk reader** | Part I §0, §1.2 (Execution-Governance Problem), §1.3 (Scope) | Part V (Threat Model); Part VI §28–29 (Conformance); [Appendix K - CROA Core Profile](../appendices/appendix-k-croa-core-profile.md) |
| **Implementation team** | Part I §1.4 (Audience), Chapter 2 (Definitions) | Part II (C1–C7 components); Part IV (Deployment Models); Appendix G (Reference Implementation); [Appendix S](../appendices/appendix-s-implementing-c4-in-common-enterprise-cases.md); [Appendix R](../appendices/appendix-r-c5-high-performance-evidence-pattern.md) |
| **Auditor or regulator** | CROA Conformance Evidence Guide companion document | Part VI §28–29; [Appendix Q](../appendices/appendix-q-evidence-pack-and-reference-negative-tests.md) |
| **Vendor** | Part I §0, Part II (C1–C7); Part VI (Conformance) | Appendix G (Riven and Minimal Reference Harness); [Appendix K - CROA Core Profile](../appendices/appendix-k-croa-core-profile.md) |

### Companion Documents

Three non-normative companion documents are published alongside the specification for audiences who need a targeted entry point before engaging the full technical text:

| Companion document | Audience | Purpose |
|---|---|---|
| CROA Executive Brief | CEO, CTO, CDO, AI leaders, governance leaders | Understand the problem, value proposition, risks, and adoption path |
| CROA Implementation Primer | Enterprise architects, security architects, tech leads | Understand how to implement C1–C7 and run a pilot |
| CROA Conformance Evidence Guide | Auditors, risk teams, security leads | Understand evidence, C5 records, negative tests, and conformance claims |

Companion documents are non-normative. Where a companion document and a Part differ, the Part governs.

---

## How This Document Is Organized

The CROA framework is published as this Front Matter, seven Parts (I–VII), and supporting Appendices (A–S); three non-normative companion documents (listed above) are published alongside it. A reader new to the framework should begin with the one-page overview in Part I (§0, "CROA in One Page") and the reading guide in Part I §1.4, which routes each audience to the most relevant chapters.

| Section | Document | Purpose |
|---|---|---|
| Front Matter | *(this document)* | Cover, publication information, document status, revision history |
| Part I | [Part I - Foundations](../parts/part-1-foundations.md) | Purpose, scope, definitions, tenets — includes the executive overview (§0) |
| Part II | [Part II - Reference Architecture](../parts/part-2-reference-architecture.md) | Logical components, invariants, trust boundaries |
| Part III | [Part III - Policy-as-Code & Lifecycle](../parts/part-3-policy-as-code-and-lifecycle.md) | The CROA Policy-as-Code Lifecycle |
| Part IV | [Part IV - Deployment Models](../parts/part-4-deployment-models.md) | Concrete realizations and integration patterns |
| Part V | [Part V - Threat Model](../parts/part-5-threat-model.md) | Threats, failure modes, and mitigations |
| Part VI | [Part VI - Conformance and Maturity](../parts/part-6-conformance-and-maturity.md) | Conformance levels, pilot path, and maturity model |
| Part VII | [Part VII - Governance of the Standard](../parts/part-7-governance-of-the-standard.md) | Lifecycle, claims usage guide, public review process, community participation |
| Appendices A–S | See [Framework structure](../framework-structure.md) for the full catalog | Lexicon, notation, deliverables, framework/regulatory mappings, reference implementation, worked examples (NovaCare + Luxury/Logistics/E-commerce), profiles, evidence pack, negative tests, C5 pattern, C4 enterprise cases, and adjacent-mechanism comparison |

Three non-normative companion documents are published alongside the specification:

| Companion Document | Audience | Location |
|---|---|---|
| CROA Executive Brief | CEO, CTO, CDO, AI governance leaders | Companion Documents/ |
| CROA Implementation Primer | Enterprise architects, security architects, tech leads | Companion Documents/ |
| CROA Conformance Evidence Guide | Auditors, risk teams, independent assessors | Companion Documents/ |

The navigational scaffold for the whole corpus — including the appendix catalog and status of each appendix — is [Framework structure](../framework-structure.md). Where this front matter and a Part differ on technical content, the Part governs.

---

## Revision History

The table below records the framework's high-level evolution to the first public review release. A detailed, per-file change history is maintained in [CHANGELOG](../../CHANGELOG.md).

| Version | Description |
|---|---|
| 0.1 | Initial concept |
| 0.2 | Architecture refinement |
| 0.3 | Governance model updates |
| 0.4 | Threat model additions |
| **1.0 Draft** | **First public review release** |

---

*Continue to [Part I - Foundations](../parts/part-1-foundations.md).*
