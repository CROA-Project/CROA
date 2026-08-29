# Limitations, residuals, and the state of the evidence

**Objective:** put in one place everything CROA does not do, does not prove, and has not yet shown —
so that a reviewer does not have to assemble it from seven Parts and nineteen appendices.

**Audience:** anyone deciding whether to trust, pilot, or challenge CROA.

**Authoritative source:** the specification. This page consolidates statements that are already
normative or already disclosed there; where it and the spec differ, the spec governs. Nothing here is
a new concession — the point is that it should be *findable*.

---

## 1. What the central claim does not cover

The T1 guarantee is conditional and the conditions are load-bearing:

> *Within the modeled action space, under the registered invariant set, and given network-enforced
> execution-boundary containment (P4), no sequence of governed actions reaches an
> invariant-violating state except through a valid authorization.*

Part VI §28.6 states the five things an L4 conformance claim explicitly does **not** assert. In short:
not the semantic safety of a permitted action's content; not the completeness of the enterprise's
invariant registry; not effects through channels outside the modeled boundary; not exactness of
approximated (`E3`) evaluations; and nothing transitive to another deployment, model version, or
configuration.

**A further honesty note about the formalism.** Part I §2.5 models the governed system as a
constrained state machine and defines structural unreachability over it. That section is
**informative**, and it contains no theorem: unreachability there is *defined* in terms of the
enforcement logic rather than *derived* from it. The claim CROA makes is that a conformant deployment
exhibits the property and can demonstrate it from evidence — not that the property has been proved.
A reviewer is entitled to hold CROA to that distinction, and should compare the claim against
Schneider's characterisation of monitor-enforceable policies (TISSEC 3(1), 2000) and against systems
where mediation is machine-checked (seL4). CROA is not in the latter category.

## 2. Properties CROA does not have

Set out with their tracking references in [`spec/properties.md`](../spec/properties.md). Summarised:

| Not established | Consequence |
|---|---|
| **Cumulative-state consistency under concurrency** | Two actions evaluated concurrently against the same `TP-C`/`TP-X` aggregate carry distinct commitments, so the §4.8 redemption CAS does not relate them; both may be admitted against the same pre-increment total and jointly cross a threshold. v1.1-draft adds a minimum per-accumulation-key serialisation requirement; general serializability is **not** claimed. (RQ-16) |
| **Commit-time authorization freshness** | A commitment stays redeemable until expiry (default ≤24h). At redemption `C6` re-checks the invariant *registry* version, not the runtime trajectory state or the policy-artifact version. (RQ-17) |
| **Trap-state freedom** | A permitted action may lead to a state from which every continuation is denied. Safety is preserved; liveness is not, and the operational pressure to unblock is real. Not modelled. (RQ-18) |
| **Resource, cost, and token budgets** | Not governed quantities in v1.0. An enterprise may register spend as a `TP-C` invariant; nothing requires it and no reference test covers it. (RQ-19) |
| **Irreversibility as a trajectory dimension** | R0–R4 sets the bar for a *single* transition and is used by no trajectory profile. Twenty reversible effects and twenty irreversible ones accumulate identically. (RQ-20) |
| **Cross-agent trajectory detection** | `C4`'s scope is per-session, and per-subject for `TP-X`. Cross-session analysis is OPTIONAL; cross-agent state exists only inside one orchestrated delegation session (Appendix L D4). Two cooperating agents under distinct identities, outside a delegation chain, are outside `C4`'s default scope — while TH-7 (path composition) is claimed as mitigated by `C4`. This is the sharpest scope gap in the framework. (RQ-10) |
| **Capture completeness of the evidence record** | The hash chain proves ordering and non-alteration of what was written. That everything was written follows from the I6/I6.1 fail-deny gate and is corroborated by external anchoring and the §29.4(c) cross-checks — it is an architectural assumption, verifiable by cross-check, not a cryptographic result. |

## 3. Dependencies CROA consumes but does not provide

Detailed in [`prerequisites.md`](prerequisites.md). The two that most often decide whether a pilot
works:

