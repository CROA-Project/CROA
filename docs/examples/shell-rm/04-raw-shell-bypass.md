# Case 04 — attempts to bypass CROA

> **Non-normative.** Part of the [governed shell delete with Claude Code](README.md) worked example. The shared context (design, invariants, subject binding, limits, vendor-neutrality note and references) is in the [README](README.md).

Version française: [04-raw-shell-bypass](fr/04-raw-shell-bypass.md).

**Outcome:** Hook replaced, failing, or skipped · nothing deleted

What happens when a command tries to skip the governed path. A project cannot replace the managed hook (`allowManagedHooksOnly`). A crashing or slow hook blocks instead of letting the command through, because `onFailure` is `block`; the default, `continue`, would let it run. If a misconfiguration still lets the command reach the shell, it runs as `claude-agent`, which does not own `/ws`: the write fails with `EPERM`. A retry with `dangerouslyDisableSandbox` does not escape: with `allowUnsandboxedCommands: false`, Claude Code ignores the parameter and runs the command in the sandbox again. File ownership is what holds; the sandbox and the managed settings are defense in depth.

## Overview

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>rm -rf src/"]) --> L1{"A · project hook<br/>replaces the managed one?"}
    L1 -- "ignored: allowManagedHooksOnly" --> L2{"B · managed hook<br/>crashes or times out?"}
    L2 -- yes --> X2[["Blocked: onFailure block<br/>(default continue would let it run)"]]
    L2 -. "C · misconfiguration lets<br/>the command reach the shell" .-> L3{"claude-agent writes /ws?"}
    L3 -- "no: owned by croa-exec" --> X3[["EPERM · nothing deleted"]]
    X3 -. "D · retry with<br/>dangerouslyDisableSandbox" .-> D1["Parameter ignored:<br/>allowUnsandboxedCommands false"]
    D1 --> X4[["Runs sandboxed again · EPERM"]]
    X4 ~~~ N(["Only croa-exec can write /ws, and C6 does so only from an ECC.<br/>File ownership is the boundary; the sandbox and settings are defense in depth."])
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class L1,L2,L3,D1 check;
    class X2,X3,X4 ko;
    class N note;
```

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Claude Code agent<br/>(OS user claude-agent)
    participant CC as Bash tool<br/>(OS sandbox)
    participant HK as PreToolUse hook<br/>(managed · onFailure block)
    participant FS as Workspace /ws<br/>(owned by croa-exec · read-only for claude-agent)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prerequisites in place, see 00-prerequisites: /ws owned by croa-exec · Claude Code runs as claude-agent · managed settings · rules signed [S1]

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: A · The project tries to replace the hook
        AG->>CC: Bash tool call: rm -rf src/
        CC->>CC: a project .claude/settings.json declares its own permissive hook · ignored: allowManagedHooksOnly
        CC->>HK: PreToolUse to the managed hook only
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: B · The managed hook fails or times out
        HK--xCC: crash or timeout
        CC--xAG: blocked, because onFailure is block (the default, continue, would let it run)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: C · The command still reaches the shell (for example a misconfiguration)
        AG->>CC: Bash tool call: rm -rf src/
        CC->>FS: unlink /ws/src/... as claude-agent, from inside the sandbox
        FS--xCC: EPERM · /ws belongs to croa-exec (and denyWrite in the sandbox)
        CC--xAG: command failed · nothing deleted
        Note over CC,C5: The sandbox and the OS are not CROA components: forwarding their denials to C5 is this example's choice
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: D · Retry outside the sandbox
        AG->>CC: retry with dangerouslyDisableSandbox
        CC->>CC: parameter ignored, because allowUnsandboxedCommands is false: runs sandboxed again
        CC->>FS: unlink /ws/src/... as claude-agent
        FS--xCC: EPERM
        CC--xAG: command failed · nothing deleted
    end
    
    Note over FS,C5: Only croa-exec can write /ws, and C6 does so only from an ECC. Every path that skips CROA ends without a change to /ws, given the OS preconditions of 00.
```

[← Case 03 — obfuscated delete](03-obfuscated-delete.md) · [Index](README.md)
