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

See Appendix B (Notation, Identifiers and Symbols) of the specification for the namespace and
enumeration index.
