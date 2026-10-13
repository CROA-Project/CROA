# Case 06 — exception refused

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [06-exception-refused](fr/06-exception-refused.md).

**Outcome:** €3,500 · `DENY` · approval refused or timed out · nothing executed

Starts like case 02, but the approver refuses, or does not answer before the request expires. `C1` issues no authorization artifact and records the refusal. The `DENY` stands: any resubmission is denied again on `I-PAY-001`, nothing is compiled, and the I-PAY-003 aggregate is unchanged.

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
        C1->>C2: distributes signed policy artifacts (I-PAY-001, I-PAY-002, I-PAY-003)
        C1->>C5: POLICY_ARTIFACT_ISSUED
        C2->>C2: verifies the C1 signature · keeps the last verified set (§4.3)
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
        Note over AG,C5: DENY · I-PAY-001 violated · no authorization artifact yet
        C2->>C5: DENY · deny_reason I-PAY-001 · invariant_state [I-PAY-001]
        C2->>C6: deny signal
        C6--xSRV: answer to the gar.* request · structured deny · invariant id · C5 reference · Refusal Gateway
        SRV--xHK: DENY
        HK--xAG: DENY
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Human-initiated escalation · the agent's output is never an input to C1 (§4.3)
        REQ->>C1: exception request via ITSM · references the C5 DENY record
        C1->>C5: exception request recorded
        C1->>APP: approval request (beneficiary, invoice, amount, invariant to waive I-PAY-001)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Approval refused or timed out
        APP--xC1: rejection, or no answer before the request expires
        C1->>C5: exception refusal recorded
        REQ->>AG: exception refused (out of band)
        Note over C2,C7: No authorization artifact exists: a resubmission is denied again on I-PAY-001, and nothing is ever compiled
        Note over C4: Nothing was permitted, so the I-PAY-003 aggregate is unchanged
    end

    Note over API: Never reached: no ECC exists (P4).
```

[← Case 05 — context failure](05-context-failure.md) · [Index](README.md) · [Case 07 — blocked at the execution boundary →](07-boundary-blocked.md)
