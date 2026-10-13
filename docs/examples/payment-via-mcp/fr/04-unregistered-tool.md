# Cas 04 — outil non enregistré

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [04-unregistered-tool](../04-unregistered-tool.md).

**Résultat:** Outil non enregistré · bloqué à trois niveaux

L'agent appelle un outil non enregistré (`wire.transfer`). Le hook l'arrête en premier, mais ce n'est qu'une défense en profondeur. Si le hook est contourné, l'Agent Surface rejette la demande avec `ADMISSION_REJECTED` (`UNAUTHORIZED_ACTION_CLASS`). Si les deux étaient contournés, il n'y aurait toujours pas d'ECC : `C6` bloque et l'API reste inaccessible (P4). L'accès à un outil ne vaut pas autorité d'exécution.

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
