---
tags:
  - croa_foundation
version: 1
language: english
---

# CROA Framework — Part VII: Governance of the Standard

**Full title:** CROA — Constrained Reachability Orchestration Architecture: A Framework for Deterministic Governance of Agentic AI Execution
**Series designation:** CROA-7
**Status:** Official Specification (v1.0.1)
**Version:** v1.0.1
**Date:** 2026-09-03
**Part:** VII of VII

---

> **Revision history.** This file's earlier revision notes are consolidated in [CHANGELOG](../../CHANGELOG.md) (relocated 2026-06-16, Y. Durand; corpus bumped to v1.0.1.1). The

> *Scope of this Part. Parts I–VI specify how a governed agentic system is architected, developed, threat-modeled, deployed, and assessed. Part VII specifies how the **standard itself** is versioned, governed, and stewarded — so that CROA can evolve as a neutral, auditable, multi-stakeholder artifact rather than a single party's document. Part VII is the standardization-readiness layer: it is what a recognition body, an adopter, or a contributor consults to understand the stability, neutrality, and change process of the standard.*

---

## Chapter 31. Lifecycle and Versioning of the Standard

**Chapter abstract.** This chapter specifies the versioning model of the CROA framework, the stability guarantees attached to its identifiers, the classes of change permitted between versions, and the release and deprecation process. Its purpose is to let adopters depend on the standard: an enterprise that asserts conformance against a version (Part VI §29.1) must know what that version means and how it can change.

---

### 31.1 Versioning Model

the CROA framework is versioned as **MAJOR.MINOR.PATCH**:

- **MAJOR** — a change that alters or removes an existing normative requirement, a tenet, an invariant, a component contract, or a conformance level in a way that could cause a previously conformant system to become non-conformant, or vice versa. A MAJOR version may renumber only under the deprecation rules of §31.2.
- **MINOR** — a backward-compatible addition: a new optional capability, a new threat class, a new deployment model, a new admission control, or clarifying normative text that does not invalidate an existing conformant system. (The addition of TH-11, the RBAC subject-authorization model, and the Agent Qualification Layer are examples of MINOR-class additions.) By contrast, introducing a new pipeline component or changing an existing component's contract — for example, splitting ECC compilation out of `C2` into the distinct component `C7` (Contract Compiler) and changing the ECC signer accordingly — is a **MAJOR**-class change, because it alters a component contract.
- **PATCH** — editorial corrections and errata that change no normative meaning: typographic fixes, cross-reference repairs, non-normative clarifications, and the relocation of misplaced content.

A published version MUST carry its MAJOR.MINOR.PATCH identifier on every Part. A conformance assertion (Part VI §29.1) MUST name the version it was assessed against.

---

### 31.2 Identifier Stability

The identifier schemes defined in Part I §1.8 and catalogued in [Appendix B - Notation, Identifiers and Symbols](../appendices/appendix-b-notation-identifiers-and-symbols.md) — tenets (`Tn`), components (`Cn`), invariants (`In`), threats (`TH-n`), deployment models (`DM-n`), deployment invariant properties (`Pn`), integration patterns (`IP-n`), conformance levels (`Ln`), deliverables/artifacts (`C-n`), architecture decision records (`ADR-n`), reversibility/consequence classes (`Rn`), invariant evaluability classes (`En`), trajectory rule profiles (`TP-*`), delegation requirements (`Dn`), and figures/tables — are **stable once published**. (Appendix B is the authoritative catalog of these schemes.) Specifically:

- An identifier, once assigned in a published version, MUST NOT be reused for a different concept in any later version.
- A concept that is withdrawn retains its identifier, which is marked **DEPRECATED** in the lexicon with a pointer to its successor or to the rationale for withdrawal. A deprecated identifier MUST NOT be silently deleted.
- New concepts receive the next unused identifier in their scheme; they do not displace existing ones.

Identifier stability is what allows external artifacts — threat assessments, conformance records, regulatory mappings — to cite the standard durably across versions.

---

### 31.3 Classes of Change

