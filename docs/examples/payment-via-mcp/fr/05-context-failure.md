# Cas 05 — échec d'ancrage

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [05-context-failure](../05-context-failure.md).

**Résultat:** Bénéficiaire ou facture inconnus · `CONTEXT_FAILURE` · refusé

La demande est admise, mais `C3` ne peut pas l'ancrer : le bénéficiaire n'est pas dans le référentiel fournisseurs, ou la facture n'est pas approuvée, déjà payée, ou d'un autre bénéficiaire. Un échec d'ancrage n'est jamais transmis à `C2` (§4.5.1, §4.10). `C3` enregistre `CONTEXT_FAILURE` et remet la demande à `C6`, dont la Refusal Gateway renvoie un refus structuré. Aucune décision n'est prise et aucun ECC n'existe.

## Vue d'ensemble

```mermaid
flowchart TD
    A(["Agent IA · payment.create"]) --> H{"Hook<br/>outil dans l'allowlist ?"}
    H -- non --> X1[["Bloqué localement<br/>(voir cas 04)"]]
    H -- oui --> S{"Serveur MCP · Agent Surface<br/>sujet authentifié, RBAC ?"}
    S -- non --> X2[["ADMISSION_REJECTED<br/>(voir cas 04)"]]
    S -- oui --> G{"C3 · ancrage<br/>bénéficiaire et facture connus ?"}
    G -- "non : bénéficiaire inconnu, facture non approuvée,<br/>déjà payée ou autre bénéficiaire" --> CF["C3 enregistre CONTEXT_FAILURE dans C5<br/>unresolved_refs"]
    CF --> C6["C3 remet la demande à C6<br/>jamais à C2 (§4.5.1, §4.10)"]
    C6 --> X[["Refus structuré via la Refusal Gateway<br/>ni décision · ni ECC · API jamais atteinte"]]

    classDef ok fill:#e3f4ec,stroke:#2a9d6f,color:#111;
    classDef ko fill:#fbe4e4,stroke:#d04848,color:#111;
    classDef check fill:#eef2fb,stroke:#5a78c8,color:#111;
    classDef human fill:#fdf1dc,stroke:#d08a1e,color:#111;
    classDef note fill:#fffbe6,stroke:#c9b458,color:#111,stroke-dasharray: 4 3;
    class X1,X2,CF,C6,X ko;
    class H,S,G check;
```

## Séquence

```mermaid
sequenceDiagram
    autonumber
    actor AG as Agent IA<br/>(ap-agent-01)
    participant HK as Hook préalable<br/>(défense en profondeur)
    participant SRV as Serveur MCP<br/>(Agent Surface)
    participant C3 as C3 Path Resolver
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
    rect rgba(220, 60, 60, 0.10)
        Note over AG,C5: L'ancrage échoue · bénéficiaire inconnu, ou facture non approuvée / déjà payée / bénéficiaire différent
        C3->>C3: ancrage dans le Federated Context Registry · référence non résolue
        C3->>C5: CONTEXT_FAILURE · unresolved_refs
        C3->>C6: gga.* avec semantic_result CONTEXT_FAILURE
        Note over C3,C6: Jamais transmis à C2 (§4.5.1, §4.10) : ni décision, ni ECC
        C6--xSRV: réponse à la demande gar.* · refus structuré (type, motif, référence C5) · Refusal Gateway
        SRV--xHK: DENY
        HK--xAG: DENY
    end

    Note over API: Jamais atteinte (P4).
```

[← Cas 04 — outil non enregistré](04-unregistered-tool.md) · [Index](README.md) · [Cas 06 — exception refusée →](06-exception-refused.md)
