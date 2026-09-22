---
rfc: 0000
title: Governed Action Catalog and Session Action-Surface Admission
status: draft
change_level: extension
authors: [Sylvain Durand]
created: 2026-09-22
affects: [Part II §4.9, Part III §9.2, Part III §9.3, Appendix B, Appendix Q, event.schema.json]
tracking_issue: https://github.com/CROA-Project/CROA/issues/21
---

# RFC 0000 — Governed Action Catalog and Session Action-Surface Admission

## Summary

An agent or orchestrator may request a set of tools/actions for a task or session. CROA determines which subset of those capabilities is actually admissible for that subject and session.

This RFC proposes a governed layer before individual action execution. The central distinction is: **Available to request != authorised to execute.** Tool admission does not grant execution authority. Every individual invocation remains governed by the existing `GAR → C3/C4/C2 → C7/ECC → C6` pipeline.

## Motivation

This RFC aims to narrow the available action surface for a governed agent during a task or session, minimizing unnecessary capability exposure.

This relates to CROA research questions **RQ-2** and **RQ-4**. The Governed Action Catalog (GAC) helps represent the modeled action space, and the Effective Action Set helps narrow that surface per task/session.

However, this RFC does NOT automatically solve the translation of a domain-level requirement into exact invariants. For example, the domain requirement: *"Sensitive information must never leave the authorised perimeter."*
Exact enforcement still requires typed representation of resources, destinations, trust zones, classification, provenance/lineage, parameters, and information-flow properties. If attributes are structurally represented, an invariant like `derived_from_sensitive = true AND destination.trust_zone != APPROVED → DENY` may be evaluated at E1/E2. Asking a semantic model *"Does this generated content contain sensitive information?"* remains firmly at E3 where exact structural representation is unavailable. This RFC narrows the action surface but does not overclaim the capability to automatically bridge semantic domain rules into exact invariants.

## Change Level and Impact

This RFC is positioned as a conditional-normative **extension/profile** for now.

The current evidence base does not firmly establish that task/session action-surface narrowing improves the utility–guarantee tradeoff (precisely RQ-4). Therefore:

- Deployments that implement Session Action-Surface Admission MUST follow the RFC requirements.
- Existing CROA L0–L5 conformance semantics are NOT changed by this RFC.
- Future pilot evidence may justify promotion into the core conformance model.

## Detailed Design

### 1. Agent Surface Composition

When this extension is enabled, Session Action-Surface Admission acts as an **ADDITIONAL conjunctive admission condition**.

Conceptually:

- **Core eligibility:** RBAC (§4.9.1) + AQL where applicable (§4.9.2)
- **Extension:** The concrete invoked capability must map to a `gac.entry_id` that is present in the current session/task Effective Action Set.

This extension MUST only narrow admission. It MUST NOT replace RBAC or AQL. It explicitly does NOT modify the existing ECC execution path.

### 2. Governed Action Catalog (GAC) Specializes C1 Policy

The **Governed Action Catalog (GAC)** is the structured, C1-issued representation of the modeled action/tool surface governed under existing C1 policy authority.

The GAC MUST NOT become a second independent source of truth. The current specification states that the set of valid action types is defined in the applicable C1 policy artifact. If GAC and another applicable C1 artifact disagree, the system MUST fail closed; precedence must not be invented silently.

Agent requests NEVER update the GAC and are never direct policy-authoring inputs to C1.

### 3. GAC Identity Model

The semantic action class must be separated from the provider implementation. The same canonical action class may be implemented by multiple providers/tools with different schemas and governance bindings.

A GAC entry should include:

- `gac.entry_id` — stable catalog-entry identifier
- `gac.action_type` — canonical `gar.type`
- `gac.provider_id` — governed provider identity
- `gac.provider_action_name` — provider-native tool name
- `gac.entry_version`
- `gac.source`
- `gac.description`
- `gac.schema_version`
- `gac.schema_digest`
- `gac.scope` (provider capability envelope where appropriate)
- `gac.deprecated`

