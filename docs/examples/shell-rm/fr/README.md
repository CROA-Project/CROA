# Exemple commenté — suppression gouvernée dans le shell avec Claude Code

> **Non normatif.** Cet exemple illustre une façon d'appliquer l'architecture logique CROA à un outil shell brut. Il n'ajoute aucune exigence. En cas d'écart, la spécification prévaut. Les identifiants d'invariants, les chemins, les comptes système, la conception de l'exécuteur et le mécanisme entre le hook et l'exécuteur sont illustratifs.
>
> **Neutralité vis-à-vis des fournisseurs.** Claude Code sert ici de runtime d'exemple concret, parce que ses hooks, ses règles de permission et son bac à sable sont documentés publiquement. Le même modèle s'applique à tout runtime d'agent doté d'un hook avant exécution. Le citer n'implique aucune certification ni aucun soutien d'un fournisseur, et ses hooks et son bac à sable n'apportent à eux seuls aucune garantie CROA. La conformité n'exige jamais un produit particulier (voir [Vendor neutrality](../../../../README.md#vendor-neutrality)).

English version: [../README.md](../README.md).

## Pourquoi un shell est différent

Dans l'[exemple du paiement](../../payment-via-mcp/fr/README.md), un outil réalise une action : une allowlist d'outils a encore un sens. Un shell est un seul outil qui peut réaliser **n'importe quelle** action, de `ls` à `rm -rf /*`. Autoriser l'outil `Bash` ne dit rien de ce qu'il va faire. C'est la forme la plus forte de la règle *l'accès à un outil ne vaut pas autorité d'exécution* : la gouvernance doit porter sur l'action, pas sur l'outil.

Trois faits documentés de Claude Code orientent la conception :

1. **Les règles de permission Bash ne sont pas une frontière de sécurité.** La [documentation des permissions](https://code.claude.com/docs/en/permissions) indique qu'une règle Bash « matches the command text Claude writes » et « isn't a security boundary around the program » : une règle de refus comme `Bash(rm *)` n'arrête ni `/bin/rm -rf build/` ni `bash -c 'rm -rf build/'`.
2. **Un hook en échec laisse passer la commande par défaut.** Selon la [documentation des hooks](https://code.claude.com/docs/en/hooks), un hook `PreToolUse` qui plante ou dépasse son délai ne bloque pas l'appel, sauf si `onFailure` vaut `block` (Claude Code v2.1.295 ou plus récent) ; la valeur par défaut est `continue`.
3. **Le bac à sable laisse le répertoire de travail inscriptible par défaut.** La [documentation du bac à sable](https://code.claude.com/docs/en/sandboxing) indique que les commandes peuvent écrire dans le répertoire de travail, le répertoire temporaire de l'utilisateur et les répertoires ajoutés. Le bac à sable protège donc `/bin` et `/etc`, mais un `rm -rf /*` lancé dedans effacerait quand même le projet.

## Conception

- **La frontière, c'est la propriété des fichiers.** Le projet `/ws` appartient à un utilisateur système dédié, `croa-exec`. Claude Code tourne sous un autre utilisateur système, `claude-agent`, qui peut lire `/ws` mais pas y écrire. Tout ce que lance Claude Code tourne sous `claude-agent` : le shell dans le bac à sable, les outils `Edit` et `Write`, les serveurs MCP, les hooks et les commandes `!`. Aucun ne peut modifier `/ws`, quelle que soit sa configuration Claude Code, à condition que les préconditions système soient respectées : `claude-agent` n'a ni sudo ni binaire setuid pour élever ses droits, n'est ni dans le groupe `croa-exec` ni dans le groupe docker, `/ws` n'est pas inscriptible par le groupe ou par tous, et aucun service autre que `C6` tournant sous `croa-exec` ou root ne peut être piloté par lui.
- **`C6` est un exécuteur local** qui tourne sous `croa-exec`, le seul compte qui peut écrire dans `/ws`. Il n'exécute que des opérations issues d'un ECC valide et non rédimé, signé par `C7` [S3], après avoir vérifié l'époque et la révocation du signataire, la révocation de l'ECC et la version du registre d'invariants (§4.8, §4.3.3). C'est l'équivalent local de P4 dans l'exemple du paiement.
- **L'Agent Surface analyse la commande.** La passerelle est l'adaptateur qui construit le `gar.*` à partir de l'appel d'outil, comme le serveur MCP dans l'exemple du paiement ; le texte brut de la commande n'est jamais transmis comme contenu de la demande. Un analyseur déterministe accepte des commandes simples avec des arguments littéraux, et transmet les motifs de glob comme `/*` sans les développer, dans `gar.context_refs`, pour que `C3` les résolve contre le registre. Il transforme la commande en `gar.*` dont le type est la classe d'action (`fs.delete`) : le RBAC porte sur l'action, et `gar.type` reste identique jusqu'à l'ECC (§4.5.1, §4.9.1). Une commande que la grammaire ne peut pas réduire, comme une substitution de commande, un `eval` ou un contenu décodé, devient `shell.exec_dynamic` : un type déclaré dans l'artefact de `C1` (§4.5.1), qu'aucun rôle n'inclut. Un appel direct de `croa-exec` par l'agent n'est pas non plus une classe d'action et est rejeté à l'admission ; une référence d'ECC qui fuiterait reste à usage unique et liée à son sujet.
- **Le hook est un client de CROA, pas la garantie.** Le hook `PreToolUse` imposé transmet la commande brute à la passerelle. Sur `PERMIT`, il répond `allow` avec `updatedInput`, qui remplace la commande par `croa-exec --ecc <réf>` ; sur un refus, il répond `deny` avec le motif, que Claude voit.
- **Les réglages imposés de Claude Code sont une défense en profondeur** ([managed settings](https://code.claude.com/docs/en/managed-settings)) : bac à sable actif avec `failIfUnavailable: true` et `allowUnsandboxedCommands: false` ; `sandbox.filesystem.denyWrite` sur `/ws` ; règles de refus imposées pour `Edit` et `Write` sur `/ws` ; `allowManagedHooksOnly`, avec un hook sur `Bash`, `PowerShell` et `Monitor`, réglé sur `onFailure: "block"`.
- **Le canal vers `C6`.** `croa-exec` joint `C6` par un socket Unix appartenant à `croa-exec`. Sur macOS, le réglage imposé `sandbox.network.allowUnixSockets` liste ce seul socket. Sur Linux, où ce réglage ne s'applique pas, une entrée imposée `sandbox.excludedCommands` exécute hors du bac à sable le binaire `croa-exec`, propriété de root. Les deux options n'élargissent le bac à sable que pour un seul chemin, et aucune ne donne le droit d'écrire dans `/ws`, puisque l'appelant reste `claude-agent`. Sur Linux, la documentation du bac à sable précise que le blocage des sockets Unix dépend d'un filtre seccomp optionnel.

## Identité du sujet

La passerelle et `C6` écoutent sur des sockets Unix et lisent l'utilisateur système de l'appelant auprès du noyau (identifiants du pair). Le sujet est donc l'utilisateur système `claude-agent`, et non une valeur fournie par l'appelant. Il désigne le déploiement de l'agent, pas une personne : tout ce qui tourne sous `claude-agent`, y compris les commandes `!` du développeur dans Claude Code, le partage. La passerelle émet son propre identifiant de session au premier contact (§4.6.1) ; le `session_id` de Claude Code n'est conservé que pour la corrélation, donc ouvrir une nouvelle session Claude Code ne remet rien à zéro. Une limite cumulée, si on en ajoutait une, serait indexée par sujet (TP-X, §4.6.3), comme dans l'exemple du paiement. `C6` n'exécute un ECC que si le processus qui le présente tourne sous `ecc.subject`. Tout processus qui tourne sous `claude-agent` peut toujours demander une action, mais seulement via CROA, et seulement dans les limites du rôle et des invariants.

## Invariants et rôle enregistrés (illustratifs)

| Règle | Classe | Énoncé |
|---|---|---|
| Rôle de `claude-agent` | — | Inclut `fs.delete`. `shell.exec_dynamic` est un type d'action déclaré, inclus dans aucun rôle. |
| `I-FS-001` | E2 | Les cibles de `fs.delete` DOIVENT appartenir à l'ensemble des chemins enregistrés sous `/ws`. |
| `I-FS-002` | E1 | `fs.delete` NE DOIT PAS être récursif sur `/ws` lui-même ni sur un chemin protégé (`.git`, `.claude`). |

Le registre de `C3` est limité à `/ws`. Une cible hors de ce périmètre est non résolvable : la demande se termine en `CONTEXT_FAILURE` avant `C2`, et `I-FS-001` et `I-FS-002` forment une seconde ligne de défense.

**Réversibilité.** Une suppression dans `/ws` est précédée d'un snapshot pris par `C6` : elle est compensable (**R1**), et le snapshot est le `compensating_controls` de l'ECC. Une suppression hors de `/ws` serait R4 au sens de la Tenet T5 (refus par défaut). Cet exemple va plus loin et la tient complètement hors de la surface d'action, en limitant le registre.

## Les cas

| Cas | Résultat |
|---|---|
| [00 — Prérequis](00-prerequisites.md) | Ce qui doit être en place avant toute commande |
| [Cas 01 — rm d'un fichier du projet](01-rm-workspace-file.md) | `rm build/tmp.log` · `PERMIT` (R1) · exécuté par C6 |
| [Cas 02 — rm -rf /*](02-rm-rf-root.md) | `rm -rf /*` · `CONTEXT_FAILURE` · refusé, rien n'est supprimé |
| [Cas 03 — suppression déguisée](03-obfuscated-delete.md) | `bash -c "$(… \| base64 -d)"` · `ADMISSION_REJECTED` |
| [Cas 04 — tentatives de contournement](04-raw-shell-bypass.md) | Hook remplacé, en échec ou évité · rien n'est supprimé |

## Lire les schémas

Chaque fichier montre deux vues du même cas. La **vue d'ensemble** (flowchart) se lit de haut en bas : chaque contrôle est un losange, chaque refus sort vers une case rouge. Le schéma de **séquence**, en dessous, donne chaque échange dans l'ordre, y compris chaque écriture dans `C5`.

Dans les schémas de séquence :

- Les flèches pleines (`->>`) sont synchrones. Une écriture dans `C5` qui doit être validée avant l'étape suivante apparaît avec son accusé de réception.
- Les flèches en pointillé terminées par une croix (`--x`) sont des refus ou des blocages.
- Les zones grises sont les étapes communes ou les contre-exemples ; vert : permis ou admis ; rouge : refusé ou bloqué ; bleu : présentation à la frontière d'exécution.
- Chaque cas s'ouvre sur un rappel d'une ligne des prérequis, détaillés dans [00 — Prérequis](00-prerequisites.md). Dans un cas, la numérotation commence à l'appel de l'agent.

## Les signatures en jeu

Seules deux des trois signatures de l'exemple du paiement apparaissent ici, puisqu'aucun humain n'approuve d'exception :

- **[S1]** la clé de `C1` sur les artefacts de politique (rôle, `I-FS-001`, `I-FS-002`), vérifiée par `C2` et `C3`.
- **[S3]** la clé de `C7` sur l'ECC, vérifiée par `C6` avant de toucher à `/ws`.

`permissionDecision` et `updatedInput` sont des sorties du hook, pas des signatures d'autorisation : l'autorité de supprimer, c'est l'ECC, vérifié et rédimé par `C6`.

## Limites

- **Toute écriture passe par `C6`.** Comme `claude-agent` ne peut pas écrire dans `/ws`, modifier du code demande aussi un chemin gouverné (`fs.write` via `C6`), pas seulement supprimer. Un déploiement réel gouvernerait toutes les écritures de cette façon, ou limiterait la zone gouvernée à un sous-répertoire.
- **Les réglages du développeur peuvent élargir le bac à sable.** Plusieurs réglages du bac à sable, comme `excludedCommands` et `filesystem.allowWrite`, n'ont pas de verrou réservé aux réglages imposés, et les réglages en liste se cumulent. Cela ne casse pas cette conception, puisque c'est la propriété des fichiers, et non le bac à sable, qui fait frontière. C'est pour cela que le bac à sable n'est présenté que comme une défense en profondeur.
- **Hors du bac à sable.** Les outils fichiers de Claude Code, les serveurs MCP, les hooks, les commandes `!`, et les processus lancés par des mods, des serveurs LSP ou des moniteurs de plugins tournent hors du bac à sable. Ici, ils tournent quand même sous `claude-agent` : ils ne peuvent pas non plus écrire dans `/ws`.
- **Les lectures ne sont pas gouvernées.** L'agent lit `/ws` directement ; seules les modifications passent par CROA.
- **Événements de l'OS et du bac à sable.** Ni l'OS ni le bac à sable ne sont des composants CROA. Remonter leurs refus dans `C5` est un choix de l'exemple, pas une garantie du runtime.
- **Confiance dans l'analyseur.** L'analyseur de shell de l'Agent Surface fait partie de la base de confiance : un analyseur qui lit mal une commande pourrait ancrer une mauvaise cible. Garder une grammaire acceptée réduite (commandes simples, arguments littéraux) est ce qui la rend déterministe.
- **`updatedInput`.** La documentation des hooks indique que `updatedInput` « replaces a tool's arguments before it runs ». Cet exemple ne s'appuie que sur cela. Les règles de refus et de demande s'appliquent toujours à l'appel, quelle que soit la décision du hook.

## Références de la spécification

- Classes d'évaluabilité et réduction de la surface d'action : Part I §2.6 ; Part III §9.3
- Sessions et profils de trajectoire : Part II §4.6.1, §4.6.3
- Classes de réversibilité : Part I Chapter 3, Tenet T5
- Époques de signataire et révocation : Part II §4.3.3
- `C2.eval` : Part II §4.4.2 ; champs de l'ECC (`reversibility_class`, `compensating_controls`) : Part II §4.4.1 et `spec/schemas/ecc.schema.json`
- `gga.type` identique à `gar.type`, `CONTEXT_FAILURE` transmis à `C6` : Part II §4.5.1, §4.10 ; périmètre du registre : Part II §4.5.2
- Événements C5 (`ADMISSION_REJECTED`, `CONTEXT_FAILURE`, `EXECUTION_*`) : Part II §4.7.1 et `spec/schemas/event.schema.json`
- `C6` seul à écrire, rachat atomique, Refusal Gateway : Part II §4.8
- Agent Surface, RBAC sur `gar.type` : Part II §4.9, §4.9.1
- Policy as code et séparation des rôles : Part III §7.2, §7.3
- Exécution par canal détourné (TH-9) : Part V Chapter 26
