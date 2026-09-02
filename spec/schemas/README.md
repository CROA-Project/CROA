> **Erratum E-15 — namespace.** These schemas carry `$id` values under
> `https://croa.foundation/standard/v1/` and describe their source as the "CROA Standard". Both
> overstate the project's institutional status: the project operates as **The CROA Project**, and
> CROA is a Public Review Draft, not a recognised standard. Read the `$id` as an opaque identifier.
> A correction is proposed in [RFC 0002](../../rfcs/text/0002-schema-namespace.md) and will land when
> its comment period closes — not before, because the project has stopped making normative changes
> ahead of its own process ([`GOVERNANCE-DEVIATIONS.md`](../../GOVERNANCE-DEVIATIONS.md)).

# CROA v1 machine-readable schemas

These [JSON Schema](https://json-schema.org/) (draft 2020-12) files are the machine-readable
companions to the field schemas defined normatively in the CROA specification. **The prose
specification (on Zenodo) is authoritative**; these files are provided to make the framework
directly implementable and testable. In any discrepancy, the cited Part/section prevails.

| File | Namespace | Normative source |
|---|---|---|
| `gar.schema.json` | `gar.*` — Governed Action Request | Part II §4.5.1 |
| `gga.schema.json` | `gga.*` — Grounded Governed Action | Part II §4.5.1 |
| `cc.schema.json` | `cc.*` — Compiled Commitment (execution commitment) | Part II §4.4.1 |
| `event.schema.json` | `event.*` — C5 Governance Event | Part II §4.7.1 |

**Notes.**

- `cc.schema.json` carries the governed-exception fields `cc.decision_basis`, `cc.auth_ref`, and
  `cc.exception_scope` (present iff `PERMIT_WITH_AUTHORIZATION`), which make the single-use, per-action
  exception (§4.3.1/§4.8) instantiable and boundary-enforceable.
- `event.schema.json` records `event.auth_id` and the `AUTHORIZATION_ALREADY_REDEEMED` block reason so
  every use — and refused reuse — of a governed exception is auditable (reference test NT-007).
- `cc.schema.json` references `gga.schema.json` (a CC's `cc.action` is a grounded governed action with
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