Note: Fixed risk or reversibility classifications are intentionally omitted from the entry. The Part V inherent risk baseline is non-normative. Furthermore, CROA T5 classifies the governed transition; a concrete action context, target, and parameters can change the consequence class. The GAC cannot replace or lower the transition-level classification used for the actual governed action.

### 4. MCP / Provider Boundary

**Tool discovery is not tool admission.**
An MCP server may advertise candidate tools. Provider-advertised tools MUST NOT become governed capabilities automatically. Provider-supplied descriptions, prompts, schemas, and examples are not authoritative governance content merely because the provider supplied them. The enterprise-controlled GAC definition remains authoritative.

### 5. Schema Drift

Schema drift is defined deterministically against the exact GAC entry/provider binding:
`observed canonical schema digest != approved gac.schema_digest`

The canonicalization method and hash algorithm must be pinned as part of the governed catalog definition. Any digest mismatch is drift. A different provider that shares the same `gac.action_type` does not inherit another entry's approved schema digest.

If schema drift occurs, the system MUST fail closed. Provider drift MUST NOT automatically update the GAC.
This mechanism detects schema drift, not arbitrary semantic implementation drift behind an unchanged schema.

### 6. Requested Action Set

The **Requested Action Set** is untrusted agent-side input. It means only: *"These are the action classes requested for this task/session."*

This set is normalized by the Agent Surface into requested GAC entry references (`gac.entry_id`). The agent does not need to know or author internal catalog identifiers directly. For example, an MCP tool selection may arrive as provider/tool identity, but the Agent Surface maps it to the authoritative `gac.entry_id` before calculating the Effective Action Set. Provider discovery remains non-authoritative.

It may only remove possibilities through intersection. It MUST NOT:

- Modify GAC or C1 policy
- Create an authorization artifact
- Satisfy an invariant
- Widen RBAC/AQL eligibility
- Influence a permit decision except by causing earlier rejection when an action is outside the admitted set

This preserves T6/I8.

### 7. Effective Action Set and Session Binding

Define the authoritative **Effective Action Set** as a set of admitted `gac.entry_id` references, not merely canonical `gar.type` values.

Conceptually, applying monotonicity:
`EffectiveActionSet(session) ⊆ RequestedCatalogEntries ∩ CataloguedEntries ∩ (entries whose gac.action_type is RBAC-eligible) ∩ (entries satisfying qualification where applicable) ∩ (entries compatible with applicable C1 policy scope)`

It must be bound to enough state to prevent reuse outside the admission decision:

- Authenticated subject
- Task/session ID
- GAC artifact/version
- Policy artifact/version
- Qualification state/version (where applicable)
- Issuance time
- Surface version/generation

Relevant changes (GAC change, policy change, role change) invalidate or require recomputation. No second execution token is invented.

### 8. Individual Admission Rule and Agent Surface Binding

The GAR schema remains unchanged. Do NOT add `provider_id` or `gac.entry_id` to `gar.*`. Instead, we define an Agent Surface binding.

For provider/tool-backed actions, the Agent Surface must deterministically bind the concrete invoked capability to exactly one governed GAC entry using governed attributes.

Conceptually:
`(provider_id, provider_action_name, observed_schema_digest) → gac.entry_id → gac.action_type → gar.type`

**Provider Identity Must Not Be Agent-Authored**
The `provider_id`, `provider_action_name`, and observed schema metadata used for admission MUST come from a trusted deployment-controlled binding. They MUST NOT be accepted as authoritative merely because the governed agent supplied them. For MCP-backed actions, provider identity SHOULD be derived from the authenticated MCP connection / configured server binding / deployment-controlled endpoint identity, or another authoritative deployment mechanism. Agent-provided provider/tool identifiers are untrusted hints only. If the Agent Surface cannot establish the provider/tool identity independently, it MUST fail closed. This is strictly an Agent Surface / deployment binding concern before C3.

The authoritative binding comes from GAC, not provider prose. If no unique current GAC entry can be established, fail closed.

