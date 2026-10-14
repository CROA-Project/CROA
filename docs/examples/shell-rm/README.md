# Worked example — governed shell delete with Claude Code

> **Non-normative.** This example illustrates one way to apply the CROA logical architecture to a raw shell tool. It adds no requirement. Where it differs from the specification, the specification governs. Invariant identifiers, paths, OS accounts, the executor design and the hook-to-executor mechanism below are illustrative.
>
> **Vendor neutrality.** Claude Code is used here as a concrete example runtime, because its hooks, permission rules and sandbox are publicly documented. The same pattern applies to any agent runtime with a pre-execution hook. Naming it implies no certification or endorsement by any vendor, and its hooks and sandbox provide no CROA guarantee on their own. Conformance never requires any particular product (see [Vendor neutrality](../../../README.md#vendor-neutrality)).

French version: [fr/README.md](fr/README.md).

## Why a shell is different

In the [payment example](../payment-via-mcp/README.md), one tool performs one action, so a tool allowlist still means something. A shell is one tool that can perform **any** action, from `ls` to `rm -rf /*`. Allowing the `Bash` tool says nothing about what it will do. This is the strongest form of the rule *access to a tool is not authority to execute*: the governance has to bear on the action, not on the tool.

Three documented facts about Claude Code shape the design:

1. **Permission rules on Bash are not a security boundary.** The [permissions documentation](https://code.claude.com/docs/en/permissions) says a Bash rule "matches the command text Claude writes" and "isn't a security boundary around the program": a deny rule such as `Bash(rm *)` does not stop `/bin/rm -rf build/` or `bash -c 'rm -rf build/'`.
2. **A failing hook lets the command through by default.** According to the [hooks documentation](https://code.claude.com/docs/en/hooks), a `PreToolUse` hook that crashes or times out does not block the tool call unless `onFailure` is set to `block` (Claude Code v2.1.295 or later); the default is `continue`.
3. **The sandbox leaves the working directory writable by default.** The [sandboxing documentation](https://code.claude.com/docs/en/sandboxing) says sandboxed commands can write the working directory, the per-user temp directory and added directories. So the sandbox protects `/bin` and `/etc`, but `rm -rf /*` run inside it would still erase the project.

## Design

- **The boundary is file ownership.** The workspace `/ws` belongs to a dedicated OS user, `croa-exec`. Claude Code runs as another OS user, `claude-agent`, which can read `/ws` but not write it. Everything Claude Code starts runs as `claude-agent`: the sandboxed shell, the `Edit` and `Write` tools, MCP servers, hooks and `!` commands. None of them can change `/ws`, whatever their Claude Code configuration, provided the OS preconditions hold: `claude-agent` has no sudo or setuid escalation, is in neither the `croa-exec` group nor the docker group, `/ws` is not group- or world-writable, and no service other than `C6` running as `croa-exec` or root can be driven by it.
- **`C6` is a local executor** running as `croa-exec`, the only account that can write `/ws`. It executes only operations derived from a valid, unredeemed ECC signed by `C7` [S3], after checking signer epoch and revocation, ECC revocation and the invariant registry version (§4.8, §4.3.3). This is the local equivalent of P4 in the payment example.
- **The Agent Surface parses the command.** The gateway is the adapter that builds the `gar.*` from the tool call, as the MCP server does in the payment example; the raw command text is never forwarded as request content. A deterministic parser accepts simple commands with literal arguments, and passes glob patterns such as `/*` unexpanded in `gar.context_refs` for `C3` to resolve against the registry. It turns the command into a `gar.*` whose type is the action class (`fs.delete`), so RBAC applies to the action and `gar.type` stays the same all the way to the ECC (§4.5.1, §4.9.1). A command the grammar cannot reduce, such as a command substitution, `eval` or a decoded payload, becomes `shell.exec_dynamic`: a type declared in the `C1` artifact (§4.5.1) that no role includes. A direct call to `croa-exec` by the agent is not an action class either and is rejected at admission; a leaked ECC reference stays single-use and bound to its subject.
- **The hook is CROA's client, not the guarantee.** The managed `PreToolUse` hook forwards the raw command to the gateway. On `PERMIT` it returns `allow` with `updatedInput`, which replaces the command with `croa-exec --ecc <ref>`; on a refusal it returns `deny` with the reason, which Claude sees.
- **Managed Claude Code settings are defense in depth** ([managed settings](https://code.claude.com/docs/en/managed-settings)): sandbox on with `failIfUnavailable: true` and `allowUnsandboxedCommands: false`; `sandbox.filesystem.denyWrite` on `/ws`; managed deny rules for `Edit` and `Write` on `/ws`; `allowManagedHooksOnly`, with the hook matching `Bash`, `PowerShell` and `Monitor` and set to `onFailure: "block"`.
- **The channel to `C6`.** `croa-exec` reaches `C6` over a Unix socket owned by `croa-exec`. On macOS the managed setting `sandbox.network.allowUnixSockets` lists that one socket. On Linux, where that setting does not apply, a managed `sandbox.excludedCommands` entry runs the root-owned `croa-exec` binary outside the sandbox. Either option widens the sandbox for one path only, and neither grants write access to `/ws`, because the caller is still `claude-agent`. On Linux, the sandboxing documentation notes that Unix-socket blocking depends on an optional seccomp filter.

## Subject binding

The gateway and `C6` listen on Unix sockets and read the caller's OS user from the kernel (peer credentials). The subject is therefore the OS user `claude-agent`, not a value the caller supplies. It identifies the agent deployment, not a person: anything running as `claude-agent`, including the developer's `!` commands inside Claude Code, shares it. The gateway issues its own session identifier at first contact (§4.6.1); the Claude Code `session_id` is kept only for correlation, so opening a new Claude Code session does not reset anything. A cumulative limit, if one were added, would be keyed per subject (TP-X, §4.6.3), as in the payment example. `C6` executes an ECC only if the presenting process runs as `ecc.subject`. Any process running as `claude-agent` can still ask for an action, but only through CROA, and only within what the role and the invariants allow.

## Registered invariants and role (illustrative)

| Rule | Class | Statement |
|---|---|---|
| Role of `claude-agent` | — | Includes `fs.delete`. `shell.exec_dynamic` is a declared action type, included in no role. |
| `I-FS-001` | E2 | `fs.delete` targets MUST resolve into the set of registered paths under `/ws`. |
| `I-FS-002` | E1 | `fs.delete` MUST NOT be recursive on `/ws` itself or on a protected path (`.git`, `.claude`). |

`C3`'s registry is scoped to `/ws`. A target outside it is unresolvable, so the request ends in `CONTEXT_FAILURE` before `C2`; `I-FS-001` and `I-FS-002` are a second line of defense.

**Reversibility.** A delete inside `/ws` is preceded by a snapshot taken by `C6`, so it is compensatable (**R1**); the snapshot is the ECC's `compensating_controls`. A delete outside `/ws` would be R4 under Tenet T5 (default denial). This example goes further and keeps it out of the action surface altogether, by scoping the registry.

## Cases

| Case | Outcome |
|---|---|
| [00 — Prerequisites](00-prerequisites.md) | What must be in place before any command |
| [Case 01 — rm of a workspace file](01-rm-workspace-file.md) | `rm build/tmp.log` · `PERMIT` (R1) · executed by C6 |
| [Case 02 — rm -rf /*](02-rm-rf-root.md) | `rm -rf /*` · `CONTEXT_FAILURE` · refused, nothing deleted |
| [Case 03 — obfuscated delete](03-obfuscated-delete.md) | `bash -c "$(… \| base64 -d)"` · `ADMISSION_REJECTED` |
| [Case 04 — attempts to bypass CROA](04-raw-shell-bypass.md) | Hook replaced, failing, or skipped · nothing deleted |

## Reading the diagrams

Each file shows two views of the same case. The **overview** (flowchart) reads top to bottom: each check is a diamond, each refusal exits to a red box. The **sequence** diagram below it gives every exchange in order, including each `C5` write.

In the sequence diagrams:

- Solid arrows (`->>`) are synchronous. A `C5` write that must commit before the next step proceeds is shown with its acknowledgement.
- Dashed arrows ending in a cross (`--x`) are refusals or blocks.
- Grey zones are common steps or counterfactuals; green means permitted or admitted; red means refused or blocked; blue is the presentation at the execution boundary.
- Each case opens with a one-line reminder of the prerequisites, detailed in [00 — Prerequisites](00-prerequisites.md). Numbering in a case starts at the agent's call.

## Signatures involved

Only two of the three signatures from the payment example appear here, because no human approves an exception:

- **[S1]** `C1`'s key on the policy artifacts (role, `I-FS-001`, `I-FS-002`), verified by `C2` and `C3`.
- **[S3]** `C7`'s key on the ECC, verified by `C6` before it touches `/ws`.

`permissionDecision` and `updatedInput` are hook outputs, not authorization signatures: the authority to delete is the ECC, verified and redeemed by `C6`.

## Limits

- **Every write goes through `C6`.** Because `claude-agent` cannot write `/ws`, editing code also needs a governed path (`fs.write` through `C6`), not only deleting. A real deployment would either govern all writes this way or scope the governed area to a subdirectory.
- **Developer settings can widen the sandbox.** Several sandbox settings, such as `excludedCommands` and `filesystem.allowWrite`, have no managed-only lock, and array settings merge. That does not break this design, because file ownership, not the sandbox, is the boundary. It is why the sandbox is presented only as defense in depth.
- **Outside the sandbox.** Claude Code's file tools, MCP servers, hooks, `!` commands, and processes started by mods, LSP servers or plugin monitors run outside the sandbox. They still run as `claude-agent` here, so they cannot write `/ws` either.
- **Reads are not governed.** The agent reads `/ws` directly; only changes go through CROA.
- **OS and sandbox events.** Neither the OS nor the sandbox is a CROA component. Forwarding their denials to `C5` is this example's choice, not a guarantee of the runtime.
- **Parser trust.** The Agent Surface's shell parser is part of the trusted base: a parser that misreads a command could ground the wrong target. Keeping the accepted grammar small (simple commands, literal arguments) is what makes it deterministic.
- **`updatedInput`.** The hooks documentation says `updatedInput` "replaces a tool's arguments before it runs". This example relies only on that. Deny and ask rules still apply to the call regardless of the hook's decision.

## Spec references

- Evaluability classes and narrowing the action surface: Part I §2.6; Part III §9.3
- Sessions and trajectory profiles: Part II §4.6.1, §4.6.3
- Reversibility classes: Part I Chapter 3, Tenet T5
- Signer epochs and revocation: Part II §4.3.3
- `C2.eval`: Part II §4.4.2; ECC fields (`reversibility_class`, `compensating_controls`): Part II §4.4.1 and `spec/schemas/ecc.schema.json`
- `gga.type` unchanged from `gar.type`, `CONTEXT_FAILURE` routed to `C6`: Part II §4.5.1, §4.10; registry scope: Part II §4.5.2
- C5 events (`ADMISSION_REJECTED`, `CONTEXT_FAILURE`, `EXECUTION_*`): Part II §4.7.1 and `spec/schemas/event.schema.json`
- `C6` as sole writer, atomic redemption, Refusal Gateway: Part II §4.8
- Agent Surface, RBAC on `gar.type`: Part II §4.9, §4.9.1
- Policy as code and separation of duties: Part III §7.2, §7.3
- Sidechannel execution (TH-9): Part V Chapter 26
