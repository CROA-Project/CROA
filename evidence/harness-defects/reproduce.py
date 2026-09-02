#!/usr/bin/env python3
"""Dated reproduction of harness defects H-01, H-02 and H-03, as they stood on
2 September 2026 — BEFORE the fix.

Run:  python3 reproduce.py
Exit: 1, always, by design. See below.

WHAT THIS IS. A frozen snapshot. It copies the relevant classes from
croa-reference-harness verbatim as they were published before the fix, so that the three
defects can still be observed by anyone, on any machine, with no clone and no dependency,
long after the code has changed. It is the evidence that the defects were real.

WHAT THIS IS NOT — a correction to an earlier claim. When this file was first published,
its README described it as "a regression gate once the defects are fixed". **That was
wrong**, and the mistake is instructive: because the code is copied rather than imported,
this script tests the copy and would go on reporting the defects for ever, no matter what
the real harness did. A gate that cannot fail is not a gate.

THE ACTUAL REGRESSION GATE is the harness's own test suite, which now contains
`TestAdversarial` — including h01/h02/h03/h04 and two 100-thread races. Run it there:

    git clone https://github.com/CROA-Project/croa-reference-harness.git
    cd croa-reference-harness && make test

Findings and their current status are in spec/known-defects-harness.md.
"""
import hashlib
import hmac
import json
import uuid
import datetime

# --------------------------------------------------------------- from mrh/audit.py
_DEMO_KEY = b"CROA-MRH-DEMO-KEY-not-for-production"
GENESIS = "0" * 64


def _canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"))


def _sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


class AuditStore:
    def __init__(self):
        self.events = []
        self._prev = GENESIS

    def emit(self, etype, emitter_id, subject_id, **fields):
        ev = {
            "event.id": "evt-" + uuid.uuid4().hex[:16],
            "event.type": etype,
            "event.timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event.subject_id": subject_id,
            "event.emitter_id": emitter_id,
            "event.chain_hash": self._prev,
        }
        ev.update(fields)
        ev["event.emitter_signature"] = hmac.new(
            _DEMO_KEY, _canon(ev).encode(), hashlib.sha256
        ).hexdigest()
        self.events.append(ev)
        self._prev = _sha(_canon(ev))
        return ev

    def verify(self):
        prev = GENESIS
        for ev in self.events:
            if ev["event.chain_hash"] != prev:
                return False, f"chain break at {ev['event.id']}"
            unsigned = {k: v for k, v in ev.items() if k != "event.emitter_signature"}
            sig = hmac.new(_DEMO_KEY, _canon(unsigned).encode(), hashlib.sha256).hexdigest()
            if sig != ev["event.emitter_signature"]:
                return False, f"bad signature at {ev['event.id']}"
            prev = _sha(_canon(ev))
        return True, f"chain verified: {len(self.events)} events, unbroken"


# ---------------------------------------------------------- from mrh/components.py
_CC_KEY = b"CROA-MRH-CC-DEMO-KEY"


class PolicyAuthority:
    def __init__(self, approved_export_targets):
        self.approved_export_targets = set(approved_export_targets)
        self.redeemed_auths = set()

    def violated_invariants(self, action):
        v = []
        if (action["action_class"] == "data.export"
                and action["target"] not in self.approved_export_targets):
            v.append("I-EXPORT-001")
        return v

    def issue_authorization(self, action, now, ttl=60):
        auth = {
            "auth_id": "auth-" + uuid.uuid4().hex[:12],
            "action_fingerprint": hashlib.sha256(_canon(action).encode()).hexdigest(),
            "expiry": now + ttl,
        }
        auth["signature"] = hmac.new(_CC_KEY, _canon(auth).encode(), hashlib.sha256).hexdigest()
        return auth

    def authorization_covers(self, auth, action, now):
        if auth is None:
            return False
        unsigned = {k: v for k, v in auth.items() if k != "signature"}
        if hmac.new(_CC_KEY, _canon(unsigned).encode(), hashlib.sha256).hexdigest() != auth["signature"]:
            return False
        if now > auth["expiry"]:
            return False
        if auth["auth_id"] in self.redeemed_auths:
            return False
        return auth["action_fingerprint"] == hashlib.sha256(_canon(action).encode()).hexdigest()

    def redeem_authorization(self, auth_id):
        self.redeemed_auths.add(auth_id)


