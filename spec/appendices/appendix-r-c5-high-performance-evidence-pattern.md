---
tags:
  - croa_foundation
version: 1
language: english
---

# Appendix R — C5 High-Performance Evidence Pattern

**Full title:** CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution
**Series designation:** CROA-R
**Status:** Official Specification (v1.0.1) — Informative
**Version:** v1.0.1
**Date:** 2026-09-03
**Appendix:** R (Informative)

---



This appendix is informative. It specifies a recommended implementation pattern for satisfying the C5 completeness requirement in high-frequency agentic workflows without sacrificing throughput. It does not relax any normative requirement. Authoritative C5 specifications are in Part II §4.7; conformance criteria are in Part VI, criterion 8.

---

## R.1 Purpose and Context

The C5 completeness requirement (Part II §4.7, Part VI conformance criterion 8) requires that every governed action produce a C5 event before the next governed action is admitted. In high-frequency agentic workflows — where an agent may submit dozens of governed actions per second — a naive implementation might interpret this as requiring round-trip latency to a central evidence store before each action proceeds. This appendix specifies an implementation pattern that preserves the non-repudiation and completeness requirements of C5 while remaining compatible with high-throughput deployment contexts.

The core insight: the CROA specification requires that evidence is committed before the next action proceeds. It does not require that the committed evidence has replicated to a central store. Local durability is the synchronous gate; central availability is the asynchronous consequence.

This pattern is informative. An implementation may satisfy C5 completeness by other means, provided it can demonstrate that every governed action produced a durable, tamper-evident, verifiable event record before the subsequent governed action was admitted.

---

## R.2 Terminology

The following terms are used in this appendix. They are not redefined here as normative terms; they describe components of the implementation pattern.

**Local WAL (Write-Ahead Log):** An append-only, durable log maintained on the same host or execution environment as the governed agent. The local WAL records C5 events synchronously before each subsequent action is admitted. It is the primary synchronous gate in the pattern described here.

**Central C5 Store:** The shared, organization-wide evidence repository to which local WAL events are replicated asynchronously. The central C5 store provides the consolidated, auditable record accessible to auditors, compliance functions, and the C4 trajectory monitor across sessions and agents.

**Synchronous Gate:** The checkpoint that must be passed before the next governed action is admitted. In this pattern, the synchronous gate is the successful durable write to the local WAL (step 5 in R.3). No subsequent action proceeds until the gate is passed.

**Replication Lag:** The elapsed time between the durable local WAL write (step 5) and the central C5 store acknowledgment (step 8). Replication lag is expected and permissible. It must be documented as a governed operational parameter per R.4, invariant 5.

**Chain Continuity:** The property that every event in the local WAL (and by extension in the central C5 store after replication) contains a `chain_hash` field that equals the cryptographic hash of the immediately prior event record. Chain continuity allows auditors to detect any gap, reordering, or insertion in the evidence record.

**Fail-Deny:** The mandatory response when the local WAL write fails. If the synchronous gate cannot be passed — because the durable write did not succeed — the next governed action MUST be denied. The governed action that would have been admitted is blocked, and an operational alert MUST be raised.

---

## R.3 The Permitted Pattern

The following nine-step sequence describes the permitted C5 evidence pattern for high-throughput deployments. Steps 1–6 form the synchronous gate sequence and MUST complete before the next governed action is admitted. Steps 7–9 are asynchronous and may complete after the next governed action has already proceeded.

### Synchronous Sequence (steps 1–6 — must complete before next action is admitted)

**Step 1 — Governance decision reached.**
The C2 policy evaluator (or C3, in the case of a CONTEXT_FAILURE) produces a verdict for the current governed action. The verdict is one of: PERMIT, DENY, CONTEXT_FAILURE, SCOPE_EXCEEDED, or another verdict type defined in Part II §4.4. The verdict, along with all decision inputs, is held in memory pending event construction.

**Step 2 — Event record constructed.**
A C5 event record is constructed with all required fields populated. Required fields include, at minimum: `gar_id` (unique event identifier), `verdict`, `policy_version`, `subject_id`, `action_class`, `timestamp` (UTC, ISO 8601), and any trajectory state identifiers required by C4 (if a trajectory profile is active for this action class). No field may be left unpopulated. Incomplete records MUST NOT be written to the local WAL.

**Step 3 — Prior event hash appended.**
The hash of the immediately prior event record in the local WAL is computed and written into the new event record:

```
event.chain_hash = hash(prior_event_record)
```

