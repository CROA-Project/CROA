# Case 06 — exception refused

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [06-exception-refused](fr/06-exception-refused.md).

**Outcome:** €3,500 · `DENY` · approval refused or timed out · nothing executed

Starts like case 02, but the approver refuses, or does not answer before the request expires. `C1` issues no authorization artifact and records the refusal. The `DENY` stands: any resubmission is denied again on `I-PAY-001`, nothing is compiled, and the I-PAY-003 aggregate is unchanged.

## Overview

```mermaid
flowchart TD
    A(["AI agent · payment.create €3,500"]) --> H{"Hook<br/>tool on the allowlist?"}
    H -- no --> X1[["Blocked locally<br/>(see case 04)"]]
    H -- yes --> S{"MCP server · Agent Surface<br/>subject authenticated, RBAC?"}
    S -- no --> X2[["ADMISSION_REJECTED<br/>(see case 04)"]]
    S -- yes --> G{"C3 · grounding<br/>beneficiary and invoice known?"}
    G -- no --> X3[["CONTEXT_FAILURE<br/>refused via C6 (see case 05)"]]
    G -- yes --> D{"C2 · C2.eval<br/>with C4 state"}
    D -- "€3,500 · I-PAY-001 violated" --> DN[["DENY · I-PAY-001 violated<br/>structured refusal via C6 Refusal Gateway"]]
    DN --> EC(["End of the MCP call<br/>DENY returned immediately, nothing stays open"])
    subgraph ESC["Asynchronous escalation, outside any MCP call (minutes to days)"]
        direction TB
        RQ["Requester opens an ITSM request<br/>referencing the C5 DENY record"] --> AK["C1 asks the approver (Finance Lead)"]
        AK --> DC{"Approver's decision"}
        DC -- "refused or no answer before expiry" --> RF["C1 records the refusal<br/>no authorization artifact"]
        RF --> INF["Requester informs the agent"]
    end
    EC --> RQ
    INF --> RES[["DENY stands: any new call is denied again on I-PAY-001<br/>nothing compiled · I-PAY-003 unchanged · API never reached"]]

    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class X1,X2,X3,DN,RES ko;
    class H,S,G,D check;
    class RQ,AK,DC,RF,INF human;
    class EC note;
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