class PathResolver:
    def __init__(self, golden_record):
        self.golden_record = set(golden_record)

    def resolve(self, target):
        return target in self.golden_record


class ExecutionGovernor:
    def __init__(self, c1):
        self.c1 = c1

    def evaluate(self, action, authorization, now):
        violations = self.c1.violated_invariants(action)
        if not violations:
            return "PERMIT", "no registered invariant violated"
        if self.c1.authorization_covers(authorization, action, now):
            return "PERMIT_WITH_AUTHORIZATION", "covered by " + authorization["auth_id"]
        return "DENY", "violates " + ",".join(violations)


class ContractCompiler:
    def compile(self, action, now, authorization=None, ttl=300):
        cc = {
            "cc.id": "cc-" + hashlib.sha256(
                (_canon(action) + uuid.uuid4().hex).encode()
            ).hexdigest()[:16],
            "action": action,
            "expiry": now + ttl,
            "single_use": True,
        }
        if authorization is not None:
            cc["auth_ref"] = authorization["auth_id"]
        cc["signature"] = hmac.new(
            _CC_KEY, _canon({k: v for k, v in cc.items()}).encode(), hashlib.sha256
        ).hexdigest()
        return cc


class ExecutionFirewall:
    def __init__(self):
        self.redeemed = set()

    def _sig_ok(self, cc):
        unsigned = {k: v for k, v in cc.items() if k != "signature"}
        return hmac.new(
            _CC_KEY, _canon(unsigned).encode(), hashlib.sha256
        ).hexdigest() == cc["signature"]

    def redeem(self, cc, now):
        if cc is None:
            return "BLOCKED", "CC_NOT_FOUND"
        if not self._sig_ok(cc):
            return "BLOCKED", "CC_SIGNATURE_INVALID"
        if now > cc["expiry"]:
            return "BLOCKED", "CC_EXPIRED"
        if cc["cc.id"] in self.redeemed:
            return "BLOCKED", "CC_ALREADY_REDEEMED"
        self.redeemed.add(cc["cc.id"])
        return "AUTHORIZED", None


# ------------------------------------------------------------ from mrh/harness.py
class Harness:
    def __init__(self):
        golden = {"orders-db", "crm", "billing", "reporting-api"}
        self.c1 = PolicyAuthority(approved_export_targets={"crm"})
        self.c3 = PathResolver(golden)
        self.c2 = ExecutionGovernor(self.c1)
        self.c7 = ContractCompiler()
        self.c6 = ExecutionFirewall()
        self.c5 = AuditStore()

    def present(self, cc, now, sid):
        status, br = self.c6.redeem(cc, now)
        if status == "AUTHORIZED":
            fields = {"event.cc_id": cc["cc.id"]}
            auth_ref = cc.get("auth_ref")
            if auth_ref is not None:
                self.c1.redeem_authorization(auth_ref)
                fields["event.auth_id"] = auth_ref
            self.c5.emit("EXECUTION_AUTHORIZED", "C6", sid, **fields)
            return {"admitted": True}
        self.c5.emit(
            "EXECUTION_BLOCKED", "C6", sid,
            **{"event.block_reason": br, "event.cc_id": (cc or {}).get("cc.id")}
        )
        return {"admitted": False, "block_reason": br}


# ============================================================== reproductions
reproduced = []


