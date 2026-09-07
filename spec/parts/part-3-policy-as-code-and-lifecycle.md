# CROA Framework — Part III: Policy-as-Code & Lifecycle

**Version:** 1.0.1

## Chapter 7. GitOps and CI/CD Governance Integration

**Chapter abstract.** This chapter defines the mandatory Policy-as-Code (PaC) lifecycle for the CROA architecture. The legacy nine-phase architecture cycle has been entirely removed to eliminate bureaucratic bottlenecks. CROA governance is now managed strictly through declarative code, utilizing standard Continuous Integration and Continuous Deployment (CI/CD) pipelines. This ensures that governance mechanisms operate with the same velocity, automation, and determinism as the generative AI systems they regulate.

### 7.1 Policy-as-Code Principles

A conformant CROA implementation MUST manage all governance artifacts through a declarative Policy-as-Code (PaC) paradigm.

The Policy Authority (C1) operates as an automated engine integrated within the enterprise version control system (e.g., Git). Manual architecture review boards and phase-gated methodologies are strictly outside the scope of the CROA execution path. The Automated CAB relies on machine-readable policies to produce the Execution Change Contract (ECC).

### 7.2 The GitOps Workflow

The lifecycle of a governance rule MUST adhere to the following GitOps workflow:

1. **Definition:** Policies MUST be defined in standard declarative formats (e.g., JSON/YAML schemas, OPA/Rego, or AWS Cedar).
2. **Proposal:** Modifications, additions, or revocations of policies MUST be submitted as version-controlled change requests (e.g., Pull Requests).
3. **Validation:** CI/CD pipelines MUST automatically validate the proposed policy against the authoritative schema definitions prior to approval. This includes static analysis and conflict detection against the existing invariant registry.
4. **Deployment:** Upon merge to the primary branch, the C1 component MUST dynamically and securely distribute the updated policies to the Execution Governor (C2) and the Federated Path Resolver (C3).
5. **Rollback:** In the event of a critical governance failure, the version control system MUST support automated reversion to the previous stable policy state.

### 7.3 Separation of Duties in the Pipeline

Automating the governance lifecycle removes the review board; it does not remove the separation of duties the review board existed to provide. The pipeline MUST preserve the following separations, enforced by repository and signing controls rather than by convention.

1. **The pipeline does not issue policy.** A merge does not make a policy artifact authoritative: `C1` does. The Deployment step (§7.2, Step 4) MUST distribute only artifacts signed by `C1`, and no CI credential MAY hold a `C1` signing key (I4).
2. **Proposal and approval MUST be distinct principals** for any change request that registers, amends, or deprecates a `BLOCKING` invariant, that alters the governance boundary (§9.2), or that changes a pinned `E3` analyzer version (§11.5). A self-approved change of this class is non-conformant regardless of the reviewer's seniority.
3. **Operations MUST NOT be able to alter `C5`.** The role that runs the pipeline and the role that could modify the evidence of what the pipeline did MUST be separate, and the append-only property MUST be enforced at the storage layer (Part II §4.7), not by withholding a credential.
4. **The validation gate MUST NOT be bypassable by the proposing principal.** Where an emergency path exists, it MUST shorten review time, never remove the Validation step (§7.2, Step 3) or the negative tests of §10.3.

### 7.4 Governance Roles

The following roles are normative. A deployment MAY assign several to one person where the incompatibilities below are respected, and MAY name them differently provided the mapping is recorded.

| Role | Responsibility | Constraint |
| --- | --- | --- |
| **Governance Architect** | Leads the Policy-as-Code lifecycle for the deployment: owns the invariant registry (§9.1), the governance boundary (§9.2), and the action-surface sizing decision (§9.3). | Distinct from `C1`. The Governance Architect specifies policy; `C1` issues it. The role carries no capability to sign a policy artifact. |
| **Policy Authority Representative** | The accountable human authority for `C1` operation: custody of the signing key infrastructure, issuance, amendment, and revocation of policy artifacts (Part II §4.3). | MUST NOT hold the merge authority for the repository whose changes it signs (§7.3, clause 2). |
| **Compliance Lead** | Review authority over `CONSTRAINED`-mode designations and over the accepted-residuals record (§10.4); confirms that a proposed relaxation is an accepted risk rather than an unrecorded one. | MUST NOT be the proposing principal for a change it reviews. |
| **Operations** | Runs the pipeline and the deployment: executes the workflow of §7.2, operates the OCP components, and monitors governance friction (§10.4). | MUST NOT issue policy or authorization artifacts, and MUST NOT hold any capability to modify, delete, or truncate `C5` records (§7.3, clause 3). |

