# CROA Public Review Program

CROA is a published document. This program exists to make it a tested one.

Its purpose is not to convince you that CROA is correct — it is to give you enough to find out whether
it is, and to put whatever you find on the public record.

---

## What we are asking for

In order of value to the project:

1. **Falsification.** Show us where the central claim does not hold. (→ *Discussions → Challenge the Claim*, or a [Challenge the Claim issue](https://github.com/CROA-Project/CROA/issues/new?template=challenge-the-claim.yml).)
2. **Implementation evidence — including failures.** Build CROA, or part of it, and tell us what worked, what didn't, and what it cost. (→ [Pilot Program](pilot-program.md), [Evidence reports](../evidence/README.md).)
3. **Scrutiny of the open questions.** Help us resolve the things we genuinely don't know yet. (→ [Research Questions](research-questions.md).)
4. **Specification review.** Find ambiguities, conformance gaps, and internal conflicts. (→ Issue templates.)

You do not have to agree with CROA to take part. A rigorous objection is one of the most valuable contributions you can make.

## How to participate (pick your level)

| Level | Effort | What you do |
|---|---|---|
| **Comment** | minutes | React to an open question or claim in Discussions. The cheapest way to start. |
| **Reviewer** | hours/month | Join the review pool; review RFCs and findings in your area of expertise. See [reviewer onboarding](reviewer-onboarding.md). |
| **Pilot implementer** | weeks | Implement CROA against a real (or realistic) system and publish an evidence report. See the [Pilot Program](pilot-program.md). |
| **Review board member** | ongoing | By invitation, after sustained contribution; helps steer review priorities and FCP dispositions. |

## Scope of this review round (v1.0)

**In scope:** the central claim and its conditions; the reference architecture (C1–C7) and trust boundaries; the conformance model (L0–L5); the threat model; the schemas; implementation feasibility, cost, and developer experience; the open [research questions](research-questions.md).

**Out of scope for this round:** rebranding/renaming debates, governance restructuring beyond what is in `GOVERNANCE.md`, and feature requests unrelated to the core guarantee. (These are welcome later; flagging scope keeps the round productive.)

## Timeline (phase-based, not date-locked)

We deliberately gate on outcomes, not dates — date-driven specs slip and signal it.

| Phase | Goal | Exit criterion |
|---|---|---|
| **R0 — Seeding** | A small cohort of invited reviewers stress-tests the draft and the harness before wide announcement. | The harness runs cleanly for outside reviewers; the top open questions are sharp and answerable. |
| **R1 — Open review** | Public call. Collect challenges, clarifications, and conformance-gap findings. | Triage backlog stable; recurring themes identified; first RFCs opened from findings. |
| **R2 — Pilots** | Independent teams implement CROA and publish evidence. | ≥ 3 independent evidence reports, including at least one partial/failed implementation. |
| **R3 — Consolidation** | Fold validated findings into the spec via RFCs; publish a v1.0 final draft. | Open normative conflicts resolved or documented; changelog complete; v1.0 released. |

Progress is tracked publicly in the open — through labeled, linked issues and, once opened, a GitHub **Projects** board (its link will be added here when it exists).

## How findings are handled

```text
finding (issue/discussion) → triage → accepted → [needs-rfc?] → resolved/RFC → changelog
```

- Every accepted finding is labeled and linked in the open (and surfaced on the project board once it exists). **Nothing disappears silently.**
- Findings that imply a normative change go through the [RFC process](../rfcs/README.md).
- Maintainers commit to acknowledging every well-formed finding, even when the answer is "no, and here's why."
- **Evidence outweighs opinion.** A reproducible result or a real implementation report carries more weight than a preference.

## The review board

During Public Review the review board is advisory and lightweight:

- **Composition:** maintainers + invited reviewers spanning multiple organizations and disciplines (architecture, security, AI, governance, academia).
- **Role:** prioritize review themes, weigh in on FCP dispositions, and safeguard the principles in `GOVERNANCE.md` (neutrality, evidence, transparency).
- **Path:** as the project matures, the board's advisory votes become binding under the Technical Steering Committee (`GOVERNANCE.md` §5).

Board membership is earned through sustained, substantive contribution — not appointed for affiliation or title.

## What success looks like

This program has succeeded if, at the end of v1.0 review, we can point to: independent attempts to break the central claim and what they found; at least one real implementation *and* at least one honest failure; a set of open questions that are now smaller and sharper; and a specification changed by evidence, in public, with every decision traceable.

→ Start with the [Research Questions](research-questions.md), or open a [Challenge the Claim](https://github.com/CROA-Project/CROA/issues/new?template=challenge-the-claim.yml) issue.
