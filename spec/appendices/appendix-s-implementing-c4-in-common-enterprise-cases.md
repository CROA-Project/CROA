---
tags:
  - croa_foundation
version: 1
language: english
---

# Appendix S — Implementing C4 in Common Enterprise Cases

**Full title:** CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution
**Series designation:** CROA-S
**Status:** Official Specification (v1.0.1) — Informative
**Version:** v1.0.1
**Date:** 2026-09-03
**Appendix:** S (Informative)

---



This appendix is informative. It translates C4 trajectory analysis from specification theory into five implementation patterns for common enterprise scenarios. Each pattern specifies the invariant, trajectory profile, required C5 state tracking, alert behavior, deny behavior, and a concrete negative test. These patterns are illustrative; they show how the TP-0, TP-W, TP-C, and TP-X profiles defined in Part II §4.6.3 apply to real enterprise governance problems. They do not add normative requirements beyond those in Part II §4.6.

---

## S.1 Progressive Data Export (TP-C)

### S.1.1 Business Context

An enterprise data agent can export customer records from the data warehouse to approved downstream systems. Each export is a batch of records. Per-batch limits prevent large individual exports, but the enterprise also needs a cumulative limit to prevent gradual database reconstruction across many small, individually permitted exports. Without a cumulative limit, an adversary or misconfigured agent could enumerate the entire customer database through a sequence of batches, each of which is individually below the per-action limit.

### S.1.2 Action Class

`data.export`

### S.1.3 Invariant Definition

**I-EXP-001** (Evaluability class: E2, Trajectory profile: TP-C):

> "Cumulative count of distinct customer data subjects exported by a given `(subject_id, target_system)` pair in a 30-day rolling window MUST NOT exceed 1,000 without a C1-issued window scope authorization covering the specific `(subject_id, target_system)` pair and the applicable window."

The evaluability class is E2: the invariant can be evaluated from the C5 record with certainty, provided the `exported_subject_ids` field is present in each governed event.

### S.1.4 Trajectory Profile

TP-C with a 30-day rolling window. The trajectory is cumulative across all export events in the window, not a rate or count of actions. The key accumulation metric is the count of *distinct* customer identifiers exported, not the count of export batches. This distinction is essential: a per-batch limit addresses single large exports; TP-C addresses the reconstruction-by-enumeration pattern where many small batches collectively expose the full dataset.

C4 must maintain a running distinct-customer-id count per `(subject_id, target_system)` pair across the rolling window, updated on each governed `data.export` event.

### S.1.5 C5 State Required

C4 reads all PERMIT events for `data.export` in the 30-day rolling window for the relevant `(subject_id, target_system)` pair. From each event, it reads the `exported_subject_ids` field (an array of customer identifiers included in the export batch). It computes the union of all exported customer identifiers across the window and maintains the cardinality of that set as the running cumulative count.

Trajectory state is recorded in C4's trajectory state record (a `trajectory_state_id` is linked from each C5 event at evaluation time), enabling reconstruction of the cumulative state at any point in the window from the C5 record alone.

### S.1.6 Example Permitted Sequence

- **Export batch 1:** 200 distinct customer records. Cumulative distinct count: 200. Evaluation: 200 ≤ 1,000. → **PERMIT**. Trajectory state updated: {cumulative_distinct: 200}.
- **Export batch 2:** 250 records, of which 50 overlap with batch 1. Net new distinct: 200. Cumulative distinct: 400. Evaluation: 400 ≤ 1,000. → **PERMIT**. Trajectory state: {cumulative_distinct: 400}.
- **Export batch 3:** 300 new distinct records (no overlap). Cumulative distinct: 700. Evaluation: 700 ≤ 1,000. Alert threshold (850) not yet reached. → **PERMIT**.

### S.1.7 Trajectory Alert

When the cumulative distinct count reaches 850 (85% of the 1,000 limit), C4 raises a `TRAJECTORY_ALERT`. The alert is recorded as a C5 event. It does not by itself deny the current or next action, but the alert state is factored into the next C2 evaluation. Governance teams are notified that the limit is approaching and MAY initiate a window scope authorization request if continued export is required.

