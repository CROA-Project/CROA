# Case 03 — €7,500, CFO exception

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [03-exception-cfo-7500](fr/03-exception-cfo-7500.md).

**Outcome:** €7,500 · `DENY`, then `PERMIT_WITH_AUTHORIZATION` · executed

Same flow as case 02, with two differences. €7,500 violates both `I-PAY-001` and `I-PAY-002`, so `deny_reason` names `I-PAY-002` and `invariant_state` lists both. Only the CFO can approve, and the authorization artifact waives both invariants. It is still one artifact, for one action, used once.

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

    autonumber off
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Prerequisite · state before any request (on issuance or change, not numbered)
        C1->>C2: distributes policy artifacts signed with C1's key [S1] (I-PAY-001, I-PAY-002, I-PAY-003)
        C1->>C5: POLICY_ARTIFACT_ISSUED
        C2->>C2: verifies signature [S1] with C1's public key · keeps the last verified set (§4.3)
    end

    autonumber 1
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