| Change class | May | MUST NOT |
|---|---|---|
| Editorial / errata (PATCH) | Fix typos, cross-references, formatting; relocate misplaced content; clarify non-normative text | Alter any normative requirement or its meaning |
| Additive (MINOR) | Add optional capabilities, threat classes, deployment models, admission controls, profiles, clarifying normative text | Invalidate any system conformant to the prior version; relax an existing requirement |
| Breaking (MAJOR) | Alter, strengthen, or remove a normative requirement, tenet, invariant, component contract, or conformance level | Reuse a retired identifier; remove an identifier without deprecation |

A change that strengthens a requirement (making some previously conformant systems non-conformant) is a MAJOR change even if it adds no new text, because it changes the conformance boundary.

**Worked example (in-draft).** The promotion of **Appendix L** (Governed Multi-Agent Delegation) from informative to *conditional normative* — adding an OPTIONAL multi-agent-delegation capability whose requirements bind only deployments that implement it, while invalidating no prior-conformant system and relaxing or strengthening no existing requirement — is an **Additive (MINOR)** change. Like the in-draft `C7`/`C6` component-contract change recorded in this Part's revision notes (a MAJOR change), it is incorporated into the 1.0 draft rather than issued as a version increment over a published baseline, because no published baseline yet exists; a conformance assertion always names the version it was assessed against (§31.1).

---

### 31.4 Release and Deprecation Process

- Each version is released as a complete, internally consistent set of Parts I–VII; Parts are not versioned independently of one another.
- A MAJOR version SHOULD provide a migration note describing what conformant systems must change and over what period prior-version conformance continues to be recognized.
- Deprecated content is retained in the lexicon for at least one MAJOR version after deprecation before it MAY be removed, and its removal is itself a MAJOR change.
- Before a release, the editor (§32.3) SHOULD run the **reference editorial linter** published in `tools/` (identifier-range checks, count-consistency checks, prose↔JSON enumeration cross-checks, and duplicated-normative-position checks) so that the internal-consistency discipline this framework relies on is reproduced mechanically rather than by hand. The linter is a **non-normative** editorial aid; it does not replace technical-committee review (§32) or change classification (§31.3), and a clean linter run is neither necessary nor sufficient for conformance.

---

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 31**

- §31.1: Every published Part MUST carry the MAJOR.MINOR.PATCH version; a conformance assertion MUST name the version assessed.
- §31.2: Identifiers are stable once published; a retired identifier MUST NOT be reused and MUST be marked DEPRECATED rather than silently deleted.
- §31.3: A change that relaxes or strengthens a normative requirement is a MAJOR change; a PATCH MUST NOT alter normative meaning.

**Cross-references.** Chapter 31 formalizes the identifier-stability statement in Part I §1.8 and the version-naming requirement in the conformance assertion (Part VI §29.1).

---

## Chapter 32. Governance of the Standard

**Chapter abstract.** This chapter specifies how the standard is governed: the mandate of the steward, the neutrality and independence commitments that keep CROA vendor- and implementation-agnostic, the roles and decision rights for change, and the public process by which changes are proposed, reviewed, and ratified. It is the chapter a recognition body consults to judge whether CROA is governed as a neutral standard rather than a single party's document.

---

### 32.1 Steward and Mandate

the CROA framework is maintained by a **steward** whose mandate is limited to: maintaining the integrity, consistency, and neutrality of the standard; operating the change process (§32.4); publishing versions (§31); and recognizing conformance assessment practice (Chapter 33). The steward does not own conformance outcomes, does not certify products as a condition of using the standard, and does not privilege any implementation.

> *Status note (non-normative). The standard is currently stewarded by the CROA Project. The neutrality and multi-stakeholder requirements in §32.2–§32.4 describe the governance model the standard commits to operate under. Establishing the independent technical committee and external review described below is an organizational action the steward undertakes; until that committee is constituted and recorded, the standard's status with respect to independent governance MUST be represented honestly as "single-steward, transitioning to multi-stakeholder governance," not as a ratified multi-party standard.*

---

### 32.2 Neutrality and Independence Commitments

