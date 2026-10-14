# Case 03 — €7,500, CFO exception

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [03-exception-cfo-7500](fr/03-exception-cfo-7500.md).

**Outcome:** €7,500 · `DENY`, then `PERMIT_WITH_AUTHORIZATION` · executed

Same flow as case 02, with two differences. €7,500 violates both `I-PAY-001` and `I-PAY-002`, so `deny_reason` names `I-PAY-002` and `invariant_state` lists both. Only the CFO can approve, and the authorization artifact waives both invariants. It is still one artifact, for one action, used once.

## Overview

```mermaid
flowchart TD
    A(["AI agent · payment.create €7,500"]) --> H{"Hook<br/>tool on the allowlist?"}
    H -- no --> X1[["Blocked locally<br/>(see case 04)"]]
    H -- yes --> S{"MCP server · Agent Surface<br/>subject authenticated, RBAC?"}
    S -- no --> X2[["ADMISSION_REJECTED<br/>(see case 04)"]]
    S -- yes --> G{"C3 · grounding<br/>beneficiary and invoice known?"}
    G -- no --> X3[["CONTEXT_FAILURE<br/>refused via C6 (see case 05)"]]
    G -- yes --> D{"C2 · C2.eval<br/>with C4 state"}
    D -- "€7,500 · I-PAY-001 + I-PAY-002 violated" --> DN[["DENY · I-PAY-001 + I-PAY-002 violated<br/>structured refusal via C6 Refusal Gateway"]]
    DN --> EC(["End of the MCP call<br/>DENY returned immediately, nothing stays open"])
    subgraph ESC["Asynchronous escalation, outside any MCP call (minutes to days)"]
        direction TB
        RQ["Requester opens an ITSM request<br/>referencing the C5 DENY record"] --> AK["C1 asks the approver (CFO)"]
        AK --> DC{"Approver's decision"}
        DC -- "signs [S2]" --> VR["C1 checks [S2] and the role<br/>in the authoritative directory"]
        VR --> IS["C1 issues the authorization [S1]<br/>waives I-PAY-001 + I-PAY-002 · single-use · expires_at"]
        IS --> DI["C1 distributes it to C2"]
        DI --> INF["Requester informs the agent"]
    end
    EC --> RQ
    DC -. "refused" .-> X6[["refused: see case 06"]]
    INF --> NC(["New MCP call, before expires_at<br/>same parameters, new request_id"])
    NC --> AG2["Admission and grounding again<br/>(hook, Agent Surface, C3)"]
    AG2 --> S5["C2 · step 5: violation covered by a valid,<br/>unredeemed authorization → PERMIT_WITH_AUTHORIZATION"]
    S5 --> E
    E["C7 · compiles the ECC, signs it [S3]<br/>auth_ref + exception_scope · R2"] --> R(["Agent receives<br/>the ECC reference"])
    R --> F{"C6 · execution boundary<br/>ECC valid, right subject?"}
    F -- no --> X4[["EXECUTION_BLOCKED<br/>(see case 07)"]]
    F -- yes --> CAS["C6 · one CAS: ecc.id + auth_ref redeemed<br/>EXECUTION_AUTHORIZED in C5"]
    CAS --> API[("Payment API<br/>201 payment created")]
    API --> OK(["EXECUTION_COMPLETED<br/>payment executed"])

    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class S5,E,CAS,API,OK ok;
    class X1,X2,X3,DN,X6,X4 ko;
    class H,S,G,D,F,AG2 check;
    class RQ,AK,DC,VR,IS,DI,INF human;
    class EC,NC note;
```

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor AG as AI Agent<br/>(ap-agent-01)
    participant HK as Pre-execution Hook<br/>(defense-in-depth)
    participant SRV as MCP Server<br/>(Agent Surface)
    participant C3 as C3 Path Resolver
    participant C2 as C2 Execution Governor
    participant C4 as C4 Invariant Monitor
    participant C1 as C1 Policy Authority
    actor REQ as Requester<br/>(AP clerk · ITSM)
    actor APP as Approver<br/>(Finance Lead / CFO)
    participant C7 as C7 Contract Compiler
    participant C6 as C6 Execution Firewall<br/>(egress gateway + Refusal Gateway)
    participant API as Payment API
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prerequisites in place, see 00-prerequisites: rules signed [S1] and distributed · approvers enrolled · identities issued · only C6 reaches the API (P4)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        AG->>HK: tool_call payment.create(amount, beneficiary_id, invoice_id)
        HK->>SRV: tool call (tool is on the allowlist)
        SRV->>SRV: authenticate subject (workload identity) · RBAC · qualification
        SRV->>C3: gar.* (new request_id · ap-agent-01 · payment.create · beneficiary_id · invoice_id · amount)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Grounding
        C3->>C3: grounding against the Federated Context Registry · vendor master · invoice approved, unpaid, beneficiary match, amount ≤ open balance
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Evaluation
        C3->>C2: gga.* · semantic_result GROUNDED
        C2->>C4: action under evaluation
        C4-->>C2: invariant state · I-PAY-003 aggregate for (ap-agent-01, beneficiary_id)
        C2->>C2: deterministic C2.eval (steps 1 to 6) on the last verified policy artifact set
    end
    rect rgba(230, 160, 40, 0.12)
        Note over AG,C5: DENY · I-PAY-001 + I-PAY-002 violated · no authorization artifact yet
        C2->>C5: DENY · deny_reason I-PAY-002 · invariant_state [I-PAY-001, I-PAY-002]
        C2->>C6: deny signal
        C6--xSRV: answer to the gar.* request · structured deny · invariant id · C5 reference · Refusal Gateway
        SRV--xHK: DENY
        HK--xAG: DENY
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Human-initiated escalation · the agent's output is never an input to C1 (§4.3)
        REQ->>C1: exception request via ITSM · references the C5 DENY record
        C1->>C5: exception request recorded
        C1->>APP: approval request (beneficiary, invoice, amount, invariants to waive I-PAY-001 + I-PAY-002)
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Approval granted · C1 issues the authorization artifact
        APP->>C1: approves · approver's personal signature [S2] (personal key + MFA)
        C1->>C1: verifies signature [S2] and the approver's role in the authoritative directory · CFO required for I-PAY-002 (covers I-PAY-001)
        C1->>C1: issue authorization artifact · auth_id · subject ap-agent-01 · single action class payment.create · beneficiary, invoice, amount ≤ €7,500 · waived I-PAY-001 + I-PAY-002 · single-use · expires_at · signed with C1's key [S1]
        C1->>C5: POLICY_ARTIFACT_ISSUED · artifact_action ISSUED · policy_artifact_id = auth_id
        C1->>C2: distributes the authorization artifact signed [S1]
        C2->>C2: verifies signature [S1] · adds it to the verified set
        REQ->>AG: exception granted, retry (out of band)
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Resubmission · PERMIT_WITH_AUTHORIZATION
        AG->>HK: tool_call payment.create (same parameters, no authorization field)
        HK->>SRV: tool call
        SRV->>SRV: authenticate subject · RBAC · qualification
        SRV->>C3: new gar.* (new request_id)
        C3->>C3: grounding (as before)
        C3->>C2: gga.* · GROUNDED
        C2->>C4: action under evaluation
        C4-->>C2: current invariant state
        C2->>C2: step 5 · I-PAY-001 + I-PAY-002 violated but covered by a valid, applicable, unredeemed, unrevoked authorization
        C2->>C5: PERMIT · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C2->>C4: permitted · add €7,500 to I-PAY-003 aggregate (serialized per key)
        C2->>C7: PERMIT_WITH_AUTHORIZATION + authorization artifact
        C7->>C7: compile the ECC and sign it with C7's key [S3] · auth_ref = auth_id · exception_scope copied verbatim · reversibility_class R2 · compensating_controls (approved invoice)
    end
    rect rgba(60, 120, 220, 0.10)
        Note over AG,C5: Execution · ECC presented at the boundary
        C7->>C5: ECC_COMPILED · ecc_id · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C7->>SRV: ECC reference + decision notification (§4.10)
        SRV-->>HK: permit + ECC reference
        HK-->>AG: permit + ECC reference
        AG->>HK: execute payment.create with ECC reference
        HK->>SRV: tool call + ECC reference
        SRV->>SRV: token exchange with the identity provider (RFC 8693) · sub ap-agent-01 · act mcp-payment-server · aud C6
        SRV->>C6: operation + ECC reference + exchanged token
        Note over C6: Execution boundary (TB-3)
        C6->>C6: signature [S3] of C7 and signer epoch · not expired · not revoked · invariant_set_version consistent · operation within authorization_scope and exception_scope · sub equals ecc.subject · act is a registered presenter
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Admitted
        C6->>C6: one linearizable CAS · redeem ecc.id + ecc.auth_ref
        C6->>C5: EXECUTION_AUTHORIZED · ecc_id · auth_id
        C5-->>C6: committed
        C6->>API: POST /payments · C6 service identity (authentication, not an authorization signature)
        API-->>C6: 201 payment created
        API--)C4: state change notification
        C4->>C4: post-execution invariant verification
        C6->>C5: EXECUTION_COMPLETED · ecc_id · exit_status
        C6-->>SRV: result
        SRV-->>HK: result
        HK-->>AG: payment executed
    end

    Note over API: Accepts traffic from C6 only (P4, network-enforced). Neither the agent nor the MCP server holds an API credential.
```

[← Case 02 — €3,500, Finance Lead exception](02-exception-finance-3500.md) · [Index](README.md) · [Case 04 — unregistered tool →](04-unregistered-tool.md)
