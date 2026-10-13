# Worked example — governed payment via MCP

> **Non-normative.** This example illustrates one way to realize the CROA logical architecture for a payment tool exposed over MCP. It adds no requirement. Where it differs from the specification, the specification governs. Invariant identifiers, thresholds, roles, the deployment split and the identity mechanism below are illustrative.
>
> **Vendor neutrality.** The example is technology-agnostic. It is compatible with an implementation that uses an agent runtime's own permission and hook mechanisms (for example, Claude Code hooks and permissions). That compatibility is not a certification by any vendor, and the hooks themselves provide no CROA guarantee. Conformance never requires any particular product (see [Vendor neutrality](../../README.md#vendor-neutrality)).

French version: [payment-via-mcp.fr.md](payment-via-mcp.fr.md).

## Scenario

An accounts-payable agent (`ap-agent-01`) can call the MCP tool `payment.create(amount, beneficiary_id, invoice_id)`. The payment API is a governed system behind the execution boundary.

The deployment is a **hybrid** (Part IV §18.3). The MCP server hosts the Agent Surface, as Part IV §23.5.2 suggests. `C6` runs at a separate egress gateway in front of the payment API, which is the DM-4 pattern (Part IV Chapter 22). In a pure DM-5 deployment `C6` would instead be embedded in the MCP server, and the MCP server would then hold the API credential.

The **pre-execution hook** in the agent runtime is **defense-in-depth only**. It catches unregistered tools early, but the guarantee does not come from it. The guarantee is `C6` together with P4: the payment API accepts traffic only from `C6`, and `C6` admits only operations derived from a valid, unredeemed ECC.

## Registered invariants (illustrative)

| Invariant | Class | Statement | Waivable by a `C1` authorization? |
|---|---|---|---|
| `I-PAY-001` | E1 | `payment.create` MUST NOT exceed €1,000 per payment without a `C1` authorization artifact covering the beneficiary, invoice and amount. | Yes, issued on a Finance Lead's (or higher) approval |
| `I-PAY-002` | E1 | `payment.create` MUST NOT exceed €5,000 per payment without a `C1` authorization artifact covering the beneficiary, invoice and amount. | Yes, issued on the CFO's approval |
| `I-PAY-003` | E2, TP-X | Cumulative `payment.create` value per (subject, `beneficiary_id`) over a rolling 24 h window MUST NOT exceed €10,000. | No: a cumulative breach is denied at `C2.eval` step 4, which has no authorization path (Part II §4.4.2) |

`I-PAY-003` is declared TP-X because a 24 h window spans sessions, and TP-X aggregates are keyed per subject (Part II §4.6.3). `C4` adds each permitted amount to the aggregate, serialized per key. In this example the amount is released again if the ECC is blocked, expires, or the execution fails.

**Reversibility.** A bank transfer is treated as **R2** (irreversible, low-impact) on every path. Every ECC therefore carries `ecc.reversibility_class = R2` and `ecc.compensating_controls`. In this example the R2 control is the prior human approval of the invoice in the ERP. `C3` verifies it at grounding: the invoice is approved and unpaid, its beneficiary matches, and the amount does not exceed the open balance. A Governed Exception is **not** recorded in `compensating_controls`; it is bound through `ecc.auth_ref` and `ecc.exception_scope`.

## The four paths

| Request | `C2.eval` outcome | Authorization | Result |
|---|---|---|---|
| €350 | `PERMIT` | none | ECC compiled and admitted |
| €3,500 | `DENY` (`I-PAY-001`), then `PERMIT_WITH_AUTHORIZATION` | Requested via ITSM; Finance Lead approves; `C1` issues `auth_id` waiving `I-PAY-001` | ECC with `auth_ref` and `exception_scope`; `ecc.id` and `auth_ref` redeemed in one CAS |
| €7,500 | `DENY` (`I-PAY-001`, `I-PAY-002`), then `PERMIT_WITH_AUTHORIZATION` | Same as above, with the CFO approving and both invariants waived | Same as above |
| Unregistered tool | none | none | Blocked by the hook. If the hook is bypassed: `ADMISSION_REJECTED` (`UNAUTHORIZED_ACTION_CLASS`) at the Agent Surface |

## Subject binding at the boundary

The MCP server presents the operation to `C6`, but the ECC subject is the agent. In this example the binding works like this:

1. The agent authenticates to the Agent Surface with a workload identity (for example, a SPIFFE SVID). That identity becomes `ecc.subject`.
2. To present, the MCP server performs an OAuth 2.0 token exchange (RFC 8693). The result is a short-lived token with `sub = ap-agent-01`, `act = mcp-payment-server` and audience `C6`, bound to the `ecc.id`.
3. `C6` checks that `sub` equals `ecc.subject` and that `act` is a registered presenter for this tool. An ECC presented under any other subject is blocked.

