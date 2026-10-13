# Case 05 — context failure

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [05-context-failure](fr/05-context-failure.md).

**Outcome:** Unknown beneficiary or invoice · `CONTEXT_FAILURE` · refused

The request is admitted, but `C3` cannot ground it: the beneficiary is not in the vendor master, or the invoice is not approved, already paid, or for another beneficiary. A context failure is never forwarded to `C2` (§4.5.1, §4.10). `C3` records `CONTEXT_FAILURE` and hands the request to `C6`, whose Refusal Gateway returns a structured deny. No decision is made and no ECC exists.

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor AG as AI Agent<br/>(ap-agent-01)
    participant HK as Pre-execution Hook<br/>(defense-in-depth)
    participant SRV as MCP Server<br/>(Agent Surface)
    participant C3 as C3 Path Resolver
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
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Grounding fails · unknown beneficiary, or invoice not approved / already paid / beneficiary mismatch
        C3->>C3: grounding against the Federated Context Registry · reference cannot be resolved
        C3->>C5: CONTEXT_FAILURE · unresolved_refs
        C3->>C6: gga.* with semantic_result CONTEXT_FAILURE
        Note over C3,C6: Never forwarded to C2 (§4.5.1, §4.10): no decision, no ECC
        C6--xSRV: structured deny (type, reason, C5 reference) · Refusal Gateway
        SRV--xAG: DENY
    end

    Note over API: Never reached (P4).
```

[← Case 04 — unregistered tool](04-unregistered-tool.md) · [Index](README.md) · [Case 06 — exception refused →](06-exception-refused.md)
