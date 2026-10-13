# Cas 02 — 3 500 €, exception Responsable Finance

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [02-exception-finance-3500](../02-exception-finance-3500.md).

**Résultat:** 3 500 € · `DENY`, puis `PERMIT_WITH_AUTHORIZATION` · exécuté

3 500 € viole `I-PAY-001`. `C2` refuse via la Refusal Gateway. Un demandeur humain, jamais l'agent, demande une exception à `C1`, un Responsable Finance signe, et `C1` émet un artefact d'autorisation à usage unique. L'agent soumet ensuite une nouvelle demande sans champ d'autorisation : `C2` trouve l'autorisation dans le registre de `C1` et rend `PERMIT_WITH_AUTHORIZATION`. `C7` lie `ecc.auth_ref` et `ecc.exception_scope`, et `C6` rédime `ecc.id` et `ecc.auth_ref` dans le même compare-and-swap.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["Agent IA · payment.create 3 500 €"]) --> H{"Hook<br/>outil dans l'allowlist ?"}
    H -- non --> X1[["Bloqué localement<br/>(voir cas 04)"]]
    H -- oui --> S{"Serveur MCP · Agent Surface<br/>sujet authentifié, RBAC ?"}
    S -- non --> X2[["ADMISSION_REJECTED<br/>(voir cas 04)"]]
    S -- oui --> G{"C3 · ancrage<br/>bénéficiaire et facture connus ?"}
    G -- non --> X3[["CONTEXT_FAILURE<br/>refus via C6 (voir cas 05)"]]
    G -- oui --> D{"C2 · C2.eval<br/>avec l'état de C4"}
    D -- "3 500 € · I-PAY-001 violé(s)" --> DN[["DENY · I-PAY-001 violé(s)<br/>refus structuré via la Refusal Gateway de C6"]]
    DN --> EC(["Fin de l'appel MCP<br/>DENY rendu immédiatement, rien ne reste ouvert"])
    subgraph ESC["Escalade asynchrone, hors de tout appel MCP (minutes à jours)"]
        direction TB
        RQ["Le demandeur ouvre une demande ITSM<br/>qui référence le DENY dans C5"] --> AK["C1 sollicite l'approbateur (Resp. Finance)"]
        AK --> DC{"Décision de l'approbateur"}
        DC -- "signe [S2]" --> VR["C1 vérifie [S2] et le rôle<br/>dans l'annuaire de référence"]
        VR --> IS["C1 émet l'autorisation [S1]<br/>lève I-PAY-001 · usage unique · expires_at"]
        IS --> DI["C1 la distribue à C2"]
        DI --> INF["Le demandeur informe l'agent"]
    end
    EC --> RQ
    DC -. "refus" .-> X6[["refus : voir cas 06"]]
    INF --> NC(["Nouvel appel MCP, avant expires_at<br/>mêmes paramètres, nouveau request_id"])
    NC --> AG2["Admission et ancrage à nouveau<br/>(hook, Agent Surface, C3)"]
    AG2 --> S5["C2 · étape 5 : violation couverte par une autorisation<br/>valide et non rédimée → PERMIT_WITH_AUTHORIZATION"]
    S5 --> E
    E["C7 · compile l'ECC, le signe [S3]<br/>auth_ref + exception_scope · R2"] --> R(["L'agent reçoit<br/>la référence de l'ECC"])
    R --> F{"C6 · frontière d'exécution<br/>ECC valide, bon sujet ?"}
    F -- non --> X4[["EXECUTION_BLOCKED<br/>(voir cas 07)"]]
    F -- oui --> CAS["C6 · un seul CAS : ecc.id + auth_ref rédimés<br/>EXECUTION_AUTHORIZED dans C5"]
    CAS --> API[("API de paiement<br/>201 paiement créé")]
    API --> OK(["EXECUTION_COMPLETED<br/>paiement exécuté"])

    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class S5,E,CAS,API,OK ok;
    class X1,X2,X3,DN,X6,X4 ko;
    class H,S,G,D,F,AG2 check;
    class RQ,AK,DC,VR,IS,DI,INF human;
    class EC,NC note;