**Individual Admission Rule**:
For a provider/tool-backed invocation, the Agent Surface MUST first resolve the concrete invoked capability to a current `gac.entry_id`.
If `resolved gac.entry_id NOT IN EffectiveActionSet(session)`, the invocation MUST be rejected before C3.

**gar.type Must Be Derived or Verified**
Once the Agent Surface resolves `gac.entry_id → gac.action_type`, the resulting canonical action class MUST control the `gar.type` entering the CROA pipeline.

- If the Agent Surface constructs the GAR, it MUST set `gar.type = gac.action_type`.
- If the governed agent supplied a GAR containing `gar.type`, the Agent Surface MUST verify `gar.type == gac.action_type` and reject the request if they differ. The agent MUST NOT be able to choose a different `gar.type` after admission.

A typed admission rejection (such as `ACTION_TYPE_BINDING_MISMATCH`) must be used. Do not silently rewrite a mismatching agent-authored GAR without recording the mismatch.

For direct/client action surfaces that are not provider-tool-backed, define an equivalent governed binding to a GAC entry. There is no bypass category.

### 9. Critical Distinction: Admitted != Authorized

**An admitted action is still not authorized to execute.**
Membership in the Effective Action Set is necessary only for admission under this extension and never sufficient for execution.

For example, admitting a specific github-prod implementation of `code.change` does NOT imply execution. A concrete invocation still proceeds through the standard path (`GAR → C3/C4/C2`).

If a relevant invariant is violated, C2 will return a `DENY`. In this case:

- No ECC is compiled.
- C6 receives no executable commitment.
- No external effect occurs.

### 10. C5 Evidence Mechanics

C5 should capture sufficient evidence to reconstruct: `requested → admitted → invoked → permitted/denied → executed`

We propose dedicated event concepts for audit mechanics:

- `ACTION_SURFACE_ESTABLISHED`
- `ACTION_SURFACE_UPDATED`

These events should record effective `gac.entry_id` values and their canonical `gac.action_type` values, binding at least:

- `subject_id`
- session/task identifier
- requested action/tool references
- effective admitted entries/action classes
- rejected entries + typed reasons
- GAC artifact/version
- applicable policy artifact/version
- qualification reference where applicable
- surface version/generation
- timestamp

For rejected tool invocations, evidence should make it possible to reconstruct:
`provider/tool identity → resolved gac.entry_id → admission result`
without relying on agent narration.

For provider/tool binding decisions, C5 evidence should make it possible to reconstruct:
`trusted provider/session binding → provider tool identity → observed schema digest → resolved gac.entry_id → canonical gac.action_type → supplied gar.type if present → admission result`
Do not rely on agent narration as proof of provider identity.

Individual GAR rejection because it is outside the current Effective Action Set should remain an `ADMISSION_REJECTED` event with a new typed rejection reason: `ACTION_NOT_ADMITTED_FOR_SESSION`.

### 11. NT-009 Negative Tests

A focused **NT-009** family of negative tests:

- **NT-009.A — Uncatalogued action**: Expected: not admitted, no request reaches C3, C5 evidence.
- **NT-009.B — Catalogued but unauthorized**: Expected: absent from Effective Action Set, no authority expansion.
- **NT-009.C — Admitted action still denied**: Action is in Effective Action Set but concrete invocation violates an invariant. Expected: normal CROA request path, C2 DENY, no ECC, no external effect. (Crucial proof that tool admission != execution authorization).
- **NT-009.D — Action absent from current Effective Action Set**: Action is globally catalogued and normally role-eligible but absent from this session's Effective Action Set. Expected: reject before C3, no ECC, no effect.
- **NT-009.E — Provider schema drift**: Expected: fail closed, no silent GAC update, C5 evidence.
- **NT-009.F — Authority non-expansion**: A broad request cannot widen existing subject authority.
- **NT-009.G — Safe inability to continue**: Expected: escalation/clarification/out-of-scope outcome, no automatic capability grant, no governed external effect.
- **NT-009.H — Same action class, different provider**:
  - **Setup**: Two GAC entries map to the same `gac.action_type / gar.type`; only provider A's entry is in the Effective Action Set; provider B exposes an equivalent-named or semantically equivalent tool.
  - **Expected**: Provider A invocation can proceed to normal GAR evaluation. Provider B invocation is rejected at Agent Surface before C3. The shared `gar.type` MUST NOT cause provider B to inherit provider A's admission. No ECC is compiled for provider B, and C5 records the rejected `gac.entry_id`/provider binding. This falsifies any collapse of provider/tool distinction.
