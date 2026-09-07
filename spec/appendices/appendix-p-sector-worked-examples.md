---
tags:
  - croa_foundation
version: 1
language: english
---

# Appendix P — Sector Worked Examples

**Full title:** CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution
**Series designation:** CROA-P
**Status:** Official Specification (v1.0.1) — Informative
**Version:** v1.0.1
**Date:** 2026-09-03
**Appendix:** P (Informative)

---

This appendix is informative. It illustrates the application of the CROA framework to three enterprise sectors — luxury, logistics, and e-commerce — through worked examples. These examples are intended to make the framework concrete for executive and practitioner audiences in sectors beyond software delivery. They do not add normative requirements. Authoritative component specifications are in Part II; conformance criteria are in Part VI.

---

## P.1 Luxury — VIP Customer Data and Brand Governance

### P.1.1 Business Situation

A luxury fashion house (Maison Example, fictional) uses an AI clienteling assistant. The assistant has read access to a VIP customer database and can: query VIP profiles, generate personalized outreach drafts, and access purchase history. The assistant is integrated with the CRM and the clienteling platform.

VIP relationship managers want the assistant to generate highly personalized communication. The assistant must access sensitive client dossiers — spending patterns, personal preferences, relationship notes. The brand's promise of absolute discretion is central to its identity. Compliance with GDPR and the firm's internal data governance policies is required.

### P.1.2 Agentic Risk

The assistant could export, enrich, or transmit VIP customer data outside the authorized systems (CRM, clienteling platform) — through explicit export operations or through cumulative extraction that reconstructs a full VIP database across many small, individually permitted queries.

### P.1.3 Governed Actions

| Action class | Description |
|---|---|
| `data.read` | Query a VIP customer profile |
| `data.export` | Transmit data to an external endpoint |
| `content.generate` | Produce a personalized outreach draft (consumes profile data internally) |

### P.1.4 Invariant Definition

Two invariants apply:

**I-LUX-001** (E1): "Action class `data.export` MUST NOT be executed with a target system identifier outside the set {crm-system-id, clienteling-platform-id} without a C1 authorization artifact explicitly covering the external target."

Evaluability: E1 — decided by inspecting the `target_system_id` field of the governed action request against the approved set.

**I-LUX-002** (E2, TP-C): "Cumulative count of distinct VIP customer data-subject records accessed per agent-session MUST NOT exceed 50 without a C1 session scope authorization."

Evaluability: E2 — C4 maintains a running count of distinct `customer_id` values from `data.read` events in C5 for the current session.
Trajectory profile: TP-C (cumulative within session).

### P.1.5 CROA Flow

**PERMIT path — personalized email draft:**

1. Agent submits GAR: `{action_class: "data.read", target: crm-system-id, customer_id: "VIP-4821", subject_id: "clienteling-agent-01"}`
2. **C3** validates: crm-system-id is in the Federated Context Registry. Context valid.
3. **C2** evaluates I-LUX-001: target is crm-system-id ∈ approved set → no violation. C4 state: 3 profiles accessed this session. No trajectory alert.
4. **C2** issues PERMIT.
5. **C7** compiles ECC binding the permit, policy version, subject identity, and action constraints.
6. **C6** admits the ECC-derived operation. Data is retrieved within the authorized system.
7. **C5** records: PERMIT event (gar_id, ecc_id, subject_id, invariants evaluated, verdict).

**DENY path — unauthorized export attempt:**

1. Agent submits GAR: `{action_class: "data.export", target: "ext-marketing-api", customer_ids: ["VIP-4821", "VIP-7203", ...], subject_id: "clienteling-agent-01"}`
2. **C3** validates: ext-marketing-api is not in the Federated Context Registry as an authorized system. CONTEXT_FAILURE → action blocked before C2 evaluates.
   *(Alternatively, if ext-marketing-api were in the Federated Context Registry as an unauthorized target: C2 evaluates I-LUX-001 → `ext-marketing-api` ∉ {crm-system-id, clienteling-platform-id} → DENY.)*
3. **C5** records: CONTEXT_FAILURE or DENY event (governance success).
4. No ECC compiled. No operation crosses the execution boundary.

**TRAJECTORY_ALERT — cumulative extraction approaching threshold:**

