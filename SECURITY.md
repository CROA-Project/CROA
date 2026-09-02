# Security & Responsible Disclosure

CROA is an architecture, not a deployed service — but two kinds of "security" report matter to this project, and we want both.

## 1. Flaws in the architecture or its claims

If you believe you have found a way to **defeat CROA's central guarantee** — a class of attack or a condition under which invariant-violating execution becomes reachable despite a conformant deployment — that is exactly the scrutiny this project exists to invite.

- If it is **not sensitive**, please open it in the open: *Discussions → Challenge the Claim*, or a [Challenge the Claim issue](https://github.com/CROA-Project/CROA/issues/new?template=challenge-the-claim.yml). Public scrutiny is the point.
- If you believe public disclosure could **enable harm to live deployments** before they can respond, email the maintainers privately first (see below). We will coordinate a responsible, time-bounded disclosure and credit you.

## 2. Vulnerabilities in the reference harness or tooling

For defects in the [Minimal Reference Harness](https://github.com/CROA-Project/croa-reference-harness) or repository tooling that have a security impact (e.g., the harness could be made to forge a `C5` event, or break chain verification), please **report privately first**:

- Email: **<croaproject@gmail.com>** (use a subject line starting with `[SECURITY]`). This is the channel we monitor. If GitHub's private vulnerability reporting is available to you on the repository, that works too.
- Do not open a public issue until we have acknowledged and agreed on a disclosure timeline.

## What to expect

- **Acknowledgement** within a few business days.
- A good-faith effort to assess and, where applicable, fix or document the issue.
- **Credit** for the reporter, unless you prefer to remain anonymous.
- For architecture-level findings, transparent handling through the normal review/RFC process once any deployment risk is managed.

## Scope note

Because CROA's guarantee is explicitly *conditioned* (modeled action space, registered invariants, network-enforced containment), a "vulnerability" that relies on violating those stated conditions is a finding about the **conditions' achievability** (valuable — see research questions RQ-2, RQ-8) rather than a break of the claim as stated. Both are welcome; please note which you believe it is.