Two further roles are defined elsewhere and are referenced here for completeness: the **Semantic Custodian**, owner of the Federated Context Registry against which `C3` grounds (Part I §2.1, Part II §4.5.2), and the **Evidence Officer**, custodian of the Audit and Provenance Store (Part II §4.7). Independent assessment is not a deployment role: it is specified in Part VI Chapter 29 and bound by the neutrality requirements of Part VII §32.2.

**Role assignments are governed content.** The mapping of named individuals or groups to these roles MUST be recorded as versioned policy content and MUST be revised through a governed change event (§11.1). An undocumented role assignment cannot be audited, and a separation of duties that is not recorded is not a separation.

## Chapter 8. Schema Definitions for Policies

**Chapter abstract.** This chapter outlines the canonical schemas required for policy definition and the Execution Change Contract (ECC). These schemas replace the narrative documentation of legacy governance.

### 8.1 Governance Policy Schema

To guarantee deterministic evaluation by C2, governance rules MUST conform to a standardized, machine-readable schema. The schema enforces strict typing and prevents execution ambiguity.

```yaml
# Canonical CROA Policy Schema (Informative Example)
apiVersion: croa.dev/v1.0.1
kind: GovernancePolicy
metadata:
  name: core-data-protection
  domain: enterprise-global
spec:
  rules:
    - action: data.export
      condition: "target.env != 'production'"
      enforcement: BLOCKING
      evaluability: E1
    - action: config.change
      condition: "request.user.role == 'system_agent'"
      enforcement: CONSTRAINED
      evaluability: E2
```

### 8.2 Execution Change Contract (ECC) Schema

The ECC serves as the authoritative, machine-speed ITIL Change Record. The Contract Compiler (C7) MUST generate an ECC that strictly adheres to the following structural requirements. It completely replaces the legacy "Request for Change".

* **ECC Identifier:** A cryptographic hash (SHA-256 or stronger) of the contract payload.
* **Subject:** The authenticated identity of the autonomous agent initiating the change.
* **Action Scope:** The exact permitted action and target system boundaries.
* **Temporal Bounds:** Strict issuance and expiration timestamps.
* **Signatures:** M-of-N signatures where applicable, prioritizing standard mTLS for routine operations and reserving HSM-backed signatures for policy root mutations.

## Chapter 9. Invariant Registration and Evaluability Profiles

**Chapter abstract.** Chapters 7 and 8 specify *how* a governance rule travels from a proposal to a distributed policy artifact. This chapter specifies *what* must be true of the rule before it is admissible to that pipeline. An enterprise governance invariant is not a sentence in a policy document: it is a registry entry carrying a declared evaluability class, a declared trajectory profile, a declared reversibility class, and — for any invariant evaluated by an approximated method — a pinned analyzer identity. These declarations are what make `C2.eval` deterministic (I2) and what make a decision reconstructable years later (I3). This chapter also specifies the governance boundary that scopes the registry, the sizing method that keeps approximated invariants tractable, and the authorization-propagation contract that binds a permitted scope to the ECC that carries it.

### 9.1 The Invariant Registry Entry

The invariant registry is a version-controlled artifact under the GitOps workflow of §7.2. A registry entry is a policy change like any other: it is proposed as a change request, validated by the pipeline, and distributed by `C1` on merge.

Every registered enterprise governance invariant MUST carry the following declared properties. An entry missing any of them is malformed, and the Validation step (§7.2, Step 3) MUST fail the change request.

