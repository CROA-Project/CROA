# Exemple commenté — paiement gouverné via MCP

> **Non normatif.** Cet exemple illustre une façon de réaliser l'architecture logique CROA pour un outil de paiement exposé via MCP. Il n'ajoute aucune exigence. En cas d'écart, la spécification prévaut. Les identifiants d'invariants, les seuils, les rôles, la répartition du déploiement et le mécanisme d'identité ci-dessous sont illustratifs.
>
> **Neutralité vis-à-vis des fournisseurs.** L'exemple est indépendant de toute technologie. Il est compatible avec une implémentation qui s'appuie sur les mécanismes de permissions et de hooks propres à un runtime d'agent (par exemple les hooks et permissions de Claude Code). Cette compatibilité ne constitue une certification d'aucun fournisseur, et les hooks eux-mêmes n'apportent aucune garantie CROA. La conformité n'exige jamais un produit particulier (voir [Vendor neutrality](../../../../README.md#vendor-neutrality)).

English version: [../README.md](../README.md).

## Scénario

Un agent comptable fournisseurs (`ap-agent-01`) peut appeler l'outil MCP `payment.create(amount, beneficiary_id, invoice_id)`. L'API de paiement est un système gouverné situé derrière la frontière d'exécution.

Le déploiement est **hybride** (Part IV §18.3). Le serveur MCP héberge l'Agent Surface, comme le suggère Part IV §23.5.2. `C6` tourne sur une passerelle de sortie distincte, placée devant l'API de paiement : c'est le modèle DM-4 (Part IV Chapter 22). Dans un déploiement DM-5 pur, `C6` serait au contraire embarqué dans le serveur MCP, et c'est alors le serveur MCP qui détiendrait le secret de l'API.

Le **hook préalable** du runtime de l'agent n'est qu'une **défense en profondeur**. Il arrête tôt les outils non enregistrés, mais la garantie ne vient pas de lui. La garantie, c'est `C6` associé à P4 : l'API de paiement n'accepte que le trafic venant de `C6`, et `C6` n'admet que les opérations issues d'un ECC valide et non encore rédimé.

## Invariants enregistrés (illustratifs)

| Invariant | Classe | Énoncé | Levable par une autorisation `C1` ? |
|---|---|---|---|
| `I-PAY-001` | E1 | `payment.create` NE DOIT PAS dépasser 1 000 € par paiement sans artefact d'autorisation `C1` couvrant le bénéficiaire, la facture et le montant. | Oui, émise sur approbation d'un Responsable Finance (ou supérieur) |
| `I-PAY-002` | E1 | `payment.create` NE DOIT PAS dépasser 5 000 € par paiement sans artefact d'autorisation `C1` couvrant le bénéficiaire, la facture et le montant. | Oui, émise sur approbation du CFO |
| `I-PAY-003` | E2, TP-X | Le cumul des `payment.create` par (sujet, `beneficiary_id`) sur une fenêtre glissante de 24 h NE DOIT PAS dépasser 10 000 €. | Non : un dépassement cumulé est refusé à l'étape 4 de `C2.eval`, qui ne prévoit aucune autorisation (Part II §4.4.2) |

`I-PAY-003` est déclaré TP-X parce qu'une fenêtre de 24 h couvre plusieurs sessions, et que les agrégats TP-X sont indexés par sujet (Part II §4.6.3). `C4` ajoute chaque montant permis à l'agrégat, de façon sérialisée par clé. Dans cet exemple, le montant est retiré de l'agrégat si l'ECC ne peut plus être rédimé (expiré, invariants modifiés, ou autorisation déjà consommée par un autre ECC) ou si l'exécution échoue. Un blocage qui laisse l'ECC authentique utilisable, comme une copie altérée ou une opération modifiée, ne retire rien.

**Réversibilité.** Un virement est traité comme **R2** (irréversible, faible impact) sur tous les chemins. Chaque ECC porte donc `ecc.reversibility_class = R2` et `ecc.compensating_controls`. Dans cet exemple, le contrôle R2 est l'approbation humaine préalable de la facture dans l'ERP. `C3` la vérifie à l'ancrage : la facture est approuvée et non payée, son bénéficiaire correspond, et le montant ne dépasse pas le solde restant. Une Governed Exception n'est **pas** inscrite dans `compensating_controls` : elle est liée par `ecc.auth_ref` et `ecc.exception_scope`.

## Les cas

Un fichier par cas, chacun avec son propre schéma de séquence :

| Cas | Résultat |
|---|---|
| [Cas 01 — 350 €, automatique](01-auto-350.md) | 350 € · `PERMIT` · exécuté |
| [Cas 02 — 3 500 €, exception Responsable Finance](02-exception-finance-3500.md) | 3 500 € · `DENY`, puis `PERMIT_WITH_AUTHORIZATION` · exécuté |
| [Cas 03 — 7 500 €, exception CFO](03-exception-cfo-7500.md) | 7 500 € · `DENY`, puis `PERMIT_WITH_AUTHORIZATION` · exécuté |
| [Cas 04 — outil non enregistré](04-unregistered-tool.md) | Outil non enregistré · bloqué à trois niveaux |
| [Cas 05 — échec d'ancrage](05-context-failure.md) | Bénéficiaire ou facture inconnus · `CONTEXT_FAILURE` · refusé |
| [Cas 06 — exception refusée](06-exception-refused.md) | 3 500 € · `DENY` · approbation refusée ou expirée · rien n'est exécuté |
| [Cas 07 — bloqué à la frontière d'exécution](07-boundary-blocked.md) | ECC rejoué, consommé, altéré, expiré, périmé ou dépassé · `EXECUTION_BLOCKED` |

## Lire les schémas

- Les flèches pleines (`->>`) sont synchrones. Une écriture dans `C5` qui doit être validée avant l'étape suivante apparaît avec son accusé de réception.
- Les flèches en pointillé terminées par une croix (`--x`) sont des refus ou des blocages.
- Les zones grises sont les étapes communes (admission, ancrage, évaluation) ; vert : permis ou admis ; orange : refusé en attente d'exception ; rouge : refusé ou bloqué ; bleu : présentation à la frontière d'exécution.
- Chaque cas reprend volontairement les étapes communes, pour que chaque fichier se lise seul.

## Lien entre le sujet et la frontière

C'est le serveur MCP qui présente l'opération à `C6`, mais le sujet de l'ECC est l'agent. Dans cet exemple, le lien se fait ainsi :

1. L'agent s'authentifie auprès de l'Agent Surface avec une identité de charge de travail (par exemple un SVID SPIFFE). Cette identité devient `ecc.subject`.
2. Pour présenter l'opération, le serveur MCP fait un échange de jeton OAuth 2.0 (RFC 8693). Il obtient un jeton de courte durée avec `sub = ap-agent-01`, `act = mcp-payment-server` et l'audience `C6`, lié à l'`ecc.id`.
3. `C6` vérifie que `sub` est égal à `ecc.subject` et que `act` est un présentateur enregistré pour cet outil. Un ECC présenté sous un autre sujet est bloqué.

Ces vérifications sont le mécanisme propre à cet exemple, pas une exigence MUST du §4.8. Elles mettent en œuvre la clause d'I8 qui interdit le rachat d'un ECC par un autre sujet (Part II §5.9, qui renvoie à Part IV §21.3). Ni l'agent ni le serveur MCP ne détiennent de secret pour l'API de paiement : `C6` l'appelle avec sa propre identité de service. Sur l'identité et la délégation, voir Appendix O §O.5.

## Références de la spécification

- Policy Authority `C1` ; ce que produit l'agent n'est jamais une entrée de `C1` : Part II §4.3
- Artefacts d'autorisation, liaison `auth_ref` / `exception_scope`, rachat à usage unique : Part II §4.3.1
- Époque du signataire et statut de révocation : Part II §4.3.3
- Étapes de `C2.eval` et résultats `PERMIT` / `PERMIT_WITH_AUTHORIZATION` : Part II §4.4.2
- Compilation de l'ECC : Part II §4.4.3, §4.8 et `spec/schemas/ecc.schema.json`
- `CONTEXT_FAILURE` transmis à `C6`, jamais à `C2` : Part II §4.5.1, §4.10
- Historique de session de `C4` et vérification après exécution : Part II §4.6
- Profils de trajectoire (TP-C, TP-X) et agrégats sérialisés : Part II §4.6.3
- Champs des événements de gouvernance : Part II §4.7.1 et `spec/schemas/event.schema.json`
- Rachat atomique, `AUTHORIZATION_ALREADY_REDEEMED`, Refusal Gateway : Part II §4.8
- Agent Surface, RBAC et qualification : Part II §4.9, §4.9.1
- Flux autorisés entre composants : Part II §4.10
- Pas de rachat par un autre sujet (I8) : Part II §5.9
- Classes de réversibilité : Part I Chapter 3, Tenet T5 ; Part II §4.4.1 (`ecc.reversibility_class`, `ecc.compensating_controls`)
- Configurations hybrides : Part IV §18.3 ; passerelle DM-4 : Part IV Chapter 22 ; MCP comme hôte de l'Agent Surface : Part IV §23.5.2
- Demandes d'exception via ITSM / ChatOps : Part IV §24.4
- Identité de l'agent et délégation : Appendix O §O.5
- Modèle d'invariant commenté (`I-EC-001`) : Appendix P §P.3.4
- Test de l'exception à usage unique : Appendix Q, NT-007
