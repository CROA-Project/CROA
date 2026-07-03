# CROA Ecosystem Roadmap

**This is an ecosystem roadmap, not a feature backlog.** It describes how CROA earns its way from a published draft to (potentially) a recognized standard — through evidence and community, not assertion.

**Every phase is gated on outcomes, not dates.** We will not advance a phase until its exit criteria are met, and we will say so publicly. Live status is on the Roadmap project board.

> Guiding test for every step: *would Kubernetes / OpenTelemetry / OpenAPI / The Open Group do this?* If not, we don't.

---

## Phase 1 — Public Review  *(current)*

**Objective:** subject CROA to serious, independent scrutiny and the first real implementations.

**Deliverables:** public repository (this); runnable Minimal Reference Harness; Public Review Program; open research questions; RFC process; seeded reviewer cohort.

**Exit criteria:**

- The harness runs cleanly for outside users and produces a verifiable `C5` log.
- Independent challenges to the central claim have been filed and addressed in public.
- ≥ 3 independent evidence reports exist, **including at least one partial/failed implementation**.
- A v1.0 final draft incorporating validated findings is released (with DOI).

## Phase 2 — Pilot Implementations

**Objective:** accumulate enough real-world implementation evidence to know where CROA holds, where it is too costly, and where it must change.

**Deliverables:** a public Implementations & Evidence index; benchmark data (RQ-5/6); pilot reports across ≥ 2 sectors; an FAQ/known-issues set derived from pilots.

**Exit criteria:**

- ≥ 5 independent evidence reports across ≥ 3 organizations.
- Performance, friction, and dependency questions (RQ-3 to RQ-8) have evidence-backed answers, even if the answer is "costly under condition X."
- Recurring findings folded into the spec via RFCs.

## Phase 3 — Community Validation

**Objective:** establish that the architecture is understood, implementable, and assessable consistently by people who didn't write it.

**Deliverables:** reviewer pool spanning ≥ 5 organizations; community calls and notes; independent conformance-assessment trials; a stabilized conformance model validated against real deployments (RQ-13).

**Exit criteria:**

- Multiple independent parties reach the same conformance assessment of the same deployment.
- An active review board with multi-organization representation.
- Demonstrated demand beyond the founding circle (issues, pilots, citations from independents).

## Phase 4 — Reference Implementations

**Objective:** more than one credible, independently-built implementation of the CROA Core Profile.

**Deliverables:** ≥ 3 independent implementations (built by separate organizations); interoperability/evidence-format alignment; a conformance test suite beyond the minimal reference negative tests.

**Exit criteria:**

- ≥ 3 independent Core-Profile implementations, verified against the conformance suite.
- A shared, machine-checkable conformance test corpus.

## Phase 5 — Industry Adoption

**Objective:** real production deployments and recognition by adjacent communities and standards bodies.

**Deliverables:** documented production adoptions; mappings maintained against evolving regulation and adjacent standards; conference and working-group presence.

**Exit criteria:**

- Production deployments reported by independent organizations.
- CROA referenced or adopted in adjacent ecosystem/standards conversations on its merits.

## Phase 6 — Conformance Program

**Objective:** a neutral, credible way to make and verify a "CROA-conformant" claim.

**Deliverables:** a published conformance process; a neutral assessment path (self-declared + evidence during this phase, moving toward independent verification); a public registry of conformance claims.

**Exit criteria:**

- Conformance claims are verifiable by parties that did not build the system.
- A documented, repeatable assessment process exists and has been exercised.

## Phase 7 — Foundation

**Objective:** transfer stewardship to an independent, vendor-neutral foundation (see `GOVERNANCE.md` §5, Phase C).

**Deliverables:** a ratified open-governance charter; a Technical Steering Committee with no single-employer majority; trademark and conformance administered neutrally; contribution of the spec and marks to an established neutral home.

**Exit criteria:**

- A functioning TSC and sustained multi-organization contribution.
- Neutral administration of trademark and conformance.
- Adoption maturity sufficient to sustain independent governance.

## Phase 8 — Certification *(aspirational)*

**Objective:** if and only if the ecosystem warrants it, an independent certification regime administered by the foundation.

**Exit criteria:** market demand for formal certification; a neutral certification authority; an accredited, repeatable assessment standard.

---

### Principles that hold across all phases

- We never *claim* "standard" status; adopters and standards bodies confer it.
- We publish negative results on our own initiative.
- No implementation — commercial or otherwise — receives privileged standing.
- Advancement is announced with the evidence that justified it.
