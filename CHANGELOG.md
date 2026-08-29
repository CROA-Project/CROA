# Changelog

Release notes for the CROA corpus. Each release is also published to Zenodo with a version-specific DOI; cite the **concept DOI** (always resolves to latest). Change levels follow the specification's scheme (Part VII §31.3): *editorial · clarification · normative-correction · normative-change · extension.*

This file records **public releases**. Day-to-day edits live in git history; substantive changes are traced through [RFCs](rfcs/README.md).

> **Version naming (canonical).** One release, three surfaces: the **public label** is **v1.0 (Public Review Draft)**; the **editorial identifier** carried inside the corpus is **1.0.0-draft.3**; the **Git tag / GitHub Release** is **`v1.0.0-draft.3`** and the **Zenodo** deposit is version **v1.0** at DOI [`10.5281/zenodo.21063423`](https://doi.org/10.5281/zenodo.21063423). These all denote the same artifact.

## [Unreleased]

- Public Review ecosystem established: repository front door, governance, RFC process, Public Review Program, research questions, evidence framework.

### Pre-public-communication audit (2026-08) — *clarification · normative-correction · extension*

An adversarial pre-publication audit against the 2025–2026 literature on runtime governance of
agentic systems. Nothing in the seven-component architecture, the conditioned T1 claim, the
evaluability model, or the conformance ladder was changed. What changed is what CROA *says* about
itself, and one property it asserted piecewise without ever composing or testing.

- **Added `spec/properties.md`** — the claim-bearing properties (P-A…P-F) in
  claim → preconditions → invariant → enforcement → falsifying test → evidence → what it does *not*
  establish form, plus an explicit list of properties CROA does **not** have. Two are named
  deliberately narrowly: *Single-Use Authorization Consistency* (not "stateful authorization
  consistency") and *Decision Reconstructability* (not "evidence completeness").
- **Added invariant I8 — Authority Non-Expansion** (property P-B) and reference negative test
  **NT-008**. *Extension, additive.* Two clauses: **(a)** delegation attenuates — along any chain,
  authority is non-increasing from the authorizing subject; **(b)** no authority laundering — an
  action is admitted only if independently authorized for the subject that submits it, so a
  composition's reachable operations are the **union** of the participants' authorized sets, never a
  superset. Clause (a) is entailed by Appendix L D1 and D3 inductively; clause (b) by the §4.9.1
  admission predicate with T6, the no-widening rule on compilation, and the monotone execution
  surface. No component, artifact, or mechanism is introduced.
  An earlier draft of this branch stated the property as bounding a composition by its
  *least-authorized participant*. That was wrong — it would have forbidden delegation outright — and
  the correction is recorded in `spec/properties.md` P-B and in errata E-12 rather than dropped.
- **Added a minimum serialisation requirement for cumulative trajectory state** (Part II §4.6.3): the
  read-evaluate-increment cycle of a `TP-C`/`TP-X` aggregate is serialised per accumulation key.
  *Normative-correction.* v1.0 mandated atomic linearizable redemption at `C6` but specified no
  concurrency semantics for cumulative counters, so two concurrently evaluated actions carrying
  distinct commitments could jointly cross a threshold. General serializability is **not** claimed;
  the residual is declared (errata E-11, RQ-16).
- **Added `docs/prior-art.md` Part 2 — research prior art.** v1.0 compared CROA only to product
  categories and cited no research. It now cites the classical foundations it stands on (Anderson;
  Saltzer & Schroeder; Schneider; Miller; HRU; RFC 9162) and the contemporary agentic-governance
  literature, and states plainly which CROA properties are no longer differentiating.
- **Added `docs/limitations.md`** — consolidated limitations, residuals, and an honest classification
  of the evidence base (five of seven buckets empty).
- **Added `spec/errata-v1.0.md`** — thirteen defects in the published draft (E-01…E-13) with the
  reading that governs until the next version, including the P1–P7 enumeration conflict, the
  six-versus-seven negative-test count, and I1's omission of `C6`.
- **Rewrote unsupported evidential claims.** Part VI §29.5's bolded "empirically validated"; the
  quick-start's description of four mock assertions as "the minimum mechanical evidence that the key
  properties hold"; the README's "run the experiment"; RQ-14's "the harness proves it".
- **Rescoped unbounded novelty claims** in Part V §26 and Part I §1.5 to dated, citable statements.
- **New research questions RQ-16…RQ-20** — cumulative state under concurrency, commit-time freshness,
  trap states, resource budgets, irreversibility accumulation.

## [1.0.0-draft.3] — 2026-06 — Public Review Draft

- First public release of the full framework: front matter, Parts I–VII, Appendices A–S, machine-readable schemas.
- Published to Zenodo (DOI: [`10.5281/zenodo.21063423`](https://doi.org/10.5281/zenodo.21063423)); supersedes and expands the April 2026 working paper (`10.5281/zenodo.19846872`).
- Highest change level in this release: **extension** (new appendices and companion material) plus normative corrections from pre-publication review.

> Earlier internal revision history is preserved in the specification's own provenance and in git history.
