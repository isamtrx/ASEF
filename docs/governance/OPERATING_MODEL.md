# OPERATING_MODEL.md — ASEF

> Source de vérité du cycle de vie opérationnel complet d'une demande.  
> 1 responsabilité : décrire comment une demande entre, est traitée et sort du système.  
> Dépend de : GOVERNANCE.md, QUALITY_GATES.md, AGENTS.md  
> Ne doit jamais contenir : règles de code, stratégie produit.

---

## Cycle de vie complet d'une demande

```
Demande entrante
      │
      ▼
[Gate 0 — Intake]
  Formulation DoD · Vérification scope
      │
      ├─ HORS SCOPE → Refus ou évolution scope (ADR)
      │
      ▼
[Gate 1 — Scope validé]
  Plan d'implémentation · Identification dépendances
      │
      ▼
[Gate 2 — Architecture validée]
  Revue architecture · ADR si structurant
      │
      ▼
[Implémentation]
  Agent developer · Tests unitaires · Revues itératives
      │
      ▼
[Gate 3 — Code conforme]
  Lint · Type-check · Standards
      │
      ▼
[Gate 4 — Tests passés]
  Tests unitaires + intégration + E2E · Coverage
      │
      ▼
[Gate 5 — Sécurité validée]
  SAST · Dependency audit · Secret scan
      │
      ▼
[Gate 6 — Documentation]
  CHANGELOG · SESSION_LOG · ADR si applicable
      │
      ▼
[Gate 7 — Release] (si release)
  Validation humaine · Evidence package · Tag Git
      │
      ▼
Production / Livraison
```

---

## Acteurs par étape

| Étape | Acteur principal | Acteurs secondaires |
|-------|-----------------|---------------------|
| Intake | Humain (PO/TL) | Agent intake |
| Scope | Humain (TL) | Agent architect |
| Architecture | Agent architect | Tech Lead (validation si structurant) |
| Implémentation | Agent developer | Agent QA (tests) |
| Gate 3-4 | CI automatique | Agent QA |
| Gate 5 | CI automatique + Agent security | Tech Lead (si auth/authz) |
| Gate 6 | Agent docs | Humain (vérification) |
| Gate 7 | Humain (CTO/TL) | — |
| Post-production | Agent observability | Tech Lead |

---

## Artefacts produits par étape

| Étape | Artefacts |
|-------|----------|
| Intake | DoD écrit |
| Scope | Plan d'implémentation, mise à jour SCOPE.md si applicable |
| Architecture | ADR si applicable, mise à jour ARCHITECTURE.md |
| Implémentation | Code, tests, composants |
| Gate 3-4 | Rapports tests, rapport coverage |
| Gate 5 | Rapport SAST, rapport audit, rapport secret scan |
| Gate 6 | CHANGELOG.md mis à jour, SESSION_LOG.md mis à jour |
| Gate 7 | Evidence package, tag Git, CHANGELOG section versionnée |

---

## Interactions humain-agent

### Ce que l'humain fait toujours
- Valider le DoD avant implémentation
- Approuver les décisions structurantes (ADR)
- Signer les exceptions (EXCEPTIONS.md)
- Valider Gate 7 avant release production

### Ce que l'agent fait seul
- Exécuter les contrôles CI
- Écrire le code et les tests
- Mettre à jour la documentation courante
- Remonter les blocages et risques

### Ce qui requiert dialogue humain-agent
- Ambiguïté sur le scope → humain clarifie
- Gate bloquant → agent documente, humain décide (exception ou blocage)
- Risque sécurité détecté → agent remonte, humain valide

---

## SLA opérationnels

| Étape | SLA cible |
|-------|----------|
| Réponse à un intake | < 24h |
| Validation Gate 7 | < 4h (planifiée), < 1h (urgente) |
| Réponse à un incident P1 | < 30min |
| Réponse à un incident P2 | < 2h |

---

## Règle de non-contournement

Aucune étape ne peut être sautée. Si une étape ne peut pas être complétée, ouvrir une exception dans `docs/quality/EXCEPTIONS.md` avec validation humaine.  
Un agent qui saute une étape sans exception documentée = violation critique tracée dans `SESSION_LOG.md`.
