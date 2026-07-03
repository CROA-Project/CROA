# External prerequisites and load-bearing dependencies

**Objective:** name honestly the things CROA's guarantee *depends on* but does **not** itself provide —
so no one discovers them mid-pilot. Two are load-bearing enough to make or break adoption: **agent
identity** and a **sufficiently complete Technical Golden Record.**
**Audience:** architects and decision-makers pressure-testing feasibility.
**Authoritative source:** Part I §1.3 (scope/assumptions), Part II (C3), research questions RQ-7 and RQ-2.

---

## 1. Agent identity is an external, not-yet-standardized prerequisite

CROA's admission stage authenticates an agent as a subject (identity → RBAC eligibility → qualification
→ runtime policy). The guarantee assumes **you can reliably identify the acting agent.** CROA
deliberately does *not* define how — and today, that primitive is **still in motion across the industry**:

- **Workload identity / SPIFFE-SPIRE** — strong for service-to-service, but "which *agent instance*,
  acting on whose behalf, under what delegated scope?" is not fully solved.

- **OAuth token exchange / on-behalf-of flows for agents** — evolving; delegation semantics for
  autonomous agents are not standardized.

- **Model/agent-platform identity** — vendor-specific and non-portable.

**Treat agent identity as an external dependency at risk**, not a solved substrate. Practical guidance:

- For a pilot, pin to whatever identity your platform already issues (mesh workload identity, an OIDC
  client per agent) and **document its limits** — especially delegation and impersonation resistance.

- Record the identity primitive you relied on in your evidence report; it is a first-class finding.
- Watch this space: as agent-identity standards converge, the admission stage gets stronger for free —
  but the CROA guarantee is only ever as strong as the identity feeding it. If identity can be spoofed,
  the boundary is enforcing rules for the wrong principal.

> This is a genuine open dependency, related to research question **RQ-2** (how much of the action
> surface can be reliably attributed and modeled).

## 2. The Technical Golden Record: the real bet

C3 grounds every request against the **Technical Golden Record** — the registry of legitimate endpoints,
resources, and entities. The structural guarantee is conditioned on that registry being **sufficiently
complete and maintained.** For most enterprises the nearest existing asset is a **CMDB / service catalog
— and most CMDBs are wrong** (incomplete, stale, 60%-accurate on a good day). The framework says so
plainly (research question **RQ-7** calls the Golden Record "notoriously incomplete").

Be clear-eyed about what this means:

- **This is arguably the framework's biggest practical risk — more than the central claim.** The claim
  is sound; the question is whether you can feed C3 a registry good enough to make it useful without
  blocking legitimate work.

- **An incomplete Golden Record fails in one of two directions.** Under fail-closed, a missing-but-legitimate
  target is *denied* (friction); if you relax grounding to reduce friction, you reopen the gap. Both are
  visible and measurable — which is the point.

### The pilot answer vs. the scale answer

- **Pilot (defensible today):** scope the Golden Record to the pilot's targets only. For one action class
  against a handful of known systems, a complete-enough registry is achievable by hand. This is the
  recommended path and it works.

- **Scale (the open story):** how a complete-enough Golden Record is built and *kept* current across a
  whole enterprise is **not yet answered** — it is exactly what pilot evidence (RQ-7) is meant to
  establish. Do not assume it generalizes from the pilot for free. Candidate strategies to test and
  report on: derive the registry from IaC / service-catalog / mesh service registry as the source of
  truth rather than a hand-maintained CMDB; treat "unregistered" as a triaged event stream that *grows*
  the registry rather than a silent deny; measure completeness over time as a first-class metric.

If your CMDB is the plan for C3 at scale, treat that as the highest-risk assumption in your adoption
and design the pilot to test it directly.

## 3. The other assumed layers (named for completeness)

- **Network-enforced containment (P4).** The boundary assumes governed systems accept *only*
  commitment-derived operations. In real topologies with shadow paths and legacy integrations this must
  be verified, not assumed (research question **RQ-8**). See [`deployment-topologies.md`](deployment-topologies.md).

- **Isolation / sandboxing.** CROA realizes P4 *on top of* your network policy and workload isolation;
  it does not replace them (see [`mapping-to-your-stack.md`](mapping-to-your-stack.md)).

- **A tier-0 audit store.** C5's availability is coupled to the systems it governs — see [`operating-c5.md`](operating-c5.md).

## Why this list is here, not hidden

A framework that lists its load-bearing dependencies is more trustworthy than one that pretends the hard
parts are solved. None of these is an architectural flaw — they are the honest boundary of what CROA
supplies versus what it consumes. Bring findings on any of them: an evidence report on Golden-Record
completeness, or on agent-identity limits you hit, is among the most valuable contributions to this
review (see [`../evidence/README.md`](../evidence/README.md)).
