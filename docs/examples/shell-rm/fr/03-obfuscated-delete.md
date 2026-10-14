# Cas 03 — suppression déguisée

> **Non normatif.** Fait partie de l'exemple commenté [suppression gouvernée dans le shell avec Claude Code](README.md). Le contexte commun (conception, invariants, identité du sujet, limites, note de neutralité et références) est dans le [README](README.md).

English version: [03-obfuscated-delete](../03-obfuscated-delete.md).

**Résultat:** `bash -c "$(… | base64 -d)"` · `ADMISSION_REJECTED`

Le même `rm -rf /*`, caché dans un contenu base64 exécuté par `bash -c`. L'analyseur de l'Agent Surface n'accepte qu'une grammaire littérale : il n'évalue pas une substitution de commande, parce que l'évaluer, c'est exécuter du code. La commande donne donc `shell.exec_dynamic`, un type qu'aucun rôle n'inclut, et la demande est rejetée à l'admission avec `UNAUTHORIZED_ACTION_CLASS`, avant que `C3` ou `C2` ne la voient. C'est une réduction volontaire de la surface d'action (Part I §2.6, Part III §9.3), pas une supposition sur le contenu. Les règles de Claude Code n'aideraient pas : la documentation précise qu'une règle comme `Bash(rm *)` ne correspond pas à `bash -c '…'` et n'est pas une frontière de sécurité.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>bash -c #quot;$(… | base64 -d)#quot;"]) --> H{"Hook PreToolUse (imposé)<br/>répond à temps ?"}
    H -- "non : onFailure block" --> X0[["Bloqué (voir cas 04)"]]
    H -- oui --> PA["Agent Surface · analyse déterministe<br/>shell.exec_dynamic<br/>(substitution non évaluée)"]
    PA --> S{"RBAC sur gar.type<br/>un rôle l'inclut-il ?"}
    S -- non --> X1[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS"]]
    X1 ~~~ N1["Évaluer la substitution, c'est exécuter du code :<br/>la grammaire acceptée est volontairement littérale"]
    N1 ~~~ N2["Bash(rm *) ne correspondrait pas non plus :<br/>les règles Bash ne sont pas une frontière de sécurité"]
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class H,PA,S check;
    class X0,X1 ko;
    class N1,N2 note;
```

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Agent Claude Code<br/>(utilisateur système claude-agent)
    participant CC as Outil Bash<br/>(bac à sable OS)
    participant HK as Hook PreToolUse<br/>(imposé · onFailure block)
    participant SRV as Passerelle CROA<br/>(Agent Surface + analyseur shell)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prérequis en place, voir 00-prerequisites : /ws propriété de croa-exec · Claude Code tourne sous claude-agent · réglages imposés · règles signées [S1]

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Admission · rejetée avant le pipeline
        AG->>CC: appel de l'outil Bash : bash -c "$(echo cm0gLXJmIC8q | base64 -d)"
        CC->>HK: PreToolUse (tool_name Bash · tool_input.command · session_id · cwd)
        HK->>SRV: appel d'outil (commande, cwd, session_id) par le socket Unix de la passerelle · la passerelle en construit le gar.*
        SRV->>SRV: sujet = utilisateur système claude-agent, d'après les identifiants du pair sur le socket · identifiant de session CROA émis par la passerelle, session_id de Claude Code conservé pour la corrélation
        SRV->>SRV: analyse déterministe, grammaire littérale uniquement → une substitution de commande : hors de la grammaire littérale → gar.type shell.exec_dynamic
        SRV->>SRV: RBAC sur gar.type : shell.exec_dynamic est un type déclaré, mais aucun rôle ne l'inclut
        SRV->>C5: ADMISSION_REJECTED · rejection_reason UNAUTHORIZED_ACTION_CLASS · attempted_type shell.exec_dynamic · subject_id claude-agent · session_id · emitter Agent Surface
        Note over SRV: L'analyseur n'évalue pas la substitution : l'évaluer, c'est exécuter du code. La grammaire acceptée est volontairement réduite (§2.6, Part III §9.3)
        SRV--xHK: rejeté + motif
        HK--xCC: permissionDecision deny · permissionDecisionReason
        CC--xAG: erreur d'outil : refusé (Claude voit le motif)
        Note over AG,HK: Une règle Claude Code comme Bash(rm *) ne correspondrait pas non plus : la documentation dit que les règles Bash ne sont pas une frontière de sécurité
    end
```

[← Cas 02 — rm -rf /*](02-rm-rf-root.md) · [Index](README.md) · [Cas 04 — tentatives de contournement →](04-raw-shell-bypass.md)
