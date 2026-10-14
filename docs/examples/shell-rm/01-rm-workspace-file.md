# Case 01 — rm of a workspace file

> **Non-normative.** Part of the [governed shell delete with Claude Code](README.md) worked example. The shared context (design, invariants, subject binding, limits, vendor-neutrality note and references) is in the [README](README.md).

Version française: [01-rm-workspace-file](fr/01-rm-workspace-file.md).

**Outcome:** `rm build/tmp.log` · `PERMIT` (R1) · executed by C6

The baseline. The Agent Surface parses the raw command with a deterministic, literal-only grammar and turns it into a `gar.*` of type `fs.delete`, so RBAC applies to the action, not to the `Bash` tool. `C3` grounds the target in the `/ws` registry and `C2` permits it. A snapshot is taken before the delete, so the transition is compensatable (R1), and the snapshot is the ECC's compensating control. On `PERMIT` the hook does not let the shell run `rm`. It returns `allow` with `updatedInput`, which replaces the command with `croa-exec`. `croa-exec` presents the ECC to `C6`, which checks it, redeems it and deletes the file as `croa-exec`.

## Overview

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>rm build/tmp.log"]) --> H{"PreToolUse hook (managed)<br/>answers in time?"}
    H -- "no: onFailure block" --> X0[["Blocked (see case 04)"]]
    H -- yes --> PA["Agent Surface · deterministic parse<br/>fs.delete · build/tmp.log"]
    PA --> S{"RBAC on gar.type<br/>does a role include it?"}
    S -- no --> X1[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS"]]
    S -- yes --> G{"C3 · target in the /ws registry,<br/>not protected?"}
    G -- no --> X2[["CONTEXT_FAILURE<br/>(see case 02)"]]
    G -- yes --> D{"C2.eval<br/>I-FS-001 · I-FS-002"}
    D -- "one file in /ws, not recursive" --> PM["PERMIT · R1"]
    PM --> E["C7 · ECC signed [S3]<br/>compensation: snapshot"]
    E --> U["Hook: allow + updatedInput<br/>croa-exec --ecc ref"]
    U --> F{"C6 · ECC valid, not revoked,<br/>caller = ecc.subject, not redeemed?"}
    F -- no --> X4[["EXECUTION_BLOCKED"]]
    F -- yes --> C["One CAS · EXECUTION_AUTHORIZED<br/>snapshot, then unlink by C6"]
    C --> OK(["EXECUTION_COMPLETED<br/>file removed, restorable"])
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class H,PA,S,G,D,F check;
    class X0,X1,X2,X4 ko;
    class PM,E,U,C,OK ok;
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
    participant C7 as C7 Contract Compiler
    participant C6 as C6 executor<br/>(OS user croa-exec · only writer)
    participant FS as Workspace /ws<br/>(owned by croa-exec · read-only for claude-agent)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prerequisites in place, see 00-prerequisites: /ws owned by croa-exec · Claude Code runs as claude-agent · managed settings · rules signed [S1]

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        AG->>CC: Bash tool call: rm build/tmp.log
        CC->>HK: PreToolUse (tool_name Bash · tool_input.command · session_id · cwd)
        HK->>SRV: tool call (command, cwd, session_id) over the gateway's Unix socket · the gateway builds gar.* from it
        SRV->>SRV: subject = OS user claude-agent, from the socket peer credentials · CROA session id issued by the gateway, Claude Code session_id kept for correlation
        SRV->>SRV: deterministic parse, literal-only grammar → gar.type fs.delete · target build/tmp.log · recursive false
        SRV->>SRV: RBAC on gar.type: the role of claude-agent includes fs.delete · qualification
        SRV->>C3: gar.* (new request_id · type fs.delete · targets)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Grounding
        C3->>C3: registry: /ws/build/tmp.log exists, inside /ws, not a protected path
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Evaluation
        C3->>C2: gga.* fs.delete · semantic_result GROUNDED
        C2->>C4: action under evaluation
        C4-->>C2: invariant state (deletions by this subject)
        C2->>C2: C2.eval · I-FS-001 target in the /ws set · I-FS-002 not recursive
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: PERMIT · R1 (compensatable by snapshot)
        C2->>C5: PERMIT · decision_basis PERMIT
        C2->>C7: PERMIT
        C7->>C7: compile the ECC and sign it [S3] · fs.delete /ws/build/tmp.log · reversibility_class R1 · compensating_controls: restore from snapshot
    end
    rect rgba(60, 120, 220, 0.10)
        Note over AG,C5: Execution · the hook substitutes the governed client
        C7->>C5: ECC_COMPILED · ecc_id
        C7->>SRV: ECC reference + decision notification
        SRV-->>HK: PERMIT + ECC reference
        HK-->>CC: permissionDecision allow · updatedInput: croa-exec --ecc ref
        CC->>C6: croa-exec presents the ECC reference over C6's Unix socket
        C6->>C6: [S3] valid · signer epoch not revoked · ECC not expired or revoked · invariant_set_version consistent · operation equals the ECC · caller's OS user equals ecc.subject
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Admitted
        C6->>C6: one linearizable CAS · redeem ecc.id
        C6->>C5: EXECUTION_AUTHORIZED · ecc_id
        C5-->>C6: committed
        C6->>FS: snapshot /ws/build/tmp.log (compensation point)
        C6->>FS: unlink /ws/build/tmp.log
        FS-->>C6: done
        C6->>C5: EXECUTION_COMPLETED · ecc_id · exit_status
        Note over C6,C5: If the snapshot fails, C6 does not unlink: EXECUTION_FAILED, and the ECC stays consumed
        C6-->>CC: result + snapshot id
        CC-->>AG: tool result: file removed (restorable)
    end
```

[← 00 — Prerequisites](00-prerequisites.md) · [Index](README.md) · [Case 02 — rm -rf /* →](02-rm-rf-root.md)