| Property | Requirement |
| --- | --- |
| Identifier | A stable enterprise-scoped identifier, retained for the life of the invariant. A superseded invariant retains its identifier and is marked deprecated with a pointer to its successor. |
| Statement | The governance property expressed over the typed action space — over `gar.*` / `gga.*` / `ecc.*` fields and resolved entities, not over the agent's stated intent, reasoning, or self-report. |
| Evaluability class | Exactly one of `E1` (syntactic / attribute), `E2` (static / decidable), or `E3` (semantic / approximated), per Part I §2.6. |
| Enforcement mode | `BLOCKING` or `CONSTRAINED`, per the policy schema of §8.1. |
| Reversibility class | The `R0`–`R4` class of the governed transition the invariant guards (Part I, Tenet T5). An unassigned transition MUST be registered as at least `R2`. |
| Trajectory relevance | `YES` or `NO`. Where `YES`, the entry MUST declare a trajectory rule profile — `TP-0`, `TP-W`, `TP-C`, or `TP-X` (Part II §4.6.3) — and, for a windowed or cumulative profile, the window or threshold. |
| Evaluation method | The procedure by which `C2` or `C4` decides the invariant, at the precision required to reproduce the decision. |

An invariant registered as `E3` MUST additionally declare:

1. **A pinned analyzer identity.** The analyzer and its evaluation configuration MUST be identified by a version that is immutable for the life of the policy artifact version that references it. This identity is recorded on every decision as `event.analyzer_version` and is part of the I2 determinism key.
2. **A declared budget.** The bound — time, depth, or resource — beyond which the analyzer MUST return `AMBIGUOUS` rather than continue. An analyzer without a declared budget cannot return a reproducible verdict.
3. **A governance-friction target.** The intended `AMBIGUOUS`→`DENY` rate for the invariant, against which operation is measured (§10.4, Part I §2.7.1).

**Fail-deny is a registration property, not an implementation choice.** An `E2` or `E3` evaluation that cannot return `SATISFIED` or `VIOLATED` MUST return `AMBIGUOUS`, and `C2.eval` MUST treat `AMBIGUOUS` as deny (Part I §2.6; Part II §4.4.2). A registry entry MUST NOT declare an alternative disposition for `AMBIGUOUS`, and the Validation step MUST reject a change request that attempts one.

### 9.2 Governance Boundary Specification

The governance boundary is the declared set of systems, agents, and action classes over which the registered invariants are enforced. It is a version-controlled artifact, revised through §7.2 like any other policy content.

An enterprise MUST specify its governance boundary through the following steps:

1. **Enumerate the governed agents and subjects** — every autonomous component that can propose or execute an action with persistent effect, and every human subject that submits governed actions.
2. **Enumerate the governed external systems** — every system whose state a governed action can change.
3. **Enumerate the action classes** — the set of `gar.type` values admissible at the Agent Surface. The set MUST be defined in a `C1` policy artifact (Part II §4.5.1); an action type absent from that set is rejected at admission.
4. **Record the documented architectural exclusions.** Any channel by which a governed agent can reach a governed external system without traversing the OCP MUST be either eliminated, brought under governance by an additional deployment model (Part IV), or recorded as an explicit, justified exclusion from the governance scope. An undocumented exclusion is a breach of I1, not a scoping decision: the conformance claim of a deployment is bounded by what this step records.
5. **Bind the boundary to the invariant registry version** in force, so that a decision can be reconstructed against the scope that applied at the time it was taken.

The governance boundary specification MUST be reviewed on every change to the deployment model (§11.2) and on every addition of a governed external system.

### 9.3 Action-Surface Sizing and the Utility–Guarantee Frontier

The strength of the T1 guarantee is conditioned on the modeled action space. A wide action surface buys agent capability and pushes invariants toward `E3`; a narrow one buys an exact guarantee over a smaller agent. Neither is more conformant than the other. What the framework requires is that the point be chosen deliberately and recorded, rather than arriving by default.

For each governed action class, a deployment SHOULD:

