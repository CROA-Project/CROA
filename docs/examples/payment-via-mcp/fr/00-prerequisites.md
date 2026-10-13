# 00 — Prérequis

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [00-prerequisites](../00-prerequisites.md).

**Portée:** Ce qui doit être en place avant toute demande

Ce n'est pas un cas : c'est l'état sur lequel reposent tous les cas. Quatre choses sont en place avant la première demande. Les règles (`I-PAY-001` à `003`) passent par une pull request, une validation en CI et l'approbation d'une seconde personne, puis `C1` les signe [S1] et les distribue à `C2` et `C3`. Les approbateurs sont enrôlés dans l'annuaire de référence avec leur clé personnelle et leur rôle : c'est ce qui permet ensuite à `C1` de vérifier leur signature [S2]. L'agent reçoit son identité de charge de travail et son rôle RBAC, et le serveur MCP est enregistré comme présentateur. Enfin, la clé de `C7` [S3] est connue de `C6`, et seul `C6` peut atteindre l'API de paiement (P4). Les étapes de ce fichier ne font pas partie d'une demande ; dans les cas, la numérotation commence à l'appel de l'agent.

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
