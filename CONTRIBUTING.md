# Contributing to CROA

**Objective:** make it easy — and intellectually attractive — to participate, and make clear that *challenging* CROA is as welcome as supporting it.

**Audience:** anyone, from a researcher with a counter-example to a team running CROA in production.

CROA is in **Public Review**. The most valuable contribution right now is not a feature — it is **evidence** and **scrutiny**.

---

## What we most want

In rough order of value to the project today:

1. **Challenges to the central claim.** Scenarios or arguments where invariant-violating execution paths are *not* structurally unreachable under the stated conditions. → *Discussions → Challenge the Claim.*
2. **Evidence reports — including failures.** You implemented CROA (or part of it) and it worked, partly worked, or didn't. Failed and abandoned implementations are especially valuable; they tell us where the architecture is too costly or unclear. → [`evidence/README.md`](evidence/README.md).
3. **Conformance gaps and ambiguities.** Places where the spec is unclear, internally inconsistent, or under-specified for real implementation. → open an Issue.
4. **Reference-harness improvements.** Bugs, additional negative tests, new adapters. → the [`croa-reference-harness`](https://github.com/croa-project/croa-reference-harness) repo.
5. **Normative proposals.** Changes to requirements, schemas, or the conformance model. → the [RFC process](rfcs/README.md).

You do **not** need to be an expert, and you do not need to agree with CROA to contribute. A well-reasoned objection is a contribution.

## Where things go

| You have… | Use… |
|---|---|
| An open-ended argument, doubt, or idea | **Discussions** (Challenge the Claim, Governance, RFC Pre-Discussion) |
| A specific, trackable defect or gap | **Issue** (pick the matching template) |
| Results from implementing CROA | **Evidence report** (PR into `evidence/reports/`) |
| A proposed change to the framework | **RFC** ([rfcs/](rfcs/README.md)) |
| A fix to docs, links, or the harness | **Pull request** |

When in doubt, open a Discussion. Maintainers will help route it.

## Contribution workflow

1. **Discuss first** for anything non-trivial. It saves everyone effort and is how RFCs are socialized.
2. **Fork and branch.** Use a descriptive branch name (`clarify-c4-trajectory-state`, `evidence-acme-pilot`).
3. **Make focused changes.** One concern per pull request. Run the markdown linter and link-checker (CI will too).
4. **Open a pull request** against `main`, referencing any related Issue or RFC. Fill in the PR template.
5. **Add a DCO sign-off to your commits** — `git commit -s` (this is a Developer Certificate of Origin sign-off, not a cryptographic commit signature; see *Developer Certificate of Origin* below).
6. **Engage with review.** Maintainers and reviewers will respond in the open.

Normative changes are **not** merged by PR alone — they must go through an accepted RFC first. The PR then implements the RFC.

What happens to your pull request after you open it — which checks run, how many approvals are needed, and why some surfaces need two — is described in [`.github/REVIEW_AND_MERGE.md`](.github/REVIEW_AND_MERGE.md).

## Developer Certificate of Origin (DCO)

All commits must be signed off, certifying you have the right to submit the work under the project's licenses:

```text
git commit -s -m "Your message"
```

This adds a `Signed-off-by:` line ([DCO 1.1](https://developercertificate.org/)). We use DCO rather than a CLA to keep the barrier to contribution low and to preserve the project's vendor-neutral, no-single-owner posture.

## Licensing of contributions

By contributing you agree that your contribution is licensed under the project's terms:

- **Documentation and specification text** under **CC BY 4.0**;
- **Code and machine-readable artifacts** under **Apache-2.0**.

## Style and quality bar

- **Credibility over persuasion.** Write like a systems engineer documenting a result, not like marketing. Claims are conditioned and cited.
- **Normative precision.** RFC 2119 keywords (MUST/SHOULD/MAY) carry their formal meaning; use them deliberately.
- **No silent normative drift.** If a change alters a requirement, say so and classify it (editorial → extension).
- CI runs a Markdown linter and a link-checker on every pull request (see `.github/workflows/`); a clean run is expected before a release but is neither necessary nor sufficient for conformance.

## Recognition

Contributors are credited in release notes and in `CONTRIBUTORS.md`. Pilot implementers and reviewers who produce substantive evidence are acknowledged in the corresponding reports and may be invited into the review board.

## Getting started

- Read [`docs/why-croa.md`](docs/why-croa.md) and the one-page [`docs/architecture-overview.md`](docs/architecture-overview.md).
- Run the [Quick Start](docs/quick-start.md) (≤15 minutes).
- Browse issues labeled [`good-first-challenge`](.github/labels.yml).
- Skim the open [`research-questions.md`](public-review/research-questions.md) and pick one to poke at.

By participating you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