1. **Enumerate the hazards** the action class can realize against the registered invariants.
2. **Classify each hazard** by the evaluability class required to decide it (§9.1) and by the reversibility class of the transition it would produce.
3. **Locate the exact frontier** — the subset of hazards decidable at `E1` or `E2` over the current action surface.
4. **Declare the residual** — the hazards that remain in the `E3` region, with the governance-friction target accepted for each.
5. **Narrow the action surface where the residual is unacceptable.** Replacing an unbounded action type with a typed, bounded one moves hazards from `E3` to `E1`/`E2` and is the primary lever available to a deployment. A narrowed surface is expressed as a typed action schema in the `C1` policy artifact, not as a convention.
6. **Record the chosen point** — the selected action surface, the hazards deliberately left at `E3`, and the residuals accepted — as part of the invariant's evaluation-method record, so the trade-off is auditable rather than implicit.

**Federated Context Registry compliance is a mandatory registered invariant.** Every deployment MUST register an invariant requiring that a governed action reference only entities resolvable in the Federated Context Registry (Part II §4.5.2). This invariant's source is the framework rather than an enterprise candidate: without it, `C3` grounding is advisory, and the modeled action space over which T1 is claimed is not bounded by anything the enterprise controls.

### 9.4 Authorization Propagation

A permitted scope is only as strong as its propagation to the boundary that enforces it. The following contract is normative for every deployment.

1. The scope a permit decision authorizes MUST be carried in `ecc.authorization_scope`, compiled into the ECC by `C7` (Part II §4.4.1).
2. `C6` MUST enforce that every operation in the presented execution request lies within `ecc.authorization_scope` before authorizing passage across TB-3 (Part II §4.8).
3. For a `PERMIT_WITH_AUTHORIZATION` decision, `C7` MUST additionally bind the authorization's `auth_id` and its bounded exception scope into the ECC unchanged, and `C6` MUST redeem that `auth_id` in the same atomic operation that redeems `ecc.id` (Part II §4.3.1, §4.8).
4. No component downstream of `C7` MAY widen a scope. A scope that must change requires a fresh permit decision and a new ECC.

A deployment MUST record, as part of its policy architecture, how each governed external system's operations map onto `ecc.authorization_scope` entries. Where that mapping is not expressible, the operations concerned belong in the documented exclusions of §9.2, Step 4.

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 9**

* §9.1: Every registered invariant MUST declare an identifier, a statement over the typed action space, an evaluability class, an enforcement mode, a reversibility class, and its trajectory relevance with a `TP-*` profile where relevant; the Validation step MUST fail a malformed entry.
* §9.1: An `E3` invariant MUST additionally declare a pinned analyzer identity, a budget beyond which the analyzer returns `AMBIGUOUS`, and a governance-friction target.
* §9.1: A registry entry MUST NOT declare any disposition for `AMBIGUOUS` other than deny.
* §9.2: The governance boundary MUST be specified through the five steps of §9.2; any channel reaching a governed system outside the OCP MUST be eliminated, governed, or recorded as a documented architectural exclusion (Step 4).
* §9.3: A deployment SHOULD locate and record its point on the utility–guarantee frontier; narrowing the action surface (Step 5) is the primary lever for moving hazards out of the `E3` region.
* §9.3: Every deployment MUST register a Federated Context Registry compliance invariant.
* §9.4: The permitted scope MUST be carried in `ecc.authorization_scope` and enforced by `C6` at TB-3; no component downstream of `C7` MAY widen a scope.

## Chapter 10. Threat Assessment and Negative Testing in the Pipeline

**Chapter abstract.** A governance architecture is credible only where its failure to govern is testable. This chapter specifies the threat assessment as a version-controlled pipeline artifact rather than a review-board exercise, and makes the reference negative tests of Appendix Q a merge gate rather than a periodic audit. The distinction from a conventional security control set is the direction of proof: these tests are written to demonstrate that a bypass is *unavailable*, and a test that passes because the attack was not attempted is not evidence.

### 10.1 The Threat Assessment Artifact

Every deployment MUST maintain a threat assessment covering all eleven threat classes of Part V: TH-1 Technical Sycophancy, TH-2 Policy Drift, TH-3 Orchestration Bypass, TH-4 Audit Tampering, TH-5 Refusal Coercion, TH-6 Identity Confusion, TH-7 Path Composition Attacks, TH-8 Latent State Carryover, TH-9 Sidechannel Execution, TH-10 Governance Surface Confusion, and TH-11 Governance Availability Exhaustion.

