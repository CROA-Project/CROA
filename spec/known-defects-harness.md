# Known defects — Minimal Reference Harness

The [Minimal Reference Harness](https://github.com/CROA-Project/croa-reference-harness) is the only
runnable artifact CROA publishes. In September 2026 an independent enterprise-architecture audit
reviewed it line by line, ran its tests, validated its outputs against this repository's JSON
schemas, and wrote negative tests the harness does not ship. It reproduced two bypasses. The
project has since reproduced those two and a third.

This page exists so that a reader meets those findings before running the harness, rather than after.
It is maintained until each entry is closed by a fix and a test.

> **Status of these findings — confirmed.** They were reported by an external auditor. The CROA
> Project has since reproduced **H-01, H-02 and H-03** against the published harness code, and
> publishes the reproduction as a runnable script:
> [`evidence/harness-defects/reproduce.py`](../evidence/harness-defects/reproduce.py). It exits
> non-zero while any of the three reproduces, so it works as a regression gate once they are fixed.
> H-04 through H-07 are structural and verifiable by reading the code; they have not been given a
> separate script.
>
> A reader who makes the script *fail* to reproduce, or who finds a defect it misses, is giving this
> project something more useful than a confirmation. Either result will be recorded here.

---

## What this means for the claims

Three statements the project had published are **not supported by the harness as it stands**, and
have been corrected:

| Statement | Where it appeared | Corrected to |
|---|---|---|
| "demonstrates the C1–C7 enforcement behavior" | `docs/quick-start.md` | a *reduced* control plane: mock C1, C2, C3, C5, C6, C7 — **no C4**, **no admission layer** |
| "the decisions are reconstructable from the log alone" | `docs/quick-start.md` | `verify()` recomputes the chain and signatures and does nothing else; Appendix G.2.4 correlation is not implemented |
| a signed authorization admits "exactly one" execution | harness `README.md` | **false** — H-01 below, reproduced by the project |

**None of this changes the specification.** These are defects in a demonstrator, not in the
architecture it demonstrates. But a demonstrator that admits what the specification forbids is worse
than no demonstrator, because it invites a reader to conclude the specification is what fails.

---

## Critical

### H-01 — One exception authorization can produce two admitted executions

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

**Fix required.** Consumption must be a single atomic, linearizable operation shared by all
instances — reserve or consume `auth_id` at compilation, or make admission one `authorize-and-redeem`
transaction at `C6`. The CC must carry the authorization and its scope; `C6` must atomically consume
the `auth_id`/`cc.id` pair before any external effect. Tests at N = 2 and N ≥ 100, across multiple
`C6` instances.

### H-02 — Subject substitution is admitted; the presented operation is never compared to the CC

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

**Fix required.** `C6` must receive the authenticated identity and the concrete operation, recompute
the canonical representation, and compare at minimum `cc.subject`, `cc.session_id`, `cc.action`,
`cc.authorization_scope`, `cc.policy_artifact_id`, `cc.invariant_set_version`, expiry, revocation,
exception scope and signature. The `C5` write must take its values from the validated CC and the
admission, never from a caller-supplied `sid`.

### H-03 — Harness output does not validate against this repository's schemas

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

**Fix required.** Generate the harness's types from the schemas; validate every CC and event at
emission under test; fail CI on any deviation. Define `cc.id` as the SHA-256 over all canonical
fields except the identifier, with canonicalisation and signing rules written down.

---

## High

### H-04 — `C5` verification does not reconstruct decisions

Appendix G.2.4 requires a verifier to check the chain, detect a break, link each `PERMIT` to a
`CC_COMPILED` bearing the same `cc_id`, and require exactly one `EXECUTION_AUTHORIZED` per compiled
commitment. `AuditStore.verify()` recomputes the chain and each event's HMAC and performs no
correlation at all. The events are in any case too sparse to support it (no session, policy version,
full invariant state, permit-event id, or complete action on the `C7`/`C6` events).

The practical consequence is H-01's log: two authorized executions from one single-use
authorization, and `verify()` returns true.

**Fix required.** Implement G.2.4 in full, with cardinality and causality constraints and an
enforced `PERMIT → CC_COMPILED → EXECUTION_AUTHORIZED` order; then add negative-log tests —
deletion, duplication, reordering, corruption, orphan CC, double authorization.

### H-05 — `C4` and the admission layer are absent

| Component | State | Gap |
|---|---|---|
| Admission | absent | no authentication, RBAC or AQL |
| `C1` | partial mock | in-memory Python set; no versioned, signed policy artifact |
| `C2` | partial mock | one boolean invariant; no state, version or decision basis |
| `C3` | partial mock | static membership test |
| `C4` | **absent** | no trajectory state, no TP-C/TP-X, no NT-006 |
| `C5` | partial | chain and signatures, but no G.2.4 reconstruction |
| `C6` | partial | no network boundary, no concrete operation, no scope check |
| `C7` | partial | compiles without linking to PERMIT, policy or invariant set; CC not canonical |

### H-06 — Property P4 is not demonstrated

The harness calls a Python method. There is no governed system, no alternative channel, no network
policy, and no gateway constituting the sole execution path; `C6` returns a boolean rather than
performing an operation. NT-001 therefore shows that `present(None)` returns `BLOCKED` — not that a
non-CC execution is structurally unreachable. Network-enforced containment is the most load-bearing
condition of CROA's central claim, and it is the one the harness does not test at all.

**Fix required.** An isolated target system with two paths: a direct call that must fail at the
network or identity layer, and a call through `C6` with a valid CC. Assert on external effects, not
on a function's return value.

### H-07 — The test suite is cooperative

`make test` runs two test methods; `make demo` shows six scenarios, all of which call the API in the
intended order with well-formed inputs. Nothing attempts forgery, mutation, subject substitution,
event tampering, orphan commitments, or concurrency. The harness README already says `redeem` is a
check-then-act on an unlocked `set`; the risk that describes is live, not hypothetical.

---

## Where each reference negative test actually stands

| Test | Claimed | Audited state | Verdict |
|---|---|---|---|
| NT-001 non-CC blocked | yes | `present(None)` blocked; no external execution path tested | partial |
| NT-002 expired CC | yes | correctly blocked | holds in the mock |
| NT-003 replay | yes | sequential replay of one `cc.id` blocked; concurrency untested and racy | partial |
| NT-004 unknown context | yes | `C3` blocks before `C2` | holds in the mock |
| NT-005 ambiguous E3 | no | absent | not covered |
| NT-006 trajectory | no | `C4` absent | not covered |
| NT-007 governed exception | replay only | simple replay blocked; **double pre-compilation succeeds** (H-01) | **fails** |
| NT-008 authority non-expansion | no | delegation absent; **subject substitution admitted** (H-02) | **fails on a base case** |

---

## Exit criteria

The harness should not be described as a reference for CROA behaviour until all of the following
hold at once:

- zero validation errors against the canonical schemas;
- NT-001 to NT-007 complete, including concurrency and scope widening;
- exactly one admission for N concurrent presentations of the same CC or authorization;
- subject, session and action substitution always refused;
- a `C5` verifier conformant to G.2.4 that rejects every negative log;
- a direct network path to the governed system that is technically unreachable;
- required, reproducible CI on a protected commit;
- an immutable release bound to a specific specification version.

Until then it is a demonstrator of the *mechanism*, with the defects above.

---

**Related.** [`docs/limitations.md`](../docs/limitations.md) (evidence base) ·
[`properties.md`](properties.md) (what the specification claims) ·
[`errata-v1.0.md`](errata-v1.0.md) (defects in the published draft) ·
[`../GOVERNANCE-DEVIATIONS.md`](../GOVERNANCE-DEVIATIONS.md) (where the project did not follow its own process)
