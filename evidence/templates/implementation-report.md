---
report_type: implementation        # implementation | benchmark | architecture-review | adoption-story
title: <short descriptive title>
organization: <name or pseudonym>
authors: [<name / handle, optional>]
date: <YYYY-MM-DD>
croa_version: <e.g. v1.0 Public Review Draft>
related_research_questions: [<e.g. RQ-5, RQ-12>]
related_issues: [<links, optional>]
---

# Implementation report — <title>

## Summary

Three to five sentences: what you implemented, the headline outcome, and the single most useful thing you learned.

## Context

- **Workflow governed:** what the agent(s) do, and against which systems.
- **Why CROA:** what problem you were trying to address.
- **Environment:** scale, stack, constraints (anonymize as needed).

## Scope of implementation

What you implemented and — just as important — what you deliberately did **not**.

| CROA element | Implemented? | Notes |
|---|---|---|
| Admission (RBAC / AQL) | yes / partial / no | |
| C3 context grounding (Golden Record) | | |
| C2 evaluation (E1/E2/E3 invariants) | | |
| C7 compiled commitment | | |
| C6 execution-boundary enforcement (P4) | | |
| C5 audit (append-only, chained) | | |
| C4 trajectory monitoring | | |
| Conformance level targeted | L? | |

## What worked

The parts that behaved as the framework predicts. Be specific.

## What didn't (or surprised you)

Where the spec was unclear, the cost was higher than expected, or behavior diverged. **This section is the point of the report — don't soften it.**

## Cost & friction

- **Integration effort:** rough person-time to first governed action.
- **Performance:** latency added per action; throughput ceiling; C5 write behavior (for RQ-5 / RQ-6).
- **Friction:** false-positive / deny rate; how often legitimate work was blocked (RQ-3).
- **Maintenance:** Golden Record / invariant upkeep observed or anticipated (RQ-7, RQ-9).

## Findings against the research questions

For each related `RQ-`: what does your experience suggest? Be explicit about confidence and limits.

## Would you continue / recommend?

Your honest assessment, with the conditions under which it holds.

## Artifacts (optional)

Links to code, configs, sample `C5` logs, dashboards — anything reproducible.
