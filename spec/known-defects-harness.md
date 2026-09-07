# Known defects — Minimal Reference Harness

The [Minimal Reference Harness](https://github.com/CROA-Project/croa-reference-harness) is the only
runnable artifact CROA publishes. In September 2026 an independent enterprise-architecture audit
reviewed it line by line, ran its tests, validated its outputs against this repository's JSON
schemas, and wrote negative tests the harness did not ship. It reproduced two bypasses. The project
reproduced those two, found a third, and fixed four.

On **7 September 2026**, while making the harness atomic across enforcement instances, the project
found a fifth: **H-08**, a second bypass of the same class as H-01, living in the code written to fix
H-01. It is recorded below rather than folded into H-01, because a defect found after its class was
declared closed is the more useful record.

Later the same day, **H-03 closed** and **H-06 narrowed**. Both had stood since the audit, and
neither closed the way this page had predicted: H-03 was not a set of missing fields but a missing
artifact, and H-06 is closed *in the harness* and open *in every deployment*, which is a distinction
the entry keeps rather than rounding off.

This page exists so that a reader meets the findings before running the harness, rather than after.
Fixed entries keep their original description: what a defect *was* is part of what a reader needs, and
a register that erases its closed entries is a marketing page. Each entry is closed only by a fix
**and** a test.

> **Status — confirmed, then fixed.** The findings were reported by an external auditor on
> 2 September 2026. The CROA Project reproduced **H-01, H-02 and H-03** the same day, found that
> **H-04** followed from H-01, and **fixed all four**. The fix ships with an adversarial test group
> and two 100-thread concurrency races; the full suite is 16 tests and passes.
>
> **Updated 7 September 2026, twice.** The v1.0.1 work closed part of this page and found **H-08**,
> a second bypass of the same class as H-01, inside the code written to fix H-01. Later the same day
> **H-03 closed completely** and **H-06 was narrowed** — the two entries that had stood longest.
>
> **H-03 · closed.** Every emitted event and every compiled ECC validates against the published
> schemas, and both are gated in CI. The fix was not the list of missing fields this entry used to
> carry: the harness had no grounded governed action at all.
>
> **H-06 · partly closed, and read the second half.** There is now a governed system in its own
> process, reachable only through `C6`, and every assertion is on that system's own log rather than
> on a return value. What that establishes is that **the mechanism can be demonstrated**; it does not
> establish that a *deployment* has property P4, because the unreachability comes from not naming a
> socket rather than from a network policy. The difference is the whole of what an adopter needs, and
> it is still open.
>
> **H-05 · partly closed** — `C4` exists, and so does an admission predicate; authentication does
> not. **H-07** is broadened, not closed, and H-08 is what that cost.
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
| "demonstrates the C1–C7 enforcement behavior" | `docs/quick-start.md` | **Still overstated, and less so again.** The plane now includes `C4`, an admission predicate, and a `C6` gateway holding the only channel to a governed system in its own process. It remains *reduced*: no authentication behind the predicate (H-05), and the boundary is process isolation rather than network policy (H-06). |
| "the decisions are reconstructable from the log alone" | `docs/quick-start.md` | **Now true of the harness, within its scope.** `verify()` performs the Appendix G.2.4 correlation as of the H-04 fix. It remains false that a chain proves *capture completeness* — see P-E. |
| a signed authorization admits "exactly one" execution | harness `README.md` | **Was false; then true in one process; now true across processes.** H-01 was fixed with a test at N = 2 and a 100-thread race; H-08 showed that guarantee stopped at the process boundary, and it now holds across enforcement instances through a shared registry, tested with an 8-process race. Across *hosts* it is delegated to the deployment, not demonstrated. |

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

*That paragraph was written as a limitation. It was a defect — see **H-08**.*

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

### H-03 — Harness output does not validate against this repository's schemas **· FIXED**

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

**Half closed — events, 7 September 2026.** Every event the harness emits now validates against
[`schemas/event.schema.json`](schemas/event.schema.json), and this is enforced rather than asserted:
`TestEventSchemaConformance` in the harness suite checks out this repository, validates the whole
emitted record, and the `schema-conformance` job fails the build on any drift. That is the join
between the two repositories, and it now exists in CI rather than in a promise.

**Closed — the ECC, 7 September 2026.** The list above is what the ECC looked like when this
entry was last written, and it is kept because what a defect *was* is part of what a reader needs.
The fix did not add those fields.

**The defect was not a set of missing fields.** It was that the harness had no grounded governed
action at all: `C3` answered a boolean and the raw request was carried onward, so `ecc.action`
described an action that nothing had grounded. Padding the contract with the properties the schema
names would have produced an object that validates and still lies — the failure this page exists to
catch — so `C3` now returns the `gga.*` artifact of §4.5.1, and everything downstream carries it.

Three consequences worth recording, because each was a latent defect of its own:

- **`C7` now requires a `GROUNDED` gga** and raises otherwise, so an ECC compiled from an ungrounded
  request is not constructible.
- **`subject_id` is mandatory at compilation** and comes from the permit decision. It was being read
  out of the request payload — the same mistake H-02 fixed at the boundary and left standing one
  component upstream.
- **The authorization fingerprint bound the authorization to `session_id` and `gar_id`.** The same
  authorized operation arriving in a different session would have been refused as "not bound to this
  action", a constraint §4.3.1 does not impose. It now covers the operation and the subject, and
  nothing about where the request came from.

`C1` gained two things it had never been asked: a reversibility class and, above `R0`, a recorded
control. Both **raise rather than defaulting** — an action class whose consequence nobody classified
is one nobody thought about, and a silently assumed `R0` is the most expensive possible guess (§2.6).

**How it was caught, and the order it was caught in.** The conformance test was committed **before**
the fix, red, and is on record having failed: a conformance job added after the object already
conforms proves nothing about the object. Both halves of H-03 are now gated in CI —
`TestEventSchemaConformance` and `TestEccSchemaConformance` — and verified on the merged harness:
**13 events and 2 ECCs, zero validation errors.**

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

## Fixed — 7 September 2026

### H-08 — The redemption registry was per-instance, so H-01 was reachable one instance away **· FIXED**

**What the specification requires.** Part II §4.8: an ECC and its authorization are redeemed exactly
once, by a **single linearizable compare-and-swap**, and the guarantee holds **across every
enforcement instance**. §4.8 says "every enforcement instance" precisely because a per-process
guarantee is the easy thing to build and not the thing required.

**How it was found.** Not by an audit, and not by a test. H-01's entry above already ended with the
sentence that describes this defect:

> *The atomic section is a `threading.Lock` in one process. A real deployment needs one shared
> authority — a conditional write, a compare-and-swap, or a transaction — visible to every `C6` and
> `C7` instance. The tests establish the shape of the guarantee, not that it survives distribution.*

That was written as a limitation of a demonstrator. It was a defect. The demonstrator admitted what
§4.8 forbids, which is the definition this page uses for every other entry on it; calling the same
fact a limitation when it appears in one's own fix, and a defect when someone else finds it, is the
distinction the register exists to refuse.

**Cause.** Each `ExecutionFirewall` held its own `redeemed` set. Two `C6` instances over the same
policy each kept a private record of what had been spent, so a single ECC was redeemable **once per
instance**, and one single-use authorization backed one execution per instance.

**Why the September fix did not catch it, and why the 100-thread race did not either.** Both the
regression test for H-01 and its race exercised **one** instance. On a single instance a per-instance
registry and a shared one are observationally identical: every assertion passes either way. The test
measured the property it was written for and was blind to the property beside it — which is H-07,
stated concretely.

**Why it matters.** H-01 multiplied by the number of enforcement instances rather than by the number
of compilations. And it sat behind a **green adversarial suite** that was cited as evidence the class
was closed. A defect behind a passing test that was believed to cover it is worse than a defect
behind no test, because the passing test is what stops anyone looking.

**Fixed.** Redemption moved out of the component and behind a `RedemptionRegistry` interface whose
`claim(keys)` is **all-or-nothing over the whole key set** — the ECC identifier and the authorization
identifier are claimed together or neither is, which is what makes "a single compare-and-swap" true
rather than approximately true. Three implementations ship:

| implementation | mechanism | deployment |
|---|---|---|
| `InProcessRegistry` | a lock and a set | single process; tests |
| `FileLockRegistry` | an `fcntl` advisory lock over a durable set | single host, multiple processes |
| `ConditionalWriteRegistry` | a conditional write against an external store | distributed |

Tested by a second `C6` instance being refused the same ECC, by an all-or-nothing claim where the
authorization conflicts and the ECC is left untouched, and by an **8-process** race across real
`fork`ed processes that must and does produce exactly one winner.

**What the fix does not do.** `ConditionalWriteRegistry` is the seam, not an adapter: no Postgres,
Redis or etcd binding ships, and a half-tested one under a section whose entire content is *"exactly
once"* would be worse than the seam. `FileLockRegistry` uses `fcntl` and is therefore POSIX-only. So
the distributed guarantee is **stated and delegated to the deployment**, not demonstrated — which is
the honest position, and is the same sentence H-01 ended on. It is written here so that whoever
writes the first adapter knows this paragraph is where the next H-08 would live.

---

## Still open

### H-05 — `C4` and the admission layer are absent **· PARTLY CLOSED**

As audited, and as it stands after v1.0.1:

| Component | As audited | 7 September 2026 |
|---|---|---|
| Admission | absent — no authentication, RBAC or AQL | *partial* — `AgentSurface` applies the §4.9.1 predicate against the **submitting** subject's own roles, and carries a qualification flag standing in for the AQL (§4.9.2). **Still no authentication.** |
| `C1` | in-memory set; no versioned, signed policy artifact | names a `policy_artifact_id` and an invariant-set version on every decision; still no artifact *document*, versioned or signed |
| `C2` | one boolean invariant; no state, version or decision basis | registered invariants with evaluability classes E1/E2/E3, a decision basis, and an `E3` analyzer with a pinned version and a budget beyond which it returns `AMBIGUOUS` |
| `C3` | static membership test | **produces the grounded governed action** of §4.5.1, with the resolution record the ECC is required to carry, and a fail-closed `available` flag (§4.5). The resolution itself is still a membership test |
| `C4` | **absent** — no trajectory state, no TP-C/TP-X, no NT-006 | **present** — `InvariantMonitor` keeps trajectory state, implements TP-C and TP-X, emits `TRAJECTORY_ALERT`, and NT-006 runs against it |
| `C5` | chain, signatures and G.2.4 correlation since H-04 | unchanged |
| `C6` | subject, operation and content address | + redemption through a **shared** registry (H-08); + a **gateway process** holding the only channel to a governed system (H-06), though by process isolation rather than network policy |
| `C7` | permit link, atomic reservation, canonical `cc.id` | + refuses an action class the submitting subject does not hold; + requires a `GROUNDED` action and a subject from the decision rather than from the payload; the ECC **validates** against `ecc.schema.json` (H-03) |

**Partly closed.** `C4` is no longer absent, and neither is the admission predicate. That predicate
is what makes authority laundering structurally impossible rather than merely unlikely — I8 clause
(b) is enforced by refusing the request at the surface, before any component that could be persuaded
has seen it, which is what NT-008 Part B now tests.

**Still open — authentication.** The H-02 fix closed subject *substitution*. `AgentSurface` closes
what a subject may **ask for**. Neither gives the harness a way to know that a subject is who it says
it is: `subject_id` is still *taken* as authentic, because nothing in the harness could establish it.
An RBAC predicate over an unauthenticated identifier is an honest half of an admission layer, and it
should not be read as more than that.

### H-06 — Property P4 is not demonstrated **· PARTLY CLOSED — in the harness, not in a deployment**

As audited: the harness calls a Python method. There is no governed system, no alternative channel,
no network policy, and no gateway constituting the sole execution path; `C6` returns a boolean rather
than performing an operation. NT-001 therefore shows that `present(None)` returns `BLOCKED` — not
that a non-CC execution is structurally unreachable. Network-enforced containment is the most
load-bearing condition of CROA's central claim, and it was the one the harness did not test at all.

**What now exists (7 September 2026).** `mrh/p4.py` builds the arrangement the fix asked for, in
three operating-system processes rather than three objects:

```text
agent ──(unix socket)──▶ C6 gateway ──(fd)──▶ governed system
  │                                                  │
  └────── no address to connect to ────X             ▼
                                                its own log
```

The governed system is a separate process whose only channel is one end of a `socketpair` handed to
the gateway at spawn. **It never calls `bind()`**, so there is no path in the filesystem and no port
on the loopback interface: the agent has nothing to connect *to*. The unreachability is not a check
that could be wrong — it is the absence of an address, and the proof is a line that does not exist.

The gateway is addressable, and must be: `C6` is the *sole* execution path, not a hidden one. It runs
the same `ExecutionFirewall` over the same `RedemptionRegistry` the in-process harness uses; a
gateway with its own friendlier admission logic would be testing something other than what ships.

**Every assertion is on an external effect.** The governed system appends each operation it performs
to its own log file, and the tests read that file. No test in `tests/test_p4.py` asserts on a return
value from the code under test — which is Part VI §29.4's distinction, applied to the demonstrator
itself. The direct attempt fails with `ENOENT` inside `connect(2)`, before any of the project's code
runs. A missing ECC, a substituted subject, an out-of-scope operation, an expired ECC and a replay
each leave the log untouched; a valid ECC produces exactly one entry; and one test states the
property over a mixed run — the log length equals the number of admissions.

**NT-001 and NT-003 now exist in a form in which they could fail.** They could not before.

**Still open, and it is the half that matters to an adopter.** This is process isolation obtained by
not naming a socket. It is not a network policy, and this page will not call it one. A deployment has
named endpoints and must obtain the same property from a network namespace, a security group or a
service-mesh authorization policy — and must demonstrate it the same way: attempt the direct path,
watch it fail at the network layer, and read the target's own log. Until a deployment does that and
publishes the result, what is demonstrated is that **the mechanism can be demonstrated at all**,
which is a smaller claim than P4 and is the one this entry makes.

This is also the most useful thing a Pilot Implementer could contribute, and it is worth more coming
from them than from the project: see H-07.

### H-07 — The test suite is cooperative **· PARTLY CLOSED**

As audited: `make test` ran two test methods; `make demo` showed six scenarios, all calling the API in
the intended order with well-formed inputs. Nothing attempted forgery, mutation, subject
substitution, event tampering, orphan commitments, or concurrency.

**Partly closed.** The suite was sixteen tests at the September fix. It is now **56 tests across
nine classes**, and `make demo` runs **25 scenarios**, all passing: the adversarial group (forged
signatures, a forged-and-re-signed content address, mutated operations, subject substitution, deleted
and tampered events, orphan executions, double authorization, two 100-thread races), the shared
registry including an **8-process** compare-and-swap race, the Appendix R write-ahead log, the
reference negative tests NT-001 to NT-008, event **and ECC** schema conformance against this
repository, and the nine-test P4 boundary bench, which is the only group whose assertions are on an
effect outside the process under test.

**Still open, and one degree worse than described.** Every one of those tests is still written by the
project, against its own artifact. H-08 is what that costs: a green adversarial suite, cited as
evidence that H-01's class was closed, while the same class was reachable one enforcement instance
away. The suite tested the property it was written for and was blind to the one beside it. An outside
attempt would start at H-05 and H-06, and the ECC half of H-03 is now the cheapest place for it to
find something.

---

## Where each reference negative test actually stands

| Test | Claimed | State | Verdict |
|---|---|---|---|
| NT-001 non-CC blocked | yes | since 7 September, asserted against a **governed system in another process**: the direct path fails in `connect(2)`, the system's own log stays empty, and a valid ECC produces exactly one entry | holds against an external effect |
| NT-002 expired CC | yes | correctly blocked | holds in the mock |
| NT-003 replay | yes | sequential replay blocked, a 100-thread race admits exactly one, and the replay is now also refused at the process boundary with the governed system performing the operation **once** | holds against an external effect |
| NT-004 unknown context | yes | `C3` blocks before `C2` | holds in the mock |
| NT-005 ambiguous E3 | no | present since 7 September 2026 — pinned analyzer, `AMBIGUOUS` verdict, fail-deny, checked against the nine criteria Appendix Q states | holds in the mock |
| NT-006 trajectory | no | present since 7 September 2026 — `C4` keeps trajectory state, the alert is emitted after the fifth permit and before the sixth decision, and the cumulative total is reconstructed out of `C5` rather than read from the counter that produced it | holds in the mock |
| NT-007 governed exception | replay only | replay blocked; double pre-compilation refused at `C7`; **scope widening now refused**, and the exception scope is enforced independently of the permit scope (§4.3.1) | holds in the mock |
| NT-008 authority non-expansion | no | delegation present (Appendix L, D1–D5); clause (a) tested on all five scope dimensions, clause (b) on four laundering routes | holds in the mock |

---

## Exit criteria

The harness should not be described as a reference for CROA behaviour until all of the following hold
at once. **Five of eight are met outright, three are partly met, and none is untouched** — the
count is written this way because "partly met" is where a reader is most likely to be misled.

| | Criterion | State |
|---|---|---|
| ☑ | zero validation errors against the canonical schemas | met — 13 events and 2 ECCs validated on the merged harness, zero errors, both gated in CI (H-03) |
| ☑ | NT-001 to NT-007 complete, including concurrency and scope widening | met in the demonstrator — NT-001 now asserts on an unreachable path and an external effect, NT-003 likewise, and NT-005 to NT-008 exist |
| ☑ | exactly one admission for N concurrent presentations of the same commitment or authorization | met across processes (H-01, H-08); across hosts it is delegated, not demonstrated |
| ☑ | subject and action substitution always refused | met (H-02) |
| ☑ | a `C5` verifier conformant to G.2.4 that rejects every negative log | met for the negative logs tested (H-04) |
| ◐ | a direct network path to the governed system that is technically unreachable | **partly met** — the direct path is unreachable and fails in `connect(2)`, but because no address exists, not because a network policy forbids it. A deployment must obtain and show the same property from network controls (H-06) |
| ◐ | required, reproducible CI on a protected commit | **partly met** — CI runs the full suite on every push and pull request across Python 3.8–3.13, plus schema conformance against this repository; the harness repository still has no ruleset, so the commit is not protected |
| ☐ | an immutable release bound to a specific specification version | **not met** (erratum E-14) |

Until all eight hold, it is a demonstrator of the *mechanism*, with the gaps above.

---

**Related.** [`docs/limitations.md`](../docs/limitations.md) (evidence base) ·
[`properties.md`](properties.md) (what the specification claims) ·
[`errata-v1.0.md`](errata-v1.0.md) (defects in the published draft) ·
[`../GOVERNANCE-DEVIATIONS.md`](../GOVERNANCE-DEVIATIONS.md) (where the project did not follow its own process)
