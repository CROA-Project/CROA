# CROA RFC Process

**Objective:** give every substantive change to CROA a single, transparent, evidence-based path — so the framework evolves in public and no requirement changes silently.

**Audience:** anyone proposing a change to the specification, schemas, conformance model, or governance.

The RFC (Request for Comments) process is how CROA makes **normative** decisions. It is deliberately lightweight — modeled on the conventions that worked for Rust, Kubernetes (KEPs), and React — but tied to CROA's own change-classification scheme.

---

## When you need an RFC

| Change | RFC required? |
|---|---|
| Typo, broken link, formatting | No — open a PR |
| Clarification that changes **no** requirement | No — PR (label `change-level:clarification`) |
| Correcting a defect in a normative requirement | **Yes** |
| Adding, removing, or altering a requirement, schema field, or conformance criterion | **Yes** |
| Changing the central claim or a tenet | **Yes** |
| New appendix, profile, or mapping (extension) | **Yes** |
| Governance changes | **Yes** (longer comment period) |

Every RFC declares its highest **change level** (Part VII §31.3): *Editorial · Clarification · Normative correction · Normative change · Extension.*

## Lifecycle

```text
Pre-Discussion  →  Draft RFC (PR)  →  Review  →  Final Comment Period  →  Decision  →  Implementation
   (optional)        rfcs/text/         open        ≥14 days (≥21 gov.)     accepted /
                                                                            rejected
```

1. **Pre-Discussion (recommended).** Float the idea in *Discussions → RFC Pre-Discussion*. Cheap to do, saves rework.
2. **Draft.** Copy [`0000-template.md`](0000-template.md) to `rfcs/text/0000-my-proposal.md` (keep `0000` until a number is assigned) and open a pull request. The PR *is* the RFC discussion.
3. **Review.** Maintainers and reviewers comment in the open. The author updates the RFC; substantive objections must be addressed or explicitly noted as unresolved.
4. **Final Comment Period (FCP).** When discussion converges, a maintainer proposes a disposition (accept / reject / postpone) and opens an FCP of **≥14 days** (**≥21 days** for governance). The FCP is announced in *Announcements*.
5. **Decision.** At FCP end, maintainers record the outcome and a one-paragraph rationale. Accepted RFCs are merged into `rfcs/text/` with a number and a `status: accepted` field; rejected RFCs are merged too, marked `rejected`, so the reasoning is preserved.
6. **Implementation.** A tracking Issue links the RFC to the spec/schema/harness changes that realize it. The RFC is `implemented` once those land and ship in a release.

## Decision rule (Public Review phase)

- Maintainers hold final authority during Public Review.
- Maintainers commit **not to override a clear reviewer consensus without a written, public rationale.**
- **Evidence outweighs opinion:** a pilot/evidence report demonstrating a problem carries more weight than an unsupported preference. Cite evidence where it exists.
- Reviewer votes during FCP are advisory in this phase and become binding under the Technical Steering Committee (see [`GOVERNANCE.md`](../GOVERNANCE.md) §5).

## What makes a strong RFC

- A crisp problem statement grounded in a real implementation difficulty, ambiguity, or counter-example.
- The **change level** stated honestly.
- Backward-compatibility and migration impact addressed.
- Alternatives considered (including "do nothing").
- Where possible, a reference to evidence (an Issue, a pilot report, a failing test).

A good RFC can be *rejected* and still be valuable: it documents a path the project chose not to take, and why.

## Index

Accepted and rejected RFCs live in [`rfcs/text/`](text/). Each carries a status field. RFCs currently in a Final Comment Period are surfaced by the `status:in-review` label (and on a project board once one is opened).
