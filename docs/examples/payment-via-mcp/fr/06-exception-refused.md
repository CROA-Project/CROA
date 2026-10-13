# Cas 06 — exception refusée

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [06-exception-refused](../06-exception-refused.md).

**Résultat:** 3 500 € · `DENY` · approbation refusée ou expirée · rien n'est exécuté

Commence comme le cas 02, mais l'approbateur refuse, ou ne répond pas avant l'expiration de la demande. `C1` n'émet aucun artefact d'autorisation et enregistre le refus. Le `DENY` tient : toute resoumission est de nouveau refusée sur `I-PAY-001`, rien n'est compilé, et l'agrégat I-PAY-003 reste inchangé.

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Agent IA<br/>(ap-agent-01)
    participant HK as Hook préalable<br/>(défense en profondeur)
    participant SRV as Serveur MCP<br/>(Agent Surface)
    participant C3 as C3 Path Resolver
    participant C2 as C2 Execution Governor
    participant C4 as C4 Invariant Monitor
    participant C1 as C1 Policy Authority
    actor REQ as Demandeur<br/>(comptable · ITSM)
    actor APP as Approbateur<br/>(Resp. Finance / CFO)
    participant C7 as C7 Contract Compiler
    participant C6 as C6 Execution Firewall<br/>(passerelle de sortie + Refusal Gateway)
    participant API as API Paiement
    participant C5 as C5 Audit (append-only)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Prérequis · avant toute demande (à l'émission ou à chaque modification)
        C1->>C2: distribue les artefacts de politique signés (I-PAY-001, I-PAY-002, I-PAY-003)
        C1->>C5: POLICY_ARTIFACT_ISSUED
        C2->>C2: vérifie la signature de C1 · conserve le dernier jeu vérifié (§4.3)
    end

    AG->>HK: tool_call payment.create(amount, beneficiary_id, invoice_id)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        HK->>SRV: appel de l'outil (outil présent dans l'allowlist)
        SRV->>SRV: authentification du sujet (identité de charge de travail) · RBAC · qualification
        SRV->>C3: gar.* (nouveau request_id · ap-agent-01 · payment.create · beneficiary_id · invoice_id · amount)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Ancrage
        C3->>C3: ancrage dans le Federated Context Registry · référentiel fournisseurs · facture approuvée, non payée, bénéficiaire identique, montant ≤ solde restant
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Évaluation
        C3->>C2: gga.* · semantic_result GROUNDED
        C2->>C4: action en cours d'évaluation
        C4-->>C2: état des invariants · agrégat I-PAY-003 pour (ap-agent-01, beneficiary_id)
        C2->>C2: C2.eval déterministe (étapes 1 à 6) sur le dernier jeu d'artefacts vérifié
    end
    rect rgba(230, 160, 40, 0.12)
        Note over AG,C5: DENY · I-PAY-001 violé(s) · pas encore d'artefact d'autorisation
        C2->>C5: DENY · deny_reason I-PAY-001 · invariant_state [I-PAY-001]
        C2->>C6: signal de refus
        C6--xSRV: réponse à la demande gar.* · refus structuré · identifiant d'invariant · référence C5 · Refusal Gateway
        SRV--xHK: DENY
        HK--xAG: DENY
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Escalade déclenchée par un humain · ce que produit l'agent n'est jamais une entrée de C1 (§4.3)
        REQ->>C1: demande d'exception via l'ITSM · référence l'enregistrement DENY de C5
        C1->>C5: demande d'exception enregistrée
        C1->>APP: demande d'approbation (bénéficiaire, facture, montant, invariant à lever I-PAY-001)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: Approbation refusée ou expirée
        APP--xC1: refus, ou pas de réponse avant expiration de la demande
        C1->>C5: refus d'exception enregistré
        REQ->>AG: exception refusée (hors bande)
        Note over C2,C7: Aucun artefact d'autorisation n'existe : une resoumission est de nouveau refusée sur I-PAY-001, et rien n'est jamais compilé
        Note over C4: Rien n'a été permis : l'agrégat I-PAY-003 est inchangé
    end

    Note over API: Jamais atteinte : aucun ECC n'existe (P4).
```

[← Cas 05 — échec d'ancrage](05-context-failure.md) · [Index](README.md) · [Cas 07 — bloqué à la frontière d'exécution →](07-boundary-blocked.md)
