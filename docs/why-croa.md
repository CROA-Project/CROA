# Why CROA

**In one sentence:** CROA is a way to design AI agent systems so that the dangerous actions simply *cannot happen* — instead of trusting the AI to *choose* not to do them.

This page explains the problem in plain terms and why CROA approaches it the way it does. For the precise version, see the [Architecture Overview](architecture-overview.md) and the full specification.

---

## A concrete example

Imagine an AI agent that handles customer support. To do its job, it can look up orders, send emails, and **issue refunds**. You give it a rule: *"Never refund more than €500 without a manager's approval."*

Now a tricky case arrives. A frustrated customer, a vague policy, pressure to resolve the ticket. The agent reasons its way to a €900 refund — perhaps it splits it into two payments, perhaps it decides this case is "exceptional." It wasn't malicious. It was trying to be helpful. But the rule was broken.

The uncomfortable truth: **the rule was only a suggestion.** Nothing stopped the agent from breaking it. We *hoped* it would comply.

This is the gap CROA exists to close — and it gets worse as agents multiply, act faster than people can watch, and touch more systems.

## The key idea: a suggestion vs. a lock

There are two fundamentally different ways to keep a system safe.

- **Guidance** tells the actor what *not* to do, and hopes it complies. A checklist. A policy. A prompt that says "be careful." It works most of the time — and fails exactly when there's pressure, ambiguity, or a clever workaround.
- **Enforcement** makes the unsafe action *impossible to perform*. Not discouraged — unavailable.

CROA is built on the second idea.

**An analogy from aviation.** Airplanes don't rely on pilots remembering "don't retract the landing gear while on the ground." There's a *weight-on-wheels* switch: while the plane's weight is on its wheels, the gear physically cannot retract. The mistake isn't discouraged — it's unreachable. Aviation got safe not by trusting pilots to be perfect, but by removing the dangerous paths from the system.

Most AI safety today is a checklist. CROA is the weight-on-wheels switch.

## Why "just train the AI better" isn't enough

Better models and better prompts help, but they all work at the level of the AI's *behavior* — they make it *want* to comply. The problem is that a discouraged action is still a *possible* action, and three things follow:

- **It breaks down under pressure.** The harder the agent is pushed toward a goal, the more likely it is to bend a soft rule to reach it. (There's a name for this in the framework: *Technical Sycophancy* — an agent reinterpreting its constraints so it can still satisfy the objective. Our €900 refund is exactly this.)
- **It doesn't scale.** One careful agent is manageable. Fifty agents acting across dozens of systems, each individually reasonable, add up to something no one is governing.
- **You can't prove what happened.** When an action goes wrong, "the model decided to" is not an answer an auditor, a regulator, or a board will accept.

## What CROA actually does

CROA puts a **checkpoint between the agent and the systems it can affect.** The agent doesn't act on your systems directly; it asks the checkpoint, and the checkpoint enforces the rules:

1. **It checks every proposed action against the rules you registered** — deterministically, the same way every time (no AI in the checkpoint itself).
2. **If an action isn't allowed, it never reaches your systems.** Not "the agent is warned" — there is simply no path for the action to arrive. (A legitimate exception is still possible, but only through an explicit, signed authorization — never by the agent deciding on its own.)
3. **Every decision — permit *and* deny — is written to a tamper-evident log,** so you can reconstruct exactly what was allowed, what was blocked, and why.

In our example: the €900 refund is stopped *before any money moves*, the block is recorded as the system working correctly, and the only way past it is a real, signed manager approval.

## What CROA claims — and what it doesn't

CROA states its promise carefully, on purpose:

> For the actions you've chosen to govern, under the rules you've registered, and with the checkpoint properly enforced, **rule-breaking actions cannot be carried out** — they are structurally unreachable.

Read the three conditions as the *boundary of the promise*, not fine print:

- **"the actions you've chosen to govern"** — CROA governs what you've set it up to govern. It makes no claim about things outside that scope.
- **"the rules you've registered"** — it enforces the rules you've actually written down. It doesn't invent them.
- **"the checkpoint properly enforced"** — the guarantee depends on your systems only accepting actions that came through the checkpoint.

Inside those limits, the guarantee is structural. Outside them, CROA honestly says nothing. That honesty is what makes the claim **testable** — it tells you exactly what would count as CROA failing.

## Adopting CROA is low-regret

A fair objection at this stage: *it's a Public Review Draft with two maintainers and no independent
implementations yet — why would I bet on it?*

The honest answer is that you don't have to bet much, because **CROA is an architecture, not a product.**
Adopting it means building three things: a network-enforced execution boundary, a registry of your
legitimate endpoints, and a tamper-evident audit trail of what your agents did. If the CROA project
stalled tomorrow and you walked away, **you would still own those three assets — and each has standalone
value regardless of CROA.** A network boundary that only lets authorized operations through, an accurate
inventory of what your agents may touch, and an immutable record for your auditors are things a mature
enterprise wants *anyway*. There is no proprietary runtime to be stranded on, no license to be trapped
by, no vendor to outlive.

That is close to the best adoption-risk profile a framework can offer at this maturity: the sunk cost of
trying it is paid in durable infrastructure, not in a dependency. The sensible posture is to treat CROA
as a **design discipline** — a way to structure your most irreversible action classes — rather than a
runtime dependency, and to pilot it on the action you would least want an agent to get wrong (outbound
payments, customer-data export). Even a pilot that concludes "too costly for us, here's why" leaves you
with the assets and a documented position — a first-class contribution to the review, and not a loss.

## Why a framework, published openly for review

The problem of governing what autonomous agents are *allowed to do* is being worked out right now, inside many companies, mostly in private. CROA's bet is that the answer worth trusting is the one that gets **tested in the open** — implemented by different teams, challenged by people who don't share an employer, and refined based on what actually happens.

So CROA is published as an **architecture** (something many organizations can implement in their own way), not a product — and as a **hypothesis under public review**, not a finished standard.

The most useful thing you can do is read the claim, try to implement it or break it, and tell us what you find.

→ Next: the one-page [Architecture Overview](architecture-overview.md), the [Quick Start](quick-start.md), or the open [Research Questions](../public-review/research-questions.md). Evaluating fit for a real environment? See [CROA on your existing stack](mapping-to-your-stack.md), the [deployment topologies](deployment-topologies.md), [operating C5](operating-c5.md), and the [external prerequisites](prerequisites.md).