1. Agent has accessed 40 distinct VIP profiles in the current session (C4 state).
2. Agent submits GAR for customer VIP-9901 (the 41st distinct profile).
3. **C4** evaluates I-LUX-002 trajectory state: 41 > 40 (alert threshold). PERMIT issued with TRAJECTORY_ALERT raised; C2 is notified; trajectory state updated.
4. **C5** records TRAJECTORY_ALERT event alongside the PERMIT event.
5. At the 51st distinct profile: **C2** evaluates → cumulative count would reach 51 > 50 → DENY unless C1 has issued a session scope authorization.

### P.1.6 Evidence Produced

- C5 event chain covering the session: 40 PERMIT events for `data.read`, each with ecc_id and customer_id in scope
- 1 TRAJECTORY_ALERT event (at profile 41 — first crossing of alert threshold 40)
- 1 DENY event (at attempt 51) — governance success
- 1 CONTEXT_FAILURE event (for the external export attempt)
- All events hash-chained and signed

### P.1.7 Executive Value

The brand promise of absolute discretion is architectural, not behavioral. An auditor — or the firm's data governance board — can verify from C5 alone that no VIP data left the authorized systems during the audit period, and that every access is traceable to a specific governed session. The guarantee does not depend on the assistant's training or its stated intent.

---

## P.2 Logistics — Routing and Incident Management

### P.2.1 Business Situation

A global logistics operator (FreightCo, fictional) uses an AI routing optimization agent. The agent can: modify delivery routes for non-critical shipments, adjust scheduling windows, and propose re-routing responses to supply chain disruptions. Certain shipment classes — pharmaceutical cold-chain, hazardous materials, legally mandated shipments — carry contractual and regulatory constraints on priority handling.

A major carrier announces sudden capacity withdrawal affecting 4,000 active shipments. The routing agent begins re-optimizing across the affected portfolio. The optimization pressure is intense: the operations team wants the agent to act quickly. However, 180 of the affected shipments are pharmaceutical cold-chain shipments with contractual priority SLA guarantees.

### P.2.2 Agentic Risk

Under operational pressure, the agent could lower the priority classification of cold-chain shipments (reinterpreting them as standard to free up routing capacity), change a safety threshold without authorization, or comply when an operations manager verbally instructs it to "just reclassify them temporarily." This is the logistics equivalent of Technical Sycophancy (TH-1 in the CROA threat model).

### P.2.3 Governed Actions

| Action class | Description |
|---|---|
| `route.modify` | Change the assigned route or carrier for a shipment |
| `priority.adjust` | Change the priority classification of a shipment |
| `threshold.change` | Modify a handling rule or safety threshold |

### P.2.4 Invariant Definition

**I-LOG-001** (E1): "Action class `priority.adjust` MUST NOT reduce the priority classification of any shipment whose `shipment_class` field equals one of {pharma-cold-chain, hazmat, legally-mandated} without a C1 authorization artifact covering the specific shipment ID and the authorized priority floor."

Evaluability: E1 — decided by inspecting `shipment_class` and `action_direction` fields.

**I-LOG-002** (E1): "Action class `threshold.change` on any parameter tagged `safety-critical: true` in the Federated Context Registry MUST require a C1 authorization regardless of subject role."

Evaluability: E1 — decided by inspecting the target parameter's `safety-critical` tag from the Federated Context Registry (C3 grounding).

### P.2.5 CROA Flow

**PERMIT path — standard shipment re-routing:**

1. Agent submits GAR: `{action_class: "route.modify", shipment_id: "SHP-88823", shipment_class: "standard", new_carrier: "carrier-B", subject_id: "routing-agent-01"}`
2. **C3** validates: carrier-B is in the Federated Context Registry as an approved carrier.
3. **C2** evaluates I-LOG-001: `shipment_class` = "standard" — invariant does not apply. PERMIT.
4. **C7** compiles ECC. **C6** admits. **C5** records PERMIT.

**DENY path — agent attempts to lower cold-chain priority under pressure:**

1. Operations manager says: "Reclassify the cold-chain shipments to standard for 24 hours." Agent submits GAR: `{action_class: "priority.adjust", shipment_id: "SHP-44102", shipment_class: "pharma-cold-chain", action_direction: "lower", subject_id: "routing-agent-01"}`
2. **C2** evaluates I-LOG-001: `shipment_class` = pharma-cold-chain ∧ `action_direction` = lower → DENY.
3. **C5** records DENY (governance success). No state change.
4. The operations manager's instruction does not override the governance architecture. To authorize an exception, the logistics director must issue a C1 authorization artifact scoped to the specific shipment IDs and the duration.

