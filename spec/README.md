# The CROA Specification

**The citable, authoritative version of the CROA specification is the Zenodo release:**

> DOI: [`10.5281/zenodo.21063423`](https://doi.org/10.5281/zenodo.21063423) · Record: <https://zenodo.org/records/21063423>
> Cite this for any reference to CROA. This DOI resolves to the published Public Review Draft; when Zenodo mints a version-independent *concept* DOI for the series, cite that instead so links always resolve to the latest version.
>
> **A note on the name.** The project operates as **The CROA Project** — the repository, the Zenodo record, and all materials use that name. "Foundation" is reserved for a future independent entity, not yet incorporated. One historical trace remains: the **front-matter text inside the v1.0 PDF** still carries the earlier working name "CROA Foundation" (the dated record is left as published rather than re-rendered). It refers to the same group and the same work.

## Where the specification lives

The full framework — Front Matter, Parts I–VII, and Appendices A–S — is
**published on Zenodo** at the DOI above. That dated record is the single source of truth;
this repository deliberately does **not** carry its own copy of the prose, so there is nothing
here to drift out of sync with the citable release.

> 📄 **Read the specification:** [https://doi.org/10.5281/zenodo.21063423](https://doi.org/10.5281/zenodo.21063423)

A line-by-line Markdown mirror of the specification is **not** published in this repository for
the v1.0 review cycle either. To keep citation friction low, the specification's **stable
identifier scheme** (every Part, component, level, appendix, and reference test) is mirrored in
[`identifiers.md`](identifiers.md), so an issue or RFC can point to *Part VI §29.5* or *Appendix Q*
precisely.

## Errata and normative properties

Two companion pages live here because the Zenodo record is dated and is not re-rendered:

- [`errata-v1.0.md`](errata-v1.0.md) — defects found in the published draft, each with the reading
  that governs until the next version. It covers normative conflicts (notably that Part IV defines
  **seven** deployment properties, P1–P7, while three other sections still say six), claim-hygiene
  corrections, and two coverage gaps that public review should treat as open.
- [`properties.md`](properties.md) — CROA's claim-bearing properties written so they can be attacked:
  claim, preconditions, invariant, enforcement mechanism, falsifying test, evidence produced, and
  what each does **not** establish. It also lists, explicitly, the properties CROA does *not* have.

## Machine-readable schemas

The specification's machine-readable JSON schemas **are published here**, in
[`schemas/`](schemas/), so implementers and tests can validate against them directly and propose
changes by PR against the actual files:

- [`cc.schema.json`](schemas/cc.schema.json) — the Compiled Commitment (CC), including the
  governed-exception fields `cc.decision_basis`, `cc.auth_ref`, and `cc.exception_scope` (§4.4.1).
- [`event.schema.json`](schemas/event.schema.json) — the append-only `C5` governance event.
- [`gar.schema.json`](schemas/gar.schema.json) — the Governed Action Request submitted at the Agent Surface.
- [`gga.schema.json`](schemas/gga.schema.json) — the Grounded Governed Action produced by C3.

In any discrepancy between a schema file and the normative prose on Zenodo, the specification
(Part II §4.4.1 and the referenced sections) governs; corrections flow through the RFC process.

Proposed corrections and changes to the prose are handled through the
[RFC process](../rfcs/README.md) and cite the numbered Parts/Chapters/§ of the Zenodo document.
Substantive challenges to the central claim go to **Discussions → Challenge the Claim**;
ambiguities and conformance gaps go to [Issues](../.github/ISSUE_TEMPLATE).

## How to reference a specific requirement

Cite by the framework's own stable identifiers rather than page numbers (full list in [`identifiers.md`](identifiers.md)):

- **Parts and chapters** — e.g., *Part II §12.3*, *Part VI Chapter 28*.
- **Components** — C1–C7 (e.g., "C6 Execution Firewall").
- **Conformance levels** — L0–L5 (L4 is the conformance threshold).
- **Appendices** — by letter (e.g., *Appendix Q* for the evidence pack and reference negative tests). The published v1.0 record carries NT-001–NT-007; NT-008 (authority non-expansion) is added in the next version — see [`errata-v1.0.md`](errata-v1.0.md) E-02 and E-12. The [reference harness](https://github.com/CROA-Project/croa-reference-harness) implements **NT-001–NT-004** (the mechanically checkable boundary tests) and the replay half of NT-007; NT-005 (ambiguous E3), NT-006 (trajectory), NT-007's scope-widening and concurrency steps, and NT-008 (delegation) are left as contributed extensions. Per-test status is in [`identifiers.md`](identifiers.md).

These identifiers are stable across editions, so a comment or RFC that cites "Part VI §29.5" stays valid even as pagination changes.

## Reading order

New readers should **not** start here. Start with [Why CROA](../docs/why-croa.md) and the one-page [Architecture Overview](../docs/architecture-overview.md), then come here for the precise requirements.

- **Implementers:** Part II (components C1–C7), Part IV (deployment models), Appendix G (reference-implementation pattern), and the machine-readable schemas referenced in Appendix Q.
- **Assessors / auditors:** Part VI (conformance and maturity), Appendix Q (evidence pack & reference negative tests).
- **Security / risk:** Part I §0–§1.3, Part V (threat model), Appendix O (CROA and adjacent enforcement mechanisms).
- **Executives / governance leaders:** the Front Matter reading map, Part I §0 ("CROA in One Page"), and Part VII (governance).

## Try it

To see the enforcement behavior and the audit model in action, clone the vendor-neutral reference harness and run the reference negative tests:

- [`CROA-Project/croa-reference-harness`](https://github.com/CROA-Project/croa-reference-harness) — pure-Python, no commercial software, ≤15 minutes (see [`docs/quick-start.md`](../docs/quick-start.md)).