def h01():
    """H-01 — one single-use exception authorization admits two executions.

    Expected under P-D / NT-007: at most one admitted execution per authorization.
    """
    print("\n--- H-01  one exception authorization, two admitted executions ---")
    h, now = Harness(), 1000
    action = {"action_class": "data.export", "target": "billing",
              "subject_id": "subject-A", "params": {"rows": 100}}
    assert h.c1.violated_invariants(action), "the action must violate an invariant"

    auth = h.c1.issue_authorization(action, now)
    print(f"  authorization issued  : {auth['auth_id']}  (documented as single-use)")

    # Both decisions are taken BEFORE any redemption. Nothing in the design prevents this.
    d1, _ = h.c2.evaluate(action, auth, now)
    d2, _ = h.c2.evaluate(action, auth, now)
    print(f"  two C2 decisions      : {d1} / {d2}")

    cc1 = h.c7.compile(action, now, authorization=auth)
    cc2 = h.c7.compile(action, now, authorization=auth)
    print(f"  two commitments       : {cc1['cc.id']} / {cc2['cc.id']}")

    r1 = h.present(cc1, now, "subject-A")
    r2 = h.present(cc2, now, "subject-A")
    ok, msg = h.c5.verify()
    n = sum(1 for e in h.c5.events if e["event.type"] == "EXECUTION_AUTHORIZED")

    print(f"  first presentation    : admitted={r1['admitted']}")
    print(f"  second presentation   : admitted={r2['admitted']}")
    print(f"  EXECUTION_AUTHORIZED  : {n} in the C5 log")
    print(f"  C5.verify()           : {ok}  ({msg})")

    if r1["admitted"] and r2["admitted"]:
        reproduced.append("H-01")
        print("  >>> REPRODUCED: two executions from one single-use authorization")
        if ok:
            print("  >>> and C5 reports the chain as valid (this is H-04)")
    else:
        print("  >>> not reproduced")


def h02():
    """H-02 — a commitment compiled for one subject is admitted under another."""
    print("\n--- H-02  subject substitution at the execution boundary ---")
    h, now = Harness(), 1000
    action = {"action_class": "data.read", "target": "crm",
              "subject_id": "subject-A", "params": {}}
    assert not h.c1.violated_invariants(action)

    cc = h.c7.compile(action, now)
    print(f"  commitment compiled for : {cc['action']['subject_id']}")

    r = h.present(cc, now, "subject-B")   # sid is passed separately and never checked
    logged = [e for e in h.c5.events if e["event.type"] == "EXECUTION_AUTHORIZED"]
    print("  presented on behalf of  : subject-B")
    print(f"  admitted                : {r['admitted']}")
    if logged:
        print(f"  C5 recorded             : {logged[0]['event.subject_id']}")

    if r["admitted"] and logged and logged[0]["event.subject_id"] == "subject-B":
        reproduced.append("H-02")
        print("  >>> REPRODUCED: subject-A's commitment admitted and attributed to subject-B")
    else:
        print("  >>> not reproduced")


def h03():
    """H-03 — cc.id is not the content address of the commitment."""
    print("\n--- H-03  cc.id is not content-addressed ---")
    c7, now = ContractCompiler(), 1000
    action = {"action_class": "data.read", "target": "crm", "subject_id": "s", "params": {}}
    a = c7.compile(action, now)["cc.id"]
    b = c7.compile(action, now)["cc.id"]
    digest = hashlib.sha256(_canon(action).encode()).hexdigest()[:16]
    print(f"  same action, compiled twice : {a} / {b}")
    print(f"  sha256(canonical action)    : cc-{digest}")
    if a != b:
        reproduced.append("H-03")
        print("  >>> REPRODUCED: a random uuid4 is mixed in, so the identifier is not deterministic")
    else:
        print("  >>> not reproduced")


if __name__ == "__main__":
    import sys
    print("CROA Minimal Reference Harness — defect reproduction")
    print("Code copied verbatim from CROA-Project/croa-reference-harness@main")
    h01()
    h02()
    h03()
    print("\n" + "=" * 62)
    print("REPRODUCED:", ", ".join(reproduced) if reproduced else "none")
    print("=" * 62)
    sys.exit(1 if reproduced else 0)
