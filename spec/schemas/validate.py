#!/usr/bin/env python3
"""
Schema validation gate for the CROA Policy-as-Code pipeline.

This is the artifact side of Part III §7.2, Step 3 (Validation): a change request
that touches spec/schemas/ does not merge unless every schema is a valid JSON
Schema draft 2020-12 document, every cross-reference resolves, and the v1.0.1
namespace contract still holds.

Run:  python3 spec/schemas/validate.py [schema_dir]
Exit: 0 clean, 1 on any failure. No network access, no third-party service.
"""
import json, pathlib, sys

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    sys.exit("install the gate's dependencies:  pip install 'jsonschema>=4.18' referencing")

D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent)

EXPECTED = {"gar.schema.json", "gga.schema.json", "ecc.schema.json", "event.schema.json"}

# Identifiers retired in v1.0.1. Checked against declared identifiers only -- property
# keys, enum values, $id and $ref -- never against prose: the migration note in each
# file necessarily names what it retired.
RETIRED = {"cc.schema.json", "CC_COMPILED", "CC_EXPIRED", "CC_NOT_FOUND",
           "CC_SIGNATURE_INVALID", "CC_INVARIANT_STALE", "CC_ALREADY_REDEEMED",
           "event.cc_id", "event.emitter_signature"}


def identifiers(node, out):
    """Every declared identifier in a schema document: keys of properties/$defs,
    enum values, and the $id/$ref URIs. Descriptions and $comments are excluded."""
    if isinstance(node, dict):
        for key in ("properties", "$defs", "definitions", "patternProperties"):
            out |= set(node.get(key, {}))
        out |= {v for v in node.get("enum", []) if isinstance(v, str)}
        for key in ("$id", "$ref"):
            if isinstance(node.get(key), str):
                out.add(node[key].rsplit("/", 1)[-1])
        for v in node.values():
            identifiers(v, out)
    elif isinstance(node, list):
        for v in node:
            identifiers(v, out)
    return out

# Editorial residue ruled out of v1.0.1: must not reappear as a declared field or enum value.
RESIDUE = {"ecc.integrity_mode", "ecc.decision_digest", "event.decision_digest",
           "ECC_DECISION_BINDING_INVALID"}

# Normative floor. Each entry: (schema, must-declare set, source section).
FLOOR = [
    ("event.schema.json", {"EXECUTION_COMPLETED", "EXECUTION_FAILED", "EFFECT_ATTESTED"},
     "event.type", "Part II §4.7.1"),
    ("event.schema.json", {"AUTHORIZATION_ALREADY_REDEEMED", "ECC_ALREADY_REDEEMED"},
     "event.block_reason", "Part II §4.8 / Appendix Q NT-003, NT-007"),
    ("event.schema.json", {"AMBIGUOUS"}, "event.decision_basis", "Part I §2.6 fail-deny"),
    ("gga.schema.json", {"GROUNDED", "CONTEXT_FAILURE"}, "gga.semantic_result", "Part II §4.5.1"),
]

fail = []


def bad(msg):
    fail.append(msg)
    print("FAIL", msg)


def main():
    present = {f.name for f in D.glob("*.schema.json")}
    if present != EXPECTED:
        bad(f"schema set is {sorted(present)}, expected {sorted(EXPECTED)}")

    store = {}
    for name in sorted(present):
        try:
            store[name] = json.loads((D / name).read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            bad(f"{name}: not valid JSON -- {e}")
            continue
        for token in sorted(RETIRED & identifiers(store[name], set())):
            bad(f"{name}: retired v1.0.0 identifier {token!r} is back")

    for name, s in store.items():
        try:
            Draft202012Validator.check_schema(s)
        except Exception as e:
            bad(f"{name}: not a valid draft 2020-12 schema -- {str(e).splitlines()[0]}")
        if s.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            bad(f"{name}: $schema is not draft 2020-12")
        if not s.get("$id", "").endswith(name):
            bad(f"{name}: $id {s.get('$id')!r} does not end in the file name")

        declared = set(s.get("properties", {}))
        for v in s.get("properties", {}).values():
            declared |= set(v.get("enum", []))
        for r in sorted(RESIDUE & declared):
            bad(f"{name}: {r} is editorial residue and must not be declared")

        prefix = name.split(".")[0] + "."
        for k in s.get("properties", {}):
            if not k.startswith(prefix):
                bad(f"{name}: property {k!r} is outside the {prefix}* namespace")

    for name, required, field, source in FLOOR:
        if name not in store:
            continue
        vals = set(store[name].get("properties", {}).get(field, {}).get("enum", []))
        missing = required - vals
        if missing:
            bad(f"{name}: {field} is missing {sorted(missing)} required by {source}")

    # cross-references must resolve inside the directory
    reg = Registry().with_resources(
        [(n, Resource.from_contents(s)) for n, s in store.items()] +
        [(s["$id"], Resource.from_contents(s)) for s in store.values() if "$id" in s])
    for name, s in store.items():
        try:
            Draft202012Validator(s, registry=reg).iter_errors({})
            list(Draft202012Validator(s, registry=reg).iter_errors({"probe": 1}))
        except Exception as e:
            bad(f"{name}: unresolved $ref -- {str(e).splitlines()[0]}")

    if fail:
        print(f"\n{len(fail)} failure(s) -- change request blocked at Validation (Part III §7.2, Step 3)")
        return 1
    print(f"{len(store)} schemas valid; namespace contract and normative floor hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