These checks are this example's own mechanism, not a §4.8 MUST. They implement the no-cross-subject-redemption clause of I8 (Part II §5.9, which cites Part IV §21.3). Neither the agent nor the MCP server holds a credential for the payment API; `C6` calls it with its own service identity. On identity and delegation, see Appendix O §O.5.

## Sequence

Solid arrows (`->>`) are synchronous. A `C5` write that must commit before the next step proceeds is shown with its acknowledgement.

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

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: CASE 1 · Tool not registered
        HK--xAG: blocked locally (fail-closed) · defense-in-depth only
        Note over AG,SRV: If the hook is bypassed or misconfigured
        AG->>SRV: direct tool call
        SRV->>C5: ADMISSION_REJECTED · rejection_reason UNAUTHORIZED_ACTION_CLASS · attempted_type
        SRV--xAG: rejected at the Agent Surface
        Note over C6,API: Even if both failed: no ECC, so C6 blocks and the API is unreachable (P4)
    end

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: CASE 2 · Registered tool
        HK->>SRV: tool call
        SRV->>SRV: authenticate subject (workload identity) · RBAC · qualification
        SRV->>C3: gar.* (new request_id · ap-agent-01 · payment.create · beneficiary_id · invoice_id · amount)
        C3->>C3: grounding against the Federated Context Registry · vendor master · invoice approved, unpaid, beneficiary match, amount ≤ open balance

        rect rgba(220, 60, 60, 0.10)
            Note over SRV,C5: 2a · Unknown beneficiary or invoice → CONTEXT_FAILURE (never forwarded to C2)
            C3->>C5: CONTEXT_FAILURE · unresolved_refs
            C3->>C6: gga.* with semantic_result CONTEXT_FAILURE
            C6--xSRV: structured deny (type, reason, C5 reference) · Refusal Gateway
            SRV--xAG: DENY
        end

        rect rgba(120, 120, 120, 0.06)
            Note over SRV,C5: 2b · GROUNDED
            C3->>C2: gga.* · semantic_result GROUNDED
            C1-->>C2: signed policy artifacts (I-PAY-001, I-PAY-002, I-PAY-003) and any authorization artifacts
            C2->>C4: action under evaluation
            C4-->>C2: invariant state · I-PAY-003 aggregate for (ap-agent-01, beneficiary_id)
            C2->>C2: deterministic C2.eval (steps 1 to 6)

            rect rgba(40, 170, 120, 0.12)
                Note over SRV,C5: €350 · no invariant violated → PERMIT
                C2->>C5: PERMIT · decision_basis PERMIT
                C2->>C4: permitted · add amount to I-PAY-003 aggregate (serialized per key)
                C2->>C7: PERMIT
                C7->>C7: compile and sign ECC · decision_basis PERMIT · reversibility_class R2 · compensating_controls (approved invoice)
            end

            rect rgba(230, 160, 40, 0.12)
                Note over AG,C5: €3,500 violates I-PAY-001 · €7,500 violates I-PAY-001 and I-PAY-002 · no authorization artifact yet
                C2->>C5: DENY · deny_reason I-PAY-001 (€3,500) or I-PAY-002 (€7,500) · invariant_state lists every violated invariant
                C2->>C6: deny signal
                C6--xSRV: structured deny · invariant id · C5 reference · Refusal Gateway
                SRV--xAG: DENY
                Note over AG,REQ: The agent's output is never an input to C1 (§4.3). A human requests the exception.
                REQ->>C1: exception request via ITSM · references the C5 DENY record
                C1->>C5: exception request recorded
                C1->>APP: approval request (beneficiary, invoice, amount, invariant(s) to waive)

                rect rgba(40, 170, 120, 0.12)
                    Note over C1,APP: Approval granted
                    APP->>C1: personal signature (key + MFA)
                    C1->>C1: check approver role in the authoritative directory · Finance Lead+ for I-PAY-001 · CFO for I-PAY-002
                    C1->>C1: issue authorization artifact · auth_id · subject ap-agent-01 · single action class payment.create · beneficiary, invoice, amount constraints · waived invariant(s) · single-use · expires_at
                    C1->>C5: POLICY_ARTIFACT_ISSUED · artifact_action ISSUED · policy_artifact_id = auth_id
                    REQ-->>AG: exception granted, retry (out of band)
                    AG->>SRV: new gar.* (new request_id, same parameters, no authorization field)
                    SRV->>C3: gar.*
                    C3->>C2: gga.* · GROUNDED
                    C1-->>C2: authorization artifact from C1's registry
                    C4-->>C2: current invariant state
                    C2->>C2: step 5 · violation covered by a valid, applicable, unredeemed, unrevoked authorization
                    C2->>C5: PERMIT · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
                    C2->>C4: permitted · add amount to I-PAY-003 aggregate (serialized per key)
                    C2->>C7: PERMIT_WITH_AUTHORIZATION + authorization artifact
                    C7->>C7: compile and sign ECC · auth_ref = auth_id · exception_scope copied verbatim · reversibility_class R2 · compensating_controls (approved invoice)
                end

                rect rgba(220, 60, 60, 0.10)
                    Note over C1,APP: Rejected, or no answer before expiry
                    APP--xC1: rejection / timeout
                    C1->>C5: exception refusal recorded
                    Note over AG,C5: No authorization artifact exists, so the DENY stands and nothing is compiled
                end
            end

            rect rgba(60, 120, 220, 0.10)
                Note over AG,C5: EXECUTION · only after PERMIT or PERMIT_WITH_AUTHORIZATION
                C7->>C5: ECC_COMPILED · ecc_id (decision_basis and auth_id on the exception path)
                C7-->>SRV: ECC reference
                SRV-->>AG: permit + ECC reference
                AG->>SRV: execute payment.create with ECC reference
                SRV->>SRV: token exchange (RFC 8693) · sub ap-agent-01 · act mcp-payment-server · aud C6
                SRV->>C6: operation + ECC reference + exchanged token

                Note over C6: Execution boundary (TB-3)
                C6->>C6: C7 signature and signer epoch · not expired · ECC and auth_id not revoked · invariant_set_version consistent · operation within authorization_scope (and exception_scope if auth_ref) · sub equals ecc.subject · act is a registered presenter

                rect rgba(40, 170, 120, 0.12)
                    Note over AG,C5: Valid ECC → admitted
                    C6->>C6: one linearizable CAS · redeem ecc.id (and ecc.auth_ref)
                    C6->>C5: EXECUTION_AUTHORIZED · ecc_id (and auth_id)
                    C5-->>C6: committed
                    C6->>API: POST /payments · C6 service identity
                    API-->>C6: 201 payment created
                    API--)C4: state change notification
                    C4->>C4: post-execution invariant verification
                    C6->>C5: EXECUTION_COMPLETED · ecc_id · exit_status
                    Note over C6,C5: If the API call fails: EXECUTION_FAILED, and the I-PAY-003 amount is released
                    C6-->>SRV: result
                    SRV-->>AG: payment executed
                end

                rect rgba(220, 60, 60, 0.10)
                    Note over AG,C5: ECC missing, tampered, expired, replayed, authorization already spent, invariants changed, or operation outside scope → blocked
                    C6->>C5: EXECUTION_BLOCKED · block_reason<br/>ECC_NOT_FOUND / ECC_INTEGRITY_INVALID / ECC_EXPIRED<br/>ECC_ALREADY_REDEEMED / AUTHORIZATION_ALREADY_REDEEMED / ECC_INVARIANT_STALE
                    C5-->>C6: committed
                    C6--xSRV: structured block · only after the C5 commit
                    SRV--xAG: BLOCKED · API never reached
                end
            end
        end
    end

    Note over API: Accepts traffic from C6 only (P4, network-enforced). Neither the agent nor the MCP server holds an API credential.