- **Agent identity.** CROA authenticates a subject; it does not mint one, and workload identity for
  agents is still standardising. The guarantee is only ever as strong as the identity feeding it.
- **The Technical Golden Record.** `C3` grounds every request against a registry the framework itself
  calls notoriously incomplete in real enterprises. An incomplete registry either blocks legitimate
  work or leaves gaps, and the friction it produces is what drives the governance-erosion loop
  (Part V §26). Its construction and maintenance is the least-bounded cost of adoption. (RQ-7)

And one operational consequence worth stating plainly: because governance is fail-closed with a
synchronous durable evidence write, **`C5` is tier-0 infrastructure** whose availability must match
the most critical system it governs. See [`operating-c5.md`](operating-c5.md). (RQ-6, RQ-15)

## 4. The state of the evidence

Classified honestly. Five of seven buckets are empty.

| Evidence type | Status |
|---|---|
| **Author-controlled testing** | Present. The Minimal Reference Harness (four reference negative tests over a self-contained mock), the CROA-Bench seed and its three rule-based mock adapters, and the founding comparative study. |
| **Reproducible testing** | Partially present. The harness and CROA-Bench are deterministic and runnable on a clean machine — but what reproduces is authored fixtures and mock behaviour, not system behaviour. Reproducible is not the same as informative. |
| **Adversarial testing** | **Empty.** No red-team result exists. Nothing has yet tried to forge a commitment, mutate one after compilation, tamper with an event and observe chain verification fail, or drive concurrent redemption. |
| **Independent replication** | **Empty.** `evidence/reports/` is unpopulated. |
| **Multi-implementation validation** | **Empty.** No third-party implementation exists. |
| **Multi-domain validation** | **Empty.** Existing material is scoped to software-engineering and enterprise-action workflows. |
| **Enterprise / production validation** | **Empty.** No pilot has been executed. |

**On the founding study.** The comparative study behind the framework (Durand & Smith, forthcoming)
reports 51 runs across three adversarial scenario classes. It is directional validation of the
architectural thesis and of Technical Sycophancy as a phenomenon. It is **not** a conformance
assertion, and three limits apply: it was conducted by the framework's originators, not an
independent assessor; it evaluated the earlier four-layer model rather than the seven-component
control plane, the L0–L5 levels, or the RBAC/AQL admission model of this version; and its authors
characterise the results as directional, not statistically generalisable. It has no published venue
or DOI yet.

**On CROA-Bench.** Its reference adapters are rule-based mocks that score well by construction; the
repository says so in its own README, its results file carries `"illustrative": true` as a
machine-readable field, and its results directory states the numbers carry no weight as conformance
or comparative evidence. That labelling should be read as intended: the numbers are a demonstration
of the metric design, not a measurement of any system.

## 5. The experiments that would most change the picture

In descending order of value per unit of effort. Each is a genuine falsification attempt, not a
confirmation exercise.

1. **Adversarial red-team of the execution boundary.** Hand-construct a commitment bypassing `C7`;
   mutate a signature by one byte; alter the action after compilation; present a commitment issued
   for a different subject; tamper with an event and assert that chain verification fails. Today this
   exercises code paths that no test reaches.
2. **Concurrency test on redemption.** Drive N threads presenting the same commitment, and the same
   authorization, simultaneously; assert exactly one authorization. This tests the one concurrency
   property CROA actually claims (P-D), in the topology where it matters.
3. **Concurrency test on a cumulative counter.** The same, but two distinct commitments against one
   `TP-C` threshold. We expect this to *fail* against a naive implementation — which is the point:
   it is the fastest way to establish whether RQ-16 is a specification gap or an implementation
   pitfall.
4. **Authority non-expansion under delegation.** Present a delegation token that widens an action
   class, a target, a parameter constraint, or a validity window; assert fail-deny with no
   commitment compiled. This is property P-B, and it is currently asserted rather than tested.
5. **One real system under CROA-Bench.** Until one adapter is a real system rather than a fixture,
   every benchmark number is a property of the fixtures.

If you run any of these — especially if the result is unfavourable — an
[evidence report](../evidence/README.md) is the most valuable contribution this project can receive.