```

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

    Note over AG,C5: Prérequis en place, voir 00-prerequisites : règles signées [S1] et distribuées · approbateurs enrôlés · identités émises · seul C6 atteint l'API (P4)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        AG->>HK: tool_call payment.create(amount, beneficiary_id, invoice_id)
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
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Approbation accordée · C1 émet l'artefact d'autorisation
        APP->>C1: approuve · signature personnelle de l'approbateur [S2] (clé personnelle + MFA)
        C1->>C1: vérifie la signature [S2] et le rôle de l'approbateur dans l'annuaire de référence · Resp. Finance ou plus requis pour I-PAY-001
        C1->>C1: émet l'artefact d'autorisation · auth_id · sujet ap-agent-01 · classe d'action unique payment.create · bénéficiaire, facture, montant ≤ 3 500 € · lève I-PAY-001 · usage unique · expires_at · signé avec la clé de C1 [S1]
        C1->>C5: POLICY_ARTIFACT_ISSUED · artifact_action ISSUED · policy_artifact_id = auth_id
        C1->>C2: distribue l'artefact d'autorisation signé [S1]
        C2->>C2: vérifie la signature [S1] · l'ajoute au jeu vérifié
        REQ->>AG: exception accordée, relancer (hors bande)
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Resoumission · PERMIT_WITH_AUTHORIZATION
        AG->>HK: tool_call payment.create (mêmes paramètres, aucun champ d'autorisation)
        HK->>SRV: appel de l'outil
        SRV->>SRV: authentification du sujet · RBAC · qualification
        SRV->>C3: nouveau gar.* (nouveau request_id)
        C3->>C3: ancrage (identique)
        C3->>C2: gga.* · GROUNDED
        C2->>C4: action en cours d'évaluation
        C4-->>C2: état courant des invariants
        C2->>C2: étape 5 · I-PAY-001 violé(s) mais couvert(s) par une autorisation valide, applicable, non rédimée et non révoquée
        C2->>C5: PERMIT · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C2->>C4: permis · ajout de 3 500 € à l'agrégat I-PAY-003 (sérialisé par clé)
        C2->>C7: PERMIT_WITH_AUTHORIZATION + artefact d'autorisation
        C7->>C7: compile l'ECC et le signe avec la clé de C7 [S3] · auth_ref = auth_id · exception_scope copié à l'identique · reversibility_class R2 · compensating_controls (facture approuvée)
    end
    rect rgba(60, 120, 220, 0.10)
        Note over AG,C5: Exécution · ECC présenté à la frontière
        C7->>C5: ECC_COMPILED · ecc_id · decision_basis PERMIT_WITH_AUTHORIZATION · auth_id
        C7->>SRV: référence de l'ECC + notification de décision (§4.10)
        SRV-->>HK: permis + référence de l'ECC
        HK-->>AG: permis + référence de l'ECC
        AG->>HK: exécute payment.create avec la référence de l'ECC
        HK->>SRV: appel de l'outil + référence de l'ECC
        SRV->>SRV: échange de jeton auprès du fournisseur d'identité (RFC 8693) · sub ap-agent-01 · act mcp-payment-server · aud C6
        SRV->>C6: opération + référence de l'ECC + jeton échangé
        Note over C6: Frontière d'exécution (TB-3)
        C6->>C6: signature [S3] de C7 et époque du signataire · non expiré · non révoqué · invariant_set_version cohérent · opération dans authorization_scope et exception_scope · sub égal à ecc.subject · act présentateur enregistré
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Admis
        C6->>C6: un seul CAS linéarisable · rédime ecc.id + ecc.auth_ref
        C6->>C5: EXECUTION_AUTHORIZED · ecc_id · auth_id
        C5-->>C6: validé
        C6->>API: POST /payments · identité de service de C6 (authentification, pas une signature d'autorisation)
        API-->>C6: 201 paiement créé
        API--)C4: notification de changement d'état
        C4->>C4: vérification des invariants après exécution
        C6->>C5: EXECUTION_COMPLETED · ecc_id · exit_status
        C6-->>SRV: résultat
        SRV-->>HK: résultat
        HK-->>AG: paiement exécuté
    end

    Note over API: N'accepte que le trafic issu de C6 (P4, contrôle réseau). Ni l'agent ni le serveur MCP ne détiennent de secret de l'API.
```

[← Cas 01 — 350 €, automatique](01-auto-350.md) · [Index](README.md) · [Cas 03 — 7 500 €, exception CFO →](03-exception-cfo-7500.md)
