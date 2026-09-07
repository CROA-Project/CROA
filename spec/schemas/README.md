> **Erratum E-15 — namespace.** These schemas carry `$id` values under
> `https://croa.foundation/standard/v1/` and describe their source as the "CROA Standard". Both
> overstate the project's institutional status: the project operates as **The CROA Project**, and
> CROA is a Public Review Draft, not a recognised standard. Read the `$id` as an opaque identifier.
> A correction is proposed in [RFC 0002](../../rfcs/text/0002-schema-namespace.md) and will land when
> its comment period closes — not before, because the project has stopped making normative changes
> ahead of its own process ([`GOVERNANCE-DEVIATIONS.md`](../../GOVERNANCE-DEVIATIONS.md)).

# CROA v1.0.1 machine-readable schemas

These [JSON Schema](https://json-schema.org/) (draft 2020-12) files are the machine-readable
companions to the field schemas defined normatively in the CROA specification. **The prose
specification (on Zenodo) is authoritative**; these files are provided to make the framework
directly implementable and testable. In any discrepancy, the cited Part/section prevails.

| File | Namespace | Normative source |
|---|---|---|
| `gar.schema.json` | `gar.*` — Governed Action Request | Part II §4.5.1 |
| `gga.schema.json` | `gga.*` — Grounded Governed Action | Part II §4.5.1 |
| `ecc.schema.json` | `ecc.*` — Execution Change Contract | Part II §4.4.1 |
| `event.schema.json` | `event.*` — C5 Governance Event | Part II §4.7.1 |

**Notes.**

- **v1.0.1 renaming.** The `cc.*` namespace ("Compiled Commitment") is retired in favour of `ecc.*`
  (Execution Change Contract). `cc.schema.json` becomes `ecc.schema.json`; `CC_*` block reasons become
  `ECC_*`; `event.cc_id` becomes `event.ecc_id`; and `event.emitter_signature` becomes `event.signature`
  per the §4.7.1 field table. Implementations reading v1.0.0 records should treat the old names as
  aliases for the new ones.
- `ecc.schema.json` carries the governed-exception fields `ecc.decision_basis`, `ecc.auth_ref`, and
  `ecc.exception_scope` (present iff `PERMIT_WITH_AUTHORIZATION`), which make the single-use, per-action
  exception (§4.3.1/§4.8) instantiable and boundary-enforceable. These three are required by §4.3.1,
  §4.8 and NT-007 but are **absent from the §4.4.1 field table** — a v1.0.1 editorial defect; they are
  retained here and each carries a `$comment` naming the section that imposes it.
- `event.schema.json` carries the three effect-attestation types `EXECUTION_COMPLETED`,
  `EXECUTION_FAILED` and `EFFECT_ATTESTED` (§4.7.1), with `event.exit_status`, `event.failure_reason`
  and `event.attestation_reference` required respectively. §4.7.1 names those three fields without the
  `event.` prefix; that is read here as an editorial slip, not a break in the namespace.
- **Deliberately not modelled:** `ecc.integrity_mode`, `ecc.decision_digest`, `event.decision_digest`
  and the error code `ECC_DECISION_BINDING_INVALID`. In v1.0.1 these appear only as four bare sentences
  duplicated at the end of Part II and Part III, outside any field table, with no type, no MUST and no
  binding rule. They are recorded as editorial residue pending a v1.0.2 ruling.
- **Validation gate.** `validate.py` is the Part III §7.2 Step 3 check: it refuses a retired identifier,
  a re-declared editorial residue, an out-of-namespace property, and any drop below the normative floor
  (the three effect-attestation types, both redemption block reasons, `AMBIGUOUS`, and the two
  `gga.semantic_result` values).
- `event.schema.json` records `event.auth_id` and the `AUTHORIZATION_ALREADY_REDEEMED` block reason so
  every use — and refused reuse — of a governed exception is auditable (reference test NT-007).
  `AUTHORIZATION_ALREADY_REDEEMED` is required by §4.8 but missing from the closed `event.block_reason`
  enumeration of §4.7.1 — a v1.0.1 defect; without it NT-007 is not expressible.
- `ecc.schema.json` references `gga.schema.json` (an ECC's `ecc.action` is a grounded governed action with
  `gga.semantic_result = GROUNDED`). Resolve `$ref`s relative to this directory.
- `event.schema.json` uses `if/then` per `event.type` to require the type-specific additional fields
  (e.g., `DENY` → `event.deny_reason`). It leaves `additionalProperties: true` so deployments may add
  extension fields.
- These schemas validate **structure**, not governance semantics: schema-validity is necessary but not
  sufficient for conformance (determinism I2, the integrity chain I3/I6, and monotonicity are
  behavioral properties verified per Part VI §29).

**On interoperability with other evidence formats.** These four schemas are CROA's own event model;
they are not proposed as a general evidence standard, and CROA has no interest in inventing one where
a vendor-neutral format already exists. A `C5` governance event is intended to be mappable onto a
per-decision runtime evidence record — the decision verb, the policy basis, the hash references to
inputs and outputs, and the chain position all have direct counterparts. Work such as AIREP
(arXiv:2608.21363) and the governance-receipt model of arXiv:2606.30970 is a natural interoperability
target; see [`docs/prior-art.md`](../../docs/prior-art.md) §2.2. If you are building a mapping, that is
a welcome contribution and a good candidate for an RFC.

**What an event proves.** A conformant chain establishes the ordering and non-alteration of the
events it contains, and — given a signing key held outside the governed agent's trust domain plus
external anchoring — that they were not forged, and that suppression or truncation of a sealed
segment is detectable. It does not, by itself, establish that
every governed action produced an event: that follows from the fail-closed gate (I6/I6.1) and is
corroborated by the cross-checks of §29.4. The distinction is stated as property **P-E** in
[`spec/properties.md`](../properties.md), which is deliberately named *Decision Reconstructability*
rather than "Evidence Completeness".

See Appendix B (Notation, Identifiers and Symbols) of the specification for the namespace and
enumeration index.
