# Cas 07 — bloqué à la frontière d'exécution

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [07-boundary-blocked](../07-boundary-blocked.md).

**Résultat:** ECC rejoué, consommé, altéré, expiré, périmé ou dépassé · `EXECUTION_BLOCKED`

Ce qui se passe quand arrive à `C6` quelque chose qui ne correspond pas à un ECC valide et non rédimé. Chaque variante est enregistrée en `EXECUTION_BLOCKED` avec son `block_reason`, et validée dans `C5` avant que le blocage soit renvoyé. L'API n'est jamais atteinte. La variante E n'a pas de `block_reason` dédié dans la spec actuelle : c'est un point ouvert remonté aux mainteneurs.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["L'agent détient une référence d'ECC<br/>(obtenue comme dans les cas 01 à 03)"]) --> P["Le serveur MCP présente opération + ECC à C6"]
    P --> Q1{"A · ecc.id déjà rédimé ?"}
    Q1 -- oui --> XA[["ECC_ALREADY_REDEEMED"]]
    Q1 -- non --> Q2{"B · auth_ref déjà rédimé<br/>par un autre ECC ?"}
    Q2 -- oui --> XB[["AUTHORIZATION_ALREADY_REDEEMED<br/>montant I-PAY-003 retiré"]]
    Q2 -- non --> Q3{"C · intégrité valide<br/>et non expiré ?"}
    Q3 -- non --> XC[["ECC_INTEGRITY_INVALID ou ECC_EXPIRED<br/>retiré seulement si expiré"]]
    Q3 -- oui --> Q4{"D · registre d'invariants<br/>cohérent ?"}
    Q4 -- non --> XD[["ECC_INVARIANT_STALE<br/>à recompiler · montant retiré"]]
    Q4 -- oui --> Q5{"E · opération dans<br/>authorization_scope ?"}
    Q5 -- non --> XE[["Bloqué · pas de block_reason dédié<br/>(point ouvert) · rien n'est retiré"]]
    Q5 -- oui --> OK(["Admis : voir cas 01 à 03"])
    P2["F · le serveur MCP appelle l'API directement"] -.-> XF[["Refusé au niveau réseau (P4)<br/>aucun secret de l'API hors de C6"]]
    N(["Chaque blocage est validé dans C5 en EXECUTION_BLOCKED<br/>avant d'être renvoyé · l'API n'est jamais atteinte"])
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class XA,XB,XC,XD,XE,XF ko;
    class Q1,Q2,Q3,Q4,Q5 check;
    class OK ok;
    class N note;
```

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Agent IA<br/>(ap-agent-01)
    participant SRV as Serveur MCP<br/>(Agent Surface)
    participant C4 as C4 Invariant Monitor
    participant C6 as C6 Execution Firewall<br/>(passerelle de sortie + Refusal Gateway)
    participant API as API Paiement
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prérequis en place, voir 00-prerequisites : règles signées [S1] et distribuées · approbateurs enrôlés · identités émises · seul C6 atteint l'API (P4)

    Note over AG,C5: Point de départ : ap-agent-01 détient une référence d'ECC obtenue comme dans les cas 01 à 03. Le hook laisse passer les outils enregistrés et n'est pas représenté ici.

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: A · Rejeu d'un ECC déjà rédimé
        AG->>SRV: exécute payment.create avec la référence de l'ECC
        SRV->>C6: même référence d'ECC présentée une seconde fois
        C6->>C6: le CAS sur ecc.id échoue · déjà rédimé
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_ALREADY_REDEEMED
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: I-PAY-003 inchangé : le montant a été compté une fois, pour l'exécution qui a eu lieu
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: B · Deux ECC sous une même autorisation (demandes concurrentes, cas 02 et 03)
        AG->>SRV: exécute payment.create avec la référence de l'ECC
        Note over SRV,C6: Les deux ECC ont été compilés avant tout rachat. Le premier a gagné le CAS et a été exécuté.
        SRV->>C6: second ECC, même auth_ref
        C6->>C6: même CAS · auth_ref déjà rédimé, donc cet ecc.id n'est pas rédimé non plus
        C6->>C5: EXECUTION_BLOCKED · block_reason AUTHORIZATION_ALREADY_REDEEMED
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: Cet ECC ne pourra jamais être rédimé : son montant est retiré de I-PAY-003 (choix de l'exemple)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: C · ECC altéré, ou expiré
        AG->>SRV: exécute payment.create avec la référence de l'ECC
        SRV->>C6: ECC dont le contenu ne correspond plus à son hash, ou dépassant expires_at
        C6->>C6: échec du contrôle d'intégrité ou d'expiration
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_INTEGRITY_INVALID ou ECC_EXPIRED
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: Expiré : le montant est retiré. Altéré : l'ECC authentique reste utilisable jusqu'à expires_at, rien n'est encore retiré
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: D · Registre d'invariants modifié depuis la compilation
        AG->>SRV: exécute payment.create avec la référence de l'ECC
        SRV->>C6: ECC valide, mais un invariant plus récent interdit son périmètre
        C6->>C6: invariant_set_version incohérent
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_INVARIANT_STALE · l'ECC doit être recompilé
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: Cet ECC ne pourra jamais être rédimé : son montant est retiré (choix de l'exemple)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: E · Opération différente de l'ECC (par exemple montant porté de 350 € à 3 500 €)
        AG->>SRV: exécute payment.create avec la référence de l'ECC
        SRV->>C6: ECC valide + opération hors de ecc.authorization_scope
        C6->>C6: opération hors périmètre · rien n'est rédimé
        C6->>C5: EXECUTION_BLOCKED · aucun block_reason dédié dans la spec (point ouvert)
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: L'ECC authentique reste utilisable jusqu'à expires_at, rien n'est encore retiré
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: F · Appel direct de l'API, sans passer par C6
        SRV-xAPI: POST /payments sans passer par C6
        Note over API: Refusé au niveau réseau (P4). Le serveur MCP ne détient de toute façon aucun secret de l'API.
    end
```

[← Cas 06 — exception refusée](06-exception-refused.md) · [Index](README.md)
