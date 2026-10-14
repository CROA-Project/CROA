# Case 03 — obfuscated delete

> **Non-normative.** Part of the [governed shell delete with Claude Code](README.md) worked example. The shared context (design, invariants, subject binding, limits, vendor-neutrality note and references) is in the [README](README.md).

Version française: [03-obfuscated-delete](fr/03-obfuscated-delete.md).

**Outcome:** `bash -c "$(… | base64 -d)"` · `ADMISSION_REJECTED`

The same `rm -rf /*`, hidden in a base64 payload run by `bash -c`. The Agent Surface's parser accepts only a literal grammar: it does not evaluate a command substitution, because evaluating it means running code. The command therefore parses to `shell.exec_dynamic`, a type no role includes, and the request is rejected at admission with `UNAUTHORIZED_ACTION_CLASS`, before `C3` or `C2` see it. This is a deliberate narrowing of the action surface (Part I §2.6, Part III §9.3), not a guess about the payload. Claude Code's own rules would not help here: the docs state that a rule like `Bash(rm *)` does not match `bash -c '…'` and is not a security boundary.

## Overview

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>bash -c #quot;$(… | base64 -d)#quot;"]) --> H{"PreToolUse hook (managed)<br/>answers in time?"}
    H -- "no: onFailure block" --> X0[["Blocked (see case 04)"]]
    H -- yes --> PA["Agent Surface · deterministic parse<br/>shell.exec_dynamic<br/>(substitution not evaluated)"]
    PA --> S{"RBAC on gar.type<br/>does a role include it?"}
    S -- no --> X1[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS"]]
    X1 ~~~ N1["Evaluating the substitution means running code:<br/>the accepted grammar is literal-only on purpose"]
    N1 ~~~ N2["Bash(rm *) would not match either:<br/>Bash rules are not a security boundary"]
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class H,PA,S check;
    class X0,X1 ko;
    class N1,N2 note;
```

## Sequence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Claude Code agent<br/>(OS user claude-agent)
    participant CC as Bash tool<br/>(OS sandbox)
    participant HK as PreToolUse hook<br/>(managed · onFailure block)
    participant SRV as CROA gateway<br/>(Agent Surface + shell parser)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prerequisites in place, see 00-prerequisites: /ws owned by croa-exec · Claude Code runs as claude-agent · managed settings · rules signed [S1]

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Admission · rejected before the pipeline
        AG->>CC: Bash tool call: bash -c "$(echo cm0gLXJmIC8q | base64 -d)"
        CC->>HK: PreToolUse (tool_name Bash · tool_input.command · session_id · cwd)
        HK->>SRV: tool call (command, cwd, session_id) over the gateway's Unix socket · the gateway builds gar.* from it
        SRV->>SRV: subject = OS user claude-agent, from the socket peer credentials · CROA session id issued by the gateway, Claude Code session_id kept for correlation
        SRV->>SRV: deterministic parse, literal-only grammar → a command substitution: outside the literal-only grammar → gar.type shell.exec_dynamic
        SRV->>SRV: RBAC on gar.type: shell.exec_dynamic is a declared type, but no role includes it
        SRV->>C5: ADMISSION_REJECTED · rejection_reason UNAUTHORIZED_ACTION_CLASS · attempted_type shell.exec_dynamic · subject_id claude-agent · session_id · emitter Agent Surface
        Note over SRV: The parser does not evaluate the substitution: evaluating it means running code. The accepted grammar is narrowed on purpose (§2.6, Part III §9.3)
        SRV--xHK: rejected + reason
        HK--xCC: permissionDecision deny · permissionDecisionReason
        CC--xAG: tool error: denied (Claude sees the reason)
        Note over AG,HK: A Claude Code rule such as Bash(rm *) would not match this command either: the docs say Bash rules are not a security boundary
    end
```

[← Case 02 — rm -rf /*](02-rm-rf-root.md) · [Index](README.md) · [Case 04 — attempts to bypass CROA →](04-raw-shell-bypass.md)
