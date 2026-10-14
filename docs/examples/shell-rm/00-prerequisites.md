# 00 — Prerequisites

> **Non-normative.** Part of the [governed shell delete with Claude Code](README.md) worked example. The shared context (design, invariants, subject binding, limits, vendor-neutrality note and references) is in the [README](README.md).

Version française: [00-prerequisites](fr/00-prerequisites.md).

**Scope:** What must be in place before any command

Not a case: the state every case relies on. The boundary is the operating system's file ownership: the workspace `/ws` belongs to the OS user `croa-exec`, and Claude Code runs as `claude-agent`, which can read `/ws` but not write it. Everything Claude Code starts runs as `claude-agent`: its sandboxed shell, its file tools, MCP servers and `!` commands. This holds only under OS preconditions: `claude-agent` has no sudo or setuid escalation, is in neither the `croa-exec` group nor the docker group, and no service other than `C6` running as `croa-exec` or root can be driven by it. Managed Claude Code settings add defense in depth: the sandbox is on and the agent cannot retry outside it, `/ws` is also `denyWrite`, and only the organization's `PreToolUse` hook runs, blocking if it fails. The rules go through a pull request and a second approver before `C1` signs them [S1]. `C6` is the executor that runs as `croa-exec`: it verifies `C7`'s signature [S3], the revocation status and the invariant registry version before writing anything.

## Overview

```mermaid
flowchart TD
    subgraph O["1 · OS accounts: the actual boundary"]
        direction TB
        O1["/ws owned by croa-exec<br/>the only account that can write it"]
        O2["Claude Code runs as claude-agent:<br/>Bash, sandbox, Edit, Write, MCP, ! commands<br/>read /ws, never write it"]
        O3["Gateway and C6 on Unix sockets<br/>caller's OS user read from the kernel"]
        O4["OS preconditions: no sudo or setuid for claude-agent,<br/>not in croa-exec or docker groups, no other<br/>croa-exec or root service it can drive"]
    end
    subgraph M["2 · Managed settings (defense in depth)"]
        direction TB
        M1["Sandbox on · failIfUnavailable<br/>allowUnsandboxedCommands false"]
        M2["denyWrite /ws · Edit and Write denied on /ws"]
        M3["allowManagedHooksOnly · PreToolUse hook on<br/>Bash, PowerShell, Monitor · onFailure block"]
        M4["Channel to C6: allowUnixSockets (macOS)<br/>managed excludedCommands for croa-exec (Linux)"]
    end
    subgraph R["3 · Rules (Part III §7.2, §7.3)"]
        direction TB
        R1["PR · CI · second approver · merge"] --> R2["C1 signs [S1]: I-FS-001, I-FS-002<br/>role of claude-agent: fs.delete<br/>shell.exec_dynamic declared, in no role"]
        R2 --> R3["C2 and C3 verify [S1]<br/>C3 registry scoped to /ws"]
        R4["C4 gives C6 the invariant<br/>registry version (§4.10)"]
    end
    subgraph E["4 · Executor"]
        direction TB
        E1["C6 knows C7's key [S3]<br/>signer epochs and revocation"]
        E2["Linearizable redemption registry<br/>snapshot store (R1)"]
    end
    O ~~~ M ~~~ R ~~~ E
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class O1,O2,O3,O4,M1,M2,M3,M4,R1,R2,R3,R4,E1,E2 check;
```

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Claude Code agent<br/>(OS user claude-agent)
    participant CC as Bash tool<br/>(OS sandbox)
    participant HK as PreToolUse hook<br/>(managed · onFailure block)
    participant SRV as CROA gateway<br/>(Agent Surface + shell parser)
    participant C3 as C3 Path Resolver
    participant C2 as C2 Execution Governor
    participant C4 as C4 Invariant Monitor
    participant C1 as C1 Policy Authority
    participant C7 as C7 Contract Compiler
    participant C6 as C6 executor<br/>(OS user croa-exec · only writer)
    participant FS as Workspace /ws<br/>(owned by croa-exec · read-only for claude-agent)
    participant C5 as C5 Audit (append-only)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: 1 · OS accounts: the actual boundary
        C6->>FS: /ws is owned by the OS user croa-exec: the only account that can write it
        Note over AG,FS: Claude Code, its sandbox, file tools, MCP servers and ! commands all run as claude-agent, which can read /ws but not write it
        Note over SRV,C6: The gateway and C6 listen on Unix sockets and read each caller's OS user from the kernel (peer credentials)
        Note over AG,FS: OS preconditions: no sudo or setuid escalation for claude-agent · not in the croa-exec or docker group · /ws not group- or world-writable · no other croa-exec or root service it can drive
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: 2 · Managed Claude Code settings (defense in depth)
        Note over CC,HK: sandbox.enabled true · failIfUnavailable true · allowUnsandboxedCommands false
        Note over CC,FS: sandbox.filesystem.denyWrite /ws · managed deny rules for Edit and Write on /ws
        Note over HK,SRV: allowManagedHooksOnly · PreToolUse hook on Bash, PowerShell and Monitor · onFailure block (Claude Code v2.1.295+)
        Note over CC,C6: Channel to C6: allowUnixSockets on macOS · on Linux a managed excludedCommands entry for the root-owned croa-exec binary
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: 3 · Rules (Part III §7.2, §7.3)
        Note over C1,C2: Pull request · CI · approval by a second person · merge
        C1->>C1: signs the policy artifact [S1]: I-FS-001, I-FS-002 · role of claude-agent: fs.delete · declared types include shell.exec_dynamic
        C1->>C5: POLICY_ARTIFACT_ISSUED
        C1->>C2: distributes the signed artifact
        C1->>C3: distributes the signed artifact
        C2->>C2: verifies [S1] · keeps the last verified set
        C3->>C3: verifies [S1] · registry scoped to /ws · protected paths .git and .claude
        C4->>C6: current invariant registry version (§4.10)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: 4 · Executor
        C6->>C6: knows C7's public key [S3], the signer epochs and revocation status (§4.3.3)
        C6->>C6: linearizable redemption registry · snapshot store
        Note over C7,C6: C6 executes only operations derived from a valid, unredeemed ECC
    end
```

[Index](README.md) · [Case 01 — rm of a workspace file →](01-rm-workspace-file.md)
