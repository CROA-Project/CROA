# Cas 07 — bloqué à la frontière d'exécution

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [07-boundary-blocked](../07-boundary-blocked.md).

**Résultat:** ECC rejoué, consommé, altéré, expiré, périmé ou dépassé · `EXECUTION_BLOCKED`

Ce qui se passe quand arrive à `C6` quelque chose qui ne correspond pas à un ECC valide et non rédimé. Chaque variante est enregistrée en `EXECUTION_BLOCKED` avec son `block_reason`, et validée dans `C5` avant que le blocage soit renvoyé. L'API n'est jamais atteinte. La variante E n'a pas de `block_reason` dédié dans la spec actuelle : c'est un point ouvert remonté aux mainteneurs.

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

    Note over AG,C5: Point de départ : ap-agent-01 détient une référence d'ECC obtenue comme dans les cas 01 à 03

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: A · Rejeu d'un ECC déjà rédimé
        SRV->>C6: même référence d'ECC présentée une seconde fois
        C6->>C6: le CAS sur ecc.id échoue · déjà rédimé
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_ALREADY_REDEEMED
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: B · Nouvel ECC sous une autorisation déjà consommée (cas 02, 03)
        SRV->>C6: second ECC dont l'auth_ref pointe vers un auth_id déjà rédimé
        C6->>C6: même CAS · auth_ref déjà rédimé, donc ecc.id n'est pas rédimé non plus
        C6->>C5: EXECUTION_BLOCKED · block_reason AUTHORIZATION_ALREADY_REDEEMED
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: Le montant réservé dans l'agrégat I-PAY-003 est libéré (choix de l'exemple)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: C · ECC altéré, ou expiré
        SRV->>C6: ECC dont le contenu ne correspond plus à son hash, ou dépassant expires_at
        C6->>C6: échec du contrôle d'intégrité ou d'expiration
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_INTEGRITY_INVALID ou ECC_EXPIRED
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: Le montant réservé dans l'agrégat I-PAY-003 est libéré (choix de l'exemple)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: D · Registre d'invariants modifié depuis la compilation
        SRV->>C6: ECC valide, mais un invariant plus récent interdit son périmètre
        C6->>C6: invariant_set_version incohérent
        C6->>C5: EXECUTION_BLOCKED · block_reason ECC_INVARIANT_STALE · l'ECC doit être recompilé
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: Le montant réservé dans l'agrégat I-PAY-003 est libéré (choix de l'exemple)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: E · Opération différente de l'ECC (par exemple montant porté de 350 € à 3 500 €)
        SRV->>C6: ECC valide + opération hors de ecc.authorization_scope
        C6->>C6: opération hors périmètre
        C6->>C5: EXECUTION_BLOCKED · aucun block_reason dédié dans la spec (point ouvert)
        C5-->>C6: validé
        C6--xSRV: blocage structuré · seulement après validation dans C5
        SRV--xAG: BLOQUÉ · API jamais atteinte
        Note over C4: Le montant réservé dans l'agrégat I-PAY-003 est libéré (choix de l'exemple)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: F · Appel direct de l'API, sans passer par C6
        SRV-xAPI: POST /payments sans passer par C6
        Note over API: Refusé au niveau réseau (P4). Le serveur MCP ne détient de toute façon aucun secret de l'API.
    end
```

[← Cas 06 — exception refusée](06-exception-refused.md) · [Index](README.md)
