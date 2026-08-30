# Core Team

The core team is the group that **writes the framework**: the specification, the threat model, the method, and the conformance material. Its members hold write authority over the specification and decide, collectively, what enters it.

Members join at different times. That is the only difference between them: the published versions credit the authors who wrote them, and later members are not retroactively credited. Going forward, the framework is written by this team.

| Name | GitHub | Affiliation | Area(s) |
|---|---|---|---|
| Yasmine Durand | [`Yaouldha`](https://github.com/Yaouldha) | The CROA Project | Architecture, governance, conformance |
| Darrin Smith | [`darrinps`](https://github.com/darrinps) | The CROA Project | Architecture, threat model, method |
| Sylvain Durand | [`sdurand06`](https://github.com/sdurand06) | The CROA Project | Architecture, adoption method, conformance |

*Affiliations are disclosed for transparency. Core team members are bound by the neutrality commitment in `GOVERNANCE.md` §2: no implementation, commercial or otherwise, receives privileged standing.*

## Maintainers within the core team

**Maintainers** ([`MAINTAINERS.md`](MAINTAINERS.md)) are core team members who additionally carry the operational load of the project during Public Review: triage, release management, running the RFC process, and final call on merges. It is a function held within the core team, not a rank above it.

## How the core team works with implementers

The core team does not decide in a vacuum. **Pilot Implementers** (`GOVERNANCE.md` §3) build CROA against real systems and publish evidence reports — including failures, which are the most valuable kind. The core team examines those findings and decides whether the framework must change; a report that surfaces a genuine gap becomes an RFC.

That loop is the point of the Public Review phase: the framework is written here, but it is tested out there.

## Joining

There is no application process. The core team invites contributors whose work on the specification has been sustained and substantive. Active reviewers and pilot leads are natural candidates — see the [Public Review Program](public-review/README.md).

## Relationship to the other roles

- **Core team** (this file) — writes the framework.
- **Maintainers** ([`MAINTAINERS.md`](MAINTAINERS.md)) — core team members holding the operational duties.
- **Pilot Implementers** — implement CROA and report evidence that the core team acts on.
- **Reviewers** ([`REVIEWERS.md`](REVIEWERS.md)) — recurring review of RFCs and findings.
- **Contributors** ([`CONTRIBUTORS.md`](CONTRIBUTORS.md)) — everyone else who improves the project.

All roles are defined in [`GOVERNANCE.md`](GOVERNANCE.md) §3.
