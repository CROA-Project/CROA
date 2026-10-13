# Case 04 — unregistered tool

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [04-unregistered-tool](fr/04-unregistered-tool.md).

**Outcome:** Tool not registered · blocked at three layers

The agent calls a tool that is not registered (`wire.transfer`). The hook stops it first, but that is defense-in-depth only. If the hook is bypassed, the Agent Surface rejects the request with `ADMISSION_REJECTED` (`UNAUTHORIZED_ACTION_CLASS`). If both were bypassed, there would still be no ECC, so `C6` blocks and the API cannot be reached (P4). Access to a tool is not authority to execute.

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

    AG->>HK: tool_call wire.transfer(...) · not on the allowlist

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Layer 1 · hook (defense-in-depth only)
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