- **NT-009.I — Provider/action binding spoof**:
  - **A. Agent claims provider A identity while invocation arrives through provider B**: Expected: fail closed before C3, no ECC, C5 evidence of binding failure.
  - **B. Concrete provider/tool resolves to `gac.action_type = code.change` but agent-supplied GAR claims `gar.type = data.read`**: Expected: `ADMISSION_REJECTED` before C3 (e.g. `ACTION_TYPE_BINDING_MISMATCH`), no ECC, C5 records expected vs supplied action type, agent cannot influence canonical action identity. This proves GAC binding cannot be bypassed by agent-authored identity fields.

## Alternatives Considered

- **Do nothing / rely on existing RBAC + per-action CROA governance**: Relies entirely on C2 to block inappropriate actions, exposing a wider theoretical attack surface prior to invariant checks.
- **Provider-native MCP tool allowlists only**: Fails to decouple semantic action classes from provider implementations and delegates governance authority to dynamic discovery.
- **GAC without session-specific narrowing**: Improves catalog management but leaves the full RBAC-authorized surface available to an agent for simple tasks that do not require it.
- **Session narrowing without GAC**: Relies on ad-hoc or dynamic schema generation without authoritative, governed definitions.
- **Redefining ECC**: Explicitly considered and rejected. This RFC maintains the core architectural integrity of CROA. It does not introduce Execution Warrants (EW), ECC migration, namespace reuse, higher-level ECC representations, or human ECC validation.

## Risks and Drawbacks

- **Stale catalog/tool churn**: Managing GAC versions against rapidly evolving MCP servers introduces overhead.
- **Over-narrowing and liveness/task-completion loss**: The agent may fail to complete tasks if the requested/admitted action surface is too restrictive.
- **Recomputation complexity**: Dynamically re-evaluating the Effective Action Set during a session adds overhead.
- **Provider/action mapping ambiguity**: Mapping disparate provider tools to canonical `gar.type` definitions may be ambiguous.
- **Schema canonicalization operational cost**: Hashing exact schemas requires strict normalization which can be brittle.
- **Additional C5 volume**: `ACTION_SURFACE_ESTABLISHED` events increase audit storage requirements.
- **False confidence**: Stakeholders might falsely believe that tool narrowing solves semantic information-flow governance (which remains E3).

## Open Questions

1. **Safe Inability to Continue**: A constrained agent must not be forced to improvise or gain authority merely because the current surface is insufficient. How can we cleanly map a "request clarification / escalate / task out of scope" outcome onto an already-specified CROA control/output path without inventing new exit actions in this RFC?
2. Under what exact conditions must an Effective Action Set be recomputed during a long-lived session?
3. How does this extension interact with Appendix L and delegated agents?
4. At what point does utility loss become unacceptable under aggressive narrowing?
5. Does action-surface narrowing materially reduce E3 friction without degrading useful task completion?

## Prior Art

- **MCP / tool permission surfaces**: Defining discrete, declarable capabilities for large language models.
- **Seccomp / pledge-style capability narrowing**: Systems where an application restricts its own syscall surface post-initialization.
- **Capability systems / least privilege**: Traditional principle of granting only the authority necessary for the task at hand.
- **Platform permission manifests**: Static declarations of required capabilities (e.g., mobile OS app permissions).

This RFC adapts these concepts carefully without claiming novelty, mapping them explicitly into CROA's admission lifecycle.
