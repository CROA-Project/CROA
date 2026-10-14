# Cas 02 — rm -rf /*

> **Non normatif.** Fait partie de l'exemple commenté [suppression gouvernée dans le shell avec Claude Code](README.md). Le contexte commun (conception, invariants, identité du sujet, limites, note de neutralité et références) est dans le [README](README.md).

English version: [02-rm-rf-root](../02-rm-rf-root.md).

**Résultat:** `rm -rf /*` · `CONTEXT_FAILURE` · refusé, rien n'est supprimé

Le glob `/*` s'étend à `/bin`, `/etc`, `/home`, … et à `/ws` lui-même. Cet exemple limite le registre de `C3` à `/ws` : `/bin` et `/etc` ne sont pas des entités enregistrées, et les supprimer est hors de la surface d'action par conception (Part II §4.5.2, Part III §9.3). Les références sont non résolvables, pas partiellement vérifiées : `C3` enregistre `CONTEXT_FAILURE` et remet la demande à `C6`, qui la refuse via la Refusal Gateway. La demande n'atteint jamais `C2`, donc aucun ECC ne peut exister. Ce n'est ni le jugement du hook ni un humain qui l'arrête. La zone grise montre pourquoi le bac à sable seul ne suffit pas : avec ses réglages par défaut, il protège `/bin` et `/etc`, mais laisse le répertoire de travail inscriptible, et la même commande effacerait le projet.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>rm -rf /*"]) --> H{"Hook PreToolUse (imposé)<br/>répond à temps ?"}
    H -- "non : onFailure block" --> X0[["Bloqué (voir cas 04)"]]
    H -- oui --> PA["Agent Surface · analyse déterministe<br/>fs.delete · recursive · motif /*"]
    PA --> S{"RBAC sur gar.type<br/>un rôle l'inclut-il ?"}
    S -- non --> X1[["ADMISSION_REJECTED<br/>UNAUTHORIZED_ACTION_CLASS"]]
    S -- oui --> G{"C3 · développe /* contre le registre<br/>toutes les cibles enregistrées ?"}
    G -- "non : /bin, /etc, … non résolvables" --> CF["CONTEXT_FAILURE dans C5<br/>remis à C6, jamais à C2"]
    CF --> X[["Refus structuré via la Refusal Gateway<br/>ni décision · ni ECC"]]
    X ~~~ W["Contre-exemple · bac à sable seul, par défaut :<br/>/bin et /etc protégés, mais le répertoire<br/>de travail est inscriptible : /ws est effacé"]
    W ~~~ Y["Ici /ws appartient à croa-exec :<br/>même ce chemin se termine en EPERM"]
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class H,PA,S,G check;
    class X0,X1,CF,X ko;
    class W warn;
    class Y ok;
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
    participant C6 as Exécuteur C6<br/>(utilisateur croa-exec · seul à écrire)
    participant FS as Projet /ws<br/>(propriété de croa-exec · lecture seule pour claude-agent)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prérequis en place, voir 00-prerequisites : /ws propriété de croa-exec · Claude Code tourne sous claude-agent · réglages imposés · règles signées [S1]

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
        AG->>CC: appel de l'outil Bash : rm -rf /*
        CC->>HK: PreToolUse (tool_name Bash · tool_input.command · session_id · cwd)
        HK->>SRV: appel d'outil (commande, cwd, session_id) par le socket Unix de la passerelle · la passerelle en construit le gar.*
        SRV->>SRV: sujet = utilisateur système claude-agent, d'après les identifiants du pair sur le socket · identifiant de session CROA émis par la passerelle, session_id de Claude Code conservé pour la corrélation
        SRV->>SRV: analyse déterministe, grammaire littérale uniquement → gar.type fs.delete · recursive true · motif /* transmis sans développement dans gar.context_refs
        SRV->>SRV: RBAC sur gar.type : le rôle de claude-agent inclut fs.delete · qualification
        SRV->>C3: gar.* (nouveau request_id · type fs.delete · cibles)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: L'ancrage échoue · le registre est limité à /ws
        C3->>C3: développe /* contre le registre : il couvre /bin, /etc, /home, … qui ne sont pas enregistrés · non résolvables, pas partiellement vérifiées, donc pas de confiance bornée
        C3->>C5: CONTEXT_FAILURE · unresolved_refs /bin, /etc, …
        C3->>C6: gga.* avec semantic_result CONTEXT_FAILURE
        Note over C3,C6: Jamais transmis à C2 : aucune décision, donc aucun ECC ne peut exister. I-FS-001 et I-FS-002 la refuseraient aussi : défense en profondeur
        C6--xSRV: réponse à la demande gar.* · refus structuré · référence C5 · Refusal Gateway
        SRV--xHK: DENY + motif
        HK--xCC: permissionDecision deny · permissionDecisionReason
        CC--xAG: erreur d'outil : refusé (Claude voit le motif)
    end
    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Contre-exemple · bac à sable de Claude Code seul, réglages par défaut, sans CROA
        Note over CC,FS: Le bac à sable bloquerait l'écriture dans /bin, /etc, … mais par défaut le répertoire de travail est inscriptible : le glob atteint /ws et l'efface
        Note over CC,FS: Ici /ws appartient à croa-exec : même ce chemin se termine en EPERM
    end
```

[← Cas 01 — rm d'un fichier du projet](01-rm-workspace-file.md) · [Index](README.md) · [Cas 03 — suppression déguisée →](03-obfuscated-delete.md)
