# Cas 04 — outil non enregistré

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [04-unregistered-tool](../04-unregistered-tool.md).

**Résultat:** Outil non enregistré · bloqué à trois niveaux

L'agent appelle un outil non enregistré (`wire.transfer`). Le hook l'arrête en premier, mais ce n'est qu'une défense en profondeur. Si le hook est contourné, l'Agent Surface rejette la demande avec `ADMISSION_REJECTED` (`UNAUTHORIZED_ACTION_CLASS`). Si les deux étaient contournés, il n'y aurait toujours pas d'ECC : `C6` bloque et l'API reste inaccessible (P4). L'accès à un outil ne vaut pas autorité d'exécution.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["Agent IA · wire.transfer(...)<br/>outil non enregistré"]) --> H{"Couche 1 · hook<br/>outil dans l'allowlist ?"}
    H -- non --> X1[["Bloqué localement<br/>rien n'est envoyé"]]
    H -. "hook contourné ou mal configuré" .-> S{"Couche 2 · Agent Surface<br/>un rôle RBAC inclut-il cette action ?"}
    S -- non --> X2[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS · dans C5"]]
    S -. "les deux contournés" .-> F{"Couche 3 · C6<br/>ECC présenté ?"}
    F -- non --> X3[["EXECUTION_BLOCKED<br/>ECC_NOT_FOUND · dans C5"]]
    X1 ~~~ N(["API jamais atteinte<br/>seul C6 peut la joindre (P4)"])
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class X1,X2,X3 ko;
    class H,S,F check;
    class N note;
```

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Agent IA<br/>(ap-agent-01)
    participant HK as Hook préalable<br/>(défense en profondeur)
    participant SRV as Serveur MCP<br/>(Agent Surface)
    participant C6 as C6 Execution Firewall<br/>(passerelle de sortie + Refusal Gateway)
    participant API as API Paiement
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prérequis en place, voir 00-prerequisites : règles signées [S1] et distribuées · approbateurs enrôlés · identités émises · seul C6 atteint l'API (P4)

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Couche 1 · hook (défense en profondeur uniquement)
        AG->>HK: tool_call wire.transfer(...) · absent de l'allowlist
        HK->>HK: outil absent de l'allowlist
        HK--xAG: bloqué localement (fail-closed) · rien n'est envoyé
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Couche 2 · hook contourné ou mal configuré → Agent Surface
        AG->>SRV: appel direct wire.transfer(...)
        SRV->>SRV: authentification du sujet · RBAC : aucun rôle d'ap-agent-01 n'inclut ce type d'action
        SRV->>C5: ADMISSION_REJECTED · rejection_reason UNAUTHORIZED_ACTION_CLASS · attempted_type
        SRV--xAG: rejeté à l'Agent Surface · rien n'atteint C3 ni C2
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Couche 3 · les deux contournés → frontière d'exécution (la vraie garantie)
        AG->>C6: opération sans référence d'ECC
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_NOT_FOUND
        C5-->>C6: validé
        C6--xAG: blocage structuré
    end

    Note over API: Jamais atteinte. N'accepte que le trafic issu de C6 (P4, contrôle réseau).
```

[← Cas 03 — 7 500 €, exception CFO](03-exception-cfo-7500.md) · [Index](README.md) · [Cas 05 — échec d'ancrage →](05-context-failure.md)
