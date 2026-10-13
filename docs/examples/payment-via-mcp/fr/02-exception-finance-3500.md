# Cas 02 — 3 500 €, exception Responsable Finance

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [02-exception-finance-3500](../02-exception-finance-3500.md).

**Résultat:** 3 500 € · `DENY`, puis `PERMIT_WITH_AUTHORIZATION` · exécuté

3 500 € viole `I-PAY-001`. `C2` refuse via la Refusal Gateway. Un demandeur humain, jamais l'agent, demande une exception à `C1`, un Responsable Finance signe, et `C1` émet un artefact d'autorisation à usage unique. L'agent soumet ensuite une nouvelle demande sans champ d'autorisation : `C2` trouve l'autorisation dans le registre de `C1` et rend `PERMIT_WITH_AUTHORIZATION`. `C7` lie `ecc.auth_ref` et `ecc.exception_scope`, et `C6` rédime `ecc.id` et `ecc.auth_ref` dans le même compare-and-swap.

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
        C1-->>C2: artefacts de politique signés (I-PAY-001, I-PAY-002, I-PAY-003) et éventuels artefacts d'autorisation
        C2->>C4: action en cours d'évaluation
        C4-->>C2: état des invariants · agrégat I-PAY-003 pour (ap-agent-01, beneficiary_id)
        C2->>C2: C2.eval déterministe (étapes 1 à 6)
    end
    rect rgba(230, 160, 40, 0.12)
        Note over AG,C5: DENY · I-PAY-001 violé(s) · pas encore d'artefact d'autorisation
        C2->>C5: DENY · deny_reason I-PAY-001 · invariant_state [I-PAY-001]
        C2->>C6: signal de refus
        C6--xSRV: refus structuré · identifiant d'invariant · référence C5 · Refusal Gateway
        SRV--xAG: DENY
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Escalade déclenchée par un humain · ce que produit l'agent n'est jamais une entrée de C1 (§4.3)
        REQ->>C1: demande d'exception via l'ITSM · référence l'enregistrement DENY de C5
        C1->>C5: demande d'exception enregistrée
        C1->>APP: demande d'approbation (bénéficiaire, facture, montant, invariant à lever I-PAY-001)
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Approbation accordée · C1 émet l'artefact d'autorisation
        APP->>C1: signature personnelle (clé + MFA)
        C1->>C1: vérifie le rôle de l'approbateur dans l'annuaire de référence · Resp. Finance ou plus requis pour I-PAY-001
        C1->>C1: émet l'artefact d'autorisation · auth_id · sujet ap-agent-01 · classe d'action unique payment.create · bénéficiaire, facture, montant ≤ 3 500 € · lève I-PAY-001 · usage unique · expires_at
        C1->>C5: POLICY_ARTIFACT_ISSUED · artifact_action ISSUED · policy_artifact_id = auth_id
        REQ-->>AG: exception accordée, relancer (hors bande)
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Resoumission · PERMIT_WITH_AUTHORIZATION
        AG->>SRV: nouveau gar.* (nouveau request_id, mêmes paramètres, aucun champ d'autorisation)
        SRV->>C3: gar.* · admission identique
        C3->>C2: gga.* · GROUNDED
        C1-->>C2: artefact d'autorisation issu du registre de C1
        C4-->>C2: état courant des invariants
        C2->>C2: étape 5 · I-PAY-001 violé(s) mais couvert(s) par une autorisation valide, applicable, non rédimée et non révoquée
        C2->>C5: PERMIT · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C2->>C4: permis · ajout de 3 500 € à l'agrégat I-PAY-003 (sérialisé par clé)
        C2->>C7: PERMIT_WITH_AUTHORIZATION + artefact d'autorisation
        C7->>C7: compile et signe l'ECC · auth_ref = auth_id · exception_scope copié à l'identique · reversibility_class R2 · compensating_controls (facture approuvée)
    end
    rect rgba(60, 120, 220, 0.10)
        Note over AG,C5: Exécution · ECC présenté à la frontière
        C7->>C5: ECC_COMPILED · ecc_id · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C7-->>SRV: référence de l'ECC
        SRV-->>AG: permis + référence de l'ECC
        AG->>SRV: exécute payment.create avec la référence de l'ECC
        SRV->>SRV: échange de jeton (RFC 8693) · sub ap-agent-01 · act mcp-payment-server · aud C6
        SRV->>C6: opération + référence de l'ECC + jeton échangé
        Note over C6: Frontière d'exécution (TB-3)
        C6->>C6: signature C7 et époque du signataire · non expiré · non révoqué · invariant_set_version cohérent · opération dans authorization_scope et exception_scope · sub égal à ecc.subject · act présentateur enregistré
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Admis
        C6->>C6: un seul CAS linéarisable · rédime ecc.id + ecc.auth_ref
        C6->>C5: EXECUTION_AUTHORIZED · ecc_id · auth_id
        C5-->>C6: validé
        C6->>API: POST /payments · identité de service de C6
        API-->>C6: 201 paiement créé
        API--)C4: notification de changement d'état
        C4->>C4: vérification des invariants après exécution
        C6->>C5: EXECUTION_COMPLETED · ecc_id · exit_status
        C6-->>SRV: résultat
        SRV-->>AG: paiement exécuté
    end

    Note over API: N'accepte que le trafic issu de C6 (P4, contrôle réseau). Ni l'agent ni le serveur MCP ne détiennent de secret de l'API.
```

[← Cas 01 — 350 €, automatique](01-auto-350.md) · [Index](README.md) · [Cas 03 — 7 500 €, exception CFO →](03-exception-cfo-7500.md)
