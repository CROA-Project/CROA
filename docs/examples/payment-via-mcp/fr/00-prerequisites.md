# 00 — Prérequis

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [00-prerequisites](../00-prerequisites.md).

**Portée:** Ce qui doit être en place avant toute demande

Ce n'est pas un cas : c'est l'état sur lequel reposent tous les cas. Quatre choses sont en place avant la première demande. Les règles (`I-PAY-001` à `003`) passent par une pull request, une validation en CI et l'approbation d'une seconde personne, puis `C1` les signe [S1] et les distribue à `C2` et `C3`. Les approbateurs sont enrôlés dans l'annuaire de référence avec leur clé personnelle et leur rôle : c'est ce qui permet ensuite à `C1` de vérifier leur signature [S2]. L'agent reçoit son identité de charge de travail et son rôle RBAC, et le serveur MCP est enregistré comme présentateur. Enfin, la clé de `C7` [S3] est connue de `C6`, et seul `C6` peut atteindre l'API de paiement (P4). Les étapes de ce fichier ne font pas partie d'une demande ; dans les cas, la numérotation commence à l'appel de l'agent.

## Vue d'ensemble

```mermaid
flowchart TD
    subgraph R1["1 · Règles (Part III §7.2, §7.3)"]
        direction TB
        PR["Pull request<br/>invariants I-PAY-001 à 003"] --> CI["Validation CI<br/>schémas + registre d'invariants"]
        CI --> AP2["Approbation par une seconde personne<br/>(proposition ≠ approbation)"]
        AP2 --> MG["Fusion dans la branche principale"]
        MG --> SG["C1 signe l'artefact [S1]<br/>clé dans un HSM"]
        SG --> LOG["C5 · POLICY_ARTIFACT_ISSUED"]
        SG --> D2["C2 vérifie [S1]<br/>conserve le dernier jeu vérifié"]
        SG --> D3["C3 vérifie [S1]"]
    end
    subgraph R2["2 · Approbateurs"]
        direction TB
        EN["L'approbateur s'enrôle<br/>clé personnelle + MFA"] --> DIR["Annuaire de référence<br/>identité, clé, rôle (Resp. Finance, CFO)"]
        DIR -. "au moment de l'approbation (cas 02, 03)" .-> USE["C1 vérifie [S2] et le rôle"]
    end
    subgraph R3["3 · Identités"]
        direction TB
        WID["L'annuaire émet l'identité de charge<br/>de travail de l'agent (par exemple SPIFFE)"] --> RB["Rôle RBAC d'ap-agent-01<br/>inclut payment.create"]
        PRS["mcp-payment-server enregistré auprès de C6<br/>comme présentateur pour payment.create"]
    end
    subgraph R4["4 · Frontière d'exécution"]
        direction TB
        K7["C7 signe les ECC [S3]<br/>C6 connaît la clé publique de C7 + la révocation"]
        P4["API de paiement joignable depuis C6 seulement (P4)<br/>seul C6 détient le secret de l'API"]
        REG["C4 transmet à C6 la version courante<br/>du registre d'invariants (§4.10)"]
    end
    R1 ~~~ R2 ~~~ R3 ~~~ R4
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class PR,CI,AP2,MG,EN human;
    class SG,D2,D3,LOG,REG,DIR,USE,WID,RB,PRS,K7,P4 check;
```

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor GOV as Équipe de gouvernance<br/>(Git · pull requests)
    participant DIR as Annuaire de référence<br/>(IdP / IAM)
    actor APP as Approbateur<br/>(Resp. Finance / CFO)
    actor AG as Agent IA<br/>(ap-agent-01)
    participant SRV as Serveur MCP<br/>(Agent Surface)
    participant C1 as C1 Policy Authority
    participant C2 as C2 Execution Governor
    participant C3 as C3 Path Resolver
    participant C4 as C4 Invariant Monitor
    participant C7 as C7 Contract Compiler
    participant C6 as C6 Execution Firewall<br/>(passerelle de sortie + Refusal Gateway)
    participant API as API Paiement
    participant C5 as C5 Audit (append-only)

    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 1 · Règles : d'une pull request jusqu'à C2 et C3 (Part III §7.2, §7.3)
        Note right of GOV: l'auteur ouvre une pull request : invariants I-PAY-001, I-PAY-002, I-PAY-003 (policy as code)
        Note right of GOV: la CI valide contre les schémas et le registre d'invariants existant
        Note right of GOV: approbation par une autre personne (proposition et approbation sont deux personnes distinctes)
        GOV->>C1: fusion dans la branche principale
        C1->>C1: signe l'artefact de politique avec la clé de C1 [S1] (clé conservée dans un HSM, §4.3.3)
        C1->>C5: POLICY_ARTIFACT_ISSUED
        C1->>C2: distribue l'artefact signé
        C1->>C3: distribue l'artefact signé
        C2->>C2: vérifie [S1] · conserve le dernier jeu vérifié
        C3->>C3: vérifie [S1]
        C4->>C6: version courante du registre d'invariants (§4.10)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 2 · Approbateurs : enrôlés avant de pouvoir approuver
        APP->>DIR: enrôlement : clé de signature personnelle + MFA, liées à l'identité de la personne
        DIR->>DIR: rôle attribué par le processus IAM (Responsable Finance, CFO)
        Note over DIR,C1: Au moment de l'approbation (cas 02, 03), C1 vérifie la signature [S2] et le rôle dans cet annuaire
    end
    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 3 · Identités de l'agent et du serveur MCP
        DIR->>AG: identité de charge de travail pour ap-agent-01 (par exemple un SVID SPIFFE)
        DIR->>DIR: le rôle RBAC d'ap-agent-01 inclut payment.create, et rien d'autre qui déplace de l'argent
        Note over SRV,C6: mcp-payment-server est enregistré auprès de C6 comme présentateur pour payment.create (mécanisme propre à l'exemple)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over GOV,C5: 4 · Frontière d'exécution
        Note over C7,C6: C7 signe les ECC avec sa propre clé [S3]. C6 connaît la clé publique de C7 et consulte le statut de révocation (§4.3.3)
        Note over API,C5: API joignable uniquement depuis C6 (P4, réseau)<br/>Seul C6 en détient le secret
    end
```

[Index](README.md) · [Cas 01 — 350 €, automatique →](01-auto-350.md)
