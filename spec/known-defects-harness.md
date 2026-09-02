# Known defects — Minimal Reference Harness

The [Minimal Reference Harness](https://github.com/CROA-Project/croa-reference-harness) is the only
runnable artifact CROA publishes. In September 2026 an independent enterprise-architecture audit
reviewed it line by line, ran its tests, validated its outputs against this repository's JSON
schemas, and wrote negative tests the harness did not ship. It reproduced two bypasses. The project
reproduced those two, found a third, and fixed four.

This page exists so that a reader meets the findings before running the harness, rather than after.
Fixed entries keep their original description: what a defect *was* is part of what a reader needs, and
a register that erases its closed entries is a marketing page. Each entry is closed only by a fix
**and** a test.

> **Status — confirmed, then fixed.** The findings were reported by an external auditor on
> 2 September 2026. The CROA Project reproduced **H-01, H-02 and H-03** the same day, found that
> **H-04** followed from H-01, and **fixed all four**. The fix ships with an adversarial test group
> and two 100-thread concurrency races; the full suite is 16 tests and passes.
>
> **H-05, H-06 and H-07 remain open**, and H-06 is the one that matters most: the harness still has
> no network boundary, so property **P4** — the most load-bearing condition of CROA's central claim —
> is not demonstrated at all.
>
> The frozen reproduction of the defects as they stood before the fix is kept at
> [`evidence/harness-defects/`](../evidence/harness-defects/). The **regression gate** is the
> harness's own `TestAdversarial` suite, which runs against the real code. (An earlier version of
> this page called the frozen script the gate. It is not: it copies the harness rather than importing
> it, so it can never pass. The correction is recorded in that directory's README.)
>
> A reader who finds a defect this list misses is giving the project something more useful than a
> confirmation.

---

## What this means for the claims

Three statements the project had published were not supported by the artifact meant to support them.
All three were corrected in the documentation first, before any code changed:

| Statement | Where it appeared | Outcome |
|---|---|---|
| "demonstrates the C1–C7 enforcement behavior" | `docs/quick-start.md` | **Still overstated, and still corrected.** The harness runs a *reduced* plane — mock C1, C2, C3, C5, C6, C7 — with **no C4** and **no admission layer**. The fix did not change this (H-05). |
| "the decisions are reconstructable from the log alone" | `docs/quick-start.md` | **Now true of the harness, within its scope.** `verify()` performs the Appendix G.2.4 correlation as of the H-04 fix. It remains false that a chain proves *capture completeness* — see P-E. |
| a signed authorization admits "exactly one" execution | harness `README.md` | **Was false; is now true and tested.** H-01 is fixed, with a test at N = 2 and a 100-thread race. |

**None of this changes the specification.** These are defects in a demonstrator, not in the
architecture it demonstrates. But a demonstrator that admits what the specification forbids is worse
than no demonstrator, because it invites a reader to conclude the specification is what fails.

---

## Fixed — 2 September 2026

H-01 to H-04 are closed. Each entry keeps its original description, so a reader can see what the
defect was, and ends with what was done.

### H-01 — One exception authorization can produce two admitted executions **· FIXED**

**What the specification requires.** Property **P-D** and reference negative test **NT-007**: a
governed exception authorization admits at most one execution, including under concurrency, across
every enforcement instance.

**Reported cause.** `PolicyAuthority.authorization_covers()` checks only that `auth_id` is absent
from `redeemed_auths`. Consumption happens later, in `Harness.present()`, *after* `C6` admits. Two
`C2` decisions and two compiled commitments can therefore be produced before the first redemption.
Each commitment carries a distinct `cc.id`, so `C6` sees no conflict and admits both.

**Reproduction (sequential, no threads).** Issue an authorization for an invariant-violating action;
call `C2` twice with it before any execution; compile two CCs; present both. Both are admitted, and
`C5` chain verification still returns true. **Confirmed by the project on 2 September 2026** —
[`evidence/harness-defects/reproduce.py`](../evidence/harness-defects/reproduce.py), test `h01`.

The defect is a *check-then-act* — and it is one the specification already forbids. Part II §4.8
requires redemption to be a single atomic linearizable compare-and-swap. Every commitment compiled
between the read and the write is admissible.

**Why it matters.** The exception path is the architecture's most sensitive surface, and this makes
it multiplicative: one single-use authorization becomes *N* commitments before the first redemption.

**Fixed.** Consumption moved from `C6` to `C7` and became an atomic test-and-set:
`PolicyAuthority.reserve_authorization()` is now the only method that may spend an authorization, and
it raises `AuthorizationSpent` — fail-deny, **no commitment produced** — if the authorization is
already spent. A `C2` decision is explicitly not a reservation. `C6` additionally consumes the
`auth_id`/`cc.id` pair inside one critical section. Tested at N = 2 and with a **100-thread race**,
which must and does admit exactly one winner.

**What the fix does not do.** The atomic section is a `threading.Lock` in one process. A real
deployment needs one shared authority — a conditional write, a compare-and-swap, or a transaction —
visible to every `C6` and `C7` instance. The tests establish the *shape* of the guarantee, not that
it survives distribution.

### H-02 — Subject substitution is admitted; the presented operation is never compared to the CC **· FIXED**

**What the specification requires.** Complete mediation (**P-A**) and authority non-expansion
(**P-B**, **I8**) require the executed operation to be the one authorized, for the subject, session,
target and scope recorded.

**Reported cause.** `ExecutionFirewall.redeem(cc, now)` receives neither an authenticated identity
nor the operation being presented. It validates the HMAC, expiry and `cc.id` only.
`Harness.present(cc, now, sid)` takes an unsigned `sid` separately and writes it into `C5` without
comparing it to the subject inside the CC's action.

**Reproduction.** A fresh CC containing `subject-A` was presented with `sid="subject-B"` and
admitted. `C5` recorded `subject-B`. **Confirmed by the project on 2 September 2026** —
[`evidence/harness-defects/reproduce.py`](../evidence/harness-defects/reproduce.py), test `h02`.

**Why it matters.** The harness cannot detect presentation of a commitment by another subject,
mutation of the operation between compilation and execution, widening of target, parameters or
scope, or session and tenant confusion. This is the falsifying case of **NT-008**, on a demonstrator
that does not implement NT-008.

**Fixed.** `redeem(cc, now, subject_id, operation)` and `present(cc, now, subject_id, operation)` —
both new arguments are **mandatory**, so the unsafe call is no longer expressible. `C6` compares the
authenticated subject and the concrete operation against the signed commitment and returns
`CC_SUBJECT_MISMATCH` or `CC_OPERATION_MISMATCH`. The `C5` write now takes its subject, action and
session from the validated commitment; nothing on that event comes from the caller.

**What the fix does not do.** The harness has no admission layer, so `subject_id` is *taken* as
authentic because there is nothing that could authenticate it (H-05). This closes the substitution
case, not the identity problem. And delegation is still absent, so **NT-008** remains unimplemented.

### H-03 — Harness output does not validate against this repository's schemas **· PARTLY FIXED**

Validating the harness's output against [`spec/schemas/`](schemas/) fails.

- **Compiled Commitment** — carries `action`, `expiry`, `signature`, `single_use`, which the schema
  does not define; and omits `cc.action`, `cc.subject`, `cc.session_id`, `cc.permit_event_id`,
  `cc.decision_basis`, `cc.authorization_scope`, `cc.policy_artifact_id`,
  `cc.invariant_set_version`, `cc.reversibility_class`, `cc.compiled_at`, `cc.expires_at`,
  `cc.signer_id`, `cc.signature`.
- **Events** — `PERMIT` omits `event.session_id`, `event.policy_artifact_id`,
  `event.invariant_state`; `CC_COMPILED` omits those plus `event.action_spec` and
  `event.decision_basis`; `EXECUTION_AUTHORIZED` omits `event.session_id` and `event.action_spec`.
- **`cc.id` is not content-addressed.** A random UUID is mixed in and the digest truncated to 16
  characters, so the identifier is not the SHA-256 of the commitment's content — which is what
  "content-addressed" means in Part II §4.4.1. **Confirmed by the project on 2 September 2026**:
  compiling the identical action twice yields two different identifiers
  ([`reproduce.py`](../evidence/harness-defects/reproduce.py), test `h03`).

**Why it matters.** The reference demonstrator and the machine-readable contract describe two
incompatible protocols. An auditor cannot use the schemas to check the harness, and a
schema-conformant implementation cannot consume the harness's events.

**Partly fixed — the content-address half only.** `cc.id` is now the full SHA-256 of the
commitment's canonical content, with no random component; `permit_event_id` is part of that content,
so two legitimate decisions over the same action still yield distinct identifiers. `C6` recomputes
the address and refuses a mismatch (`CC_ID_NOT_CONTENT_ADDRESSED`).

*One note on the test for that.* The first version of it forged `cc.id` without re-signing, so the
signature check fired first and the content-address branch was never reached — a dead failure branch,
which is the very defect class H-07 is about. The test now re-signs the forged commitment and asserts
on the specific block reason.

**Still open — schema conformance.** Commitments and events do **not** validate against
[`schemas/`](schemas/). Generating the harness's types from the schemas, validating at emission under
test, and failing CI on drift is the next thing worth doing, and the most useful contribution
available here.

---

## High

### H-04 — `C5` verification does not reconstruct decisions **· FIXED**

Appendix G.2.4 requires a verifier to check the chain, detect a break, link each `PERMIT` to a
`CC_COMPILED` bearing the same `cc_id`, and require exactly one `EXECUTION_AUTHORIZED` per compiled
commitment. `AuditStore.verify()` recomputes the chain and each event's HMAC and performs no
correlation at all. The events are in any case too sparse to support it (no session, policy version,
full invariant state, permit-event id, or complete action on the `C7`/`C6` events).

The practical consequence is H-01's log: two authorized executions from one single-use
authorization, and `verify()` returns true.

**Fixed.** `AuditStore` now exposes three methods, kept deliberately separate so that no one can
mistake one for the other:

- `verify_chain()` — the old behaviour: hashes and signatures, and nothing more.
- `verify_decisions()` — the G.2.4 correlation: every commitment cites an earlier permit, one
  commitment per permit, one execution per commitment, **one execution per authorization**, and the
  executing subject is the one the commitment was compiled for.
- `verify()` — both.

Events gained the fields the correlation needs (`event.session_id`, `event.permit_event_id`,
`event.action_spec` on the `C7`/`C6` events). Negative-log tests cover deletion, tampering, an orphan
execution, and a double authorization; each must break verification while the chain stays intact.

*The new verifier caught a defect in its own author's test code on first run* — a scenario that drove
`C7` directly without recording `CC_COMPILED`, producing an execution citing a commitment absent from
the log. It refused, correctly.

## Still open

### H-05 — `C4` and the admission layer are absent **· OPEN**

| Component | State | Gap |
|---|---|---|
| Admission | absent | no authentication, RBAC or AQL — `subject_id` is *taken* as authentic |
| `C1` | partial mock | in-memory Python set; no versioned, signed policy artifact |
| `C2` | partial mock | one boolean invariant; no state, version or decision basis |
| `C3` | partial mock | static membership test |
| `C4` | **absent** | no trajectory state, no TP-C/TP-X, no NT-006 |
| `C5` | *improved* | chain, signatures **and** G.2.4 correlation since the H-04 fix |
| `C6` | *improved* | now checks subject, operation and content address — but still no network boundary (H-06) |
| `C7` | *improved* | links to the permit event, reserves the authorization atomically, emits a canonical `cc.id` — but the commitment still does not match the schema |

The H-02 fix closes subject *substitution*. It does not give the harness a way to know that a subject
is who it says it is: that needs an admission layer, and there isn't one.

### H-06 — Property P4 is not demonstrated **· OPEN, and the largest gap**

The harness calls a Python method. There is no governed system, no alternative channel, no network
policy, and no gateway constituting the sole execution path; `C6` returns a boolean rather than
performing an operation. NT-001 therefore shows that `present(None)` returns `BLOCKED` — not that a
non-CC execution is structurally unreachable. Network-enforced containment is the most load-bearing
condition of CROA's central claim, and it is the one the harness does not test at all.

**Fix required.** An isolated target system with two paths: a direct call that must fail at the
network or identity layer, and a call through `C6` with a valid CC. Assert on external effects, not
on a function's return value.

### H-07 — The test suite is cooperative **· PARTLY CLOSED**

As audited: `make test` ran two test methods; `make demo` showed six scenarios, all calling the API in
the intended order with well-formed inputs. Nothing attempted forgery, mutation, subject
substitution, event tampering, orphan commitments, or concurrency.

**Partly closed.** The suite is now sixteen tests, with an adversarial group covering forged
signatures, a forged-and-re-signed content address, mutated operations, subject substitution, deleted
and tampered events, orphan executions, double authorization, and two 100-thread races on
reservation and redemption.

**Still open.** Every one of those tests was written by the project, against its own artifact, from a
list of defects someone else found. That is a weaker thing than an outside attempt to break it, and
the gaps in H-05 and H-06 are where an outside attempt would start.

---

## Where each reference negative test actually stands

| Test | Claimed | State | Verdict |
|---|---|---|---|
| NT-001 non-CC blocked | yes | `present(None)` blocked; still no external execution path tested (H-06) | partial |
| NT-002 expired CC | yes | correctly blocked | holds in the mock |
| NT-003 replay | yes | sequential replay blocked, and now a 100-thread race admits exactly one | holds in the mock |
| NT-004 unknown context | yes | `C3` blocks before `C2` | holds in the mock |
| NT-005 ambiguous E3 | no | absent | not covered |
| NT-006 trajectory | no | `C4` absent | not covered |
| NT-007 governed exception | replay only | replay blocked; double pre-compilation now refused at `C7`; **scope widening still absent** | partial |
| NT-008 authority non-expansion | no | delegation still absent; subject substitution now refused | **partial — the base case only** |

---

## Exit criteria

The harness should not be described as a reference for CROA behaviour until all of the following hold
at once. Four of eight are met.

| | Criterion | State |
|---|---|---|
| ☐ | zero validation errors against the canonical schemas | **not met** (H-03, remaining half) |
| ☐ | NT-001 to NT-007 complete, including concurrency and scope widening | **not met** — NT-005, NT-006 absent; NT-007 lacks scope widening |
| ☑ | exactly one admission for N concurrent presentations of the same commitment or authorization | met, in one process (H-01) |
| ☑ | subject and action substitution always refused | met (H-02) |
| ☑ | a `C5` verifier conformant to G.2.4 that rejects every negative log | met for the negative logs tested (H-04) |
| ☐ | a direct network path to the governed system that is technically unreachable | **not met** (H-06) |
| ☐ | required, reproducible CI on a protected commit | **not met** — the harness repository still has no CI and no ruleset |
| ☐ | an immutable release bound to a specific specification version | **not met** (erratum E-14) |

Until all eight hold, it is a demonstrator of the *mechanism*, with the gaps above.

---

**Related.** [`docs/limitations.md`](../docs/limitations.md) (evidence base) ·
[`properties.md`](properties.md) (what the specification claims) ·
[`errata-v1.0.md`](errata-v1.0.md) (defects in the published draft) ·
[`../GOVERNANCE-DEVIATIONS.md`](../GOVERNANCE-DEVIATIONS.md) (where the project did not follow its own process)
