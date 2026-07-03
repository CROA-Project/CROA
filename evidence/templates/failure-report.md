---
report_type: failure
title: <short descriptive title>
organization: <name or pseudonym>
date: <YYYY-MM-DD>
croa_version: <e.g. v1.0 Public Review Draft>
related_research_questions: [<e.g. RQ-4, RQ-7>]
outcome: <abandoned | partial-then-stopped | failed-to-meet-goal>
---

# Failure / lessons-learned report — <title>

> Thank you for writing this. Negative results are the most valuable evidence we receive, and they are treated as a first-class contribution — never as a mark against you or against CROA.

## Summary

What you set out to do, and what stopped you, in a few sentences.

## What you were trying to achieve

The workflow, the slice of CROA, and the goal (e.g., "govern `data.export` to L4 on a real CRM").

## Where it broke down

The specific obstacle(s). Choose all that apply and explain:

- [ ] **Conceptual** — the spec was unclear or seemed internally inconsistent (link issues).
- [ ] **Cost** — too much effort to implement or operate (where, and how much).
- [ ] **Performance** — overhead or bottleneck made it impractical (numbers if available).
- [ ] **Dependency** — couldn't build a usable Golden Record / couldn't enforce P4 / etc.
- [ ] **Friction** — too many legitimate actions were blocked.
- [ ] **Fit** — CROA was the wrong tool for this problem (why).
- [ ] **Organizational** — non-technical blockers (resourcing, priorities).

## What you tried before stopping

Workarounds attempted, and why they didn't resolve it.

## What would have changed the outcome

What in the framework, tooling, or guidance — if it had existed or been different — would have let you succeed?

## Findings against the research questions

For each related `RQ-`: what does this failure tell us?

## Anything reusable

Even from a failure: a config, a counter-example, a diagram, a sharpened question.
