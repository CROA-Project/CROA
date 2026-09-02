---
rfc: 0002
title: Move the schema namespace off croa.foundation and drop "Standard" from the schema descriptions
status: draft
change_level: normative-correction
authors: [Yasmine Durand, Darrin Smith]
created: 2026-09-02
affects: [spec/schemas/cc.schema.json, spec/schemas/event.schema.json, spec/schemas/gar.schema.json, spec/schemas/gga.schema.json, spec/schemas/README.md]
tracking_issue: (opened with the pull request that lands this file)
fcp_opens: 2026-09-02
fcp_closes: 2026-09-16
---

# RFC 0002 — Schema namespace and "Standard"

> **This RFC follows the process.** The Final Comment Period runs from **2 September 2026 to
> 16 September 2026**, and the schemas are **not** changed until it closes — even though the change
> is a two-line correction everyone already agrees with. That is exactly why it is worth doing this
> way: the last two normative changes bypassed this process
> ([`GOVERNANCE-DEVIATIONS.md`](../../GOVERNANCE-DEVIATIONS.md)), each time because the change seemed
> too obvious to wait for. A project whose entire argument is that constraints should be hard to
> bypass cannot keep making exceptions for its own convenience. The defect is meanwhile recorded as
> erratum **E-15**, so no reader is misled while the period runs.
>
> **Objections are wanted, not merely tolerated.** If the namespace proposed below is the wrong one,
> saying so before 16 September costs the project nothing and saves it a second rename.

## Summary

The four machine-readable schemas carry `$id` values under
`https://croa.foundation/standard/v1/schemas/` and describe their normative source as the "CROA
Standard". Both are wrong on the project's own terms. This RFC replaces the namespace with one under
the repository the project actually controls, and replaces "CROA Standard" with "CROA specification".

## Motivation

An independent audit in September 2026 raised this, and it is correct on two counts.

**"foundation".** [`spec/README.md`](../../spec/README.md) states that the project operates as **The
CROA Project**, and that "Foundation" is reserved for a future independent entity that has not been
incorporated. A schema `$id` naming a foundation that does not exist asserts an institutional
standing the project explicitly disclaims elsewhere in the same repository. The domain is also not
resolvable, so the `$id` dereferences to nothing.

**"standard".** The corpus says on its front page that CROA is a **Public Review Draft** and "not a
finished or formally recognized standard". The schemas contradict that in their own description
field — which is the part a tool reads.

Neither is a drafting nicety. The audit's finding F-11 is that the project's institutional claims are
inconsistent across artifacts, and inconsistency of that kind is exactly what a reviewer uses to
decide how carefully to read the rest.

## Change level and impact

**Normative-correction.**

- **Changed:** the `$id` of four schemas, and the wording "CROA Standard" in four `description`
  fields.
- **Not changed:** every property, type, constraint and required field. No instance that validates
  today stops validating.
- **Backward compatibility:** a `$id` is an identifier, not an endpoint, and nothing in the corpus
  resolves these URIs at runtime. An implementation that pinned the old `$id` string must update it;
  we know of none, and the schemas have been public for one week.

## Detailed design

Replace, in each of the four files:

```diff
-  "$id": "https://croa.foundation/standard/v1/schemas/cc.schema.json",
+  "$id": "https://raw.githubusercontent.com/CROA-Project/CROA/main/spec/schemas/cc.schema.json",
```

and identically for `event`, `gar` and `gga`.

In each `description`, `CROA Standard Part II §…` becomes `the CROA specification, Part II §…`.

Add to [`spec/schemas/README.md`](../../spec/schemas/README.md) a note that the `$id` tracks `main`
during Public Review, and that it will be repointed at an immutable release tag when the first tagged
release is cut — which is the subject of the release-identity work in erratum **E-14**.

## Alternatives considered

**Do nothing.** Rejected: the schemas would keep asserting a foundation that does not exist and a
standard status the project disclaims.

**Register and use a real `croa.foundation` domain.** Rejected for now. It would make the `$id`
resolvable, but it would also entrench "Foundation" as the project's identity before any entity
exists — the opposite of what `spec/README.md` says. Revisit if and when an entity is incorporated.

**Use a URN (`urn:croa:spec:v1:cc`).** Legitimate, and immune to hosting changes. Rejected because a
dereferenceable `$id` is more useful to implementers and tooling, and the repository is the honest
authority for now.

**Pin the `$id` to a release tag immediately.** Deferred rather than rejected: there is no tagged
release whose contents match the Zenodo deposit (erratum E-14). Doing this properly is release-identity
work, not a namespace rename, and bundling them would delay both.

## Risks and drawbacks

- **A `main`-tracking `$id` is mutable.** It identifies a moving target, which is a real weakness for
  a normative artifact. It is an improvement on an unresolvable URI naming a non-existent entity, and
  it is explicitly temporary.
- **Churn.** Anyone who has already copied a schema sees its identifier change. One week of exposure
  makes this small, and doing it later makes it larger.

## Open questions

1. Should the eventual permanent namespace be a project-owned domain, a release-tagged GitHub URL, or
   a URN? This decides itself once release identity (E-14) is settled.
2. Should the schemas carry an explicit `$comment` recording the specification version and DOI they
   correspond to, so a copied file remains traceable?

## Prior art

JSON Schema's own guidance is that `$id` should be a URI the schema's author controls and, where
practical, one that dereferences. Projects at a comparable stage commonly use a raw repository URL
and repoint it at a stable host on first release; W3C and IETF drafts similarly carry
draft-scoped identifiers until ratification.
