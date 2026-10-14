# Case 02 — rm -rf /*

> **Non-normative.** Part of the [governed shell delete with Claude Code](README.md) worked example. The shared context (design, invariants, subject binding, limits, vendor-neutrality note and references) is in the [README](README.md).

Version française: [02-rm-rf-root](fr/02-rm-rf-root.md).

**Outcome:** `rm -rf /*` · `CONTEXT_FAILURE` · refused, nothing deleted

The glob `/*` expands to `/bin`, `/etc`, `/home`, … and to `/ws` itself. This example scopes `C3`'s registry to `/ws`, so `/bin` and `/etc` are not registered entities: deleting them is outside the action surface by design (Part II §4.5.2, Part III §9.3). The references are unresolvable rather than partially verified, so `C3` records `CONTEXT_FAILURE` and hands the request to `C6`, which refuses it through the Refusal Gateway. The request never reaches `C2`, so no ECC can exist. Neither the hook's judgment nor a human stops it. The grey zone shows why the sandbox alone is not enough: with its default settings it protects `/bin` and `/etc`, but it leaves the working directory writable, so the same command would erase the workspace.

## Overview

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>rm -rf /*"]) --> H{"PreToolUse hook (managed)<br/>answers in time?"}
    H -- "no: onFailure block" --> X0[["Blocked (see case 04)"]]
    H -- yes --> PA["Agent Surface · deterministic parse<br/>fs.delete · recursive · pattern /*"]
    PA --> S{"RBAC on gar.type<br/>does a role include it?"}
    S -- no --> X1[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS"]]
    S -- yes --> G{"C3 · expands /* against the registry<br/>all targets registered?"}
    G -- "no: /bin, /etc, … unresolvable" --> CF["CONTEXT_FAILURE in C5<br/>handed to C6, never to C2"]
    CF --> X[["Structured deny via the Refusal Gateway<br/>no decision · no ECC"]]
    X ~~~ W["Counterfactual · sandbox alone, defaults:<br/>/bin and /etc protected, but the working<br/>directory is writable, so /ws is erased"]
    W ~~~ Y["Here /ws belongs to croa-exec:<br/>even that path ends in EPERM"]
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class H,PA,S,G check;
    class X0,X1,CF,X ko;
    class W warn;
    class Y ok;
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
    participant C6 as C6 executor<br/>(OS user croa-exec · only writer)
    participant FS as Workspace /ws<br/>(owned by croa-exec · read-only for claude-agent)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prerequisites in place, see 00-prerequisites: /ws owned by croa-exec · Claude Code runs as claude-agent · managed settings · rules signed [S1]

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        AG->>CC: Bash tool call: rm -rf /*
        CC->>HK: PreToolUse (tool_name Bash · tool_input.command · session_id · cwd)
        HK->>SRV: tool call (command, cwd, session_id) over the gateway's Unix socket · the gateway builds gar.* from it
        SRV->>SRV: subject = OS user claude-agent, from the socket peer credentials · CROA session id issued by the gateway, Claude Code session_id kept for correlation
        SRV->>SRV: deterministic parse, literal-only grammar → gar.type fs.delete · recursive true · pattern /* passed unexpanded in gar.context_refs
        SRV->>SRV: RBAC on gar.type: the role of claude-agent includes fs.delete · qualification
        SRV->>C3: gar.* (new request_id · type fs.delete · targets)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Grounding fails · the registry is scoped to /ws
        C3->>C3: expands /* against the registry: it covers /bin, /etc, /home, … which are not registered · unresolvable, not partially verified, so no bounded trust
        C3->>C5: CONTEXT_FAILURE · unresolved_refs /bin, /etc, …
        C3->>C6: gga.* with semantic_result CONTEXT_FAILURE
        Note over C3,C6: Never forwarded to C2: no decision, so no ECC can exist. I-FS-001 and I-FS-002 would also deny it: defense in depth
        C6--xSRV: answer to the gar.* request · structured deny · C5 reference · Refusal Gateway
        SRV--xHK: DENY + reason
        HK--xCC: permissionDecision deny · permissionDecisionReason
        CC--xAG: tool error: denied (Claude sees the reason)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Counterfactual · Claude Code sandbox alone, default settings, no CROA
        Note over CC,FS: The sandbox would block writes to /bin, /etc, … but by default the working directory is writable: the glob reaches /ws and erases it
        Note over CC,FS: Here /ws belongs to croa-exec: even that path ends in EPERM
    end
```

[← Case 01 — rm of a workspace file](01-rm-workspace-file.md) · [Index](README.md) · [Case 03 — obfuscated delete →](03-obfuscated-delete.md)