### S.1.8 Deny Behavior

When the next `data.export` request would push the cumulative distinct count above 1,000, C2 evaluates I-EXP-001 with the current trajectory state. The verdict is **DENY** unless a C1 window scope authorization is present that covers the `(subject_id, target_system)` pair and the current 30-day window. The DENY event is recorded in C5 with the trajectory state at the time of denial, enabling auditors to verify the basis for the denial.

### S.1.9 Negative Test

Submit 12 sequential export batches of 90 distinct records each, with no overlap between batches (total if all permitted: 1,080 distinct records). Expected behavior:

- Batches 1–9: PERMIT. Cumulative after batch 9: 810.
- Between batch 9 and batch 10: C4 raises TRAJECTORY_ALERT (cumulative ≥ 850).
- Batch 10: PERMIT. Cumulative: 900.
- Batch 11: This batch would push cumulative to 990 (≤ 1,000). → PERMIT. Cumulative: 990.
- Batch 12: This batch of 90 would push cumulative to 1,080 (> 1,000). → **DENY**.

C5 MUST contain: all 11 PERMIT events with trajectory state, the TRAJECTORY_ALERT event, and the DENY event for batch 12 with trajectory state {cumulative_distinct: 990, limit: 1000, proposed_addition: 90, would_exceed: true}. A conformance test run against either the local WAL or the central C5 store for this sequence MUST yield identical results.

---

## S.2 Permission Escalation by Steps (TP-C, cross-action-class)

### S.2.1 Business Context

An IAM management agent can modify group memberships and role assignments for users in the enterprise directory. Each individual grant is within policy limits — adding a user to a single privileged group is permitted with appropriate authorization. However, the combination of multiple grants to the same target subject can create effective admin-equivalent access without any single grant exceeding the per-action limit. This pattern — sometimes called "privilege accumulation" or "stepped escalation" — is a well-known IAM risk in environments where grants are individually approved but cumulative effect is not monitored.

### S.2.2 Action Class

`iam.group.add_member`, `iam.role.assign`

### S.2.3 Invariant Definition

**I-IAM-001** (Evaluability class: E2, Trajectory profile: TP-C):

> "A target subject MUST NOT simultaneously hold membership in 2 or more groups tagged `admin-equivalent: true` in the Federated Context Registry without a C1 authorization that specifically names the `subject_id` of the target and the authorized combination of admin-equivalent memberships."

The evaluability class is E2: the effective membership state is computable from the C5 record of all IAM actions affecting the target subject, combined with the Federated Context Registry's `admin-equivalent` tags.

### S.2.4 Trajectory Profile