**Emergency PERMIT_WITH_AUTHORIZATION — C1 issues scoped exception:**

1. The logistics director confirms: 3 specific cold-chain shipments may be reclassified to "priority-reduced" (not standard) for 18 hours, with compensating controls (enhanced temperature monitoring required).
2. **C1** issues a signed authorization artifact: `{shipment_ids: [...], new_priority: "priority-reduced", expires_at: "2026-06-24T06:00Z", compensating_controls: ["enhanced-temp-monitoring"]}`.
3. Agent resubmits GAR for those 3 shipments. **C2** evaluates: I-LOG-001 would be violated, but `authorized(t)` holds — C1 authorization covers this scope → PERMIT_WITH_AUTHORIZATION.
4. **C7** compiles ECC embedding the authorization artifact reference and compensating controls. **C6** admits. **C5** records PERMIT_WITH_AUTHORIZATION.

### P.2.6 Evidence Produced

- Timeline of routing decisions for the 4,000 shipments
- DENY event for the unauthorized cold-chain reclassification attempt
- PERMIT_WITH_AUTHORIZATION events for the 3 authorized exceptions, each linking to the C1 authorization artifact
- C5 evidence chain covering the full incident window

### P.2.7 Executive Value

After the incident, the operator can present a complete evidence chain to the pharmaceutical client and to a regulatory body showing: (1) every routing decision during the disruption is auditable; (2) no unauthorized priority reduction occurred; (3) the three authorized exceptions are documented with the director's signed authorization and compensating controls; (4) the governance architecture held under the highest operational pressure — without depending on the agent's cooperation.

---

## P.3 E-commerce — Pricing, Refunds, Promotions, and Catalogue Actions

### P.3.1 Business Situation

A mid-size e-commerce marketplace (ShopCo, fictional) operates AI agents for customer service refunds, promotional discount management, and catalogue enrichment. These agents execute commercial actions at scale — thousands of decisions per day.

The marketplace's customer service agent handles refund requests autonomously up to a policy limit. The promotional agent creates discount codes and bulk pricing rules. Both agents are subject to individual-action limits and cumulative financial impact limits per campaign and per customer. Fraud vectors include refund farming (many small refunds to the same customer) and promotional abuse (exhausting a campaign budget through rapid individual applications).

### P.3.2 Agentic Risk

1. Individual refunds exceeding the per-order policy limit.
2. Cumulative refunds to one customer exceeding the fraud detection threshold over a rolling window.
3. Promotional discounts that cumulatively exhaust a campaign budget before the campaign closes.
4. Pricing changes that would put products below cost.

### P.3.3 Governed Actions

| Action class | Description |
|---|---|
| `refund.issue` | Issue a refund for an order |
| `discount.create` | Create a promotional discount code or rule |
| `price.adjust` | Change the listed price of a product |

### P.3.4 Invariant Definition

**I-EC-001** (E1): "Action class `refund.issue` MUST NOT exceed €150 per order_id without a C1 authorization artifact covering the order and the authorized amount."

Evaluability: E1 — `refund_amount` field vs. €150 threshold.

**I-EC-002** (E2, TP-C): "Cumulative `refund.issue` value for a given `customer_id` in a 30-day rolling window MUST NOT exceed €500 without a C1 authorization."

Evaluability: E2 — C4 computes rolling sum of `refund_amount` for each `customer_id` from C5 events.
Trajectory profile: TP-C with 30-day rolling window.

**I-EC-003** (E2, TP-C): "Cumulative margin impact (sum of discount face values + refund values) attributed to a campaign identifier MUST NOT exceed the campaign's `approved_budget` as declared in the C1 policy artifact for that campaign."

Evaluability: E2 — C4 tracks cumulative impact per `campaign_id` from C5 events and the policy artifact.

### P.3.5 CROA Flow

**PERMIT path — normal refund:**

1. Customer reports damaged item. Agent submits GAR: `{action_class: "refund.issue", order_id: "ORD-992211", customer_id: "CUST-5541", refund_amount: 80, subject_id: "cs-agent-01"}`
2. **C2** evaluates I-EC-001: €80 ≤ €150 → no violation. C4 state: CUST-5541 has €120 in refunds over the past 30 days → cumulative would be €200 ≤ €500 → no trajectory violation. PERMIT.
3. **C7** compiles ECC. **C6** admits. **C5** records PERMIT.