- **Vendor and tool neutrality.** The standard MUST NOT require, name as mandatory, or privilege any specific product, vendor, model provider, or tool. Where a concrete technology is named, it is illustrative (Part II §4.11).
- **Separation from the reference implementation.** The standard is independent of any reference implementation. A reference implementation MAY demonstrate conformance but MUST NOT be the definition of conformance; conformance is defined solely by Parts I–VI. No requirement may be introduced that only a particular implementation can satisfy.
- **Separation from certification and commercial offerings.** Any certification, training, or commercial program is separate from the standard and MUST NOT alter normative requirements. Using the standard MUST NOT be conditioned on purchasing any such program (Chapter 33).
- **Steward conflict of interest.** Where the steward also operates a certification, training, or commercial program — as is currently the case — this is a structural conflict of interest that MUST be managed explicitly: the steward MUST NOT make conformance contingent on any such program, MUST keep the change-ratification function (§32.4) organizationally separate from its commercial functions, and MUST record that separation publicly.
- **Conflict of interest.** Participants in the change process MUST disclose material commercial interests in a proposal's outcome. Ratification MUST NOT be controlled by any single commercial interest.

---

### 32.3 Roles and Decision Rights

| Role | Responsibility | Decision right |
|---|---|---|
| Editor(s) | Maintain document integrity, consistency, and identifier discipline; prepare releases | Editorial/PATCH changes; no normative authority |
| Technical committee | Review and decide proposals; safeguard neutrality and internal consistency | Approve MINOR and MAJOR changes by the ratification rule (§32.4) |
| Steward | Operate the process; publish versions; maintain the lexicon and registry | Procedural; no unilateral normative authority |
| Contributors | Propose changes, interpretations, and errata | Submit; participate in review |

No single role — including the steward — may unilaterally introduce or remove a normative requirement. Normative change requires the committee process.

---

### 32.4 Change Proposal and Ratification

- **Proposal.** Any party MAY submit a change proposal. A proposal MUST identify the affected Parts/identifiers, the change class (§31.3), the rationale, and the impact on existing conformant systems.
- **Review.** The technical committee reviews each proposal for internal consistency (it MUST NOT contradict an existing requirement without being classed MAJOR), neutrality (§32.2), and conformance impact (Part VI).
- **Ratification.** MINOR and MAJOR changes MUST be ratified by the committee under a documented rule that no single commercial interest controls; the decision and its rationale MUST be recorded publicly. The concrete ratification threshold (for example, consensus or a defined supermajority) MUST be fixed in the committee charter and published.
- **Change classification.** Whether a change is editorial (PATCH), additive (MINOR), or breaking (MAJOR) per §31.3 is determined by the technical committee, not by the editors; an editor MUST escalate any change whose class is uncertain rather than apply it as editorial.
- **Public record.** Proposals, decisions, and rationales MUST be recorded so that the evolution of the standard is itself auditable — the same evidentiary discipline (T10) the standard requires of conformant systems.

---

### 32.5 Interpretations and Errata

- An **interpretation** clarifies how an existing requirement applies without changing it; interpretations are published against a version and do not change the version's normative meaning.
- An **erratum** corrects an error that does not change normative intent (PATCH); an erratum that *does* change intent is reclassified as a MINOR or MAJOR change and processed accordingly.

---

### 32.6 Intellectual Property, Licensing, and Contribution

- **Standard text.** The text of the CROA framework is published under a license that permits its use, implementation, and citation by any party without fee. The applicable license MUST be stated in the published version.
- **Implementation rights.** Implementing the standard MUST NOT require a license from the steward. No conformance, profile, or "CROA-based" claim may be conditioned on a patent or copyright grant from the steward.
- **Contributions.** A contributor submitting a change proposal (§32.4) grants the steward the right to incorporate and publish the contribution under the standard's license, and represents that the contribution does not knowingly infringe third-party rights. A contributor MUST disclose any patent they believe is essential to implementing a proposed normative requirement.
- **Patent stance.** Normative requirements SHOULD be implementable without a license to any patent held or controlled by the steward; where this is not possible, the steward MUST disclose the dependency and offer terms that do not discriminate between implementers.

> *License declaration. The text of the CROA framework (Parts I–VII and the appendices) is published under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license; accompanying code and machine-readable materials (e.g., the reference JSON schemas in `schemas/`) are published under the **Apache License 2.0**. These licenses permit use, implementation, redistribution, and citation by any party without fee, subject only to attribution. Implementing the standard requires no license, fee, or commercial program from the steward. This declaration satisfies the stated-license requirement of this section and the "Open implementability" criterion of the Part VII Conformance Requirements.*

