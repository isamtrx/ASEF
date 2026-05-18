# ASEF-QA — Framework Qualité Logicielle

**Problème résolu** : La QA sans gouvernance produit des résultats non vérifiables et des preuves non traçables.
**Domaine** : `software`
**Version** : 0.1.0
**Héritage** : `core/ASEF-Core.md`, `core/ASEF-Gates.md`, `core/ASEF-Evidence.md`

---

## Démarrage rapide

1. Lire `PURPOSE.md` pour comprendre le périmètre.
2. Identifier les agents QA requis pour votre contexte.
3. Spécialiser les gates G3 (code) et G4 (tests) avec vos critères.
4. Exécuter le playbook `playbooks/produce-evidence-package.md` après chaque cycle.

---

## Agents QA définis

| Agent | Responsabilité | Permissions |
|---|---|---|
| **QA-Lead** | Orchestrer la stratégie de test, valider les gates G4-G5 | READ all, WRITE rapports QA, EXECUTE tests |
| **TestDesigner** | Concevoir les cas de test selon les critères d'acceptance | READ code + DoD, WRITE specs de tests |
| **TestExecutor** | Exécuter les tests et collecter les preuves | READ tests, WRITE logs + evidence, EXECUTE CI |
| **DefectTracker** | Tracer les défauts du détection à la résolution | READ tout, WRITE BACKLOG.md + rapports |

---

## Gates spécialisés ASEF-QA

### G3 — Code conforme (hérité + spécialisation)
**Critères QA additionnels** :
- Coverage ≥ 80% (lignes) sur le code nouveau
- Zéro smell critique (selon outil SAST configuré)
- Conventions de nommage des tests respectées (`test_[action]_[context]`)

### G4 — Tests passés (hérité + spécialisation)
**Critères QA additionnels** :
- Zéro test rouge (bloquant absolu)
- Zéro test flaky non documenté
- Rapport d'exécution présent dans `docs/evidence/[slug]/logs/`
- Tests d'intégration passés si modification d'interface publique

### G5 — Sécurité (hérité + spécialisation)
**Critères QA additionnels** :
- Tests de sécurité exécutés pour les routes authentifiées
- Validation des inputs testée aux limites (boundary testing)

---

## Workflows QA

### WF-QA-REGRESSION
Utilisé après chaque changement de code.
```
Step 1 : Identifier la zone d'impact (quels modules affectés)
Step 2 : Exécuter les tests unitaires de la zone (G4)
Step 3 : Exécuter les tests d'intégration si interface publique modifiée
Step 4 : Produire le rapport dans docs/evidence/
Step 5 : Gate G4 évalué par QA-Lead
```

### WF-QA-ACCEPTANCE
Utilisé avant toute livraison.
```
Step 1 : Vérifier que les critères d'acceptance du DoD sont testés
Step 2 : Exécuter la suite complète
Step 3 : Évaluer les gates G3 + G4 + G5
Step 4 : Produire l'evidence package complet
Step 5 : QA-Lead valide ou déclenche HITL si blocage
```

---

## Preuves QA attendues

| Preuve | Type | Emplacement |
|---|---|---|
| Rapport test runner | LOG | `logs/test-results-[date].txt` |
| Rapport coverage | REPORT | `reports/coverage-[date].html` |
| Rapport SAST | REPORT | `reports/sast-[date].json` |
| Logs d'intégration | LOG | `logs/integration-[date].txt` |

---

## Liens

- Héritage gates : [core/ASEF-Gates.md](../../core/ASEF-Gates.md)
- Evidence : [core/ASEF-Evidence.md](../../core/ASEF-Evidence.md)
- Risk : [core/ASEF-Risk.md](../../core/ASEF-Risk.md)
- Playbook evidence : [playbooks/produce-evidence-package.md](../../playbooks/produce-evidence-package.md)
