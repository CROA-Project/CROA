# Case 07 — blocked at the execution boundary

> **Non-normative.** Part of the [governed payment via MCP](README.md) worked example. The shared context (invariants, reversibility, deployment, subject binding, vendor-neutrality note and spec references) is in the [README](README.md).

Version française: [07-boundary-blocked](fr/07-boundary-blocked.md).

**Outcome:** ECC replayed, spent, tampered, expired, stale or exceeded · `EXECUTION_BLOCKED`

What happens when something reaches `C6` that does not match a valid, unredeemed ECC. Each variant is recorded as `EXECUTION_BLOCKED` with its `block_reason` and committed to `C5` before the block is returned. The API is never reached. Variant E has no dedicated `block_reason` in the current spec; that is an open point raised with the maintainers.

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor AG as AI Agent<br/>(ap-agent-01)
    participant SRV as MCP Server<br/>(Agent Surface)
    participant C4 as C4 Invariant Monitor
    participant C6 as C6 Execution Firewall<br/>(egress gateway + Refusal Gateway)
    participant API as Payment API
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Starting point: ap-agent-01 holds an ECC reference obtained as in cases 01 to 03

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: A · Replay of an ECC already redeemed
        SRV->>C6: same ECC reference presented a second time
        C6->>C6: CAS on ecc.id fails · already redeemed
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_ALREADY_REDEEMED
        C5-->>C6: committed
        C6--xSRV: structured block · only after the C5 commit
        SRV--xAG: BLOCKED · API never reached
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: B · New ECC under an authorization already spent (cases 02, 03)
        SRV->>C6: second ECC whose auth_ref points to a redeemed auth_id
        C6->>C6: same CAS · auth_ref already redeemed, so ecc.id is not redeemed either
        C6->>C5: EXECUTION_BLOCKED · block_reason AUTHORIZATION_ALREADY_REDEEMED
        C5-->>C6: committed
        C6--xSRV: structured block · only after the C5 commit
        SRV--xAG: BLOCKED · API never reached
        Note over C4: The amount reserved in the I-PAY-003 aggregate is released (example choice)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: C · ECC tampered with, or expired
        SRV->>C6: ECC whose content no longer matches its hash, or past expires_at
        C6->>C6: integrity check or expiry check fails
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_INTEGRITY_INVALID or ECC_EXPIRED
        C5-->>C6: committed
        C6--xSRV: structured block · only after the C5 commit
        SRV--xAG: BLOCKED · API never reached
        Note over C4: The amount reserved in the I-PAY-003 aggregate is released (example choice)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: D · Invariant registry changed since compilation
        SRV->>C6: valid ECC, but a newer invariant prohibits its scope
        C6->>C6: invariant_set_version not consistent
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_INVARIANT_STALE · the ECC must be recompiled
        C5-->>C6: committed
        C6--xSRV: structured block · only after the C5 commit
        SRV--xAG: BLOCKED · API never reached
        Note over C4: The amount reserved in the I-PAY-003 aggregate is released (example choice)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: E · Operation differs from the ECC (for example amount raised from €350 to €3,500)
        SRV->>C6: valid ECC + operation outside ecc.authorization_scope
        C6->>C6: operation not within scope
        C6->>C5: EXECUTION_BLOCKED · no dedicated block_reason in the spec (open point)
        C5-->>C6: committed
        C6--xSRV: structured block · only after the C5 commit
        SRV--xAG: BLOCKED · API never reached
        Note over C4: The amount reserved in the I-PAY-003 aggregate is released (example choice)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: F · Direct call to the API, bypassing C6
        SRV-xAPI: POST /payments without going through C6
        Note over API: Refused at the network layer (P4). The MCP server holds no API credential anyway.
    end
```

[← Case 06 — exception refused](06-exception-refused.md) · [Index](README.md)
