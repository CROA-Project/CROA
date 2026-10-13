# Case 02 — €3,500, Finance Lead exception

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [02-exception-finance-3500](fr/02-exception-finance-3500.md).

**Outcome:** €3,500 · `DENY`, then `PERMIT_WITH_AUTHORIZATION` · executed

€3,500 violates `I-PAY-001`. `C2` denies through the Refusal Gateway. A human requester, never the agent, asks `C1` for an exception, a Finance Lead signs, and `C1` issues a single-use authorization artifact. The agent then submits a fresh request with no authorization field: `C2` finds the authorization in `C1`'s registry and returns `PERMIT_WITH_AUTHORIZATION`. `C7` binds `ecc.auth_ref` and `ecc.exception_scope`, and `C6` redeems `ecc.id` and `ecc.auth_ref` in the same compare-and-swap.

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

    AG->>HK: tool_call payment.create(amount, beneficiary_id, invoice_id)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
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
        C1-->>C2: signed policy artifacts (I-PAY-001, I-PAY-002, I-PAY-003) and any authorization artifacts
        C2->>C4: action under evaluation
        C4-->>C2: invariant state · I-PAY-003 aggregate for (ap-agent-01, beneficiary_id)
        C2->>C2: deterministic C2.eval (steps 1 to 6)
    end
    rect rgba(230, 160, 40, 0.12)
        Note over AG,C5: DENY · I-PAY-001 violated · no authorization artifact yet
        C2->>C5: DENY · deny_reason I-PAY-001 · invariant_state [I-PAY-001]
        C2->>C6: deny signal
        C6--xSRV: structured deny · invariant id · C5 reference · Refusal Gateway
        SRV--xAG: DENY
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Human-initiated escalation · the agent's output is never an input to C1 (§4.3)
        REQ->>C1: exception request via ITSM · references the C5 DENY record
        C1->>C5: exception request recorded
        C1->>APP: approval request (beneficiary, invoice, amount, invariant to waive I-PAY-001)
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Approval granted · C1 issues the authorization artifact
        APP->>C1: personal signature (key + MFA)
        C1->>C1: check approver role in the authoritative directory · Finance Lead+ required for I-PAY-001
        C1->>C1: issue authorization artifact · auth_id · subject ap-agent-01 · single action class payment.create · beneficiary, invoice, amount ≤ €3,500 · waived I-PAY-001 · single-use · expires_at
        C1->>C5: POLICY_ARTIFACT_ISSUED · artifact_action ISSUED · policy_artifact_id = auth_id
        REQ-->>AG: exception granted, retry (out of band)
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Resubmission · PERMIT_WITH_AUTHORIZATION
        AG->>SRV: new gar.* (new request_id, same parameters, no authorization field)
        SRV->>C3: gar.* · admission as before
        C3->>C2: gga.* · GROUNDED
        C1-->>C2: authorization artifact from C1's registry
        C4-->>C2: current invariant state
        C2->>C2: step 5 · I-PAY-001 violated but covered by a valid, applicable, unredeemed, unrevoked authorization
        C2->>C5: PERMIT · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C2->>C4: permitted · add €3,500 to I-PAY-003 aggregate (serialized per key)
        C2->>C7: PERMIT_WITH_AUTHORIZATION + authorization artifact
        C7->>C7: compile and sign ECC · auth_ref = auth_id · exception_scope copied verbatim · reversibility_class R2 · compensating_controls (approved invoice)
    end
    rect rgba(60, 120, 220, 0.10)
        Note over AG,C5: Execution · ECC presented at the boundary
        C7->>C5: ECC_COMPILED · ecc_id · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C7-->>SRV: ECC reference
        SRV-->>AG: permit + ECC reference
        AG->>SRV: execute payment.create with ECC reference
        SRV->>SRV: token exchange (RFC 8693) · sub ap-agent-01 · act mcp-payment-server · aud C6
        SRV->>C6: operation + ECC reference + exchanged token
        Note over C6: Execution boundary (TB-3)
        C6->>C6: C7 signature and signer epoch · not expired · not revoked · invariant_set_version consistent · operation within authorization_scope and exception_scope · sub equals ecc.subject · act is a registered presenter
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Admitted
        C6->>C6: one linearizable CAS · redeem ecc.id + ecc.auth_ref
        C6->>C5: EXECUTION_AUTHORIZED · ecc_id · auth_id
        C5-->>C6: committed
        C6->>API: POST /payments · C6 service identity
        API-->>C6: 201 payment created
        API--)C4: state change notification
        C4->>C4: post-execution invariant verification
        C6->>C5: EXECUTION_COMPLETED · ecc_id · exit_status
        C6-->>SRV: result
        SRV-->>AG: payment executed
    end

    Note over API: Accepts traffic from C6 only (P4, network-enforced). Neither the agent nor the MCP server holds an API credential.
```

[← Case 01 — €350, automatic](01-auto-350.md) · [Index](README.md) · [Case 03 — €7,500, CFO exception →](03-exception-cfo-7500.md)