The assessment is a repository-resident, version-controlled artifact. It MUST record, per threat class: the relevance determination and its rationale (§10.2), the inherent severity, the structural mitigations that address it, the residual condition after mitigation, and the negative test that exercises it (§10.3). It is revised through the GitOps workflow of §7.2 like any other governance artifact, and a change to the deployment model, the governance boundary, or the registered invariant set MUST trigger its review.

### 10.2 Relevance Determination

A threat class is assessed as relevant where the deployment's governance boundary (§9.2), deployment model (§11.2), or registered invariant set admits the attack pattern the class describes. A class assessed as not relevant MUST carry a recorded rationale referring to a structural property of the deployment — not to an operational practice, an intention, or the absence of an observed incident.

**TH-1 is assessed regardless of severity rating.** Technical Sycophancy is the category-defining threat: it is the class of attack in which the agent's stated reasoning, urgency, or claimed authority is used to obtain an action that the invariants would otherwise refuse. A deployment MUST assess TH-1 and MUST carry its negative tests whatever severity it assigns, because a deployment that judges TH-1 irrelevant has typically done so by trusting a channel the architecture is built not to trust.

### 10.3 Reference Negative Tests in Continuous Integration

The reference negative tests of Appendix Q are normative for conformance and MUST execute in the pipeline:

| Test | Property demonstrated |
| --- | --- |
| `NT-001` | Non-ECC execution blocked at TB-3. |
| `NT-002` | Expired ECC blocked. |
| `NT-003` | ECC replay blocked; a redeemed `ecc.id` is refused. |
| `NT-004` | Unregistered context blocked; `C3` grounding failure is fail-closed. |
| `NT-005` | Ambiguous `E3` verdict denied; `AMBIGUOUS` resolves to deny. |
| `NT-006` | Progressive trajectory alert and subsequent deny across a session. |
| `NT-007` | Governed exception is single-use; authorization replay and widening blocked. |
| `NT-008` | Authority non-expansion along a delegation chain (I8). |

The following requirements apply:

1. **The Validation step (§7.2, Step 3) MUST execute the negative tests** applicable to the deployment's conformance level and MUST fail the change request on any failure. A policy change that would make a previously blocked action reachable is a governance regression, and the pipeline is where it is caught.
2. **A negative test MUST assert on the `C5` record, not only on the refusal.** A blocked action that produced no `EXECUTION_BLOCKED` event with the expected `event.block_reason` has not demonstrated the property; it has demonstrated a coincidence. Where the test concerns a governed exception, the assertion MUST include the `event.auth_id` of the redeemed authorization.
3. **Test execution MUST be recorded.** Executed results — not test plans — constitute the evidence a conformance claim at L4 or above rests on (Part VI §29.3).
4. **A negative test MUST NOT be disabled to unblock a merge.** Where a test is superseded, its replacement MUST be merged in the same change request, and the supersession MUST be recorded as a governed change event (§11.1).

For each threat class assessed as relevant, the pipeline MUST additionally include at least the minimum negative test case specified for that class in Part V §27.3.

### 10.4 Mitigation Map and Accepted Residuals

The threat assessment MUST be accompanied by two further version-controlled artifacts:

* **A mitigation map**, relating each relevant threat to the structural mitigation that addresses it — the invariant or component, not the procedure — to the design reference where it is implemented, and to the test case that verifies it.
* **An accepted-residuals record**, listing each residual condition the enterprise has decided to accept, its rationale, and the authority that accepted it. A residual accepted without a named accepting authority is not accepted; it is unrecorded.

The governance-friction rate — the `AMBIGUOUS`→`DENY` proportion, per `E3` invariant and in aggregate — MUST be measured from `C5` extracts and compared against the targets declared under §9.1. A friction rate persistently above target is a signal to revisit the action surface (§9.3, Step 5), not to relax the invariant: relaxation under friction pressure is the TH-2 erosion loop the framework exists to prevent.

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 10**

