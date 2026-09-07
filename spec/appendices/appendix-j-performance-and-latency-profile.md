---
tags:
  - croa_foundation
---

# Appendix J — Performance and Latency Profile

**CROA Framework v1.0.1.1 · Informative.** Part of the CROA Framework; see [Framework structure](../framework-structure.md) for the full index.

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The 
## J.1 Why a performance profile is needed

Every governed action traverses a control path: admission (RBAC §4.9.1, AQL §4.9.2) → context grounding (`C3`) → invariant/trajectory state (`C4`) → evaluation (`C2.eval`) → on permit, compilation and signing (`C7`) → synchronous evidence write (`C5`, I6/I6.1) → execution-boundary validation (`C6`). A modern coding agent emits hundreds of actions per hour; a tool-calling agent thousands. If the added per-action latency or the throughput ceiling is unknown, two failure modes follow: (a) the deployment is under-provisioned and `C5` backpressure or `C2` saturation forces fail-deny under load (TH-11), and (b) operators feel governance "slows the agent down" and apply pressure to relax it (TH-2.C). Both are governance risks, so performance is in scope for the framework even though it is not a conformance criterion.

## J.2 The per-action latency budget

Treat the added governance latency as a sum of component contributions:

`L_action = L_admit + L_C3 + L_C4 + L_C2 + [L_C7 + L_C6]_permit + L_C5`

| Term | Dominant cost driver | Typical class | Notes |
|---|---|---|---|
| `L_admit` | RBAC predicate; AQL verdict lookup | E1 lookup | O(1); cache the current verdict + fingerprint |
| `L_C3` | Golden-record resolution (lookups) | E1/E2 | Cost set by golden-record store latency; cacheable (see §J.4) |
| `L_C4` | Trajectory projection + horizon check | E1–E3 | Pattern A/B: O(1); Pattern C: O(b^h) — see Appendix I |
| `L_C2` | Invariant evaluation per evaluability class | E1/E2/E3 | E3 conservative analyzers dominate; pin and budget them |
| `L_C7` | Canonical serialization + signature | crypto | One signature per permitted action |
| `L_C6` | ECC validity + invariant-set-version check | E1 lookup | O(1) registry membership |
| `L_C5` | Durable, signed append (I6.1 local commit) | I/O + crypto | Synchronous on the critical path; the usual bottleneck |

**Recommended budgeting practice.**
- Set an explicit **per-action governance latency target** (e.g., a p99 added-latency budget) per consequence class: high-consequence actions (R3–R4) can tolerate more governance latency than high-rate, low-consequence (R0–R1) actions. Tiering the budget by R-class mirrors the risk-proportionate method (Appendix K, CROA Core).
- Identify the **critical-path synchronous steps** — `C2`, `C7`, `C5` (local durable commit), `C6` — and keep only these on the action's blocking path. `C5` *replication* to the central store is asynchronous under I6.1 and MUST NOT be on the critical path.
- Budget the **E3 analyzers explicitly.** An E3 invariant (Part I §2.6) backed by a heavy static analyzer can dominate `L_C2`; give it its own sub-budget and a timeout that degrades to `AMBIGUOUS`→DENY rather than blocking unboundedly.

## J.3 Throughput and the `C2` / session guidance

The existing "≈ <50 concurrent sessions per `C2` instance" guidance is a *sizing heuristic*, not a limit; it presumes a mixed E1/E2 invariant set and bounded-cost `C4`. Throughput scales by:
- **Horizontal `C2`/`C3` replication** — `C2` and `C3` are stateless per action given the current policy and invariant-set-version, so they scale linearly (DM-3 distributes them to the agent edge; see Part IV §21).
- **`C4` is stateful and does not scale like `C2`/`C3`.** `C4` maintains per-session and cross-agent **trajectory state** (it is what makes cumulative constraints and NT-006 possible), so it is not embarrassingly parallel. Horizontally scaling `C4` requires a **shared or consistently-partitioned trajectory store**: all events contributing to one cumulative metric MUST be evaluated against one consistent state. Partitioning by session id is the common case; cross-agent/cross-session trajectory invariants require a shared low-latency state tier whose consistency — like the redemption authority of §4.8 — is on the governance-correctness path, not merely a cache. Its read/update latency and scaling cost are a distinct capacity line from `C2`/`C3` and MUST be sized separately.
- **`C5` write throughput** — the genuine shared bottleneck. Size `C5` (and the per-sidecar write-ahead journal under I6.1) for peak action rate × event size, with headroom for the buffering RTO. Backpressure handling is a TH-11 control (Part V §26): when `C5` cannot keep up, the system fails *deny*, never open.
- **AQL batteries** — qualification cost is amortized across the validity window; it is not on the per-action path except for the O(1) verdict/fingerprint check.

## J.4 Safe batching and caching

Caching and batching are permitted **only where they cannot widen reachability**. Safe patterns:

- **Cache policy artifacts and invariant-set snapshots** (already specified for the DM-3 sidecar, Part IV §21.3) with explicit validity windows; a stale or expired cache MUST fail-deny, never serve a stale permit (monotonicity: caches may only cause *more* denies, never more permits).
- **Cache `C3` golden-record lookups** within a session, keyed by the resolved entity version, provided cache invalidation is driven by golden-record version changes; a cache miss or version change re-resolves. Never cache across a golden-record version boundary.
- **Cache AQL verdicts** for the validity window keyed by the configuration fingerprint; any fingerprint change invalidates the cache (this is already required by §4.9.2).
- **Batch `C5` writes at the transport layer only.** Multiple events MAY be flushed to the central store in one transfer, but each event MUST be *durably committed locally first* (I6.1) and a transition MUST NOT proceed before its own event is committed. Batching MUST NOT defer the durability point past the transition.

**Unsafe (prohibited) optimizations:** evaluating a batch of actions under one `C2.eval` and applying the verdict to all; permitting an action before its evidence is durably committed; serving a cached *permit* after a policy/invariant-set version change; or skipping `C4` under load. Each of these widens reachability or breaks I6 and is non-conformant.

## J.5 Measurement protocol (for pilots)

So that pilot results are comparable, a pilot SHOULD report:

1. **Added per-action latency**, p50/p95/p99, broken down by the `L_*` terms in §J.2, separately for the permit and deny branches.
2. **Sustained and peak governed-action throughput** per `C2`/`C5` instance, and the action rate at which `C5` backpressure first induces fail-deny.
3. **`AMBIGUOUS`→DENY rate** overall and per E3 invariant (the governance-friction metric of Part III §7.2 Step 6), with the action types that dominate it.
4. **I6.1 reconciliation lag** distribution and the maximum observed buffering window versus the declared RTO.
5. **Configuration fingerprint** (model, prompt, tool set), invariant-registry version, horizon *h*, and C4 pattern mix (Appendix I) under which the figures were obtained — without these, the numbers are not interpretable.

These five series are the minimum needed to size a production deployment and to substantiate the TH-11 (availability) and performance claims a deployment makes. They are the natural companion to the conformance evidence of Part VI §29.

---

## J.6 Agent-sizing series (the §2.7.1 indicators B and C)

The utility–guarantee frontier (Part I §2.7) and the agent-sizing instrument (§2.7.1) require two quantities that are only observable at pilot, not derivable from the registry. This section specifies them as measurement series so that pilots report them comparably; like the rest of this appendix they are *informative* and carry no conformance obligation, but a deployment that adopts the §2.7.1 instrument SHOULD report them.

**Indicator B — governance-friction rate** (the "is the strain showing?" signal). This is the `AMBIGUOUS`→DENY series already in §J.5 item 3, read for the sizing decision rather than for availability: report it per `E3` invariant and in aggregate, against the per-invariant target declared in GitOps Definition (§7.2). A rate that persistently exceeds its target on `R3`/`R4` hazards is the measurable "too big" edge of §2.7 (Part V §26). To avoid asphyxiating business teams, deployments SHOULD establish friction alert thresholds or explicit "fallback circuits" (circuits de secours) that, when triggered by an abnormal `AMBIGUOUS` rate, alert the Governance Architect to refactor the invariant towards E1/E2 or narrow the action surface.

**Indicator C — utility retention vs. the ungoverned baseline** (the "is it still useful?" signal). This is the one series that requires a second, *ungoverned* run and is therefore the instrument most often missing today:

1. Fix a representative task suite for the action class and a configuration fingerprint (model, prompt, tool set) — the same fields as §J.5 item 5.
2. Run the suite twice in a sandbox: once **governed** by the full OCP, once with the **same model under no CROA overlay**.
3. Report **C = (governed value delivered) ÷ (ungoverned value delivered)**, net of governance friction, with the value measure stated (task success rate, accepted-output rate, or a domain metric) and the ungoverned-baseline value alongside it, so the **dominated** condition (C at or below 1.0 against the ungoverned baseline, §2.7) is visible.
4. Record the run cost: the ungoverned sandbox pass has a real expense and is itself a reason C is sampled periodically rather than continuously.

| Series | Symbol | Source | Stage | Reads as |
|---|---|---|---|---|
| Governance-friction rate | B | `C5` (`AMBIGUOUS`→DENY) | Pilot (Policy Deployment (§7.2)) + production | High/sustained on high-consequence hazards ⇒ too big |
| Utility retention | C | Sandbox: governed vs. ungoverned run | Pilot (Policy Deployment (§7.2)), sampled | ≤ ungoverned baseline ⇒ dominated / too small |

> *Note. The numeric examples for B in this corpus (e.g. the ≤10–15% targets in Appendix H §H.6) and the illustrative C ratios in Part I §2.7.1's worked example are **declared targets and illustrations, not measured results**. Supplying real B and C series from an independent pilot remains an open validation item (Part VI §29.5).*

> *First reproducible micro-benchmark. The published Minimal Reference Harness (Appendix G) now provides a dependency-free way to produce a first p50/p95/p99 series for the control-path terms of §J.2 (grounding → decision → compile → boundary check → synchronous C5 append) on a single machine. Such figures are **toy** — mock components, demonstration keys, no real Golden Record or network boundary — and MUST NOT be read as production numbers; but a reproducible harness micro-benchmark is a better starting point than none, and pilots are asked to report measured series against their own Operational Envelope (research question RQ-5). Independent measured datasets supersede any figure in this appendix.*

---

*End of Appendix J — Performance and Latency Profile.*