---

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 32**

- §32.1: The steward's mandate is limited to integrity, neutrality, process, publication, and assessment recognition; it does not own conformance or privilege any implementation.
- §32.2: The standard MUST remain vendor-, tool-, and implementation-neutral; conformance MUST be definable without reference to any particular implementation or commercial program.
- §32.2: Where the steward also runs a commercial or certification program, that conflict of interest MUST be managed — conformance MUST NOT be contingent on the program, and the ratification function MUST be organizationally separate from commercial functions.
- §32.3–§32.4: No role MAY unilaterally introduce or remove a normative requirement; normative change MUST be ratified by the committee under a published threshold that no single commercial interest controls, with the decision recorded publicly. Change classification is the committee's determination, not the editors'.
- §32.6: The standard text MUST be published under a stated license; implementing the standard MUST NOT require a license, fee, or commercial program from the steward; contributors grant publication rights and MUST disclose patents essential to a proposed normative requirement.

**Cross-references.** Chapter 32 is the governance basis for the change classes in §31.3 and the conformance-stewardship functions in Chapter 33. Its public-record requirement applies the auditability principle (T10) to the standard itself.

---

## Chapter 33. Conformance Stewardship and Derivative Works

**Chapter abstract.** This chapter specifies how conformance assessment practice is recognized, how conformance claims may be recorded, and how derivative works — profiles, extensions, and "CROA-based" offerings — may relate to the standard without diluting it. It closes the loop between the conformance model (Part VI) and the governance of the standard (Chapter 32).

---

### 33.1 Recognition of Assessment Practice

The steward MAY publish criteria for recognizing independent assessors and assessment practice consistent with Part VI §29.4 (independence; verifiability from the Conformance Evidence Record, `C5`, and the named read-access cross-check sources). Recognition pertains to *practice*, not to outcomes: the steward recognizes that an assessor follows the independence and evidence discipline, not that any particular system is conformant.

---

### 33.2 Conformance Claims Registry (Claims Register)

- A conformance assertion (Part VI §29.1) MAY be recorded in a public registry maintained by the steward. This registry is referred to in this framework as the **Claims Register**. Registration is OPTIONAL and is not a precondition for conformance.
- A registered assertion MUST carry its version, level, governance boundary, assessor, and independence basis. The registry records claims and their evidence references; it does not itself re-perform assessment.
- The Claims Register is the standard's mechanism for **honest, comparable capability communication**: it lets an adopter publish what it claims, scoped to a governance boundary and substantiated by an evidence reference, in a form a third party can locate and challenge (§33.5). It is the registry referenced by the T1 claim-scope statement (Part I, Chapter 3) and by the transparency mapping in Appendix M (Art. 13). The Claims Register records *conformance* assertions; **adoption-status** declarations are kept in the separate adoption-status registry (§33.3) and MUST NOT be recorded as conformance claims.
- Until the steward operates a public Claims Register, an adopter making a conformance claim SHOULD retain the equivalent assertion record (Part VI §29.1) as a Publication Package artifact (§33.6) so that the claim remains independently locatable and challengeable.

---

### 33.3 Profiles and Derivative Works

- A **profile** is a named, version-bound restriction or extension of the standard for a domain (for example, a sector-specific qualification battery, or a deployment-model constraint). A profile MAY add requirements and MAY narrow optionality; a profile **MUST NOT relax, remove, or contradict** any normative requirement of the version it profiles. A profile that does so is not a CROA profile.
- A **"CROA-based"** or **"CROA-aligned"** claim MUST cite the version and Part(s) it builds on and MUST state plainly where it deviates. A derivative work MUST NOT present itself as the standard or imply steward endorsement absent recognition under §33.1.
- A reference implementation is a derivative work in this sense: it demonstrates, it does not define (Part VII §32.2).
- **Recognized profile — CROA Core.** The standard publishes one first-party profile in this version: **CROA Core**, a risk-proportionate adoption profile (Appendix K). CROA Core narrows the governance boundary and tiers evaluation-method depth by consequence class; it adds requirements and narrows optionality and therefore satisfies the profile rule above. Its non-conformant on-ramp tier (Tier 0) MUST be claimed only as an adoption status, never as conformance; its conformant tier (Tier 1) claims L3 or L4 only for its declared narrow boundary.
- **Adoption-status claims.** The statuses **CROA-aware**, **CROA-aligned**, and **Targeting L*n*** (Part VI §28.5) describe an adoption journey and MUST NOT imply conformance. Any public adoption-status claim MUST cite the standard version, the scope (governance boundary), and the status; only an evidenced L4+ assertion (Part VI Chapter 29) MAY be stated as "CROA-conformant". The steward MAY maintain a registry of adoption statuses kept **separate from** the conformance-assertion registry (§33.2).

