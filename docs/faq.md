# FAQ

The questions below are the ones we actually get asked first, in roughly the order a skeptical reader
asks them. Where the honest answer is "we don't know yet", it says so and points at the open research
question.

---

**Is CROA a standard?**
No — not yet, and we don't claim it is. CROA is a **Public Review Draft**: an open architectural hypothesis published for the community to test and challenge. "Standard" status, if it ever comes, is conferred by adopters and standards bodies, not asserted by us. See [`ROADMAP.md`](../ROADMAP.md).

**Is CROA tied to a company or product?**
No. CROA is **vendor-neutral and implementation-agnostic.** Conformance never requires any specific product. The only implementation the project hosts is a vendor-neutral reference harness for demonstration. The neutrality commitment is in [`GOVERNANCE.md`](../GOVERNANCE.md) §2.

**How is this different from guardrails or "Responsible AI"?**
Guardrails and behavioral alignment operate on what the model *does* — they *discourage* unsafe actions. CROA operates at the execution layer and aims to make unauthorized actions *unreachable*. A discouraged action is still possible; an unreachable one is not. CROA complements model-level safety; it does not replace it.

**Isn't "structurally unreachable" an overclaim?**
It would be, unconditioned. The claim is explicitly bounded: *within the modeled action space, under the registered invariants, and given network-enforced containment.* Outside those conditions CROA makes no claim. Testing whether those conditions are achievable in practice is exactly what the [research questions](../public-review/research-questions.md) and pilots are for.

**How is this different from LATTICE, AgentBound, "Policies on Paths", or the other 2026 runtime-governance work?**
It overlaps with all of them, and we say where. The short version: deterministic governance, execution gating, complete mediation, signed execution tokens, tamper-evident chains and trajectory monitoring are **not** CROA differentiators — that is the field's consensus as of mid-2026. What we think is distinctive is the evaluability classification of every registered invariant (E1/E2/E3, with `AMBIGUOUS` → deny and the ambiguity rate as a governed quantity), the utility–guarantee frontier as a recorded design obligation, the claim-scope discipline, the per-invariant trajectory profile with an L4 rule that refuses windowed analysis alone where accumulation is possible, and mandated atomic linearizable redemption across every enforcement instance. The full comparison, with citations, is in [prior art §2](prior-art.md#part-2--research-prior-art).

**What does the audit log actually prove?**
That the events it contains are in the order they were written and have not been altered — and, given a signing key held outside the agent's trust domain plus external anchoring, that they were not forged, and that a suppressed or truncated segment is detectable. It does **not**, by itself, prove that every governed action produced an event; completeness follows from the fail-closed gate and is corroborated by cross-checks against the governed systems' own logs. And a complete, verifiable record of a wrong decision is still a wrong decision — the log proves what happened, not that the policy was right. See [`spec/properties.md`](../spec/properties.md) P-E.

**What are CROA's biggest known holes?**
Cumulative state under concurrency (two actions evaluated at once against one budget — open in v1.0 as published, addressed by a per-accumulation-key serialisation requirement in the next version, and in neither case a claim of general serializability), cross-agent trajectory detection outside a delegation chain, no notion of a spend or token budget, and no use of the irreversibility classification in trajectory analysis. All four are stated with tracking references in [`limitations.md`](limitations.md) and as research questions RQ-16 to RQ-20.

**Does CROA require a specific tech stack?**
No. It defines logical components (C1–C7) and properties, not a product or language. You implement them however suits your environment; deployment models are in Part IV.

**What does it cost to adopt?**
We don't have enough public evidence yet — that's an open question (RQ-12). The dominant costs are building the Technical Golden Record, authoring invariants (especially E3 ones), and enforcing the execution boundary. Pilot reports will make this concrete.

**Won't this slow my agents down?**
Possibly; how much is an open question (RQ-5). Every action traverses a control path including a synchronous audit write. The framework discusses a high-performance pattern; real benchmarks are wanted.

**How is this different from my OPA policy engine plus an API gateway?**
OPA (or Cedar) is a natural implementation of **one** component — C2, the decision point. A bare policy decision is advisory unless something structurally stops the agent from acting on a "deny." CROA adds the compiled, single-use commitment and the boundary that admits only commitments (C7+C6), plus context grounding (C3), cumulative trajectory enforcement (C4), and a conformance-bearing audit chain (C5). See [CROA on your existing stack](mapping-to-your-stack.md).

**Where does each component actually run?**
On the topology you already have — centralized, federated, as a sidecar in your service mesh, behind your API gateway, or embedded in your agent platform. See the five reference [deployment topologies](deployment-topologies.md).

**What happens if C5 (the audit store) goes down?**
Governed agents stop — CROA is fail-closed by design, so a lost audit path means no execution. That makes C5 **tier-0 infrastructure** whose availability must match the systems it governs. This is a real operational cost we name explicitly, with sizing and mitigations, in [Operating C5](operating-c5.md) (and research questions RQ-6, RQ-15).

**The Technical Golden Record is basically my CMDB — and mine is incomplete. Doesn't that break the guarantee?**
This is the framework's biggest practical dependency, and we don't pretend it's solved (research question RQ-7). For a pilot, scope the registry to the pilot's targets only — that's achievable. The enterprise-scale story is an open question the pilots are meant to answer. Read [external prerequisites](prerequisites.md) before assuming C3 is "done."

**How does CROA identify an agent?**
It consumes an identity; it doesn't mint one. Agent identity (workload identity/SPIFFE, OAuth token exchange for agents) is an **external, still-standardizing prerequisite** — we flag it as a dependency at risk rather than assume it. See [external prerequisites](prerequisites.md).

**Can I use CROA today?**
You can read it, implement against it, and challenge it today. It is stable enough for evaluation and pilots, and explicitly **not** finalized — expect material change during review.

**Why was it published as a 300-page document?**
That's the full specification, on Zenodo, for citation and rigor. You should **not** start there — start with [Why CROA](why-croa.md) and the [one-page overview](architecture-overview.md). The depth exists so implementers and assessors have something precise to work from.

**How do I challenge or contribute?**
Read [CONTRIBUTING.md](../CONTRIBUTING.md). The most valuable contribution right now is an attempt to break the central claim, or a real (even failed) implementation report.

**What's the relationship to the April 2026 CROA paper?**
This framework supersedes and expands that earlier working paper (DOI 10.5281/zenodo.19846872); earlier drafts used the name "Cognitive RFC Orchestration Architecture."

**Wait — the acronym used to expand to something else. Isn't that a retrofit?**
Fair question, and the honest answer is: partly, yes. "CROA" was originally *Cognitive RFC Orchestration Architecture*, from the era when the central artifact was called an "RFC" (a Request for Change — unrelated to IETF RFCs). Two things changed and the name followed. The artifact was renamed the **Compiled Commitment** because "RFC" was actively confusing. And the claim the framework actually makes turned out to be about *reachability* — which execution states an agent can be made to reach — not about cognition, which the architecture deliberately does not model or trust. So the expansion became *Constrained Reachability Orchestration Architecture*. The acronym was kept because it was already in the citation record. You can hold this against us; what you should not conclude is that the current expansion is decorative — Part I §2.5 formalises reachability, and Invariant I1 is named for it. The change is disclosed in the specification (Part VI §29.5) and is why the founding study's title still says "RFC-Driven".

**Who is behind it?**
The founding maintainers (see [`MAINTAINERS.md`](../MAINTAINERS.md)) during Public Review, with a published path to an independent, vendor-neutral foundation as the project matures.
