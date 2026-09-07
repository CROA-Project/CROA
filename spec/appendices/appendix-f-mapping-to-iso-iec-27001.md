---
tags:
  - croa_foundation
---

# Appendix F — Mapping to ISO/IEC 27001 (Annex A, 2022)

**CROA Framework v1.0.1.1 · Informative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The
ISO/IEC 27001 specifies an information-security management system; CROA is a technical control architecture that supplies evidence for several Annex A controls (Part I §1.5). The mapping is approximate and non-exhaustive.

| Annex A control (2022) | CROA contribution |
|---|---|
| 5.7 Threat intelligence | Part V threat model (TH-1…TH-11) and Policy Validation (§7.2) assessment |
| 5.15 Access control | RBAC subject authorization (§4.9.1) |
| 5.16 Identity management | Subject identity at the Agent Surface (TB-1) |
| 5.17 Authentication information | IdP integration (IP-1); token verification |
| 8.2 Privileged access rights | Authorization artifacts / Constrained Execution Mode (§4.3.1) |
| 8.3 Information access restriction | Access-control invariants (§5.8 taxonomy) |
| 8.15 Logging | `C5` synchronous, typed governance events (I6) |
| 8.16 Monitoring activities | `C4` monitoring; `C5` detection signatures (Part V) |
| 8.17 Clock synchronization | `event.timestamp` (ISO 8601 UTC) in every `C5` event |
| 8.24 Use of cryptography | Policy/ECC signing, `event.chain_hash` chaining |
| 8.28 Secure coding | AQL Secure Coding qualification battery (illustrative, §4.9.2) |
| 8.32 Change management | CROA-PaC GitOps Pipeline (§7.2) |

Cross-reference: the ISO/IEC 27001 §§8.15–8.17 ↔ `C5` relationship is noted in Part I §1.5.

---

*End of Appendix F — Mapping to ISO/IEC 27001.*