```

## Spec references

- `C1` policy authority; agent output is never a `C1` input: Part II §4.3
- Authorization artifacts, `auth_ref` / `exception_scope` binding, single-use redemption: Part II §4.3.1
- Signer epoch and revocation status: Part II §4.3.3
- `C2.eval` steps and the `PERMIT` / `PERMIT_WITH_AUTHORIZATION` outcomes: Part II §4.4.2
- ECC compilation: Part II §4.4.3, §4.8, and `spec/schemas/ecc.schema.json`
- `CONTEXT_FAILURE` routed to `C6`, never to `C2`: Part II §4.5.1, §4.10
- `C4` session history and post-execution verification: Part II §4.6
- Trajectory profiles (TP-C, TP-X) and serialized aggregates: Part II §4.6.3
- Governance event fields: Part II §4.7.1 and `spec/schemas/event.schema.json`
- Atomic redemption, `AUTHORIZATION_ALREADY_REDEEMED`, Refusal Gateway: Part II §4.8
- Agent Surface, RBAC and qualification: Part II §4.9, §4.9.1
- Authorized inter-component flows: Part II §4.10
- No cross-subject redemption (I8): Part II §5.9
- Reversibility classes: Part I Chapter 3, Tenet T5; Part II §4.4.1 (`ecc.reversibility_class`, `ecc.compensating_controls`)
- Hybrid configurations: Part IV §18.3; DM-4 gateway: Part IV Chapter 22; MCP as Agent Surface host: Part IV §23.5.2
- Exception requests through ITSM / ChatOps: Part IV §24.4
- Agent identity and delegation: Appendix O §O.5
- Worked invariant pattern (`I-EC-001`): Appendix P §P.3.4
- Single-use exception test: Appendix Q, NT-007
