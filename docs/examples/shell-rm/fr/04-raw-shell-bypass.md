# Cas 04 — tentatives de contournement

> **Non normatif.** Fait partie de l'exemple commenté [suppression gouvernée dans le shell avec Claude Code](README.md). Le contexte commun (conception, invariants, identité du sujet, limites, note de neutralité et références) est dans le [README](README.md).

English version: [04-raw-shell-bypass](../04-raw-shell-bypass.md).

**Résultat:** Hook remplacé, en échec ou évité · rien n'est supprimé

Ce qui se passe quand une commande tente d'éviter le chemin gouverné. Un projet ne peut pas remplacer le hook imposé (`allowManagedHooksOnly`). Un hook qui plante ou tarde bloque au lieu de laisser passer, car `onFailure` vaut `block` ; la valeur par défaut, `continue`, laisserait passer. Si une erreur de configuration laisse quand même la commande arriver au shell, elle tourne sous `claude-agent`, qui n'est pas propriétaire de `/ws` : l'écriture échoue avec `EPERM`. Un nouvel essai avec `dangerouslyDisableSandbox` ne permet pas de s'échapper : avec `allowUnsandboxedCommands: false`, Claude Code ignore le paramètre et relance la commande dans le bac à sable. C'est la propriété des fichiers qui tient ; le bac à sable et les réglages imposés sont une défense en profondeur.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["Claude Code · Bash<br/>rm -rf src/"]) --> L1{"A · un hook du projet<br/>remplace le hook imposé ?"}
    L1 -- "ignoré : allowManagedHooksOnly" --> L2{"B · le hook imposé<br/>plante ou dépasse son délai ?"}
    L2 -- oui --> X2[["Bloqué : onFailure block<br/>(continue, par défaut, laisserait passer)"]]
    L2 -. "C · une erreur de configuration<br/>laisse la commande arriver au shell" .-> L3{"claude-agent écrit dans /ws ?"}
    L3 -- "non : propriété de croa-exec" --> X3[["EPERM · rien n'est supprimé"]]
    X3 -. "D · nouvel essai avec<br/>dangerouslyDisableSandbox" .-> D1["Paramètre ignoré :<br/>allowUnsandboxedCommands false"]
    D1 --> X4[["Nouvelle exécution dans le bac à sable · EPERM"]]
    X4 ~~~ N(["Seul croa-exec peut écrire dans /ws, et C6 ne le fait qu'à partir d'un ECC.<br/>La propriété des fichiers est la frontière ; bac à sable et réglages sont une défense en profondeur."])
    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef warn fill:#f1f1f1,stroke:#888,color:#111,stroke-dasharray: 4 3;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class L1,L2,L3,D1 check;
    class X2,X3,X4 ko;
    class N note;
```

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Agent Claude Code<br/>(utilisateur système claude-agent)
    participant CC as Outil Bash<br/>(bac à sable OS)
    participant HK as Hook PreToolUse<br/>(imposé · onFailure block)
    participant FS as Projet /ws<br/>(propriété de croa-exec · lecture seule pour claude-agent)
    participant C5 as C5 Audit (append-only)

    Note over AG,C5: Prérequis en place, voir 00-prerequisites : /ws propriété de croa-exec · Claude Code tourne sous claude-agent · réglages imposés · règles signées [S1]

    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: A · Le projet tente de remplacer le hook
        AG->>CC: appel de l'outil Bash : rm -rf src/
        CC->>CC: un fichier .claude/settings.json du projet déclare son propre hook permissif · ignoré : allowManagedHooksOnly
        CC->>HK: PreToolUse vers le seul hook imposé
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: B · Le hook imposé plante ou dépasse son délai
        HK--xCC: plantage ou délai dépassé
        CC--xAG: bloqué, car onFailure vaut block (la valeur par défaut, continue, laisserait passer)
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: C · La commande arrive quand même au shell (par exemple une erreur de configuration)
        AG->>CC: appel de l'outil Bash : rm -rf src/
        CC->>FS: unlink /ws/src/... sous claude-agent, depuis le bac à sable
        FS--xCC: EPERM · /ws appartient à croa-exec (et denyWrite dans le bac à sable)
        CC--xAG: échec de la commande · rien n'est supprimé
        Note over CC,C5: Le bac à sable et l'OS ne sont pas des composants CROA : remonter leurs refus dans C5 est un choix de l'exemple
    end
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: D · Nouvel essai hors du bac à sable
        AG->>CC: nouvel essai avec dangerouslyDisableSandbox
        CC->>CC: paramètre ignoré, car allowUnsandboxedCommands vaut false : nouvelle exécution dans le bac à sable
        CC->>FS: unlink /ws/src/... sous claude-agent
        FS--xCC: EPERM
        CC--xAG: échec de la commande · rien n'est supprimé
    end
    
    Note over FS,C5: Seul croa-exec peut écrire dans /ws, et C6 ne le fait qu'à partir d'un ECC. Tout chemin qui évite CROA se termine sans modification de /ws, sous les préconditions système du 00.
```

[← Cas 03 — suppression déguisée](03-obfuscated-delete.md) · [Index](README.md)
