# Cas 05 — échec d'ancrage

> **Non normatif.** Fait partie de l'exemple commenté [paiement gouverné via MCP](README.md). Le contexte commun (invariants, réversibilité, déploiement, lien entre sujet et frontière, note de neutralité et références de la spec) est dans le [README](README.md).

English version: [05-context-failure](../05-context-failure.md).

**Résultat:** Bénéficiaire ou facture inconnus · `CONTEXT_FAILURE` · refusé

La demande est admise, mais `C3` ne peut pas l'ancrer : le bénéficiaire n'est pas dans le référentiel fournisseurs, ou la facture n'est pas approuvée, déjà payée, ou d'un autre bénéficiaire. Un échec d'ancrage n'est jamais transmis à `C2` (§4.5.1, §4.10). `C3` enregistre `CONTEXT_FAILURE` et remet la demande à `C6`, dont la Refusal Gateway renvoie un refus structuré. Aucune décision n'est prise et aucun ECC n'existe.

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

    AG->>HK: tool_call payment.create(amount, beneficiary_id, invoice_id)

    rect rgba(120, 120, 120, 0.06)
        Note over AG,C5: Admission
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
        C6--xSRV: refus structuré (type, motif, référence C5) · Refusal Gateway
        SRV--xAG: DENY
    end

    Note over API: Jamais atteinte (P4).
```

[← Cas 04 — outil non enregistré](04-unregistered-tool.md) · [Index](README.md) · [Cas 06 — exception refusée →](06-exception-refused.md)