---

### 33.4 Relationship to Certification and the Reference Implementation

Certification programs, training, and the reference implementation are downstream of the standard and governed separately. They MAY assert conformance to a CROA version using the Part VI evidence model, but they MUST NOT introduce normative requirements, condition use of the standard on their purchase, or substitute their own criteria for the conformance levels in Part VI. The standard remains independently usable by any party from Parts I–VI alone.

---

### 33.5 Interpretations, Challenges, and Appeals

- **Interpretation requests.** Any party MAY request a formal interpretation of how a normative requirement applies to a case. Interpretations are issued per §32.5, recorded publicly, and do not change the version's normative meaning.
- **Conformance-claim challenges.** A party MAY challenge a recorded conformance assertion (§33.2) on the basis that its evidence does not substantiate the claimed level (Part VI, Chapter 29). A challenge MUST cite the specific criterion alleged to be unmet.
- **Adjudication and appeal.** The steward MUST operate a documented procedure for adjudicating interpretation disputes and conformance-claim challenges, with an appeal path to the technical committee. Adjudications and appeals MUST be recorded publicly (T10), and MUST NOT be performed by a party holding a material commercial interest in the outcome (§32.2).

---

### 33.6 Recommended Publication Package (Informative)

This section is **informative**. It recommends, but does not require, a packaging of the standard that lowers the barrier to evaluation and adoption. None of the items below adds to or alters the normative content of Parts I–VI.

The recommended publication package comprises:

1. **Executive Brief** (≈2 pages) — the problem, the thesis (structural unreachability), and what conformance does and does not claim.
2. **Architecture Overview** (1 diagram + ≈1 page) — the C1–C7 reference architecture and the canonical request flow (Figures CROA-4a, CROA-4b).
3. **Implementer Guide** — a practical path to L3 and L4, mapped to the CROA-PaC phases (Part III) and the conformance matrix (§28.3).
4. **Conformance Pilot Kit** — a sample Test Plan, a sample `C5` event, a sample ECC, and a sample Conformance Evidence Record (C-32), drawn from the templates in the Part VI appendix.
5. **Threat Model Summary** — the TH-1…TH-11 table with the §27.1 mitigation mapping.
6. **Glossary / Lexicon** — the stable terms ([Appendix A - Lexicon](../appendices/appendix-a-lexicon.md)).
7. **Technical Committee Charter (draft)** — the governance instrument operationalizing Chapter 32 (currently single-steward, transitioning; §32.1).
8. **Reference Implementation Statement** — a plain statement that a reference implementation (e.g., Riven) *demonstrates* conformance but does **not** *define* it; conformance is defined solely by Parts I–VI (§32.2, §33.4).

The package is a recommended delivery format only. A version is conformant with Part VII on the basis of its normative content, not on the presence of any packaging artifact.

---

### 33.7 Brand and Claims Usage Policy

Some obligations in this framework constrain how CROA and its central claim are **communicated** — for example, the Tenet T1 requirement that marketing or executive summaries not state the bare "unsafe execution paths are unreachable" claim without its conditions (Part I, Chapter 3), and the adoption-status communication rules of §33.3 and Part VI §28.5. These are **claims-usage obligations**, not conformance criteria of a deployed system: the conformance mechanisms of Part VI (reproducible tests against `C5`) cannot test the wording of an external marketing document, and a standards body would rightly object to treating a brochure's phrasing as a testable normative requirement of a technical architecture.

