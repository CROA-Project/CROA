---
tags:
  - croa_foundation
---

# Appendix E — Mapping to NIST SP 800-207 (Zero Trust Architecture)

**CROA Framework v1.0.1.1 · Informative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The
CROA applies Zero Trust principles to agent state transitions rather than network packets (Part I §1.5). This crosswalk is orientational; CROA conformance is defined solely by Parts I–VI.

**ZT logical components → CROA.**

| NIST 800-207 component | CROA realization |
|---|---|
| Policy Engine (decision) | `C2` (Execution Governor / PDP) — `C2.eval` |
| Policy Administrator (establishes/terminates the path) | `C7` — Contract Compiler (produces the ECC) + `C6` |
| Policy Enforcement Point | `C6` (Execution Firewall) enforcing TB-3 |
| Policy (rules feeding the PE) | `C1` policy artifacts (signed, versioned) |
| Data sources / CDM, context | `C3` (Federated Context Registry) and `C4` (invariant state, trajectory) |
| Activity logs / audit | `C5` (Audit and Provenance Store) |
| Identity / ICAM | Agent Surface authentication + RBAC (§4.9.1), via IP-1 (IAM/OIDC) |

**ZT tenets → CROA expression.**

| ZT tenet (abridged) | CROA expression |
|---|---|
| All resources accessed securely regardless of location | TB-3: only ECC-derived operations reach governed systems |
| Access granted per-session, least privilege | RBAC eligibility (§4.9.1) + per-action `C2.eval` |
| Access determined by dynamic policy | `C1` policy + `C4` invariant state at decision time |
| No implicit trust; continuous verification | T6 (no intent-based trust); AQL continuous qualification (§4.9.2) |
| Integrity/security posture of assets monitored | `C4` trajectory analysis; AQL configuration-fingerprint validation |
| Authentication/authorization dynamic and strictly enforced | Four-stage admission model (§4.9.2) before the pipeline |
| Collect data to improve posture | `C5` evidence; Policy Deployment (§7.2) operation reviews |

Cross-reference: IP-1 and IP-2 (Part IV, Chapter 24) are the concrete Zero Trust integration patterns.

---

*End of Appendix E — Mapping to NIST SP 800-207.*
