# CROA Framework — Part III: Policy-as-Code & Lifecycle

**Version:** 1.0.1

## Chapter 7. GitOps and CI/CD Governance Integration

**Chapter abstract.** This chapter defines the mandatory Policy-as-Code (PaC) lifecycle for the CROA architecture. The legacy nine-phase architecture cycle has been entirely removed to eliminate bureaucratic bottlenecks. CROA governance is now managed strictly through declarative code, utilizing standard Continuous Integration and Continuous Deployment (CI/CD) pipelines. This ensures that governance mechanisms operate with the same velocity, automation, and determinism as the generative AI systems they regulate.

### 7.1 Policy-as-Code Principles

A conformant CROA implementation MUST manage all governance artifacts through a declarative Policy-as-Code (PaC) paradigm.

The Policy Authority (C1) operates as an automated engine integrated within the enterprise version control system (e.g., Git). Manual architecture review boards and phase-gated methodologies are strictly outside the scope of the CROA execution path. The Automated CAB relies on machine-readable policies to produce the Execution Change Contract (ECC).

### 7.2 The GitOps Workflow

The lifecycle of a governance rule MUST adhere to the following GitOps workflow:

1. **Definition:** Policies MUST be defined in standard declarative formats (e.g., JSON/YAML schemas, OPA/Rego, or AWS Cedar).
2. **Proposal:** Modifications, additions, or revocations of policies MUST be submitted as version-controlled change requests (e.g., Pull Requests).
3. **Validation:** CI/CD pipelines MUST automatically validate the proposed policy against the authoritative schema definitions prior to approval. This includes static analysis and conflict detection against the existing invariant registry.
4. **Deployment:** Upon merge to the primary branch, the C1 component MUST dynamically and securely distribute the updated policies to the Execution Governor (C2) and the Federated Path Resolver (C3).
5. **Rollback:** In the event of a critical governance failure, the version control system MUST support automated reversion to the previous stable policy state.

## Chapter 8. Schema Definitions for Policies

**Chapter abstract.** This chapter outlines the canonical schemas required for policy definition and the Execution Change Contract (ECC). These schemas replace the narrative documentation of legacy governance.

### 8.1 Governance Policy Schema

To guarantee deterministic evaluation by C2, governance rules MUST conform to a standardized, machine-readable schema. The schema enforces strict typing and prevents execution ambiguity.

```yaml
# Canonical CROA Policy Schema (Informative Example)
apiVersion: croa.dev/v1.0.1
kind: GovernancePolicy
metadata:
  name: core-data-protection
  domain: enterprise-global
spec:
  rules:
    - action: data.export
      condition: "target.env != 'production'"
      enforcement: BLOCKING
      evaluability: E1
    - action: config.change
      condition: "request.user.role == 'system_agent'"
      enforcement: CONSTRAINED
      evaluability: E2
```

### 8.2 Execution Change Contract (ECC) Schema

The ECC serves as the authoritative, machine-speed ITIL Change Record. The Contract Compiler (C7) MUST generate an ECC that strictly adheres to the following structural requirements. It completely replaces the legacy "Request for Change".

* **ECC Identifier:** A cryptographic hash (SHA-256 or stronger) of the contract payload.
* **Subject:** The authenticated identity of the autonomous agent initiating the change.
* **Action Scope:** The exact permitted action and target system boundaries.
* **Temporal Bounds:** Strict issuance and expiration timestamps.
* **Signatures:** M-of-N signatures where applicable, prioritizing standard mTLS for routine operations and reserving HSM-backed signatures for policy root mutations.
