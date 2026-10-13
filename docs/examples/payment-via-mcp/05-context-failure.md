# Case 05 — context failure

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [05-context-failure](fr/05-context-failure.md).

**Outcome:** Unknown beneficiary or invoice · `CONTEXT_FAILURE` · refused

The request is admitted, but `C3` cannot ground it: the beneficiary is not in the vendor master, or the invoice is not approved, already paid, or for another beneficiary. A context failure is never forwarded to `C2` (§4.5.1, §4.10). `C3` records `CONTEXT_FAILURE` and hands the request to `C6`, whose Refusal Gateway returns a structured deny. No decision is made and no ECC exists.

## Overview

```mermaid
flowchart TD
    A(["AI agent · payment.create"]) --> H{"Hook<br/>tool on the allowlist?"}
    H -- no --> X1[["Blocked locally<br/>(see case 04)"]]
    H -- yes --> S{"MCP server · Agent Surface<br/>subject authenticated, RBAC?"}
    S -- no --> X2[["ADMISSION_REJECTED<br/>(see case 04)"]]
    S -- yes --> G{"C3 · grounding<br/>beneficiary and invoice known?"}
    G -- "no: unknown beneficiary, invoice not approved,<br/>already paid or other beneficiary" --> CF["C3 records CONTEXT_FAILURE in C5<br/>unresolved_refs"]
    CF --> C6["C3 hands the request to C6<br/>never to C2 (§4.5.1, §4.10)"]
    C6 --> X[["Structured deny via the Refusal Gateway<br/>no decision · no ECC · API never reached"]]

    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class X1,X2,CF,C6,X ko;
    class H,S,G check;
```

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

    Note over AG,C5: Prerequisites in place, see 00-prerequisites: rules signed [S1] and distributed · approvers enrolled · identities issued · only C6 reaches the API (P4)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        AG->>HK: tool_call payment.create(amount, beneficiary_id, invoice_id)
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
        C6--xSRV: answer to the gar.* request · structured deny (type, reason, C5 reference) · Refusal Gateway
        SRV--xHK: DENY
        HK--xAG: DENY
    end

    Note over API: Never reached (P4).
```

[← Case 04 — unregistered tool](04-unregistered-tool.md) · [Index](README.md) · [Case 06 — exception refused →](06-exception-refused.md)