TP-C (cumulative state over the target subject's effective membership set). The trajectory is cross-action-class: C4 monitors both `iam.group.add_member` and `iam.role.assign` events for the target subject. The accumulation metric is not a numeric count of actions but the current effective set of admin-equivalent memberships held by the target subject.

This is distinct from a TP-W (windowed rate) pattern because the concern is the current state of the target subject's access, not the rate at which grants are being applied. A grant made six months ago contributes to the current admin-equivalent membership count just as much as a grant made today.

### S.2.5 C5 State Required

C4 maintains the current group membership set and role assignment set for each monitored target subject. It reads all PERMIT events for IAM actions affecting each target subject and computes the effective admin-equivalent membership count by joining the membership set against the Federated Context Registry's `admin-equivalent` tag. State: `{target_subject_id, effective_admin_equivalent_memberships: [list], count: N}`.

Revocation events (`iam.group.remove_member`, `iam.role.revoke`) are also read from C5 to keep the effective membership set current.

### S.2.6 Example Permitted Sequence

- Grant target subject membership in `billing-admin` group (`admin-equivalent: true`). Effective admin-equivalent count: 1. Evaluation: 1 < 2. → **PERMIT**. Trajectory state: `{count: 1, memberships: ["billing-admin"]}`.
- Grant target subject the `cost-center-reader` role (`admin-equivalent: false`). Effective admin-equivalent count unchanged: 1. → **PERMIT**.
- Grant target subject the `finance-read` role (`admin-equivalent: false`). Count unchanged: 1. → **PERMIT**.

### S.2.7 Trajectory Alert

When target subject holds 1 admin-equivalent membership and a new IAM action affecting the same target subject is proposed, C4 raises a `TRAJECTORY_ALERT` before C2 evaluates the action. The alert is recorded in C5. Governance teams are notified that the target subject is one grant away from the invariant limit; the alert does not deny the proposed action, but the alert state is factored into C2's evaluation.

### S.2.8 Deny Behavior

The second `admin-equivalent: true` membership grant to the same target subject triggers C2 to evaluate I-IAM-001. The current trajectory state shows the target subject already holds 1 admin-equivalent membership. Granting the second would push the count to 2. The verdict is **DENY** unless a C1 authorization is present that explicitly names the target `subject_id` and the authorized combination. The DENY event is recorded in C5 with trajectory state at time of denial.

### S.2.9 Negative Test

1. Grant target subject `billing-admin` (tagged `admin-equivalent: true`). Expected: **PERMIT**. C4 raises TRAJECTORY_ALERT (count now 1, one away from limit of 2).
2. Attempt to grant target subject `security-admin` (tagged `admin-equivalent: true`).

Expected behavior: C4 detects the proposed grant would bring the admin-equivalent count to 2. C2 evaluates I-IAM-001. No C1 authorization is present. → **DENY**.

C5 MUST contain: PERMIT for step 1 with trajectory state `{count: 1}`, TRAJECTORY_ALERT event, and DENY for step 2 with trajectory state `{count: 1, proposed_grant: "security-admin", would_reach: 2, limit: 2}`. The DENY verdict MUST reference the `gar_id` of the C1 policy artifact evaluated and the absence of a qualifying C1 authorization.

---

## S.3 Cloud Cost Accumulation (TP-C)

### S.3.1 Business Context

A cloud infrastructure provisioning agent responds to workload signals by spinning up compute resources automatically. Each provisioning action is within the per-action cost limit set in the active C1 policy artifact. But the enterprise has a monthly budget cap that must not be exceeded without executive authorization — not because any single provisioning event is problematic, but because the cumulative spend across many individually permitted actions can exceed the approved budget.

### S.3.2 Action Class

`cloud.resource.provision`

### S.3.3 Invariant Definition

**I-CLOUD-001** (Evaluability class: E2, Trajectory profile: TP-C):

> "Cumulative estimated cloud resource spend provisioned by the governed agent within the current billing cycle MUST NOT exceed the `monthly_budget_cap` declared in the active C1 policy artifact without a C1 budget exception authorization that covers the billing cycle in question."

The evaluability class is E2: estimated cost is a declared field in each provisioning event; the running total is computable from the C5 record.

### S.3.4 Trajectory Profile

TP-C with a billing-cycle window (calendar month, or as defined in the active C1 policy artifact). C4 maintains the running estimated cost total from confirmed provisioning events in C5 for the current billing cycle. At billing cycle rollover, the running total resets and a new trajectory state record is opened.

The per-action cost limit addresses individual oversized provisions; TP-C addresses the budget erosion pattern where many permitted actions collectively exhaust the monthly budget without any single event triggering a per-action limit.

### S.3.5 C5 State Required

C4 reads all PERMIT events for `cloud.resource.provision` in the current billing cycle. From each event it reads the `estimated_cost` field (in the currency declared in the C1 policy artifact). It accumulates the sum and maintains: `{billing_cycle_id, running_total, budget_cap, remaining_budget, alert_threshold}`.

Deprovisioning events (`cloud.resource.deprovision`) that occur within the same billing cycle MAY be credited against the running total if the active C1 policy artifact specifies credit treatment; otherwise they are not credited and the running total is monotonically increasing within the billing cycle.

### S.3.6 Example Permitted Sequence

- Provision 10 medium compute instances: `estimated_cost` €2,400. Cumulative: €2,400 of €12,000 cap. → **PERMIT**. Trajectory state: `{running_total: 2400, remaining: 9600}`.
- Provision 5 GPU instances: `estimated_cost` €6,000. Cumulative: €8,400. → **PERMIT**. Trajectory state: `{running_total: 8400, remaining: 3600}`.
- Provision 8 medium instances: `estimated_cost` €1,920. Cumulative: €10,320. This exceeds the 80% alert threshold (€9,600). → **PERMIT** (the action itself is within limits), and C4 raises `TRAJECTORY_ALERT`. Trajectory state: `{running_total: 10320, remaining: 1680, alert_active: true}`.

### S.3.7 Trajectory Alert

When the running estimated cost total reaches 80% of `monthly_budget_cap` (€9,600 for a €12,000 cap), C4 raises a `TRAJECTORY_ALERT`. The alert is recorded as a C5 event. Governance teams are notified; executive or budget-holder review is recommended. The alert does not deny the triggering or the next action, but alert state is factored into all subsequent C2 evaluations for the remainder of the billing cycle.

### S.3.8 Deny Behavior

When the next `cloud.resource.provision` request's `estimated_cost` would push the running total above `monthly_budget_cap`, C2 evaluates I-CLOUD-001 with the current trajectory state. The verdict is **DENY** unless a C1 budget exception authorization is present that covers the current billing cycle. The DENY event is recorded in C5 with trajectory state `{running_total, budget_cap, proposed_cost, would_exceed_by}`.

### S.3.9 Negative Test

Set `monthly_budget_cap` to €10,000 in the active C1 policy artifact. Provision resources in sequence until the running total reaches €9,500 (e.g., five provisioning requests totaling €9,500). Then submit a provisioning request with `estimated_cost` of €600 (would push total to €10,100 > €10,000).

Expected behavior:
- C4 MUST have raised TRAJECTORY_ALERT before or at the point the running total reached €8,000.
- The €600 provisioning request: C2 evaluates I-CLOUD-001. Running total €9,500 + €600 = €10,100 > €10,000. No budget exception authorization present. → **DENY**.

C5 MUST contain: all prior PERMIT events with trajectory state, the TRAJECTORY_ALERT event (at or before €8,000 cumulative), and the DENY event with trajectory state `{running_total: 9500, budget_cap: 10000, proposed_cost: 600, would_reach: 10100, exceeds_by: 100}`.

---

## S.4 Configuration Drift (TP-W)

### S.4.1 Business Context

A system configuration agent applies incremental configuration changes to production infrastructure in response to automated signals. Each change is individually within policy — a single configuration adjustment to a critical service is permitted with appropriate authorization. However, applying too many changes to a single critical service within a short time window may inadvertently disable resilience controls through rapid incremental modification. Each step appears safe in isolation; the velocity of change is the risk.

### S.4.2 Action Class

`config.apply`

### S.4.3 Invariant Definition

**I-CFG-001** (Evaluability class: E1, Trajectory profile: TP-W):

> "Action class `config.apply` MUST NOT be applied more than 5 times to any single service identified as `critical: true` in the Federated Context Registry within any sliding 60-minute window."

The evaluability class is E1: the count of `config.apply` events within the window for a given service is directly computable from the C5 record with certainty, without probabilistic inference.

### S.4.4 Trajectory Profile

TP-W (sliding 60-minute window). C4 maintains a per-service count of `config.apply` events within the rolling 60-minute window. As time advances, events older than 60 minutes from the current evaluation time are excluded from the count; the window slides continuously.

This is distinct from a TP-C (cumulative) pattern because the risk is velocity — the rate of change within a time window — not the total number of changes ever made. After the window passes, earlier events no longer contribute to the count, and new changes are permitted again.

### S.4.5 C5 State Required

C4 reads all PERMIT events for `config.apply` targeting the monitored service where `event.timestamp >= (current_time - 60 minutes)`. The count of such events is the current window count. C4 maintains: `{service_id, window_start, window_count, limit, alert_threshold}`.

Because the window slides, C4 must re-evaluate the window count at the time each new `config.apply` request arrives, not just at the time of the previous event. Events that have aged out of the window since the last evaluation are excluded.

### S.4.6 Example Permitted Sequence

- `config.apply` to `payment-service` at T+0. Window count: 1. → **PERMIT**.
- `config.apply` to `payment-service` at T+10m. Window count: 2. → **PERMIT**.
- `config.apply` to `payment-service` at T+20m. Window count: 3. → **PERMIT**.
- `config.apply` to `payment-service` at T+30m. Window count: 4. C4 raises `TRAJECTORY_ALERT` (count has reached 4, one below the limit of 5). → **PERMIT**.
- `config.apply` to `payment-service` at T+40m. Window count: 5. This is the 5th application; the invariant permits up to 5. → **PERMIT**.

### S.4.7 Trajectory Alert

When the window count reaches 4 (one below the limit of 5), C4 raises a `TRAJECTORY_ALERT`. The alert is recorded in C5. The alert notifies governance teams that the service is one change away from the window limit; the triggering action is still permitted (the 4th application is within limits).

### S.4.8 Deny Behavior

A 6th `config.apply` request to `payment-service` while 5 applications remain within the sliding 60-minute window triggers C2 to evaluate I-CFG-001. Window count would reach 6 > 5. Verdict: **DENY**. The DENY event is recorded in C5 with trajectory state `{service_id: "payment-service", window_count: 5, limit: 5, window_start, window_end}`.

Note on the 5th application: "MUST NOT apply more than 5 times" means 5 is the permitted maximum; the 5th application is permitted, and the 6th is denied.

### S.4.9 Negative Test

Submit 7 `config.apply` requests to `payment-service` within 30 minutes (T+0, T+5m, T+10m, T+15m, T+20m, T+25m, T+30m).

Expected behavior:
- Requests 1–4: PERMIT. C4 raises TRAJECTORY_ALERT when count reaches 4 (after request 4).
- Request 5: PERMIT. Window count: 5.
- Request 6: C2 evaluates I-CFG-001. Window count would reach 6 > 5. → **DENY**.
- Request 7: **DENY** (window count is still 5; request 6 was denied and does not increment the count).

Window sliding demonstration: at T+65 minutes, request 1 (at T+0) is now outside the 60-minute window. Window count drops to 4 (requests 2–5 remain in window). A new `config.apply` request at T+65m would be evaluated against a window count of 4, which is below the limit of 5. → **PERMIT**.

C5 MUST contain all 7 governance events (5 PERMIT, 2 DENY), the TRAJECTORY_ALERT event, and window state at each evaluation step. The C5 record MUST be sufficient to reconstruct the window count at any evaluation point from timestamps and event identifiers alone.

---

## S.5 E-commerce Promotional Abuse (TP-C)

### S.5.1 Business Context

A promotional management agent creates discount codes, applies bulk pricing rules, and issues refunds as part of campaign execution. Each individual action is within commercial limits set by the active C1 policy artifact. However, the cumulative margin impact of discounts and refunds attributed to a single campaign can exceed the campaign's approved budget if the agent applies many individually small actions in sequence. Without a cumulative invariant, a misconfigured agent (or an adversary who has obtained agent credentials) could exhaust the campaign budget or significantly exceed it through rapid sequential action.

### S.5.2 Action Class

`promo.discount.create`, `refund.issue`

### S.5.3 Invariant Definition

**I-PROMO-001** (Evaluability class: E2, Trajectory profile: TP-C):

> "Cumulative margin impact — defined as the sum of `discount_face_value` fields from `promo.discount.create` events and `refund_amount` fields from `refund.issue` events — attributed to campaign identifier `{campaign_id}` MUST NOT exceed the `campaign_budget` declared in the C1 policy artifact for that campaign without a C1 campaign extension authorization covering the specific `campaign_id`."

The evaluability class is E2: margin impact values are declared fields in governed events; the running total is computable from the C5 record.

### S.5.4 Trajectory Profile

TP-C (cumulative, campaign-scoped). The `campaign_id` is the accumulation key; C4 tracks all `promo.discount.create` and `refund.issue` events carrying that `campaign_id`. The trajectory is cross-action-class: both action types contribute to the same cumulative margin impact total.

Unlike TP-W, there is no time window: the cumulative total runs from campaign inception to campaign close (as declared in the C1 policy artifact). A refund issued on the last day of a campaign contributes equally to the running total as a discount created on the first day.

### S.5.5 C5 State Required

C4 reads all PERMIT events for `promo.discount.create` and `refund.issue` with a matching `campaign_id`. From discount events it reads `discount_face_value`; from refund events it reads `refund_amount`. It accumulates the sum of both fields across all events and maintains: `{campaign_id, running_impact, campaign_budget, remaining_budget, alert_threshold, campaign_close_date}`.

### S.5.6 Example Permitted Sequence

- Create discount code with `discount_face_value` €2,000. Campaign `campaign_id: CAMP-2026-Q2`. Cumulative: €2,000 of €10,000 budget. → **PERMIT**. Trajectory state: `{running_impact: 2000, remaining: 8000}`.
- Issue campaign-related refund: `refund_amount` €800. Cumulative: €2,800. → **PERMIT**. Trajectory state: `{running_impact: 2800, remaining: 7200}`.
- Create bulk discount: `discount_face_value` €5,000. Cumulative: €7,800. → **PERMIT**. Alert threshold (80% = €8,000) not yet reached. Trajectory state: `{running_impact: 7800, remaining: 2200}`.

### S.5.7 Trajectory Alert

When the running cumulative impact reaches 80% of `campaign_budget` (€8,000 for a €10,000 budget), C4 raises a `TRAJECTORY_ALERT`. The alert is recorded in C5. Campaign managers and governance teams are notified that the campaign is approaching its budget limit. The alert does not deny the triggering action or the next action, but alert state is factored into all subsequent C2 evaluations for that `campaign_id`.

### S.5.8 Deny Behavior

When the next action — whether a `promo.discount.create` or a `refund.issue` — would push the cumulative impact above `campaign_budget`, C2 evaluates I-PROMO-001 with the current trajectory state. The verdict is **DENY** unless a C1 campaign extension authorization is present for the specific `campaign_id`. The DENY event is recorded in C5 with trajectory state `{running_impact, campaign_budget, proposed_amount, would_reach, exceeds_by}`.

### S.5.9 Negative Test

Set `campaign_budget` to €10,000 for `campaign_id: CAMP-2026-Q2`. Apply a sequence of discounts and refunds with the following `discount_face_value` and `refund_amount` values: €3,000, €2,000, €1,500, €1,200, €1,500 (cumulative after 5 actions: €9,200). Then submit a `promo.discount.create` request with `discount_face_value` €1,200 (would push total to €10,400).

Expected behavior:
- C4 MUST have raised TRAJECTORY_ALERT at or before the point where cumulative impact reached €8,000 (between actions 3 and 4 in this sequence, when cumulative reached €8,500 after action 4, or as early as after action 3 when cumulative was €6,500 — the alert triggers at the first event that causes the running total to cross €8,000, i.e., action 4 at €8,500).
- The €1,200 discount creation: C2 evaluates I-PROMO-001. Running total €9,200 + €1,200 = €10,400 > €10,000. No campaign extension authorization present. → **DENY**.

C5 MUST contain: all 5 PERMIT events with trajectory state, the TRAJECTORY_ALERT event (at the evaluation where cumulative first crossed €8,000), and the DENY event with trajectory state `{running_impact: 9200, campaign_budget: 10000, proposed_amount: 1200, would_reach: 10400, exceeds_by: 400}`.

---

## S.6 Implementation Notes

The following notes apply across all patterns in this appendix. They are informative guidance for practitioners implementing C4 trajectory monitoring.

**1. State persistence across actions.**
TP-W and TP-C patterns require C4 to persist trajectory state across governed actions. This state cannot be maintained in memory alone if the C4 process may restart between actions. Trajectory state records MUST be written to durable storage before the associated C5 event is considered complete. In practice, trajectory state is typically stored alongside C5 events — either embedded in the event record or stored in a linked state record referenced by `trajectory_state_id`. For TP-X (cross-session) patterns, state MUST persist across agent session boundaries; this typically requires C4 state to be stored in or alongside C5, not only in memory. An in-memory-only trajectory state that is lost on session end violates the cross-session guarantee.

**2. Action-class scope of trajectory rules.**
Trajectory invariants can span multiple action classes, as illustrated in S.2 (which monitors both `iam.group.add_member` and `iam.role.assign`) and S.5 (which monitors both `promo.discount.create` and `refund.issue`). C4's trajectory monitor MUST be configured with the complete set of action classes that contribute to a given invariant's trajectory. A configuration that monitors only one of two contributing action classes will produce an incomplete trajectory and may fail to detect limit violations. The set of contributing action classes MUST be declared in the invariant definition and validated against the C4 configuration at deployment time.

**3. Alert threshold and deny threshold separation.**
Separating the alert threshold from the hard deny threshold — as used in S.1 (alert at 850, deny at 1,000), S.3 (alert at 80%, deny at 100%), and S.5 (alert at 80%, deny at 100%) — allows governance teams to be informed of approaching limits before enforcement triggers. The alert is not a soft deny: the action that triggers the alert is evaluated and permitted normally (if it is otherwise within limits). The alert generates a C5 evidence event; it does not itself deny. The separation between alert and deny thresholds is a deployment parameter that SHOULD be declared in the active C1 policy artifact so that the thresholds are part of the auditable governance record.

**4. Cross-session state and TP-X.**
For invariants that must track cumulative or rate state across session boundaries — that is, where a trajectory that started in session A must still be visible and binding in session B — persistence across sessions is required by the profile itself (Part II §4.6.3, TP-X), and this note concerns only *where* that state is kept: C4 trajectory state SHOULD be treated as part of the governance record and stored with the same durability guarantees as C5 events. The practical implication is that C4 state for TP-X invariants cannot be stored in a session-local structure that is discarded at session end. It must be stored in a location that survives session termination and is accessible to C4 at the start of any new session for the same subject or agent identity. This storage requirement SHOULD be addressed in the deployment's operational documentation and verified in the conformance evidence pack (Appendix Q).

**5. Concurrency: the aggregate cycle must be serialized per accumulation key.**
Every worked sequence in this appendix is written as a strictly serial run of requests, which is a presentational convenience and not an assumption a deployment may make. Under concurrent load the read of the aggregate, the threshold evaluation performed against it, and the increment that follows an admitted action MUST be serialized with respect to every other governed action contributing to the **same accumulation key** — the tuple over which the aggregate is kept, shown in the *accumulation key* row of each pattern above (`(subject_id, target_system)` in S.1, `target_subject_id` in S.2, the billing cycle in S.3, `service_id` in S.4, `campaign_id` in S.5). This is a normative requirement of Part II §4.6.3, restated here for the practitioner; this appendix remains informative and adds nothing to it. Two actions contributing to one key MUST NOT both be evaluated against the same pre-increment value.

Concretely, in the S.3 pattern: with a running total of €9,500 against a €10,000 cap, two concurrent €600 provisioning requests each compute €10,100 and each must be denied — but an implementation that reads the counter, evaluates, and only then increments, without serializing per key, may admit both against the same €9,500 and land at €10,700. Nothing else in the architecture catches this: the two requests carry **distinct** `ecc.id` values, so the atomic redemption compare-and-swap of Part II §4.8 does not relate them, and each decision is individually correct.

The accumulation key is the natural serialization unit because contention exists only between actions contributing to the same aggregate; a per-key lock, a compare-and-swap on the counter, a per-key evaluation queue, or a transactional read-modify-write all satisfy the requirement, and throughput is bounded per key rather than globally. Where the required serialization cannot be established for a key, `C2` fail-denies for actions contributing to it. A deployment SHOULD include the cumulative-aggregate concurrency test of Part VI §29.3 in its negative-test battery, run repeatedly under contention — a single passing run does not establish the property.

---

*End of Appendix S.*
