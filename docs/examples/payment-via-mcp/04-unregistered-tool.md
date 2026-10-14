# Case 04 — unregistered tool

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [04-unregistered-tool](fr/04-unregistered-tool.md).

**Outcome:** Tool not registered · blocked at three layers

The agent calls a tool that is not registered (`wire.transfer`). The hook stops it first, but that is defense-in-depth only. If the hook is bypassed, the Agent Surface rejects the request with `ADMISSION_REJECTED` (`UNAUTHORIZED_ACTION_CLASS`). If both were bypassed, there would still be no ECC, so `C6` blocks and the API cannot be reached (P4). Access to a tool is not authority to execute.

## Overview

```mermaid
flowchart TD
    A(["AI agent · wire.transfer(...)<br/>tool not registered"]) --> H{"Layer 1 · hook<br/>tool on the allowlist?"}
    H -- no --> X1[["Blocked locally<br/>nothing is sent"]]
    H -. "hook bypassed or misconfigured" .-> S{"Layer 2 · Agent Surface<br/>does an RBAC role include this action?"}
    S -- no --> X2[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS · in C5"]]
    S -. "both bypassed" .-> F{"Layer 3 · C6<br/>ECC presented?"}
    F -- no --> X3[["EXECUTION_BLOCKED<br/>ECC_NOT_FOUND · in C5"]]
    X1 ~~~ N(["API never reached<br/>only C6 can reach it (P4)"])
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class X1,X2,X3 ko;
    class H,S,F check;
    class N note;
```

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor AG as AI Agent<br/>(ap-agent-01)
    participant HK as Pre-execution Hook<br/>(defense-in-depth)
    participant SRV as MCP Server<br/>(Agent Surface)
    participant C6 as C6 Execution Firewall<br/>(egress gateway + Refusal Gateway)
    participant API as Payment API
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prerequisites in place, see 00-prerequisites: rules signed [S1] and distributed · approvers enrolled · identities issued · only C6 reaches the API (P4)

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Layer 1 · hook (defense-in-depth only)
        AG->>HK: tool_call wire.transfer(...) · not on the allowlist
        HK->>HK: tool not on the allowlist
        HK--xAG: blocked locally (fail-closed) · nothing is sent
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Layer 2 · hook bypassed or misconfigured → Agent Surface
        AG->>SRV: direct tool call wire.transfer(...)
        SRV->>SRV: authenticate subject · RBAC: no role of ap-agent-01 includes this action type
        SRV->>C5: ADMISSION_REJECTED · rejection_reason UNAUTHORIZED_ACTION_CLASS · attempted_type
        SRV--xAG: rejected at the Agent Surface · nothing reaches C3 or C2
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Layer 3 · both bypassed → execution boundary (the actual guarantee)
        AG->>C6: operation without an ECC reference
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_NOT_FOUND
        C5-->>C6: committed
        C6--xAG: structured block
    end

    Note over API: Never reached. Accepts traffic from C6 only (P4, network-enforced).
```

[← Case 03 — €7,500, CFO exception](03-exception-cfo-7500.md) · [Index](README.md) · [Case 05 — context failure →](05-context-failure.md)
