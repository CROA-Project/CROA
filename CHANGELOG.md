# Changelog

Release notes for the CROA corpus. Each release is also published to Zenodo with a version-specific DOI. Zenodo has not yet minted a version-independent *concept* DOI for this series; until it does, cite the version DOI below. Change levels follow the specification's scheme (Part VII §31.3): *editorial · clarification · normative-correction · normative-change · extension.*

This file records **public releases**. Day-to-day edits live in git history; substantive changes are traced through [RFCs](rfcs/README.md).

> **Version naming (canonical).** One release, four surfaces. For the current release the **public label** is **v1.0.1 (Official Specification)**; the **editorial identifier** carried inside the corpus is **1.0.1**; the **Zenodo** deposit is version **v2** at DOI [`10.5281/zenodo.22310276`](https://doi.org/10.5281/zenodo.22310276), published 4 September 2026; the **Git tag / GitHub Release** is **`v1.0.1`**.
>
> ⚠️ **These four do not denote an identical artifact, and that is the one thing a reader must know.** The Zenodo deposit is the corpus as it stood on **3 September 2026**. The repository was repaired on **7 September**: the Creative Commons licence declaration, three semantic inversions, Part III §7.3, §7.4 and Chapters 9–11, and the `ecc.*` schemas all landed *after* the deposit was published. **The deposited PDF therefore still contains the defects this release repaired.** Cite the DOI for the immutable record; read `spec/` for the current text; and the difference between them belongs in [`spec/errata-v1.0.md`](spec/errata-v1.0.md), which is where the project said it would put exactly this.
>
> For the previous release: public label **v1.0 (Public Review Draft)**, editorial identifier **1.0.0-draft.3**, tag **`v1.0.0-draft.3`**, Zenodo version **v1.0** at DOI [`10.5281/zenodo.21063423`](https://doi.org/10.5281/zenodo.21063423).
>
> **Between v1.0 and v1.0.1 the label changes from *Public Review Draft* to *Official Specification*.** That is a claim about the document's stability, not about the evidence base, and the two should not be confused: [`docs/limitations.md`](docs/limitations.md) still classifies five of seven evidence buckets as empty, and [`spec/known-defects-harness.md`](spec/known-defects-harness.md) still records the reference harness as a demonstrator with five of eight exit criteria met. A stable specification is not a validated one.

## [Unreleased]

Nothing yet.

## [1.0.1] — 2026-09-07 — Official Specification

*Change level: normative-correction · normative-change · extension · editorial.* Implements
[the v1.0.1 normative-surface RFC](rfcs/text/0000-v1.0.1-normative-surface.md); the August audit
below ships as part of this release.

**The corpus now lives in this repository.** Front Matter, Parts I–VII and Appendices A–S are under
[`spec/`](spec/), reversing the v1.0 policy of keeping the prose off the repository: a correction can
now be proposed as a pull request against the actual text rather than described against a frozen PDF.
The Zenodo deposit remains the citable record of v1.0; `spec/` is the working baseline, and every
difference between them belongs in the errata.

### Repaired — *editorial*

A find-and-replace that retired the nine-phase development cycle had damaged the corpus. Sixteen
repairs, each declared with its rationale, of which three are worth naming:

- **The licence.** `CC BY 4.0` had become **`ECC BY 4.0`** in three places, including Part VII's own
  licence declaration. The framework was, as published, licensed under a licence that does not exist.
- **Three semantic inversions**, where the replacement gave the *old* model the *new* model's name,
  so the sentence asserted the opposite of what it meant.
- Welds, duplicated orphan blocks, a duplicated `event.chain_hash` table row, and a retired TOGAF
  phase-letter line.

### Added — Part III — *extension*

Part III had been replaced wholesale, 118 KB down to a 4 KB chapter pair, leaving twenty-four
cross-references from Parts I, II, IV, V, VI and Appendix H pointing at sections that no longer
existed — several inside MUST sentences. These are **new requirements, not a restoration**; the
nine-phase method is not coming back.

- **§7.3** separation of duties in the pipeline. Automating the lifecycle removes the review board;
  it does not remove what the review board provided.
- **§7.4** governance roles — Governance Architect, Policy Authority Representative, Compliance Lead,
  Operations — and their incompatibilities. Role assignments are governed content. Appendix A,
  Appendix M and Framework structure had named §7.4 as the normative home of the Governance Architect
  role; it had never existed.
- **Chapter 9** invariant registration and evaluability profiles: the registry entry, the `E3`
  obligations (pinned analyzer, declared budget, friction target), governance-boundary specification
  with documented architectural exclusions, action-surface sizing, the authorization-propagation
  contract.
- **Chapter 10** threat assessment and negative testing in the pipeline: the eleven threat classes as
  a version-controlled artifact, TH-1 assessed whatever severity it is given, `NT-001`–`NT-008` as a
  merge gate.
- **Chapter 11** governed change, deployment-model selection and rollback: the eight change types,
  declared operational parameters, rollback constraints, `E3` analyzer versioning under I2.

### Changed — schemas — *normative-change*

- **`cc.*` → `ecc.*`.** The retired *Compiled Commitment* vocabulary is renamed to *Execution Change
  Contract* throughout (§4.4.1): `cc.schema.json` → `ecc.schema.json`, `CC_COMPILED` →
  `ECC_COMPILED`, `CC_SIGNATURE_INVALID` → `ECC_INTEGRITY_INVALID`, `event.cc_id` → `event.ecc_id`,
  `event.emitter_signature` → `event.signature`. **This breaks any implementation built on `cc.*`.**
- Added the three effect-attestation event types `EXECUTION_COMPLETED`, `EXECUTION_FAILED` and
  `EFFECT_ATTESTED`, each with its required field, and the signature block `event.signer_id`,
  `event.signer_epoch`, `event.signature_algorithm`.
- **Fixed an inert conditional guard.** One block had `"required"` nested *inside* `"properties"`, so
  it parsed as a property literally named `required`: the metaschema rejected the document, and the
  guard never fired — a record carrying no `event.type` matched the `if` vacuously and inherited the
  `then`.
- Editorial rulings are recorded in the files. **Kept**, each with a `$comment` naming the section
  that imposes it: `ecc.auth_ref`, `ecc.exception_scope`, `ecc.decision_basis`, `event.auth_id`,
  `AUTHORIZATION_ALREADY_REDEEMED` — required by a normative section, absent from the field tables,
  and without them NT-007 is not expressible. **Excluded** as editorial residue pending a decision:
  `ecc.integrity_mode`, `ecc.decision_digest`, `event.decision_digest`,
  `ECC_DECISION_BINDING_INVALID`.
- `spec/schemas/validate.py` and a CI job implement Part III §7.2 Step 3: a retired identifier, a
  re-declared residue, an out-of-namespace property or a drop below the normative floor all fail the
  build.

### The reference harness

Tracked separately in [`spec/known-defects-harness.md`](spec/known-defects-harness.md), and released
as `croa-reference-harness` **v1.0.1**, bound to this specification version.

- **H-08 found and fixed** — the redemption registry was per-instance, so H-01 was reachable one
  enforcement instance away. It was not found by an audit: H-01's own entry already contained the
  sentence describing it, written as a limitation. Redemption now runs through a shared
  `RedemptionRegistry` whose claim is all-or-nothing over the ECC and its authorization.
- **H-03 closed** — every emitted event and every compiled ECC validates against the published
  schemas, gated in CI. The defect was not the missing fields it appeared to be: the harness had no
  grounded governed action at all.
- **H-06 narrowed** — there is now a governed system in its own process, reachable only through a
  `C6` gateway, with every assertion on that system's own log rather than on a return value.
  **Still open for a deployment**: the unreachability comes from not naming a socket, not from a
  network policy.
- Appendix Q complete (`NT-005`, `NT-006`, `NT-008` and the Evidence Pack) and Appendix R
  implemented.

### Governance

- **An RFC was opened and merged before the normative surface**, which `CONTRIBUTING.md` §42
  requires and which had not been done before. **It is not marked accepted.** The RFC on `main`
  still carries `rfc: 0000` and `status: draft`, and `rfcs/README.md` §5 says an accepted RFC is
  merged "with a number and a `status: accepted` field". So the process step that authorises the
  normative change is, on the record, incomplete — recorded here rather than smoothed over, because
  a release freezes the record.
- **D-04 and D-05** recorded in [`GOVERNANCE-DEVIATIONS.md`](GOVERNANCE-DEVIATIONS.md): four pull
  requests merged past a required check, one merged into the wrong branch, and the correction for the
  bypass merged through the bypass. None is claimed compliant.
- The elevated review tier is **satisfiable** for the first time, and approvals are now counted only
  from declared owners of the paths a pull request touches.

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
- **Added `spec/errata-v1.0.md`** — defects in the published draft (E-01…E-15) with the
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

### Post-publication independent audit (2026-09) — *clarification · normative-correction*

An external enterprise-architecture audit of the two public repositories, the specification and the
founding study. It reproduced two bypasses in the reference harness and found that three statements
the project had published were not supported by the artifact meant to support them.

- **Added `spec/known-defects-harness.md`** — the harness defect register (H-01…H-07), the state of
  each reference negative test, and exit criteria. Published before the defects are fixed, and
  before the project has independently re-run them, because the findings contradict claims already
  made in public.
- **Corrected three claims.** The harness "demonstrates the C1–C7 enforcement behavior" (it
  demonstrates a reduced plane with no `C4` and no admission layer); "the decisions are
  reconstructable from the log alone" (`verify()` does no causal correlation); and, in the harness's
  own README, that a signed authorization admits "exactly one" execution.
- **Added `GOVERNANCE-DEVIATIONS.md`** — PR #1 and PR #2 were merged without the RFC and Final
  Comment Period the project's own rules require. Recorded, not backdated, with the structural gaps
  that made it possible.
- **Added errata E-14 and E-15** — release identity (the Zenodo deposit, the Git tag and `main` are
  not the same artifact) and the schema namespace asserting an institutional status the corpus
  disclaims.
- **Opened [RFC 0002](rfcs/text/0002-schema-namespace.md)** for the schema namespace, as a draft
  under a real comment period. The schemas are deliberately not changed before it closes.
- **Corrected the evidence inventory** — the founding study's current version is v2, DOI
  `10.5281/zenodo.19898196`; what is deposited is the paper, not the protocol, data, scoring rubric
  or code, so it is not reproducible by a third party.
- **CI hygiene** — removed the stale link-check exclusion that assumed the harness repository was
  private, and stopped excluding `spec/**` from Markdown linting.
- **Fixed H-01 to H-04 in the reference harness.** *(harness `0.2.0`.)* Authorization consumption
  moved from `C6` to `C7` and became an atomic test-and-set, so a spent authorization yields no
  commitment at all — Part II §4.8 as the specification already required it. `C6` now requires the
  authenticated subject and the concrete operation and compares both against the signed commitment;
  both arguments are mandatory, so the unsafe call is no longer expressible, and the `C5` write takes
  its values from the validated commitment rather than the caller. `cc.id` became the full SHA-256 of
  the commitment's canonical content. `AuditStore` gained `verify_decisions()` — the Appendix G.2.4
  correlation — kept separate from `verify_chain()` so the two cannot be confused. The suite is now
  16 tests including an adversarial group and two 100-thread races; all pass. **H-05, H-06 and H-07
  remain open**, and H-06 is the largest: there is still no network boundary, so property P4 is not
  demonstrated.
- **Corrected a claim made three days earlier.** `evidence/harness-defects/` was described as "a
  regression gate once the defects are fixed". It is not: it copies the harness rather than importing
  it, so it can never pass whatever the real code does. It is now labelled as what it is — a frozen,
  dated reproduction of the defects as they stood — and the regression gate is named as the harness's
  own `TestAdversarial` suite.
- **Reproduced the audit's findings.** H-01, H-02 and H-03 were re-run by the project against the
  published harness code on 2 September 2026 and **all three reproduce**. The reproduction ships as
  a runnable, dependency-free script at [`evidence/harness-defects/`](evidence/harness-defects/) that
  exits non-zero while any defect stands, so it serves as the regression gate for the fix. The
  defect register now states the findings as confirmed rather than as reported. This is the first
  entry in the *adversarial testing* evidence bucket — author-run, and it found defects rather than
  confirming a property.