* §10.1: Every deployment MUST maintain a version-controlled threat assessment covering all eleven threat classes, recording relevance, severity, mitigations, residuals, and the negative test per class.
* §10.2: A class assessed as not relevant MUST carry a rationale grounded in a structural property of the deployment; TH-1 MUST be assessed and tested regardless of assigned severity.
* §10.3: The Validation step MUST execute the applicable reference negative tests `NT-001`–`NT-008` and MUST fail the change request on any failure.
* §10.3: A negative test MUST assert on the `C5` record including the expected `event.block_reason`; executed results, not test plans, are the conformance evidence.
* §10.3: A negative test MUST NOT be disabled to unblock a merge; supersession MUST be merged in the same change request and recorded as a governed change event.
* §10.3: For each relevant threat class, the pipeline MUST include at least the minimum negative test case of Part V §27.3.
* §10.4: The mitigation map and the accepted-residuals record MUST be maintained as version-controlled artifacts; an accepted residual MUST name its accepting authority.
* §10.4: Governance friction MUST be measured from `C5` and compared against the declared targets.

## Chapter 11. Governed Change, Deployment-Model Selection, and Rollback

**Chapter abstract.** Governance content changes. So does the software that enforces it, the model it is deployed under, and the analyzer that decides its approximated invariants. This chapter specifies those changes as governed change events under the GitOps workflow of §7.2, so that a change to the governing architecture is subject to the same provenance, validation, and reversibility discipline as a change to a policy rule. It also specifies the operational parameters a deployment must declare, and the analyzer-versioning rule without which the determinism invariant I2 is unverifiable across time.

### 11.1 The Governed Change Event

A **governed change event** is any change to governance content or to the components that enforce it. The following are governed change events and MUST traverse the workflow of §7.2 in full:

* Issuance, amendment, or revocation of a policy artifact.
* Registration, amendment, or deprecation of an enterprise governance invariant (§9.1).
* A change to the governance boundary or to its documented exclusions (§9.2).
* A change to the action surface of a governed action class (§9.3).
* A change to the Federated Context Registry content or schema that alters resolution outcomes (Part II §4.5.2).
* A change to qualification batteries, passing criteria, validity windows, or recertification triggers (Part II §4.9.2).
* A change to the deployment model or its topology (§11.2), **including a sidecar or gateway software upgrade** that can alter `C2.eval`, `C6` validation, or `C5` emission behaviour.
* A change to a pinned `E3` analyzer version or its evaluation configuration (§11.5).

Each governed change event MUST:

1. Be issued by `C1` as a versioned, signed policy artifact where it changes policy content, so that provenance is carried by the artifact and not by the pipeline that produced it (I4).
2. Produce a `POLICY_ARTIFACT_ISSUED` event in `C5` with the appropriate `event.artifact_action` (Part II §4.7.1).
3. Record the invariant registry version it was issued against, so that a later decision is reconstructable.
4. Generate a corresponding change record in the enterprise's IT service management system where the enterprise operates one, referencing the change request and the resulting policy artifact version. The `C5` record remains the authoritative governance record; the ITSM record is the enterprise-process counterpart, not a substitute.

### 11.2 Deployment-Model Selection and Migration

An enterprise MUST select a deployment model — DM-1 through DM-5, or a documented hybrid (Part IV) — and MUST record the selection with its rationale in the OCP architecture specification, traceable to at least one recorded requirement.

A change of deployment model is a governed change event under §11.1. During migration, all four trust boundaries TB-1 through TB-4 MUST remain enforced continuously; a migration window in which a governed agent can reach a governed external system without traversing `C6` is a breach of I1, whatever its duration. Migration steps MUST be ordered so that no such window exists, and the migration plan MUST state how that ordering is guaranteed.

### 11.3 Declared Operational Parameters

A deployment MUST declare the following parameters as versioned policy content. Each is a governed change event under §11.1 when it changes.

1. **Maximum invariant state age.** The maximum age of the invariant state on which `C2.eval` may be executed. A `C2` instance MUST NOT evaluate using invariant state older than this bound; where the bound is exceeded, the deployment fails deny (Part II §4.6). This parameter is what makes a distributed or sidecar topology's staleness explicit rather than emergent.
2. **Maximum ECC validity window.** The upper bound on `ecc.expires_at` relative to `ecc.compiled_at` (Part II §4.4.1).
3. **Maximum Federated Context Registry snapshot age.** The age beyond which `C3` MUST treat grounding as failed rather than resolve against a stale record (Part II §4.5.2).
4. **`C5` retention period.** The period for which governance events are retained. It MUST satisfy the enterprise's governance retention policy and MUST NOT be shorter than the period during which conformance claims based on those records remain assertable (Part II §4.3).
5. **Qualification validity window and recertification triggers**, where the Agent Qualification Layer is deployed (Part II §4.9.2).