For the first event in a local WAL, `chain_hash` is set to a well-known genesis value (e.g., a string of zeros of the appropriate length, documented in the deployment's operational configuration). The hash function MUST be SHA-256 or stronger.

**Step 4 — Event signed locally.**
The event record is signed using the local signing key:

```
event.signature = sign(event_record, local_signing_key)
```

The local signing key MUST be consistent with the key infrastructure used for central C5 signing (see R.4, invariant 4). The signature covers the complete event record as it will be written to the WAL, including `chain_hash`.

**Step 5 — Event written to local append-only WAL.**
The signed event record is written to the local WAL. The write MUST be durable: an `fsync` call (or platform-equivalent durability barrier) MUST complete before step 6 proceeds. A write that has been acknowledged by the OS page cache but not yet flushed to durable storage does not satisfy this requirement.

If the write fails for any reason (I/O error, storage full, lock contention, fsync failure), the fail-deny procedure is triggered: the next governed action MUST be denied, and an operational alert MUST be raised immediately. See R.4, invariant 1.

**Step 6 — Local WAL pre-commit acknowledged → next governed action MAY proceed.**
Once the durable write in step 5 has completed successfully, the synchronous gate is passed. The next governed action MAY be submitted to the governance pipeline. Steps 7–9 proceed asynchronously in the background and do not block the next action.

### Asynchronous Sequence (steps 7–9 — may complete after the next action is admitted)

**Step 7 — Replication batch prepared and sent to central C5 store.**
One or more events from the local WAL are batched and transmitted to the central C5 store. Batching is implementation-defined. Implementations SHOULD minimize replication lag subject to the documented operational parameters (R.4, invariant 5).

**Step 8 — Central C5 store acknowledges receipt and verifies chain continuity.**
The central C5 store receives the batch, verifies that hash-chain continuity is maintained from the last previously replicated event, and acknowledges receipt. If the central C5 store cannot verify chain continuity (e.g., due to a gap or detected tampering), it MUST reject the batch and raise an operational alert. The local WAL remains authoritative during the resolution period.

**Step 9 — Proof-of-replication marker appended to local WAL (optional but recommended).**
After the central C5 store acknowledges receipt, a lightweight proof-of-replication marker is appended to the local WAL. This marker records the central store's acknowledgment identifier and timestamp, enabling recovery tooling to determine which local WAL events have been confirmed as replicated without querying the central store.

---

## R.4 Invariants of the Pattern

The following invariants apply to any implementation using this pattern. Statements using MUST are normative obligations under the CROA specification; they are re-stated here for convenience and do not introduce new requirements beyond those in Part II §4.7.

**Invariant 1 — Gate sequence is mandatory.**
Steps 1–6 MUST complete before the next governed action is admitted. Failure at any point in steps 1–6 triggers fail-deny: the governed action that would have been admitted MUST be denied. An operational alert MUST be raised. No exception is permitted, including during periods of degraded system performance.

**Invariant 2 — Local WAL is append-only.**
The local WAL MUST be append-only. No modification or deletion of prior entries is permitted under any circumstances, including error correction. If an event was recorded incorrectly, the correction MUST be recorded as a new event of type `CORRECTION` (or equivalent), referencing the `gar_id` of the event being corrected. The original erroneous event MUST remain in the WAL.

**Invariant 3 — Hash-chain continuity is mandatory.**
The local WAL MUST maintain hash-chain continuity. Every event's `chain_hash` field MUST equal the cryptographic hash of the immediately prior event record as written to the WAL. A gap, reordering, or missing event in the hash chain constitutes a WAL integrity failure and MUST be treated as a critical operational incident.

**Invariant 4 — Local signing key consistency, held off the agent host.**
The local signing key MUST be consistent with the key infrastructure used for central C5 signing. An auditor MUST be able to verify local WAL signatures using the same verification process and key registry as for central C5 signatures. Key rotation procedures MUST ensure continuity of verifiability across key versions (Part II §4.3.3).

The local WAL signing key MUST NOT reside in the governed agent's own trust domain. If the key that signs an agent's audit journal is resident on, and readable by, the compromised agent host, the journal is forgeable by the very principal it is meant to hold accountable — defeating the tamper-evidence guarantee against an A2 (insider/host-compromise) adversary. Therefore the signing operation for the local WAL MUST be performed in a co-located but **separately-trusted** signer — an HSM, a TPM-backed key, or a sidecar signer in a distinct security context — such that a compromise of the agent workload cannot extract the key or produce arbitrary signatures. A WAL whose signing key is extractable from the agent host is non-conformant. External anchoring of the sealed-segment head (Part V TH-4) remains required so that even suppression or truncation on the host is detectable centrally.

**Invariant 5 — Replication lag is a governed operational parameter.**
Replication lag MUST be documented as a governed operational parameter. The maximum acceptable replication lag MUST be declared in the deployment's operational documentation and actively monitored. Breaches of the declared maximum MUST generate an operational alert. The acceptable lag value is deployment-specific and outside the scope of this appendix, but MUST be declared.

**Invariant 6 — Local WAL is the authoritative record during replication gaps.**
In the event of replication failure, the local WAL is the authoritative evidence record. An auditor who cannot access the central C5 store for a period MUST be able to reconstruct the complete governance record for that period from the local WAL alone. The local WAL MUST therefore be stored with durability and access-control guarantees appropriate to its role as a primary evidence record, not merely as a staging buffer.

**Invariant 7 — Conformance tests are WAL-executable.**
A conformance test for C5 completeness MUST be executable from the local WAL (and, after replication, from the central store). The test MUST yield the same result whether run against the local WAL or the central C5 store for the same time period. If the two records diverge, the divergence itself is a conformance failure and MUST be reported as such.

---

## R.5 What This Pattern Does NOT Permit

The following practices are inconsistent with C5 completeness and MUST NOT be used, even when implementing the local WAL pattern:

- **Admitting the next governed action before step 5 completes.** The durable local WAL write is the gate. An OS page-cache write that has not been flushed to durable storage (e.g., write without `fsync`) does not satisfy the gate requirement, even if central replication has already been attempted.

- **Using central C5 replication latency as the synchronous gate.** The local WAL — not the central store — is the synchronous gate in this pattern. Waiting for central replication before admitting the next action is correct behavior but is not required; using central replication as the only gate (with no local WAL) is not this pattern and removes the local durability guarantee.

- **Retroactively inserting events into the local WAL.** Even to correct an error, no event may be inserted between existing WAL entries. Corrections are new forward entries. The WAL is strictly append-only.

- **Operating without a local WAL, using only direct central C5 writes.** If the network connecting the agent host to the central C5 store is unavailable, a direct-write-only implementation would have no gate mechanism. The local WAL is required precisely to decouple local governance durability from network availability.

- **Treating unreplicated events as lost or invalid.** Events that have been written to the local WAL but not yet replicated to the central C5 store are fully valid, authoritative evidence records. They are not provisional, tentative, or lower-status than replicated events. Their authority is the local WAL signature and hash chain, not their presence in the central store.

---

## R.6 Performance Reference

With a local NVMe or equivalent durable storage medium, step 5 (WAL write with `fsync`) adds approximately 0.5–2 milliseconds of latency per governed action in typical deployment conditions. This is a reference figure for planning purposes, not a conformance criterion. Implementations MUST measure and report their own latency characteristics per Appendix J.

The latency impact of this pattern is substantially lower than the round-trip cost to a remote central C5 store. A round-trip to a central store in a different availability zone or region will typically incur 5–50 milliseconds of network latency before storage write time. Organizations evaluating C5 performance in high-throughput scenarios SHOULD evaluate the local WAL pattern before concluding that synchronous evidence commitment is operationally infeasible.

Throughput at 1 ms per WAL write (mid-range estimate): approximately 1,000 governed actions per second per WAL instance. Implementations requiring higher throughput may operate multiple parallel WAL instances (one per agent instance), provided each WAL independently satisfies all invariants in R.4 and the central C5 store is designed to receive and merge concurrent replication streams with chain-continuity verification per stream.

---

## R.7 Sequence Description

The following text-based sequence summary is provided for implementation reference. It captures the decision structure of the pattern for integration into design documentation and code review checklists.

```
For each governed action in the pipeline:

[SYNCHRONOUS — gate sequence]
  Decision produced by C2 (or C3 for CONTEXT_FAILURE)
    → Construct event record (all required fields populated)
    → Compute chain_hash = hash(prior_event_record)
    → Sign event: event.signature = sign(event_record, local_signing_key)
    → Write to local WAL (durable write — fsync or equivalent must complete)
      → If WAL write FAILS:
            FAIL-DENY — block next governed action
            Raise operational alert (do not suppress)
            Do not proceed to asynchronous sequence
      → If WAL write SUCCEEDS:
            GATE PASSED — next governed action may proceed

[ASYNCHRONOUS — replication, runs in background]
  Batch one or more WAL events
    → Transmit to central C5 store
    → Central C5 store verifies chain continuity from last replicated event
      → If continuity check FAILS:
            Reject batch
            Raise operational alert
            Local WAL remains authoritative — do not discard
      → If continuity check SUCCEEDS:
            Central C5 store acknowledges receipt
            [Optional] Append proof-of-replication marker to local WAL
```

The gate is crossed at "WAL write SUCCEEDS." Everything before that point is the synchronous obligation. Everything after is the asynchronous replication consequence. The two sequences are independent: replication failure does not retroactively invalidate events already written to the local WAL and does not block subsequent gate passages, but MUST trigger an operational alert and remediation.

---

*End of Appendix R.*
