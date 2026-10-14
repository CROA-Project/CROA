# Cas 01 — rm d'un fichier du projet

> **Non normatif.** Fait partie de l'exemple commenté [suppression gouvernée dans le shell avec Claude Code](README.md). Le contexte commun (conception, invariants, identité du sujet, limites, note de neutralité et références) est dans le [README](README.md).

English version: [01-rm-workspace-file](../01-rm-workspace-file.md).

**Résultat:** `rm build/tmp.log` · `PERMIT` (R1) · exécuté par C6

Le cas de base. L'Agent Surface analyse la commande brute avec une grammaire déterministe, limitée aux arguments littéraux, et la transforme en `gar.*` de type `fs.delete` : le RBAC porte donc sur l'action, pas sur l'outil `Bash`. `C3` ancre la cible dans le registre de `/ws` et `C2` la permet. Un snapshot est pris avant la suppression : la transition est compensable (R1), et le snapshot est le contrôle compensatoire de l'ECC. Sur `PERMIT`, le hook ne laisse pas le shell exécuter `rm`. Il répond `allow` avec `updatedInput`, qui remplace la commande par `croa-exec`. `croa-exec` présente l'ECC à `C6`, qui le vérifie, le rédime et supprime le fichier sous `croa-exec`.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>rm build/tmp.log"]) --> H{"Hook PreToolUse (imposé)<br/>répond à temps ?"}
    H -- "non : onFailure block" --> X0[["Bloqué (voir cas 04)"]]
    H -- oui --> PA["Agent Surface · analyse déterministe<br/>fs.delete · build/tmp.log"]
    PA --> S{"RBAC sur gar.type<br/>un rôle l'inclut-il ?"}
    S -- non --> X1[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS"]]
    S -- oui --> G{"C3 · cible dans le registre /ws,<br/>non protégée ?"}
    G -- non --> X2[["CONTEXT_FAILURE<br/>(voir cas 02)"]]
    G -- oui --> D{"C2.eval<br/>I-FS-001 · I-FS-002"}
    D -- "un fichier dans /ws, non récursif" --> PM["PERMIT · R1"]
    PM --> E["C7 · ECC signé [S3]<br/>compensation : snapshot"]
    E --> U["Hook : allow + updatedInput<br/>croa-exec --ecc réf"]
    U --> F{"C6 · ECC valide, non révoqué,<br/>appelant = ecc.subject, non rédimé ?"}
    F -- non --> X4[["EXECUTION_BLOCKED"]]
    F -- oui --> C["Un seul CAS · EXECUTION_AUTHORIZED<br/>snapshot, puis unlink par C6"]
    C --> OK(["EXECUTION_COMPLETED<br/>fichier supprimé, restaurable"])
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class H,PA,S,G,D,F check;
    class X0,X1,X2,X4 ko;
    class PM,E,U,C,OK ok;
```

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Agent Claude Code<br/>(utilisateur système claude-agent)
    participant CC as Outil Bash<br/>(bac à sable OS)
    participant HK as Hook PreToolUse<br/>(imposé · onFailure block)
    participant SRV as Passerelle CROA<br/>(Agent Surface + analyseur shell)
    participant C3 as C3 Path Resolver
    participant C2 as C2 Execution Governor
    participant C4 as C4 Invariant Monitor
    participant C7 as C7 Contract Compiler
    participant C6 as Exécuteur C6<br/>(utilisateur croa-exec · seul à écrire)
    participant FS as Projet /ws<br/>(propriété de croa-exec · lecture seule pour claude-agent)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prérequis en place, voir 00-prerequisites : /ws propriété de croa-exec · Claude Code tourne sous claude-agent · réglages imposés · règles signées [S1]

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        AG->>CC: appel de l'outil Bash : rm build/tmp.log
        CC->>HK: PreToolUse (tool_name Bash · tool_input.command · session_id · cwd)
        HK->>SRV: appel d'outil (commande, cwd, session_id) par le socket Unix de la passerelle · la passerelle en construit le gar.*
        SRV->>SRV: sujet = utilisateur système claude-agent, d'après les identifiants du pair sur le socket · identifiant de session CROA émis par la passerelle, session_id de Claude Code conservé pour la corrélation
        SRV->>SRV: analyse déterministe, grammaire littérale uniquement → gar.type fs.delete · cible build/tmp.log · recursive false
        SRV->>SRV: RBAC sur gar.type : le rôle de claude-agent inclut fs.delete · qualification
        SRV->>C3: gar.* (nouveau request_id · type fs.delete · cibles)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Ancrage
        C3->>C3: registre : /ws/build/tmp.log existe, dans /ws, chemin non protégé
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Évaluation
        C3->>C2: gga.* fs.delete · semantic_result GROUNDED
        C2->>C4: action en cours d'évaluation
        C4-->>C2: état des invariants (suppressions par ce sujet)
        C2->>C2: C2.eval · I-FS-001 cible dans l'ensemble /ws · I-FS-002 non récursif
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: PERMIT · R1 (compensable par snapshot)
        C2->>C5: PERMIT · decision_basis PERMIT
        C2->>C7: PERMIT
        C7->>C7: compile l'ECC et le signe [S3] · fs.delete /ws/build/tmp.log · reversibility_class R1 · compensating_controls : restauration depuis le snapshot
    end
    rect rgba(60, 120, 220, 0.10)
        Note over AG,C5: Exécution · le hook substitue le client gouverné
        C7->>C5: ECC_COMPILED · ecc_id
        C7->>SRV: référence de l'ECC + notification de décision
        SRV-->>HK: PERMIT + référence de l'ECC
        HK-->>CC: permissionDecision allow · updatedInput : croa-exec --ecc réf
        CC->>C6: croa-exec présente la référence de l'ECC par le socket Unix de C6
        C6->>C6: [S3] valide · époque du signataire non révoquée · ECC ni expiré ni révoqué · invariant_set_version cohérent · opération identique à l'ECC · utilisateur système de l'appelant égal à ecc.subject
    end
    rect rgba(40, 170, 120, 0.12)
        Note over AG,C5: Admis
        C6->>C6: un seul CAS linéarisable · rédime ecc.id
        C6->>C5: EXECUTION_AUTHORIZED · ecc_id
        C5-->>C6: validé
        C6->>FS: snapshot de /ws/build/tmp.log (point de compensation)
        C6->>FS: unlink /ws/build/tmp.log
        FS-->>C6: fait
        C6->>C5: EXECUTION_COMPLETED · ecc_id · exit_status
        Note over C6,C5: Si le snapshot échoue, C6 ne supprime rien : EXECUTION_FAILED, et l'ECC reste consommé
        C6-->>CC: résultat + identifiant du snapshot
        CC-->>AG: résultat de l'outil : fichier supprimé (restaurable)
    end
```

[← 00 — Prérequis](00-prerequisites.md) · [Index](README.md) · [Cas 02 — rm -rf /* →](02-rm-rf-root.md)