this framework therefore **consolidates the communication obligations into a single Brand and Claims Usage Policy**, governed by the steward and applicable to any party using the CROA name, marks, or central claim:

- The canonical statement of the structural-unreachability claim is the **conditioned** T1 formulation (Part I, Chapter 3). Communications that state the bare claim without its conditions misrepresent the standard and are a brand-usage violation, addressed through the steward's marks policy and the challenge procedure (§33.5) — not through a deployed system's conformance assessment.
- A public conformance claim MUST be substantiated by an evidenced assertion (Part VI Chapter 29) and SHOULD be locatable in the Claims Register (§33.2); an adoption-status claim MUST follow §33.3 and Part VI §28.5.
- Where this framework's technical body (Parts I–VI) states a constraint on *claims or marketing wording*, that constraint is to be read as a pointer to this policy. The constraint's force derives from the steward's brand governance and the challenge/appeal procedure, not from the Part VI conformance tests; a deployed system is never found non-conformant for a third party's marketing wording.
- **Communicate the *form* of the guarantee, not its supposed scope.** Communications SHOULD foreground what the guarantee *is* — **deterministic, auditable, bounded to the declared modeled action space, and reconstructible from the `C5` record** — rather than an unbounded scope it does not have ("dangerous actions are impossible"). The honest and defensible property is the *form* of enforcement (structural, evidenced, bounded), not a claim of total semantic safety; §28.6 enumerates precisely what L4 does and does not claim, and the underlying design cost is stated in Part I §2.7.
- **Align the title and any showcase example with the conditioned claim.** Where a deployment or the standard's own worked example is used in outreach — for example the NovaCare PHI case (Appendix H) — the headline MUST NOT assert a property the body conditions away. The NovaCare example's honest scope is stated in Appendix H §H.6.1 (the PHI/crypto/authz invariants are `E3`, bounded over the modeled action surface, not a guarantee of semantic completeness). A showcase headline such as "PHI cannot leak" misrepresents that scope and is a brand-usage violation; the faithful showcase claim is "**PHI exfiltration is structurally blocked within the modeled action space, and every block is evidenced**," not "PHI cannot leak."

This relocation answers the standards-committee objection that conformance MUSTs must be testable by the standard's own mechanisms: the anti-overselling intent is preserved, but its enforcement is correctly located in brand governance (§33.5) rather than in the conformance model.

---

### 33.8 CROA Claims Usage Guide

> *Informative. This section operationalizes §33.7 by providing specific approved and prohibited claim formulations. It is a practical reference for communications teams, legal teams, and technical authors preparing materials that reference CROA.*

#### One-sentence safe positioning

> CROA is a vendor-neutral architecture framework for making selected unsafe execution paths structurally unreachable within a modeled action space, under a registered invariant set, and with auditable evidence of enforcement.

This sentence carries all three scope conditions and is defensible under external review. Communications SHOULD use this or an equally precise formulation as the primary CROA positioning statement.

#### Approved claims

The following claim formulations are approved. Each carries a required condition; omitting the condition converts an approved claim into a prohibited one.

| Approved claim | Required condition |
|---|---|
| CROA makes unsafe execution paths structurally unreachable within a modeled action space and registered invariant set. | Must mention *modeled action space* and *registered invariant set*. Must not be stated as an unconditional property. |
| CROA provides deterministic enforcement for machine-evaluable governance constraints. | Must distinguish E1/E2 (exact) from E3 (approximated/bounded). Must not imply all invariants are exactly decidable. |
| CROA turns selected AI governance controls into reproducible architectural evidence. | Must not imply that all AI governance controls, or all AI risks, are covered by CROA. |
| CROA governs execution, not model intent or model alignment. | Must distinguish execution-layer controls from model-layer alignment. Both are necessary; CROA addresses the execution layer. |
| CROA supports independent audit through C5 evidence, without requiring the implementing party's cooperation, attestation, or interpretation. | Must qualify: independent audit requires read access to C5 and the named cross-check artifacts (per Part VI §29.4). C5 alone is not sufficient to establish a conformance level. |
| A CROA L4-conformant implementation provides deterministic, auditable, and independently verifiable evidence that registered-invariant-violating execution paths are structurally unreachable within the declared governance boundary. | Must name the conformance level (L4), the governance boundary, and the version assessed. |

