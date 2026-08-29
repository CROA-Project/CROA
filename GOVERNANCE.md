# CROA Governance

**Objective:** make it unambiguous *how decisions are made, by whom, and where the project is heading* — so that participants can trust that CROA evolves through evidence, in the open, and is not controlled by any single commercial interest.

**Audience:** contributors, reviewers, pilot implementers, prospective adopters, and any organization evaluating whether to depend on CROA.

This document is itself governed by the [RFC process](rfcs/README.md): changing it requires an RFC.

---

## 1. Principles

These principles bind the maintainers and survive any change of stewardship.

1. **Vendor neutrality.** CROA is implementation-agnostic. Conformance never requires a specific product. No commercial entity receives privileged influence over the specification.
2. **Evidence over opinion.** Normative change is justified by implementation experience, reproducible tests, or demonstrated defects — not by authority or preference.
3. **Transparency by default.** Decisions, rationales, and dissent are recorded in public (Issues, RFCs, discussion threads, community-call notes).
4. **Falsifiability.** CROA's central claim is stated conditionally and is open to challenge. Refutation is a first-class contribution.
5. **Backward-compatible humility.** During Public Review the specification may change materially. Changes are classified by impact and announced; nothing is changed silently.

## 2. The neutrality commitment

CROA is an architecture, not a product. Anyone may build an implementation of it.

The maintainers commit that:

- CROA is and remains **independent of any commercial product.**
- Conformance to CROA **never requires any specific implementation.**
- No implementation receives **privileged standing** in the specification, the RFC process, or conformance criteria — regardless of who builds it.
- The only implementation hosted by the project is the **vendor-neutral Minimal Reference Harness**, whose purpose is to let anyone run and verify the architecture's behavior, not to be a production tool.

If at any point an implementation and the specification diverge, **the specification governs**, and the divergence is treated as either an implementation defect or an RFC-worthy question — decided in the open.

## 3. Roles

| Role | Who | Responsibilities |
|---|---|---|
| **Maintainers** | The founding authors during Public Review | Final decision authority on merges and RFC outcomes during this phase; triage; release management; upholding these principles. |
| **Core Team** | Sustained contributors to the specification, invited by the maintainers | Work on the specification, threat model, method and conformance material alongside the maintainers. No final decision authority: merges and RFC outcomes remain with the maintainers during Public Review. |
| **Reviewers** | Practitioners admitted via the [Public Review Program](public-review/README.md) | Review RFCs and findings; vote in final-comment periods (advisory during Public Review). |
| **Pilot Implementers** | Teams running CROA against real systems | Produce evidence reports; their findings carry special weight in normative decisions. |
| **Contributors** | Anyone | Open issues, discussions, RFCs, evidence, documentation, harness code. |
| **Technical Steering Committee (TSC)** | *Formed at the foundation transition (§5)* | Multi-organization body that assumes specification authority from the maintainers. |

Maintainers are listed in `MAINTAINERS.md`. The current maintainers are the framework's founding authors. Core team members are listed in `CORE-TEAM.md`.

## 4. How decisions are made

```text
idea → Discussion (RFC Pre-Discussion) → RFC (rfcs/) → review + Final Comment Period → decision → implementation
```

- **Routine changes** (typos, clarifications that change no requirement, documentation, harness fixes) are handled by pull request and maintainer review. No RFC required.
- **Normative changes** (anything that alters a requirement, a conformance criterion, a schema, or the central claim) **require an RFC** and a Final Comment Period of no less than 14 days.
- **Change classification** follows the specification's own scheme (Part VII §31.3): *Editorial · Clarification · Normative correction · Normative change · Extension.* Every RFC and every release states the highest change level it contains.
- **Decision record.** Every accepted or rejected RFC retains its discussion and a one-paragraph rationale. Dissent is recorded, not erased.

During Public Review, maintainers hold final authority but commit to **not overriding a clear reviewer consensus without a written, public rationale.**

## 5. Progression to a vendor-neutral foundation

CROA's long-term objective is stewardship by an **independent, vendor-neutral foundation** (e.g., a Linux Foundation / OASIS-style home). This transition is **gated on demonstrated maturity, not on a date.** The maintainers will initiate it only when the project can credibly sustain neutral governance.

**Phase A — Founder stewardship (current).** Maintainers steward the project through Public Review. Goal: a stable v1.0, a working reference harness, and an active review community.

**Phase B — Shared stewardship.** A Technical Steering Committee is formed with representation from **multiple independent organizations** (no single employer holding a majority). Maintainers transfer specification authority to the TSC. Entry gate — *all* of:

- ≥ 3 independent implementations of the CROA Core Profile, built by separate organizations;
- ≥ 5 published pilot/evidence reports from independent teams;
- an active reviewer pool spanning ≥ 5 organizations;
- a ratified, written charter and a public conformance process.

**Phase C — Foundation.** The project, marks, and specification are contributed to an established neutral foundation under an open governance charter; trademark and conformance certification are administered neutrally. Entry gate: a functioning TSC, sustained multi-organization contribution, and demonstrated adoption beyond the founding circle.

Progress against these gates is tracked publicly in [`ROADMAP.md`](ROADMAP.md) (and, once the public review opens, on a GitHub project board linked from there). The maintainers will not claim "industry standard" status; that designation, if it ever comes, is conferred by adopters and standards bodies — not asserted by us.

## 6. Trademarks and conformance claims

During Public Review, "CROA-conformant" is a claim a deployment may make only against the published conformance criteria (Part VI) and only at L4 or above, with evidence. The maintainers do not yet operate a certification program; until a neutral conformance authority exists (Phase C), all conformance claims are **self-declared and evidence-backed**, and must be presented as such. Claims-usage rules are in Part VII §33.

## 7. Changing this document

Amendments to governance follow the RFC process and require a Final Comment Period of no less than 21 days. The neutrality principles (§1, §2) are intended to be durable; weakening them requires explicit, public justification and broad reviewer support.
