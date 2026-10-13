# 00 — Prerequisites

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [00-prerequisites](fr/00-prerequisites.md).

**Scope:** What must be in place before any request

Not a case: the state every case relies on. Four things are set up before the first request. The rules (`I-PAY-001` to `003`) go through a pull request, CI validation and approval by a second person, then `C1` signs them [S1] and distributes them to `C2` and `C3`. Approvers are enrolled in the authoritative directory with their personal key and role, which is what lets `C1` check their signature [S2] later. The agent receives its workload identity and its RBAC role, and the MCP server is registered as a presenter. Finally, `C7`'s key [S3] is known to `C6`, and only `C6` can reach the payment API (P4). Nothing here is numbered as a request step; the cases start numbering at the agent's call.

## Overview

```mermaid
flowchart TD
    subgraph R1["1 · Rules (Part III §7.2, §7.3)"]
        direction TB
        PR["Pull request<br/>invariants I-PAY-001 to 003"] --> CI["CI validation<br/>schemas + invariant registry"]
        CI --> AP2["Approval by a second person<br/>(proposal ≠ approval)"]
        AP2 --> MG["Merge to main branch"]
        MG --> SG["C1 signs the artifact [S1]<br/>key in an HSM"]
        SG --> LOG["C5 · POLICY_ARTIFACT_ISSUED"]
        SG --> D2["C2 verifies [S1]<br/>keeps the last verified set"]
        SG --> D3["C3 verifies [S1]"]
    end
    subgraph R2["2 · Approvers"]
        direction TB
        EN["Approver enrolls<br/>personal key + MFA"] --> DIR["Authoritative directory<br/>identity, key, role (Finance Lead, CFO)"]
        DIR -. "at approval time (cases 02, 03)" .-> USE["C1 checks [S2] and the role"]
    end
    subgraph R3["3 · Identities"]
        direction TB
        WID["Directory issues the agent's<br/>workload identity (for example SPIFFE)"] --> RB["RBAC role of ap-agent-01<br/>includes payment.create"]
        PRS["mcp-payment-server registered at C6<br/>as presenter for payment.create"]
    end
    subgraph R4["4 · Execution boundary"]
        direction TB
        K7["C7 signs ECCs [S3]<br/>C6 knows C7's public key + revocation status"]
        P4["Payment API reachable from C6 only (P4)<br/>only C6 holds the API credential"]
        REG["C4 gives C6 the current<br/>invariant registry version (§4.10)"]
    end
    R1 ~~~ R2 ~~~ R3 ~~~ R4
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class PR,CI,AP2,MG,EN human;
    class SG,D2,D3,LOG,REG,DIR,USE,WID,RB,PRS,K7,P4 check;
```

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor GOV as Governance team<br/>(Git · pull requests)
    participant DIR as Authoritative directory<br/>(IdP / IAM)
    actor APP as Approver<br/>(Finance Lead / CFO)
    actor AG as AI Agent<br/>(ap-agent-01)
    participant SRV as MCP Server<br/>(Agent Surface)
    participant C1 as C1 Policy Authority
    participant C2 as C2 Execution Governor
    participant C3 as C3 Path Resolver
    participant C4 as C4 Invariant Monitor
    participant C7 as C7 Contract Compiler
    participant C6 as C6 Execution Firewall<br/>(egress gateway + Refusal Gateway)
    participant API as Payment API
    participant C5 as C5 Audit (append-only)

    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 1 · Rules: from a pull request to C2 and C3 (Part III §7.2, §7.3)
        Note right of GOV: author opens a pull request: invariants I-PAY-001, I-PAY-002, I-PAY-003 (policy as code)
        Note right of GOV: CI validates against the schemas and the existing invariant registry
        Note right of GOV: approved by a different person (proposal and approval are distinct principals)
        GOV->>C1: merge to the main branch
        C1->>C1: signs the policy artifact with C1's key [S1] (key held in an HSM, §4.3.3)
        C1->>C5: POLICY_ARTIFACT_ISSUED
        C1->>C2: distributes the signed artifact
        C1->>C3: distributes the signed artifact
        C2->>C2: verifies [S1] · keeps the last verified set
        C3->>C3: verifies [S1]
        C4->>C6: current invariant registry version (§4.10)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 2 · Approvers: enrolled before they can approve
        APP->>DIR: enrollment: personal signing key + MFA bound to the person's identity
        DIR->>DIR: role assigned through the IAM process (Finance Lead, CFO)
        Note over DIR,C1: At approval time (cases 02, 03), C1 checks signature [S2] and the role against this directory
    end
    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 3 · Agent and MCP server identities
        DIR->>AG: workload identity for ap-agent-01 (for example a SPIFFE SVID)
        DIR->>DIR: RBAC role of ap-agent-01 includes payment.create, and nothing that moves money otherwise
        Note over SRV,C6: mcp-payment-server is registered at C6 as a presenter for payment.create (example's own mechanism)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 4 · Execution boundary
        Note over C7,C6: C7 signs ECCs with its own key [S3]. C6 knows C7's public key and consults the revocation status (§4.3.3)
        Note over API,C5: API reachable from C6 only (P4, network)<br/>Only C6 holds the API credential
    end
```

[Index](README.md) · [Case 01 — €350, automatic →](01-auto-350.md)
