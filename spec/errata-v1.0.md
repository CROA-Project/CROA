# Errata — CROA v1.0 Public Review Draft

**Applies to:** the dated Zenodo record, DOI [`10.5281/zenodo.21063423`](https://doi.org/10.5281/zenodo.21063423).

The published record is a dated artifact and is **not** re-rendered to correct defects. Corrections
are recorded here and applied in the next version. Each entry states the defect, the reading that
governs until the next release, and the disposition.

Entries are numbered `E-nn` and are stable. Found another? Open a
[clarification issue](https://github.com/CROA-Project/CROA/issues/new?template=clarification.yml) or a
[normative-conflict issue](https://github.com/CROA-Project/CROA/issues/new?template=normative-conflict.yml) — internal
inconsistency in a normative document is a defect and is exactly what public review is for.

---

## Normative-conflict errata

### E-01 — Deployment invariant property P7 omitted from the conformance checklist

**Defect.** Part IV §18.1 defines **seven** deployment invariant properties, P1–P7, and P7 (`C5` as a
tier-0 availability dependency) carries production MUSTs — high availability for the durable-commit
path and the redemption authority, a declared availability class with RPO = 0, and a defensible
sizing method. But the Part IV Conformance Requirements section says *"All six invariant properties
(P1 through P6 of §18.1) hold"*, the §18.1 recap lists P1–P6 only, the §6.5 deployment viewpoint says
*"while preserving P1–P6"*, and Part VI §29.2 records deployment conformance as "P1–P6".

**Reading that governs.** P7 is normative. §18.1 is the defining section; the enumerations elsewhere
are stale. An assessment that does not evidence P7 is incomplete, and an assessor should record it.

**Disposition.** All enumerations corrected to P1–P7 in the next version.

### E-02 — Reference negative tests: six or seven

**Defect.** Appendix Q's introduction says *"seven Reference Negative Tests (NT-001 through NT-007)"*
and NT-007 (governed exception is single-use) is fully specified in the body. Three other places
still say six: the Appendix Q Part 2 lead-in (*"The six tests below…"*), the Appendix Q revision note,
and Part VI §28.5.1.

**Reading that governs.** In the published v1.0 record there are **seven** reference negative tests, NT-001 through NT-007. The three stale counts saying six are wrong.

**Disposition.** The stale counts corrected, and NT-008 (see E-12) added, in the next version — which therefore carries **eight**. A reader assessing a deployment against the published record applies seven; a reader working from the next version applies eight.

### E-03 — Dangling cross-reference from NT-007 to §29.3

**Defect.** NT-007 step 4 cites *"the concurrent double-redemption test (Part VI §29.3)"*. §29.3 as
published contains no concurrency test; its CC-integrity item is a sequential replay check.

**Reading that governs.** The concurrent double-redemption requirement is normative — it is stated
in Part II §4.8 and tested by NT-007 step 4 itself. §29.3 should be read as incorporating it.

**Disposition.** §29.3 amended to carry the test explicitly.

### E-04 — Invariant I1's enforcing components omit `C6`

**Defect.** Part II §5.1 lists I1's enforcing components as `C3`, `C2`, `C4`. `C6` is absent —
although §6.2 makes `C6` the component that blocks any operation outside the execution surface, and
§4.8 makes it the redeemer, i.e. the runtime enforcer of the reachability guarantee at the boundary.

**Reading that governs.** `C6` (and `C7`, which produces the only admissible artifact) are enforcing
components of I1. Tenet T1's own "Relationship to Part II" paragraph already says so.

**Disposition.** I1's enforcing-component list corrected in the next version.

### E-05 — Appendix S: `TP-X` state persistence stated at two different strengths

**Defect.** Appendix S §S.6 note 1 says cross-session (`TP-X`) trajectory state **MUST** persist
across session boundaries; note 4 of the same section says it **SHOULD** be treated as part of the
governance record with `C5`-equivalent durability.

**Reading that governs.** Appendix S is informative and adds no normative requirement. The governing
normative text is Part II §4.6.3, under which a `TP-X` aggregate persists across sessions for the
subject by definition of the profile. Note 4's SHOULD concerns *where* the state is stored, not
*whether* it persists.

**Disposition.** Note 4 reworded to remove the apparent conflict.

### E-06 — Appendix S §S.3: budget cap changes mid-pattern

**Defect.** The worked cloud-provisioning pattern sets an alert threshold at 80% of a €12,000 cap in
§S.3.7 and then uses a €10,000 cap (80% = €8,000) in the §S.3.9 negative tests, without saying the
figure changed.

**Reading that governs.** The figures are illustrative; Appendix S states this. The pattern is the
normative content, not the numbers.

**Disposition.** Figures made consistent in the next version.

### E-07 — Appendix K: method tiering versus the "no relaxation within the boundary" rule

**Defect.** Appendix K §K.1 states as a normative design rule that the CROA Core profile *"MUST NOT
lower any requirement that applies within its declared boundary."* §K.3 then makes `C4` trajectory
analysis (counters/automaton) **optional** for R0–R1 (fully reversible and compensatable) transitions
inside that boundary.

**Reading that governs.** §K.3 sets the *minimum method depth per consequence class* rather than
relaxing a requirement: Tenet T5 already fixes the minima by class, and an invariant that is not
exposed to accumulation needs no cumulative profile. The two statements are reconcilable, but the
text does not reconcile them.

**Disposition.** §K.1's rule reworded to say explicitly that consequence-proportionate method tiering
is not a relaxation, with a pointer to T5.

---

## Claim-hygiene errata

### E-08 — "empirically validated" in Part VI §29.5

**Defect.** §29.5 states in bold that the architectural thesis *"has been **empirically validated** in
the founding comparative study"*. The note it points to then discloses that the study was conducted
by the framework's originators rather than an independent assessor, that it evaluated the earlier
four-layer model rather than the seven-component control plane and the L0–L5 and RBAC/AQL model of
this version, and that its authors characterise the results as directional and not statistically
generalisable. A sentence quoted without its note therefore overstates the evidence.

**Reading that governs.** The founding study supplies **directional validation** of the architectural
thesis and of Technical Sycophancy as a phenomenon. It is not independent, not current with this
version's architecture, and not generalisable. See [`docs/limitations.md`](../docs/limitations.md) §4.

**Disposition.** The sentence rewritten to carry its own qualification.

### E-09 — Unbounded novelty claims in Part V §26

**Defect.** Part V §26 says Technical Sycophancy is *"the failure mode… that no prior governance
framework formally defines"*, and the TH-1 delimitation says *"**Only** an execution-layer
architecture that…"*. Both are unbounded universal negatives over a literature that grew
substantially during 2026.

**Reading that governs.** The defensible statement is scoped and dated: as of publication, CROA is
not aware of a governance framework that defines this failure mode as an *execution-layer* threat
class with a structural (rather than behavioural) remedy. Adjacent 2026 work states parts of the same
problem — notably arXiv:2608.01558 and arXiv:2603.16586 on trajectory-dependent violation — and is
now cited in [`docs/prior-art.md`](../docs/prior-art.md) §2.

**Disposition.** Both statements rescoped and given a related-work pointer.

### E-10 — "none specifies how unsafe execution paths are made structurally unreachable" (Part I §1.5)

**Defect.** The sentence is true of the frameworks in the §1.5 table (NIST AI RMF, ISO/IEC 42001, the
EU AI Act, NIST SP 800-207, TOGAF, RBAC/ABAC) but reads as a claim about the field.

**Reading that governs.** The scope is the table. It is not a claim about the research literature on
runtime governance of agentic systems, which is surveyed in `docs/prior-art.md` §2.

**Disposition.** Scoping clause added.

---

## Coverage errata

### E-11 — Cumulative trajectory state under concurrent evaluation is unspecified

**Defect.** Part II §4.8 mandates an atomic linearizable compare-and-swap for redemption of a
Compiled Commitment or an authorization artifact, across all `C6` instances, in every topology. No
equivalent requirement exists for the read-evaluate-increment cycle of a `TP-C`/`TP-X` aggregate.
Because two concurrently evaluated actions carry distinct `cc.id`s, the redemption CAS does not
relate them: both may be evaluated against the same pre-increment total and jointly cross a threshold
neither crossed alone. Appendix S contains no concurrency treatment; nor does Appendix L for
concurrent sub-agents sharing a budget.

**Reading that governs.** This is a genuine gap in v1.0, not a reading error: the published record
states no requirement here at all. Until the next version, a deployment enforcing a `TP-C`/`TP-X`
invariant under concurrent load SHOULD serialise the read-evaluate-increment cycle per accumulation
key and MUST record the exposure in its Residual Risk Register (C-24). The **SHOULD** is the
strongest reading available against a record that is silent; the next version makes it a **MUST**
with `C2` fail-deny where the serialisation cannot be established. The two are not in conflict — they
apply to different versions — but an assessor must be explicit about which version a claim is made
against.

**Disposition.** A minimum serialisation requirement added to Part II §4.6.3 in the next version;
tracked as research question RQ-16 and as a declared non-property in
[`spec/properties.md`](properties.md) P-D. The general problem is formalised, independently of CROA,
by Peng & Wu, arXiv:2608.02764.

### E-12 — Authority non-expansion is asserted pointwise but not composed or tested

**Defect.** Monotonicity is required of RBAC admission (§4.9.1), of the AQL (§4.9.2), of compilation
(§4.4.3, `C7` MUST NOT widen an exception scope), of the execution surface (§6.2), and of delegated
scope (Appendix L D3). No statement composes these into a property over the architecture, and no
reference negative test covers authority expansion outside the optional Appendix L delegation tests.

**Reading that governs.** The pointwise requirements are normative and stand. The composed property
is entailed by them but was not stated.

**Disposition.** Stated as invariant **I8 — Authority Non-Expansion** and as property **P-B** in
[`spec/properties.md`](properties.md), with a new reference negative test NT-008. This names and
tests an existing property; it introduces no component, artifact, or mechanism.

> *A correction recorded rather than dropped.* An earlier draft of this errata pass stated the
> property as bounding a composition by its **least-authorized participant**. That formulation was
> wrong: it would have forbidden delegation outright — delegation exists precisely to give a
> sub-agent authority it did not hold — and it was strictly stronger than the pointwise clauses it
> claimed to follow from. The two-clause form that shipped (attenuation *along a chain*; no
> *laundering* across a composition, with the **union** rather than the intersection as the bound) is
> what the architecture entails. The error is left visible here because an errata page that silently
> revises itself is not an errata page.

### E-13 — The reversibility classification R0–R4 is unused by trajectory analysis

**Defect.** Tenet T5 requires every governed transition to carry a reversibility/consequence class
R0–R4, which fixes the authorization bar for that transition. No trajectory rule profile, conformance
level, or reference test uses the class: an accumulation of reversible effects and an accumulation of
irreversible ones are treated identically.

**Reading that governs.** T5 governs single transitions, as written. It makes no claim about
accumulated irreversibility.

**Disposition.** Tracked as research question RQ-20; a decision on whether irreversibility should
weight a cumulative threshold is deferred to evidence rather than settled by fiat.