#### Prohibited claims

The following claim formulations are prohibited. They overstate CROA's scope, omit required conditions, or assert a status CROA does not have.

| Prohibited claim | Why it is prohibited |
|---|---|
| CROA makes AI agents safe. | Too broad. CROA governs execution paths within a declared scope; it does not govern model behavior, all possible outputs, or all AI risks. |
| CROA eliminates AI risk. | CROA reduces and structures execution-layer risk within its declared scope. AI risk has many components outside that scope. |
| CROA guarantees every output is safe or correct. | CROA governs whether a proposed action is permitted to cause state change in governed systems — not the content, correctness, or safety of all generated outputs. |
| CROA makes unsafe actions impossible. | The scope conditions are missing. The claim is only valid within the modeled action space, under the registered invariant set, given network-enforced P4. |
| CROA is an official industry standard. | The current status is Official Specification. The path toward formal standardization is described in this Part. |
| Our system is CROA-conformant because it uses a policy engine and an audit log. | CROA conformance requires independent assessment against the Part VI criteria. Component presence is necessary but not sufficient. |
| CROA prevents all prompt injection attacks. | CROA mitigates prompt-injection-driven execution failures by removing the ability to execute unauthorized actions, but it does not prevent prompt injection as a technique at the model layer. |

---

### 33.9 Public Review Process

> *Informative. This section describes the process for submitting feedback on this Official Specification. It imposes no conformance obligation.*

The CROA framework is under active public review. The CROA Project welcomes structured feedback from enterprise pilots, practitioners, security specialists, auditors, and regulators.

#### How to submit feedback

During the public review period, feedback may be submitted through the participation channels published by the CROA Project at each release. Submissions SHOULD follow the structure below to enable efficient classification and response.

A useful feedback submission includes:

- the Part, chapter, and section identifier affected;
- a clear description of the issue or proposed change;
- the issue label (see below) that best classifies the submission;
- if proposing new normative text, a draft of the proposed replacement or addition.

#### Issue labels

Use one of the following labels to classify a feedback item:

| Label | Meaning |
|---|---|
| `clarification` | Wording or explanation could be clearer without changing the normative requirement |
| `normative-conflict` | Possible contradiction between two normative requirements within the specification |
| `implementation-feedback` | Experience from a pilot or attempted implementation; includes practical friction points |
| `conformance-gap` | An issue with the evidence model, the negative tests, or the conformance criteria |
| `threat-model-gap` | A threat class, manifestation pattern, or mitigation that appears missing or unclear |
| `claims-risk` | A wording in the specification or companion documents that may be overstatement |
| `adoption-feedback` | An enterprise adoption concern — something that makes the framework harder to adopt |

#### Change levels

The CROA Project will triage each submission and classify any resulting change using the change classes defined in §31.3:

| Change level | Meaning |
|---|---|
| Editorial | Wording, formatting, or cross-reference correction; no technical meaning change |
| Clarification | Improves understanding without changing the normative requirement |
| Normative correction | Fixes a contradiction or broken normative requirement (MINOR or MAJOR per §31.3) |
| Normative change | Changes a normative requirement in a way that may affect conformant systems (MAJOR per §31.3) |
| Extension | Adds new optional guidance, an informative pattern, or an informative appendix |

All normative changes follow the ratification process in §32.4 before incorporation into a published version.

#### Pilot implementation reports

Organizations running CROA-aligned pilots are encouraged to report:

- which agentic use cases were governed;
- which components (C1–C7) were implemented, and with which technologies;
- which conformance levels were targeted;
- what evidence was produced and what gaps remained;
- what friction points the framework created.

Pilot reports are treated as `implementation-feedback` submissions and inform the framework's evolution without exposing commercially sensitive information (reports may be anonymized).

---

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 33**