### 11.4 Rollback and Reversion

The version control system MUST support automated reversion of governance content to the previous stable state (§7.2, Step 5). The following constraints apply.

1. **A rollback is itself a governed change event.** It MUST produce its own `POLICY_ARTIFACT_ISSUED` record in `C5`. Reverting a policy artifact does not revert the `C5` record of its issuance: `C5` is append-only, and the history of what was in force is part of the evidence (I3, I7).
2. **A rollback MUST NOT retroactively legitimate an action.** Decisions taken under the reverted artifact were taken under the policy then in force and remain recorded as such.
3. **A rollback MUST NOT widen the reachable action set without traversing Validation.** Where reverting would restore a permit path that current invariants prohibit, the reversion MUST fail the pipeline; the correct remedy is a forward change request.
4. **Emergency reversion follows the same path.** There is no bypass at `C6` and none in the pipeline: an urgent change is an expedited change request, not an ungoverned one.

### 11.5 `E3` Analyzer Version Changes

An `E3` invariant's verdict is a property of its pinned analyzer as much as of the action it judges. Changing that analyzer changes what the invariant means.

1. A change to a pinned analyzer version or to its evaluation configuration is a governed change event under §11.1 and MUST produce a new policy artifact version. An analyzer MUST NOT be upgraded in place under a policy artifact version that pins its predecessor.
2. Every decision in which an `E3` method participated MUST record `event.analyzer_version` (Part II §4.7.1). Without it, two decisions on identical inputs that differ because the analyzer changed are indistinguishable from a determinism failure, and I2 becomes unverifiable across time.
3. An analyzer version change MUST be accompanied by re-execution of the negative tests of §10.3 that depend on it — at minimum `NT-005` — and by a re-measurement of the governance-friction rate for every invariant that pins it.
4. Where a new analyzer version raises the friction rate above the target declared under §9.1, the deployment MUST either narrow the action surface (§9.3, Step 5), revise the target through a governed change event, or revert the analyzer version. It MUST NOT reclassify the invariant to a lower evaluability class to obtain a verdict the method cannot support.

**Summary of Normative Content (recap — skippable on a first linear read) — Chapter 11**

* §11.1: The eight change types listed MUST traverse the §7.2 workflow in full; each governed change event MUST be issued as a signed `C1` artifact where it changes policy content, MUST produce a `POLICY_ARTIFACT_ISSUED` record in `C5`, and MUST record the invariant registry version it was issued against.
* §11.1: A sidecar or gateway software upgrade that can alter `C2.eval`, `C6` validation, or `C5` emission is a governed change event.
* §11.1: Where the enterprise operates an ITSM system, every governed change event MUST generate a corresponding change record; the `C5` record remains authoritative.
* §11.2: An enterprise MUST select and document a deployment model with traceable rationale; a model change is a governed change event, and no migration window may exist in which a governed agent reaches a governed system without traversing `C6`.
* §11.3: A deployment MUST declare the maximum invariant state age (Step 1), the maximum ECC validity window (Step 2), the maximum context-registry snapshot age (Step 3), the `C5` retention period (Step 4), and the qualification validity window where AQL is deployed (Step 5).
* §11.4: A rollback is a governed change event and MUST be recorded in `C5`; it MUST NOT retroactively legitimate an action, MUST NOT bypass Validation, and MUST fail where it would restore a prohibited permit path. Emergency reversion follows the same path.
* §11.5: A pinned `E3` analyzer version or configuration MUST NOT change in place; every `E3`-involving decision MUST record `event.analyzer_version`; an analyzer change MUST trigger re-execution of the dependent negative tests and re-measurement of governance friction.
* §11.5: A deployment MUST NOT reclassify an invariant to a lower evaluability class in order to obtain a verdict its method cannot support.
