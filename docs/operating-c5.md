# Operating C5: the audit store is tier-0 infrastructure

**Objective:** state plainly an operational consequence the logical architecture implies but doesn't
advertise: **fail-closed governance makes C5 (and the control path) a tier-0 availability dependency.**
This page names the coupling, the cost, and the mitigations so you can size it before you commit.
**Audience:** platform, SRE, and infrastructure architects.
**Authoritative source:** Part IV §18 (fail-closed / throughput) and Appendix R (C5 high-performance
evidence pattern) of the specification. Honest-limits page; the spec governs.

---

## The coupling nobody says out loud

CROA requires **fail-closed** behaviour: if the audit store or context grounding is unavailable, the
action does **not** proceed (Part IV §18.1). Combined with a **synchronous** C5 write on the permit
path, this has a direct consequence:

> If C5 is down, governed agents stop. C5's availability requirement therefore rises to **match the most
> critical system it governs.** If you put payment transfers behind CROA, C5 inherits the availability
> class of your payment switch.

This is not a flaw — it is the price of a *structural* guarantee (a "deny" you can't lose is worth more
than a log you might). But it means C5 is not "a log sink." It is an **append-only, hash-chained,
tamper-evident store with a broker-grade SLA**, and it must be planned, funded, and run as such. Neither
a generic logging stack nor an afterthought will do.

## What that means concretely

| Property | Requirement it inherits |
|---|---|
| **Availability** | Equal to the highest-criticality governed system (fail-closed couples them). HA/replication is mandatory, not optional. |
| **Latency** | On the synchronous permit path — every governed action waits on a C5 write. This is a per-action budget line (research question RQ-5). |
| **Durability & integrity** | Append-only + hash-chained + signed; a lost or reordered event breaks the evidence guarantee, not just a log. |
| **Throughput** | Must sustain peak governed-action rate. Coding/tool-calling agents emit hundreds–thousands of actions/hour each; C5 write throughput is a binding capacity constraint (RQ-6). |
| **Retention & cost** | Immutable growth. Storage sizing, compaction/segmentation, and long-term retention are real line items. |

## Mitigations the architecture already anticipates

You are not forced to put a slow database on the critical path. Appendix R specifies a
**high-performance evidence pattern** — the same shape as a write-ahead log in a database or a durable
broker:

- **Append to a durable, replicated WAL synchronously; materialize/index asynchronously.** The critical
  path is a sequential append + fsync to a replicated log, not a random-write to a query store.

- **Segment and seal.** Periodically seal chained segments; verification is per-segment and parallel.
- **Co-locate C5 with the boundary** so the synchronous hop is local, not a network round-trip to a
  distant service.

- **Scale by deployment model.** In DM-3 (sidecar) the write path fans out with agent count; a shared
  C5 becomes a durable-log tier (Kafka-class), not a single database.

With this pattern the synchronous cost is an append to a replicated log — well-understood infrastructure
with well-understood SLAs — rather than a synchronous query-database write.

## Degraded-mode: decide it deliberately

Fail-closed is the default and the safe choice. But you should choose your degraded-mode policy
**explicitly, per action class**, and write it down:

- **Fail-closed (default):** C5 unavailable → deny. Correct for irreversible / high-blast-radius actions
  (fund movement, data export, production change). This is the point of CROA; do not weaken it for these.

- **Graceful shedding (only for low-consequence classes):** you *may* route low-consequence, reversible
  action classes to a fallback durable buffer so they continue while the primary index is degraded —
  **but only if the buffer still guarantees append + chain integrity.** Never trade evidence integrity
  for availability; trade *materialization latency* instead.

The one thing you must not do is silently relax fail-closed under operational pressure — that is exactly
the governance-erosion loop the framework warns about, moved into the ops layer.

## Before you pilot: a C5 sizing checklist

- [ ] Peak governed-action rate for the pilot scope (actions/sec) → required C5 append throughput.
- [ ] Added per-action latency budget for the synchronous write, measured against your operational envelope (the expected action rate, latency budget, and fail-closed definition you set for the scope — Part IV).
- [ ] Availability target for C5 = availability target of the most critical governed system in scope.
- [ ] Replication / HA topology for the WAL tier; failover tested.
- [ ] Storage growth model + retention policy + segment-sealing/verification cost.
- [ ] Degraded-mode policy chosen **per action class**, documented, and reviewed.

If you can't meet the availability target for C5, narrow the pilot to a less critical action class until
you can — don't ship a fail-closed guarantee on top of a best-effort store.

→ Related: [deployment topologies](deployment-topologies.md) (where C5 sits per model),
[external prerequisites](prerequisites.md), and research questions **RQ-5** (latency), **RQ-6** (C5
sustainability), and **RQ-15** (availability coupling / degraded-mode viability).