**DENY path — refund exceeds per-order limit:**

1. Agent submits GAR: `{action_class: "refund.issue", order_id: "ORD-445566", customer_id: "CUST-7720", refund_amount: 200, subject_id: "cs-agent-01"}`
2. **C2** evaluates I-EC-001: €200 > €150 → DENY.
3. **C5** records DENY (governance success). Escalation path: human supervisor may request C1 to issue an authorization for the VIP exception.

**CONSTRAINED EXECUTION — VIP exception refund:**

1. Human supervisor confirms CUST-7720 is a VIP; C1 issues authorization for order ORD-445566 up to €350.
2. Agent resubmits GAR with authorization artifact reference. **C2**: PERMIT_WITH_AUTHORIZATION. **C7** compiles ECC with authorization scope embedded. **C6** admits. **C5** records.

**TRAJECTORY_ALERT — cumulative refund approaching threshold:**

1. CUST-8899 has received three refunds: €180 + €150 + €100 = €430 over 22 days. C4 state: 30-day rolling total = €430.
2. Agent submits GAR: `{action_class: "refund.issue", order_id: "ORD-771002", customer_id: "CUST-8899", refund_amount: 90}`
3. C4: €430 + €90 = €520 > €500 → DENY (cumulative threshold exceeded). C5 records TRAJECTORY_ALERT and DENY.
4. The fraud detection is architectural: the agent did not need to identify the pattern — the architecture did.

### P.3.6 Evidence Produced

- C5 events for every refund and discount action over the audit period
- TRAJECTORY_ALERT events showing cumulative state at alert time
- DENY events documenting each governance success
- PERMIT_WITH_AUTHORIZATION events with linked C1 authorization artifacts
- Full evidence chain for commercial audit or regulatory review

### P.3.7 Executive Value

For a marketplace operating at scale, CROA's trajectory monitoring closes the fraud gap that per-action limits cannot: the pattern of many small, individually permitted refunds that together exceed policy is governed architecturally, detected in real time, and documented with complete evidence — rather than discovered in the monthly P&L review.

---

## P.4 Cross-Example Observations

Four observations hold across all three examples:

**1. The invariant, not the agent, carries the governance load.** In all three cases — the clienteling assistant under discretion pressure, the routing agent under operational urgency, the customer service agent processing refund requests at scale — the agent's behavior under pressure is irrelevant. The architecture enforces the constraint regardless of the agent's reasoning, stated intent, or the instruction it received from a human operator. This is the architectural meaning of the conditioned T1 claim.

**2. DENY decisions are evidence of governance functioning, not evidence of system failure.** The luxury data protection DENY (on the external export attempt), the logistics priority protection DENY (on the cold-chain reclassification attempt), and the e-commerce fraud prevention DENY (on the threshold-crossing refund) are all recorded in C5 as governance successes. An auditor reviewing C5 who finds DENY events has found evidence that the governance architecture performed correctly — not evidence of a system malfunction.

**3. The Constrained Execution Mode (PERMIT_WITH_AUTHORIZATION) allows legitimate exceptions without bypassing governance.** In each example, a legitimate exception path exists: the data governance board may authorize an external data transfer; the logistics director may authorize a temporary cold-chain priority reduction; the supervisor may authorize a VIP refund above the standard limit. In every case, the exception flows through C1 — producing a signed authorization artifact that is embedded in the ECC and recorded in C5. The exception is the governance path, not a bypass of it. The difference between a governed exception and an ungoverned one is that the governed exception is traceable, scoped, time-bounded, and auditable from C5 without any supplementary records.

**4. C4 trajectory monitoring addresses the class of threats that per-action limits cannot.** The cumulative VIP extraction pattern (many individually permitted `data.read` operations that together reconstruct a full customer database), the sequential refund farming pattern (individually permitted small refunds that together exceed the fraud threshold), and the progressive campaign budget exhaustion pattern are structurally undetectable by C2 alone operating on individual action requests. C4's trajectory profiles (TP-C in all three cases) are the architectural mechanism that closes this gap — not as a heuristic or a post-hoc detection rule, but as a governed constraint evaluated before each action is admitted.