- §33.1: Recognition pertains to assessment *practice* (per §29.4), not to conformance outcomes.
- §33.7: Obligations on how the CROA name and the central claim are communicated are **claims-usage obligations** governed by the Brand and Claims Usage Policy and the challenge procedure (§33.5), not conformance criteria of a deployed system; the canonical claim is the conditioned T1 formulation (Part I, Chapter 3). Communications SHOULD foreground the *form* of the guarantee (deterministic, auditable, bounded to the modeled action space, reconstructible from `C5`) rather than a supposed scope, and a showcase headline MUST NOT assert a property the body conditions away (the NovaCare PHI example is bounded per Appendix H §H.6.1).
- §33.2: Registration of a conformance assertion in the **Claims Register** is OPTIONAL and is not a precondition for conformance; a registered assertion MUST carry version, level, boundary, assessor, and independence basis. The Claims Register records conformance claims only; adoption-status declarations are kept separately (§33.3).
- §33.3: A profile MUST NOT relax, remove, or contradict any normative requirement of the version it profiles; a derivative work MUST cite the version it builds on, state deviations, and MUST NOT imply steward endorsement absent recognition.
- §33.4: Certification, training, and reference implementations MUST NOT introduce normative requirements or condition use of the standard on their purchase.
- §33.5: The steward MUST operate a public, documented procedure for interpretation requests, conformance-claim challenges, and appeals; adjudication MUST NOT be performed by a party with a material commercial interest in the outcome.

**Cross-references.** Chapter 33 depends on the conformance model (Part VI, Chapters 28–29) and the neutrality commitments (§32.2). The registry applies the version-naming requirement of §31.1.

---

## Part VII Conformance Requirements

Part VII governs the standard and its derivative works rather than a deployed system. A published version of the standard, and any work claiming a relationship to it, conforms with Part VII if and only if:

**Version integrity.** The published version carries a MAJOR.MINOR.PATCH identifier on every Part, and its identifiers satisfy the stability rules of §31.2. Verifiable by: inspection of the published version.

**Neutrality.** No normative requirement names a mandatory vendor, tool, product, or implementation, and conformance is definable from Parts I–VI without reference to any particular implementation or commercial program (§32.2). Verifiable by: inspection of normative content.

**Open implementability.** Implementing the standard requires no license, fee, or commercial program from the steward, and the standard text is published under a stated license (§32.2, §32.6). Verifiable by: inspection of the published license and normative content.

**Governed change.** Every normative change between versions is classed per §31.3, ratified per §32.4, and recorded publicly with rationale. Verifiable by: the public change record.

**Faithful derivation.** A profile or derivative work does not relax, remove, or contradict any normative requirement of the version it builds on, cites that version, and states its deviations (§33.3). Verifiable by: comparison of the derivative work against the cited version.

A version or derivative work that fails any single criterion does not have a recognized Part VII conformance relationship. Partial conformance is not recognized.

---

## Community Participation

> *Non-normative. This closing section invites participation in the public review of the CROA framework. It imposes no conformance obligation.*

The CROA framework is entering a public review and experimentation phase.

Practitioners, architects, governance specialists, researchers, and organizations are encouraged to provide feedback, challenge assumptions, and share implementation experiences.

Future revisions of the framework may incorporate community feedback and lessons learned from real-world applications.

**How to engage.** During the public review period, the CROA Project welcomes:

- **Evaluation feedback** — clarity, completeness, and internal consistency of the specification, surfaced through the interpretation-request and challenge procedure stewarded under §33.5.
- **Pilot reports** — experiences from applying the CROA Development Cycle (Part III) and the conformance model (Part VI) to real or representative agentic workloads, including where the framework was difficult to apply or appeared to over- or under-constrain.
- **Threat and failure-mode contributions** — additional manifestation patterns, detection signatures, or mitigations relevant to the Part V threat model.
- **Mapping contributions** — corrections or extensions to the framework and regulatory mappings (Appendices D–F, M, N) and the adjacent-mechanism comparison (Appendix O).

Contributions are reviewed under the neutrality and governed-change commitments of this Part (§32.2, §32.4): no contribution confers endorsement, and every normative change between versions is classed (§31.3), ratified (§32.4), and recorded publicly with rationale. Participation channels are published by the CROA Project with each released version.

---

*End of Part VII — Governance of the Standard.*
*End of the CROA Framework — Official Specification v1.0.1 (editorial version v1.0.1; Parts I–VII).*
